#########################################################################
#########################################################################
####                                                                 ####
####               Too lazy to figure it out yourself?               ####
####                                                                 ####
#########################################################################
#########################################################################

#       Copyright (C) 2018
#
#  This Program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2, or (at your option)
#  any later version.
#
#  This Progr`am is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with XBMC; see the file COPYING.  If not, write to
#  the Free Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.
#  http://www.gnu.org/copyleft/gpl.htm
#

import xbmc
import xbmcgui

import os

import iptv_utils
import sfile

if iptv_utils.API == 2:
    import iptv2 as iptv
    import browseDialog2 as browseDialog
else:
    import iptv
    import browseDialog


ADDONID   = iptv_utils.ADDONID    
ADDON     = iptv_utils.ADDON
HOME      = iptv_utils.HOME
RESOURCES = iptv_utils.RESOURCES
TITLE     = iptv_utils.TITLE
VERSION   = iptv_utils.VERSION
ICON      = iptv_utils.ICON
FANART    = iptv_utils.FANART
GETTEXT   = iptv_utils.GETTEXT


NULL              = 0
MAIN              = 100
LATEST            = 150
DOWNLOADS         = 175
ACCOUNT           = 200
LIVE              = 300
LIVE_ALL          = 350
VOD               = 400
VOD_ALL           = 425
VOD_TV            = 450
VOD_TV_ALL        = 475
VOD_BOXSETS       = 480
CATCHUP           = 500
FOOTBALL_SCHEDULE = 600
UK_SPORT_LISTS    = 700
SETTINGS          = 800
SPEEDTEST         = 900
IPTV_PVR          = 1000
LAUNCH_PVR        = 1100
DISABLE_PVR       = 1200
INTEGRATION       = 1300

LIVE_CAT       = 2100
VOD_CAT        = 2200
PLAYABLE       = 2300
CREDENTIALS    = 2400
LIVE_SEARCH    = 2500
VOD_SEARCH     = 2600
VOD_TV_SEARCH  = 2650
CATCHUP_CAT    = 2700 
CATCHUP_ALL    = 2725 
CATCHUP_DAY    = 2750 
CATCHUP_SEARCH = 2800  
CATCHUP_PLAY   = 2900  
BROWSE_VOD     = 3000  
DOWNLOADED     = 3100  
DELETE         = 3200

MOVIES  = 100
TVSHOWS = 200


INITIAL_ITEM = 0


SETTINGS = 10000


IMG_LATEST            = None
IMG_DOWNLOADS         = None
IMG_ACCOUNT           = sfile.join(RESOURCES, 'art', 'myacc.png')
IMG_LIVE              = sfile.join(RESOURCES, 'art', 'livetv.png')
IMG_VOD               = sfile.join(RESOURCES, 'art', 'vod.png')
IMG_VOD_TV            = sfile.join(RESOURCES, 'art', 'vod.png')
IMG_CATCHUP           = sfile.join(RESOURCES, 'art', 'catchup.jpg')
IMG_FOOTBALL_SCHEDULE = sfile.join(RESOURCES, 'art', 'football.jpg')
IMG_UK_SPORT_LISTS    = None
IMG_SETTINGS          = sfile.join(RESOURCES, 'art', 'settings.png')
IMG_SPEEDTEST         = sfile.join(RESOURCES, 'art', 'speed.png')
IMG_IPTV_PVR          = None
IMG_LAUNCH_PVR        = sfile.join(RESOURCES, 'art', 'launchpvr.jpg')
IMG_DISABLE_PVR       = sfile.join(RESOURCES, 'art', 'disablepvr.jpg')
IMG_INTEGRATION       = None


global APPLICATION
#global ACCOUNT_INFO

APPLICATION  = None
#ACCOUNT_INFO = None


def initGlobals(application):
    global APPLICATION
    #global ACCOUNT_INFO
    if APPLICATION is None:
        APPLICATION  = application

    #if ACCOUNT_INFO is None:
    #    ACCOUNT_INFO = ''


def GetGlobalMenu():
    menu = []
    menu.append((GETTEXT(31007), '?mode=%d' % SETTINGS))
    return menu


def Main():
    #iptv.MigrateCredentials()
    iptv_utils.CheckVersion()

    menu = GetGlobalMenu()

    try:
        AccountInfo()
    except:
        pass
        

    AddDir(GETTEXT(31014), LATEST,             image=IMG_LATEST,            isFolder=False, contextMenu=menu, desc=GETTEXT(32014))

    AddDir(GETTEXT(31002), LIVE,               image=IMG_LIVE,              isFolder=True,  contextMenu=menu, desc=GETTEXT(32002), fave=True)

    AddDir(GETTEXT(31003), VOD,                image=IMG_VOD,               isFolder=True,  contextMenu=menu, desc=GETTEXT(32003), fave=True)

    AddDir(GETTEXT(31013), VOD_TV,             image=IMG_VOD_TV,            isFolder=True,  contextMenu=menu, desc=GETTEXT(32013), fave=True)

    AddDir(GETTEXT(31016), VOD_BOXSETS,        image=IMG_VOD_TV,            isFolder=True,  contextMenu=menu, desc=GETTEXT(32016), fave=True)

    AddDir(GETTEXT(31004), CATCHUP,            image=IMG_CATCHUP,           isFolder=True,  contextMenu=menu, desc=GETTEXT(32004), fave=True)

    #AddDir(GETTEXT(31005), FOOTBALL_SCHEDULE, image=IMG_FOOTBALL_SCHEDULE, isFolder=False, contextMenu=menu, desc=GETTEXT(32005))

    #AddDir(GETTEXT(31006), UK_SPORT_LISTS,    image=IMG_UK_SPORT_LISTS,    isFolder=True,  contextMenu=menu, desc=GETTEXT(32006))

    AddDir(GETTEXT(31007), SETTINGS,           image=IMG_SETTINGS,          isFolder=False, contextMenu=menu, desc=GETTEXT(32007))

    AddDir(GETTEXT(31008), SPEEDTEST,          image=IMG_SPEEDTEST,         isFolder=False, contextMenu=menu, desc=GETTEXT(32008))

    if xbmc.getCondVisibility('Pvr.HasTVChannels'):
        AddDir(GETTEXT(31010), LAUNCH_PVR,     image=IMG_LAUNCH_PVR,        isFolder=False, contextMenu=menu, desc=GETTEXT(32010))
        AddDir(GETTEXT(31011), DISABLE_PVR,    image=IMG_DISABLE_PVR,       isFolder=True,  contextMenu=menu, desc=GETTEXT(32011))
    else:
        if not xbmcgui.Window(10000).getProperty('PVR_SETUP') == 'true':
            AddDir(GETTEXT(31009), IPTV_PVR,   image=IMG_IPTV_PVR,          isFolder=True,  contextMenu=menu, desc=GETTEXT(32009))

    #AddDir(GETTEXT(31012), INTEGRATION,        image=IMG_INTEGRATION,       isFolder=False, contextMenu=menu, desc=GETTEXT(32012))

    folder = iptv_utils.GetSetting('DOWNLOAD')
    if folder:
        AddDir(GETTEXT(31015), DOWNLOADS,      image=IMG_DOWNLOADS,         isFolder=False, contextMenu=menu, desc=GETTEXT(32015), listID=69)

    if iptv_utils.GetSetting('DEBUG') != 'true':
        AddDir(GETTEXT(31001), ACCOUNT,            image=IMG_ACCOUNT,           isFolder=False, contextMenu=menu, desc=GETTEXT(32001))


def ShowAccountInfo():
    try:    return _ShowAccountInfo()
    except: pass

    try:
        iptv_utils.DialogOK(iptv_utils.GETTEXT(30035))
        iptv_utils.OpenSettings(focus=2.1)

        _ShowAccountInfo()

    except:
        pass


def _ShowAccountInfo():
    info = AccountInfo(0)

    user        = info['username'] 
    status      = info['status'] 
    max_conn    = info['max_connections']
    active_conn = info['active_cons']
    expires     = info['exp_date']

    if expires:
        import datetime
        expires = datetime.datetime.fromtimestamp(int(expires)).strftime('%H:%M %d/%m/%Y')

    user        = '%s: %s'    % (GETTEXT(35001), user)
    status      = '%s'        % (status)
    expires     = '%s: %s'    % (GETTEXT(35003), expires)
    connections = '%s: %s/%s' % (GETTEXT(35005), active_conn, max_conn)

    if status.lower() == 'active':
        status = '[COLOR lime]%s[/COLOR]' % status 
    else:
        status = '[COLOR red]%s[/COLOR]' % status 

    text  = '%s [%s][CR]' % (user, status)
    text += '%s[CR]'      % (expires)
    text += '%s[CR]'      % (connections)

    iptv_utils.DialogOK(text)

        
def AccountInfo(maxSec=86400):
    user        = '' 
    status      = '' 
    max_conn    = 0
    active_conn = 0
    expires     = ''

    try:
        info        = iptv.GetAccountInfo(maxSec=maxSec)['user_info']
        user        = info['username'] 
        status      = info['status'] 
        max_conn    = info['max_connections']
        active_conn = info['active_cons']
        expires     = info['exp_date']
    except:
        pass

    if expires:
        import datetime
        expires = datetime.datetime.fromtimestamp(int(expires)).strftime('%H:%M %d/%m/%Y')

    user        = '%s: %s' % (GETTEXT(35001), user)
    status      = '%s: %s' % (GETTEXT(35002), status)
    expires     = '%s: %s' % (GETTEXT(35003), expires)
    max_conn    = '%s: %s' % (GETTEXT(35004), max_conn)
    active_conn = '%s: %s' % (GETTEXT(35005), active_conn)

    xbmcgui.Window(10000).setProperty('CREDS_USER',        user)
    xbmcgui.Window(10000).setProperty('CREDS_STATUS',      status)
    xbmcgui.Window(10000).setProperty('CREDS_EXPIRES',     expires)
    xbmcgui.Window(10000).setProperty('CREDS_MAX_CONN',    max_conn)
    xbmcgui.Window(10000).setProperty('CREDS_ACTIVE_CONN', active_conn)

    #info = []
    #info.append(user)
    #info.append(status)
    #info.append(expires)
    #info.append(max_conn)
    #info.append(active_conn)
    ##info.append(formats)
    ##info.append(port)

    #global ACCOUNT_INFO
    #ACCOUNT_INFO = '[CR]'.join(info)

    return info


def Live():
    menu = GetGlobalMenu()

    image = IMG_LIVE

    #Search item
    AddDir(GETTEXT(30005), LIVE_SEARCH, 0, image=image, isFolder=True, contextMenu=menu, desc=GETTEXT(30013), listID=79)
    GetCategories(iptv.GetLiveCategories, LIVE_CAT, image=image, type=LIVE)


def LiveAll():
    LiveCategory(0)


def Vod(search=True):
    menu = GetGlobalMenu()

    image = IMG_VOD

    if search:
        AddDir(GETTEXT(30006), VOD_SEARCH, 0, image=image, isFolder=True, contextMenu=menu, desc=GETTEXT(30014), listID=69)

    GetCategories(iptv.GetVODCategories, VOD_CAT, image=image, type=MOVIES)
    #GetCategories(iptv.GetBoxSets,       VOD_CAT, image=image, type=MOVIES)


def VodAll():
    VODCategory(0)


def VodTV(search=True):
    menu = GetGlobalMenu()

    image = IMG_VOD

    if search:
        AddDir(GETTEXT(30006), VOD_TV_SEARCH, 0, image=image, isFolder=True, contextMenu=menu, desc=GETTEXT(30014), listID=69)

    if iptv_utils.API == 2:
        GetCategories(iptv.GetVODSeriesCategories, VOD_CAT, image=image, type=TVSHOWS)
    else:
        GetCategories(iptv.GetVODCategories, VOD_CAT, image=image, type=TVSHOWS)


def VodTVAll():
    VodTV(search=False)


def VodBoxsets():
    image = IMG_VOD

    GetCategories(iptv.GetBoxSets, VOD_CAT, image=image, type=MOVIES)


def GetCategories(func, mode, image=None, desc=None, type=None):
    if iptv_utils.API == 2:
        return GetCategories2(func, mode, image, desc, type)
        
    menu = GetGlobalMenu()

    cats = func()

    for cat in cats:
        category_name = cat['category_name']
        playlist_url  = cat['playlist_url']

        try:    desc = cat['description']
        except: pass

        if category_name.startswith('****') and category_name.endswith('****'):
            continue

        if type == MOVIES:
            if 'type=get_vod_streams' in playlist_url:
                listID     = 69
                isFolder   = False
                AddDir(category_name, mode, playlist_url, image=image, isFolder=isFolder, desc=desc, listID=listID)


        elif type == TVSHOWS:
            # 415 is the Movie boxsets
            if 'type=get_vod_scategories&scat_id=415' not in playlist_url and 'type=get_vod_scategories' in playlist_url:
                listID     = 49
                isFolder   = True
                AddDir(category_name, mode, playlist_url, image=image, isFolder=isFolder, desc=desc, listID=listID)


        elif type == LIVE:
            if 'type=get_live_streams' in playlist_url:
                listID     = 79   # when new list available this will be the ID
                isFolder   = False # when new list available this will False
                AddDir(category_name, mode, playlist_url, image=image, isFolder=isFolder, desc=desc, listID=listID)


def GetCategories2(func, mode, image=None, desc=None, type=None):  
    menu = GetGlobalMenu()

    cats = func()

    for cat in cats:
        category_name = cat['category_name']
        playlist_url  = cat['playlist_url']
        desc          = ''

        if category_name.startswith('****') and category_name.endswith('****'):
            continue

        if type == MOVIES:
            if 'get_vod_streams' in playlist_url:
                listID   = 69
                isFolder = False
                AddDir(category_name, mode, playlist_url, image=image, isFolder=isFolder, contextMenu=menu, desc=desc, listID=listID)


        elif type == TVSHOWS:
            if 'get_series' in playlist_url:
                listID   = 49
                isFolder = True
                AddDir(category_name, mode, playlist_url, image=image, isFolder=isFolder, contextMenu=menu, desc=desc, listID=listID, fave=True)


        elif type == LIVE:
            if 'type=get_live_streams' in playlist_url:
                listID   = 79   # when new list available this will be the ID
                isFolder = False # when new list available this will False
                AddDir(category_name, mode, playlist_url, image=image, isFolder=isFolder, contextMenu=menu, desc=desc, listID=listID)



def VODSubCategory(url, search=None):
    items = iptv.GetSVODCategory(url, search)

    if len(items) == 0:
        if search:
            return False

        Empty(GETTEXT(30009), 'VODCategory(%s, %r)' % (url, search))

    menu = GetGlobalMenu()

    for item in items:
        url   = item['playlist_url']
        image = item['stream_icon']
        desc  = item['description']
        name  = item['category_name']

        AddDir(name, VOD_CAT, url, image=image, isFolder=False, contextMenu=menu, desc=desc, plot=desc, listID=109)

        #this version will unpack all seasons
        #playlist_url = item['playlist_url']
        #VODCategory(playlist_url, search)

    return True


def VODCategory(url, search=None):
    test = str(url)
    if 'get_vod_scategories' in test or 'get_series' in test:
        if '&season_id=' not in test:
            return VODSubCategory(url, search)

    items = iptv.GetVODCategory(url, search)

    AddVODItems(items, search)

    return items


def SearchVODSeries(search):
    #SJP
    cats = iptv.GetVODSeriesCategories(search)

    listID   = 49
    isFolder = True
    mode     = VOD_CAT

    for cat in cats:
        category_name = cat['category_name']
        playlist_url  = cat['playlist_url']

        try:
            info  = iptv.GetSeriesByCategoryID(cat['category_id'])
            desc  = info['plot']
            image = info['cover']      
            AddDir(category_name, mode, playlist_url, image=image, isFolder=isFolder, desc=desc, listID=listID)
        except:
            pass

    return cats


def Latest():
    nmrItems = iptv_utils.GetSetting('RELEASES')
 
    items = iptv.GetVODLatest(nmrItems)

    AddVODItems(items)


def Downloads():
    folder = GetDownloadFolder()

    if not folder:
        Empty('', 'Downloads')

    playable = xbmc.getSupportedMedia('video')
    playable = playable .split('|') 

    def isPlayable(file):
        try:
            file, ext = file.rsplit('.', 1)
            ext = '.%s' % ext.lower()
            return ext in playable
        except:
            return False


    def getMetadata(root, file):
        title    = file.rsplit('.', 1)[0]
        info     = '%s.txt' % title
        filename = os.path.join(root, file)
        info     = os.path.join(root, info)

        try:
            contents = sfile.readlines(info)
            image = contents[0]
            title = contents[1]
            plot  = '\n'.join(contents[2:])
        except Exception as e:
            image    = ''
            plot     = ''

        meta = {}
        meta['title']    = title
        meta['filename'] = filename
        meta['image']    = image
        meta['plot']     = plot

        return meta

    root, folders, files = sfile.walk(folder)

    items = []

    for folder in folders:
        fullname = os.path.join(root, folder)
        locals   = sfile.glob(fullname)
        for local in locals:            
            if isPlayable(local):
                theRoot, file = local.rsplit(os.sep, 1)
                metadata = getMetadata(theRoot, file)

                title    = metadata['title']
                filename = metadata['filename']
                image    = metadata['image']
                plot     = metadata['plot']

                items.append((title, filename, image, plot, fullname))

        
    for file in files:
        if isPlayable(file):
            metadata = getMetadata(root, file)

            title    = metadata['title']
            filename = metadata['filename']
            image    = metadata['image']
            plot     = metadata['plot']

            items.append((title, filename, image, plot, ''))

    items.sort()

    globalMenu = GetGlobalMenu()

    for item in items:
        name   = item[0]
        url    = item[1]
        image  = item[2]
        plot   = item[3]
        folder = item[4]

        menu = []
        menu.append((GETTEXT(30026), '?mode=%d&title=%s&filename=%s&folder=%s' % (DELETE, iptv_utils.qplus(name), iptv_utils.qplus(url), iptv_utils.qplus(folder))))
        menu.extend(globalMenu)

        AddDir(name, DOWNLOADED, url, image=image, isFolder=False, contextMenu=menu, desc=plot, plot=plot, listID=None)


def AddVODItems(items, search=None):
    if len(items) == 0:
        if search:
            return False
        Empty(GETTEXT(30009), 'VODCategory()')

    menu = GetGlobalMenu()

    for item in items:
        name        = item['name']
        stream_type = item['stream_type']
        stream_id   = item['stream_id']
        stream_icon = item['stream_icon']

        try:    desc = item['description']
        except: desc = ''

        try:    container_extension = item['container_extension']
        except: container_extension = 'ts' 

        AddDir(name, BROWSE_VOD, stream_id, container_extension, stream_type, image=stream_icon, isFolder=False, contextMenu=menu, desc=desc, plot=desc, fave=True)

    return True


def VODSearch():
    search = iptv_utils.GetText(GETTEXT(30012))

    if search:
        try:
            if (VODCategory(0, search=search)):
                return
        except:
            pass

    if search:
        iptv_utils.DialogOK(GETTEXT(30008) % search)

    Empty('', 'VODSearch')


def VODTVSearch():
    search = iptv_utils.GetText(GETTEXT(30012))

    if search:
        if SearchVODSeries(search):
            return

    if search:
        iptv_utils.DialogOK(GETTEXT(30008) % search)

    Empty('', 'VODTVSearch')


def LiveCategory(cat, search=None):
    items = iptv.GetLiveCategory(cat, search)

    if len(items) == 0:
        return False

    menu = GetGlobalMenu()

    for item in items:
        name        = item['name']
        stream_type = item['stream_type']
        stream_id   = item['stream_id']
        stream_icon = item['stream_icon']
        now         = item['now']
        next        = item['next']

        try:    container_extension = item['container_extension']
        except: container_extension = 'ts' 

        #desc = '%s[CR][CR]%s' % (now, next)
        desc = now

        infoLabels = {}

        infoLabels['FL_TV_NOW']  = now.split('[CR]')[0].replace('[B]', '').replace('[/B]', '')
        infoLabels['FL_TV_NEXT'] = next.split('[CR]')[0].replace('[B]', '').replace('[/B]', '')
       
        AddDir(name, PLAYABLE, stream_id, container_extension, stream_type, image=stream_icon, isFolder=False, infoLabels=infoLabels, contextMenu=menu, desc=desc, plot=desc, fave=True)

    return True


def LiveSearch():
    search = iptv_utils.GetText(GETTEXT(30012))

    try:
        if search:
            if (LiveCategory(0, search=search)):
                return
    except:
        pass

    if search:
        iptv_utils.DialogOK(GETTEXT(30008) % search)

    Empty('', 'LiveSearch')


def Catchup():
    items = iptv.Catchup()

    if len(items) == 0:
        Empty(GETTEXT(30010), 'Catchup')

    menu = GetGlobalMenu()
    for item in items:
        name                = item['name']
        stream_id           = item['stream_id']
        stream_icon         = item['stream_icon']
        tv_archive_duration = item['tv_archive_duration']

        #AddDir(name, CATCHUP_CAT, stream_id, image=stream_icon, isFolder=False, contextMenu=menu, extra=tv_archive_duration, listID=89)
        AddDir(name, CATCHUP_CAT, stream_id, image=stream_icon, isFolder=True, contextMenu=menu, extra=tv_archive_duration, fave=True)


def CatchupAll():
    Catchup()


def CatchupCat(title, stream_id, tv_archive_duration, image, search=None):
    try:
        stream_id = int(stream_id)
    except:
        Empty(GETTEXT(30010), 'CatchupCat(%s, %s, %s, %s)' % (title, stream_id, tv_archive_duration, image))

    try:
        tv_archive_duration = int(tv_archive_duration)
    except:
        Empty(GETTEXT(30010), 'CatchupCat(%s, %s, %s, %s)' % (title, stream_id, tv_archive_duration, image))

    if search:
        search = iptv_utils.GetText(GETTEXT(30012))

        if not search:
            Empty('', 'CatchupCat')

    items = iptv.CatchupCat(stream_id, tv_archive_duration, search)

    if len(items) == 0:
        if search:
            text = GETTEXT(30008) % search
        else:
            text = GETTEXT(30009)

        Empty(text, 'CatchupCat')

    menu = GetGlobalMenu()

    dates  = []

    for item in items:
        day = item['start'].date()
        if day not in dates:
            dates.append(day)

    dates = dates[::-1]

    for day in dates:
        title = '%s' % (iptv_utils.getDay(day))
        AddDir(title, CATCHUP_DAY, stream_id, image=image, isFolder=False, contextMenu=menu, desc='', plot='', extra='%s*%d' % (day, tv_archive_duration), listID=89)

    # dates  = []
    # starts = []
    #
    # import calendar
    # for item in items:
    #     start = item['start'].date()
    #     if start not in starts:
    #         starts.append(start)
    #         day = calendar.day_name[start.weekday()]
    #         dates.append((str(start), day))
    #
    # for start, day in sorted(dates)[::-1]:
    #     title = '%s %s' % (start, day)
    #     AddDir(title, CATCHUP_DAY, stream_id, image=image, isFolder=False, contextMenu=menu, desc='', plot='', extra='%s*%d' % (start, tv_archive_duration), listID=89)


def CatchupDay(params):
    error = GETTEXT(30009)

    try:    duration = int(params['extra'].split('*', 1)[-1])
    except: duration = 7 #assume 7 days in this case

    try:    
        start = params['extra'].split('*', 1)[0] 
    except:
        Empty(error, 'CatchupDay1')

    try:
        stream_id = params['url']
    except:
        Empty(error, 'CatchupDay2')

    image = params['image'] 

    items = iptv.CatchupCat(stream_id, duration, start)

    if len(items) == 0:
        Empty(error, 'CatchupDay3')

    menu = GetGlobalMenu()

    #Search item
    #if not search:
    #    text = GETTEXT(30011) % title
    #    desc = GETTEXT(30015) % title
    #    AddDir(text, CATCHUP_SEARCH, stream_id, image=image, isFolder=True, contextMenu=menu, desc=desc)

    for item in items:
        title = item['title']
        desc  = item['description']
        start = item['start']
        end   = item['end']

        container_extension = 'ts' 

        title = '%s - %s' % (str(start).split(' ', 1)[-1][:-3], title)
        title = title.strip()

        AddDir(title, CATCHUP_PLAY, stream_id, image=image, isFolder=False, contextMenu=menu, desc=desc, plot=desc, extra='%s*%s' % (start, end), fave=True)


def _CatchupCat(title, stream_id, tv_archive_duration, image, search=None):
    try:
        stream_id = int(stream_id)
    except:
        Empty(GETTEXT(30010), 'CatchupCat(%s, %s, %s, %s)' % (title, stream_id, tv_archive_duration, image))

    try:
        tv_archive_duration = int(tv_archive_duration)
    except:
        Empty(GETTEXT(30010), 'CatchupCat(%s, %s, %s, %s)' % (title, stream_id, tv_archive_duration, image))

    if search:
        search = iptv_utils.GetText(GETTEXT(30012))

        if not search:
            Empty('', 'CatchupCat')

    items = iptv.CatchupCat(stream_id, tv_archive_duration, search)

    if len(items) == 0:
        if search:
            text = GETTEXT(30008) % search
        else:
            text = GETTEXT(30009)

        Empty(text, 'CatchupCat')

    menu = GetGlobalMenu()

    #Search item
    if not search:
        text = GETTEXT(30011) % title
        desc = GETTEXT(30015) % title
        AddDir(text, CATCHUP_SEARCH, stream_id, image=image, isFolder=True, contextMenu=menu, desc=desc)

    for item in items:
        title = item['title']
        desc  = item['description']
        start = item['start']
        end   = item['end']

        container_extension = 'ts' 

        title = '%s - %s' % (str(start), title)

        AddDir(title, CATCHUP_PLAY, stream_id, image=image, isFolder=False, contextMenu=menu, desc=desc, plot=desc, extra='%s*%s' % (start, end))


def SportListings():
    import sport
    results = sport.Listings()

    menu = GetGlobalMenu()

    if len(results) == 0:
        Empty(text=GETTEXT(30016), reason='No Sport Listings')

    for result in results:
        title  = result.get('title')
        desc   = result.get('desc')
        plot   = result.get('plot')
        image  = result.get('image')
        fanart = result.get('fanart')
        AddDir(title, image=image, fanart=fanart, isFolder=False, infoLabels={}, contextMenu=menu, desc=desc, plot=plot)
        
        
def VerifyImages(image, fanart=None):
    if not fanart:
        fanart = image or FANART

    if not image:
        image = ICON
        
    return image, fanart


def InitListItem(title, image, path=None):
    image, fanart = VerifyImages(image)

    liz = xbmcgui.ListItem(title, iconImage=image, thumbnailImage=image, path=path)
    liz.setProperty('Fanart_Image', image)
 
    # Jarvis way of setting artwork
    if hasattr(liz, 'setArt'):
        art = {}
        art['landscape'] = fanart
        art['banner']    = fanart
        art['poster']    = fanart
        art['thumb']     = fanart
        art['fanart']    = fanart
        liz.setArt(art) 

    return liz


def FileSystemSafe(text):
    import re
    text = re.sub('[:\\/*?\<>|"]+', '', text)
    return text.strip()


def BrowseVOD(params):
    option = browseDialog.show(ADDONID, params)

    if option == 'TRAILER':
        return PlayTrailer(params)

    on_play = int(iptv_utils.GetSetting('ON_PLAY'))
    on_down = int(iptv_utils.GetSetting('ON_DOWN'))
    title   = params.get('title', None)

    play     = False
    download = False

    if option == 'PLAY':
        play     = True
        download = False

        #if on_play == 0: # ask
        #    if iptv_utils.DialogYesNo(GETTEXT(30021) % title):
        #        download = True

        #if on_play == 2: # play and download
        #    download = True

    if option == 'DOWNLOAD':
        download = True

        if on_down == 0: # ask
            if iptv_utils.DialogYesNo(GETTEXT(30022) % title):
                play = True

        if on_down == 2: # download and play
            play = True

    #if option == 'JUST_PLAY':
    #    play     = True
    #    download = False


    if download:
        try:    Download(params)
        except: pass

    if play:
        try:    PlayLive(params)
        except: pass


def PlayTrailer(params):
    iptv_utils.DialogOK('Feature coming soon in a future update')


def GetDownloadFolder():
    folder = iptv_utils.GetSetting('DOWNLOAD')
    if folder:
        return folder

    iptv_utils.DialogOK(GETTEXT(30023))
    iptv_utils.OpenSettings(focus=2.6)

    folder = iptv_utils.GetSetting('DOWNLOAD')

    if folder:
        return folder

    return None


def Download(params):
    url   = params.get('url',    None)
    title = params.get('title',  None)
    type  = params.get('type',   None)
    ext   = params.get('ext',    None)
    plot  = params.get('plot',   '')
    image = params.get('fanart', '')

    url = iptv.GetStreamURL(url, type, ext)

    if ext != 'mp4':
        iptv_utils.DialogOK(GETTEXT(30024) % title)
        return

    folder = GetDownloadFolder()

    if not folder:
        return
        
    import download

    filename = FileSystemSafe(title)
    folder   = os.path.join(folder, filename)

    sfile.makedirs(folder)

    dest = os.path.join(folder, '%s.%s' % (filename, ext))
    inf  = os.path.join(folder, '%s.%s' % (filename, 'txt'))

    with open(inf, 'w') as f:
        f.write('%s\n' % image)
        f.write('%s\n' % title)
        f.write('%s\n' % plot)
    
    download.download(url, dest, title, quiet=True)


def PlayLive(params):
    url   = params.get('url',   None)
    title = params.get('title', None)
    image = params.get('image', None)
    ext   = params.get('ext',   None)
    type  = params.get('type',  None)
    plot  = params.get('plot',  None)

    Play(iptv.GetStreamURL(url, type, ext), title, plot, image)


def PlayCatchup(params):
    url   = params.get('url',   None)
    title = params.get('title', None)
    image = params.get('image', None)
    plot  = params.get('plot',  None)

    extra = params.get('extra', '-*-')
    start, end = extra.split('*', 1)

    Play(iptv.GetCatchupStreamURL(url, start, end), title, plot, image)


def PlayDownload(params):
    url   = params.get('url',   None)
    title = params.get('title', None)
    image = params.get('image', None)
    plot  = params.get('plot',  None)

    if sfile.isdir(url):
        try:    url = sfile.glob(url)[0]
        except: pass 

    if not sfile.isfile(url):
        iptv_utils.DialogOK(GETTEXT(30025) % title)
        return

    Play(url, title, plot, image)
   

def Play(url, title, plot, image):
    image, fanart = VerifyImages(image)

    liz = InitListItem(title, image, url)

    infoLabels = {}
    infoLabels['plot'] = plot

    liz.setInfo(type='Video', infoLabels=infoLabels)

    setResolvedUrl(url, liz)


def Delete(params):
    title  = params.get('title',    None)
    folder = params.get('folder',   None)
    file   = params.get('filename', None)
    
    if not iptv_utils.DialogYesNo(title, GETTEXT(30027)):
        return

    if folder:
        sfile.rmtree(folder)
    else:
        sfile.remove(file)


def speedTest():
    options = [GETTEXT(30019), GETTEXT(30020)]
    options = ['[COLOR white]%s[/COLOR]' % o for o in options] 

    title = '[COLOR white]%s[/COLOR]' % TITLE

    choice = xbmcgui.Dialog().select(title, options)

    if choice < 0:
        return

    root = os.path.join(RESOURCES, 'speedtest') 

    if choice == 0:
        script = 'speedtest'

    if choice == 1:
        script = 'fast'

    script = os.path.join(root, '%s.py' % script)

    xbmc.executebuiltin('Runscript("%s")' % script)


def setupPVR():
    if not iptv_utils.DialogYesNo(GETTEXT(30028)):
        return

    import pvr
    pvr.setup()


def launchPVR():
    import pvr
    pvr.launch()


def disablePVR():
    if not iptv_utils.DialogYesNo(GETTEXT(30029)):
        return

    import pvr
    pvr.disable()


def setResolvedUrl(url, listItem):
    windowed = iptv_utils.GetCondVisibility('Player.HasVideo')
    APPLICATION.setResolvedUrl(url, success=True, listItem=listItem, windowed=windowed)

   

def AddDir(title, mode=NULL, url='', extension='', type='', image=None, fanart=None, isFolder=True, infoLabels=None, contextMenu=None, desc=None, plot=None, extra=None, listID=None, altMode=None, fave=False):
    image, fanart = VerifyImages(image, fanart)

    if desc is None:
        desc = title

    if infoLabels is None:
        infoLabels = {}

    u  = ''
    u += '?mode='  + str(mode)

    u += '&title=' + iptv_utils.qplus(iptv_utils.fixText(title))

    u += '&image='  + iptv_utils.qplus(image)
    u += '&fanart=' + iptv_utils.qplus(fanart)

    if url is not None:
        url = str(url)     
        u += '&url=' + iptv_utils.qplus(url) 

    if extension:   
        u += '&ext=' + extension 

    if type:   
        u += '&type=' + type 

    if plot:
        plot = plot.replace(' / ', ', ')
        u += '&plot=' + iptv_utils.qplus(iptv_utils.fixText(plot))

    if desc:
        desc = desc.replace(' / ', ', ')
        u += '&desc=' + iptv_utils.qplus(iptv_utils.fixText(desc))

    if extra:
        extra = extra.replace(' / ', ', ')
        u += '&extra=' + iptv_utils.qplus(iptv_utils.fixText(extra))


    infoLabels['title']  = title
    infoLabels['plot']   = plot
    infoLabels['desc']   = desc
    infoLabels['fanart'] = fanart

    totalItems = 0

    isPlayable = not isFolder

    APPLICATION.addDir(title, mode, u, image, isFolder, isPlayable, totalItems=totalItems, contextMenu=contextMenu, replaceItems=True, infoLabels=infoLabels, listID=listID, altMode=altMode, fave=fave)


def inFavourites(param):
    utils.DialogOK(param)
    return True


def get_params(params):
    if not params:
        return {}

    param = {}

    cleanedparams = params.replace('?','')

    if (params[len(params)-1] == '/'):
       params = params[0:len(params)-2]

    pairsofparams = cleanedparams.split('&')    

    for i in range(len(pairsofparams)):
        splitparams = pairsofparams[i].split('=')

        if len(splitparams) == 2:
            param[splitparams[0]] = iptv_utils.unqplus(splitparams[1])

    return param


def updateComingSoon():
    iptv_utils.DialogOK(GETTEXT(30007))


def Empty(text='', reason=''):
    raise iptv_utils.EmptyListException(text=text, reason=reason)


def isSearchMode(_params):
    params = get_params(_params)

    try:    mode = int(params['mode'])
    except: mode = None

    return mode in [LIVE_SEARCH, VOD_SEARCH, VOD_TV_SEARCH, CATCHUP_SEARCH]

    

def onParams(application, _params):
    initGlobals(application)

    if xbmc.getCondVisibility('Pvr.HasTVChannels'):
        xbmcgui.Window(10000).clearProperty('PVR_SETUP')

    title  = None
    desc   = None
    footer = None
    
    params = get_params(_params)

    mode = None

    try:    mode = int(params['mode'])
    except: pass

    #iptv_utils.DialogOK('Mode = %r' % mode)

    try:    url = params['url']
    except: url = None

    try:    title = params['title']
    except: title = None

    if mode == NULL:
        pass


    elif mode == LATEST:
        Latest()


    elif mode == DOWNLOADS:
        Downloads()


    elif mode == LIVE:
        Live()


    elif mode == LIVE_ALL:
        LiveAll()

    elif mode == VOD:
        Vod()


    elif mode == VOD_ALL:
        VodAll()


    elif mode == VOD_TV:
        VodTV()


    elif mode == VOD_TV_ALL:
        VodTVAll()


    elif mode == VOD_BOXSETS:
        VodBoxsets()


    elif mode == CATCHUP:
        Catchup()


    elif mode == CATCHUP_ALL:
        CatchupAll()


    elif mode == CATCHUP_CAT or mode == CATCHUP_SEARCH:
        try:    duration = params['extra'] 
        except: duration = 7 #assume 7 days in this case

        image = params['image'] 
        CatchupCat(title, url, duration, image, mode == CATCHUP_SEARCH)


    elif mode == CATCHUP_DAY:
        CatchupDay(params)


    elif mode == CATCHUP_PLAY:
        PlayCatchup(params)
        

    elif mode == FOOTBALL_SCHEDULE:
        updateComingSoon()


    elif mode == UK_SPORT_LISTS:
        SportListings()


    elif mode == SETTINGS:
        ADDON.openSettings()


    elif mode == SPEEDTEST:
        speedTest()


    elif mode == IPTV_PVR:
        setupPVR()
        APPLICATION.removeListItem()
        Main()


    elif mode == LAUNCH_PVR:
        launchPVR()


    elif mode == DISABLE_PVR:
        disablePVR()
        APPLICATION.removeListItem()
        Main()


    elif mode == INTEGRATION:
        updateComingSoon()


    elif mode == LIVE_CAT:
        LiveCategory(url)


    elif mode == VOD_CAT:
        VODCategory(url)


    elif mode == PLAYABLE:
        PlayLive(params)


    elif mode == LIVE_SEARCH:
        LiveSearch()


    elif mode == VOD_SEARCH:
        VODSearch()


    elif mode == VOD_TV_SEARCH:
        VODTVSearch()


    elif mode == BROWSE_VOD:
        BrowseVOD(params)


    elif mode == DOWNLOADED:
        PlayDownload(params)


    elif mode == DELETE:
        Delete(params)


    elif mode == ACCOUNT:
        ShowAccountInfo()


    else:
        Main()

    if title:
        title = '%s - %s' % (TITLE, title)
    else:
        title = TITLE 

    if not desc:
        desc = GETTEXT(36001)

    footer = '%s v%s' % (TITLE, VERSION)
    if not footer:
        footer = GETTEXT(36002)

    xbmcgui.Window(10000).setProperty('FLAWLESS_TITLE',    title)
    xbmcgui.Window(10000).setProperty('FLAWLESS_FOOTER',   footer)
    xbmcgui.Window(10000).setProperty('FLAWLESS_MAINDESC', desc)
