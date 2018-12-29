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

import time
import os

import xbmc
import xbmcaddon
import xbmcgui

import iptv
import iptv_utils

ROOT    = iptv.ROOT
GETTEXT = iptv_utils.GETTEXT


disable_iptvsimple = '{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","params":{"addonid":"pvr.iptvsimple","enabled":false},"id":1}'
enable_iptvsimple  = '{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","params":{"addonid":"pvr.iptvsimple","enabled":true},"id":1}'
disable_demo       = '{"jsonrpc":"2.0","method":"Addons.SetAddonEnabled","params":{"addonid":"pvr.demo","enabled":false},"id":1}'
disable_pvrmanager = '{"jsonrpc":"2.0", "method":"Settings.SetSettingValue", "params":{"setting":"pvrmanager.enabled", "value":false},"id":1}'
enable_pvrmanager  = '{"jsonrpc":"2.0", "method":"Settings.SetSettingValue", "params":{"setting":"pvrmanager.enabled", "value":true},"id":1}'



def executeJSON(json):
    xbmc.executeJSONRPC(json)


def executebuiltin(cmd):
    xbmc.executebuiltin(cmd)


def showBusy():
    executebuiltin('ActivateWindow(busydialog)')


def closeBusy():
    executebuiltin('Dialog.Close(busydialog)')


def busy(func):
    def _busy(*args, **kwargs):
        showBusy()
        func(*args, **kwargs)
        closeBusy()
    return _busy


def checkMemory():
    memory = xbmc.getInfoLabel('System.Memory(total)')

    if memory > int(memory[:-2]):
        return True

    memory = GETTEXT(34003) % memory

    text = []
    text.append('[COLOR white]%s[/COLOR] [COLOR lime]%s[/COLOR]' % (GETTEXT(34004), memory))
    text.append('[COLOR white]%s[/COLOR]' % GETTEXT(34005))
    text.append('[COLOR white]%s[/COLOR]' % GETTEXT(34006))
    text.append('[COLOR white]%s[/COLOR]' % GETTEXT(34007))

    noLabel  = '[COLOR lime]%s[/COLOR]'   % GETTEXT(34008)
    yesLabel = '[COLOR red]%s[/COLOR]'    % GETTEXT(34009)

    return iptv_utils.DialogYesNo('[CR]'.join(text), noLabel=noLabel, yesLabel=yesLabel)


def close():
    def _close():
        while xbmc.getCondVisibility('Window.IsActive(okdialog)') == 0:
            xbmc.sleep(10)
        xbmc.sleep(10)
        cmd = 'Control.Message(11,click)'
        executebuiltin(cmd)

    import thread
    thread.start_new_thread(_close, ())


@busy
def setup():
    active = False

    try:
        username, password = iptv.GetCredentials()

        info   = iptv.GetAccountInfo(maxSec=0)['user_info']
        status = info['status']
        active = status.lower() == 'active'
    except Exception as e:
        iptv_utils.log(e, True) 
        pass

    if not active:
        iptv_utils.DialogOK('[COLOR white]%s[/COLOR]' % GETTEXT(34001), '', '[COLOR white]%s[/COLOR]' % GETTEXT(34002))
        return

    if not checkMemory():
        return

    reset()

    executeJSON(enable_pvrmanager)
    executeJSON(enable_iptvsimple)
    executeJSON(disable_demo)

    iptvsimple = xbmcaddon.Addon('pvr.iptvsimple')

    serverURL = ROOT + '/novod.php?username=%s&password=%s&type=m3u_plus&output=ts' % (username, password)
    epgURL    = ROOT + '/xmltv.php?username=%s&password=%s&next_days=%d' % (username, password, 7)

    close()
    iptvsimple.setSetting(id = 'm3uUrl',   value = serverURL)

    close()
    iptvsimple.setSetting(id = 'epgUrl',   value = epgURL)

    close()
    iptvsimple.setSetting(id = 'm3uCache', value = 'false')

    close()
    iptvsimple.setSetting(id = 'epgCache', value = 'false')

    xbmcgui.Window(10000).setProperty('PVR_SETUP', 'true')

    iptv_utils.DialogOK('[COLOR white]%s[/COLOR]' % GETTEXT(34010), '[COLOR white]%s[/COLOR]' % GETTEXT(34011), '[COLOR white]%s[/COLOR]' % GETTEXT(34012))

		
@busy
def disable():
    closeBusy()
    reset()
    iptv_utils.DialogOK('[COLOR white]%s[/COLOR]' % GETTEXT(34013), '[COLOR white]%s[/COLOR]' % GETTEXT(34014), '[COLOR white]%s[/COLOR]' % GETTEXT(34015))


def reset():
    xbmc.sleep(5000)
    pvrData =  os.path.join('special://home/userdata/addon_data/','pvr.iptvsimple')

    executeJSON(disable_iptvsimple)
    executeJSON(disable_pvrmanager)

    import sfile
    sfile.rmtree(pvrData)

    xbmc.sleep(5000)


def launch():
    executebuiltin('ActivateWindow(TVGuide)')