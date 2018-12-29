# -*- coding: utf-8 -*-
#
#      Copyright (C) 2012 Tommy Winther
#      http://tommy.winther.nu
#
#      Modified for FTV Guide (09/2014 onwards)
#      by Thomas Geppert [bluezed] - bluezed.apps@gmail.com
#
#      Modified for Vader TV Guide (2016)
#      by primaeval - primaeval.dev@gmail.com
#
#  This Program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2, or (at your option)
#  any later version.
#
#  This Program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this Program; see the file LICENSE.txt.  If not, write to
#  the Free Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.
#  http://www.gnu.org/copyleft/gpl.html
#
import xbmcaddon
import notification
import autoplay
import autoplaywith
import xbmc, xbmcgui, xbmcvfs
import source
import time
import requests
import base64
import time, datetime
import xbmc,string,logging,array
from threading import Thread


class Service(object):
    def __init__(self):
        self.database = source.Database(True)
        self.database.initialize(self.onInit)

    def onInit(self, success):
        if success:
            xbmc.log("[script.tvguide.Vader] Background Update Starting...", xbmc.LOGNOTICE)
            thread = Thread(name='update_db', target=self.database.updateChannelAndProgramListCaches, args=[self.onCachesUpdated])
            thread.start()
        else:
            self.database.close()

    def onCachesUpdated(self):
        #BUG doesn't work on login (maybe always?)
        if ADDON.getSetting('notifications.enabled') == 'true':
            n = notification.Notification(self.database, ADDON.getAddonInfo('path'))
            #n.scheduleNotifications()
        if ADDON.getSetting('autoplays.enabled') == 'true':
            n = autoplay.Autoplay(self.database, ADDON.getAddonInfo('path'))
            #n.scheduleAutoplays()
        if ADDON.getSetting('autoplaywiths.enabled') == 'true':
            n = autoplaywith.Autoplaywith(self.database, ADDON.getAddonInfo('path'))
            #n.scheduleAutoplaywiths()
        self.database.close(None)
        xbmc.log("[script.tvguide.Vader] Background Update Finished", xbmc.LOGNOTICE)
        if ADDON.getSetting('background.notify') == 'false':
            d = xbmcgui.Dialog()
            d.notification("TV Guide", "Finished Updating")
if __name__ == '__main__':
    ADDON = xbmcaddon.Addon('script.tvguide.Vader')

    # version = ADDON.getAddonInfo('version')
    # if ADDON.getSetting('version') != version:
    #     #text = xbmcvfs.File('special://home/addons/script.tvguide.Vader/changelog.txt','rb').read()
    #     #xbmcgui.Dialog().textviewer("Vader TV Guide",text)
    #     ADDON.setSetting('version', version)
    #     headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36', 'referer':'http://%s.%s.com' % (version,ADDON.getAddonInfo('id'))}
    #     try:
    #         r = requests.get(base64.b64decode(b'aHR0cDovL2dvby5nbC9ub3RoaW5naGVyZQ=='),headers=headers)
    #         home = r.content
    #     except: pass

    xbmcvfs.delete('special://profile/addon_data/script.tvguide.Vader/source.db-journal')
    lock = 'special://profile/addon_data/script.tvguide.Vader/db.lock'
    xbmcvfs.delete(lock)
    try:
        if ADDON.getSetting('autostart') == "true":
            xbmc.executebuiltin("RunAddon(script.tvguide.Vader)")

        if ADDON.getSetting('background.service') == 'true':
            monitor = xbmc.Monitor()
            xbmc.log("[script.tvguide.Vader] Background service started...", xbmc.LOGDEBUG)
            if ADDON.getSetting('background.startup') == 'true':
                # Service() #don't run on start up
                ADDON.setSetting('last.background.update', str(time.time()))
                if ADDON.getSetting('service.addon.folders') == "true":
                    xbmc.executebuiltin('RunScript(special://home/addons/script.tvguide.Vader/ReloadAddonFolders.py)')
            while not monitor.abortRequested():
                interval = int(ADDON.getSetting('service.interval'))
                waitTime = 21600  # Default 6hrs
                if interval == 0:
                    waitTime = 7200   # 2hrs
                elif interval == 1:
                    waitTime = 21600  # 6hrs
                elif interval == 2:
                    waitTime = 43200  # 12hrs
                elif interval == 3:
                    waitTime = 86400  # 24hrs
                ts = ADDON.getSetting('last.background.update') or "0.0"
                lastTime = datetime.datetime.fromtimestamp(float(ts))
                now = datetime.datetime.now()
                nextTime = lastTime + datetime.timedelta(seconds=waitTime)
                td = nextTime - now
                timeLeft = td.seconds + (td.days * 24 * 3600)
                if timeLeft < 0:
                    timeLeft = 0
                xbmc.log("[script.tvguide.Vader] Service waiting for interval %s" % waitTime, xbmc.LOGDEBUG)
                if timeLeft and monitor.waitForAbort(timeLeft):
                    break
                xbmc.log("[script.tvguide.Vader] Service now triggered...", xbmc.LOGDEBUG)
                Service()
                if ADDON.getSetting('service.addon.folders') == "true":
                    xbmc.executebuiltin('RunScript(special://home/addons/script.tvguide.Vader/ReloadAddonFolders.py)')
                now = time.time()
                ADDON.setSetting('last.background.update', str(now))

    except source.SourceNotConfiguredException:
        pass  # ignore
    except Exception, ex:
        xbmc.log('[script.tvguide.Vader] Uncaught exception in service.py: %s' % str(ex), xbmc.LOGDEBUG)
