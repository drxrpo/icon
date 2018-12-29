import xbmcgui
import xbmc
import plugintools
import traceback
import urllib2
import json
import time
from datetime import datetime
from datetime import date
from datetime import timedelta
import dateutil.parser
from dateutil import tz
from dateutil.tz import tzoffset
import math
import utils
import kodigui
import hashlib
import subprocess
import os
import xbmcaddon
import requests
import vader, xbmcplugin, sys

__addon__ = xbmcaddon.Addon()
__author__ = __addon__.getAddonInfo('author')
ADDONNAME = __addon__.getAddonInfo('name')
ADDONID = __addon__.getAddonInfo('id')
__cwd__ = __addon__.getAddonInfo('path')
__version__ = __addon__.getAddonInfo('version')


LOGPATH  = xbmc.translatePath('special://logpath')
DATABASEPATH = xbmc.translatePath('special://database')
USERDATAPATH = xbmc.translatePath('special://userdata')
ADDONDATA = xbmc.translatePath( __addon__.getAddonInfo('profile') )
PVRADDONDATA = os.path.join(xbmc.translatePath('special://userdata'), 'addon_data/pvr.iptvsimple')
THUMBPATH = xbmc.translatePath('special://thumbnails')
ADDONLIBPATH = os.path.join(xbmcaddon.Addon(ADDONID).getAddonInfo('path'), 'lib')
ADDONPATH = xbmcaddon.Addon(ADDONID).getAddonInfo('path')
KODIPATH = xbmc.translatePath('special://xbmc')

def to_timestamp(t):
    return time.mktime(t.timetuple())



class BaseDialog(xbmcgui.WindowXMLDialog):
    def __init__(self,*args,**kwargs):
        self._closing = False
        self._winID = ''

    def onInit(self):
        self._winID = xbmcgui.getCurrentWindowDialogId()

    def setProperty(self,key,value):
        if self._closing: return
        xbmcgui.Window(self._winID).setProperty(key,value)
        xbmcgui.WindowXMLDialog.setProperty(self,key,value)

    def doClose(self):
        self._closing = True
        self.close()

    def onClosed(self): pass

class BaseWindow(xbmcgui.WindowXML):
    def __init__(self,*args,**kwargs):
        self._closing = False
        self._winID = ''

    def onInit(self):
        self._winID = xbmcgui.getCurrentWindowId()

    def setProperty(self,key,value):
        if self._closing: return
        xbmcgui.Window(self._winID).setProperty(key,value)
        xbmcgui.WindowXMLDialog.setProperty(self,key,value)

    def doClose(self):
        self._closing = True
        self.close()

    def onClosed(self): pass

class MyAddon(BaseWindow):
    def __init__(self,*args,**kwargs):
        """Class constructor"""
        # Call the base class' constructor.
        self.player = xbmc.Player()
        self.eventMap = {}
        self.mcData = None
        self.vader = vader.vader()
        self._closing = False
        self._winID = xbmcgui.getCurrentWindowId()

        self.setWindowProperties()
        BaseWindow.__init__(self,*args,**kwargs)


    def setWindowProperties(self):
        self.setProperty('hide_video_preview', 'true')
        self.setProperty('disable_list_view_preview', 'true')


    def createVersionSelect(self, item):
        d = utils.xbmcDialogSelect()
        versions = item.versions
        for version in versions:
            d.addItem(version['id'], version['name'])

        selection = d.getIndex()
        if selection >= 0:
           self.playfromStream(item, selection)

    def onClick(self,controlID):
        if controlID == 101:
            self.categorySelected()
        elif controlID == 201:
            self.programSelected()

    def onAction(self, action):


        if action.getId() == xbmcgui.ACTION_PREVIOUS_MENU or action.getId() == xbmcgui.ACTION_NAV_BACK:
            # xbmc.executebuiltin("RunPlugin(plugin://plugin.video.VADER/menu)")
            plugintools.set_setting('mcClosedTime', str(int(time.time())))

            self.close()

        #return True


    def onInit(self):
        self.programsList = kodigui.ManagedControlList(self,201,11)
        self.categoryList = self.getControl(101)
        self.catList = []
        try:
            self.mcList()
        except:
            utils.log(traceback.format_exc())
            pass
        try:
            self.fillCategories()
        except:
            utils.log(traceback.format_exc())
            pass


    def fillCategories(self):
        items = []
        item = xbmcgui.ListItem('All')
        # item.setProperty('color', utils.makeColorGif('FFFFFFFF',os.path.join(utils.COLOR_GIF_PATH,'{0}.gif'.format('FFFFFFFF'))))
        items.append(item)

        for epgItem in self.mcData:

            itemCategory = epgItem['category']['name']


            if itemCategory not in self.catList:
                self.catList.append(itemCategory)

        self.catList.sort()
        for c in self.catList:
            if c != '':
                item = xbmcgui.ListItem(c)
                item.setProperty('category',c.strip('- '))
                # item.setProperty('color',self.getGifPath(c))
                items.append(item)
        self.categoryList.reset()
        self.categoryList.addItems(items)


    def playfromStream(self,item, versionIndex):

        version = item.versions[versionIndex]
        chanUrl = self.vader.build_stream_url(version['id'])
        r = requests.get(chanUrl, allow_redirects=False)
        chanUrl = r.headers['Location']
        listitem = xbmcgui.ListItem(path=chanUrl)

        listitem = xbmcgui.ListItem(
            '{title} - {channel}'.format(title=item.getLabel(), channel=version['name'], path=chanUrl)
        )

        if '.mpd' in chanUrl:
            listitem.setProperty('inputstreamaddon', 'inputstream.adaptive')
            listitem.setProperty('inputstream.adaptive.manifest_type', 'mpd')


        # xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)

        self.player.play(chanUrl, listitem)

        xbmc.sleep(1000)
        if not self.player.isPlaying():
            utils.showNotification('Match Center', 'Stream could not be played. Please try again later.')

    def categorySelected(self):
        item = self.categoryList.getSelectedItem()
        if not item:
            return
        cat = item.getProperty('category')
        if not cat:
            self.category = None
        else:
            self.category = cat
        # self.setProperty('category',item.getLabel().strip('- '))
        plugintools.set_setting('mcLastCategory', cat)
        self.showPrograms(cat)

    def showPrograms(self, cat):
        self.setFocusId(201)
        self.mcList(category=cat)

    def programSelected(self):
        item = self.programsList.getSelectedItem()
        if not item:
            return

        if item.versions == None:
            self.playFromEvent(item)
        else:
            versions = item.versions
            if len(versions) <= 1:
                self.playfromStream(item, 0)
            else:
                self.createVersionSelect(item)

    def playFromEvent(self,item):
        url = item.dataSource
        self.player.play(url, item._listItem)

    def getCachedData(self):
        action = 'mcData'
        apiEndpoint = self.vader.apiEndpoint
        username = self.vader.username
        password = self.vader.password
        embedded = self.vader.embedded

        try:
            timeNow = time.time()
            url = 'http://vapi.vaders.tv/mc/schedule?username={username}&password={password}&start={start}&end={end}'.format(
                apiEndpoint=apiEndpoint,
                username=username,
                password=password,
                start=date.today().isoformat(),
                end=date.today() + timedelta(days=2)
            )
            if embedded != True:
                utils.log('attempting to fetch ' + url)
            cacheFile = action
            cachePath = os.path.join(ADDONDATA, cacheFile)
            utils.log(cachePath)
            if os.path.exists(cachePath):
                fileTime = os.path.getmtime(cachePath)
                if timeNow - fileTime > 600:
                    utils.log('deleting cache for fetch')
                    utils.delete(cachePath)

                    readString = requests.get(url, timeout=300).text
                    with open(cachePath, 'w') as cacheFp:
                        cacheFp.write(readString)

                else:
                    utils.log('using cache...')
                    with open(cachePath, 'r') as cacheFp:
                        readString = cacheFp.read()
                        try:
                            jsonTest = json.loads(readString)
                        except:
                            readString = requests.get(url, timeout=300).text
                            with open(cachePath, 'w') as cacheFp:
                                cacheFp.write(readString)


            else:
                readString = requests.get(url, timeout=300).text
                with open(cachePath, 'w') as cacheFp:
                    cacheFp.write(readString)

            return readString


        except Exception as e:
            if embedded != True:
                utils.log("Error fetching url \n{0}\n{1}".format(e, traceback.format_exc()))
            pass

    def totimestamp(self, dt, epoch=datetime(1970, 1, 1)):
        td = dt - epoch
        # return td.total_seconds()
        return (td.microseconds + (td.seconds + td.days * 86400) * 10 ** 6) / 10 ** 6


    def mcList(self, category='all'):
        items = []

        category = plugintools.get_setting('mcLastCategory')
        if category == '' or category == None:
            category = 'all'

        self.programsList.reset()

        apiEndpoint = self.vader.apiEndpoint
        manualOffsetEnabled = plugintools.get_setting("mc_timezone_enable")

        username = self.vader.username
        password = self.vader.password
        embedded = self.vader.embedded
        from_zone = tz.tzutc()
        to_zone = tz.tzlocal()
        if self.mcData == None:
            data = self.getCachedData()
            self.mcData = json.loads(data.decode('utf-8'))

        if manualOffsetEnabled == True:
            offset = float(plugintools.get_setting('mc_timezone'))
        else:
            offset = -1000

        if offset != -1000:
            timeNow = datetime.utcnow().replace(tzinfo=tzoffset('UTC+0', 0)) + timedelta(hours=int(offset))
        else:
            timeNow = datetime.utcnow().replace(tzinfo=tzoffset('UTC+0', 0))
        itemsAdded = 0
        sortedEpg = sorted(self.mcData, key=lambda k: k['startTime'])

        for epgItem in sortedEpg:
            if len(epgItem['streams']) > 0:
                if offset != -1000:

                    startTime = dateutil.parser.parse(epgItem['startTime']) + timedelta(hours=int(offset))
                    endTime = dateutil.parser.parse(epgItem['endTime']) + timedelta(hours=int(offset))
                else:
                    startTime = dateutil.parser.parse(epgItem['startTime'])
                    startTime = startTime.replace(tzinfo=from_zone)
                    startTime = startTime.astimezone(to_zone)

                    endTime = dateutil.parser.parse(epgItem['endTime'])
                    endTime = endTime.replace(tzinfo=from_zone)
                    endTime = endTime.astimezone(to_zone)
                itemCategory = epgItem['category']['name']
                name = epgItem['title']

                if category.lower() in itemCategory.lower() or category.lower() in 'all':
                    startTimeString = startTime.strftime("%a - %H:%M")

                    title = '[COLOR crimson]' + itemCategory + '[/COLOR] ' + epgItem['title']
                    if embedded == True:
                        diffTime = to_timestamp(timeNow) % 3600
                        tokenTime = to_timestamp(timeNow) - diffTime
                        base = 'live'
                        extension = self.vader.stream_format
                        tokenString = username + password + str(epgItem['streams'][0]['id']) + str(tokenTime)
                        token = hashlib.md5(tokenString).hexdigest()
                        chanUrl = 'http://{apiEndpoint}/boxRedir?token={token}&stream={stream}&base={base}&extension={extension}&plugin={plugin}'.format(apiEndpoint=apiEndpoint, token=token, stream=epgItem['streams'][0]['id'],  base=base,extension=extension, plugin=ADDONID)
                    else:
                        tokenDict = {}
                        tokenDict['username'] = username
                        tokenDict['password'] = password
                        jsonToken = json.dumps(tokenDict)
                        import base64
                        tokens = base64.b64encode(jsonToken)
                        chanUrl = 'http://vapi.vaders.tv/play/{streamId}.m3u8?token={token}'.format(token=tokens, streamId=epgItem['streams'][0]['id'])


                    listitem = xbmcgui.ListItem(title, iconImage="DefaultVideo.png")
                    info_labels = {"Title": title, "FileName": title, "Plot": title}
                    listitem.setInfo("video", info_labels)
                    listitem.setProperty('IsPlayable', 'true')

                    item = kodigui.ManagedListItem(title, startTimeString, iconImage=None, data_source=chanUrl,
                                                    versions=epgItem['streams'])

                    endTimeTS = self.totimestamp(endTime.astimezone(from_zone).replace(tzinfo=None))
                    timeNowTS = self.totimestamp(timeNow.astimezone(from_zone).replace(tzinfo=None))
                    startTimeTS = self.totimestamp(startTime.astimezone(from_zone).replace(tzinfo=None))


                    qtex = ''
                    if endTimeTS < timeNowTS:
                        item.setProperty('old','old')

                    elif startTimeTS <= timeNowTS:


                        # prog = ((to_timestamp(timeNow) - to_timestamp(startTime)) / float(to_timestamp(endTime)-to_timestamp(startTime))) * 100
                        prog = ((float(timeNowTS) - float(startTimeTS)) / (float(endTimeTS)- float(startTimeTS))) * 100
                        # 1511760353 - 1511753400 / 1511760600-1511753400
                        # 6953 /7,200
                        prog = int(prog - (prog % 5))

                        tex = 'progress/script-progress_{0}.png'.format(prog)
                        item.setProperty('playing', tex)

                        for version in epgItem['streams']:
                            if '(720p' in version['name'].lower():
                                qtex = 'script-hd_720p.png'
                            elif '(1080i' in version['name'].lower():
                                qtex = 'script-hd_1080i.png'
                            elif '(UHD' in version['name'].lower():
                                qtex = 'script-hd_720p.png'
                    else:
                        item.setProperty('old','old')
                        timeNowTS = self.totimestamp(timeNow.astimezone(from_zone).replace(tzinfo=None))
                        startTimeTS = self.totimestamp(startTime.astimezone(from_zone).replace(tzinfo=None))

                        timeinMins = (startTimeTS - timeNowTS) / 60;
                        timeLabel = 'Starts in {mins} minutes'.format(mins=timeinMins)

                        if timeinMins > 60:
                            timeLabel = 'Starts in {hours} hours'.format(hours=int(math.ceil(timeinMins/60))+1)

                        item.setProperty('startsin', timeLabel)

                    itemsAdded = itemsAdded + 1
                    items.append(item)
                    item.setProperty('quality',qtex)

                    if len(epgItem['streams']) == 1:
                        item.setProperty('duration', epgItem['streams'][0]['name'])

        self.programsList.addItems(items)


        for i in range(len(items)):
            if not items[i].getProperty('old'):
                self.programsList.selectItem(i)
                break


        plugintools.log(str(itemsAdded))
        if itemsAdded == 0:
            plugintools.log('no events for category')
            item = kodigui.ManagedListItem('No Upcoming Events in {category}'.format(category=category), '', iconImage=None, data_source=None,
                                           versions=None)
            self.programsList.addItem(item)

        return True

class matchcenter():
    def __init__(self, ):
        self.window = None
        self.closedTime = 0

    def run(self):
        self.window = MyAddon('script-category.xml', utils.__addon__.getAddonInfo('path'), 'Main', '720p',
                         manager=None)


        self.window.doModal()

        # self.window.onClosed()
        plugintools.set_setting('mcClosedTime' , str(int(time.time())))
        del self.window
        self.window = None
