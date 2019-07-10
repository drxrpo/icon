# -*- coding: utf-8 -*-

'''
    Simple XBMC Download Script
    Copyright (C) 2013 Sean Poyser (seanpoyser@gmail.com)

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''


import re
import json
import sys        
import urllib
import urllib2
import urlparse
import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin
import xbmcvfs
import os
import inspect

def download(name, image, url):
    from resources.lib.modules import settings
    # from resources.lib.modules.utils import logger
    if url == None:
        from resources.lib.modules.nav_utils import notification
        notification('No URL found for Download. Pick another Source', 6000)
        return

    params = dict(urlparse.parse_qsl(sys.argv[2].replace('?','')))
    json_meta = params.get('meta')
    if json_meta:
        meta = json.loads(json_meta)
        db_type = meta.get('vid_type')
        title = meta.get('title')
        year = meta.get('year')
        image = meta.get('poster')
        season = meta.get('season')
        episode = meta.get('episode')
    else:
        db_type = params.get('db_type')
        image = params.get('image')

    media_folder = settings.download_directory(db_type)
    if not media_folder:
        resp = xbmcgui.Dialog().yesno(
            "No Download folder set!",
            "Fen requires you to set Download Folders.",
            "Would you like to set a folder now?")
        if resp:
            from resources.lib.modules.nav_utils import open_settings
            open_settings('7.0')
        else:
            return
    if db_type in ('movie', 'episode'):
        folder_rootname = '%s (%s)' % (title, year)
        folder = os.path.join(media_folder, folder_rootname + '/')
    else:
        folder = media_folder
    if not xbmcvfs.exists(folder): xbmcvfs.mkdir(folder)
    if db_type == 'episode':
        folder = os.path.join(folder, 'Season ' + str(season))
        if not xbmcvfs.exists(folder): xbmcvfs.mkdir(folder)

    try: headers = dict(urlparse.parse_qsl(url.rsplit('|', 1)[1]))
    except: headers = dict('')
    dest = None
    url = url.split('|')[0]
    if not 'http' in url:
        from resources.lib.modules.furk_api import FurkAPI
        from resources.lib.indexers.furk import filter_furk_tlist, seas_ep_query_list
        t_files = FurkAPI().t_files(url)
        t_files = [i for i in t_files if 'video' in i['ct'] and 'bitrate' in i]
        name, url = filter_furk_tlist(t_files, (None if db_type == 'movie' else seas_ep_query_list(season, episode)))[0:2]
        dest = os.path.join(folder, name)
    if db_type == 'archive':
        ext = 'zip'
    else:
        ext = os.path.splitext(urlparse.urlparse(url).path)[1][1:]
        if not ext in ['mp4', 'mkv', 'flv', 'avi', 'mpg']: ext = 'mp4'

    
    if not dest:
        transname = name.translate(None, '\/:*?"<>|').strip('.')
        dest = os.path.join(folder, transname + '.' + ext)
    sysheaders = urllib.quote_plus(json.dumps(headers))
    sysurl = urllib.quote_plus(url)
    systitle = urllib.quote_plus(name)
    sysimage = urllib.quote_plus(image)
    sysdest = urllib.quote_plus(dest)

    script = inspect.getfile(inspect.currentframe())
    cmd = 'RunScript(%s, %s, %s, %s, %s, %s)' % (script, sysurl, sysdest, systitle, sysimage, sysheaders)

    xbmc.executebuiltin(cmd)

def getResponse(url, headers, size):
    try:
        if size > 0:
            size = int(size)
            headers['Range'] = 'bytes=%d-' % size

        req = urllib2.Request(url, headers=headers)

        resp = urllib2.urlopen(req, timeout=30)
        return resp
    except:
        return None

def done(title, dest, downloaded):
    playing = xbmc.Player().isPlaying()

    text = xbmcgui.Window(10000).getProperty('FEN-DOWNLOADED')

    if len(text) > 0:
        text += '[CR]'

    if downloaded:
        text += '%s : %s' % (dest.rsplit(os.sep)[-1], '[COLOR forestgreen]Download succeeded[/COLOR]')
    else:
        text += '%s : %s' % (dest.rsplit(os.sep)[-1], '[COLOR red]Download failed[/COLOR]')

    xbmcgui.Window(10000).setProperty('FEN-DOWNLOADED', text)

    if (not downloaded) or (not playing): 
        xbmcgui.Dialog().ok(title, text)
        xbmcgui.Window(10000).clearProperty('FEN-DOWNLOADED')

def doDownload(url, dest, title, image, headers):
    _addon__ = xbmcaddon.Addon(id='plugin.video.fen')
    headers = json.loads(urllib.unquote_plus(headers))
    url = urllib.unquote_plus(url)
    title = urllib.unquote_plus(title)
    image = urllib.unquote_plus(image)
    dest = urllib.unquote_plus(dest)
    file = dest.rsplit(os.sep, 1)[-1]
    resp = getResponse(url, headers, 0)

    if not resp:
        xbmcgui.Dialog().ok(title, dest, 'Download failed', 'No response from server')
        return

    try:    content = int(resp.headers['Content-Length'])
    except: content = 0

    try:    resumable = 'bytes' in resp.headers['Accept-Ranges'].lower()
    except: resumable = False

    if resumable:
        print "Download is resumable"

    if content < 1:
        xbmcgui.Dialog().ok(title, file, 'Unknown filesize', 'Unable to download')
        return

    size = 1024 * 1024
    mb   = content / (1024 * 1024)

    if content < size:
        size = content

    total   = 0
    notify  = 0
    errors  = 0
    count   = 0
    resume  = 0
    sleep   = 0

    if xbmcgui.Dialog().yesno('Fen' + ' - Confirm Download', file, 'Complete file is %dMB' % mb, 'Continue with download?', 'Confirm',  'Cancel') == 1:
        return

    print 'Download File Size : %dMB %s ' % (mb, dest)

    f = xbmcvfs.File(dest, 'w')

    chunk  = None
    chunks = []

    show_notifications = True if _addon__.getSetting('download.notification') == '0' else False
    suppress_during_playback = True if _addon__.getSetting('download.suppress') == 'true' else False
    try: notification_frequency = int(_addon__.getSetting('download.frequency'))
    except: notification_frequency = 10

    while True:
        playing = xbmc.Player().isPlaying()
        downloaded = total
        for c in chunks:
            downloaded += len(c)
        percent = min(100 * downloaded / content, 100)
        if percent >= notify:
            if show_notifications:
                if playing and not suppress_during_playback:
                    xbmc.executebuiltin( "XBMC.Notification([B]%s[/B],[I]%s[/I],%i,%s)" % ('Download Progress: ' + str(percent)+'%', title, 10000, image))
                elif (not playing):
                    xbmc.executebuiltin( "XBMC.Notification([B]%s[/B],[I]%s[/I],%i,%s)" % ('Download Progress: ' + str(percent)+'%', title, 10000, image))

                notify += notification_frequency

        chunk = None
        error = False

        try:        
            chunk  = resp.read(size)
            if not chunk:
                if percent < 99:
                    error = True
                else:
                    while len(chunks) > 0:
                        c = chunks.pop(0)
                        f.write(c)
                        del c

                    f.close()
                    return done(title, dest, True)

        except Exception, e:
            print str(e)
            error = True
            sleep = 10
            errno = 0

            if hasattr(e, 'errno'):
                errno = e.errno

            if errno == 10035: # 'A non-blocking socket operation could not be completed immediately'
                pass

            if errno == 10054: #'An existing connection was forcibly closed by the remote host'
                errors = 10 #force resume
                sleep  = 30

            if errno == 11001: # 'getaddrinfo failed'
                errors = 10 #force resume
                sleep  = 30

        if chunk:
            errors = 0
            chunks.append(chunk)
            if len(chunks) > 5:
                c = chunks.pop(0)
                f.write(c)
                total += len(c)
                del c

        if error:
            errors += 1
            count  += 1
            xbmc.sleep(sleep*1000)

        if (resumable and errors > 0) or errors >= 10:
            if (not resumable and resume >= 50) or resume >= 500:
                #Give up!
                return done(title, dest, False)

            resume += 1
            errors  = 0
            if resumable:
                chunks  = []
                #create new response
                resp = getResponse(url, headers, total)
            else:
                #use existing response
                pass


if __name__ == '__main__':
    if 'downloader.py' in sys.argv[0]:
        doDownload(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])


