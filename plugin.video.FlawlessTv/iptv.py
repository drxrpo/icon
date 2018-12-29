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

ROOT = 'http://kodi.flawless-hosting.solutions'


SCALER = 1


def log(text):
    return
    text = '%r' % text
    iptv_utils.DialogOK(text1)
    iptv_utils.log(text, True)



def AssertURL(url, title):
    #return ''
    if url.startswith('http://flawless-iptv.net'):
        url = iptv_utils.IMDB
        #url = url.replace('http://flawless-iptv.net', ROOT)
        #url = url.replace('8080', '4545')

    return url



def GetCredentials(silent=False):
    username = iptv_utils.GetSetting('USERNAME')
    password = iptv_utils.GetSetting('PASSWORD')
    
    if not silent and (not username or not password):
        iptv_utils.DialogOK(utils.GETTEXT(30002))
        if not username:
            iptv_utils.DialogOK(1)
            iptv_utils.OpenSettings(focus=2.1)
        else:
            iptv_utils.DialogOK(2)
            iptv_utils.OpenSettings(focus=2.2)

        username = iptv_utils.GetSetting('USERNAME')
        password = iptv_utils.GetSetting('PASSWORD')

    if not username or not password:
        raise Exception('Credentials not set')

    return username, password


def GetAccountInfo(maxSec=86400):
    try:
        username, password = GetCredentials()

        url = ROOT + '/player_api.php?username=%s&password=%s' % (username, password)

        info = iptv_utils.GetURL(url, maxSec=maxSec)
 
        return json.loads(info)

    except Exception as e:
        #iptv_utils.log(e, True)
        return {}


def FixWhen(_when, _desc, gmtOffset):
    # fix desc for users timezone
    # times are currently GMT+1
    when = _when

    if gmtOffset != 3600:  # this is the offset the data is already in, so no need to change
        format = '%H:%M'

        when_ori  = re.compile('\[(.+?)\]').search(_when).group(1)

        when  = iptv_utils.ParseTime(when_ori,  format) 

        # correct to GMT
        when  -= datetime.timedelta(seconds=3600)

        # correct to users timezone
        when  += datetime.timedelta(seconds=gmtOffset)

        when_ori  = '[%s]' % when_ori

        fix  = '[%02d:%02d]' % (when.time().hour, when.time().minute)

        # finally fix the values
        when  = _when.replace(when_ori, fix, 1)

    desc = _desc.split('( ')[-1]
    desc = desc[:-1] #remove final '('

    return '[B]%s[/B][CR]%s' % (when, desc)


def GetNowNext(desc):
    if not desc:
        return '', ''

    gmtOffset = iptv_utils.GetGMTOffset()

    desc = desc.split('\n')

    try:    now = FixWhen(desc[0], desc[1], gmtOffset)
    except: now = ''

    try:    next = FixWhen(desc[2], desc[3], gmtOffset)
    except: next = ''

    return now.strip(), next.strip()


def GetBoxSets():
    try:
        username, password = GetCredentials()

        url = ROOT + '/enigma2.php?username=%s&password=%s&type=get_vod_scategories&scat_id=415'  % (username, password)
        log(url)
        return GetSVODCategory(url)

    except Exception as e:
        #iptv_utils.log(e, True)
        iptv_utils.DialogOK(e)
        return []


def GetVODLatest(nmrItems=10):
    nmrItems = int(nmrItems)
    items = GetVODCategory(0)

    newlist = sorted(items, key=lambda x: x['stream_id'], reverse=True)

    items = []

    for item in newlist:
        #if item['description'].startswith('IMDB_ID'):
        #    continue

        items.append(item)

        if len(items) == nmrItems:
            return items

    return items


def GetVODCategories():
    try:
        username, password = GetCredentials()

        url = ROOT + '/enigma2.php?username=%s&password=%s&type=get_vod_categories'  % (username, password)
        log(url)

        response = iptv_utils.GetURL(url, maxSec=3600 * SCALER) # 60 minutes

        channels = re.compile('<channel>(.+?)</channel>').findall(response)

        cat = []
        log(len(channels))

        for channel in channels:
            try:    category_id = re.compile('<category_id>(.+?)</category_id>').search(channel).group(1)
            except: continue

            try:    title = iptv_utils.Decode(re.compile('<title>(.+?)</title>').search(channel).group(1))
            except: continue

            #try:    desc = iptv_utils.Decode(re.compile('<description>(.+?)</description>').search(channel).group(1))
            #except: desc = ''

            try:    playlist_url = re.compile('<playlist_url><!\[CDATA\[(.+?)\]\]></playlist_url>').search(channel).group(1)
            except: playlist_url = ''

            item = {}
            item['category_name'] = title
            item['category_id']   = category_id
            item['playlist_url']  = playlist_url
            #item['description']  = desc
            cat.append(item)

        log(cat)
        return cat


    except Exception as e:
        iptv_utils.log(e, True)
        return []


def GetSVODCategory(url, search=None):
    try:
        response = iptv_utils.GetURL(url, maxSec=3600 * SCALER) # 60 minutes

        channels = re.compile('<channel>(.+?)</channel>').findall(response)

        if search:
            search = search.upper()
        
        cat = []

        for channel in channels:
            try:    title = iptv_utils.Decode(re.compile('<title>(.+?)</title>').search(channel).group(1))
            except: continue

            desc = ''

            if search:
                if (search not in title.upper()) and (search not in desc.upper()):
                    continue

            image = ''

            try:    playlist_url = re.compile('<playlist_url><!\[CDATA\[(.+?)\]\]></playlist_url>').search(channel).group(1)
            except: playlist_url = ''

            #try:    category = re.compile('<category_id>(.+?)</category_id>').search(channel).group(1)
            #except: category = ''

            title = title.split(' [', 1)

            try:    prog  = title[1].split('   ')[-1]
            except: prog = ''

            title = title[0].strip()

            item = {}
            item['category_name'] = title
            item['stream_icon']   = AssertURL(image, title)
            item['playlist_url']  = playlist_url
            item['description']   = desc

            cat.append(item)

        return cat

    except Exception as e:
        #iptv_utils.log(e, True)
        return []


def GetVODCategory(url, search=None):
    try:
        if url == 0:
            username, password = GetCredentials()
            url = ROOT + '/enigma2.php?username=%s&password=%s&type=get_vod_streams&cat_id=0' % (username, password)

        response = iptv_utils.GetURL(url, maxSec=86400 * SCALER)  # 1 day

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
            item['stream_icon']         = AssertURL(image, title)
            item['description']         = desc

            cat.append(item)

        return cat

    except Exception as e:
        #iptv_utils.log(e, True)
        return []


def GetLiveCategories():
    try:
        username, password = GetCredentials()

        url = ROOT + '/enigma2.php?username=%s&password=%s&type=get_live_categories'  % (username, password)

        response = iptv_utils.GetURL(url, maxSec=3600 * SCALER) # 60 minutes

        channels = re.compile('<channel>(.+?)</channel>').findall(response)

        cat = []

        for channel in channels:
            try:    category_id = re.compile('<category_id>(.+?)</category_id>').search(channel).group(1)
            except: continue

            try:    title = iptv_utils.Decode(re.compile('<title>(.+?)</title>').search(channel).group(1))
            except: continue

            #try:    desc = iptv_utils.Decode(re.compile('<description>(.+?)</description>').search(channel).group(1))
            #except: desc = ''

            try:    playlist_url = re.compile('<playlist_url><!\[CDATA\[(.+?)\]\]></playlist_url>').search(channel).group(1)
            except: playlist_url = ''

            item = {}
            item['category_name'] = title
            item['category_id']   = category_id
            item['playlist_url']  = playlist_url
            #item['description']   = desc

            cat.append(item)

        return cat


    except Exception as e:
        #iptv_utils.log(e, True)
        return []


def GetLiveCategory(url, search=None):
    try:
        if url == 0:
            username, password = GetCredentials()
            url = ROOT + '/enigma2.php?username=%s&password=%s&type=get_live_streams&cat_id=0'  % (username, password)
       
        response = iptv_utils.GetURL(url, maxSec=300 * SCALER) # 5 minutes

        channels = re.compile('<channel>(.+?)</channel>').findall(response)

        if search:
            search = search.upper()

        cat = []

        for channel in channels:
            try:    title  = iptv_utils.Decode(re.compile('<title>(.+?)</title>').search(channel).group(1))
            except: continue

            try:    desc = iptv_utils.Decode(re.compile('<description>(.+?)</description>').search(channel).group(1))
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

            now, next = GetNowNext(desc)

            stream = stream.split('/')

            stream_type         = stream[3]
            stream_id           = stream[6].split('.')[0]
            container_extension = stream[6].split('.')[1]

            item = {}
            item['name']                = title
            item['stream_type']         = stream_type
            item['stream_id']           = stream_id
            item['container_extension'] = container_extension
            item['stream_icon']         = AssertURL(image, title)
            item['now']                 = now
            item['next']                = next
            #item['description']         = '%s[CR][CR]%s' % (now, next)

            cat.append(item)
            #return cat

        return cat

    except Exception as e:
        #iptv_utils.log(e, True)
        return []


def Catchup():
    try:
        username, password = GetCredentials()

        url = ROOT + '/panel_api.php?username=%s&password=%s'  % (username, password)

        response = iptv_utils.GetURL(url, maxSec=3600 * SCALER) # 60 minutes

        items = re.compile('"num":.+?,"name":"(.+?)".+?"stream_id":"(.+?)","stream_icon":"(.+?)".+?"tv_archive":(.+?).+?"tv_archive_duration":(.+?)}').findall(response)

        cat = []

        for item in items:
            tvarchive = item[3]
 
            if tvarchive != '1':
                continue

            name                = item[0]
            stream_id           = item[1]
            stream_icon         = item[2].replace('\/', '/')
            tv_archive_duration = item[4].replace('"', '').replace("['", '').replace("']", '')
 
            item = {}
            item['name']                = name
            item['stream_id']           = stream_id 
            item['stream_icon']         = AssertURL(stream_icon, name)
            item['tv_archive_duration'] = tv_archive_duration

            cat.append(item)

        return cat

    except Exception as e:
        #iptv_utils.log(e, True)
        return []



def CatchupCat(stream_id, tv_archive_duration, search=None):
    try:
        username, password = GetCredentials()

        url = ROOT + '/player_api.php?username=%s&password=%s&action=get_simple_data_table&stream_id=%s'  % (username, password, str(stream_id))

        response = iptv_utils.GetURL(url, maxSec=900 * SCALER) # 15 minutes

        items = re.compile('"title":"(.+?)".+?"start":"(.+?)","end":"(.+?)","description":"(.+?)"').findall(response)

        now     = datetime.datetime.now()
        minimum = now - datetime.timedelta(tv_archive_duration) - datetime.timedelta(hours=2) # extra 2 hours seems okay

        if search:
            search = search.upper()

        cat = []

        for item in items:
            title = iptv_utils.Decode(item[0])
            desc  = iptv_utils.Decode(item[3])
            start = item[1]
            end   = item[2]

            if search:
                if (search not in title.upper()) and (search not in desc.upper() and (search not in start)):
                    continue

            start = iptv_utils.ParseTime(start)
            if start < minimum:
                continue

            end = iptv_utils.ParseTime(end)
            if end > now:
                continue

            item = {}
            item['title']       = title
            item['description'] = desc 
            item['start']       = start
            item['end']         = end

            cat.append(item)

        return cat

    except Exception as e:
        iptv_utils.DialogOK(str(e))
        iptv_utils.log(e, True)
        return []


def GetStreamURL(stream_id, type, ext):
    try:
        username, password = GetCredentials()

        if type == 'created_live':
            type = 'live'

        #port = 8080
        #return '%s:%d/%s/%s/%s/%s.%s' % (ROOT, port, type, username, password, str(stream_id), ext)

        return '%s/%s/%s/%s/%s.%s' % (ROOT, type, username, password, str(stream_id), ext)

    except Exception as e:
        #iptv_utils.log(e, True)
        return None


def GetCatchupStreamURL(stream_id, start, end):
    try:
        username, password = GetCredentials()

        duration = iptv_utils.ParseTime(end) - iptv_utils.ParseTime(start)
        
        start = start.replace(':', '-')
        start = start.replace(' ', ':')
        start = start[:-3]

        duration = duration.seconds / 60

        #port = 4545
        #return '%s:%d/streaming/timeshift.php?username=%s&password=%s&stream=%s&start=%s&duration=%d' % (ROOT, port, username, password, str(stream_id), start, duration)

        return '%s/streaming/timeshift.php?username=%s&password=%s&stream=%s&start=%s&duration=%d' % (ROOT, username, password, str(stream_id), start, duration)

    except Exception as e:
        #iptv_utils.log(e, True)
        return None
