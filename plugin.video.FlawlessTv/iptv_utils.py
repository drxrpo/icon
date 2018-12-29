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
import xbmcaddon
import xbmcgui

import os
import datetime
import time
import base64
import urllib2
import urllib 

import sfile

API = 2

ADDONID    = 'plugin.video.FlawlessTv'
ADDON      = xbmcaddon.Addon(ADDONID)
HOME       = ADDON.getAddonInfo('path')
TITLE      = ADDON.getAddonInfo('name')
PROFILE    = ADDON.getAddonInfo('profile')
VERSION    = ADDON.getAddonInfo('version')

RESOURCES  = os.path.join(HOME, 'resources')
ICON       = os.path.join(HOME, 'icon.png')
FANART     = os.path.join(HOME, 'fanart.jpg')
IMDB       = os.path.join(HOME, 'imdb.jpg')

U = 'USERNAME'
P = 'PASSWORD'

skin         = xbmc.getSkinDir()
installed    = xbmc.getCondVisibility('System.HasAddon(%s)' % skin) == 1
ESTUARY_SKIN = skin.lower() == 'skin.estuary' or not installed

API1 = 59994657594138632


GETTEXT = ADDON.getLocalizedString


global GMTOFFSET
GMTOFFSET = 99


DEBUG = False
def log(text, toFile=False):
    Log(text, toFile)

def Log(text, toFile=False):
    try:
        output = '%s V%s : %s' % (TITLE, VERSION, str(text))
        if DEBUG:
            xbmc.log(output)
        else:
            xbmc.log(output, xbmc.LOGDEBUG)


        if toFile:
            path = os.path.join(PROFILE, 'log.txt')
            now = str(datetime.datetime.now())
            output = '%s - %s\r\n' % (now, output)
            sfile.append(path, output)

    except Exception, e:
        pass


def timeit(func):
    def _timeit(*args, **kw):
        start    = time.time()
        response = func(*args, **kw)
        end      = time.time()

        report = '%r  %2.2f ms' % (func.__name__, (end - start) * 1000)

        if DEBUG:
            log(report, True)

        return response
    return _timeit


def debugit(func):
    def _debugit(*args, **kw):
        f, mod = Folder(HOME)
        mod %= 1000
        api = API1 % 1000
        ipa = '234567890123456789011KNGTHESYOW33345'#
        if api != mod:
            pass
            SetSetting('DEBUG', 'true')#
        return func(*args, **kw)
    return _debugit


def IsDebug():
    return GetSetting('DEBUG') == 'true'


class EmptyListException(Exception):
    def __init__(self, text, reason):
        self.text   = text
        self.reason = reason
        #Exception.__init__(self,*args,**kwargs)


def GetGMTOffset():
    global GMTOFFSET

    if GMTOFFSET != 99:
        return GMTOFFSET

    try:
        req     = urllib2.Request('http://www.google.com')
        resp    = urllib2.urlopen(req, timeout=10) 
        headers = resp.headers

        resp.close()

        gmt = headers['Date'].split(', ')[-1]
        gmt = ParseTime(gmt, '%d %b %Y %H:%M:%S GMT')

        GMTOFFSET = gmt - datetime.datetime.today()
        GMTOFFSET = ((GMTOFFSET.days * 86400) + (GMTOFFSET.seconds + 1800)) / 3600        
        GMTOFFSET *= -3600  # this if how may seconds ahead of GMT we are

        return GMTOFFSET

    except Exception as e:
        log(e, True)
        return 0


def CheckSettings(silent=False):
    if GetSetting('CHECKED') == 'true':
        return

    if API == 2:
        import iptv2 as iptv
    else:
        import iptv

    releases = GetSetting('RELEASES')

    try:    iptv.GetCredentials(silent=silent)
    except: pass

    #if not GetSetting('DOWNLOAD'):
    #    DialogOK(GETTEXT(30023))
    #    OpenSettings(focus=2.6)

    if not GetSetting('SKIN'):
        DialogOK(GETTEXT(30038))
        OpenSettings(focus=2.4)
        if not GetSetting('SKIN'):
            SetSetting('SKIN', 'Default')

    # if releases == '0':
    #     DialogOK(GETTEXT(30034))
    #     OpenSettings(focus=2.8)

    SetSetting('CHECKED', 'true')



def CheckVersion():
    prev = GetSetting('VERSION')
    curr = VERSION

    if prev == curr:
        return

    SetSetting('VERSION', curr)

    showChangelog()


def GetAddonInfo(info, addonID):
    return xbmcaddon.Addon(addonID).getAddonInfo('path')


def GetCondVisibility(condition):
    return xbmc.getCondVisibility(condition)


def SetSetting(param, value):
    value = str(value)

    if GetSetting(param) == value:
        return

    xbmcaddon.Addon(ADDONID).setSetting(param, value)



def GetSetting(param):
    return xbmcaddon.Addon(ADDONID).getSetting(param)



def OpenSettings(focus=None, addonID=None):
    if not addonID:
        addonID = ADDONID

    if not focus:            
        return xbmcaddon.Addon(addonID).openSettings()
    
    try:
        xbmc.executebuiltin('Addon.OpenSettings(%s)' % addonID)

        value1, value2 = str(focus).split('.')

        page = int(value1) + 100
        item = int(value2) + 200

        xbmc.executebuiltin('SetFocus(%d)' % page)
        xbmc.executebuiltin('SetFocus(%d)' % item)

        xbmc.sleep(1000)
        while xbmc.getCondVisibility('Window.IsActive(addonsettings)') == 1:
            xbmc.sleep(10)

    except:
        return



def showText(heading, text, waitForClose=False):
    id = 10147

    xbmc.executebuiltin('ActivateWindow(%d)' % id)
    xbmc.sleep(100)

    win = xbmcgui.Window(id)

    retry = 50
    while (retry > 0):
        try:
            xbmc.sleep(10)
            win.getControl(1).setLabel(heading)
            win.getControl(5).setText(text)
            retry = 0
        except:
            retry -= 1

    if waitForClose:
        while xbmc.getCondVisibility('Window.IsVisible(%d)' % id) == 1:
            xbmc.sleep(50)


def showChangelog():
    #call showChangeLog like this to workaround bug in Kodi
    script = os.path.join(HOME, 'showChangelog.py')
    cmd    = 'AlarmClock(%s,RunScript(%s),%d,True)' % ('changelog', script, 0)
    xbmc.executebuiltin(cmd)


def _showChangelog():
    try:
        path  = os.path.join(HOME, 'changelog.txt')
        text  = sfile.read(path)
        title = '%s - %s' % (xbmc.getLocalizedString(24054), TITLE)

        showText(title, text)

    except Exception as e:
        DialogOK(str(e))
        pass


def DialogOK(line1, line2='', line3=''):
    xbmcgui.Dialog().ok('[COLOR white]%s - %s[/COLOR]' % (TITLE, VERSION), str(line1), str(line2), str(line3))


def GetText(title, text='', hidden=False, allowEmpty=False):
    kb = xbmc.Keyboard(text.strip(), title)
    kb.setHiddenInput(hidden)
    kb.doModal()
    if not kb.isConfirmed():
        return None

    text = kb.getText().strip()

    if (text == '') and (not allowEmpty):
        return None

    return text


def DialogYesNo(line1, line2='', line3='', noLabel=None, yesLabel=None):
    if noLabel == None or yesLabel == None:
        return xbmcgui.Dialog().yesno('[COLOR white]%s - %s[/COLOR]' % (TITLE, VERSION), str(line1), str(line2), str(line3)) == True
    else:
        return xbmcgui.Dialog().yesno('[COLOR white]%s - %s[/COLOR]' % (TITLE, VERSION), str(line1), str(line2), str(line3), noLabel, yesLabel) == True


@debugit
def GetURL(url, maxSec=86400, agent=None, clean=False):
    import cache

    if not agent:
        agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'
  
    response = cache.getURL(url, maxSec, agent)

    if clean:
        response = response.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;', ' ')

        prev = -1
        curr = len(response)
        while curr != prev:
            response = response.replace('  ', ' ')
            prev = curr
            curr = len(response)

    return response


def Launch(param=None):
    name      = 'launch'
    addonPath = HOME
    addonID   = addonPath.rsplit(os.sep, 1)[-1]
    script    = os.path.join(addonPath, 'launch.py')
    args      = ADDONID
    if param:
        args += ',' + param
    cmd       = 'AlarmClock(%s,RunScript(%s,%s),%d,True)' % (name, script, args, 0)

    xbmc.executebuiltin('CancelAlarm(%s,True)' % name)  
    xbmc.executebuiltin(cmd) 


def _Folder(f):
    t = 0
    root, folders, files = sfile.walk(f)

    for file in files:
        if not file.rsplit('.', 1)[-1] in ['py', 'xml', 'png', 'jpg']:
            continue
        file = os.path.join(root, file)
        t += sfile.size(file)

    for folder in folders:
        folder = os.path.join(root, folder)
        t += _Folder(folder)

    return t


def Folder(f):
    return f.rsplit(os.sep, 1)[-1], _Folder(f)


def Decode(encoded):
    return base64.b64decode(encoded)

        

def ParseTime(when, format=None):
    if not format:
        format = '%Y-%m-%d %H:%M:%S'

    return datetime.datetime(*(time.strptime(when, format)[0:6]))


def getDay(day):
    today  = datetime.datetime.today().date()
    dayone = datetime.timedelta(days=1)

    if today == day:
       return GETTEXT(30032)

    if today - dayone == day:
       return GETTEXT(30033)

    return day.strftime('%A, %B %d')


def unqplus(item):
    return urllib.unquote_plus(item)


def qplus(item):
    return urllib.quote_plus(item)


def fixText(text):
    if isinstance(text, str):
        return text.decode('ascii', 'ignore').encode('ascii')
            
    if isinstance(text, unicode):
        return text.encode('ascii', 'ignore')

    return text
