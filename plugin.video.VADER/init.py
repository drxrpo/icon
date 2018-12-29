import xbmcplugin, xbmcgui
import time
from lib import utils


import pytz
from lib import routing
from lib import  vader

from xbmcplugin import addDirectoryItem, endOfDirectory
from xbmcgui import ListItem
import xbmc
from unidecode import unidecode
from datetime import datetime
from datetime import timedelta
import traceback
import plugintools
import json
import calendar
import base64
import requests
import re
import urllib
import urlresolver
import urlparse
import xbmcaddon
import dateutil.parser
import os

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



firstrun = plugintools.get_setting('first')

import sys
reload(sys)


def UTCToLocal(utc_dt):
    # get integer timestamp to avoid precision lost
    timestamp = calendar.timegm(utc_dt.timetuple())
    local_dt = datetime.fromtimestamp(timestamp)
    assert utc_dt.resolution >= timedelta(microseconds=1)
    return local_dt.replace(microsecond=utc_dt.microsecond)


def global_imports(modulename,shortname = None, asfunction = False):
    if shortname is None:
        shortname = modulename
    if asfunction is False:
        globals()[shortname] = __import__(modulename)
    else:
        globals()[shortname] = eval(modulename + "." + shortname)




sys.setdefaultencoding("utf-8")

plugin = routing.Plugin()

jsonGetTVEpisodes = '''{
        "jsonrpc": "2.0",
        "method": "VideoLibrary.GetEpisodes",
        "params": {

"filter": {"and": [{"operator": "contains", "field": "title", "value": "%s"}, {"operator": "contains", "field": "path", "value": "%s"}]},
         "properties": ["tvshowid", "plot", "showtitle", "title", "rating", "thumbnail", "playcount"]
        },
        "id": "mybash"
}'''

@plugin.route('/')
def index():
    try:
        authString = vaderClass.get_auth_status()
        if authString == 'Active':
            if vaderClass.show_categories:
                addDirectoryItem(plugin.handle, plugin.url_for(show_livetv_cat, 'all'), ListItem("Live TV"), True)
            else:
                addDirectoryItem(plugin.handle, plugin.url_for(show_livetv_all), ListItem("Live TV"), True)

            if vaderClass.enable_pvr == True:
                addDirectoryItem(plugin.handle, plugin.url_for(tvguide), ListItem("Kodi Guide"), False)
            addDirectoryItem(plugin.handle, plugin.url_for(vaderguide), ListItem("Addon Guide ~Beta~"), False)

            addDirectoryItem(plugin.handle, plugin.url_for(show_livetv_cat, '73'), ListItem("Live Sports #s"), True)
            addDirectoryItem(plugin.handle, plugin.url_for(show_mc), ListItem(vaderClass.MatchCenterName), True)
            if vaderClass.vodCapable == True:
                addDirectoryItem(plugin.handle, plugin.url_for(show_vod,'all'), ListItem("Video On Demand"), True)
            addDirectoryItem(plugin.handle, plugin.url_for(show_catchup_menu,'all'), ListItem(vaderClass.TVCatchupName), True)

            addDirectoryItem(plugin.handle, plugin.url_for(index), ListItem(""), False)
            if vaderClass.embedded == False:
                addDirectoryItem(plugin.handle, plugin.url_for(accountInfo), ListItem("My Account"), True)
            addDirectoryItem(plugin.handle, plugin.url_for(settings), ListItem("Settings"), True)
            addDirectoryItem(plugin.handle, plugin.url_for(categorySetup), ListItem("Configure Channel Groups"), True)

            addDirectoryItem(plugin.handle, plugin.url_for(show_tools), ListItem("Tools"), False)
        else:
            addDirectoryItem(plugin.handle, plugin.url_for(settings), ListItem("Unable to Login - {auth}".format(auth=authString)), True)
            addDirectoryItem(plugin.handle, plugin.url_for(show_tools),
                             ListItem("- Please send your log file for analysis if you think this was an error"), False)

            addDirectoryItem(plugin.handle, plugin.url_for(settings), ListItem('Click here to configure'), True)

        endOfDirectory(plugin.handle)

    except Exception as e:
        addDirectoryItem(plugin.handle, plugin.url_for(show_tools), ListItem("Tools - Please send your log file for analysis"), False)
        endOfDirectory(plugin.handle)
        utils.log("Error getting index \n{0}\n{1}".format(e, traceback.format_exc()))
        pass


@plugin.route('/serverSetup')
def serverSetup():
    vaderClass.serverSetup()

@plugin.route('/configPvr')
def categorySetup():
    vaderClass.updatePVRSettings()

@plugin.route('/categorySetup')
def categorySetup():
    vaderClass.categorySetup()

@plugin.route('/tools')
def show_tools():
    vaderClass.show_tools()

@plugin.route('/play/movie/<category_id>/<id>/<ext>/<name>')
def play_movie(category_id, id,ext, name):
    utils.log('TRYING TO PLAY ' + name)
    stream_id = id
    chanUrl = vaderClass.build_stream_url(stream_id, extension=ext, base='movie')
    r = requests.get(chanUrl, allow_redirects=False)
    chanUrl = r.headers['Location']
    utils.log(chanUrl)

    info = {}

    info['title'] = name
    icon = ''
    listitem = xbmcgui.ListItem(path=chanUrl, iconImage=icon)

    listitem.setInfo("video", info)
    listitem.setPath(chanUrl)

    win = xbmcgui.Window(10000)
    win.setProperty('vader.playing', 'True')
    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)


    return True

@plugin.route('/play/tv/<category_id>/<id>/<ext>/<name>/<season>/<episode>')
def play_tv(category_id, id, ext, name, season, episode):

    showName = name
    plot = ''
    chanUrl = vaderClass.build_stream_url(id, extension=ext, base='movie')
    r = requests.get(chanUrl, allow_redirects=False)
    chanUrl = r.headers['Location']
    utils.log(chanUrl)

    title = '{showName} - {season}x{episode}'.format(showName=name, season=season, episode=episode)
    icon = ''


    jsonval = xbmc.executeJSONRPC(jsonGetTVEpisodes % (title,showName ))
    jsonval = json.loads(jsonval)

    info = {}
    info['mediatype'] = 'episode'
    info['season'] = season
    info['episode'] = episode
    info['tvshowtitle'] = showName
    info['title'] = title
    info['plot'] = plot

    listitem=xbmcgui.ListItem(path=chanUrl,iconImage=icon)

    listitem.setInfo( "video", info )
    listitem.setPath(chanUrl)


    win = xbmcgui.Window(10000)
    win.setProperty('vader.playing', 'True')
    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)


    return True

@plugin.route('/vod/recent/<type>')
def show_vod_recent(type):

    streams = vaderClass.getVapiRecentVOD(type)
    if type == 'movie':
        for stream in streams:
            chanName = stream['title']
            stream_id = stream['vodItemId']
            category = stream['category']
            icon = stream['poster']
            if icon == None:
                icon = ''
            container_extension = stream['ext']
            chanUrl = vaderClass.build_stream_url(stream_id, extension=container_extension, base='movie')
            title = chanName
            title = str(title.encode('utf-8').decode('ascii', 'ignore'))
            if stream_id and chanName:
                chanData = 'plugin://' + ADDONID + '/play/movie/{cat}/{id}/{ext}/{title}'.format(cat=category, title=chanName, id=stream_id, ext=container_extension)

                plugintools.add_playable(title=title, url=chanData,
                                         thumbnail=icon, plot='', isPlayable=True, folder=False)


    if type == 'tv':
        for stream in streams:
            chanName = stream['showName']
            id = stream['id']
            icon = stream['poster']
            title = chanName
            title = str(title.encode('utf-8').decode('ascii', 'ignore'))
            addDirectoryItem(plugin.handle, plugin.url_for(show_vod_tvshow_episodes, id=id), ListItem(title), True)


    endOfDirectory(plugin.handle)

# @plugin.route('/vod/movies/<year>')
# def show_movies_year(year):
#     try:
#         if year == 'all':
#             validYears = []
#             validYears = vaderClass.get_vod_years()
#
#             for year in validYears:
#                 addDirectoryItem(plugin.handle, plugin.url_for(show_movies_year, year=str(year)), ListItem(
#                     str(year)), True)
#
#
#         else:
#             streams = vaderClass.get_vod_search(year, '53')
#             for stream in streams:
#                 name = stream['name']
#                 stream_id = stream['stream_id']
#                 icon = stream['stream_icon']
#                 extension = stream['container_extension']
#
#                 chanUrl = vaderClass.build_stream_url(stream_id, extension=extension, base='movie')
#
#                 title = name
#
#                 title = str(title.encode('utf-8').decode('ascii', 'ignore'))
#
#                 plugintools.add_playable(title=title, url=chanUrl,
#                                          thumbnail=icon, plot='', isPlayable=True, folder=False)
#
#         endOfDirectory(plugin.handle)
#
#     except Exception as e:
#         utils.log("Error listing streams \n{0}\n{1}".format(e, traceback.format_exc()))
#         pass

@plugin.route('/vod/titlesearch/<search>/')
def show_vod_titlesearch(search):
    try:
        vod_categories = vaderClass.get_vod_categories(sort=True)
        for category in vod_categories:
            parent_id = category['parent_id']
            name = category['category_name']
            cat_id = category['category_id']
            if search in name:
                addDirectoryItem(plugin.handle, plugin.url_for(show_vod, category_id=str(cat_id)), ListItem(name),
                                 True)



        endOfDirectory(plugin.handle)

    except Exception as e:
        utils.log("Error listing streams \n{0}\n{1}".format(e, traceback.format_exc()))
        pass

@plugin.route('/web_vod/parsed_shows/<type>/<channel>/')
def show_parsed_vod_shows(type, channel):
    utils.log('getting shows for ' + channel)
    data = vaderClass.getWebVodShowNames(type, channel)
    for show in data:
        addDirectoryItem(plugin.handle, plugin.url_for(show_parsed_vod_episodes, type=type, channel=channel, show=show), ListItem(
            show), True)


    endOfDirectory(plugin.handle)

@plugin.route('/playExternalLink/<link>')
def playExternalLink(link):

    try:
        link = urllib.unquote_plus(link)
        link = link.replace('https://www.youtube.com/embed/', 'http://youtube.com/watch?v=')
        utils.log(link)


        stream_url = urlresolver.resolve(link)

        if stream_url:
            utils.log('found stream url : ' + stream_url)
            xbmc.Player().play(item=stream_url, listitem=xbmcgui.ListItem(path=stream_url))
        else:
            utils.log('stream not found')

    except Exception as e:
        utils.log("Error listing streams \n{0}\n{1}".format(e, traceback.format_exc()))
        pass


    return True

@plugin.route('/web_vod/parsed_episodes/list_links_for_source/<type>/<channel>/<show>/<episode>/<source>/')
def show_links_for_vod_source(type, channel, show, episode, source):
    data = vaderClass.getParsedData(type)
    episode_links = data[channel][show][episode][source]
    for link in episode_links:
        netloc = urlparse.urlparse(link)[1]
        addDirectoryItem(plugin.handle, plugin.url_for(playExternalLink, link=urllib.quote_plus(link)), ListItem(
            'source: '+netloc), False)

    endOfDirectory(plugin.handle)


@plugin.route('/web_vod/parsed_episodes/<type>/<channel>/<show>/<episode>/')
def show_parsed_vod_episode_links(type, channel, show, episode):
    try:
        links = []
        episode_links = vaderClass.getWebVodMediaLinks(type, channel, show, episode)



        for item in episode_links:
            media_list = item['media_url']

            source_url = item['source_url']
            source_name = item['source_name']
            numLinks = len(media_list)
            itemNum = 1
            for media_url in media_list:
                appendString = str(itemNum) + '/' + str(numLinks)
                netloc = urlparse.urlparse(media_url)[1]

                if 'tvlogy.to' not in netloc:

                    addDirectoryItem(plugin.handle, plugin.url_for(playExternalLink, link=urllib.quote_plus(media_url)), ListItem(
                        source_name + ' : ' + netloc + ' : ' + appendString), True)

                itemNum = itemNum + 1

    except Exception as e:
        utils.log("Error listing streams \n{0}\n{1}".format(e, traceback.format_exc()))
        pass

    endOfDirectory(plugin.handle)


@plugin.route('/web_vod/parsed_episodes/<type>/<channel>/<show>/')
def show_parsed_vod_episodes(type, channel, show):
    try:
        data = vaderClass.getWebVodEpisodes(type, channel, show)

        for episode in data:
            addDirectoryItem(plugin.handle, plugin.url_for(show_parsed_vod_episode_links, type=type, channel=channel, show=show, episode=episode), ListItem(
                episode), True)

    except Exception as e:
        utils.log("Error listing streams \n{0}\n{1}".format(e, traceback.format_exc()))
        pass

    endOfDirectory(plugin.handle)


@plugin.route('/web_vod/parsed_chans/<type>/')
def show_parsed_vod_chans(type):

    try:
        data = vaderClass.getWebVodChanNames(type)
        for channel in data:
            addDirectoryItem(plugin.handle, plugin.url_for(show_parsed_vod_shows, type=type, channel=channel), ListItem(
                channel), True)

    except Exception as e:
        utils.log("Error listing streams \n{0}\n{1}".format(e, traceback.format_exc()))
        pass

    endOfDirectory(plugin.handle)

@plugin.route('/web_vod/')
def show_web_vod_menu():

    try:
        addDirectoryItem(plugin.handle, plugin.url_for(show_parsed_vod_chans, type='PakistanParsedData2'), ListItem(
            'Pakistan TV Shows'), True)

        addDirectoryItem(plugin.handle, plugin.url_for(show_parsed_vod_chans, type='IndianParsedData'), ListItem(
            'Indian TV Shows'), True)



    except Exception as e:
        utils.log("Error listing streams \n{0}\n{1}".format(e, traceback.format_exc()))
        pass


    endOfDirectory(plugin.handle)

@plugin.route('/vod/movies/<page>')
def show_vod_movies(page):
    movies =  vaderClass.getVapiMovies(int(page))
    for movie in movies['results']:
        title = movie['title']
        vodItem = movie['vodItemId']
        icon = movie['poster']
        plot = movie['desc']
        extension = movie['ext']
        category = movie['category']

        chanUrl = vaderClass.build_stream_url(vodItem, extension=extension, base='movie')

        title = str(title.encode('utf-8').decode('ascii', 'ignore'))
        if icon == None:
            icon = ''

        chanData = 'plugin://' + ADDONID + '/play/movie/{cat}/{id}/{ext}/{title}'.format(cat=category, title=title, id=vodItem, ext=extension)

        plugintools.add_playable(title=title, url=chanData,
                                 thumbnail=icon, plot='', isPlayable=True, folder=False)

    endOfDirectory(plugin.handle)

@plugin.route('/vod/tvshow_episodes/<id>')
def show_vod_tvshow_episodes(id):
    episodes = vaderClass.getVapiShowEpisodes(id)

    for episode in episodes:
        title = episode['title']
        name = episode['showName']
        episodeNum = episode['episode']
        seasonNum = episode['season']
        icon = episode['poster']
        plot = episode['desc']
        extension = episode['ext']
        vodItem = episode['vodItemId']
        category = episode['category']

        titlePrefix = 'Season: {season} Episode: {episode} - '.format(season=seasonNum, episode=episodeNum)
        title = titlePrefix + title
        chanUrl = vaderClass.build_stream_url(vodItem, extension=extension, base='movie')
        chanData = 'plugin://' + ADDONID + '/play/tv/{cat}/{id}/{ext}/{show}/{season}/{episode}'.format(
            show=name, season=seasonNum, episode=episodeNum, cat=category,id=vodItem, ext=extension)

        plugintools.add_playable(title=title, url=chanData,
                                 thumbnail=icon, plot='', isPlayable=True, folder=False)

    endOfDirectory(plugin.handle)

@plugin.route('/vod/tvshows/<page>')
def show_vod_tvshows(page):
    movies =  vaderClass.getVapiShowNames(int(page))
    for movie in movies['results']:
        title = movie['showName']
        id = str(movie['id'])
        icon = movie['poster']
        plot = movie['desc']
        title = str(title.encode('utf-8').decode('ascii', 'ignore'))

        if icon == None:
            icon = ''


        addDirectoryItem(plugin.handle, plugin.url_for(show_vod_tvshow_episodes, id=id), ListItem(title), True)


    endOfDirectory(plugin.handle)

@plugin.route('/vod/category/<category_id>/')
def show_vod(category_id):
    try:

        if category_id == 'all':
            # categories = vaderClass.get_vod_categories()
            # for category in categories:
            #     parent_id = str(category['parent_id'])
            #     name = str(category['category_name'])
            #     cat_id = category['category_id']
            #     if parent_id == '0':

            addDirectoryItem(plugin.handle, plugin.url_for(show_vod_movies, page='1'), ListItem(
                'Movies'), True)

            addDirectoryItem(plugin.handle, plugin.url_for(show_vod_tvshows, page='1'), ListItem(
                'TV Shows'), True)

            # addDirectoryItem(plugin.handle, plugin.url_for(show_movies_year, year='all'), ListItem(
            #     'Movies - By Year'), True)

            addDirectoryItem(plugin.handle, plugin.url_for(show_vod_recent, type='movie'), ListItem(
                'Recently Added - Movies'), True)
            addDirectoryItem(plugin.handle, plugin.url_for(show_vod_recent, type='tv'), ListItem(
                'Recently Added - TV Shows'), True)

            addDirectoryItem(plugin.handle, plugin.url_for(show_web_vod_menu), ListItem(
                'Web Based VOD ~Beta~'), True)


            addDirectoryItem(plugin.handle, plugin.url_for(show_vod_recent, type='tvshows'), ListItem(
                'Note: Surround Sound is included as the 2nd Audio Track, You can change Kodi default settings to auto select the best audio track instead of first'), True)

        # else:
        #         vod_categories = vaderClass.get_vod_categories(sort=True)
        #         uniqueShows = []
        #
        #         for category in vod_categories:
        #             parent_id = category['parent_id']
        #             name = category['category_name']
        #             cat_id = category['category_id']
        #
        #             if parent_id == category_id:
        #                 if parent_id == '55':
        #                     showName = re.split('S\d+', name)[0].strip()
        #                     if showName not in uniqueShows:
        #                         uniqueShows.append(showName)
        #                         search = showName + ' S'
        #                         addDirectoryItem(plugin.handle, plugin.url_for(show_vod_titlesearch, search=search),
        #                                          ListItem(showName),
        #                                          True)
        #                 else:
        #
        #                     addDirectoryItem(plugin.handle, plugin.url_for(show_vod, category_id=str(cat_id)), ListItem(name),
        #                                  True)
        #
        #
        #         streams = vaderClass.get_category_id_vod(category_id, sort=True)
        #         for stream in streams:
        #             chanName = stream['name']
        #             stream_id = stream['stream_id']
        #             icon = stream['stream_icon']
        #             extension = stream['container_extension']
        #
        #             chanUrl = vaderClass.build_stream_url(stream_id, extension=extension, base='movie')
        #
        #
        #             title = chanName
        #
        #             title = str(title.encode('utf-8').decode('ascii', 'ignore'))
        #             if icon == None:
        #                 icon = ''
        #
        #             plugintools.add_playable(title=title, url=chanUrl,
        #                                      thumbnail=icon, plot='', isPlayable=True, folder=False)



        endOfDirectory(plugin.handle)

    except Exception as e:
        utils.log("Error listing streams \n{0}\n{1}".format(e, traceback.format_exc()))
        pass

@plugin.route('/catchup/mc')
def show_catchup_mc():
    mcArchiveEvents = requests.get('http://vaders.tv/getMatchCenterArchive').json()

    backwardTime = datetime.utcnow() - timedelta(days=int(vaderClass.catchup_length))
    backwardTimeTs = calendar.timegm(backwardTime.timetuple())
    backwardTimeTs = int(backwardTimeTs)
    timeNow = time.time()
    timeNow = int(timeNow)
    for epgitem in mcArchiveEvents:
        title = epgitem['title']
        stream_id = epgitem['stream_id']
        startTime = int(epgitem['startTime'])
        playTime = epgitem['playTime']

        stopTime = int(epgitem['stopTime'])
        duration = int((stopTime - startTime)/60) + 5

        if (startTime > backwardTimeTs and startTime < timeNow):
            displayTime = datetime.fromtimestamp(int(startTime)).strftime('%d.%m - %H:%M')
            utc = pytz.utc
            # playTime = datetime.fromtimestamp(int(startTime), tz=utc).strftime('%Y-%m-%d:%H-%M')
            finalTitle = displayTime + " - " + title
            #(stream_id, newPlayTime,timestamp, title, duration)
            addDirectoryItem(plugin.handle, plugin.url_for(play_archive_adjusted, stream_id, playTime, startTime, title, str(duration)),
                             ListItem(finalTitle), False)

    endOfDirectory(plugin.handle)


@plugin.route('/catchup/category/<category_id>')
def show_catchup_tv_cat(category_id):

    try:

        if category_id == 'all':
            categories = vaderClass.get_categories()
            for category in categories:
                category_id_list = str(categories[category])
                addDirectoryItem(plugin.handle, plugin.url_for(show_catchup_tv_cat, category_id=category), ListItem(category_id_list), True)
        else:
            try:
                streams = vaderClass.get_category_id_live(category_id)
                for streamObj in streams:
                    chanName = streamObj['stream_display_name']
                    stream_id = streamObj['id']
                    programs = streamObj['programs']
                    channel_id = streamObj['channel_id']
                    tv_archive_duration = streamObj['tv_archive_duration']
                    if tv_archive_duration > 0:
                        title = chanName

                        title = str(title.encode('utf-8').decode('ascii', 'ignore'))
                        addDirectoryItem(plugin.handle, plugin.url_for(show_catchup_listing, stream_id, channel_id),
                                         ListItem(title), True)

            except Exception as e:
                utils.log("Error listing streams \n{0}\n{1}".format(e,traceback.format_exc()))
                pass

        endOfDirectory(plugin.handle)

    except Exception as e:
        utils.log("Error listing streams \n{0}\n{1}".format(e, traceback.format_exc()))
        pass

@plugin.route('/livetv/category/<category_id>')
def show_livetv_cat(category_id):

    try:

        if category_id == 'all':
            categories = vaderClass.get_categories()
            for category in categories:
                category_id_list = str(categories[category])


                addDirectoryItem(plugin.handle, plugin.url_for(show_livetv_cat, category_id=category), ListItem(category_id_list), True)
            endOfDirectory(plugin.handle)
        else:
            try:
                streams = vaderClass.get_category_id_live(category_id)
                for streamObj in streams:
                    chanName = streamObj['stream_display_name']

                    stream = streamObj['id']
                    icon = unidecode(streamObj['stream_icon'])
                    chanUrl = plugin.url_for(play_live, stream_id=stream)
                    programs = streamObj['programs']
                    timeNow = time.time()
                    timeNow = int(timeNow)
                    epg = ''

                    for program in programs:
                        startTime =  dateutil.parser.parse(program['start'])
                        stopTime =  dateutil.parser.parse(program['stop'])

                        startTimeLocal = UTCToLocal(startTime)
                        stopTimeLocal = UTCToLocal(stopTime)

                        startTime = int(time.mktime(startTimeLocal.timetuple()))
                        stopTime = int(time.mktime(stopTimeLocal.timetuple()))


                        if stopTime >= timeNow and startTime < timeNow:
                            epg = program['title']
                            break


                    title = '[COLOR orange]' +  unidecode(chanName) + '[/COLOR] - ' + '[I][COLOR cyan]' + unidecode(epg) +'[/COLOR][/I]'

                    title = str(title.encode('utf-8').decode('ascii', 'ignore'))


                    plugintools.add_playable(title=title, url=chanUrl,
                                             thumbnail=icon, plot='',  isPlayable=True, folder=False)

                endOfDirectory(plugin.handle)
            except Exception as e:
                utils.log("Error listing streams \n{0}\n{1}".format(e,traceback.format_exc()))
                pass

    except Exception as e:
        utils.log("Error listing streams \n{0}\n{1}".format(e, traceback.format_exc()))
        pass


@plugin.route('/livetv/all/')
def show_livetv_all():
    streams = vaderClass.get_all_streams()
    for streamObj in streams:
        chanName = streamObj['name']
        stream = streamObj['stream_id']
        icon = streamObj['stream_icon']
        category_id = streamObj['category_id']
        chanUrl = vaderClass.build_stream_url(stream)
        if category_id not in vaderClass.filter_category_list_id:
            if vaderClass.get_epg_chan(chanName):
                title = '[COLOR orange]' +  chanName + '[/COLOR] - ' + '[I][COLOR cyan]' + vaderClass.get_epg_chan(chanName) +'[/COLOR][/I]'
            else:
                title = chanName

            title = str(title.encode('utf-8').decode('ascii', 'ignore'))
            plugintools.add_playable(title=title, url=chanUrl,
                                     thumbnail=icon, plot='', isPlayable=True, folder=False)

    endOfDirectory(plugin.handle)



@plugin.route('/play/<stream_id>')
def play_live(stream_id):
    info = {}
    chanUrl = vaderClass.build_stream_url(stream_id)
    utils.log(chanUrl)
    r = requests.get(chanUrl, allow_redirects=False)
    newUrl = r.headers['Location']
    listitem = xbmcgui.ListItem(path=newUrl)

    if '.mpd' in newUrl:
        listitem.setProperty('inputstreamaddon', 'inputstream.adaptive')
        listitem.setProperty('inputstream.adaptive.manifest_type', 'mpd')


    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, listitem)


@plugin.route('/play_archive/<stream_id>/<playTime>/<title>/<duration>')
def play_archive(stream_id, playTime, title, duration):
    duration = str(int(duration) + 5)
    try:
        timestamp = int(time.mktime(datetime.strptime(playTime, "%Y-%m-%d:%H-%M").timetuple()))
    except TypeError:
        timestamp = int((time.mktime(time.strptime(playTime, "%Y-%m-%d:%H-%M"))))

    #serverTzString = vaderClass.user_info['server_timezone']
    serverTzString = 'Etc/UTC'
    tzObj = pytz.timezone(serverTzString)
    playTimeTs = datetime.fromtimestamp(int(timestamp), tz=tzObj)
    newPlayTime = playTimeTs.strftime('%Y-%m-%d:%H-%M')
    play_archive_adjusted(stream_id, newPlayTime,timestamp, title, duration)

@plugin.route('/play_archive_adjusted/<stream_id>/<playTime>/<ts>/<title>/<duration>')
def play_archive_adjusted(stream_id, playTime, ts, title, duration):
    url = vaderClass.get_playlink_archive(stream_id, playTime, ts, duration=duration)
    info = {}

    info['title'] = title
    listitem = xbmcgui.ListItem(path=url)
    listitem.setInfo("video", info)
    listitem.setPath(url)
    # win = xbmcgui.Window(10000)
    # win.setProperty('vader.playing', 'True')

    xbmc.Player().play(item=url, listitem=listitem)


@plugin.route('/catchup_search/<stream_id>/<search>')
def catchup_search(stream_id, search):

    try:
        jsondata = vaderClass.get_epg_for_stream(stream_id)['epg_listings']

        backwardTime = datetime.utcnow() - timedelta(days=int(vaderClass.catchup_length))

        backwardTimeTs = calendar.timegm(backwardTime.timetuple())
        backwardTimeTs = int(backwardTimeTs)
        timeNow = time.time()
        timeNow = int(timeNow)
        showNames = []


        for epgitem in jsondata:
            title = epgitem['title']

            title = base64.b64decode(title)
            startTime = int(epgitem['start_timestamp'])
            stopTime = int(epgitem['stop_timestamp'])
            duration = int((stopTime - startTime) / 60) + 5
            if (startTime > backwardTimeTs and startTime < timeNow):

                if search in title:
                    displayTime = datetime.fromtimestamp(int(startTime)).strftime('%d.%m - %H:%M')
                    utc = pytz.utc
                    playTimeTs = datetime.fromtimestamp(int(startTime), tz=utc)
                    playTime = playTimeTs.strftime('%Y-%m-%d:%H-%M')
                    finalTitle = displayTime + " - " + title

                    #(stream_id, newPlayTime,timestamp, title, duration)
                    addDirectoryItem(plugin.handle,
                                     plugin.url_for(play_archive_adjusted, stream_id, playTime, startTime, title, str(duration)),
                                     ListItem(finalTitle), False)



    except Exception as e:
        utils.log("Error listing streams \n{0}\n{1}".format(e, traceback.format_exc()))
        pass

    endOfDirectory(plugin.handle)



@plugin.route('/catchup_listing/<stream_id>/<channel_id>')
def show_catchup_listing(stream_id, channel_id):


    programs = vaderClass.get_epg_for_stream(channel_id)
    backwardTime = datetime.utcnow() - timedelta(days=int(vaderClass.catchup_length))
    backwardTimeTs      = calendar.timegm(backwardTime.timetuple())
    backwardTimeTs = int(backwardTimeTs)
    timeNow = time.time()
    timeNow     = int(timeNow)
    showNames = []

    timeNow = time.time()
    timeNow = int(timeNow)
    epg = ''

    for program in programs:
        startTime =  dateutil.parser.parse(program['start'])
        stopTime =  dateutil.parser.parse(program['stop'])
        startTimeLocal = UTCToLocal(startTime)
        stopTimeLocal = UTCToLocal(stopTime)

        startTime = int(time.mktime(startTimeLocal.timetuple()))
        stopTime = int(time.mktime(stopTimeLocal.timetuple()))
        duration = (stopTime - startTime)/60

        title  = program['title']
        if(startTime > backwardTimeTs and startTime < timeNow):
            if vaderClass.group_by_name == True:
                if title not in showNames:
                    showNames.append(title)
                    displayTime = datetime.fromtimestamp(int(startTime)).strftime('%d.%m - %H:%M')
                    utc = pytz.utc
                    if '[New!]' in title:
                        finalTitle = displayTime + " - " + title
                    else:
                        finalTitle = title
                    addDirectoryItem(plugin.handle,
                                     plugin.url_for(catchup_search, stream_id, title),
                                     ListItem(finalTitle), True)
            else:

                displayTime = datetime.fromtimestamp(int(startTime)).strftime('%d.%m - %H:%M')
                utc = pytz.utc
                playTimeTs = datetime.fromtimestamp(int(startTime), tz=utc)
                playTime = datetime.fromtimestamp(int(startTime), tz=utc).strftime('%Y-%m-%d:%H-%M')
                finalTitle = displayTime + " - "    +       title
                addDirectoryItem(plugin.handle, plugin.url_for(play_archive_adjusted, stream_id, playTime, startTime, title, str(duration)), ListItem(finalTitle), False)


    endOfDirectory(plugin.handle)


@plugin.route('/catchup/<type>')
def show_catchup_menu(type):

    if type == 'all':
        addDirectoryItem(plugin.handle, plugin.url_for(show_catchup_menu, 'tv'), ListItem(vaderClass.TVCatchupName), True)
        addDirectoryItem(plugin.handle, plugin.url_for(show_catchup_menu, 'mc'), ListItem(vaderClass.MCCatchupName), True)

    if type == 'tv':
        show_catchup_tv_cat('all')

    if type == 'mc':
        show_catchup_mc()

    endOfDirectory(plugin.handle)


@plugin.route('/mc/')
def show_mc():
    closedTime = plugintools.get_setting('mcClosedTime')
    if closedTime == None or closedTime == '':
        plugintools.set_setting('mcClosedTime', '0')
    closedTime = int((plugintools.get_setting('mcClosedTime')))
    timeDiff = time.time() - closedTime
    mc_quittimer = plugintools.get_setting('mc_quittimer')
    if time.time() - closedTime > int(mc_quittimer):
        endOfDirectory(plugin.handle)
        vaderClass.startMCC()
    else:

        endOfDirectory(plugin.handle)
        xbmc.executebuiltin('Action(Back)')




@plugin.route('/accountInfo')
def accountInfo():
    status = ''
    if vaderClass.user_info['enabled'] == True:
        status = 'Active'
    else:
        status = 'Banned'

    exp_date = vaderClass.user_info['exp_date']
    if exp_date:
        exp_date_str =  datetime.fromtimestamp(int(exp_date)).strftime('%d-%m-%Y')
    else:
        exp_date_str = "Never"
    trial_str = vaderClass.user_info["is_trial"]

    if trial_str != True:
        trial_str = "No"
    else:
        trial_str = "Yes"

    max_connections = str(vaderClass.user_info["max_connections"])
    username = vaderClass.user_info["username"]

    addDirectoryItem(plugin.handle, plugin.url_for(accountInfo), ListItem("[COLOR orange] User: [/COLOR]" + username), False)
    addDirectoryItem(plugin.handle, plugin.url_for(accountInfo), ListItem("[COLOR orange] Status: [/COLOR]" + status), False)
    addDirectoryItem(plugin.handle, plugin.url_for(accountInfo), ListItem("[COLOR orange] Expires: [/COLOR]" + exp_date_str), False)
    addDirectoryItem(plugin.handle, plugin.url_for(accountInfo), ListItem("[COLOR orange] Trial Account: [/COLOR]" + trial_str), False)
    addDirectoryItem(plugin.handle, plugin.url_for(accountInfo), ListItem("[COLOR orange] Max Devices: [/COLOR]" + max_connections), False)


    endOfDirectory(plugin.handle)


@plugin.route('/vaderguide')
def vaderguide():
    enable_pvr = plugintools.get_setting('enable_pvr')
    # if enable_pvr:
    #     xbmc.executebuiltin("XBMC.ActivateWindow(tvguide)")
    # else:
    xbmc.executebuiltin('XBMC.RunAddon(script.tvguide.Vader)')


    endOfDirectory(plugin.handle)

@plugin.route('/tvguide')
def tvguide():
    enable_pvr = plugintools.get_setting('enable_pvr')
    # if enable_pvr:
    xbmc.executebuiltin("XBMC.ActivateWindow(tvguide)")
    # else:
    # xbmc.executebuiltin('XBMC.RunAddon(script.tvguide.Vader)')


    endOfDirectory(plugin.handle)


@plugin.route('/settings')
def settings():
    plugintools.open_settings_dialog()

if __name__ == '__main__':

    try:
        __addon__ = xbmcaddon.Addon()
        ADDONDATA = xbmc.translatePath(__addon__.getAddonInfo('profile'))
        start = datetime.now()
        vaderClass = vader.vader()
        plugin.run()
        utils.log('Vader function ran in {0}ms'.format(str(datetime.now() - start)))
        del vaderClass
        del plugin
        del __addon__
        del ADDONDATA
    except Exception as e:
        import utils
        utils.log('something horrible happened')
        utils.log("Error getting index \n{0}\n{1}".format(e, traceback.format_exc()))

    #
    #     lockFile = os.path.join(ADDONDATA, 'file.lock')
    #
    #     if not os.path.exists(lockFile):
    #         with open(lockFile, 'w') as lockFileFd:
    #             start = datetime.now()
    #             vaderClass = vader.vader()
    #             plugin.run()
    #             utils.log('Vader function ran in {0}ms'.format(str(datetime.now() - start)))
    #             del vaderClass
    #             del plugin
    #         os.remove(lockFile)
    # except Exception as e:
    #     utils.log('something horrible happened')
    #     utils.log("Error getting index \n{0}\n{1}".format(e, traceback.format_exc()))
