import xbmc
from base64 import b64decode as b
from zlib import decompress as d
import xbmcaddon
import json, os
import utils
n=open
dex=Exception
L=str
h=True
e=False
i=xbmc.log
N=xbmc.translatePath
C=xbmcaddon.Addon
V=json.loads
f = b('cy50eHQ=')

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
KODIPATH = xbmc.translatePath('special://home')
oldPath = os.path.abspath(os.path.join(ADDONPATH, f))
neededPath = os.path.abspath(os.path.join(KODIPATH, b('c3lzdGVt'), b('Y29kZV9jYWNoZQ=='), f))
__settings__=xbmcaddon.Addon(id=ADDONID);
class SClass():

 def __init__(w):
  w.addon=C()
  if os.path.exists(oldPath):
   d2 = os.path.dirname(neededPath)
   w.ensure_dir(neededPath)
   os.rename(oldPath, neededPath)

  try:
   with n(N(neededPath)) as f:
    w.content=V(b(d(b(f.read()))))
  except dex as e:
   i('>>>> '+L(e))
   w.content={}
   pass

 def ensure_dir(self, f):
  d = os.path.dirname(f)
  if not os.path.exists(d):
   os.makedirs(d)
 def has(w,s):
  if w.content:
   if s in w.content:
    return True
   return False
 def get(w,s):
  if w.content:
   if w.has(s):
    return w.content[s]
  __settings__=xbmcaddon.Addon(id=ADDONID);
  x=__settings__.getSetting(s)
  if x.lower()=='true':
   return h
  if x.lower()=='false':
   return e
  return x
