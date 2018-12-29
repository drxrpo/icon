import xbmc
import xbmcgui
import xbmcaddon
import xbmcvfs
import sys
import re
import os
import shutil
from sclass import SClass

__addon__ = xbmcaddon.Addon()
__author__ = __addon__.getAddonInfo('author')
__scriptid__ = __addon__.getAddonInfo('id')
__addon_id__ = __scriptid__
clas = SClass()

def delete(d, isdir=False):
    """
    Safely removes files or directories if they exist
    """
    try:
        if os.path.exists(d):
            if isdir:
                shutil.rmtree(d)
            else:
                os.remove(d)
    except Exception as e:
        xbmc.log('Failed to delete data: {0}'.format(str(e)))

def ensure_dir(f):
    d = os.path.dirname(f)

    if not os.path.exists(d):
        os.makedirs(d)

def natural_sort(list, key=lambda s:s):
    """
    Sort the list into natural alphanumeric order.
    """
    def get_alphanum_key_func(key):
        convert = lambda text: int(text) if text.isdigit() else text
        return lambda s: [convert(c) for c in re.split('([0-9]+)', key(s))]
    sort_key = get_alphanum_key_func(key)
    list.sort(key=sort_key)

def check_data_dir():
    if(not xbmcvfs.exists(xbmc.translatePath(data_dir()))):
        xbmcvfs.mkdir(xbmc.translatePath(data_dir()))

def data_dir():
    return __addon__.getAddonInfo('profile')

def addon_dir():
    return __addon__.getAddonInfo('path')

def log(message,loglevel=xbmc.LOGNOTICE):
    message = decode(message)
    try:
        xbmc.log(encode(__addon_id__ + "-" + __addon__.getAddonInfo('version') + " : " + message),level=loglevel)
    except:
        xbmc.log('failed to log message')
        pass


def showNotification(title,message):
    xbmcgui.Dialog().notification(encode(getString(30000)),encode(message),time=4000,icon=xbmc.translatePath(__addon__.getAddonInfo('path') + "/icon.png"),sound=False)

def setSetting(name,value):
    if not clas.has(value):
        __addon__.setSetting(name,value)

def getSetting(name):
    return clas.get(name)

def refreshAddon():
    # log("Updated addon")
    global __addon__
    old_addon = __addon__
    __addon__ = xbmcaddon.Addon()
    return old_addon

def getString(string_id):
    return __addon__.getLocalizedString(string_id)

def encode(string):
    return string.encode('utf-8','ignore')

def decode(string):
    return string.decode('ascii', 'ignore')

class xbmcDialogSelect:
    def __init__(self,heading='Options'):
        self.heading = heading
        self.items = []

    def addItem(self,ID,display):
        self.items.append((ID,display))

    def getResult(self):
        IDs = [i[0] for i in self.items]
        displays = [i[1] for i in self.items]
        idx = xbmcgui.Dialog().select(self.heading,displays)
        if idx < 0: return None
        return IDs[idx]

    def getIndex(self):
        displays = [i[1] for i in self.items]
        idx = xbmcgui.Dialog().select(self.heading,displays)
        if idx < 0: return None
        return idx

def ERROR(txt='',hide_tb=False,notify=False):
    if isinstance (txt,str): txt = txt.decode("utf-8")
    short = str(sys.exc_info()[1])
    if hide_tb:
        LOG('ERROR: {0} - {1}'.format(txt,short))
        return short
    print "_________________________________________________________________________________"
    LOG('ERROR: ' + txt)
    import traceback
    tb = traceback.format_exc()
    for l in tb.splitlines(): print '    ' + l
    print "_________________________________________________________________________________"
    print "`"
    if notify: showNotification('ERROR: {0}'.format(short))
    return short

def LOG(message):
    message = '{0}: {1}'.format(__addon_id__,message)
    xbmc.log(msg=message, level=xbmc.LOGNOTICE)

class xbmcDialogProgress:
    def __init__(self,heading,line1='',line2='',line3='',update_callback=None):
        self.heading = heading
        self.line1 = line1
        self.line2 = line2
        self.line3 = line3
        self._updateCallback = update_callback
        self.lastPercent = 0
        self.setRange()
        self.dialog = xbmcgui.DialogProgress()

    def __enter__(self):
        self.create(self.heading,self.line1,self.line2,self.line3)
        self.update(0,self.line1,self.line2,self.line3)
        return self

    def __exit__(self,etype, evalue, traceback):
        self.close()

    def setRange(self,start=0,end=100):
        self.start = start
        self.end = end
        self.range = end - start

    def recalculatePercent(self,pct):
        #print '%s - %s %s %s' % (pct,self.start,self.range,self.start + int((pct/100.0) * self.range))
        return self.start + int((pct/100.0) * self.range)

    def create(self,heading,line1='',line2='',line3=''):
        self.dialog.create(heading,line1,line2,line3)

    def update(self,pct,line1='',line2='',line3=''):
        if self.dialog.iscanceled():
            return False
        pct = self.recalculatePercent(pct)
        if pct < self.lastPercent: pct = self.lastPercent
        self.lastPercent = pct
        self.dialog.update(pct,line1,line2,line3)
        return True

    def updateSimple(self,message):
        pct = 0
        if hasattr(message,'percent'): pct = message.percent
        return self.update(pct,message)

    def updateCallback(self,a):
        if self._updateCallback: return self._updateCallback(self,a)
        return True

    def iscanceled(self):
        return self.dialog.iscanceled()

    def close(self):
        self.dialog.close()
