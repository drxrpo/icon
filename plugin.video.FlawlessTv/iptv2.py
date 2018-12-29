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


import datetime
import json
import re

import iptv_utils
import iptv


ROOT = iptv.ROOT

SCALER = 1

SEASON   = iptv_utils.GETTEXT(30030)
SPECIALS = iptv_utils.GETTEXT(30031)


def log(text):
    return
    text = '%r' % text
    iptv_utils.DialogOK(text1)
    iptv_utils.log(text, True)


def credsOK(username, password):
    if iptv_utils.IsDebug():
        return True

    if not username:
        return False

    if not password:
        return False

    try:
        url = ROOT + '/player_api.php?username=%s&password=%s' % (username, password)
 
        info = iptv_utils.GetURL(url, maxSec=0)
        info = json.loads(info)
        info = info['user_info']

        return info['auth'] == 1

    except:
        pass

    return False


def MigrateCredentials():
    if iptv_utils.GetSetting('MIGRATED') == 'true':
        return

    iptv_utils.SetSetting('MIGRATED', 'true')

    log('MigrateCredentials')
    try:
        #first check if existing new ones work
        username = iptv_utils.GetSetting(iptv_utils.U)
        password = iptv_utils.GetSetting(iptv_utils.P)

        if credsOK(username, password):
            #clear old settings
            iptv_utils.SetSetting('Username', '')
            iptv_utils.SetSetting('Password', '')
            return

    except:
        pass

    try:
        #try old settings
        username = iptv_utils.GetSetting('Username')
        password = iptv_utils.GetSetting('Password')

        if credsOK(username, password):
            #clear old settings, and update new settings
            iptv_utils.SetSetting('Username', '')
            iptv_utils.SetSetting('Password', '')

            iptv_utils.SetSetting('USERNAME', username)
            iptv_utils.SetSetting('PASSWORD', password)
    except:
        pass


def GetCredentials(silent=False, dialogOnly=False):
    username = iptv_utils.GetSetting('USERNAME')
    password = iptv_utils.GetSetting('PASSWORD')

    if not silent and not credsOK(username, password):
        iptv_utils.DialogOK(iptv_utils.GETTEXT(30002), iptv_utils.GETTEXT(30035))
        if not dialogOnly:
            if not username:
                focus = 2.1
            else:
                focus = 2.2

            iptv_utils.OpenSettings(focus=focus)

            username = iptv_utils.GetSetting('USERNAME')
            password = iptv_utils.GetSetting('PASSWORD')

    if not username or not password:
        raise Exception('Credentials not set')

    return username, password


def GetAccountInfo(maxSec=86400, dialogOnly=False, credsWrong=False):
    try:
        username, password = GetCredentials(dialogOnly=dialogOnly)

        url = ROOT + '/player_api.php?username=%s&password=%s' % (username, password)
 
        info = iptv_utils.GetURL(url, maxSec=maxSec)
 
        return json.loads(info)

    except Exception as e:
        log('ERROR1 %s' % e)
        return {}


def GetStreamURL(stream_id, type, ext):
    log("GetStreamURL")
    try:
        username, password = GetCredentials()

        #if type == 'created_live':
        #    type = 'live'

        stream_id = stream_id.split(':')[0]

        url = '%s/%s/%s/%s/%s.%s' % (ROOT, type, username, password, str(stream_id), ext)
        #url = url.replace('watch.b2b-hosting.net', 'watch.b2b-hosting.net:80')
        return url

    except Exception as e:
        log('ERROR2 %s' % e)
        return None


def NewDay():
    try:    GetVODLatest(silent=True)
    except: pass



def GetVODCategory_V1(url, search=None):
    try:
        if url == 0:
            username, password = GetCredentials()
            url = ROOT + '/enigma2.php?username=%s&password=%s&type=get_vod_streams&cat_id=0' % (username, password)

        response = iptv_utils.GetURL(url, maxSec=3600 * SCALER) # 60 minutes

        channels = re.compile('<channel>(.+?)</channel>').findall(response)

        if search:
            search = search.upper()
        
        cat = []

        for channel in channels:
            try:    title = iptv_utils.Decode(re.compile('<title>(.+?)</title>').search(channel).group(1))
            except: continue

            try:    desc = iptv_utils.Decode(re.compile('<description>(.+?)</description>').search(channel).group(1)).replace('IMDB_ID: \n', '')
            except: desc = ''

            if search:
                if (search not in title.upper()) and (search not in desc.upper()):
                    continue

            try:    image  = re.compile('<desc_image><!\[CDATA\[(.+?)\]\]></desc_image>').search(channel).group(1)
            except: image = ''

            try:    stream = re.compile('<stream_url><!\[CDATA\[(.+?)\]\]></stream_url>').search(channel).group(1)
            except: stream = ''

            #try:    category = re.compile('<category_id>(.+?)</category_id>').search(channel).group(1)
            #except: category = ''

            title = title.split(' [', 1)

            try:    prog  = title[1].split('   ')[-1]
            except: prog = ''

            title = title[0].strip()

            stream = stream.split('/')

            stream_type         = stream[3]
            stream_id           = stream[6].split('.')[0]
            container_extension = stream[6].split('.')[1]

            item = {}
            item['name']                = title
            item['stream_type']         = stream_type
            item['stream_id']           = stream_id
            item['container_extension'] = container_extension
            item['stream_icon']         = image
            item['description']         = desc

            cat.append(item)

        return cat

    except Exception as e:
        log('ERROR3 %s' % e)
        return []



def GetVODCategory(url, search=None, silent=False):
    try:
        if '&season_id=' in url: 
            return GetSeason(url, search)
    except:
        pass

    log('GetVODCategory %r' % url)
    try:
        username, password = GetCredentials(silent=silent)

        if url == 0:
            url = ROOT + '/player_api.php?username=%s&password=%s&action=get_vod_streams' % (username, password)
        
        cat = iptv_utils.GetURL(url)

        items = json.loads(cat)

        search = search.upper() if search else ''

        #API v2
        #root = ROOT + '/player_api.php?username=%s&password=%s&action=get_vod_info&vod_id=' % (username, password)

        #API v1 to get all the categories, and use that to get plots
        cats = iptv.GetVODCategory(0, None)
        plots = {}
        for cat in cats:
            stream_id        = int(cat['stream_id'])
            description      = cat['description']
            plots[stream_id] = description

        results = []
        for item in items:
            stream_id = item['stream_id']

            #API V2
            #url = '%s%s' % (root, str(stream_id)) 
            #info = iptv_utils.GetURL(url)
            #info = json.loads(info)['info']
            #item['description'] = info['plot']

            #API v1 - use this for efficiency to get all plots in one call
            try:    item['description'] = plots[stream_id]
            except: item['description'] = ''

            if search in item['name'].upper() or search in item['description'].upper():
                results.append(item)

        return results

    except Exception as e:
        log('ERROR3 %s' % e)
        return []


def GetVODInfo(url):
    try:
        username, password = GetCredentials()
        url = ROOT + '/player_api.php?username=%s&password=%s&action=get_vod_info&vod_id=%s' % (username, password, str(url))
        
        response = iptv_utils.GetURL(url)

        return json.loads(response)

    except Exception as e:
        log('ERROR4 %s' % e)
        return []


def GetVODLatest(nmrItems=8, silent=False):
    log('GetVODLatest')
    nmrItems = int(nmrItems)

    if nmrItems < 4:
        nmrItems = 4

    items = GetVODCategory(0, silent=silent)

    newlist = sorted(items, key=lambda x: x['stream_id'], reverse=True)
    return newlist[:nmrItems]

    #items = []

    #for item in newlist:
    #    items.append(item)

    #    if len(items) == nmrItems:
    #        return items

    #return items


def GetLiveCategories():
    log('GetLiveCategories USE v1')
    return iptv.GetLiveCategories()
    try:
        username, password = GetCredentials()

        url  = ROOT + '/player_api.php?username=%s&password=%s&action=get_live_categories' % (username, password)
        cats = iptv_utils.GetURL(url, maxSec=3600 * SCALER) # 60 minutes
        cats = json.loads(cats)

        root = ROOT + '/player_api.php?username=%s&password=%s&action=get_live_streams&category_id=' % (username, password)
        
        newCats = []
        for cat in cats:
            cat['playlist_url'] = '%s%s' % (root, str(cat['category_id']))
            newCats.append(cat)

        return newCats

    except Exception as e:
        log('ERROR5 %s' % e)
        return []


def GetLiveCategory(url, search=None):
    log('GetLiveCategory %r %r USE v1' % (url, search))
    return iptv.GetLiveCategory(url, search)
    try:
        if url == 0:  # i.e. All
            url = ROOT + '/player_api.php?username=%s&password=%s&action=get_live_streams' % (username, password)

        channels = iptv_utils.GetURL(url)
        channels = json.loads(channels)

        newChannels = []

        for channel in channels:
            channel['now']  = 'now'
            channel['next'] = 'next'
            newChannels.append(channel)

        return newChannels

    except Exception as e:
        log('ERROR6 %s' % e)
        return []


def Catchup():
    return iptv.Catchup()


def CatchupCat(stream_id, tv_archive_duration, search=None):
    return iptv.CatchupCat(stream_id, tv_archive_duration, search)


def GetCatchupStreamURL(stream_id, start, end):
    return iptv.GetCatchupStreamURL(stream_id, start, end)


def GetBoxSets():
    return GetVODCategories(boxsets=True)


def GetVODCategories(boxsets=False):
    log('GetVODCategories')
    try:
        username, password = GetCredentials()

        url = ROOT + '/player_api.php?username=%s&password=%s&action=get_vod_categories' % (username, password)

        cats = iptv_utils.GetURL(url)
        cats = json.loads(cats)

        #API 2
        root = ROOT + '/player_api.php?username=%s&password=%s&action=get_vod_streams&category_id=' % (username, password)

        #API 1
        #root = ROOT + '/enigma2.php?username=%s&password=%s&type=get_vod_streams&cat_id=' % (username, password)

        newCats = []
        for cat in cats:
            isBoxset = False 
            if cat['category_name'].startswith('Boxset:'):
                isBoxset = True
                cat['category_name'] = cat['category_name'].replace('Boxset:', '', 1).strip()

            if (boxsets and isBoxset) or (not boxsets and not isBoxset):
                cat['playlist_url'] = '%s%s' % (root, cat['category_id'])
                newCats.append(cat)

        return newCats

    except Exception as e:
        log('ERROR7 %s' % e)
        return []


def GetSeriesByCategoryID(category_id):
    #log('GetSeriesByCategoryID(%r)' % category_id)
    try:
        username, password = GetCredentials()

        url = ROOT + '/player_api.php?username=%s&password=%s&action=get_series&category_id=%s' % (username, password, str(category_id))
 
        response = iptv_utils.GetURL(url, maxSec=7*86400)
        response = json.loads(response)[0]  # this will throw if no data returned, which is okay

        return response

    except Exception as e:
        return {}



def GetVODSeriesCategories(search=None):
    log('GetVODSeriesCategories(%r)' % search)
    try:
        username, password = GetCredentials()

        url = ROOT + '/player_api.php?username=%s&password=%s&action=get_series_categories' % (username, password)

        cats = iptv_utils.GetURL(url)
        cats = json.loads(cats)

        root = ROOT + '/player_api.php?username=%s&password=%s&action=get_series&category_id=' % (username, password)

        if search:
            search = search.upper()
        
        newCats = []
        for cat in cats:
            if search and search not in cat['category_name'].upper():
                continue
            cat['playlist_url'] = '%s%s' % (root, str(cat['category_id']))
            newCats.append(cat)

        return newCats

    except Exception as e:
        log('ERROR7 %s' % e)
        return []


def GetSVODCategory(url, search=None):
    log('GetSVODCategory %r %r' % (url, search))
    try:
        username, password = GetCredentials()

        cats = iptv_utils.GetURL(url)
        cats = json.loads(cats)
        
        series_id   = int(cats[0]['series_id'])
        category_id = int(cats[0]['category_id'])

        url = ROOT + '/player_api.php?username=%s&password=%s&action=get_series_info&series_id=%d' % (username, password, series_id)

        cats = iptv_utils.GetURL(url)
        cats = json.loads(cats)

        #run through all episodes storing season IDs
        allEpisodes = cats['episodes']
        liveSeasons = {}
        for episodes in allEpisodes:
            episodes = allEpisodes[episodes]
            for episode in episodes:
                season = episode['season']
                liveSeasons[season] = episode['title']

        newSeasons = []

        seasons = cats['seasons']
        if isinstance(seasons, dict):
            for season in seasons:
                season = seasons[season]
                newSeasons.append(season) 
            seasons = newSeasons
        elif len(seasons) == 0:
            for id in liveSeasons:
                season = {}
                season['season_number'] = id
                season['name'] = SEASON % id if id else SPECIALS
                season['cover']         = ''
                season['overview']      = ''
                seasons.append(season)
                
        special = None

        newSeasons = []
        for season in seasons:
            season_number = season['season_number']
            
            if season_number not in liveSeasons:
                continue

            title                   = season['name']
            season['category_name'] = title
            season['playlist_url']  = '%s&season_id=%d&category_id=%d' % (url, season_number, category_id)
            season['stream_icon']   = season['cover']
            season['description']   = season['overview']

            if season_number == 0:
                special = season
            else:
                newSeasons.append(season)

        if special:
            newSeasons.append(special)

        return newSeasons

    except Exception as e:
        log('ERROR8 %s' % e)
        return []


def GetSeason(url, search):
    log('GetSeason %r %r' % (url, None))
    try:

        url, cat_id = url.split('&category_id=')
        url, id     = url.split('&season_id=')

        info = iptv_utils.GetURL(url)
        info = json.loads(info)

        try:    episodes = info['episodes'][str(id)]
        except: episodes = []

        items = []

        for episode in episodes:
            item = {}
            item['name']                = episode['title']
            item['stream_type']         = 'series'
            item['stream_id']           = '%s:%s' % (episode['id'], cat_id)
            item['stream_icon']         = episode['info']['movie_image']
            item['description']         = episode['info']['plot']
            item['container_extension'] = episode['container_extension']

            items.append(item) 

        return items 

    except Exception as e:
        log('ERROR9 %s' % e)
        return []


def GetStreamURLByChannelID(channel_id):
    try:
        channels = GetLiveCategory(0)

        for channel in channels:
            if channel['name'] == channel_id:
                ext  = channel['container_extension']
                type = channel['stream_type']
                id   = channel['stream_id']
                return GetStreamURL(id, type, ext)
    except:
        pass

    return None
