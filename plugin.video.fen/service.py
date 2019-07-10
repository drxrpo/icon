
import time,datetime
import xbmc
from resources.lib.modules import settings
from datetime import date, timedelta
# from resources.lib.modules.utils import logger

__addon__ = settings.addon()

class AutoUpdater:             
    def runProgram(self):
        xbmc.log("[FEN] Subscription service starting...")
        hours = settings.subscription_timer()
        while not xbmc.abortRequested:
            if settings.subscription_update():
                try:
                    next_run  = datetime.datetime.fromtimestamp(time.mktime(time.strptime(__addon__.getSetting('service_time').encode('utf-8', 'replace'), "%Y-%m-%d %H:%M:%S")))
                    now = datetime.datetime.now()
                    if now > next_run:
                        if xbmc.Player().isPlaying() == False:
                            if xbmc.getCondVisibility('Library.IsScanningVideo') == False:      
                                xbmc.log("[FEN'] Updating video subscriptions")
                                time.sleep(1)
                                xbmc.executebuiltin('RunPlugin(plugin://plugin.video.fen/?&mode=update_subscriptions)')
                                time.sleep(1)
                                __addon__.setSetting('service_time', str(datetime.datetime.now() + timedelta(hours=hours)).split('.')[0])
                                xbmc.log("[FEN] Subscriptions updated. Next run at " + __addon__.getSetting('service_time'),2)
                        else:
                            xbmc.log("[FEN] Player is running, waiting until finished")
                except: pass
            xbmc.sleep(5000)

AutoUpdater().runProgram()
