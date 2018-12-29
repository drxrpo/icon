import xbmcplugin,xbmcaddon
import time
import datetime
import xbmc
import os
import urllib2,json
import zipfile
import lib.utils as utils
from lib.croniter import croniter
from collections import namedtuple
from shutil import copyfile
import traceback
import plugintools
from lib import vader
from xbmcaddon import Addon

from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SocketServer import ThreadingMixIn
from threading import Thread

jsonGetPVR = '{"jsonrpc":"2.0", "method":"Settings.GetSettingValue", "params":{"setting":"pvrmanager.enabled"}, "id":1}'
jsonSetPVR = '{"jsonrpc":"2.0", "method":"Settings.SetSettingValue", "params":{"setting":"pvrmanager.enabled", "value":%s},"id":1}'
jsonNotify = '{"jsonrpc":"2.0", "method":"GUI.ShowNotification", "params":{"title":"PVR", "message":"%s","image":""}, "id":1}'


__addon__ = xbmcaddon.Addon()

ADDONNAME = __addon__.getAddonInfo('name')
ADDONID = __addon__.getAddonInfo('id')

__author__ = __addon__.getAddonInfo('author')
__scriptid__ = __addon__.getAddonInfo('id')
__scriptname__ = __addon__.getAddonInfo('name')
__cwd__ = __addon__.getAddonInfo('path')
__version__ = __addon__.getAddonInfo('version')
debug = __addon__.getSetting("debug")


MyAddon = Addon(ADDONID)
PORT_NUMBER = int(62555)

offset = time.timezone if (time.localtime().tm_isdst == 0) else time.altzone
offset = offset / 60 / 60 * -1


class http_server:
    def __init__(self, vaderClass, portNumber):
        self.portNumber = portNumber
        self.vaderClass = vaderClass
        utils.log('INIT HTTP SERVER')
        try:
            serverThread = Thread(target=self.start_server)
            serverThread.daemon = True  # Do not make us wait for you to exit
            serverThread.start()
        except:
            utils.log('Http server died')
            pass


    def start_server(self):
        server = HTTPServer(('', self.portNumber), myHandler)
        server.vaderClass = self.vaderClass
        utils.log('HTTP Proxy started')
        server.serve_forever()


class myHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if '/playLiveAddon/' in self.path:
            streamId = self.path[2:].split('/playLiveAddon/')[1].strip()
            url = self.server.vaderClass.build_stream_url(streamId)
            self.send_response(302)
            self.send_header('Location', url)
            self.end_headers()
            self.finish()

        if '/playLive/' in self.path:
            streamId = self.path[2:].split('/playLive/')[1].strip()
            url = self.server.vaderClass.build_stream_url(streamId, pvr=True)
            self.send_response(302)
            self.send_header('Location', url)
            self.end_headers()
            self.finish()
        if '/getAddonID' in self.path:
            self.send_response(200)
            self.send_header("Content-type", "text/html")

            self.end_headers()
            self.wfile.write(ADDONID)

            self.wfile.close()

        if '/getCategories' in self.path:
            self.send_response(200)
            self.send_header("Content-type", "text/html")

            self.end_headers()
            self.wfile.write(self.server.vaderClass.get_epg_categories())

            self.wfile.close()

        if '/getStreams' in self.path:
            self.send_response(200)
            self.send_header("Content-type", "text/html")

            self.end_headers()
            streams = json.dumps(self.server.vaderClass.get_valid_streams())
            self.wfile.write(streams)

            self.wfile.close()


        if '/getCreds' in self.path:
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            username = self.server.vaderClass.username
            password = self.server.vaderClass.password
            data = {}
            data['username'] = username
            data['password'] = password
            self.end_headers()
            dataDump = json.dumps(data)
            self.wfile.write(dataDump)

            self.wfile.close()


    def do_HEAD(self):
      self.send_response(200)
      self.send_header('Content-type', 'video/mp2t')
      self.end_headers()
      self.finish()




class epgUpdater:
    def __init__(self, vaderClass):
        self.monitor = UpdateMonitor(update_method = self.settingsChanged)
        self.enable_kodi_library = plugintools.get_setting("enable_kodi_library")
        self.vaderClass = vaderClass
        self.authString = self.vaderClass.authString
        self.next_run = 0

        try:
          self.VADER_addon = xbmcaddon.Addon(ADDONID)
          utils.setSetting("pluginmissing", "false")

        except Exception as e:
            plugintools.log("Error finding vader \n{0}\n{1}".format(e, traceback.format_exc()))
            utils.log("Failed to find {addonName} addon".format(addonName=ADDONNAME))
            self.VADER_addon = None
            utils.setSetting("pluginmissing", "true")

        try:
          self.pvriptvsimple_addon = xbmcaddon.Addon('pvr.iptvsimple')

        except Exception as e:
          utils.log("Failed to find pvr.iptvsimple addon")
          self.pvriptvsimple_addon = None

    def run(self):
        try:
            utils.log("scheduler enabled, finding next run time")
            self.server = http_server(self.vaderClass, PORT_NUMBER)

            self.findNextRun(time.time())
            try:
                self.vaderClass.generate_strm_files()

                # httpd = HTTPServer(('', PORT_NUMBER), myHandler)
                # httpd_thread = Thread(target=httpd.serve_forever)
                # httpd_thread.start()
            except Exception as e:
                utils.log("failed to start http server \n{0}\n{1}".format(e, traceback.format_exc()))
                pass
        except Exception as e:
            utils.log("Error in service.py  \n{0}\n{1}".format(e, traceback.format_exc()))
            pass

        self.findNextRun(time.time())
        while(not xbmc.abortRequested):
            # Sleep/wait for abort for 10 seconds
            now = time.time()

            if(self.enable_kodi_library):
              if(self.next_run <= now):
                  if self.authString == 'Active':
                      utils.log('disabled vod sync')
                      # self.vaderClass.generate_strm_files()
                  self.findNextRun(now)
              else:
                  self.findNextRun(now)

            xbmc.sleep(500)
        # del self.monitor

    def settingsChanged(self):
        try:

            # utils.log("Settings changed - update")
            old_settings = utils.refreshAddon()


            if plugintools.get_setting("enable_kodi_library") == 'true' and old_settings.getSetting('enable_kodi_library') == 'false':
                self.vaderClass.generate_strm_files()
                self.enable_kodi_library = plugintools.get_setting('enable_kodi_library')

            if (plugintools.get_setting("username") != vaderClass.username
                or (plugintools.get_setting("password") != vaderClass.password )):

                utils.log("Settings changed - update user/pass : " + plugintools.get_setting("username")  + " : " + old_settings.getSetting('username') )
                self.vaderClass.deleteAllCache()
                self.vaderClass.updateUserPass()
                self.authString = self.vaderClass.authorise()
                if self.authString == 'Active':
                    self.vaderClass.generate_strm_files()

            if (utils.getSetting("categorySetupLastSet") != old_settings.getSetting('categorySetupLastSet')):
                utils.log("Settings changed - update categories")
                self.vaderClass.deleteAllCache()
                self.vaderClass.updatePVRSettings()
                self.vaderClass.set_enabled_categories()






        except Exception as e:
            utils.log("Error updating settings \n{0}\n{1}".format(e, traceback.format_exc()))
            pass

    def parseSchedule(self):
        schedule_type = int(utils.getSetting("schedule_interval"))
        cron_exp = utils.getSetting("cron_schedule")

        hour_of_day = utils.getSetting("schedule_time")
        hour_of_day = int(hour_of_day[0:2])
        if(schedule_type == 0 or schedule_type == 1):
            #every day
            cron_exp = "0 " + str(hour_of_day) + " * * *"
        elif(schedule_type == 2):
            #once a week
            day_of_week = utils.getSetting("day_of_week")
            cron_exp = "0 " + str(hour_of_day) + " * * " + day_of_week
        elif(schedule_type == 3):
            #first day of month
            cron_exp = "0 " + str(hour_of_day) + " 1 * *"

        return cron_exp



    def updateEpg(self):
        epgFileName = 'p2.xml.gz'
        epgFile = None
        if self.VADER_addon is None:
            updater_path = os.path.join(xbmc.translatePath('special://userdata'), 'addon_data/'+ADDONID)
        else:
            updater_path = os.path.join(xbmc.translatePath('special://userdata'), 'addon_data/'+ADDONID)
        iptvsimple_path = os.path.join(xbmc.translatePath('special://userdata'), 'addon_data/pvr.iptvsimple')
        if not os.path.exists(iptvsimple_path):
            os.makedirs(iptvsimple_path)

        try:
            response = urllib2.urlopen('http://repo.vaders.tv/'+epgFileName)
            epgFile = response.read()
        except Exception as e:
            utils.log('StalkerSettings: Some issue with epg file')
            utils.log('{0}\n{1}'.format(e, traceback.format_exc()))


        if epgFile:
            epgFH = open(updater_path + '/VADER_xmltv.xml.gz', "wb")
            epgFH.write(epgFile)
            epgFH.close()


    def findNextRun(self,now):
        #find the cron expression and get the next run time
        cron_exp = self.parseSchedule()
        cron_ob = croniter(cron_exp,datetime.datetime.fromtimestamp(now))
        new_run_time = cron_ob.get_next(float)
        # utils.log('new run time' +  str(new_run_time))
        # utils.log('next run time' + str(self.next_run))
        if(new_run_time != self.next_run):
            self.next_run = new_run_time
            self.updateEpg()
            # utils.showNotification('EPG Updater', 'Next Update: ' + datetime.datetime.fromtimestamp(self.next_run).strftime('%m-%d-%Y %I:%M %p'))
            utils.log("scheduler will run again on " + datetime.datetime.fromtimestamp(self.next_run).strftime('%m-%d-%Y %I:%M %p'))

class UpdateMonitor(xbmc.Monitor):
    update_method = None

    def __init__(self,*args, **kwargs):
        xbmc.Monitor.__init__(self)
        self.update_method = kwargs['update_method']

    def onSettingsChanged(self):
        self.update_method()

if __name__ == "__main__":
    authString = "Not Ready"
    tries = 0
    vaderClass = vader.vader(service=True)
    authString = vaderClass.authString
    if vaderClass.authString == "Active":
        epg_updater = epgUpdater(vaderClass)
        epg_updater.run()
