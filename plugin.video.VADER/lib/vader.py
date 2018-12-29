import copy
import datetime
import hashlib
# import json
import os
import random
import re
import shutil
import sys
import time
import traceback
import urllib2
from os import listdir
from os.path import isfile, join
from shutil import copyfile

import requests
import xbmc
import xbmcaddon
import xbmcgui
import base64

import matchcenter
import plugintools
import simplejson as json
import utils
from categorySelectDialog import categorySelectDialog
from unidecode import unidecode

__addon__ = xbmcaddon.Addon()
__author__ = __addon__.getAddonInfo('author')
ADDONNAME = __addon__.getAddonInfo('name')
ADDONID = __addon__.getAddonInfo('id')
__cwd__ = __addon__.getAddonInfo('path')
__version__ = __addon__.getAddonInfo('version')

LOGPATH = xbmc.translatePath('special://logpath')
DATABASEPATH = xbmc.translatePath('special://database')
USERDATAPATH = xbmc.translatePath('special://userdata')
ADDONDATA = xbmc.translatePath(__addon__.getAddonInfo('profile'))
PVRADDONDATA = os.path.join(xbmc.translatePath('special://userdata'), 'addon_data/pvr.iptvsimple')
THUMBPATH = xbmc.translatePath('special://thumbnails')
ADDONLIBPATH = os.path.join(xbmcaddon.Addon(ADDONID).getAddonInfo('path'), 'lib')
ADDONPATH = xbmcaddon.Addon(ADDONID).getAddonInfo('path')
KODIPATH = xbmc.translatePath('special://xbmc')
sys.path.append(ADDONPATH)

TIMEZONE_API_URI = 'https://eliteboxes.net/public/timezone'
USERNAMES = {
    'sctv': 'sctv_',
    'streamsupreme2': 'supreme_',
    'mediacube3': 'mediacube_',
    'clearstreamsreloaded': 'clearstreams_',
    'vsmystreams' : 'vsmystreams_',
    'goglobal' : 'goglobal_',
    'vaderscc' : 'vaderscc_',
}
URL = 'http://{apiEndpoint}/vapi?username={username}&password={password}&serverIp={serverIp}'

blockedUsers = ['beastTrial', 'black', 'coralblair', 'LeeTVbro', 'stopthepop']

sys.path.append(ADDONLIBPATH)

from xml.etree.ElementTree import fromstring, Element, tostring, SubElement

LOGFILE = os.path.join(LOGPATH, 'kodi.log')

jsonExecuteAddon = '{"jsonrpc":"2.0", "method":"Addons.ExecuteAddon", "params": { "wait": false, "addonid": "script.speedtestnet"}, "id":1}'
jsonNotify = '{"jsonrpc":"2.0", "method":"GUI.ShowNotification", "params":{"title":"PVR", "message":"%s","image":""}, "id":1}'
jsonGetPVR = '{"jsonrpc":"2.0", "method":"Settings.GetSettingValue", "params":{"setting":"pvrmanager.enabled"}, "id":1}'
jsonSetPVR = '{"jsonrpc":"2.0", "method":"Settings.SetSettingValue", "params":{"setting":"pvrmanager.enabled", "value":%s},"id":1}'
jsonSetPVR = '{"jsonrpc":"2.0", "method":"Settings.SetSettingValue", "params":{"setting":"pvrmanager.enabled", "value":%s},"id":1}'

jsonUpdateLibrary = '{"jsonrpc":"2.0","method":"VideoLibrary.Scan"}'
jsonUpdateLibraryClean = '{"jsonrpc":"2.0","method":"VideoLibrary.Clean"}'

if sys.version_info >= (2, 7):
    from collections import OrderedDict as _ordereddict
else:
    from ordereddict import OrderedDict as _ordereddict


class vader(object):
    def __init__(self, popup=True, service=False):

        self.popup = popup
        self.session = requests.session()
        self.authString = 'Not Logged In'
        self.is_generating = False
        self.addonID = ADDONID
        self.cachedEpgCat = None
        self.service = service

        self.filter_category_list_id = [26, 35]
        self.filter_category_list_name = ['Live Sports', 'MatchCenter', 'Live Events', 'EPL Events']



        capsUrl = 'http://vaders.tv/vapi?action=getConfig&pluginName={pluginName}'.format(pluginName=ADDONID)
        self.embedded = False
        self.caps = self._fetch('caps', capsUrl, expireTime=172800)
        if self.caps == None:
            caps = {}
            caps['rootCapable'] = False
            caps['embedded'] = False
            caps['apiEndpoint'] = 'vaders.tv'
            caps['vodCapable'] = True
            caps['pvrEnabled'] = False
            caps['MatchCenterName'] = 'MatchCenter'
            caps['TVCatchupName'] = 'TV Catchup'
            caps['MCCatchupName'] = 'MatchCenter Catchup'

        self.embedded = self.caps['embedded']
        self.rootCapable = self.caps['rootCapable']
        self.apiEndpoint = self.caps['apiEndpoint']
        self.vodCapable = self.caps['vodCapable']
        self.pvrEnabled = self.caps['pvrEnabled']
        self.MatchCenterName = self.caps['MatchCenterName']
        self.TVCatchupName = self.caps['TVCatchupName']
        self.MCCatchupName = self.caps['MCCatchupName']
        #
        #
        if self.pvrEnabled == True:
            plugintools.set_setting('enable_pvr', "true")

        if self.embedded == True:
            utils.log('embedded addon detected')
            self.username = plugintools.get_setting('username')
            self.password = plugintools.get_setting('password')
            self.username = self.username_check() + self.username
            if self.username == self.username_check() or self.username == None or self.username == '':
                if self.popup == True:
                    plugintools.open_settings_dialog()
                    self.username = plugintools.get_setting('username')
                    self.username = self.username_check() + self.username
                    self.password = plugintools.get_setting('password')
        else:
            utils.log('regular addon detected')
            self.username = plugintools.get_setting('username')
            self.password = plugintools.get_setting('password')
            self.username = self.username_check() + self.username
            if self.username == self.username_check() or self.username == None or self.username == '':
                if self.popup == True:
                    plugintools.open_settings_dialog()
                    self.username = plugintools.get_setting('username')
                    self.username = self.username_check() + self.username
                    self.password = plugintools.get_setting('password')

        self.enable_kodi_library = plugintools.get_setting('enable_kodi_library')
        self.enable_pvr = plugintools.get_setting("enable_pvr")
        self.mc_timezone_enable = plugintools.get_setting('mc_timezone_enable')
        self.current_offset = plugintools.get_setting('current_offset')

        self.mc_timezone = plugintools.get_setting('mc_timezone')
        self.catchup_length = plugintools.get_setting('catchup_length')
        self.group_by_name = plugintools.get_setting('group_by_name')
        schedule_time = plugintools.get_setting('schedule_time')
        if schedule_time == '02:00':
            hours = str(random.randint(0, 23)).zfill((2))
            minutes = str(random.randint(0, 59)).zfill((2))
            time = hours + ':' + minutes
            plugintools.set_setting('schedule_time', time)


        self.enableAddons()


        self.kodi_version = xbmc.getInfoLabel('System.BuildVersion').split()[0]
        self.kodi_version = self.kodi_version.split('.')[0]

        if int(self.kodi_version) == 16:
            self.stream_format = 'ts'
        if int(self.kodi_version) >= 17:
            if self.inputadaptive_addon != None:
                self.stream_format = 'ts'
            else:
                self.stream_format = 'ts'





        try:
            self.VADER_addon = xbmcaddon.Addon(ADDONID)
            utils.setSetting("pluginmissing", "false")
        except:
            utils.log("Failed to find {addonName} addon".format(addonName=ADDONNAME))
            self.VADER_addon = None
            utils.setSetting("pluginmissing", "true")
            pass
        try:
            self.pvriptvsimple_addon = xbmcaddon.Addon('pvr.iptvsimple')
        except:

            utils.log("Failed to find pvr.iptvsimple addon")
            utils.setSetting("pvrmissing", "true")
            self.pvriptvsimple_addon = None
            pass

        self.base_url = 'http://{apiEndpoint}/player_api.php?username={username}&password={password}'.format(
            username=self.username, password=self.password, apiEndpoint=self.apiEndpoint)
        self.user_info = None
        self.show_categories = plugintools.get_setting('show_categories')

        self.addonNeedsRestart = False

        self.epgMap = None
        if self.username in blockedUsers:
            self.disableVader()
            return

        current_tz = plugintools.get_setting('current_tz')
        if current_tz == 'None' or current_tz == None:
            offset = str(self.get_timezone())
            plugintools.set_setting('current_tz', offset)

        self.authString = self.authorise()
        if self.authString == "Active":
            if self.service == True:
                self.get_epg_categories()
                # self.set_enabled_categories()

    def startMCC(self):
        self.mcc = matchcenter.matchcenter()
        self.mcc.run()

    def get_auth_status(self):
        return self.authString


    def getVapiAllEpisodes(self):
        epList = []
        showNames = self.getVapiShowNames('1')['results']
        for show in showNames:
            id = show['id']
            time.sleep(1)
            episodes = self.getVapiShowEpisodes(str(id))
            epList.append(episodes)

        dict = {}
        dict['results'] = epList
        return dict


    def getVapiRecentVOD(self, type):
        url = 'http://vapi.vaders.tv/vod/streams/recent?username={username}&password={password}&pageSize=200'.format(username=self.username, password=self.password)
        response = self._fetch(action='getVapiRecentVOD', base_url=url, od=True)
        # sortedList = sorted(response[type], key=lambda k: k['added'], reverse=True)
        return response[type]


    def getVapiShowEpisodes(self, id):

        url = 'http://vapi.vaders.tv/vod/streams/tv/{id}?page=1&username={username}&password={password}'.format(username=self.username, password=self.password, id=id)
        response = requests.get(url).json()
        utils.log(url)
        eplist = []
        for episode in response:
            try:
                episodeObj = json.loads(episode)
                eplist.append(episodeObj)

            except:
                utils.log('failed to parse ' + str(episode) + '  ::: ' + str(response))
                pass

        sortedList = sorted(eplist, key=lambda k: (k['season'], k['episode']))

        return sortedList

    def getVapiShowNames(self, page):
        page = str(page)
        url = 'http://vapi.vaders.tv/vod/streams/tv?page={page}&username={username}&password={password}&pageSize=3000&sortField=showName&ascending=true'.format(page=page, username=self.username, password=self.password)

        utils.log(url)
        response = requests.get(url).json()
        return response

    def getVapiMovies(self, page):
        page = str(page)
        url = 'http://vapi.vaders.tv/vod/streams/movie?page={page}&username={username}&password={password}&pageSize=3000&sortField=title&ascending=true'.format(page=page, username=self.username, password=self.password)
        response = self._fetch(action='getVapiMovies-page-' + page, base_url=url, od=True)
        utils.log(url)
        return response


    def getWebVodEpisodes(self, type, chanName, showName):

        url = 'http://{apiEndpoint}/vapi?action=getParsedData&username={username}&password={password}&parsedKey={type}&chanName={chanName}&showName={showName}&parsedAction=getEpisodes'.format(type=type, apiEndpoint=self.apiEndpoint,
                                                                                                                             username=self.username, password=self.password, chanName=chanName, showName=showName)
        response = self._fetch(action='getParsedData-' + type + '-getEpisodes', base_url=url, od=True)
        return response



    def getWebVodMediaLinks(self, type, chanName, showName, episodeName):

        url = 'http://{apiEndpoint}/vapi?action=getParsedData&username={username}&password={password}&parsedKey={type}&episodeName={episodeName}&chanName={chanName}&showName={showName}&parsedAction=getMediaLinks'.format(type=type, apiEndpoint=self.apiEndpoint,
                                                                                                                             username=self.username, password=self.password, episodeName=episodeName, chanName=chanName, showName=showName)
        response = self._fetch(action='getParsedData-' + type + showName + episodeName +'-getMediaLinks', base_url=url, od=True)
        return response


    def getWebVodEpisodes(self, type, chanName, showName):

        url = 'http://{apiEndpoint}/vapi?action=getParsedData&username={username}&password={password}&parsedKey={type}&chanName={chanName}&showName={showName}&parsedAction=getEpisodes'.format(type=type, apiEndpoint=self.apiEndpoint,
                                                                                                                             username=self.username, password=self.password, chanName=chanName, showName=showName)


        response = self._fetch(action='getParsedData-' + type + showName + '-getEpisodes', base_url=url, od=True)
        return response

    def getWebVodShowNames(self, type, chanName):

        url = 'http://{apiEndpoint}/vapi?action=getParsedData&username={username}&password={password}&parsedKey={type}&chanName={chanName}&parsedAction=getShows'.format(type=type, apiEndpoint=self.apiEndpoint,
                                                                                                                             username=self.username, password=self.password, chanName=chanName)

        response = self._fetch(action='getParsedData-' + type + chanName + '-getShows', base_url=url, od=True)
        return response


    def getWebVodChanNames(self, type):

        url = 'http://{apiEndpoint}/vapi?action=getParsedData&username={username}&password={password}&parsedKey={type}&parsedAction=getChans'.format(type=type, apiEndpoint=self.apiEndpoint,
                                                                                                                 username=self.username, password=self.password)
        response = self._fetch(action='getParsedData-' + type + '-getChans', base_url=url, od=True)
        return response

    def disableVader(self):

        self.checkAndUpdatePVRIPTVSetting("m3uUrl", 'hello.com')

        json = '{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","params":{"addonid":"%s","enabled":false},"id":1}' % ADDONID
        result = xbmc.executeJSONRPC(json)

    def averageList(self, lst):
        utils.LOG(repr(lst))
        avg_ping = 0
        avg_ping_cnt = 0
        for p in lst:
            try:
                avg_ping += float(p)
                avg_ping_cnt += 1
            except:
                utils.LOG("Couldn't convert %s to float" % repr(p))
        return avg_ping / avg_ping_cnt

    def testServers(self, update_settings=True):

        servers = self.get_servers()


        import re, subprocess
        res = None
        ping = False
        with utils.xbmcDialogProgress('Testing servers...') as prog:
            i = 0
            for server in servers:
                serverName = server['server_name']
                serverIp = server['server_ip']

                i = i + 1
                if not prog.update(int((100.0 / len(servers)) * i), 'Testing servers...', '', serverName):
                    return
                ping_results = False
                try:
                    if xbmc.getCondVisibility('system.platform.windows'):
                        p = subprocess.Popen(["ping", "-n", "4", serverIp], stdout=subprocess.PIPE,
                                             stderr=subprocess.PIPE, shell=True)
                    else:
                        p = subprocess.Popen(["ping", "-c", "4", serverIp], stdout=subprocess.PIPE,
                                             stderr=subprocess.PIPE)
                    ping_results = re.compile("time=(.*?)ms").findall(p.communicate()[0])
                except:
                    utils.LOG("Platform doesn't support ping. Disable auto server selection")
                    utils.setSetting("auto_server", False)
                    return None

                if ping_results:
                    utils.LOG("Server %s - %s: n%s" % (i, serverIp, repr(ping_results)))
                    avg_ping = self.averageList(ping_results)
                    if avg_ping != 0:
                        if avg_ping < ping or not ping:
                            res = server
                            ping = avg_ping

                    else:
                        utils.LOG("Couldn't get ping")

        if res != None:
            xbmcgui.Dialog().ok('Done', 'Server with lowest ping ({0}) setting your server to:'.format(ping), '',
                                res['server_name'])

            #http://vapi.vaders.tv/user/server?action=serverChange&username=xxx&password=xxx&serverIp=185.59.222.88
            url = 'http://vapi.vaders.tv/user/server?action=serverChange&username={username}&password={password}&serverIp={serverIp}'.format(
                username=self.username, password=self.password, serverIp=res['server_ip'])


            utils.LOG(url)
            self.session.get(url)

    def send_log(self):

        logfilePath = LOGFILE
        iptv_settings_path = os.path.join(PVRADDONDATA, 'settings.xml')
        vader_settings_path = os.path.join(ADDONDATA, 'settings.xml')
        if '.spmc' in logfilePath:
            logfilePath = logfilePath.replace('kodi.log', 'spmc.log')

        if os.path.exists(logfilePath):
            kodi_logfile = open(logfilePath, 'r').read()
        else:
            kodi_logfile = 'No kodi_logfile'

        if os.path.exists(iptv_settings_path):
            iptv_settings = open(iptv_settings_path, 'r').read()
        else:
            iptv_settings = 'No iptv_settings'

        if os.path.exists(vader_settings_path):
            vader_settings = open(vader_settings_path, 'r').read()
        else:
            vader_settings = 'No vader settings'

        file = kodi_logfile + ' ---- \n' + ' ---- \n' + ' ---- \n' + iptv_settings + ' ---- \n' + ' ---- \n' + ' ---- \n' + vader_settings
        data = {'logfile': file, 'username': self.username}
        url = 'http://' + self.apiEndpoint + '/submitLog'
        self.session.post(url, data=data)



    def addVideoFoldersToSource(self):

        utils.log('adding files to sources.xml addVideoFoldersToSource')
        sourcesPath = USERDATAPATH + '/sources.xml'

        streamMap = {'movies': 53,
                     'tvshows': 55}

        if os.path.exists(sourcesPath):
            with open(USERDATAPATH + '/sources.xml', 'r') as file:
                sourcesXML = file.read()
                root = fromstring(sourcesXML)

            for folder in streamMap:
                utils.log('adding video folder source :' + folder)
                video = root.find('video')
                utils.log('found video tag in sources xml')
                source = SubElement(video, 'source')
                name = SubElement(source, 'name')
                name.text = 'Vader ' + folder

                path = SubElement(source, 'path')
                path.text = os.path.join(ADDONDATA, folder)

                sharing = SubElement(source, 'allowsharing')
                sharing.text = 'true'




        else:
            root = Element('sources')
            video = SubElement(root, 'video')

            for folder in streamMap:
                utils.log('adding video folder source :' + folder)
                utils.log('found video tag in sources xml')
                source = SubElement(video, 'source')
                name = SubElement(source, 'name')
                name.text = 'Vader ' + folder

                path = SubElement(source, 'path')
                path.text = os.path.join(ADDONDATA, folder)

                sharing = SubElement(source, 'allowsharing')
                sharing.text = 'true'

        with open(USERDATAPATH + '/sources.xml', 'w') as file:
            file.write(str(tostring(root)))
            utils.showNotification('EPG Updater',
                                   'Restart kodi for changes to take affect')



    def serverSetup(self):
        servers = self.get_servers()
        d = utils.xbmcDialogSelect()
        d.addItem('0', 'Let Server Decide')
        d.addItem('-1', 'Detect Best Server')

        for server in servers:
            serverName = server['server_name']
            serverIp = server['server_ip']

            d.addItem(serverIp, serverName)

        selection = d.getResult()
        if selection == '-1':
            self.testServers()

        else:
            #http://vapi.vaders.tv/user/server?action=serverChange&username=xxx&password=xxx&serverIp=185.59.222.88
            url = 'http://vapi.vaders.tv/user/server?action=serverChange&username={username}&password={password}&serverIp={serverIp}'.format(apiEndpoint=self.apiEndpoint,username=self.username
                                                                                                                                      ,password=self.password,serverIp=selection)

            utils.log('changing server to ' + selection)
            requests.get(url)



    def get_epg_for_stream(self, channel_id):

            today = datetime.datetime.utcnow()
            subDays = today - datetime.timedelta(days=5)
            startTime = subDays.strftime("%Y%m%d%H%M%S")

            stopTime = today.strftime("%Y%m%d%H%M%S")


            url = 'http://vapi.vaders.tv/epg/channels/{channel_id}?username={username}&password={password}&start={start}&stop={stop}'.format(username=self.username,
            password=self.password, channel_id=channel_id,stop=stopTime,start=startTime)
            action = 'get_live_streams&channel_id={channel_id}'.format(channel_id=channel_id)
            json = self._fetch(action, base_url=url, od=False, expireTime=3600)
            return json['programs']



    def updatePrefs(self, prefs):
        utils.log('updating prefs')
        url = 'http://vapi.vaders.tv/user/preferences?username={username}&password={password}'.format(username=self.username, password=self.password)
        response = requests.post(url, json=prefs).text

    def categorySetup(self):
        categories = self.get_categories()
        prefs = self.get_prefs()
        bouqMap = self.get_boquets()
        window = categorySelectDialog(ADDONNAME + ' Category Setup', categories, prefs, bouqMap, self)
        window.doModal()
        # Destroy the instance explicitly because
        # underlying xbmcgui classes are not garbage-collected on exit.
        del window
        timeNow = int(time.time())
        # plugintools.set_setting('categorySetupLastOpen', str(timeNow))
        # self.updatePVRSettings()

    def show_tools(self):
        d = utils.xbmcDialogSelect()
        d.addItem('configpvr', 'Configure PVR Guide')

        d.addItem('sendlog', 'Send Logs')
        d.addItem('advsetting', 'Install Advanced Settings')
        d.addItem('keyboard', 'Install Keyboard Settings')
        d.addItem('testservers', 'Auto Detect Best Server')
        d.addItem('serversetup', 'Server Select')
        d.addItem('generatestrm', 'Sync VOD & Clean Library')
        d.addItem('tool_deleteall', '[ADV] Delete ALL Settings')
        d.addItem('tool_deletecache', '[ADV] Delete {addonName} Cache'.format(addonName=ADDONNAME))

        d.addItem('tool_deletethumbs', '[ADV] Delete Thumbnails')
        d.addItem('tool_delete_epgdb', '[ADV] Delete EPG Databases')
        d.addItem('tool_deletedb', '[ADV] Delete ALL Databases')
        d.addItem('tool_test', '[ADV] Test Commnad')


        selection = d.getResult()
        if selection == 'configpvr':
            self.updatePVRSettings()
            utils.showNotification('Vader Tools',
                                   'Configuring PVR settings')

        if selection == 'sendlog':
            self.send_log()
            utils.showNotification('Vader Tools',
                                   'Log file sent')

        if selection == 'advsetting':
            self.installAdvSettings()
            utils.showNotification('Vader Tools',
                                   'Installed Advanced Settings')

        if selection == 'keyboard':
            self.installKeyboardFile()
            utils.showNotification('Vader Tools',
                                   'Install Keyboard file')

        if selection == 'testservers':
            self.testServers()

        if selection == 'generatestrm':
            plugintools.set_setting('lastAdded', '0')
            self.generate_strm_files(clean=True)

            utils.showNotification('Vader Tools',
                                   'Files generated')

        if selection == 'tool_deletethumbs':
            self.tool_deletethumbs()
            utils.showNotification('Vader Tools',
                                   'Thumbnails deleted - restart kodi')

        if selection == 'tool_deletedb':
            self.tool_deletedb()

            utils.showNotification('Vader Tools',
                                   'Databases deleted - restart kodi')

        if selection == 'tool_delete_epgdb':
            self.tool_delete_epgdb()

        if selection == 'serversetup':
            self.serverSetup()

        if selection == 'tool_test':
            self.get_epg_categories()

        if selection == 'tool_deleteall':
            self.tool_deleteall()


        if selection == 'tool_deletecache':
            self.deleteAllCache()




    def deleteAllCache(self):
        utils.log('deleting cache folder')
        vaderAddonCacheFolder = os.path.join(ADDONDATA, 'cache')


        if os.path.exists(vaderAddonCacheFolder):
            shutil.rmtree(vaderAddonCacheFolder)


        mcCache = os.path.join(ADDONDATA, 'mcData')


        if os.path.exists(mcCache):
            os.remove(mcCache)

    def tool_deleteall(self):
        vaderAddonSettingsFile = os.path.join(ADDONDATA, 'settings.xml')
        vaderAddonCacheFolder = os.path.join(ADDONDATA, 'cache')

        if os.path.exists(vaderAddonSettingsFile):
            os.remove(vaderAddonSettingsFile)

        if os.path.exists(vaderAddonCacheFolder):
            shutil.rmtree(vaderAddonCacheFolder)


        pvrIptvSettingsFile = os.path.join(PVRADDONDATA, 'settings.xml')
        if os.path.exists(pvrIptvSettingsFile):
            os.remove(pvrIptvSettingsFile)

        if xbmcgui.Dialog().yesno(ADDONNAME,
                                  'In Order To Complete The Settings Wipe - We Need To Restart The Application',
                                  'Would You Like To Restart Now?'):
            xbmc.executebuiltin("Quit")
            sys.exit()



    def tool_deletethumbs(self):
        utils.log('deleting thumbnails')
        utils.delete(THUMBPATH, isdir=True)


    def tool_delete_epgdb(self):
        utils.log('deleting epg dbs')
        onlyfiles = [f for f in listdir(DATABASEPATH) if isfile(join(DATABASEPATH, f))]
        for file in onlyfiles:
            if 'epg' in file.lower():
                utils.log('removing ' + file)
                utils.delete(os.path.join(DATABASEPATH, file))
            if 'tv' in file.lower():
                utils.log('removing ' + file)
                utils.delete(os.path.join(DATABASEPATH, file))

            m3ucache = os.path.join(PVRADDONDATA, 'iptv.m3u.cache')
            utils.delete(m3ucache)

        xbmc.executeJSONRPC(jsonSetPVR % "false")
        time.sleep(1)
        xbmc.executeJSONRPC(jsonSetPVR % "true")

    def tool_deletedb(self):
        utils.log('deleting dbs')
        onlyfiles = [f for f in listdir(DATABASEPATH) if isfile(join(DATABASEPATH, f))]
        for file in onlyfiles:
            if 'epg' in file.lower():
                utils.log('removing ' + file)
                utils.delete(os.path.join(DATABASEPATH, file))
            if 'tv' in file.lower():
                utils.log('removing ' + file)
                utils.delete(os.path.join(DATABASEPATH, file))
            if 'videos' in file.lower():
                utils.log('removing ' + file)
                utils.delete(os.path.join(DATABASEPATH, file))

            m3ucache = os.path.join(PVRADDONDATA, 'iptv.m3u.cache')
            utils.delete(m3ucache)

    def installGenresFile(self):

        try:

            origGenreFilePath = os.path.join(xbmc.translatePath('special://home'),
                                             'addons/' + ADDONID + '/' + 'genres.xml')

            genreFilePath = os.path.join(xbmc.translatePath(PVRADDONDATA), 'genres.xml')
            utils.log("Copying...Genres file")
            utils.ensure_dir(genreFilePath)
            copyfile(origGenreFilePath, genreFilePath)

        except Exception as e:
            utils.log("Error copying genre file \n{0}\n{1}".format(e, traceback.format_exc()))
            pass

    def installKeyboardFile(self):
        keyboard_file_path = os.path.join(xbmc.translatePath('special://home'), 'addons/' + ADDONID + '/keyboard.xml')
        if os.path.isfile(keyboard_file_path):
            utils.log("Keyboard file found.  Copying...")
            copyfile(keyboard_file_path, os.path.join(xbmc.translatePath('special://userdata'), 'keymaps/keyboard.xml'))

    def installAdvSettings(self):
        utils.log('deteted version: ' + self.kodi_version)
        if '17' in self.kodi_version:
            adv_file = 'advancedsettings17.xml'
        else:
            adv_file = 'advancedsettings.xml'

        adv_file_path = os.path.join(xbmc.translatePath('special://home'),
                                     'addons/' + ADDONID + '/' + adv_file)
        if os.path.isfile(adv_file_path):
            utils.log("Advanced Settings file found.  Copying...")
            copyfile(adv_file_path, os.path.join(xbmc.translatePath('special://userdata'), 'advancedsettings.xml'))


    def _fetch(self, action, base_url=None, od=True, force=False, expireTime=1800):

        if base_url == None:
            base_url = self.base_url + '&action={action}'
            url = base_url.format(action=action)

        else:
            url = base_url

        try:

            timeNow = time.time()
            cacheFile = action
            cacheFolder = os.path.join(ADDONDATA, 'cache')
            cachePath = os.path.join(cacheFolder, cacheFile)
            utils.ensure_dir(cachePath)
            if force == True:
                if os.path.exists(cachePath):
                    utils.delete(cachePath)

            if os.path.exists(cachePath):
                fileTime = os.path.getmtime(cachePath)
                if timeNow - fileTime > expireTime:
                    utils.log('deleting cache for fetch')
                    utils.delete(cachePath)

                    # utils.log('fetch ' + url)
                    readString = self.session.get(url).text
                    with open(cachePath, 'w') as cacheFp:
                        cacheFp.write(readString)
                else:
                    with open(cachePath, 'r') as cacheFp:
                        readString = cacheFp.read()
                        try:
                            jsonTest = json.loads(readString)
                        except:
                            if self.embedded != True:
                                utils.log('getting from vader api')
                            readString = self.session.get(url, timeout=30).text
                            with open(cachePath, 'w') as cacheFp:
                                cacheFp.write(readString)
            else:
                if self.embedded != True:
                    utils.log('getting from vader api')
                readString = self.session.get(url, timeout=30).text
                utils.ensure_dir(cachePath)
                with open(os.path.normpath(cachePath), 'w') as cacheFp:
                    cacheFp.write(readString)

            if od == False:
                return json.loads(readString)
            else:
                response = readString
                ordered_reponse = json.loads(response, object_pairs_hook=_ordereddict)
                return ordered_reponse

        except Exception as e:
            if self.embedded != True:
                utils.log("Error fetching url \n{0}\n{1}".format(e, traceback.format_exc()))
            pass

    def build_stream_url(self, stream, extension='ts', base='live', pvr=False):

        if pvr == True:
            self.stream_format = 'ts'
        else:
            if int(self.kodi_version) >= 17:
                if self.inputadaptive_addon != None:
                    self.stream_format = 'ts'
                else:
                    self.stream_format = 'ts'


        if self.embedded == True:

            timeNow = time.time()
            diffTime = timeNow % 3600
            tokenTime = timeNow - diffTime
            tokenString = self.username + self.password + str(stream) + str(tokenTime)
            token = hashlib.md5(tokenString).hexdigest()

            chanUrl = 'http://{apiEndpoint}/boxRedir?token={token}&stream={stream}&base={base}&extension={extension}&plugin={plugin}'.format(
                token=token,
                stream=stream,
                base=base,
                apiEndpoint=self.apiEndpoint,
                extension=extension,
                plugin=ADDONID)
            return chanUrl

        else:

            tokenDict = {}
            tokenDict['username'] = self.username
            tokenDict['password'] = self.password
            jsonToken = json.dumps(tokenDict)
            tokens = base64.b64encode(jsonToken)


            if base == 'live':
                chanUrl = 'http://vapi.vaders.tv/play/{streamId}.{extension}?token={token}'.format(extension=self.stream_format,token=tokens, streamId=stream)
                return chanUrl
            else:

                chanUrl = 'http://vapi.vaders.tv/play/vod/{streamId}.{extension}.m3u8?token={token}'.format(extension=extension,token=tokens, streamId=stream)

                return chanUrl

    def deleteCache(self, cachePath):
        if not os.path.exists(cachePath):
            return True
        timeNow = time.time()
        fileTime = os.path.getmtime(cachePath)
        if os.path.exists(cachePath):
            if timeNow - fileTime > 1200:
                utils.log('deleting cache for fetch')
                utils.delete(cachePath)
                return True
        return False

    def writeCache(self, cachePath):
        readString = self.session.get(self.base_url).text
        with open(cachePath, 'w') as cacheFp:
            cacheFp.write(readString)
        return readString

    def getAuth(self):

        try:
            url = 'http://vapi.vaders.tv/vod/user?username={username}&password={password}'.format(
                username=self.username, password=self.password, apiEndpoint=self.apiEndpoint)
            return requests.get(url, timeout=300).json()
        except Exception as e:
            utils.log("Error getting auth \n{0}\n{1}".format(e, traceback.format_exc()))
            return {}

    def username_check(self):
        for i in USERNAMES:
            if i in ADDONID:
                utils.log('Found {0}'.format(i))
                return USERNAMES[i]
        return ''



    def updateUserPass(self):

        if self.embedded == True:

            utils.log('embedded addon detected')
            self.username = plugintools.get_setting('username')
            self.password = plugintools.get_setting('password')
            self.username = self.username_check() + self.username
            if self.username == self.username_check() or self.username == None or self.username == '':
                if self.popup == True:
                    plugintools.open_settings_dialog()
                    self.username = plugintools.get_setting('username')
                    self.username = self.username_check() + self.username
                    self.password = plugintools.get_setting('password')
        else:
            utils.log('regular addon detected')
            self.username = plugintools.get_setting('username')
            self.password = plugintools.get_setting('password')
            self.username = self.username_check() + self.username
            if self.username == self.username_check() or self.username == None or self.username == '':
                if self.popup == True:
                    plugintools.open_settings_dialog()
                    self.username = plugintools.get_setting('username')
                    self.username = self.username_check() + self.username
                    self.password = plugintools.get_setting('password')


    def authorise(self):

        usernameCheck = self.username_check()

        if self.username == self.username_check() or self.username == None or self.username == '':
            utils.log('username not configured, return')
            return 'Not Logged In'

        if self.embedded == False:
            if usernameCheck != '':
                if usernameCheck not in self.username:
                    self.username = usernameCheck + self.username

        try:
            self.user_info = self.getAuth()
            # utils.log('USER INFO: ' + str(self.user_info))
        except Exception as e:
            utils.log("Error loading user info \n{0}\n{1}".format(e, traceback.format_exc()))
            pass

        if self.user_info != None:
            if self.user_info['enabled'] == True:


                if self.user_info['enabled']:
                    return 'Active'
                return 'Disabled'

            else:
                utils.log(str(self.user_info) + ' : ' + self.username + ' : ' + self.password)

                cacheFile = 'auth'
                cacheFolder = os.path.join(ADDONDATA, 'cache/')
                cachePath = os.path.join(cacheFolder, cacheFile)
                utils.log(cachePath)

                if os.path.exists(cachePath):
                    utils.delete(cachePath)

                if self.username != '' or self.username != 'black' or self.username != 'beastTrial' or self.username != 'beast1':
                    self.send_log()

                self.authString = 'Wrong user/pass'
                xbmc.executebuiltin('XBMC.RunAddon(%s)' % ADDONID)
                return 'Wrong user/pass'

    def get_playlink_archive(self, stream_id, playTime, ts, duration='120'):


        tokenDict = {}
        tokenDict['username'] = self.username
        tokenDict['password'] = self.password
        jsonToken = json.dumps(tokenDict)
        tokens = base64.b64encode(jsonToken)

        duration = int(duration) * 60
        utils.log('duration is ' + str(duration))

        #http://vapi.vaders.tv/play/dvr/1521552600/2454.m3u8?token=x==&duration=1800

        url = 'http://vapi.vaders.tv/play/dvr/{ts}/{stream_id}.m3u8?token={token}&duration={duration}'.format(token=tokens, stream_id=stream_id, ts=ts, duration=duration)
        #
        response = self.session.get(url, allow_redirects=False)
        if response.status_code == 302:
            archive_url = response.headers['Location']
            return archive_url
        else:
            return ''




    def get_epg_categories(self):

        self.filter_category_list_name = ['Live Sports', 'MatchCenter', 'Live Events', 'EPL Events']

        if self.cachedEpgCat:
            return self.cachedEpgCat
        else:
            streams = self.get_all_streams()
            categories = self.get_categories()
            if categories == None:
                categories = self.get_categories()
            if categories == None:
                utils.log('failed to fetch categories')
                return
            result = ''
            self.catMap = {}
            for catId in categories:
                self.catMap[catId] = categories[catId]

            utils.log(str(self.catMap))
            for stream in streams:
                add = True
                name = stream['stream_display_name']
                catId = stream['category_id']
                if str(catId) in self.catMap:
                    categoryName = self.catMap[str(catId)]


                    if any(categoryName.lower().strip() == x.lower().strip() for x in self.filter_category_list_name):
                        add = False

                    if add == True:
                        result = result + name + '=' + categoryName + '\n'


            self.cachedEpgCat = result
            return result
    #
    # def set_enabled_categories(self):
    #     return
    #     groups = []
    #     self.enabledGroups = []
    #     categories = self.get_categories()
    #     for category in categories:
    #         for catId in category:
    #             catName = category[catId]
    #             groups.append((catName, catId))
    #
    #     for group in groups:
    #         catSetting = plugintools.get_setting(group[0])
    #         if catSetting == None:
    #             catSetting = False
    #
    #         if catSetting == True:
    #             self.enabledGroups.append(group[1])



    def get_valid_streams(self):
        valid_streams = []
        action = 'valid_streams'
        url = 'http://vapi.vaders.tv/epg/streams?username={username}&password={password}'.format(username=self.username, password=self.password)
        valid_streams = self._fetch(action=action, base_url=url, force=True, od=True)
        return valid_streams


    def get_all_streams(self):
        valid_streams = []
        action = 'valid_streams_epg'
        url = 'http://vapi.vaders.tv/epg/streams?username={username}&password={password}'.format(username=self.username, password=self.password)
        valid_streams = self._fetch(action=action, base_url=url, od=True)
        return valid_streams


    def get_vod_by_pid(self, wanted_pid, lastUpdate=0, force=False):
        returnList = []
        catMap = {}
        categories = self.get_vod_categories()
        for category in categories:
            catMap[category['category_id']] = category['parent_id']

        action = 'getVodStreams'
        url = 'http://{apiEndpoint}/vapi?action=getVodStreams&username={username}&password={password}&lastUpdate={lastUpdate}'.format(apiEndpoint=self.apiEndpoint,username=self.username
                                                                                                                                      ,password=self.password,lastUpdate=lastUpdate)
        jsonObj = self._fetch(action=action, base_url=url, force=force)

        for streamObj in jsonObj:
            try:
                name = streamObj['name']
                added = int(streamObj['added'])
                stream_icon = streamObj['stream_icon']
                category_id = streamObj['category_id']
                stream_id = streamObj['stream_id']
                container_extension = streamObj['container_extension']

                parent_id = catMap[streamObj['category_id']]
                addFlag = False

                if parent_id == wanted_pid:
                    addFlag = True

                if category_id == wanted_pid:
                    addFlag = True

                if addFlag == True:
                    returnMap = {}

                    returnMap['stream_id'] = stream_id
                    returnMap['category_id'] = category_id
                    returnMap['stream_icon'] = stream_icon
                    returnMap['added'] = int(added)
                    returnMap['name'] = name
                    returnMap['container_extension'] = container_extension
                    returnList.append(returnMap)
            except:
                utils.log('failed to parse '+ str(streamObj))
                pass

        return returnList

    def get_category_id_vod(self, category, sort=False):
        utils.log('entering category vod')
        action = 'get_vod_streams&category_id={category}'.format(category=category)
        json = self._fetch(action)

        if sort:
            returnList = []
            for key in json:
                newDict = copy.deepcopy(key)
                returnList.append(newDict)

            returnList = sorted(returnList, key=lambda k: k['name'])
            return returnList

        return json

    def get_category_id_live(self, category, before=1, after=1):
        try:

            today = datetime.datetime.utcnow()
            subDays = today - datetime.timedelta(hours=before)
            startTime = subDays.strftime("%Y%m%d%H%M%S")

            addDays = today + datetime.timedelta(hours=after)
            stopTime = addDays.strftime("%Y%m%d%H%M%S")


            url = 'http://vapi.vaders.tv/epg/channels?username={username}&password={password}&category_id={category}&start={start}&stop={stop}'.format(username=self.username, start=startTime, stop=stopTime,
            password=self.password, category=category)
            action = 'get_live_streams&category_id={category}'.format(category=category)
            json = self._fetch(action, base_url=url, od=False, expireTime=3600)
            return json

        except Exception as e:
            utils.log("Error listing streams \n{0}\n{1}".format(e, traceback.format_exc()))
            pass

    def get_vod_categories(self, sort=False):
        action = 'get_vod_categories'
        json = self._fetch(action, od=False)
        # utils.log(str(json))
        if sort:
            returnList = []
            for key in json:
                newDict = copy.deepcopy(key)
                returnList.append(newDict)

            returnList = sorted(returnList, key=lambda k: k['category_name'])
            # utils.natural_sort(returnList, key=lambda c: c.tvg_name)

            return returnList

        return json


    def get_servers(self):
        action = 'get_servers'
        #vapi.vaders.tv/user/server?action=
        url = 'http://vapi.vaders.tv/user/server?action=getServers&username={username}&password={password}'.format(
            username=self.username, password=self.password, apiEndpoint=self.apiEndpoint)
        json = self._fetch(action, base_url=url, expireTime=172800)
        # sortedList = sorted(json, key=lambda x: x.items()[0][1])
        sortedList = sorted(json)

        return sortedList

    def get_vod_search(self, search, category):

        action = 'get_vod_search'
        url = 'http://{apiEndpoint}/vapi?username={username}&password={password}&action=getVodStreams&vodAction=search&vodSearch={search}&vodCategory={category}'.format(
            username=self.username, password=self.password, apiEndpoint=self.apiEndpoint, search=search, category=category)

        utils.log(url)

        json = self._fetch(action, base_url=url, expireTime=0)
        return json

    def get_vod_years(self):

        action = 'get_vod_years'
        url = 'http://{apiEndpoint}/vapi?username={username}&password={password}&action=getVodStreams&vodAction=getYears'.format(
            username=self.username, password=self.password, apiEndpoint=self.apiEndpoint)

        utils.log(url)

        json = self._fetch(action, base_url=url, expireTime=172800)
        return json


    def get_prefs(self):
        action = 'get_prefs'
        url = 'http://vapi.vaders.tv/user/preferences?username={username}&password={password}'.format(
            username=self.username, password=self.password)

        utils.log(url)
        json = self._fetch(action, base_url=url, expireTime=0, force=True)
        # sortedList = sorted(json, key=lambda x: x.items()[0][1])
        # sortedList = sorted(json)

        return json

    def get_boquets(self):
        action = 'get_live_categories'
        url = 'http://vapi.vaders.tv/xc/bouquets?username={username}&password={password}'.format(username=self.username, password=self.password)

        json = self._fetch(action, base_url=url, expireTime=0)
        # sortedList = sorted(json, key=lambda x: x.items()[0][1])
        # sortedList = sorted(json)

        return json

    def get_categories(self):
        action = 'get_live_categories'
        url = 'http://vapi.vaders.tv/epg/categories?username={username}&password={password}'.format(username=self.username, password=self.password)

        json = self._fetch(action, base_url=url, expireTime=0)
        # sortedList = sorted(json, key=lambda x: x.items()[0][1])
        # sortedList = sorted(json)

        return json

    def enableAddons(self):
        json = '{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","params":{"addonid":"pvr.iptvsimple","enabled":true},"id":1}'
        result = xbmc.executeJSONRPC(json)
        json = '{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","params":{"addonid":"inputstream.adaptive","enabled":true},"id":1}'
        result = xbmc.executeJSONRPC(json)

        json = '{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","params":{"addonid":"pvr.demo","enabled":false},"id":1}'
        result = xbmc.executeJSONRPC(json)

        try:
            self.pvriptvsimple_addon = xbmcaddon.Addon('pvr.iptvsimple')
        except:
            utils.log("Failed to find pvr.iptvsimple addon")
            self.pvriptvsimple_addon = None

        try:
          self.inputadaptive_addon = xbmcaddon.Addon('inputstream.adaptive')

        except Exception:
          utils.log("Failed to find input adaptive addon")
          self.inputadaptive_addon = None

    def restartAddon(self):
        utils.log("restarting addon")

        json = '{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","params":{"addonid":"pvr.iptvsimple","enabled":"toggle"},"id":1}'
        result = xbmc.executeJSONRPC(json)
        xbmc.sleep(10000)
        json = '{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","params":{"addonid":"pvr.iptvsimple","enabled":true},"id":1}'
        result = xbmc.executeJSONRPC(json)

        try:
            self.pvriptvsimple_addon = xbmcaddon.Addon('pvr.iptvsimple')
        except:
            utils.log("Failed to find pvr.iptvsimple addon")
            self.pvriptvsimple_addon = None

    def checkAndUpdatePVRIPTVSetting(self, setting, value):
        oldSetting = self.pvriptvsimple_addon.getSetting(setting)
        if oldSetting != value:
            self.pvriptvsimple_addon.setSetting(setting, value)
            self.addonNeedsRestart = True

            # PVRDATA = xbmc.translatePath(self.pvriptvsimple_addon.getAddonInfo('profile'))


            # pvrSettingsXml = os.path.join(PVRDATA, 'settings.xml')
            # if os.path.exists(pvrSettingsXml):
            #     with open(pvrSettingsXml, 'r') as readFile:
            #         pvrSettingsXmlData = readFile.read()
            #         root = fromstring(pvrSettingsXmlData)
            #         settingNode = root.findall(".//setting[@id='"+ setting     +"']")
            #         settingNode[0].attrib['value']  = value
            #         fileWrite = str(tostring(root))
            #
            #     with open(pvrSettingsXml, 'w') as writeFile:
            #         writeFile.write(fileWrite)
            #
            #
            #
            # else:
            #     utils.log('pvr settings file does not exist')
            #     self.pvriptvsimple_addon.setSetting(setting, value)

    def downloadEpg(self):
        epgFileName = 'p2.xml.gz'
        epgFile = None
        epgFilePath = os.path.join(ADDONDATA, 'VADER_xmltv.xml.gz')
        if not os.path.exists(epgFilePath):

            try:
                response = urllib2.urlopen('http://repo.vaders.tv/'+epgFileName)
                epgFile = response.read()
            except Exception as e:
                utils.log('StalkerSettings: Some issue with epg file')
                utils.log('{0}\n{1}'.format(e, traceback.format_exc()))


            if epgFile:
                epgFH = open(epgFilePath, "wb")
                epgFH.write(epgFile)
                epgFH.close()

    def updatePVRSettings(self):
        utils.log('updating pvr settings')
        advFile = os.path.join(xbmc.translatePath('special://userdata'), 'advancedsettings.xml')
        genreFile = os.path.join(xbmc.translatePath(PVRADDONDATA), 'genres.xml')


        if os.path.exists(advFile) == False:
            self.installAdvSettings()

        if self.pvriptvsimple_addon != None:

            groups = []
            filtergroup = []

            # categories = self.get_categories()
            # for category in categories:
            #     for catId in category:
            #         catName = category[catId]
            #         groups.append(catName)
            #
            # for group in groups:
            #     catSetting = plugintools.get_setting(group)
            #     if catSetting == None:
            #         catSetting = False
            #
            #     if catSetting != True:
            #         filtergroup.append(group)

            sort_alpha = plugintools.get_setting('sort_alpha')



            if self.embedded == True:
                m3uPath = 'http://{apiEndpoint}/vget?format={format}&type=plugin&pluginName={pluginName}'.format(
                    format='m3u8', pluginName=ADDONID, apiEndpoint=self.apiEndpoint)

            else:
                m3uPath = 'http://{apiEndpoint}/vget?username={username}&password={password}&format={format}&type=plugin&pluginName={pluginName}'.format(
                    username=self.username,
                    password=self.password, format='m3u8', pluginName=ADDONID,
                    apiEndpoint=self.apiEndpoint)

            if sort_alpha:
                m3uPath = m3uPath + '&sort=alpha'

            updater_path = os.path.join(xbmc.translatePath('special://userdata'), 'addon_data/' + ADDONID + '')


            offset = str(self.current_offset)
            if self.current_offset == '-1000':
                if '16' in self.kodi_version or '15' in self.kodi_version:
                    offset = self.get_timezone()
                    plugintools.set_setting('current_offset', str(offset))
                    utils.log('Using API timezone of {0}'.format(str(offset)))
                if '17' in self.kodi_version:
                    # TODO: Figure out needs for offsets on Krypton
                    offset = 0
            if self.mc_timezone_enable == True:
                offset = self.mc_timezone


            timeNow = int(time.time())
            categorySetupLastOpen = int(plugintools.get_setting('categorySetupLastOpen'))
            categorySetupLastSet = int(plugintools.get_setting('categorySetupLastSet'))

            self.checkAndUpdatePVRIPTVSetting("epgCache", "false")
            self.checkAndUpdatePVRIPTVSetting("epgPathType", "0")
            self.checkAndUpdatePVRIPTVSetting("epgPath", os.path.join(updater_path + '/VADER_xmltv.xml.gz'))
            self.checkAndUpdatePVRIPTVSetting("m3uPathType", "1")
            self.checkAndUpdatePVRIPTVSetting('epgTimeShift', str(offset))
            self.checkAndUpdatePVRIPTVSetting('epgTSOverride', 'true')
            self.checkAndUpdatePVRIPTVSetting('logoFromEpg', '2')
            self.checkAndUpdatePVRIPTVSetting("m3uPath", '')
            self.checkAndUpdatePVRIPTVSetting("m3uUrl", m3uPath)

            self.checkAndUpdatePVRIPTVSetting("m3uCache", 'false')


            if self.addonNeedsRestart:

                self.downloadEpg()
                # xbmc.executeJSONRPC(jsonNotify % "Configuring PVR & Guide")
                # xbmc.sleep(10000)
                # self.downloadEpg()

                # self.restartAddon()
                # xbmc.sleep(5000)
                # PVR = json.loads(xbmc.executeJSONRPC(jsonGetPVR))['result']['value']
                # xbmc.executeJSONRPC(jsonNotify % "Live TV Enabled, Restart Kodi")
                # xbmc.executeJSONRPC(jsonSetPVR % "false")
                # xbmc.executebuiltin('PVR.StartManager')
                #
                # xbmc.sleep(1000)
                #
                #
                #
                #
                #
                #
                # # xbmc.sleep(500)
                # xbmc.executeJSONRPC(jsonSetPVR % "true")
                #
                # # xbmc.executebuiltin('XBMC.StartPVRManager')
                # utils.log("restarting pvr complete")




                if os.path.exists(genreFile) == False:
                    self.installGenresFile()

                if xbmcgui.Dialog().yesno(ADDONNAME,
                                          'In Order To Complete The Installation We Need To Restart The Application',
                                          'Would You Like To Restart Now?'):
                    xbmc.executebuiltin("Quit")
                    sys.exit()

                if self.embedded == True and self.rootCapable == True:
                    if xbmcgui.Dialog().yesno(ADDONNAME,
                                              'In Order To Complete The Installation We Need To Restart The Application',
                                              'Would You Like To Restart Now?'):
                        if 'spmc' in KODIPATH:
                            os.system(
                                'nohup echo "killall com.semperpax.spmc16 && sleep 1 && am start com.semperpax.spmc16/.Splash" | su')
                        else:
                            os.system(
                                'nohup echo "killall org.xbmc.kodi && sleep 1 && am start org.xbmc.kodi/.Splash" | su')



        else:
            if plugintools.get_setting('warning_msg') != True:
                xbmcgui.Dialog().ok(ADDONNAME, 'Looks like you are missing some important functions inside Kodi.',
                                    'This can happen when you are using a preinstalled version of Kodi. The Guide functionality will not work until this is done',
                                    'Install Kodi or SPMC from the Play Store or kodi.tv, to fix this')
                plugintools.set_setting('warning_msg', 'true')

    def clean_streams(self, streamMap):
        for folder in streamMap:
            path = os.path.join(ADDONPATH, folder)
            if os.path.exists(path):
                shutil.rmtree(path)

        for folder in streamMap:
            path = os.path.join(ADDONDATA, folder)
            if os.path.exists(path):
                shutil.rmtree(path)

    def write_stream_data(self, folder, stream, lastUpdated, lastAdded):
        stream_id = stream['vodItemId']
        icon = stream['poster']
        extension = stream['ext']
        category = stream['category']
        added = stream['added']
        if added > lastAdded:
            if added > lastUpdated:
                lastUpdated = added

            chanUrl = self.build_stream_url(stream_id, extension=extension, base='movie')

            if folder == 'tvshows':
                    name = stream['showName']
                    showName = name
                    stream_id = stream['vodItemId']
                    season = stream['season']
                    episode = stream['episode']
                    title = stream['title']
                    ext = stream['ext']
                    cat = stream['category']
                    fileName = '{showName} - {season}x{episode}'.format(showName=showName, season=season, episode=episode)

                    strmFilePath = os.path.join(ADDONDATA, folder, showName, fileName + '.strm')
                    chanData = 'plugin://' + ADDONID + '/play/tv/{cat}/{id}/{ext}/{show}/{season}/{episode}'.format(
                        show=name, season=season, episode=episode, cat=category,id=stream_id, ext=extension)
            else:
                name = stream['title']
                strmFile = folder + '/' + name + '.strm'
                strmFile = unidecode(strmFile)
                strmFilePath = os.path.join(ADDONDATA, strmFile)
                chanData = 'plugin://' + ADDONID + '/play/movie/{cat}/{id}/{ext}/{title}'.format(cat=category, title=name, id=stream_id, ext=extension)

            try:
                utils.ensure_dir(strmFilePath)
                with open(strmFilePath, "w") as strmFp:
                    utils.log('creating file {fileName}'.format(fileName=strmFilePath))
                    strmFp.write(chanData)
            except Exception as e:
                utils.log("enable to create file \n{0}\n{1}".format(e, traceback.format_exc()))
                pass

        return lastUpdated

    def add_file_sources(self, streamMap):
        utils.log('add files to sources.xml')
        sourcesPath = USERDATAPATH + '/sources.xml'

        if os.path.exists(sourcesPath):
            write_file = False
            with open(USERDATAPATH + '/sources.xml', 'r') as file:
                sourcesXML = file.read()
                root = fromstring(sourcesXML)
                allNames = root.findall(".//path")
                utils.log('did sources query')
                for folder in streamMap:
                    for pathxml in allNames:
                        path = os.path.join(ADDONPATH, folder)

                        if pathxml.text == path:
                            write_file = True
                            utils.log('found old path')
                            pathxml.text = os.path.join(ADDONDATA, folder)

            if write_file == True:
                with open(USERDATAPATH + '/sources.xml', 'w') as file:
                    file.write(str(tostring(root)))


        else:
            self.addVideoFoldersToSource()

        if os.path.exists(sourcesPath):
            write_file = True
            with open(USERDATAPATH + '/sources.xml', 'r') as file:
                sourcesXML = file.read()
                root = fromstring(sourcesXML)
                allNames = root.findall(".//path")
                utils.log('did sources query')
                for folder in streamMap:
                    for pathxml in allNames:
                        path = os.path.join(ADDONDATA, folder)
                        if pathxml.text == path:
                            write_file = False

            if write_file == True:
                utils.log('adding video folder')
                self.addVideoFoldersToSource()

    def generate_strm_files(self, clean=False):

        force = False
        # If we are already generating, exit.
        if self.is_generating:
            utils.log('currently generating vod files, quitting')
            return

        if self.enable_kodi_library == False:
            utils.log('kodi library integration is disabled')
            return

        dialog = xbmcgui.DialogProgressBG()

        dialog.create('VOD Updater', 'Updating VOD...')
        utils.log('generating strm files clean is set to :' + str(clean))


        self.is_generating = True
        vodVersion = float(plugintools.get_setting('vodVersion'))
        if vodVersion < 6:
            utils.log('CLEAN VOD LIBRARY, VERSION INCREASE')
            clean = True
            plugintools.set_setting('vodVersion', '6')

        try:
            lastAdded = int(plugintools.get_setting('lastAdded'))
            lastUpdated = 0

            streamMap = {
                'movies': 53,
                'tvshows' : 55
            }

            if clean == True or lastAdded == 0:
                self.clean_streams(streamMap)
                force = True

            totalCount = 0
            streams = {}
            i = 0
            for folder in streamMap:
                if folder == 'movies':
                    streams[folder] = self.getVapiMovies('1')
                if folder == 'tvshows':
                    streams[folder] = self.getVapiAllEpisodes()

                totalCount = totalCount + len(streams[folder])

            for folder in streams:
                for streamObj in streams[folder]['results']:
                    if folder == 'tvshows':
                        for stream in streamObj:
                            lastUpdated = self.write_stream_data(folder, stream, lastUpdated, lastAdded)
                            i = i + 1
                            dialog.update(i / totalCount, 'Loading data from server',
                                          'Updating {0}'.format(str(unidecode(stream['title']))))
                    else:
                        stream = streamObj
                        lastUpdated = self.write_stream_data(folder, stream, lastUpdated, lastAdded)
                        i = i + 1
                        dialog.update(i / totalCount, 'Loading data from server',
                        'Updating {0}'.format(str(unidecode(stream['title']))))
            if lastUpdated != 0:
                plugintools.set_setting('lastAdded', str(lastUpdated))

            dialog.close()
            utils.showNotification('VOD Updater',
                                   'Updated VOD from ' + ADDONNAME)

            add_file_source = plugintools.get_setting('enable_filesource')

            if add_file_source == True:
                self.add_file_sources(streamMap)

            xbmc.executeJSONRPC(jsonUpdateLibrary)
            if clean == True or lastAdded == 0:
                xbmc.executeJSONRPC(jsonUpdateLibraryClean)

        except Exception as e:
            utils.log("Error listing streams \n{0}\n{1}".format(e, traceback.format_exc()))
            dialog.close()

            pass

        utils.log('completgenerating strm files')
        dialog.close()
        self.is_generating = False

    def get_timezone(self):
        try:
            request = requests.get(TIMEZONE_API_URI)
            if request.status_code != 200:
                return 0

            resp = request.json()

            if isinstance(resp, dict):
                return resp['timezone']

            return resp.json()['timezone']
        except Exception as e:
            utils.log('Exception getting remote timezone:\n ' + str(e))
            return 0
