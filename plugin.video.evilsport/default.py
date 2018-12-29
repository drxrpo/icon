# -*- coding: utf-8 -*-
import urllib
import urllib2
import re
import os
import xbmcplugin
import xbmcgui
import xbmcaddon
import xbmcvfs
import traceback
import cookielib , base64
if 64 - 64: i11iIiiIii
OO0o = base64 . b64decode ( b'aHR0cDovL3N1cGVybXlzcGFjZS54eXovRUtTUE9SVC9FS1NQT1JULnBocA==' )
from BeautifulSoup import BeautifulStoneSoup , BeautifulSoup , BeautifulSOAP
Oo0Ooo = None
try :
 from xml . sax . saxutils import escape
except : traceback . print_exc ( )
try :
 import json
except :
 import simplejson as json
import SimpleDownloader as downloader
import time
if 85 - 85: OOO0O0O0ooooo % IIii1I . II1 - O00ooooo00
if 32 - 32: ooOoO + iIiiiI1IiI1I1 * IIiIiII11i * o0oOOo0O0Ooo
I1ii11iIi11i = False
if 48 - 48: oO0o / OOooOOo / I11i / Ii1I
IiiIII111iI = [ '180upload.com' , 'allmyvideos.net' , 'bestreams.net' , 'clicknupload.com' , 'cloudzilla.to' , 'movshare.net' , 'novamov.com' , 'nowvideo.sx' , 'videoweed.es' , 'daclips.in' , 'datemule.com' , 'fastvideo.in' , 'faststream.in' , 'filehoot.com' , 'filenuke.com' , 'sharesix.com' , 'plus.google.com' , 'picasaweb.google.com' , 'gorillavid.com' , 'gorillavid.in' , 'grifthost.com' , 'hugefiles.net' , 'ipithos.to' , 'ishared.eu' , 'kingfiles.net' , 'mail.ru' , 'my.mail.ru' , 'videoapi.my.mail.ru' , 'mightyupload.com' , 'mooshare.biz' , 'movdivx.com' , 'movpod.net' , 'movpod.in' , 'movreel.com' , 'mrfile.me' , 'nosvideo.com' , 'openload.io' , 'played.to' , 'bitshare.com' , 'filefactory.com' , 'k2s.cc' , 'oboom.com' , 'rapidgator.net' , 'uploaded.net' , 'primeshare.tv' , 'bitshare.com' , 'filefactory.com' , 'k2s.cc' , 'oboom.com' , 'rapidgator.net' , 'uploaded.net' , 'sharerepo.com' , 'stagevu.com' , 'streamcloud.eu' , 'streamin.to' , 'thefile.me' , 'thevideo.me' , 'tusfiles.net' , 'uploadc.com' , 'zalaa.com' , 'uploadrocket.net' , 'uptobox.com' , 'v-vids.com' , 'veehd.com' , 'vidbull.com' , 'videomega.tv' , 'vidplay.net' , 'vidspot.net' , 'vidto.me' , 'vidzi.tv' , 'vimeo.com' , 'vk.com' , 'vodlocker.com' , 'xfileload.com' , 'xvidstage.com' , 'zettahost.tv' ]
IiII = [ 'plugin.video.dramasonline' , 'plugin.video.f4mTester' , 'plugin.video.shahidmbcnet' , 'plugin.video.SportsDevil' , 'plugin.stream.vaughnlive.tv' , 'plugin.video.ZemTV-shani' ]
if 28 - 28: Ii11111i * iiI1i1
class i1I1ii1II1iII ( urllib2 . HTTPErrorProcessor ) :
 def http_response ( self , request , response ) :
  return response
 https_response = http_response
 if 86 - 86: oO0oIIII
Oo0oO0oo0oO00 = False ;
if Oo0oO0oo0oO00 :
 if 8 - 8: OOo00O0Oo0oO / ooO
 if 28 - 28: II11i % iIi1IIii11I + I11i * IIii1I
 try :
  import pysrc . pydevd as pydevd
  if 13 - 13: oO0oIIII * ooO
  pydevd . settrace ( 'localhost' , stdoutToServer = True , stderrToServer = True )
 except ImportError :
  sys . stderr . write ( "Error: " +
 "You must add org.python.pydev.debug.pysrc to your PYTHONPATH." )
  sys . exit ( 1 )
  if 90 - 90: IIii1I / oO0oIIII
  if 89 - 89: II1 - ooO * iIi1IIii11I
O0 = xbmcaddon . Addon ( 'plugin.video.evilsport' )
I11i1i11i1I = O0 . getAddonInfo ( 'version' )
Iiii = xbmc . translatePath ( O0 . getAddonInfo ( 'profile' ) . decode ( 'utf-8' ) )
OOO0O = xbmc . translatePath ( O0 . getAddonInfo ( 'path' ) . decode ( 'utf-8' ) )
oo0ooO0oOOOOo = os . path . join ( Iiii , 'favorites' )
oO000OoOoo00o = os . path . join ( Iiii , 'history' )
iiiI11 = os . path . join ( Iiii , 'list_revision' )
OOooO = os . path . join ( OOO0O , 'icon.png' )
OOoO00o = os . path . join ( OOO0O , 'fanart.jpg' )
II111iiii = os . path . join ( Iiii , 'source_file' )
II = Iiii
oOoOo00oOo = os . path . join ( Iiii , 'LivewebTV' )
downloader = downloader . SimpleDownloader ( )
Oo = O0 . getSetting ( 'debug' )
if 85 - 85: Ii11111i % I11i * iIi1IIii11I
if os . path . exists ( oo0ooO0oOOOOo ) == True :
 OO0O00OooO = open ( oo0ooO0oOOOOo ) . read ( )
else : OO0O00OooO = [ ]
if 77 - 77: ooOoO - ooOoO . iIiiiI1IiI1I1 / OOooOOo
i1iIIIiI1I = [ { "title" : "Evilsport " , "url" : OO0o , "fanart" : "http://" , "genre" : "Sport Live " , "date" : "25.02.2018" , "credits" : "MadDog" , "thumbnail" : "http://" } ]
if 70 - 70: IIiIiII11i % IIiIiII11i . ooO % o0oOOo0O0Ooo * OOooOOo % Ii1I
if 23 - 23: i11iIiiIii + iIiiiI1IiI1I1
if 68 - 68: oO0o . Ii1I . i11iIiiIii
def IIiI ( string ) :
 if Oo == 'true' :
  xbmc . log ( "[addon.madxtreams-%s]: %s" % ( I11i1i11i1I , string ) )
  if 22 - 22: IIiIiII11i % oO0oIIII
  if 84 - 84: i11iIiiIii . OOooOOo
def o0O00oooo ( url , headers = None ) :
 try :
  if headers is None :
   headers = { 'User-agent' : 'THEHOOD' }
  O00o = urllib2 . Request ( url , None , headers )
  O00 = urllib2 . urlopen ( O00o )
  i11I1 = O00 . read ( )
  O00 . close ( )
  return i11I1
 except urllib2 . URLError , Ii11Ii11I :
  IIiI ( 'URL: ' + url )
  if hasattr ( Ii11Ii11I , 'code' ) :
   IIiI ( 'We failed with error code - %s.' % Ii11Ii11I . code )
   xbmc . executebuiltin ( "XBMC.Notification(Evilsport,We failed with error code - " + str ( Ii11Ii11I . code ) + ",10000," + OOooO + ")" )
  elif hasattr ( Ii11Ii11I , 'reason' ) :
   IIiI ( 'We failed to reach a server.' )
   IIiI ( 'Reason: %s' % Ii11Ii11I . reason )
   xbmc . executebuiltin ( "XBMC.Notification(Evilsport,We failed to reach a server. - " + str ( Ii11Ii11I . reason ) + ",10000," + OOooO + ")" )
   if 43 - 43: iIiiiI1IiI1I1 - OOo00O0Oo0oO * IIii1I
   if 97 - 97: iiI1i1 % iiI1i1 + ooOoO * OOo00O0Oo0oO
def o0o00o0 ( ) :
 try :
  if os . path . exists ( oo0ooO0oOOOOo ) == True :
   OO0O00OooO = open ( oo0ooO0oOOOOo ) . read ( )
   if OO0O00OooO == "[]" :
    os . remove ( oo0ooO0oOOOOo )
   else :
    iIi1ii1I1 ( '[COLOR yellow][B]- MIS CANALES FAVORITOS[/COLOR][/B]' , 'url' , 4 , os . path . join ( OOO0O , 'resources' , 'favorite.png' ) , OOoO00o , '' , '' , '' , '' )
    iIi1ii1I1 ( '' , '' , 100 , '' , OOoO00o , '' , '' , '' , '' )
    if 71 - 71: II11i . OOO0O0O0ooooo
  o0OO0oo0oOO = i1iIIIiI1I
  if len ( o0OO0oo0oOO ) > 1 :
   for oo0oooooO0 in o0OO0oo0oOO :
    try :
     if 19 - 19: iiI1i1 + iIi1IIii11I
     if isinstance ( oo0oooooO0 , list ) :
      iIi1ii1I1 ( oo0oooooO0 [ 0 ] . encode ( 'utf-8' ) , oo0oooooO0 [ 1 ] . encode ( 'utf-8' ) , 1 , OOooO , OOoO00o , '' , '' , '' , '' , 'source' )
     else :
      ooo = OOooO
      ii1I1i1I = OOoO00o
      OOoo0O0 = ''
      iiiIi1i1I = ''
      credits = ''
      oOO00oOO = ''
      if oo0oooooO0 . has_key ( 'thumbnail' ) :
       ooo = oo0oooooO0 [ 'thumbnail' ]
      if oo0oooooO0 . has_key ( 'fanart' ) :
       ii1I1i1I = oo0oooooO0 [ 'fanart' ]
      if oo0oooooO0 . has_key ( 'description' ) :
       OOoo0O0 = oo0oooooO0 [ 'description' ]
      if oo0oooooO0 . has_key ( 'date' ) :
       iiiIi1i1I = oo0oooooO0 [ 'date' ]
      if oo0oooooO0 . has_key ( 'genre' ) :
       oOO00oOO = oo0oooooO0 [ 'genre' ]
      if oo0oooooO0 . has_key ( 'credits' ) :
       credits = oo0oooooO0 [ 'credits' ]
      iIi1ii1I1 ( oo0oooooO0 [ 'title' ] . encode ( 'utf-8' ) , oo0oooooO0 [ 'url' ] . encode ( 'utf-8' ) , 1 , ooo , ii1I1i1I , OOoo0O0 , oOO00oOO , iiiIi1i1I , credits , 'source' )
    except : traceback . print_exc ( )
  else :
   if len ( o0OO0oo0oOO ) == 1 :
    if isinstance ( o0OO0oo0oOO [ 0 ] , list ) :
     OoOo ( o0OO0oo0oOO [ 0 ] [ 1 ] . encode ( 'utf-8' ) , OOoO00o )
    else :
     OoOo ( o0OO0oo0oOO [ 0 ] [ 'url' ] , o0OO0oo0oOO [ 0 ] [ 'fanart' ] )
 except : traceback . print_exc ( )
 if 18 - 18: i11iIiiIii
 if 46 - 46: O00ooooo00 / iiI1i1 % Ii11111i + II11i
def O0OOO00oo ( url = None ) :
 if url is None :
  if not O0 . getSetting ( "new_file_source" ) == "" :
   Iii111II = O0 . getSetting ( 'new_file_source' ) . decode ( 'utf-8' )
  elif not O0 . getSetting ( "new_url_source" ) == "" :
   Iii111II = O0 . getSetting ( 'new_url_source' ) . decode ( 'utf-8' )
 else :
  Iii111II = url
 if Iii111II == '' or Iii111II is None :
  return
 IIiI ( 'Adding New Source: ' + Iii111II . encode ( 'utf-8' ) )
 if 9 - 9: o0oOOo0O0Ooo
 i11 = None
 if 58 - 58: Ii11111i * i11iIiiIii / oO0o % II11i - I11i / Ii1I
 i11I1 = ii11i1 ( Iii111II )
 if 29 - 29: I11i % iIiiiI1IiI1I1 + iIi1IIii11I / OOooOOo + Ii11111i * OOooOOo
 if isinstance ( i11I1 , BeautifulSOAP ) :
  if i11I1 . find ( 'channels_info' ) :
   i11 = i11I1 . channels_info
  elif i11I1 . find ( 'items_info' ) :
   i11 = i11I1 . items_info
 if i11 :
  i1I1iI = { }
  i1I1iI [ 'url' ] = Iii111II
  try : i1I1iI [ 'title' ] = i11 . title . string
  except : pass
  try : i1I1iI [ 'thumbnail' ] = i11 . thumbnail . string
  except : pass
  try : i1I1iI [ 'fanart' ] = i11 . fanart . string
  except : pass
  try : i1I1iI [ 'genre' ] = i11 . genre . string
  except : pass
  try : i1I1iI [ 'description' ] = i11 . description . string
  except : pass
  try : i1I1iI [ 'date' ] = i11 . date . string
  except : pass
  try : i1I1iI [ 'credits' ] = i11 . credits . string
  except : pass
 else :
  if '/' in Iii111II :
   oo0OooOOo0 = Iii111II . split ( '/' ) [ - 1 ] . split ( '.' ) [ 0 ]
  if '\\' in Iii111II :
   oo0OooOOo0 = Iii111II . split ( '\\' ) [ - 1 ] . split ( '.' ) [ 0 ]
  if '%' in oo0OooOOo0 :
   oo0OooOOo0 = urllib . unquote_plus ( oo0OooOOo0 )
  o0O = xbmc . Keyboard ( oo0OooOOo0 , 'Displayed Name, Rename?' )
  o0O . doModal ( )
  if ( o0O . isConfirmed ( ) == False ) :
   return
  O00oO = o0O . getText ( )
  if len ( O00oO ) == 0 :
   return
  i1I1iI = { }
  i1I1iI [ 'title' ] = O00oO
  i1I1iI [ 'url' ] = Iii111II
  i1I1iI [ 'fanart' ] = ii1I1i1I
  if 39 - 39: ooO - ooOoO * o0oOOo0O0Ooo % OOooOOo * ooOoO % ooOoO
 if os . path . exists ( II111iiii ) == False :
  OoOOOOO = [ ]
  OoOOOOO . append ( i1I1iI )
  iIi1i111II = open ( II111iiii , "w" )
  iIi1i111II . write ( json . dumps ( OoOOOOO ) )
  iIi1i111II . close ( )
 else :
  o0OO0oo0oOO = json . loads ( open ( II111iiii , "r" ) . read ( ) )
  o0OO0oo0oOO . append ( i1I1iI )
  iIi1i111II = open ( II111iiii , "w" )
  iIi1i111II . write ( json . dumps ( o0OO0oo0oOO ) )
  iIi1i111II . close ( )
 O0 . setSetting ( 'new_url_source' , "" )
 O0 . setSetting ( 'new_file_source' , "" )
 xbmc . executebuiltin ( "XBMC.Notification(Evilsport,New source added.,5000," + OOooO + ")" )
 if not url is None :
  if 'xbmcplus.xb.funpic.de' in url :
   xbmc . executebuiltin ( "XBMC.Container.Update(%s?mode=14,replace)" % sys . argv [ 0 ] )
  elif 'community-links' in url :
   xbmc . executebuiltin ( "XBMC.Container.Update(%s?mode=10,replace)" % sys . argv [ 0 ] )
 else : O0 . openSettings ( )
 if 83 - 83: i11iIiiIii + I11i - ooO * OOooOOo + iiI1i1 + o0oOOo0O0Ooo
 if 66 - 66: oO0o
def oO000Oo000 ( name ) :
 o0OO0oo0oOO = json . loads ( open ( II111iiii , "r" ) . read ( ) )
 for i111IiI1I in range ( len ( o0OO0oo0oOO ) ) :
  if isinstance ( o0OO0oo0oOO [ i111IiI1I ] , list ) :
   if o0OO0oo0oOO [ i111IiI1I ] [ 0 ] == name :
    del o0OO0oo0oOO [ i111IiI1I ]
    iIi1i111II = open ( II111iiii , "w" )
    iIi1i111II . write ( json . dumps ( o0OO0oo0oOO ) )
    iIi1i111II . close ( )
    break
  else :
   if o0OO0oo0oOO [ i111IiI1I ] [ 'title' ] == name :
    del o0OO0oo0oOO [ i111IiI1I ]
    iIi1i111II = open ( II111iiii , "w" )
    iIi1i111II . write ( json . dumps ( o0OO0oo0oOO ) )
    iIi1i111II . close ( )
    break
 xbmc . executebuiltin ( "XBMC.Container.Refresh" )
 if 70 - 70: oO0oIIII . IIiIiII11i / OOooOOo . oO0oIIII - OOO0O0O0ooooo / ooO
 if 62 - 62: IIii1I * oO0o
def i1 ( url , browse = False ) :
 if url is None :
  url = 'http://xbmcplus.xb.funpic.de/www-data/filesystem/'
 OOO = BeautifulSoup ( o0O00oooo ( url ) , convertEntities = BeautifulSoup . HTML_ENTITIES )
 for oo0oooooO0 in OOO ( 'a' ) :
  Oo0oOOo = oo0oooooO0 [ 'href' ]
  if not Oo0oOOo . startswith ( '?' ) :
   Oo0OoO00oOO0o = oo0oooooO0 . string
   if Oo0OoO00oOO0o not in [ 'Parent Directory' , 'recycle_bin/' ] :
    if Oo0oOOo . endswith ( '/' ) :
     if browse :
      iIi1ii1I1 ( Oo0OoO00oOO0o , url + Oo0oOOo , 15 , OOooO , ii1I1i1I , '' , '' , '' )
     else :
      iIi1ii1I1 ( Oo0OoO00oOO0o , url + Oo0oOOo , 14 , OOooO , ii1I1i1I , '' , '' , '' )
    elif Oo0oOOo . endswith ( '.xml' ) :
     if browse :
      iIi1ii1I1 ( Oo0OoO00oOO0o , url + Oo0oOOo , 1 , OOooO , ii1I1i1I , '' , '' , '' , '' , 'download' )
     else :
      if os . path . exists ( II111iiii ) == True :
       if Oo0OoO00oOO0o in i1iIIIiI1I :
        iIi1ii1I1 ( Oo0OoO00oOO0o + ' (in use)' , url + Oo0oOOo , 11 , OOooO , ii1I1i1I , '' , '' , '' , '' , 'download' )
       else :
        iIi1ii1I1 ( Oo0OoO00oOO0o , url + Oo0oOOo , 11 , OOooO , ii1I1i1I , '' , '' , '' , '' , 'download' )
      else :
       iIi1ii1I1 ( Oo0OoO00oOO0o , url + Oo0oOOo , 11 , OOooO , ii1I1i1I , '' , '' , '' , '' , 'download' )
       if 80 - 80: Ii1I + Ii11111i - Ii11111i % OOo00O0Oo0oO
       if 63 - 63: iIiiiI1IiI1I1 - I11i + OOO0O0O0ooooo % iiI1i1 / IIii1I / OOooOOo
def O0o0O00Oo0o0 ( browse = False ) :
 O00O0oOO00O00 = 'http://community-links.googlecode.com/svn/trunk/'
 OOO = BeautifulSoup ( o0O00oooo ( O00O0oOO00O00 ) , convertEntities = BeautifulSoup . HTML_ENTITIES )
 i1Oo00 = OOO ( 'ul' ) [ 0 ] ( 'li' ) [ 1 : ]
 for oo0oooooO0 in i1Oo00 :
  Oo0OoO00oOO0o = oo0oooooO0 ( 'a' ) [ 0 ] [ 'href' ]
  if browse :
   iIi1ii1I1 ( Oo0OoO00oOO0o , O00O0oOO00O00 + Oo0OoO00oOO0o , 1 , OOooO , ii1I1i1I , '' , '' , '' , '' , 'download' )
  else :
   iIi1ii1I1 ( Oo0OoO00oOO0o , O00O0oOO00O00 + Oo0OoO00oOO0o , 11 , OOooO , ii1I1i1I , '' , '' , '' , '' , 'download' )
   if 31 - 31: II11i . oO0o / OOO0O0O0ooooo
   if 89 - 89: oO0o
def ii11i1 ( url , data = None ) :
 global Oo0Ooo , I1ii11iIi11i
 I1ii11iIi11i = False
 if url . startswith ( 'http://' ) or url . startswith ( 'https://' ) :
  OO0oOoOO0oOO0 = False
  if '$$TSDOWNLOADER$$' in url :
   I1ii11iIi11i = True
   url = url . replace ( "$$TSDOWNLOADER$$" , "" )
  if '$$LSProEncKey=' in url :
   OO0oOoOO0oOO0 = url . split ( '$$LSProEncKey=' ) [ 1 ] . split ( '$$' ) [ 0 ]
   oO0OOoo0OO = '$$LSProEncKey=%s$$' % OO0oOoOO0oOO0
   url = url . replace ( oO0OOoo0OO , "" )
   if 65 - 65: oO0oIIII . IIii1I / OOO0O0O0ooooo - oO0oIIII
  data = o0O00oooo ( url )
  if OO0oOoOO0oOO0 :
   import pyaes
   OO0oOoOO0oOO0 = OO0oOoOO0oOO0 . encode ( "ascii" )
   print OO0oOoOO0oOO0
   iii1i1iiiiIi = 16 - len ( OO0oOoOO0oOO0 )
   OO0oOoOO0oOO0 = OO0oOoOO0oOO0 + ( chr ( 0 ) * ( iii1i1iiiiIi ) )
   print repr ( OO0oOoOO0oOO0 )
   data = base64 . b64decode ( data )
   IiiiOO0OoO0o00 = pyaes . new ( OO0oOoOO0oOO0 , pyaes . MODE_ECB , IV = None )
   data = IiiiOO0OoO0o00 . decrypt ( data ) . split ( '\0' ) [ 0 ]
   if 53 - 53: OOO0O0O0ooooo * o0oOOo0O0Ooo + Ii11111i
  if re . search ( "#EXTM3U" , data ) or 'm3u' in url :
   if 50 - 50: OOO0O0O0ooooo . OOO0O0O0ooooo - Ii1I / iIiiiI1IiI1I1 - OOooOOo * oO0o
   return data
 elif data == None :
  if not '/' in url or not '\\' in url :
   if 61 - 61: iiI1i1
   url = os . path . join ( oOoOo00oOo , url )
  if xbmcvfs . exists ( url ) :
   if url . startswith ( "smb://" ) or url . startswith ( "nfs://" ) :
    O0oOoOOOoOO = xbmcvfs . copy ( url , os . path . join ( Iiii , 'temp' , 'sorce_temp.txt' ) )
    if O0oOoOOOoOO :
     data = open ( os . path . join ( Iiii , 'temp' , 'sorce_temp.txt' ) , "r" ) . read ( )
     xbmcvfs . delete ( os . path . join ( Iiii , 'temp' , 'sorce_temp.txt' ) )
    else :
     IIiI ( "failed to copy from smb:" )
   else :
    data = open ( url , 'r' ) . read ( )
    if re . match ( "#EXTM3U" , data ) or 'm3u' in url :
     if 38 - 38: II11i
     return data
  else :
   IIiI ( "Soup Data not found!" )
   return
 if '<SetViewMode>' in data :
  try :
   Oo0Ooo = re . findall ( '<SetViewMode>(.*?)<' , data ) [ 0 ]
   xbmc . executebuiltin ( "Container.SetViewMode(%s)" % Oo0Ooo )
   print 'done setview' , Oo0Ooo
  except : pass
 return BeautifulSOAP ( data , convertEntities = BeautifulStoneSoup . XML_ENTITIES )
 if 7 - 7: OOO0O0O0ooooo . OOo00O0Oo0oO % I11i - iIiiiI1IiI1I1 - IIii1I
 if 36 - 36: ooO % iIi1IIii11I % IIiIiII11i - I11i
def OoOo ( url , fanart , data = None ) :
 OOO = ii11i1 ( url , data )
 if 22 - 22: IIii1I / IIiIiII11i * I11i % OOo00O0Oo0oO
 if isinstance ( OOO , BeautifulSOAP ) :
  if 85 - 85: Ii1I % i11iIiiIii - OOo00O0Oo0oO * II1 / iIiiiI1IiI1I1 % iIiiiI1IiI1I1
  if len ( OOO ( 'channels' ) ) > 0 and O0 . getSetting ( 'donotshowbychannels' ) == 'false' :
   IIiIi1iI = OOO ( 'channel' )
   for i1IiiiI1iI in IIiIi1iI :
    if 49 - 49: oO0oIIII / o0oOOo0O0Ooo . ooOoO
    if 68 - 68: i11iIiiIii % I11i + i11iIiiIii
    iii = ''
    II1I = 0
    try :
     iii = i1IiiiI1iI ( 'externallink' ) [ 0 ] . string
     II1I = len ( i1IiiiI1iI ( 'externallink' ) )
    except : pass
    if 84 - 84: ooO . i11iIiiIii . ooO * I11i - iiI1i1
    if II1I > 1 : iii = ''
    if 42 - 42: i11iIiiIii
    Oo0OoO00oOO0o = i1IiiiI1iI ( 'name' ) [ 0 ] . string
    I11i1iIII = i1IiiiI1iI ( 'thumbnail' ) [ 0 ] . string
    if I11i1iIII == None :
     I11i1iIII = ''
     if 32 - 32: II1 / IIii1I - OOooOOo
    try :
     if not i1IiiiI1iI ( 'fanart' ) :
      if O0 . getSetting ( 'use_thumb' ) == "true" :
       o00oooO0Oo = I11i1iIII
      else :
       o00oooO0Oo = fanart
     else :
      o00oooO0Oo = i1IiiiI1iI ( 'fanart' ) [ 0 ] . string
     if o00oooO0Oo == None :
      raise
    except :
     o00oooO0Oo = fanart
     if 78 - 78: oO0oIIII % II11i + I11i
    try :
     OOoo0O0 = i1IiiiI1iI ( 'info' ) [ 0 ] . string
     if OOoo0O0 == None :
      raise
    except :
     OOoo0O0 = ''
     if 64 - 64: Ii1I * OOO0O0O0ooooo . iIiiiI1IiI1I1 + ooOoO
    try :
     oOO00oOO = i1IiiiI1iI ( 'genre' ) [ 0 ] . string
     if oOO00oOO == None :
      raise
    except :
     oOO00oOO = ''
     if 6 - 6: oO0o / OOo00O0Oo0oO . ooO . ooO
    try :
     iiiIi1i1I = i1IiiiI1iI ( 'date' ) [ 0 ] . string
     if iiiIi1i1I == None :
      raise
    except :
     iiiIi1i1I = ''
     if 62 - 62: I11i + ooO % OOo00O0Oo0oO + Ii11111i
    try :
     credits = i1IiiiI1iI ( 'credits' ) [ 0 ] . string
     if credits == None :
      raise
    except :
     credits = ''
     if 33 - 33: OOO0O0O0ooooo . ooO . iIiiiI1IiI1I1
    try :
     if iii == '' :
      iIi1ii1I1 ( Oo0OoO00oOO0o . encode ( 'utf-8' , 'ignore' ) , url . encode ( 'utf-8' ) , 2 , I11i1iIII , o00oooO0Oo , OOoo0O0 , oOO00oOO , iiiIi1i1I , credits , True )
     else :
      if 72 - 72: O00ooooo00 / o0oOOo0O0Ooo + II1 - IIiIiII11i
      iIi1ii1I1 ( Oo0OoO00oOO0o . encode ( 'utf-8' ) , iii . encode ( 'utf-8' ) , 1 , I11i1iIII , o00oooO0Oo , OOoo0O0 , oOO00oOO , iiiIi1i1I , None , 'source' )
    except :
     IIiI ( 'There was a problem adding directory from getData(): ' + Oo0OoO00oOO0o . encode ( 'utf-8' , 'ignore' ) )
  else :
   IIiI ( 'No Channels: getItems' )
   iI1Iii ( OOO ( 'item' ) , fanart )
 else :
  oO00OOoO00 ( OOO )
  if 40 - 40: iIiiiI1IiI1I1 * oO0oIIII + Ii11111i % OOo00O0Oo0oO
  if 74 - 74: Ii1I - IIiIiII11i + II1 + II11i / oO0o
def oO00OOoO00 ( data ) :
 i1I1iI1iIi111i = data . rstrip ( )
 iiIi1IIi1I = re . compile ( r'#EXTINF:(.+?),(.*?)[\n\r]+([^\r\n]+)' ) . findall ( i1I1iI1iIi111i )
 o0OoOO000ooO0 = len ( iiIi1IIi1I )
 print 'tsdownloader' , I1ii11iIi11i
 if 56 - 56: OOo00O0Oo0oO
 for oo0oO0oOOoo , oOo00O0oo00o0 , ii in iiIi1IIi1I :
  if 84 - 84: OOooOOo % ooOoO . i11iIiiIii / o0oOOo0O0Ooo
  if 'tvg-logo' in oo0oO0oOOoo :
   I11i1iIII = o0OIiII ( oo0oO0oOOoo , 'tvg-logo=[\'"](.*?)[\'"]' )
   if I11i1iIII :
    if I11i1iIII . startswith ( 'http' ) :
     I11i1iIII = I11i1iIII
     if 25 - 25: OOO0O0O0ooooo - OOO0O0O0ooooo * OOooOOo
    elif not O0 . getSetting ( 'logo-folderPath' ) == "" :
     OOOO0oo0 = O0 . getSetting ( 'logo-folderPath' )
     I11i1iIII = OOOO0oo0 + I11i1iIII
     if 35 - 35: oO0oIIII - iIiiiI1IiI1I1 % OOooOOo . II1 % oO0oIIII
    else :
     I11i1iIII = I11i1iIII
     if 47 - 47: OOo00O0Oo0oO - oO0oIIII . ooOoO + II1 . i11iIiiIii
     if 94 - 94: OOooOOo * oO0oIIII / IIiIiII11i / oO0oIIII
  else :
   I11i1iIII = ''
   if 87 - 87: IIiIiII11i . ooO
  if 'type' in oo0oO0oOOoo :
   O0OO0O = o0OIiII ( oo0oO0oOOoo , 'type=[\'"](.*?)[\'"]' )
   if O0OO0O == 'yt-dl' :
    ii = ii + "&mode=18"
   elif O0OO0O == 'regex' :
    O00O0oOO00O00 = ii . split ( '&regexs=' )
    if 81 - 81: Ii1I . OOooOOo % OOO0O0O0ooooo / iIiiiI1IiI1I1 - Ii1I
    Ii1I1i = OO ( ii11i1 ( '' , data = O00O0oOO00O00 [ 1 ] ) )
    if 37 - 37: iIi1IIii11I % Ii1I . i11iIiiIii % oO0oIIII . IIiIiII11i
    I11I1IIII ( O00O0oOO00O00 [ 0 ] , oOo00O0oo00o0 , I11i1iIII , '' , '' , '' , '' , '' , None , Ii1I1i , o0OoOO000ooO0 )
    continue
   elif O0OO0O == 'ftv' :
    ii = 'plugin://plugin.video.F.T.V/?name=' + urllib . quote ( oOo00O0oo00o0 ) + '&url=' + ii + '&mode=125&ch_fanart=na'
  elif I1ii11iIi11i and '.ts' in ii :
   ii = 'plugin://plugin.video.f4mTester/?url=' + urllib . quote_plus ( ii ) + '&amp;streamtype=TSDOWNLOADER&name=' + urllib . quote ( oOo00O0oo00o0 )
  I11I1IIII ( ii , oOo00O0oo00o0 , I11i1iIII , '' , '' , '' , '' , '' , None , '' , o0OoOO000ooO0 )
  if 25 - 25: iiI1i1
  if 50 - 50: ooOoO - o0oOOo0O0Ooo / iIi1IIii11I
def Ii1I1Ii ( name , url , fanart ) :
 OOO = ii11i1 ( url )
 OOoO0 = OOO . find ( 'channel' , attrs = { 'name' : name . decode ( 'utf-8' ) } )
 OO0Oooo0oOO0O = OOoO0 ( 'item' )
 try :
  o00oooO0Oo = OOoO0 ( 'fanart' ) [ 0 ] . string
  if o00oooO0Oo == None :
   raise
 except :
  o00oooO0Oo = fanart
 for i1IiiiI1iI in OOoO0 ( 'subchannel' ) :
  name = i1IiiiI1iI ( 'name' ) [ 0 ] . string
  try :
   I11i1iIII = i1IiiiI1iI ( 'thumbnail' ) [ 0 ] . string
   if I11i1iIII == None :
    raise
  except :
   I11i1iIII = ''
  try :
   if not i1IiiiI1iI ( 'fanart' ) :
    if O0 . getSetting ( 'use_thumb' ) == "true" :
     o00oooO0Oo = I11i1iIII
   else :
    o00oooO0Oo = i1IiiiI1iI ( 'fanart' ) [ 0 ] . string
   if o00oooO0Oo == None :
    raise
  except :
   pass
  try :
   OOoo0O0 = i1IiiiI1iI ( 'info' ) [ 0 ] . string
   if OOoo0O0 == None :
    raise
  except :
   OOoo0O0 = ''
   if 62 - 62: iIiiiI1IiI1I1
  try :
   oOO00oOO = i1IiiiI1iI ( 'genre' ) [ 0 ] . string
   if oOO00oOO == None :
    raise
  except :
   oOO00oOO = ''
   if 100 - 100: oO0oIIII - OOO0O0O0ooooo % Ii1I * Ii11111i + iIiiiI1IiI1I1
  try :
   iiiIi1i1I = i1IiiiI1iI ( 'date' ) [ 0 ] . string
   if iiiIi1i1I == None :
    raise
  except :
   iiiIi1i1I = ''
   if 88 - 88: II1 - o0oOOo0O0Ooo * OOO0O0O0ooooo * II1 . II1
  try :
   credits = i1IiiiI1iI ( 'credits' ) [ 0 ] . string
   if credits == None :
    raise
  except :
   credits = ''
   if 33 - 33: II11i + OOo00O0Oo0oO * Ii1I / IIii1I - iIiiiI1IiI1I1
  try :
   iIi1ii1I1 ( name . encode ( 'utf-8' , 'ignore' ) , url . encode ( 'utf-8' ) , 3 , I11i1iIII , o00oooO0Oo , OOoo0O0 , oOO00oOO , credits , iiiIi1i1I )
  except :
   IIiI ( 'There was a problem adding directory - ' + name . encode ( 'utf-8' , 'ignore' ) )
 iI1Iii ( OO0Oooo0oOO0O , o00oooO0Oo )
 if 54 - 54: II11i / Ii11111i . Ii1I % OOo00O0Oo0oO
 if 57 - 57: i11iIiiIii . I11i - oO0oIIII - Ii1I + oO0o
def oO00oooOOoOo0 ( name , url , fanart ) :
 OOO = ii11i1 ( url )
 OOoO0 = OOO . find ( 'subchannel' , attrs = { 'name' : name . decode ( 'utf-8' ) } )
 OO0Oooo0oOO0O = OOoO0 ( 'subitem' )
 iI1Iii ( OO0Oooo0oOO0O , fanart )
 if 74 - 74: IIii1I * I11i + oO0o / O00ooooo00 / ooOoO . IIiIiII11i
 if 62 - 62: II1 * iIiiiI1IiI1I1
def iI1Iii ( items , fanart , dontLink = False ) :
 o0OoOO000ooO0 = len ( items )
 IIiI ( 'Total Items: %s' % o0OoOO000ooO0 )
 oOOOoo0O0oO = O0 . getSetting ( 'add_playlist' )
 iIII1I111III = O0 . getSetting ( 'ask_playlist_items' )
 IIo0o0O0O00oOOo = O0 . getSetting ( 'use_thumb' )
 iIIIiIi = O0 . getSetting ( 'parentalblocked' )
 iIIIiIi = iIIIiIi == "true"
 for OO0O0 in items :
  I11I11 = False
  o000O0O = False
  if 18 - 18: OOo00O0Oo0oO - Ii11111i . II11i . IIii1I
  i1I = 'false'
  try :
   i1I = OO0O0 ( 'parentalblock' ) [ 0 ] . string
  except :
   IIiI ( 'parentalblock Error' )
   i1I = ''
  if i1I == 'true' and iIIIiIi : continue
  if 78 - 78: iiI1i1 * IIii1I . iIiiiI1IiI1I1 / OOooOOo - II1 / II11i
  try :
   Oo0OoO00oOO0o = OO0O0 ( 'title' ) [ 0 ] . string
   if Oo0OoO00oOO0o is None :
    Oo0OoO00oOO0o = 'unknown?'
  except :
   IIiI ( 'Name Error' )
   Oo0OoO00oOO0o = ''
   if 35 - 35: iiI1i1 % Ii11111i - Ii1I
   if 20 - 20: O00ooooo00 - iIi1IIii11I
  try :
   if OO0O0 ( 'epg' ) :
    if OO0O0 . epg_url :
     IIiI ( 'Get EPG Regex' )
     i1iI = OO0O0 . epg_url . string
     Oo0O0 = OO0O0 . epg_regex . string
     Ooo0OOoOoO0 = oOo0OOoO0 ( i1iI , Oo0O0 )
     if Ooo0OOoOoO0 :
      Oo0OoO00oOO0o += ' - ' + Ooo0OOoOoO0
    elif OO0O0 ( 'epg' ) [ 0 ] . string > 1 :
     Oo0OoO00oOO0o += IIo0Oo0oO0oOO00 ( OO0O0 ( 'epg' ) [ 0 ] . string )
   else :
    pass
  except :
   IIiI ( 'EPG Error' )
  try :
   O00O0oOO00O00 = [ ]
   if len ( OO0O0 ( 'link' ) ) > 0 :
    if 92 - 92: II1 * II11i
    if 100 - 100: II11i + II11i * ooO
    for oo0oooooO0 in OO0O0 ( 'link' ) :
     if not oo0oooooO0 . string == None :
      O00O0oOO00O00 . append ( oo0oooooO0 . string )
      if 1 - 1: iIi1IIii11I . iIi1IIii11I / oO0o - II11i
   elif len ( OO0O0 ( 'sportsdevil' ) ) > 0 :
    for oo0oooooO0 in OO0O0 ( 'sportsdevil' ) :
     if not oo0oooooO0 . string == None :
      oooO = 'plugin://plugin.video.SportsDevil/?mode=1&amp;item=catcher%3dstreams%26url=' + oo0oooooO0 . string
      i1I1i111Ii = OO0O0 ( 'referer' ) [ 0 ] . string
      if i1I1i111Ii :
       if 67 - 67: iIiiiI1IiI1I1 . O00ooooo00
       oooO = oooO + '%26referer=' + i1I1i111Ii
      O00O0oOO00O00 . append ( oooO )
   elif len ( OO0O0 ( 'p2p' ) ) > 0 :
    for oo0oooooO0 in OO0O0 ( 'p2p' ) :
     if not oo0oooooO0 . string == None :
      if 'sop://' in oo0oooooO0 . string :
       i1i1iI1iiiI = 'plugin://plugin.video.p2p-streams/?mode=2url=' + oo0oooooO0 . string + '&' + 'name=' + Oo0OoO00oOO0o
       O00O0oOO00O00 . append ( i1i1iI1iiiI )
      else :
       Ooo0oOooo0 = 'plugin://plugin.video.p2p-streams/?mode=1&url=' + oo0oooooO0 . string + '&' + 'name=' + Oo0OoO00oOO0o
       O00O0oOO00O00 . append ( Ooo0oOooo0 )
   elif len ( OO0O0 ( 'vaughn' ) ) > 0 :
    for oo0oooooO0 in OO0O0 ( 'vaughn' ) :
     if not oo0oooooO0 . string == None :
      oOOOoo00 = 'plugin://plugin.stream.vaughnlive.tv/?mode=PlayLiveStream&amp;channel=' + oo0oooooO0 . string
      O00O0oOO00O00 . append ( oOOOoo00 )
   elif len ( OO0O0 ( 'ilive' ) ) > 0 :
    for oo0oooooO0 in OO0O0 ( 'ilive' ) :
     if not oo0oooooO0 . string == None :
      if not 'http' in oo0oooooO0 . string :
       iiIiIIIiiI = 'plugin://plugin.video.tbh.ilive/?url=http://www.streamlive.to/view/' + oo0oooooO0 . string + '&amp;link=99&amp;mode=iLivePlay'
      else :
       iiIiIIIiiI = 'plugin://plugin.video.tbh.ilive/?url=' + oo0oooooO0 . string + '&amp;link=99&amp;mode=iLivePlay'
   elif len ( OO0O0 ( 'yt-dl' ) ) > 0 :
    for oo0oooooO0 in OO0O0 ( 'yt-dl' ) :
     if not oo0oooooO0 . string == None :
      iiI1IIIi = oo0oooooO0 . string + '&mode=18'
      O00O0oOO00O00 . append ( iiI1IIIi )
   elif len ( OO0O0 ( 'dm' ) ) > 0 :
    for oo0oooooO0 in OO0O0 ( 'dm' ) :
     if not oo0oooooO0 . string == None :
      II11IiIi11 = "plugin://plugin.video.dailymotion_com/?mode=playVideo&url=" + oo0oooooO0 . string
      O00O0oOO00O00 . append ( II11IiIi11 )
   elif len ( OO0O0 ( 'dmlive' ) ) > 0 :
    for oo0oooooO0 in OO0O0 ( 'dmlive' ) :
     if not oo0oooooO0 . string == None :
      II11IiIi11 = "plugin://plugin.video.dailymotion_com/?mode=playLiveVideo&url=" + oo0oooooO0 . string
      O00O0oOO00O00 . append ( II11IiIi11 )
   elif len ( OO0O0 ( 'utube' ) ) > 0 :
    for oo0oooooO0 in OO0O0 ( 'utube' ) :
     if not oo0oooooO0 . string == None :
      if ' ' in oo0oooooO0 . string :
       IIOOO0O00O0OOOO = 'plugin://plugin.video.youtube/search/?q=' + urllib . quote_plus ( oo0oooooO0 . string )
       o000O0O = IIOOO0O00O0OOOO
      elif len ( oo0oooooO0 . string ) == 11 :
       IIOOO0O00O0OOOO = 'plugin://plugin.video.youtube/play/?video_id=' + oo0oooooO0 . string
      elif ( oo0oooooO0 . string . startswith ( 'PL' ) and not '&order=' in oo0oooooO0 . string ) or oo0oooooO0 . string . startswith ( 'UU' ) :
       IIOOO0O00O0OOOO = 'plugin://plugin.video.youtube/play/?&order=default&playlist_id=' + oo0oooooO0 . string
      elif oo0oooooO0 . string . startswith ( 'PL' ) or oo0oooooO0 . string . startswith ( 'UU' ) :
       IIOOO0O00O0OOOO = 'plugin://plugin.video.youtube/play/?playlist_id=' + oo0oooooO0 . string
      elif oo0oooooO0 . string . startswith ( 'UC' ) and len ( oo0oooooO0 . string ) > 12 :
       IIOOO0O00O0OOOO = 'plugin://plugin.video.youtube/channel/' + oo0oooooO0 . string + '/'
       o000O0O = IIOOO0O00O0OOOO
      elif not oo0oooooO0 . string . startswith ( 'UC' ) and not ( oo0oooooO0 . string . startswith ( 'PL' ) ) :
       IIOOO0O00O0OOOO = 'plugin://plugin.video.youtube/user/' + oo0oooooO0 . string + '/'
       o000O0O = IIOOO0O00O0OOOO
     O00O0oOO00O00 . append ( IIOOO0O00O0OOOO )
   elif len ( OO0O0 ( 'imdb' ) ) > 0 :
    for oo0oooooO0 in OO0O0 ( 'imdb' ) :
     if not oo0oooooO0 . string == None :
      if O0 . getSetting ( 'genesisorpulsar' ) == '0' :
       I1iiii1I = 'plugin://plugin.video.genesis/?action=play&imdb=' + oo0oooooO0 . string
      else :
       I1iiii1I = 'plugin://plugin.video.pulsar/movie/tt' + oo0oooooO0 . string + '/play'
      O00O0oOO00O00 . append ( I1iiii1I )
   elif len ( OO0O0 ( 'f4m' ) ) > 0 :
    for oo0oooooO0 in OO0O0 ( 'f4m' ) :
     if not oo0oooooO0 . string == None :
      if '.f4m' in oo0oooooO0 . string :
       OOo0 = 'plugin://plugin.video.f4mTester/?url=' + urllib . quote_plus ( oo0oooooO0 . string )
      elif '.m3u8' in oo0oooooO0 . string :
       OOo0 = 'plugin://plugin.video.f4mTester/?url=' + urllib . quote_plus ( oo0oooooO0 . string ) + '&amp;streamtype=HLS'
       if 73 - 73: OOo00O0Oo0oO
      else :
       OOo0 = 'plugin://plugin.video.f4mTester/?url=' + urllib . quote_plus ( oo0oooooO0 . string ) + '&amp;streamtype=SIMPLE'
     O00O0oOO00O00 . append ( OOo0 )
   elif len ( OO0O0 ( 'ftv' ) ) > 0 :
    for oo0oooooO0 in OO0O0 ( 'ftv' ) :
     if not oo0oooooO0 . string == None :
      IiiiiI1i1Iii = 'plugin://plugin.video.F.T.V/?name=' + urllib . quote ( Oo0OoO00oOO0o ) + '&url=' + oo0oooooO0 . string + '&mode=125&ch_fanart=na'
     O00O0oOO00O00 . append ( IiiiiI1i1Iii )
   elif len ( OO0O0 ( 'urlsolve' ) ) > 0 :
    if 87 - 87: OOooOOo
    for oo0oooooO0 in OO0O0 ( 'urlsolve' ) :
     if not oo0oooooO0 . string == None :
      IiI1iiiIii = oo0oooooO0 . string + '&mode=19'
      O00O0oOO00O00 . append ( IiI1iiiIii )
   if len ( O00O0oOO00O00 ) < 1 :
    raise
  except :
   IIiI ( 'Error <link> element, Passing:' + Oo0OoO00oOO0o . encode ( 'utf-8' , 'ignore' ) )
   continue
  try :
   I11I11 = OO0O0 ( 'externallink' ) [ 0 ] . string
  except : pass
  if 7 - 7: II11i * o0oOOo0O0Ooo - iIi1IIii11I + Ii11111i * iIiiiI1IiI1I1 % o0oOOo0O0Ooo
  if I11I11 :
   iI1i111I1Ii = [ I11I11 ]
   I11I11 = True
  else :
   I11I11 = False
  try :
   o000O0O = OO0O0 ( 'jsonrpc' ) [ 0 ] . string
  except : pass
  if o000O0O :
   if 25 - 25: II11i - OOo00O0Oo0oO
   iI1i111I1Ii = [ o000O0O ]
   if 10 - 10: ooOoO / Ii1I % II1 * iiI1i1 % I11i
   o000O0O = True
  else :
   o000O0O = False
  try :
   I11i1iIII = OO0O0 ( 'thumbnail' ) [ 0 ] . string
   if I11i1iIII == None :
    raise
  except :
   I11i1iIII = ''
  try :
   if not OO0O0 ( 'fanart' ) :
    if O0 . getSetting ( 'use_thumb' ) == "true" :
     o00oooO0Oo = I11i1iIII
    else :
     o00oooO0Oo = fanart
   else :
    o00oooO0Oo = OO0O0 ( 'fanart' ) [ 0 ] . string
   if o00oooO0Oo == None :
    raise
  except :
   o00oooO0Oo = fanart
  try :
   OOoo0O0 = OO0O0 ( 'info' ) [ 0 ] . string
   if OOoo0O0 == None :
    raise
  except :
   OOoo0O0 = ''
   if 48 - 48: iIi1IIii11I / II11i . IIii1I * oO0o * Ii1I / O00ooooo00
  try :
   oOO00oOO = OO0O0 ( 'genre' ) [ 0 ] . string
   if oOO00oOO == None :
    raise
  except :
   oOO00oOO = ''
   if 92 - 92: IIiIiII11i % IIiIiII11i - OOooOOo / oO0o
  try :
   iiiIi1i1I = OO0O0 ( 'date' ) [ 0 ] . string
   if iiiIi1i1I == None :
    raise
  except :
   iiiIi1i1I = ''
   if 10 - 10: OOo00O0Oo0oO + IIiIiII11i * I11i + IIii1I / II11i / I11i
  Ii1I1i = None
  if OO0O0 ( 'regex' ) :
   try :
    iI1II = OO0O0 ( 'regex' )
    Ii1I1i = OO ( iI1II )
   except :
    pass
  try :
   if 69 - 69: iIi1IIii11I % Ii1I
   if len ( O00O0oOO00O00 ) > 1 :
    ii1I1IIii11 = 0
    O0o0oO = [ ]
    for oo0oooooO0 in O00O0oOO00O00 :
     if oOOOoo0O0oO == "false" :
      ii1I1IIii11 += 1
      I11I1IIII ( oo0oooooO0 , '%s) %s' % ( ii1I1IIii11 , Oo0OoO00oOO0o . encode ( 'utf-8' , 'ignore' ) ) , I11i1iIII , o00oooO0Oo , OOoo0O0 , oOO00oOO , iiiIi1i1I , True , O0o0oO , Ii1I1i , o0OoOO000ooO0 )
     elif oOOOoo0O0oO == "true" and iIII1I111III == 'true' :
      if Ii1I1i :
       O0o0oO . append ( oo0oooooO0 + '&regexs=' + Ii1I1i )
      elif any ( x in oo0oooooO0 for x in IiiIII111iI ) and oo0oooooO0 . startswith ( 'http' ) :
       O0o0oO . append ( oo0oooooO0 + '&mode=19' )
      else :
       O0o0oO . append ( oo0oooooO0 )
     else :
      O0o0oO . append ( oo0oooooO0 )
    if len ( O0o0oO ) > 1 :
     I11I1IIII ( '' , Oo0OoO00oOO0o , I11i1iIII , o00oooO0Oo , OOoo0O0 , oOO00oOO , iiiIi1i1I , True , O0o0oO , Ii1I1i , o0OoOO000ooO0 )
   else :
    if 38 - 38: Ii1I % oO0o + I11i . i11iIiiIii
    if dontLink :
     return Oo0OoO00oOO0o , O00O0oOO00O00 [ 0 ] , Ii1I1i
    if I11I11 :
     if not Ii1I1i == None :
      iIi1ii1I1 ( Oo0OoO00oOO0o . encode ( 'utf-8' ) , iI1i111I1Ii [ 0 ] . encode ( 'utf-8' ) , 1 , I11i1iIII , fanart , OOoo0O0 , oOO00oOO , iiiIi1i1I , None , '!!update' , Ii1I1i , O00O0oOO00O00 [ 0 ] . encode ( 'utf-8' ) )
      if 53 - 53: i11iIiiIii * OOo00O0Oo0oO
     else :
      iIi1ii1I1 ( Oo0OoO00oOO0o . encode ( 'utf-8' ) , iI1i111I1Ii [ 0 ] . encode ( 'utf-8' ) , 1 , I11i1iIII , fanart , OOoo0O0 , oOO00oOO , iiiIi1i1I , None , 'source' , None , None )
      if 68 - 68: IIii1I * IIii1I . OOooOOo / ooOoO % IIiIiII11i
    elif o000O0O :
     iIi1ii1I1 ( Oo0OoO00oOO0o . encode ( 'utf-8' ) , iI1i111I1Ii [ 0 ] , 53 , I11i1iIII , fanart , OOoo0O0 , oOO00oOO , iiiIi1i1I , None , 'source' )
     if 38 - 38: iIi1IIii11I - Ii11111i / OOo00O0Oo0oO
    else :
     if 66 - 66: OOO0O0O0ooooo % I11i + i11iIiiIii . oO0o / oO0oIIII + I11i
     I11I1IIII ( O00O0oOO00O00 [ 0 ] , Oo0OoO00oOO0o . encode ( 'utf-8' , 'ignore' ) , I11i1iIII , o00oooO0Oo , OOoo0O0 , oOO00oOO , iiiIi1i1I , True , None , Ii1I1i , o0OoOO000ooO0 )
     if 86 - 86: OOooOOo
  except :
   IIiI ( 'There was a problem adding item - ' + Oo0OoO00oOO0o . encode ( 'utf-8' , 'ignore' ) )
   if 5 - 5: ooO * oO0o
   if 5 - 5: II11i
def OO ( reg_item ) :
 try :
  Ii1I1i = { }
  for oo0oooooO0 in reg_item :
   Ii1I1i [ oo0oooooO0 ( 'name' ) [ 0 ] . string ] = { }
   Ii1I1i [ oo0oooooO0 ( 'name' ) [ 0 ] . string ] [ 'name' ] = oo0oooooO0 ( 'name' ) [ 0 ] . string
   if 90 - 90: II11i . iIi1IIii11I / oO0oIIII - iiI1i1
   try :
    Ii1I1i [ oo0oooooO0 ( 'name' ) [ 0 ] . string ] [ 'expres' ] = oo0oooooO0 ( 'expres' ) [ 0 ] . string
    if not Ii1I1i [ oo0oooooO0 ( 'name' ) [ 0 ] . string ] [ 'expres' ] :
     Ii1I1i [ oo0oooooO0 ( 'name' ) [ 0 ] . string ] [ 'expres' ] = ''
   except :
    IIiI ( "Regex: -- No Referer --" )
   Ii1I1i [ oo0oooooO0 ( 'name' ) [ 0 ] . string ] [ 'page' ] = oo0oooooO0 ( 'page' ) [ 0 ] . string
   try :
    Ii1I1i [ oo0oooooO0 ( 'name' ) [ 0 ] . string ] [ 'referer' ] = oo0oooooO0 ( 'referer' ) [ 0 ] . string
   except :
    IIiI ( "Regex: -- No Referer --" )
   try :
    Ii1I1i [ oo0oooooO0 ( 'name' ) [ 0 ] . string ] [ 'connection' ] = oo0oooooO0 ( 'connection' ) [ 0 ] . string
   except :
    IIiI ( "Regex: -- No connection --" )
    if 40 - 40: II1
   try :
    Ii1I1i [ oo0oooooO0 ( 'name' ) [ 0 ] . string ] [ 'notplayable' ] = oo0oooooO0 ( 'notplayable' ) [ 0 ] . string
   except :
    IIiI ( "Regex: -- No notplayable --" )
    if 25 - 25: ooO + oO0oIIII / iIi1IIii11I . OOooOOo % OOO0O0O0ooooo * o0oOOo0O0Ooo
   try :
    Ii1I1i [ oo0oooooO0 ( 'name' ) [ 0 ] . string ] [ 'noredirect' ] = oo0oooooO0 ( 'noredirect' ) [ 0 ] . string
   except :
    IIiI ( "Regex: -- No noredirect --" )
   try :
    Ii1I1i [ oo0oooooO0 ( 'name' ) [ 0 ] . string ] [ 'origin' ] = oo0oooooO0 ( 'origin' ) [ 0 ] . string
   except :
    IIiI ( "Regex: -- No origin --" )
   try :
    Ii1I1i [ oo0oooooO0 ( 'name' ) [ 0 ] . string ] [ 'accept' ] = oo0oooooO0 ( 'accept' ) [ 0 ] . string
   except :
    IIiI ( "Regex: -- No accept --" )
   try :
    Ii1I1i [ oo0oooooO0 ( 'name' ) [ 0 ] . string ] [ 'includeheaders' ] = oo0oooooO0 ( 'includeheaders' ) [ 0 ] . string
   except :
    IIiI ( "Regex: -- No includeheaders --" )
    if 84 - 84: iIi1IIii11I % oO0oIIII + i11iIiiIii
    if 28 - 28: IIiIiII11i + o0oOOo0O0Ooo * Ii11111i % Ii1I . iiI1i1 % OOO0O0O0ooooo
   try :
    Ii1I1i [ oo0oooooO0 ( 'name' ) [ 0 ] . string ] [ 'listrepeat' ] = oo0oooooO0 ( 'listrepeat' ) [ 0 ] . string
    if 16 - 16: iiI1i1 - IIii1I / iIiiiI1IiI1I1 . ooOoO + IIii1I
   except :
    IIiI ( "Regex: -- No listrepeat --" )
    if 19 - 19: o0oOOo0O0Ooo - IIiIiII11i . OOO0O0O0ooooo
    if 60 - 60: ooOoO + IIiIiII11i
    if 9 - 9: iIi1IIii11I * II1 - IIii1I + oO0o / o0oOOo0O0Ooo . o0oOOo0O0Ooo
   try :
    Ii1I1i [ oo0oooooO0 ( 'name' ) [ 0 ] . string ] [ 'proxy' ] = oo0oooooO0 ( 'proxy' ) [ 0 ] . string
   except :
    IIiI ( "Regex: -- No proxy --" )
    if 49 - 49: ooOoO
   try :
    Ii1I1i [ oo0oooooO0 ( 'name' ) [ 0 ] . string ] [ 'x-req' ] = oo0oooooO0 ( 'x-req' ) [ 0 ] . string
   except :
    IIiI ( "Regex: -- No x-req --" )
    if 25 - 25: II1 - iIiiiI1IiI1I1 . iIiiiI1IiI1I1 * Ii1I
   try :
    Ii1I1i [ oo0oooooO0 ( 'name' ) [ 0 ] . string ] [ 'x-addr' ] = oo0oooooO0 ( 'x-addr' ) [ 0 ] . string
   except :
    IIiI ( "Regex: -- No x-addr --" )
    if 81 - 81: OOo00O0Oo0oO + ooO
   try :
    Ii1I1i [ oo0oooooO0 ( 'name' ) [ 0 ] . string ] [ 'x-forward' ] = oo0oooooO0 ( 'x-forward' ) [ 0 ] . string
   except :
    IIiI ( "Regex: -- No x-forward --" )
    if 98 - 98: iIiiiI1IiI1I1
   try :
    Ii1I1i [ oo0oooooO0 ( 'name' ) [ 0 ] . string ] [ 'agent' ] = oo0oooooO0 ( 'agent' ) [ 0 ] . string
   except :
    IIiI ( "Regex: -- No User Agent --" )
   try :
    Ii1I1i [ oo0oooooO0 ( 'name' ) [ 0 ] . string ] [ 'post' ] = oo0oooooO0 ( 'post' ) [ 0 ] . string
   except :
    IIiI ( "Regex: -- Not a post" )
   try :
    Ii1I1i [ oo0oooooO0 ( 'name' ) [ 0 ] . string ] [ 'rawpost' ] = oo0oooooO0 ( 'rawpost' ) [ 0 ] . string
   except :
    IIiI ( "Regex: -- Not a rawpost" )
   try :
    Ii1I1i [ oo0oooooO0 ( 'name' ) [ 0 ] . string ] [ 'htmlunescape' ] = oo0oooooO0 ( 'htmlunescape' ) [ 0 ] . string
   except :
    IIiI ( "Regex: -- Not a htmlunescape" )
    if 95 - 95: iIi1IIii11I / iIi1IIii11I
    if 30 - 30: I11i + IIiIiII11i / IIiIiII11i % I11i . I11i
   try :
    Ii1I1i [ oo0oooooO0 ( 'name' ) [ 0 ] . string ] [ 'readcookieonly' ] = oo0oooooO0 ( 'readcookieonly' ) [ 0 ] . string
   except :
    IIiI ( "Regex: -- Not a readCookieOnly" )
    if 55 - 55: iIi1IIii11I - iiI1i1 + ooOoO + OOo00O0Oo0oO % oO0oIIII
   try :
    Ii1I1i [ oo0oooooO0 ( 'name' ) [ 0 ] . string ] [ 'cookiejar' ] = oo0oooooO0 ( 'cookiejar' ) [ 0 ] . string
    if not Ii1I1i [ oo0oooooO0 ( 'name' ) [ 0 ] . string ] [ 'cookiejar' ] :
     Ii1I1i [ oo0oooooO0 ( 'name' ) [ 0 ] . string ] [ 'cookiejar' ] = ''
   except :
    IIiI ( "Regex: -- Not a cookieJar" )
   try :
    Ii1I1i [ oo0oooooO0 ( 'name' ) [ 0 ] . string ] [ 'setcookie' ] = oo0oooooO0 ( 'setcookie' ) [ 0 ] . string
   except :
    IIiI ( "Regex: -- Not a setcookie" )
   try :
    Ii1I1i [ oo0oooooO0 ( 'name' ) [ 0 ] . string ] [ 'appendcookie' ] = oo0oooooO0 ( 'appendcookie' ) [ 0 ] . string
   except :
    IIiI ( "Regex: -- Not a appendcookie" )
    if 41 - 41: O00ooooo00 - iiI1i1 - oO0oIIII
   try :
    Ii1I1i [ oo0oooooO0 ( 'name' ) [ 0 ] . string ] [ 'ignorecache' ] = oo0oooooO0 ( 'ignorecache' ) [ 0 ] . string
   except :
    IIiI ( "Regex: -- no ignorecache" )
    if 8 - 8: o0oOOo0O0Ooo + II11i - OOooOOo % IIiIiII11i % OOooOOo * Ii1I
    if 9 - 9: IIiIiII11i - i11iIiiIii - Ii11111i * oO0oIIII + iIi1IIii11I
    if 44 - 44: ooOoO
    if 52 - 52: I11i - IIiIiII11i + I11i % OOooOOo
    if 35 - 35: IIii1I
  Ii1I1i = urllib . quote ( repr ( Ii1I1i ) )
  return Ii1I1i
  if 42 - 42: II11i . iIiiiI1IiI1I1 . O00ooooo00 + oO0o + Ii11111i + iIiiiI1IiI1I1
 except :
  Ii1I1i = None
  IIiI ( 'regex Error: ' + Oo0OoO00oOO0o . encode ( 'utf-8' , 'ignore' ) )
  if 31 - 31: OOo00O0Oo0oO . Ii11111i - iIi1IIii11I . II1 / II1
  if 56 - 56: o0oOOo0O0Ooo / Ii1I / i11iIiiIii + II1 - IIiIiII11i - iiI1i1
def Iii1iiIi1II ( url ) :
 try :
  for oo0oooooO0 in range ( 1 , 51 ) :
   OO0O00oOo = ii1II ( url )
   if "EXT-X-STREAM-INF" in OO0O00oOo : return url
   if not "EXTM3U" in OO0O00oOo : return
   xbmc . sleep ( 2000 )
  return
 except :
  return
  if 14 - 14: Ii1I / Ii1I % iIi1IIii11I
  if 56 - 56: iIiiiI1IiI1I1 . OOO0O0O0ooooo + IIiIiII11i
def i1II1I1Iii1 ( regexs , url , cookieJar = None , forCookieJarOnly = False , recursiveCall = False , cachedPages = { } , rawPost = False , cookie_jar_file = None ) :
 if not recursiveCall :
  regexs = eval ( urllib . unquote ( regexs ) )
  if 30 - 30: II1 - oO0o
  if 75 - 75: IIii1I - oO0oIIII . IIiIiII11i % i11iIiiIii % iiI1i1
 O00II1I11i = re . compile ( '\$doregex\[([^\]]*)\]' ) . findall ( url )
 if 82 - 82: iiI1i1 + II1 - O00ooooo00 . O00ooooo00
 iIi1i = True
 for I1i11111i1i11 in O00II1I11i :
  if I1i11111i1i11 in regexs :
   if 77 - 77: I11i + o0oOOo0O0Ooo / Ii1I + OOO0O0O0ooooo * OOooOOo
   I1ii11 = regexs [ I1i11111i1i11 ]
   if 74 - 74: IIiIiII11i - OOooOOo . O00ooooo00
   i1III = False
   if 'cookiejar' in I1ii11 :
    if 49 - 49: i11iIiiIii % oO0oIIII . oO0o
    i1III = I1ii11 [ 'cookiejar' ]
    if '$doregex' in i1III :
     cookieJar = i1II1I1Iii1 ( regexs , I1ii11 [ 'cookiejar' ] , cookieJar , True , True , cachedPages )
     i1III = True
    else :
     i1III = True
     if 13 - 13: i11iIiiIii + O00ooooo00 * IIii1I % II1 - ooOoO * Ii11111i
   if i1III :
    if cookieJar == None :
     if 26 - 26: II1 * iIiiiI1IiI1I1 + Ii11111i
     cookie_jar_file = None
     if 'open[' in I1ii11 [ 'cookiejar' ] :
      cookie_jar_file = I1ii11 [ 'cookiejar' ] . split ( 'open[' ) [ 1 ] . split ( ']' ) [ 0 ]
      if 24 - 24: i11iIiiIii % IIii1I + Ii11111i / i11iIiiIii
      if 70 - 70: o0oOOo0O0Ooo * OOO0O0O0ooooo . iiI1i1 + iIiiiI1IiI1I1 . ooO
     cookieJar = Ii1iIiII1Ii ( cookie_jar_file )
     if 42 - 42: OOO0O0O0ooooo * oO0oIIII . IIiIiII11i - iIiiiI1IiI1I1 * IIii1I
     if cookie_jar_file :
      iII111Ii ( cookieJar , cookie_jar_file )
      if 52 - 52: ooOoO % ooO . oO0o * IIii1I
      if 50 - 50: iIi1IIii11I - II11i * ooO . I11i
      if 37 - 37: iIi1IIii11I % i11iIiiIii % ooOoO . OOO0O0O0ooooo . oO0oIIII
    elif 'save[' in I1ii11 [ 'cookiejar' ] :
     cookie_jar_file = I1ii11 [ 'cookiejar' ] . split ( 'save[' ) [ 1 ] . split ( ']' ) [ 0 ]
     OO0oOOoo = os . path . join ( Iiii , cookie_jar_file )
     if 52 - 52: OOooOOo % IIiIiII11i
     iII111Ii ( cookieJar , cookie_jar_file )
   if I1ii11 [ 'page' ] and '$doregex' in I1ii11 [ 'page' ] :
    Oo000ooOOO = i1II1I1Iii1 ( regexs , I1ii11 [ 'page' ] , cookieJar , recursiveCall = True , cachedPages = cachedPages )
    if len ( Oo000ooOOO ) == 0 :
     Oo000ooOOO = 'http://regexfailed'
    I1ii11 [ 'page' ] = Oo000ooOOO
    if 31 - 31: IIii1I % iiI1i1 % iIi1IIii11I . oO0oIIII - iiI1i1
   if 'setcookie' in I1ii11 and I1ii11 [ 'setcookie' ] and '$doregex' in I1ii11 [ 'setcookie' ] :
    I1ii11 [ 'setcookie' ] = i1II1I1Iii1 ( regexs , I1ii11 [ 'setcookie' ] , cookieJar , recursiveCall = True , cachedPages = cachedPages )
   if 'appendcookie' in I1ii11 and I1ii11 [ 'appendcookie' ] and '$doregex' in I1ii11 [ 'appendcookie' ] :
    I1ii11 [ 'appendcookie' ] = i1II1I1Iii1 ( regexs , I1ii11 [ 'appendcookie' ] , cookieJar , recursiveCall = True , cachedPages = cachedPages )
    if 17 - 17: oO0oIIII
    if 27 - 27: i11iIiiIii % ooOoO % iiI1i1 . OOO0O0O0ooooo - IIiIiII11i + oO0o
   if 'post' in I1ii11 and '$doregex' in I1ii11 [ 'post' ] :
    I1ii11 [ 'post' ] = i1II1I1Iii1 ( regexs , I1ii11 [ 'post' ] , cookieJar , recursiveCall = True , cachedPages = cachedPages )
    if 57 - 57: IIii1I / iiI1i1 - O00ooooo00
    if 51 - 51: ooO
   if 'rawpost' in I1ii11 and '$doregex' in I1ii11 [ 'rawpost' ] :
    I1ii11 [ 'rawpost' ] = i1II1I1Iii1 ( regexs , I1ii11 [ 'rawpost' ] , cookieJar , recursiveCall = True , cachedPages = cachedPages , rawPost = True )
    if 25 - 25: II1 + ooO * I11i
    if 92 - 92: iIiiiI1IiI1I1 + iiI1i1 + OOO0O0O0ooooo / OOooOOo + II11i
   if 'rawpost' in I1ii11 and '$epoctime$' in I1ii11 [ 'rawpost' ] :
    I1ii11 [ 'rawpost' ] = I1ii11 [ 'rawpost' ] . replace ( '$epoctime$' , I1iIi1iIiiIiI ( ) )
    if 47 - 47: oO0oIIII + II11i / O00ooooo00 % i11iIiiIii
   if 'rawpost' in I1ii11 and '$epoctime2$' in I1ii11 [ 'rawpost' ] :
    I1ii11 [ 'rawpost' ] = I1ii11 [ 'rawpost' ] . replace ( '$epoctime2$' , i111iI ( ) )
    if 85 - 85: OOooOOo . oO0o / iIi1IIii11I . OOO0O0O0ooooo % II11i
    if 90 - 90: IIiIiII11i % OOO0O0O0ooooo * IIii1I . OOo00O0Oo0oO
   I1iii11 = ''
   if I1ii11 [ 'page' ] and I1ii11 [ 'page' ] in cachedPages and not 'ignorecache' in I1ii11 and forCookieJarOnly == False :
    if 74 - 74: OOO0O0O0ooooo / O00ooooo00
    I1iii11 = cachedPages [ I1ii11 [ 'page' ] ]
   else :
    if I1ii11 [ 'page' ] and not I1ii11 [ 'page' ] == '' and I1ii11 [ 'page' ] . startswith ( 'http' ) :
     if '$epoctime$' in I1ii11 [ 'page' ] :
      I1ii11 [ 'page' ] = I1ii11 [ 'page' ] . replace ( '$epoctime$' , I1iIi1iIiiIiI ( ) )
     if '$epoctime2$' in I1ii11 [ 'page' ] :
      I1ii11 [ 'page' ] = I1ii11 [ 'page' ] . replace ( '$epoctime2$' , i111iI ( ) )
      if 78 - 78: II1 . o0oOOo0O0Ooo + iIi1IIii11I - O00ooooo00
      if 31 - 31: II1 . Ii11111i
     O0iII1 = I1ii11 [ 'page' ] . split ( '|' )
     IIII1i = O0iII1 [ 0 ]
     Ii1IIIIi1ii1I = None
     if len ( O0iII1 ) > 1 :
      Ii1IIIIi1ii1I = O0iII1 [ 1 ]
      if 13 - 13: iIiiiI1IiI1I1 % oO0o . I11i / IIiIiII11i % Ii11111i . II1
      if 22 - 22: ooO / i11iIiiIii
      if 62 - 62: o0oOOo0O0Ooo / I11i
      if 7 - 7: II1 . ooO
      if 53 - 53: oO0oIIII % oO0oIIII * OOooOOo + oO0o
      if 92 - 92: II1 + O00ooooo00 / oO0oIIII * OOO0O0O0ooooo
      if 100 - 100: iIi1IIii11I % IIii1I * ooOoO - OOo00O0Oo0oO
      if 92 - 92: iIi1IIii11I
      if 22 - 22: IIiIiII11i % OOo00O0Oo0oO * I11i / Ii11111i % i11iIiiIii * iiI1i1
      if 95 - 95: II1 - ooO * iIiiiI1IiI1I1 + oO0o
     iIi1 = urllib2 . ProxyHandler ( urllib2 . getproxies ( ) )
     if 21 - 21: iiI1i1
     if 92 - 92: i11iIiiIii / II11i - OOo00O0Oo0oO % iIi1IIii11I * II11i + IIiIiII11i
     if 11 - 11: II1 . II11i
     O00o = urllib2 . Request ( IIII1i )
     if 'proxy' in I1ii11 :
      Oo0000oOo = I1ii11 [ 'proxy' ]
      if 31 - 31: iiI1i1 . II11i * iIi1IIii11I + i11iIiiIii * Ii1I
      if 93 - 93: I11i / IIii1I * O00ooooo00 % II1 * OOO0O0O0ooooo * iiI1i1
      if IIII1i [ : 5 ] == "https" :
       Ooooooo = urllib2 . ProxyHandler ( { 'https' : Oo0000oOo } )
       if 39 - 39: ooO * IIiIiII11i + IIii1I - ooO + Ii11111i
      else :
       Ooooooo = urllib2 . ProxyHandler ( { 'http' : Oo0000oOo } )
       if 69 - 69: OOO0O0O0ooooo
      o0ooO = urllib2 . build_opener ( Ooooooo )
      urllib2 . install_opener ( o0ooO )
      if 74 - 74: OOO0O0O0ooooo * Ii1I - i11iIiiIii + II11i
      if 17 - 17: IIii1I . II1 / iiI1i1 % ooOoO % O00ooooo00 / i11iIiiIii
     O00o . add_header ( 'User-Agent' , 'Mozilla/5.0 (Windows NT 6.1; rv:14.0) Gecko/20100101 Firefox/14.0.1' )
     Oo0000oOo = None
     if 58 - 58: IIiIiII11i . ooOoO + Ii1I - i11iIiiIii / ooOoO / OOO0O0O0ooooo
     if 'referer' in I1ii11 :
      O00o . add_header ( 'Referer' , I1ii11 [ 'referer' ] )
     if 'accept' in I1ii11 :
      O00o . add_header ( 'Accept' , I1ii11 [ 'accept' ] )
     if 'agent' in I1ii11 :
      O00o . add_header ( 'User-agent' , I1ii11 [ 'agent' ] )
     if 'x-req' in I1ii11 :
      O00o . add_header ( 'X-Requested-With' , I1ii11 [ 'x-req' ] )
     if 'x-addr' in I1ii11 :
      O00o . add_header ( 'x-addr' , I1ii11 [ 'x-addr' ] )
     if 'x-forward' in I1ii11 :
      O00o . add_header ( 'X-Forwarded-For' , I1ii11 [ 'x-forward' ] )
     if 'setcookie' in I1ii11 :
      if 85 - 85: oO0o + Ii11111i
      O00o . add_header ( 'Cookie' , I1ii11 [ 'setcookie' ] )
     if 'appendcookie' in I1ii11 :
      if 10 - 10: ooO / o0oOOo0O0Ooo + oO0o / O00ooooo00
      i1iII1II11I = I1ii11 [ 'appendcookie' ]
      i1iII1II11I = i1iII1II11I . split ( ';' )
      for O0Oo00O in i1iII1II11I :
       OOo0o000oO , oO0o00oOOooO0 = O0Oo00O . split ( '=' )
       OOOoO000 , OOo0o000oO = OOo0o000oO . split ( ':' )
       oOOOO = cookielib . Cookie ( version = 0 , name = OOo0o000oO , value = oO0o00oOOooO0 , port = None , port_specified = False , domain = OOOoO000 , domain_specified = False , domain_initial_dot = False , path = '/' , path_specified = True , secure = False , expires = None , discard = True , comment = None , comment_url = None , rest = { 'HttpOnly' : None } , rfc2109 = False )
       cookieJar . set_cookie ( oOOOO )
     if 'origin' in I1ii11 :
      O00o . add_header ( 'Origin' , I1ii11 [ 'origin' ] )
     if Ii1IIIIi1ii1I :
      Ii1IIIIi1ii1I = Ii1IIIIi1ii1I . split ( '&' )
      for O0Oo00O in Ii1IIIIi1ii1I :
       OOo0o000oO , oO0o00oOOooO0 = O0Oo00O . split ( '=' )
       O00o . add_header ( OOo0o000oO , oO0o00oOOooO0 )
       if 49 - 49: ooOoO . Ii1I . i11iIiiIii % ooO
     if not cookieJar == None :
      if 34 - 34: II11i % ooO
      IiI1i = urllib2 . HTTPCookieProcessor ( cookieJar )
      o0ooO = urllib2 . build_opener ( IiI1i , urllib2 . HTTPBasicAuthHandler ( ) , urllib2 . HTTPHandler ( ) )
      o0ooO = urllib2 . install_opener ( o0ooO )
      if 87 - 87: iIi1IIii11I
      if 45 - 45: o0oOOo0O0Ooo / II1 - OOo00O0Oo0oO / oO0oIIII % ooO
      if 'noredirect' in I1ii11 :
       o0ooO = urllib2 . build_opener ( IiI1i , i1I1ii1II1iII , urllib2 . HTTPBasicAuthHandler ( ) , urllib2 . HTTPHandler ( ) )
       o0ooO = urllib2 . install_opener ( o0ooO )
     elif 'noredirect' in I1ii11 :
      o0ooO = urllib2 . build_opener ( i1I1ii1II1iII , urllib2 . HTTPBasicAuthHandler ( ) , urllib2 . HTTPHandler ( ) )
      o0ooO = urllib2 . install_opener ( o0ooO )
      if 83 - 83: iIiiiI1IiI1I1 . IIii1I - ooO * i11iIiiIii
      if 20 - 20: O00ooooo00 * II11i + ooOoO % OOooOOo % Ii1I
     if 'connection' in I1ii11 :
      if 13 - 13: IIiIiII11i
      from keepalive import HTTPHandler
      oOOo000oOoO0 = HTTPHandler ( )
      o0ooO = urllib2 . build_opener ( oOOo000oOoO0 )
      urllib2 . install_opener ( o0ooO )
      if 86 - 86: ooOoO % i11iIiiIii + oO0oIIII % i11iIiiIii
      if 92 - 92: i11iIiiIii - OOo00O0Oo0oO / iIi1IIii11I / Ii1I
      if 43 - 43: ooOoO + Ii11111i + OOo00O0Oo0oO
     iI1IIIii = None
     if 7 - 7: ooO - iiI1i1 / ooOoO * oO0oIIII . OOo00O0Oo0oO * OOo00O0Oo0oO
     if 'post' in I1ii11 :
      O0O0oOOo0O = I1ii11 [ 'post' ]
      if 19 - 19: OOooOOo / II11i % OOooOOo % OOo00O0Oo0oO * ooO
      if 19 - 19: IIii1I
      if 26 - 26: II1 % iIiiiI1IiI1I1 % IIiIiII11i . iIiiiI1IiI1I1 % oO0oIIII
      if 34 - 34: ooO / oO0o
      Oo0O0Ooo0ooOO = O0O0oOOo0O . split ( ',' ) ;
      iI1IIIii = { }
      for o00OO in Oo0O0Ooo0ooOO :
       OOo0o000oO = o00OO . split ( ':' ) [ 0 ] ;
       oO0o00oOOooO0 = o00OO . split ( ':' ) [ 1 ] ;
       iI1IIIii [ OOo0o000oO ] = oO0o00oOOooO0
      iI1IIIii = urllib . urlencode ( iI1IIIii )
      if 18 - 18: ooOoO . II1 % oO0o % oO0oIIII
     if 'rawpost' in I1ii11 :
      iI1IIIii = I1ii11 [ 'rawpost' ]
      if 9 - 9: o0oOOo0O0Ooo - IIiIiII11i * II1 . IIiIiII11i
      if 2 - 2: II1 % Ii11111i
      if 63 - 63: iIiiiI1IiI1I1 % IIii1I
      if 39 - 39: OOo00O0Oo0oO / ooOoO / I11i % iIiiiI1IiI1I1
     I1iii11 = ''
     try :
      if 89 - 89: II11i + II1 + II11i * O00ooooo00 + IIii1I % iiI1i1
      if iI1IIIii :
       O00 = urllib2 . urlopen ( O00o , iI1IIIii )
      else :
       O00 = urllib2 . urlopen ( O00o )
      if O00 . info ( ) . get ( 'Content-Encoding' ) == 'gzip' :
       from StringIO import StringIO
       import gzip
       oOo0oO = StringIO ( O00 . read ( ) )
       IIi1IIIIi = gzip . GzipFile ( fileobj = oOo0oO )
       I1iii11 = IIi1IIIIi . read ( )
      else :
       I1iii11 = O00 . read ( )
       if 70 - 70: Ii11111i / ooOoO - IIii1I - OOo00O0Oo0oO
       if 11 - 11: IIii1I . II1 . ooOoO / O00ooooo00 - iiI1i1
       if 30 - 30: oO0o
      if 'proxy' in I1ii11 and not iIi1 is None :
       urllib2 . install_opener ( urllib2 . build_opener ( iIi1 ) )
       if 21 - 21: i11iIiiIii / II11i % Ii11111i * OOO0O0O0ooooo . iiI1i1 - IIii1I
      I1iii11 = iiIiiii1i1i1i ( I1iii11 )
      if 86 - 86: IIiIiII11i / Ii1I + OOO0O0O0ooooo * OOo00O0Oo0oO
      if 19 - 19: ooOoO * ooO + oO0oIIII
      if 'includeheaders' in I1ii11 :
       if 65 - 65: Ii11111i . II11i . o0oOOo0O0Ooo . OOo00O0Oo0oO - Ii11111i
       I1iii11 += '$$HEADERS_START$$:'
       for iIi1i111II in O00 . headers :
        I1iii11 += iIi1i111II + ':' + O00 . headers . get ( iIi1i111II ) + '\n'
       I1iii11 += '$$HEADERS_END$$:'
       if 19 - 19: i11iIiiIii + OOo00O0Oo0oO % iIi1IIii11I
      IIiI ( I1iii11 )
      IIiI ( cookieJar )
      if 14 - 14: o0oOOo0O0Ooo . ooOoO . iiI1i1 / oO0oIIII % I11i - iIi1IIii11I
      O00 . close ( )
     except :
      pass
     cachedPages [ I1ii11 [ 'page' ] ] = I1iii11
     if 67 - 67: iiI1i1 - Ii11111i . O00ooooo00
     if 35 - 35: OOo00O0Oo0oO + iIi1IIii11I - Ii1I . OOo00O0Oo0oO . ooO
     if 87 - 87: oO0o
     if forCookieJarOnly :
      return cookieJar
    elif I1ii11 [ 'page' ] and not I1ii11 [ 'page' ] . startswith ( 'http' ) :
     if I1ii11 [ 'page' ] . startswith ( '$pyFunction:' ) :
      Ii = oO0O ( I1ii11 [ 'page' ] . split ( '$pyFunction:' ) [ 1 ] , '' , cookieJar , I1ii11 )
      if forCookieJarOnly :
       return cookieJar
      I1iii11 = Ii
      I1iii11 = iiIiiii1i1i1i ( I1iii11 )
     else :
      I1iii11 = I1ii11 [ 'page' ]
   if '$pyFunction:playmedia(' in I1ii11 [ 'expres' ] or 'ActivateWindow' in I1ii11 [ 'expres' ] or '$PLAYERPROXY$=' in url or any ( x in url for x in IiII ) :
    iIi1i = False
   if '$doregex' in I1ii11 [ 'expres' ] :
    I1ii11 [ 'expres' ] = i1II1I1Iii1 ( regexs , I1ii11 [ 'expres' ] , cookieJar , recursiveCall = True , cachedPages = cachedPages )
   if not I1ii11 [ 'expres' ] == '' :
    if 86 - 86: oO0o . IIii1I - o0oOOo0O0Ooo
    if '$LiveStreamCaptcha' in I1ii11 [ 'expres' ] :
     Ii = oOO ( I1ii11 , I1iii11 , cookieJar )
     if 31 - 31: Ii11111i / IIiIiII11i * O00ooooo00 . oO0o
     url = url . replace ( "$doregex[" + I1i11111i1i11 + "]" , Ii )
     if 57 - 57: Ii11111i + IIii1I % O00ooooo00 % iIiiiI1IiI1I1
    elif I1ii11 [ 'expres' ] . startswith ( '$pyFunction:' ) or '#$pyFunction' in I1ii11 [ 'expres' ] :
     if 83 - 83: OOooOOo / i11iIiiIii % IIii1I . iiI1i1 % Ii1I . II1
     Ii = ''
     if I1ii11 [ 'expres' ] . startswith ( '$pyFunction:' ) :
      Ii = oO0O ( I1ii11 [ 'expres' ] . split ( '$pyFunction:' ) [ 1 ] , I1iii11 , cookieJar , I1ii11 )
     else :
      Ii = o00oO00 ( I1ii11 [ 'expres' ] , I1iii11 , cookieJar , I1ii11 )
     if 'ActivateWindow' in I1ii11 [ 'expres' ] : return
     if 59 - 59: Ii11111i + IIii1I * OOooOOo + II11i . OOo00O0Oo0oO
     if 49 - 49: II1 * iiI1i1 - IIiIiII11i . Ii1I
     if 89 - 89: iIi1IIii11I + oO0oIIII * iIi1IIii11I / iIi1IIii11I
     try :
      url = url . replace ( u"$doregex[" + I1i11111i1i11 + "]" , Ii )
     except : url = url . replace ( "$doregex[" + I1i11111i1i11 + "]" , Ii . decode ( "utf-8" ) )
    else :
     if 'listrepeat' in I1ii11 :
      i11i11 = I1ii11 [ 'listrepeat' ]
      OoOoO00O0 = re . findall ( I1ii11 [ 'expres' ] , I1iii11 )
      return i11i11 , OoOoO00O0 , I1ii11 , regexs
      if 51 - 51: IIii1I / oO0o + Ii11111i - iiI1i1 + OOo00O0Oo0oO
     Ii = ''
     if not I1iii11 == '' :
      if 29 - 29: OOooOOo % IIii1I . II1 % II1 % ooOoO / OOo00O0Oo0oO
      oo0o0000Oo0 = re . compile ( I1ii11 [ 'expres' ] ) . search ( I1iii11 )
      try :
       Ii = oo0o0000Oo0 . group ( 1 ) . strip ( )
      except : traceback . print_exc ( )
      if I1ii11 [ 'page' ] == '' :
       Ii = I1ii11 [ 'expres' ]
       if 80 - 80: II11i - IIiIiII11i
     if rawPost :
      if 96 - 96: I11i / ooOoO . oO0oIIII - OOo00O0Oo0oO * iiI1i1 * Ii1I
      Ii = urllib . quote_plus ( Ii )
     if 'htmlunescape' in I1ii11 :
      if 76 - 76: oO0oIIII - ooOoO * Ii11111i / II1
      import HTMLParser
      Ii = HTMLParser . HTMLParser ( ) . unescape ( Ii )
     try :
      url = url . replace ( "$doregex[" + I1i11111i1i11 + "]" , Ii )
     except : url = url . replace ( "$doregex[" + I1i11111i1i11 + "]" , Ii . decode ( "utf-8" ) )
     if 18 - 18: o0oOOo0O0Ooo + IIii1I - ooOoO - iIiiiI1IiI1I1
     if 71 - 71: II1
   else :
    url = url . replace ( "$doregex[" + I1i11111i1i11 + "]" , '' )
 if '$epoctime$' in url :
  url = url . replace ( '$epoctime$' , I1iIi1iIiiIiI ( ) )
 if '$epoctime2$' in url :
  url = url . replace ( '$epoctime2$' , i111iI ( ) )
  if 33 - 33: II11i
 if '$GUID$' in url :
  import uuid
  url = url . replace ( '$GUID$' , str ( uuid . uuid1 ( ) ) . upper ( ) )
 if '$get_cookies$' in url :
  url = url . replace ( '$get_cookies$' , OOO0ooo ( cookieJar ) )
  if 7 - 7: OOooOOo + O00ooooo00 . iIiiiI1IiI1I1 / IIiIiII11i
 if recursiveCall : return url
 if 22 - 22: iIi1IIii11I - iIi1IIii11I % Ii11111i . II11i + Ii1I
 if url == "" :
  return
 else :
  return url , iIi1i
  if 63 - 63: iIiiiI1IiI1I1 % II11i * OOooOOo + II11i / IIiIiII11i % OOo00O0Oo0oO
  if 45 - 45: ooO
def Ii1Iii111IiI1 ( t ) :
 import hashlib
 O0Oo00O = hashlib . md5 ( )
 O0Oo00O . update ( t )
 return O0Oo00O . hexdigest ( )
 if 98 - 98: II11i - II1 % iIiiiI1IiI1I1 + OOO0O0O0ooooo . oO0oIIII
 if 56 - 56: ooOoO / Ii1I + i11iIiiIii + Ii11111i
def O0O0o0o0o ( encrypted ) :
 IIIIIiI = ""
 if 80 - 80: IIii1I * II11i % iiI1i1 % IIiIiII11i
 if 95 - 95: IIii1I - I11i . II11i - iIiiiI1IiI1I1
 if 75 - 75: o0oOOo0O0Ooo + OOooOOo - O00ooooo00 . II1 * oO0oIIII / ooO
 if 86 - 86: oO0o * ooOoO - OOO0O0O0ooooo . oO0o % IIii1I / Ii11111i
 if 11 - 11: iIiiiI1IiI1I1 * Ii1I + I11i / I11i
 if 37 - 37: i11iIiiIii + O00ooooo00
def I1i11II ( media_url ) :
 try :
  import CustomPlayer
  II11 = CustomPlayer . MyXBMCPlayer ( )
  I1iii = xbmcgui . ListItem ( label = str ( Oo0OoO00oOO0o ) , iconImage = "DefaultVideo.png" , thumbnailImage = xbmc . getInfoImage ( "ListItem.Thumb" ) , path = media_url )
  II11 . play ( media_url , I1iii )
  xbmc . sleep ( 1000 )
  while II11 . is_active :
   xbmc . sleep ( 200 )
 except :
  traceback . print_exc ( )
 return ''
 if 51 - 51: I11i
 if 41 - 41: I11i * iIi1IIii11I - oO0oIIII + IIiIiII11i
def IiIIIII11I ( params ) :
 i11I1 = json . dumps ( params )
 Ii1I11I = xbmc . executeJSONRPC ( i11I1 )
 if 36 - 36: OOO0O0O0ooooo + IIiIiII11i
 try :
  O00 = json . loads ( Ii1I11I )
 except UnicodeDecodeError :
  O00 = json . loads ( Ii1I11I . decode ( 'utf-8' , 'ignore' ) )
  if 5 - 5: IIiIiII11i * oO0o
 try :
  if 'result' in O00 :
   return O00 [ 'result' ]
  return None
 except KeyError :
  logger . warn ( "[%s] %s" % ( params [ 'method' ] , O00 [ 'error' ] [ 'message' ] ) )
  return None
  if 46 - 46: iIi1IIii11I
  if 33 - 33: OOo00O0Oo0oO - ooOoO * II1 - IIiIiII11i - Ii11111i
def O0OO0OIiiiIiiI ( proxysettings = None ) :
 if 72 - 72: O00ooooo00
 if proxysettings == None :
  if 82 - 82: oO0o + II1 / i11iIiiIii * I11i . II1
  xbmc . executeJSONRPC ( '{"jsonrpc":"2.0", "method":"Settings.SetSettingValue", "params":{"setting":"network.usehttpproxy", "value":false}, "id":1}' )
 else :
  if 63 - 63: I11i
  i1II = proxysettings . split ( ':' )
  IiiI11i1I = i1II [ 0 ]
  OOo0iiIii1IIi = i1II [ 1 ]
  ii1IiIiI1 = i1II [ 2 ]
  OOOoOo00O = None
  O0ooOo0o0Oo = None
  if 71 - 71: IIii1I - Ii11111i . iIiiiI1IiI1I1 % II1 + Ii11111i
  if len ( i1II ) > 3 and '@' in i1II [ 3 ] :
   OOOoOo00O = i1II [ 3 ] . split ( '@' ) [ 0 ]
   O0ooOo0o0Oo = i1II [ 3 ] . split ( '@' ) [ 1 ]
   if 26 - 26: IIiIiII11i + Ii11111i / o0oOOo0O0Ooo % oO0o % I11i + ooOoO
   if 31 - 31: iiI1i1 % Ii11111i * iiI1i1
  xbmc . executeJSONRPC ( '{"jsonrpc":"2.0", "method":"Settings.SetSettingValue", "params":{"setting":"network.usehttpproxy", "value":true}, "id":1}' )
  xbmc . executeJSONRPC ( '{"jsonrpc":"2.0", "method":"Settings.SetSettingValue", "params":{"setting":"network.httpproxytype", "value":' + str ( ii1IiIiI1 ) + '}, "id":1}' )
  xbmc . executeJSONRPC ( '{"jsonrpc":"2.0", "method":"Settings.SetSettingValue", "params":{"setting":"network.httpproxyserver", "value":"' + str ( IiiI11i1I ) + '"}, "id":1}' )
  xbmc . executeJSONRPC ( '{"jsonrpc":"2.0", "method":"Settings.SetSettingValue", "params":{"setting":"network.httpproxyport", "value":' + str ( OOo0iiIii1IIi ) + '}, "id":1}' )
  if 45 - 45: O00ooooo00 . iIiiiI1IiI1I1 + Ii11111i - II1 % iIi1IIii11I
  if 1 - 1: IIii1I
  if not OOOoOo00O == None :
   xbmc . executeJSONRPC ( '{"jsonrpc":"2.0", "method":"Settings.SetSettingValue", "params":{"setting":"network.httpproxyusername", "value":"' + str ( OOOoOo00O ) + '"}, "id":1}' )
   xbmc . executeJSONRPC ( '{"jsonrpc":"2.0", "method":"Settings.SetSettingValue", "params":{"setting":"network.httpproxypassword", "value":"' + str ( O0ooOo0o0Oo ) + '"}, "id":1}' )
   if 93 - 93: O00ooooo00 . i11iIiiIii . IIiIiII11i
   if 99 - 99: iiI1i1 - II11i - Ii1I % o0oOOo0O0Ooo
def IiiIIiiiiii ( ) :
 OOOO0o = IiIIIII11I ( { 'jsonrpc' : '2.0' , "method" : "Settings.GetSettingValue" , "params" : { "setting" : "network.usehttpproxy" } , 'id' : 1 } ) [ 'value' ]
 if 10 - 10: II11i % iIiiiI1IiI1I1
 ii1IiIiI1 = IiIIIII11I ( { 'jsonrpc' : '2.0' , "method" : "Settings.GetSettingValue" , "params" : { "setting" : "network.httpproxytype" } , 'id' : 1 } ) [ 'value' ]
 if 97 - 97: II1 - II11i
 if OOOO0o :
  IiiI11i1I = IiIIIII11I ( { 'jsonrpc' : '2.0' , "method" : "Settings.GetSettingValue" , "params" : { "setting" : "network.httpproxyserver" } , 'id' : 1 } ) [ 'value' ]
  OOo0iiIii1IIi = unicode ( IiIIIII11I ( { 'jsonrpc' : '2.0' , "method" : "Settings.GetSettingValue" , "params" : { "setting" : "network.httpproxyport" } , 'id' : 1 } ) [ 'value' ] )
  OOOoOo00O = IiIIIII11I ( { 'jsonrpc' : '2.0' , "method" : "Settings.GetSettingValue" , "params" : { "setting" : "network.httpproxyusername" } , 'id' : 1 } ) [ 'value' ]
  O0ooOo0o0Oo = IiIIIII11I ( { 'jsonrpc' : '2.0' , "method" : "Settings.GetSettingValue" , "params" : { "setting" : "network.httpproxypassword" } , 'id' : 1 } ) [ 'value' ]
  if 58 - 58: IIii1I + OOO0O0O0ooooo
  if OOOoOo00O and O0ooOo0o0Oo and IiiI11i1I and OOo0iiIii1IIi :
   return IiiI11i1I + ':' + str ( OOo0iiIii1IIi ) + ':' + str ( ii1IiIiI1 ) + ':' + OOOoOo00O + '@' + O0ooOo0o0Oo
  elif IiiI11i1I and OOo0iiIii1IIi :
   return IiiI11i1I + ':' + str ( OOo0iiIii1IIi ) + ':' + str ( ii1IiIiI1 )
 else :
  return None
  if 30 - 30: iIi1IIii11I % OOo00O0Oo0oO * Ii11111i - I11i * oO0oIIII % iIi1IIii11I
  if 46 - 46: i11iIiiIii - OOO0O0O0ooooo . Ii1I
def Oo0O ( media_url , name , iconImage , proxyip , port , proxyuser = None , proxypass = None ) :
 if 1 - 1: OOO0O0O0ooooo / OOo00O0Oo0oO % II11i . IIiIiII11i + ooO
 I1Ii11iiiI = xbmcgui . DialogProgress ( )
 I1Ii11iiiI . create ( 'Progress' , 'Playing with custom proxy' )
 I1Ii11iiiI . update ( 10 , "" , "setting proxy.." , "" )
 i1II1IiIII111 = False
 IiiIi1IIII1i = ''
 if 98 - 98: Ii11111i + O00ooooo00 . iIiiiI1IiI1I1 - ooOoO - OOooOOo
 try :
  if 24 - 24: IIiIiII11i - O00ooooo00 + iiI1i1
  IiiIi1IIII1i = IiiIIiiiiii ( )
  print 'existing_proxy' , IiiIi1IIII1i
  if 38 - 38: II1 / I11i . OOO0O0O0ooooo / O00ooooo00 / IIiIiII11i + IIii1I
  if 96 - 96: OOo00O0Oo0oO
  if not proxyuser == None :
   O0OO0OIiiiIiiI ( proxyip + ':' + port + ':0:' + proxyuser + '@' + proxypass )
  else :
   O0OO0OIiiiIiiI ( proxyip + ':' + port + ':0' )
   if 18 - 18: OOo00O0Oo0oO * iiI1i1 - oO0oIIII
   if 31 - 31: IIiIiII11i - OOO0O0O0ooooo % oO0o % Ii1I
  i1II1IiIII111 = True
  I1Ii11iiiI . update ( 80 , "" , "setting proxy complete, now playing" , "" )
  if 45 - 45: I11i + ooOoO * i11iIiiIii
  I1Ii11iiiI . close ( )
  I1Ii11iiiI = None
  import CustomPlayer
  II11 = CustomPlayer . MyXBMCPlayer ( )
  I1iii = xbmcgui . ListItem ( label = str ( name ) , iconImage = iconImage , thumbnailImage = xbmc . getInfoImage ( "ListItem.Thumb" ) , path = media_url )
  II11 . play ( media_url , I1iii )
  xbmc . sleep ( 1000 )
  while II11 . is_active :
   xbmc . sleep ( 200 )
 except :
  traceback . print_exc ( )
 if I1Ii11iiiI :
  I1Ii11iiiI . close ( )
 if i1II1IiIII111 :
  if 13 - 13: II1 * Ii1I - oO0oIIII / Ii11111i + iiI1i1 + ooO
  O0OO0OIiiiIiiI ( IiiIi1IIII1i )
  if 39 - 39: IIii1I - II1
 return ''
 if 81 - 81: I11i - OOO0O0O0ooooo * II1
 if 23 - 23: ooOoO / Ii1I
def iII1Iii1I11i ( page_value , referer = None ) :
 if referer :
  referer = [ ( 'Referer' , referer ) ]
 if page_value . startswith ( "http" ) :
  i1o0oooO = page_value
  page_value = ii1II ( page_value , headers = referer )
  if 89 - 89: ooOoO / Ii1I
 IIo0OoO00 = "(eval\(function\(p,a,c,k,e,(?:r|d).*)"
 if 18 - 18: Ii1I - OOooOOo - iIiiiI1IiI1I1 - iIiiiI1IiI1I1
 OOooo00 = re . compile ( IIo0OoO00 ) . findall ( page_value )
 i1oO = ""
 if OOooo00 and len ( OOooo00 ) > 0 :
  for oO0o00oOOooO0 in OOooo00 :
   iI = Ii1IIi ( oO0o00oOOooO0 )
   i111i11I1ii = o0OIiII ( iI , '\'(.*?)\'' )
   if 'unescape' in iI :
    iI = urllib . unquote ( i111i11I1ii )
   i1oO += iI + '\n'
   if 64 - 64: Ii1I / i11iIiiIii / OOooOOo . II1
   if 11 - 11: iiI1i1 % O00ooooo00
  i1o0oooO = o0OIiII ( i1oO , 'src="(.*?)"' )
  if 16 - 16: iIiiiI1IiI1I1 + iIi1IIii11I % oO0o
  page_value = ii1II ( i1o0oooO , headers = referer )
  if 80 - 80: iIi1IIii11I * OOO0O0O0ooooo
  if 78 - 78: oO0o
  if 20 - 20: OOo00O0Oo0oO % oO0oIIII . oO0oIIII / iiI1i1 + oO0o . oO0oIIII
 O0ooOo0 = o0OIiII ( page_value , 'streamer\'.*?\'(.*?)\'\)' )
 oo00ooOoo = o0OIiII ( page_value , 'file\',\s\'(.*?)\'' )
 if 28 - 28: oO0oIIII
 if 1 - 1: oO0oIIII
 return O0ooOo0 + ' playpath=' + oo00ooOoo + ' pageUrl=' + i1o0oooO
 if 48 - 48: OOO0O0O0ooooo + OOO0O0O0ooooo . II11i - iIi1IIii11I
 if 63 - 63: Ii1I
def Oo0 ( page_value , referer = None ) :
 if referer :
  referer = [ ( 'Referer' , referer ) ]
 if page_value . startswith ( "http" ) :
  page_value = ii1II ( page_value , headers = referer )
 IIo0OoO00 = "var a = (.*?);\s*var b = (.*?);\s*var c = (.*?);\s*var d = (.*?);\s*var f = (.*?);\s*var v_part = '(.*?)';"
 OOooo00 = re . compile ( IIo0OoO00 ) . findall ( page_value ) [ 0 ]
 if 79 - 79: o0oOOo0O0Ooo % Ii11111i / IIii1I + oO0o * o0oOOo0O0Ooo
 IiI1 , iIi1i111II , IIiiiiIiIIii , O0OO , IIi1IIIIi , oO0o00oOOooO0 = ( OOooo00 )
 IIi1IIIIi = int ( IIi1IIIIi )
 IiI1 = int ( IiI1 ) / IIi1IIIIi
 iIi1i111II = int ( iIi1i111II ) / IIi1IIIIi
 IIiiiiIiIIii = int ( IIiiiiIiIIii ) / IIi1IIIIi
 O0OO = int ( O0OO ) / IIi1IIIIi
 if 39 - 39: I11i + iIiiiI1IiI1I1 - IIii1I - OOooOOo
 OoOoO00O0 = 'rtmp://' + str ( IiI1 ) + '.' + str ( iIi1i111II ) + '.' + str ( IIiiiiIiIIii ) + '.' + str ( O0OO ) + oO0o00oOOooO0 ;
 return OoOoO00O0
 if 7 - 7: ooO . oO0o / I11i . Ii11111i * iiI1i1 - ooOoO
 if 37 - 37: II11i . oO0o / OOO0O0O0ooooo * OOo00O0Oo0oO
def III11iiii11i1 ( url , useragent = None ) :
 str = '#EXTM3U'
 str += '\n#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=361816'
 str += '\n' + url + '&bytes=0-200000'
 II111iiii = os . path . join ( Iiii , 'testfile.m3u' )
 str += '\n'
 ooOo0OoO ( II111iiii , str )
 if 36 - 36: ooO - II1 / o0oOOo0O0Ooo
 return II111iiii
 if 34 - 34: iIi1IIii11I
 if 45 - 45: iIi1IIii11I / IIiIiII11i / oO0oIIII
def ooOo0OoO ( file_name , page_data , append = False ) :
 if append :
  IIi1IIIIi = open ( file_name , 'a' )
  IIi1IIIIi . write ( page_data )
  IIi1IIIIi . close ( )
 else :
  IIi1IIIIi = open ( file_name , 'wb' )
  IIi1IIIIi . write ( page_data )
  IIi1IIIIi . close ( )
  return ''
  if 44 - 44: I11i - oO0oIIII / ooOoO * o0oOOo0O0Ooo * IIiIiII11i
  if 73 - 73: OOooOOo - iIiiiI1IiI1I1 * O00ooooo00 / i11iIiiIii * Ii11111i % ooOoO
def OooOoOOo0oO00 ( file_name ) :
 IIi1IIIIi = open ( file_name , 'rb' )
 O0OO = IIi1IIIIi . read ( )
 IIi1IIIIi . close ( )
 return O0OO
 if 73 - 73: OOo00O0Oo0oO / I11i % I11i * iiI1i1 / I11i
 if 8 - 8: oO0oIIII
def I11iII ( page_data ) :
 import re , base64 , urllib ;
 IiiIiI = page_data
 while 'geh(' in IiiIiI :
  if IiiIiI . startswith ( 'lol(' ) : IiiIiI = IiiIiI [ 5 : - 1 ]
  if 23 - 23: iiI1i1
  IiiIiI = re . compile ( '"(.*?)"' ) . findall ( IiiIiI ) [ 0 ] ;
  IiiIiI = base64 . b64decode ( IiiIiI ) ;
  IiiIiI = urllib . unquote ( IiiIiI ) ;
 print IiiIiI
 return IiiIiI
 if 40 - 40: OOooOOo - ooOoO / IIiIiII11i
 if 14 - 14: I11i
def iI1 ( page_data ) :
 if 14 - 14: I11i
 II1i = ii1II ( page_data ) ;
 I1i1I = '(http.*)'
 import uuid
 iii1I1Iii = str ( uuid . uuid1 ( ) ) . upper ( )
 o00oo0 = re . compile ( I1i1I ) . findall ( II1i )
 Oo0oOooOoOo = [ ( 'X-Playback-Session-Id' , iii1I1Iii ) ]
 for I1i in o00oo0 :
  try :
   OoIiIiIi1I1 = ii1II ( I1i , headers = Oo0oOooOoOo ) ;
   if 2 - 2: O00ooooo00 - iIi1IIii11I + iIiiiI1IiI1I1 . OOooOOo * OOooOOo / oO0o
  except : pass
  if 93 - 93: O00ooooo00
 return page_data + '|&X-Playback-Session-Id=' + iii1I1Iii
 if 53 - 53: II1 + IIiIiII11i + Ii1I
 if 24 - 24: OOo00O0Oo0oO - ooO - OOo00O0Oo0oO * I11i . II1 / ooO
def o0OOoo ( page_data ) :
 if 16 - 16: iIiiiI1IiI1I1 * O00ooooo00 - OOooOOo . ooO % iiI1i1 / OOooOOo
 if page_data . startswith ( 'http://dag.total-stream.net' ) :
  Oo0oOooOoOo = [ ( 'User-Agent' , 'Verismo-BlackUI_(2.4.7.5.8.0.34)' ) ]
  page_data = ii1II ( page_data , headers = Oo0oOooOoOo ) ;
  if 14 - 14: IIii1I * II11i * I11i / IIii1I * ooO / iiI1i1
 if '127.0.0.1' in page_data :
  return OOO000 ( page_data )
 elif o0OIiII ( page_data , 'wmsAuthSign%3D([^%&]+)' ) != '' :
  Ii1 = o0OIiII ( page_data , '&ver_t=([^&]+)&' ) + '?wmsAuthSign=' + o0OIiII ( page_data , 'wmsAuthSign%3D([^%&]+)' ) + '==/mp4:' + o0OIiII ( page_data , '\\?y=([^&]+)&' )
 else :
  Ii1 = o0OIiII ( page_data , 'href="([^"]+)"[^"]+$' )
  if len ( Ii1 ) == 0 :
   Ii1 = page_data
 Ii1 = Ii1 . replace ( ' ' , '%20' )
 return Ii1
 if 62 - 62: O00ooooo00 - O00ooooo00
 if 69 - 69: oO0o % Ii1I - iiI1i1
def o0OIiII ( data , re_patten ) :
 iiIi1IIi1I = ''
 I1ii11 = re . search ( re_patten , data )
 if I1ii11 != None :
  iiIi1IIi1I = I1ii11 . group ( 1 )
 else :
  iiIi1IIi1I = ''
 return iiIi1IIi1I
 if 38 - 38: IIii1I + i11iIiiIii / i11iIiiIii % o0oOOo0O0Ooo / iIi1IIii11I % oO0oIIII
 if 7 - 7: ooO * iIiiiI1IiI1I1 + O00ooooo00 + i11iIiiIii + IIiIiII11i % iIiiiI1IiI1I1
def OOO000 ( page_data ) :
 Ii1 = ''
 if '127.0.0.1' in page_data :
  Ii1 = o0OIiII ( page_data , '&ver_t=([^&]+)&' ) + ' live=true timeout=15 playpath=' + o0OIiII ( page_data , '\\?y=([a-zA-Z0-9-_\\.@]+)' )
  if 62 - 62: OOooOOo - oO0oIIII * oO0o - i11iIiiIii % iIi1IIii11I
 if o0OIiII ( page_data , 'token=([^&]+)&' ) != '' :
  Ii1 = Ii1 + '?token=' + o0OIiII ( page_data , 'token=([^&]+)&' )
 elif o0OIiII ( page_data , 'wmsAuthSign%3D([^%&]+)' ) != '' :
  Ii1 = o0OIiII ( page_data , '&ver_t=([^&]+)&' ) + '?wmsAuthSign=' + o0OIiII ( page_data , 'wmsAuthSign%3D([^%&]+)' ) + '==/mp4:' + o0OIiII ( page_data , '\\?y=([^&]+)&' )
 else :
  Ii1 = o0OIiII ( page_data , 'HREF="([^"]+)"' )
  if 52 - 52: I11i % Ii1I - i11iIiiIii
 if 'dag1.asx' in Ii1 :
  return o0OOoo ( Ii1 )
  if 30 - 30: OOo00O0Oo0oO / o0oOOo0O0Ooo + Ii1I
 if 'devinlivefs.fplive.net' not in Ii1 :
  Ii1 = Ii1 . replace ( 'devinlive' , 'flive' )
 if 'permlivefs.fplive.net' not in Ii1 :
  Ii1 = Ii1 . replace ( 'permlive' , 'flive' )
 return Ii1
 if 6 - 6: OOo00O0Oo0oO . iiI1i1 + oO0oIIII . II11i
 if 70 - 70: o0oOOo0O0Ooo
def i1iIi1111 ( str_eval ) :
 iIII1I1 = ""
 try :
  i1IIi1i1Ii1 = "w,i,s,e=(" + str_eval + ')'
  exec ( i1IIi1i1Ii1 )
  iIII1I1 = Iii ( w , oo0oooooO0 , IiiIiI , e )
 except : traceback . print_exc ( file = sys . stdout )
 if 63 - 63: ooO + OOooOOo
 return iIII1I1
 if 1 - 1: I11i / o0oOOo0O0Ooo + Ii1I . OOooOOo / I11i - OOo00O0Oo0oO
 if 5 - 5: Ii11111i
def Iii ( w , i , s , e ) :
 I1i1iIi1I1 = 0 ;
 OOO0 = 0 ;
 iIiIIi = 0 ;
 III1I = [ ] ;
 I1I111iIi = [ ] ;
 while True :
  if ( I1i1iIi1I1 < 5 ) :
   I1I111iIi . append ( w [ I1i1iIi1I1 ] )
  elif ( I1i1iIi1I1 < len ( w ) ) :
   III1I . append ( w [ I1i1iIi1I1 ] ) ;
  I1i1iIi1I1 += 1 ;
  if ( OOO0 < 5 ) :
   I1I111iIi . append ( i [ OOO0 ] )
  elif ( OOO0 < len ( i ) ) :
   III1I . append ( i [ OOO0 ] )
  OOO0 += 1 ;
  if ( iIiIIi < 5 ) :
   I1I111iIi . append ( s [ iIiIIi ] )
  elif ( iIiIIi < len ( s ) ) :
   III1I . append ( s [ iIiIIi ] ) ;
  iIiIIi += 1 ;
  if ( len ( w ) + len ( i ) + len ( s ) + len ( e ) == len ( III1I ) + len ( I1I111iIi ) + len ( e ) ) :
   break ;
   if 53 - 53: IIii1I + OOooOOo - oO0o - Ii1I / iIi1IIii11I % i11iIiiIii
 I11 = '' . join ( III1I )
 oOOooo = '' . join ( I1I111iIi )
 OOO0 = 0 ;
 ooo0O0Oo = [ ] ;
 for I1i1iIi1I1 in range ( 0 , len ( III1I ) , 2 ) :
  if 18 - 18: Ii11111i + II11i
  OO0OO0O = - 1 ;
  if ( ord ( oOOooo [ OOO0 ] ) % 2 ) :
   OO0OO0O = 1 ;
   if 75 - 75: iiI1i1 / OOooOOo / Ii11111i / ooO % iIi1IIii11I + ooOoO
  ooo0O0Oo . append ( chr ( int ( I11 [ I1i1iIi1I1 : I1i1iIi1I1 + 2 ] , 36 ) - OO0OO0O ) ) ;
  OOO0 += 1 ;
  if ( OOO0 >= len ( I1I111iIi ) ) :
   OOO0 = 0 ;
 OoOoO00O0 = '' . join ( ooo0O0Oo )
 if 'eval(function(w,i,s,e)' in OoOoO00O0 :
  if 4 - 4: OOo00O0Oo0oO - IIiIiII11i - ooO - iiI1i1 % i11iIiiIii / o0oOOo0O0Ooo
  OoOoO00O0 = re . compile ( 'eval\(function\(w,i,s,e\).*}\((.*?)\)' ) . findall ( OoOoO00O0 ) [ 0 ]
  return i1iIi1111 ( OoOoO00O0 )
 else :
  if 50 - 50: iIi1IIii11I + O00ooooo00
  return OoOoO00O0
  if 31 - 31: oO0oIIII
  if 78 - 78: i11iIiiIii + OOooOOo + II11i / OOooOOo % IIii1I % ooO
def Ii1IIi ( page_value , regex_for_text = '' , iterations = 1 , total_iteration = 1 ) :
 try :
  Oo0O0Oo00O = None
  if page_value . startswith ( "http" ) :
   page_value = ii1II ( page_value )
   if 9 - 9: OOooOOo . iIiiiI1IiI1I1 - I11i
  if regex_for_text and len ( regex_for_text ) > 0 :
   try :
    page_value = re . compile ( regex_for_text ) . findall ( page_value ) [ 0 ]
   except : return 'NOTPACKED'
   if 32 - 32: II1 / iIiiiI1IiI1I1 / IIii1I + ooOoO . Ii1I . OOooOOo
  page_value = ii1ii ( page_value , iterations , total_iteration )
 except :
  page_value = 'UNPACKEDFAILED'
  traceback . print_exc ( file = sys . stdout )
  if 8 - 8: o0oOOo0O0Ooo + oO0o . IIii1I % OOO0O0O0ooooo
 if 'sav1live.tv' in page_value :
  page_value = page_value . replace ( 'sav1live.tv' , 'sawlive.tv' )
  if 43 - 43: I11i - OOo00O0Oo0oO
 return page_value
 if 70 - 70: OOo00O0Oo0oO / Ii11111i % iIi1IIii11I - oO0oIIII
 if 47 - 47: OOo00O0Oo0oO
def ii1ii ( sJavascript , iteration = 1 , totaliterations = 2 ) :
 if 92 - 92: Ii11111i + oO0o % O00ooooo00
 if sJavascript . startswith ( 'var _0xcb8a=' ) :
  I1I1I11Ii = sJavascript . split ( 'var _0xcb8a=' )
  i1IIi1i1Ii1 = "myarray=" + I1I1I11Ii [ 1 ] . split ( "eval(" ) [ 0 ]
  exec ( i1IIi1i1Ii1 )
  ii1Iii1 = 62
  o0OOOOO0O = int ( I1I1I11Ii [ 1 ] . split ( ",62," ) [ 1 ] . split ( ',' ) [ 0 ] )
  I1I1IiIi1 = myarray [ 0 ]
  oOO0o0oo0 = myarray [ 3 ]
  with open ( 'temp file' + str ( iteration ) + '.js' , "wb" ) as oOo000O :
   oOo000O . write ( str ( oOO0o0oo0 ) )
   if 1 - 1: IIii1I
 else :
  if 54 - 54: II1 - iIiiiI1IiI1I1 % I11i
  if "rn p}('" in sJavascript :
   I1I1I11Ii = sJavascript . split ( "rn p}('" )
  else :
   I1I1I11Ii = sJavascript . split ( "rn A}('" )
   if 92 - 92: o0oOOo0O0Ooo * iIi1IIii11I
   if 35 - 35: i11iIiiIii
  I1I1IiIi1 , ii1Iii1 , o0OOOOO0O , oOO0o0oo0 = ( '' , '0' , '0' , '' )
  if 99 - 99: ooOoO . OOooOOo + OOO0O0O0ooooo
  i1IIi1i1Ii1 = "p1,a1,c1,k1=('" + I1I1I11Ii [ 1 ] . split ( ".spli" ) [ 0 ] + ')'
  exec ( i1IIi1i1Ii1 )
 oOO0o0oo0 = oOO0o0oo0 . split ( '|' )
 I1I1I11Ii = I1I1I11Ii [ 1 ] . split ( "))'" )
 if 71 - 71: ooO + O00ooooo00 * IIiIiII11i % IIiIiII11i / IIiIiII11i
 if 55 - 55: II1 + II11i + II1 * iIi1IIii11I
 if 68 - 68: OOO0O0O0ooooo
 if 2 - 2: o0oOOo0O0Ooo + OOO0O0O0ooooo * o0oOOo0O0Ooo - oO0oIIII + Ii1I
 if 43 - 43: I11i - oO0o
 if 36 - 36: I11i - OOo00O0Oo0oO
 if 24 - 24: OOooOOo + iIi1IIii11I + iiI1i1 - IIii1I
 if 49 - 49: iiI1i1 . iIi1IIii11I * oO0o % ooO . OOO0O0O0ooooo
 if 48 - 48: OOO0O0O0ooooo * oO0oIIII - OOO0O0O0ooooo / oO0oIIII + oO0o
 if 52 - 52: o0oOOo0O0Ooo % oO0oIIII * ooOoO
 if 4 - 4: iiI1i1 % OOO0O0O0ooooo - II1 + iIi1IIii11I . Ii1I % ooOoO
 if 9 - 9: ooOoO * ooOoO . i11iIiiIii * IIii1I
 if 18 - 18: o0oOOo0O0Ooo . ooOoO % oO0o % oO0oIIII
 if 87 - 87: IIii1I . II1 * oO0o
 if 100 - 100: o0oOOo0O0Ooo / O00ooooo00 - iIiiiI1IiI1I1 % oO0oIIII - IIii1I
 if 17 - 17: iiI1i1 / OOooOOo % IIiIiII11i
 if 71 - 71: ooO . II11i . o0oOOo0O0Ooo
 if 68 - 68: i11iIiiIii % Ii1I * o0oOOo0O0Ooo * ooO * ooOoO + OOO0O0O0ooooo
 if 66 - 66: iiI1i1 % I11i % II1
 if 34 - 34: OOooOOo / OOo00O0Oo0oO % OOO0O0O0ooooo . o0oOOo0O0Ooo . O00ooooo00
 if 29 - 29: OOO0O0O0ooooo . II11i
 if 66 - 66: Ii1I * IIii1I % IIii1I * ooO - iIi1IIii11I - ooO
 Ii11Ii11I = ''
 O0OO = ''
 if 70 - 70: II11i + Ii1I
 if 93 - 93: II11i + oO0oIIII
 i1i1 = str ( i1IiIi1 ( I1I1IiIi1 , ii1Iii1 , o0OOOOO0O , oOO0o0oo0 , Ii11Ii11I , O0OO , iteration ) )
 if 22 - 22: iiI1i1 * OOO0O0O0ooooo . ooOoO - o0oOOo0O0Ooo
 if 90 - 90: Ii1I
 if 94 - 94: iiI1i1 / I11i * II11i - oO0o
 if 44 - 44: oO0oIIII % i11iIiiIii - OOo00O0Oo0oO * I11i + IIiIiII11i * Ii11111i
 if 41 - 41: OOO0O0O0ooooo * iIi1IIii11I - oO0o . oO0oIIII
 if iteration >= totaliterations :
  if 65 - 65: IIiIiII11i . II1
  return i1i1
 else :
  if 70 - 70: IIiIiII11i - Ii1I . IIii1I % iiI1i1 / oO0o - OOO0O0O0ooooo
  return ii1ii ( i1i1 , iteration + 1 )
  if 55 - 55: OOo00O0Oo0oO - o0oOOo0O0Ooo
  if 100 - 100: OOO0O0O0ooooo
def i1IiIi1 ( p , a , c , k , e , d , iteration , v = 1 ) :
 if 79 - 79: IIii1I
 if 81 - 81: Ii11111i + IIii1I * II11i - IIii1I . Ii11111i
 if 48 - 48: iiI1i1 . II1 . iIiiiI1IiI1I1 . oO0o % I11i / OOo00O0Oo0oO
 while ( c >= 1 ) :
  c = c - 1
  if ( k [ c ] ) :
   ii1I111i1Ii = str ( OOOooO0OO0o ( c , a ) )
   if v == 1 :
    p = re . sub ( '\\b' + ii1I111i1Ii + '\\b' , k [ c ] , p )
   else :
    p = I1iIiiiI1 ( p , ii1I111i1Ii , k [ c ] )
    if 42 - 42: Ii11111i % Ii1I / o0oOOo0O0Ooo - Ii1I * i11iIiiIii
    if 19 - 19: Ii1I * iIiiiI1IiI1I1 % i11iIiiIii
    if 24 - 24: OOooOOo
    if 10 - 10: OOooOOo % oO0oIIII / Ii11111i
    if 28 - 28: Ii11111i % iIi1IIii11I
    if 48 - 48: i11iIiiIii % Ii1I
 return p
 if 29 - 29: OOo00O0Oo0oO + i11iIiiIii % iiI1i1
 if 93 - 93: oO0o % IIii1I
 if 90 - 90: iIiiiI1IiI1I1 - Ii11111i / oO0oIIII / OOO0O0O0ooooo / iiI1i1
 if 87 - 87: oO0o / ooO + IIii1I
 if 93 - 93: IIii1I + Ii1I % iIi1IIii11I
def I1iIiiiI1 ( source_str , word_to_find , replace_with ) :
 iii1IiI1I1 = None
 iii1IiI1I1 = source_str . split ( word_to_find )
 if len ( iii1IiI1I1 ) > 1 :
  O00ooO0o00ooO0OoO = [ ]
  IIoO00OoOo = 0
  for OoO in iii1IiI1I1 :
   if 10 - 10: iiI1i1 / iiI1i1 * i11iIiiIii
   O00ooO0o00ooO0OoO . append ( OoO )
   Ii = word_to_find
   if 46 - 46: o0oOOo0O0Ooo * IIiIiII11i % Ii1I + OOO0O0O0ooooo * ooO
   if 34 - 34: o0oOOo0O0Ooo
   if IIoO00OoOo == len ( iii1IiI1I1 ) - 1 :
    Ii = ''
   else :
    if len ( OoO ) == 0 :
     if ( len ( iii1IiI1I1 [ IIoO00OoOo + 1 ] ) == 0 and word_to_find [ 0 ] . lower ( ) not in 'abcdefghijklmnopqrstuvwxyz1234567890_' ) or ( len ( iii1IiI1I1 [ IIoO00OoOo + 1 ] ) > 0 and iii1IiI1I1 [ IIoO00OoOo + 1 ] [ 0 ] . lower ( ) not in 'abcdefghijklmnopqrstuvwxyz1234567890_' ) :
      Ii = replace_with
      if 27 - 27: oO0oIIII - OOO0O0O0ooooo % iiI1i1 * II11i . ooO % IIii1I
    else :
     if ( iii1IiI1I1 [ IIoO00OoOo ] [ - 1 ] . lower ( ) not in 'abcdefghijklmnopqrstuvwxyz1234567890_' ) and ( ( len ( iii1IiI1I1 [ IIoO00OoOo + 1 ] ) == 0 and word_to_find [ 0 ] . lower ( ) not in 'abcdefghijklmnopqrstuvwxyz1234567890_' ) or ( len ( iii1IiI1I1 [ IIoO00OoOo + 1 ] ) > 0 and iii1IiI1I1 [ IIoO00OoOo + 1 ] [ 0 ] . lower ( ) not in 'abcdefghijklmnopqrstuvwxyz1234567890_' ) ) :
      Ii = replace_with
      if 37 - 37: II1 + OOO0O0O0ooooo - O00ooooo00 % iIi1IIii11I
   O00ooO0o00ooO0OoO . append ( Ii )
   IIoO00OoOo += 1
   if 24 - 24: oO0o
  source_str = '' . join ( O00ooO0o00ooO0OoO )
 return source_str
 if 94 - 94: O00ooooo00 * O00ooooo00 % ooOoO + Ii11111i
 if 28 - 28: iIiiiI1IiI1I1
def I11o0000o0Oo ( num , radix ) :
 if 90 - 90: IIii1I * ooOoO
 OO0O00oOo = ""
 if num == 0 : return '0'
 while num > 0 :
  OO0O00oOo = "0123456789abcdefghijklmnopqrstuvwxyz" [ num % radix ] + OO0O00oOo
  num /= radix
 return OO0O00oOo
 if 70 - 70: OOooOOo * ooOoO - iIi1IIii11I
 if 55 - 55: iIiiiI1IiI1I1
def OOOooO0OO0o ( cc , a ) :
 ii1I111i1Ii = "" if cc < a else OOOooO0OO0o ( int ( cc / a ) , a )
 cc = ( cc % a )
 Ii1i1 = chr ( cc + 29 ) if cc > 35 else str ( I11o0000o0Oo ( cc , 36 ) )
 return ii1I111i1Ii + Ii1i1
 if 65 - 65: Ii1I + I11i / Ii11111i
 if 85 - 85: IIii1I / II1 % ooOoO
def OOO0ooo ( cookieJar ) :
 try :
  IiIIi11i111 = ""
  for i111IiI1I , oooo in enumerate ( cookieJar ) :
   IiIIi11i111 += oooo . name + "=" + oooo . value + ";"
 except : pass
 if 27 - 27: i11iIiiIii - iIiiiI1IiI1I1
 return IiIIi11i111
 if 35 - 35: II1 - II11i / o0oOOo0O0Ooo
 if 50 - 50: oO0o
def iII111Ii ( cookieJar , COOKIEFILE ) :
 try :
  OO0oOOoo = os . path . join ( Iiii , COOKIEFILE )
  cookieJar . save ( OO0oOOoo , ignore_discard = True )
 except : pass
 if 33 - 33: iiI1i1
 if 98 - 98: oO0o % ooOoO
def Ii1iIiII1Ii ( COOKIEFILE ) :
 if 95 - 95: IIii1I - II11i - Ii11111i + II11i % I11i . iIiiiI1IiI1I1
 IiiIIi1 = None
 if COOKIEFILE :
  try :
   OO0oOOoo = os . path . join ( Iiii , COOKIEFILE )
   IiiIIi1 = cookielib . LWPCookieJar ( )
   IiiIIi1 . load ( OO0oOOoo , ignore_discard = True )
  except :
   IiiIIi1 = None
   if 28 - 28: OOooOOo
 if not IiiIIi1 :
  IiiIIi1 = cookielib . LWPCookieJar ( )
  if 45 - 45: OOooOOo . iIiiiI1IiI1I1 / II11i - IIiIiII11i * IIii1I
 return IiiIIi1
 if 86 - 86: ooOoO + iIi1IIii11I + ooO
 if 9 - 9: iIi1IIii11I + ooOoO % iIi1IIii11I % ooO + IIii1I
def oO0O ( fun_call , page_data , Cookie_Jar , m ) :
 oO00 = ''
 if 7 - 7: OOO0O0O0ooooo % II11i + I11i + oO0oIIII % II1 . IIiIiII11i
 if II not in sys . path :
  sys . path . append ( II )
  if 56 - 56: OOo00O0Oo0oO
  if 84 - 84: oO0o - i11iIiiIii
 try :
  i1II1II1iii1i = 'import ' + fun_call . split ( '.' ) [ 0 ]
  if 75 - 75: ooO - oO0o - IIii1I % OOooOOo
  exec ( i1II1II1iii1i )
  if 58 - 58: OOO0O0O0ooooo . ooO / II1 . o0oOOo0O0Ooo / IIiIiII11i * ooOoO
 except :
  if 53 - 53: oO0oIIII - OOO0O0O0ooooo / OOooOOo % OOo00O0Oo0oO * iIiiiI1IiI1I1 % Ii11111i
  traceback . print_exc ( file = sys . stdout )
  if 69 - 69: I11i
 exec ( 'ret_val=' + fun_call )
 if 83 - 83: OOooOOo
 if 38 - 38: II11i + II1 . O00ooooo00
 try :
  return str ( oO00 )
 except : return oO00
 if 19 - 19: OOo00O0Oo0oO - OOooOOo - oO0oIIII - oO0o . OOo00O0Oo0oO . II11i
 if 48 - 48: OOo00O0Oo0oO + ooO
def o00oO00 ( fun_call , page_data , Cookie_Jar , m ) :
 if 60 - 60: iiI1i1 + OOo00O0Oo0oO . ooO / O00ooooo00 . IIii1I
 oO00 = ''
 if II not in sys . path :
  sys . path . append ( II )
 IIi1IIIIi = open ( II + "/LSProdynamicCode.py" , "w" )
 IIi1IIIIi . write ( fun_call ) ;
 IIi1IIIIi . close ( )
 import LSProdynamicCode
 oO00 = LSProdynamicCode . GetLSProData ( page_data , Cookie_Jar , m )
 try :
  return str ( oO00 )
 except : return oO00
 if 14 - 14: Ii11111i
 if 79 - 79: oO0oIIII
def o0Oii111 ( captchakey , cj , type = 1 ) :
 if 93 - 93: II1 * IIiIiII11i
 if 10 - 10: II11i * II1 + iiI1i1 - I11i / I11i . i11iIiiIii
 if 22 - 22: II11i / OOooOOo
 oO0OooOOooo0ooo00 = ""
 oooOo = ""
 if 98 - 98: ooOoO - II1 * OOO0O0O0ooooo
 if 85 - 85: II1 % oO0o * IIii1I
 if 44 - 44: IIii1I . I11i + II11i . iIi1IIii11I
 if 7 - 7: I11i + IIii1I * iiI1i1 * iiI1i1 / ooOoO - oO0oIIII
 if 65 - 65: Ii1I + oO0o + ooOoO
 oOOoo = False
 i1I1iIii11 = None
 oooOo = None
 if len ( captchakey ) > 0 :
  oOoO0O0oO = captchakey
  if not oOoO0O0oO . startswith ( 'http' ) :
   oOoO0O0oO = 'http://www.google.com/recaptcha/api/challenge?k=' + oOoO0O0oO + '&ajax=1'
   if 92 - 92: IIiIiII11i / i11iIiiIii + I11i
  oOOoo = True
  if 87 - 87: oO0o % IIii1I
  o0OO0OOO0O = 'challenge.*?\'(.*?)\''
  Iii1I = '\'(.*?)\''
  oOoOOOOoOO0o = ii1II ( oOoO0O0oO , cookieJar = cj )
  oO0OooOOooo0ooo00 = re . findall ( o0OO0OOO0O , oOoOOOOoOO0o ) [ 0 ]
  iiI1i1I1II = 'http://www.google.com/recaptcha/api/reload?c=' ;
  O0O = oOoO0O0oO . split ( 'k=' ) [ 1 ]
  iiI1i1I1II += oO0OooOOooo0ooo00 + '&k=' + O0O + '&reason=i&type=image&lang=en'
  OOOOO0 = ii1II ( iiI1i1I1II , cookieJar = cj )
  i1I1iIii11 = re . findall ( Iii1I , OOOOO0 ) [ 0 ]
  Ooo0Oo0o = 'http://www.google.com/recaptcha/api/image?c=' + i1I1iIii11
  if not Ooo0Oo0o . startswith ( "http" ) :
   Ooo0Oo0o = 'http://www.google.com/recaptcha/api/' + Ooo0Oo0o
  import random
  OOo0o000oO = random . randrange ( 100 , 1000 , 5 )
  oo0Oo0 = os . path . join ( Iiii , str ( OOo0o000oO ) + "captcha.img" )
  oOOoOOO0oo0 = open ( oo0Oo0 , "wb" )
  oOOoOOO0oo0 . write ( ii1II ( Ooo0Oo0o , cookieJar = cj ) )
  oOOoOOO0oo0 . close ( )
  O00O = O0OOOOOoo ( captcha = oo0Oo0 )
  oooOo = O00O . get ( )
  os . remove ( oo0Oo0 )
  if 69 - 69: iIiiiI1IiI1I1 + OOo00O0Oo0oO
 if i1I1iIii11 :
  if type == 1 :
   return 'recaptcha_challenge_field=' + urllib . quote_plus ( i1I1iIii11 ) + '&recaptcha_response_field=' + urllib . quote_plus ( oooOo )
  elif type == 2 :
   return 'recaptcha_challenge_field:' + i1I1iIii11 + ',recaptcha_response_field:' + oooOo
  else :
   return 'recaptcha_challenge_field=' + urllib . quote_plus ( i1I1iIii11 ) + '&recaptcha_response_field=' + urllib . quote_plus ( oooOo )
 else :
  return ''
  if 7 - 7: OOo00O0Oo0oO + Ii1I
  if 26 - 26: IIii1I + O00ooooo00 / oO0o % I11i
def ii1II ( url , cookieJar = None , post = None , timeout = 20 , headers = None , noredir = False ) :
 if 44 - 44: II1 . ooOoO . Ii11111i % II1
 if 86 - 86: i11iIiiIii + OOO0O0O0ooooo * ooO - o0oOOo0O0Ooo * Ii11111i + OOO0O0O0ooooo
 IiI1i = urllib2 . HTTPCookieProcessor ( cookieJar )
 if 95 - 95: IIii1I . II11i % OOo00O0Oo0oO - II11i * ooOoO
 if noredir :
  o0ooO = urllib2 . build_opener ( i1I1ii1II1iII , IiI1i , urllib2 . HTTPBasicAuthHandler ( ) , urllib2 . HTTPHandler ( ) )
 else :
  o0ooO = urllib2 . build_opener ( IiI1i , urllib2 . HTTPBasicAuthHandler ( ) , urllib2 . HTTPHandler ( ) )
  if 89 - 89: OOo00O0Oo0oO . iIiiiI1IiI1I1
 O00o = urllib2 . Request ( url )
 O00o . add_header ( 'User-Agent' , 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.154 Safari/537.36' )
 if headers :
  for O0Oo00O , ooOoo0OoOO in headers :
   O00o . add_header ( O0Oo00O , ooOoo0OoOO )
   if 38 - 38: o0oOOo0O0Ooo / iIi1IIii11I % II11i * iiI1i1 + i11iIiiIii % iIi1IIii11I
 O00 = o0ooO . open ( O00o , post , timeout = timeout )
 I1iii11 = O00 . read ( )
 O00 . close ( )
 return I1iii11 ;
 if 61 - 61: II11i - oO0oIIII % I11i / iIi1IIii11I / OOo00O0Oo0oO + IIii1I
 if 87 - 87: II11i + iIi1IIii11I + OOO0O0O0ooooo / O00ooooo00 % ooO / II11i
def OOo000OO000 ( str , reg = None ) :
 if reg :
  str = re . findall ( reg , str ) [ 0 ]
 OOOO00OooO = urllib . unquote ( str [ 0 : len ( str ) - 1 ] ) ;
 OOOiI1 = '' ;
 for oo0oooooO0 in range ( len ( OOOO00OooO ) ) :
  OOOiI1 += chr ( ord ( OOOO00OooO [ oo0oooooO0 ] ) - OOOO00OooO [ len ( OOOO00OooO ) - 1 ] ) ;
 OOOiI1 = urllib . unquote ( OOOiI1 )
 if 84 - 84: Ii11111i * iIiiiI1IiI1I1 % iiI1i1 + Ii11111i / OOo00O0Oo0oO
 return OOOiI1
 if 80 - 80: II1 + ooO
 if 95 - 95: II11i / Ii1I * II11i - II1 * II1 % o0oOOo0O0Ooo
def iiIiiii1i1i1i ( str ) :
 iI1I1I1i1i = re . findall ( 'unescape\(\'(.*?)\'' , str )
 if 87 - 87: oO0o / ooO . iIi1IIii11I - Ii11111i / o0oOOo0O0Ooo
 if ( not iI1I1I1i1i == None ) and len ( iI1I1I1i1i ) > 0 :
  for iiI1I in iI1I1I1i1i :
   if 69 - 69: IIii1I . Ii11111i / Ii11111i
   str = str . replace ( iiI1I , urllib . unquote ( iiI1I ) )
 return str
 if 72 - 72: ooOoO % OOO0O0O0ooooo . O00ooooo00 / iIi1IIii11I * II11i
OooOoOO0OO = 0
if 27 - 27: ooO * iIiiiI1IiI1I1 . IIii1I - IIii1I
if 5 - 5: ooO
def oOO ( m , html_page , cookieJar ) :
 global OooOoOO0OO
 OooOoOO0OO += 1
 Oo0O0oo0o00o0 = m [ 'expres' ]
 i1o0oooO = m [ 'page' ]
 Ooi1I11 = re . compile ( '\$LiveStreamCaptcha\[([^\]]*)\]' ) . findall ( Oo0O0oo0o00o0 ) [ 0 ]
 if 5 - 5: oO0o % OOo00O0Oo0oO + ooO
 oOoO0O0oO = re . compile ( Ooi1I11 ) . findall ( html_page ) [ 0 ]
 if 13 - 13: ooO
 if not oOoO0O0oO . startswith ( "http" ) :
  ii1II1II = 'http://' + "" . join ( i1o0oooO . split ( '/' ) [ 2 : 3 ] )
  if oOoO0O0oO . startswith ( "/" ) :
   oOoO0O0oO = ii1II1II + oOoO0O0oO
  else :
   oOoO0O0oO = ii1II1II + '/' + oOoO0O0oO
   if 42 - 42: oO0oIIII
 oo0Oo0 = os . path . join ( Iiii , str ( OooOoOO0OO ) + "captcha.jpg" )
 oOOoOOO0oo0 = open ( oo0Oo0 , "wb" )
 if 68 - 68: Ii11111i . IIiIiII11i % iIi1IIii11I - II1 * OOo00O0Oo0oO . Ii11111i
 O00o = urllib2 . Request ( oOoO0O0oO )
 O00o . add_header ( 'User-Agent' , 'Mozilla/5.0 (Windows NT 6.1; rv:14.0) Gecko/20100101 Firefox/14.0.1' )
 if 'referer' in m :
  O00o . add_header ( 'Referer' , m [ 'referer' ] )
 if 'agent' in m :
  O00o . add_header ( 'User-agent' , m [ 'agent' ] )
 if 'setcookie' in m :
  if 46 - 46: i11iIiiIii - Ii11111i * iIiiiI1IiI1I1 * iiI1i1 % I11i * O00ooooo00
  O00o . add_header ( 'Cookie' , m [ 'setcookie' ] )
  if 5 - 5: OOO0O0O0ooooo / iIi1IIii11I . IIiIiII11i + II1
  if 97 - 97: ooO . oO0oIIII . oO0oIIII / IIii1I - o0oOOo0O0Ooo + OOo00O0Oo0oO
  if 32 - 32: Ii11111i . OOooOOo % ooO + I11i + o0oOOo0O0Ooo
  if 76 - 76: o0oOOo0O0Ooo - i11iIiiIii + oO0o + Ii11111i / II1
 urllib2 . urlopen ( O00o )
 O00 = urllib2 . urlopen ( O00o )
 if 50 - 50: ooOoO - II11i + IIii1I + IIii1I
 oOOoOOO0oo0 . write ( O00 . read ( ) )
 O00 . close ( )
 oOOoOOO0oo0 . close ( )
 O00O = O0OOOOOoo ( captcha = oo0Oo0 )
 oooOo = O00O . get ( )
 return oooOo
 if 91 - 91: ooOoO - OOO0O0O0ooooo . IIii1I . OOO0O0O0ooooo + I11i - ooOoO
 if 26 - 26: OOooOOo
def IiIi ( imageregex , html_page , cookieJar , m ) :
 global OooOoOO0OO
 OooOoOO0OO += 1
 if 88 - 88: oO0o - Ii11111i
 if 63 - 63: ooO * II1
 if not imageregex == '' :
  if html_page . startswith ( "http" ) :
   ii1II1II = ii1II ( html_page , cookieJar = cookieJar )
  else :
   ii1II1II = html_page
  oOoO0O0oO = re . compile ( imageregex ) . findall ( html_page ) [ 0 ]
 else :
  oOoO0O0oO = html_page
  if 'oneplay.tv/embed' in html_page :
   import oneplay
   ii1II1II = ii1II ( html_page , cookieJar = cookieJar )
   oOoO0O0oO = oneplay . getCaptchaUrl ( ii1II1II )
   if 19 - 19: ooO - OOooOOo . IIii1I . oO0o / Ii11111i
 oo0Oo0 = os . path . join ( Iiii , str ( OooOoOO0OO ) + "captcha.jpg" )
 oOOoOOO0oo0 = open ( oo0Oo0 , "wb" )
 if 87 - 87: oO0o - iIi1IIii11I - Ii11111i + IIiIiII11i % IIii1I / i11iIiiIii
 O00o = urllib2 . Request ( oOoO0O0oO )
 O00o . add_header ( 'User-Agent' , 'Mozilla/5.0 (Windows NT 6.1; rv:14.0) Gecko/20100101 Firefox/14.0.1' )
 if 'referer' in m :
  O00o . add_header ( 'Referer' , m [ 'referer' ] )
 if 'agent' in m :
  O00o . add_header ( 'User-agent' , m [ 'agent' ] )
 if 'accept' in m :
  O00o . add_header ( 'Accept' , m [ 'accept' ] )
 if 'setcookie' in m :
  if 12 - 12: iIi1IIii11I
  O00o . add_header ( 'Cookie' , m [ 'setcookie' ] )
  if 86 - 86: Ii1I - o0oOOo0O0Ooo
  if 63 - 63: iIiiiI1IiI1I1 / oO0o + II1 . iiI1i1 . iIi1IIii11I
  if 48 - 48: O00ooooo00 - OOo00O0Oo0oO - i11iIiiIii . iiI1i1 - OOo00O0Oo0oO * iiI1i1
  if 60 - 60: oO0o / I11i + Ii11111i - OOo00O0Oo0oO
  if 49 - 49: o0oOOo0O0Ooo - OOO0O0O0ooooo / o0oOOo0O0Ooo * oO0o + II11i
 O00 = urllib2 . urlopen ( O00o )
 if 35 - 35: ooOoO . iIiiiI1IiI1I1 / O00ooooo00 / iIiiiI1IiI1I1 * Ii1I
 oOOoOOO0oo0 . write ( O00 . read ( ) )
 O00 . close ( )
 oOOoOOO0oo0 . close ( )
 O00O = O0OOOOOoo ( captcha = oo0Oo0 )
 oooOo = O00O . get ( )
 return oooOo
 if 85 - 85: ooOoO . iIi1IIii11I % Ii11111i % iiI1i1
 if 80 - 80: Ii1I * iiI1i1 / IIii1I % Ii1I / IIii1I
 if 42 - 42: O00ooooo00 / i11iIiiIii . IIiIiII11i * OOo00O0Oo0oO . i11iIiiIii * OOO0O0O0ooooo
 if 44 - 44: O00ooooo00 . iIiiiI1IiI1I1 / i11iIiiIii + ooO
 if 27 - 27: Ii11111i
 if 52 - 52: II11i % oO0o + IIii1I * Ii1I . oO0oIIII
 if 95 - 95: IIii1I . ooO - II1 * o0oOOo0O0Ooo / OOooOOo
 if 74 - 74: Ii1I
 if 34 - 34: OOo00O0Oo0oO
 if 44 - 44: O00ooooo00 % iIiiiI1IiI1I1 % OOooOOo
 if 9 - 9: IIiIiII11i % II1 - oO0oIIII
 if 43 - 43: o0oOOo0O0Ooo % o0oOOo0O0Ooo
 if 46 - 46: IIiIiII11i % IIii1I . OOo00O0Oo0oO . OOO0O0O0ooooo * iIi1IIii11I / II1
 if 7 - 7: Ii1I - OOO0O0O0ooooo * iiI1i1 - OOooOOo - ooOoO
 if 41 - 41: iIiiiI1IiI1I1 - II11i % ooOoO . II11i - iiI1i1
def i1I111Ii ( name , headname ) :
 if 31 - 31: iIiiiI1IiI1I1
 if 73 - 73: iIi1IIii11I . OOO0O0O0ooooo / OOooOOo - II1 % i11iIiiIii
 O000 = xbmc . Keyboard ( 'default' , 'heading' , True )
 O000 . setDefault ( name )
 O000 . setHeading ( headname )
 O000 . setHiddenInput ( False )
 return O000 . getText ( )
 if 12 - 12: IIiIiII11i
 if 63 - 63: Ii11111i . ooOoO . iiI1i1
 if 46 - 46: iIi1IIii11I % ooO - OOooOOo - IIiIiII11i - oO0oIIII / iiI1i1
 if 68 - 68: O00ooooo00 - I11i / IIiIiII11i % iiI1i1 . OOo00O0Oo0oO
class O0OOOOOoo ( xbmcgui . WindowDialog ) :
 def __init__ ( self , * args , ** kwargs ) :
  self . cptloc = kwargs . get ( 'captcha' )
  self . img = xbmcgui . ControlImage ( 335 , 30 , 624 , 60 , self . cptloc )
  self . addControl ( self . img )
  self . kbd = xbmc . Keyboard ( )
  if 9 - 9: ooO
 def get ( self ) :
  self . show ( )
  time . sleep ( 2 )
  self . kbd . doModal ( )
  if ( self . kbd . isConfirmed ( ) ) :
   iIIIIi = self . kbd . getText ( )
   self . close ( )
   return iIIIIi
  self . close ( )
  return False
  if 50 - 50: II11i + iIi1IIii11I + OOo00O0Oo0oO
  if 15 - 15: iiI1i1
def I1iIi1iIiiIiI ( ) :
 import time
 return str ( int ( time . time ( ) * 1000 ) )
 if 13 - 13: IIii1I * oO0o / II11i % iIi1IIii11I + Ii1I
 if 41 - 41: I11i
def i111iI ( ) :
 import time
 return str ( int ( time . time ( ) ) )
 if 5 - 5: IIiIiII11i
 if 100 - 100: oO0oIIII + IIii1I
def o0o0OoO0OOO0 ( ) :
 oO0OOOO0o0 = [ ]
 oOO0 = sys . argv [ 2 ]
 if len ( oOO0 ) >= 2 :
  O00O00OoO = sys . argv [ 2 ]
  IiIiI1i1 = O00O00OoO . replace ( '?' , '' )
  if ( O00O00OoO [ len ( O00O00OoO ) - 1 ] == '/' ) :
   O00O00OoO = O00O00OoO [ 0 : len ( O00O00OoO ) - 2 ]
  ii11I1IIi1i = IiIiI1i1 . split ( '&' )
  oO0OOOO0o0 = { }
  for oo0oooooO0 in range ( len ( ii11I1IIi1i ) ) :
   iiiiiiiiiiIi = { }
   iiiiiiiiiiIi = ii11I1IIi1i [ oo0oooooO0 ] . split ( '=' )
   if ( len ( iiiiiiiiiiIi ) ) == 2 :
    oO0OOOO0o0 [ iiiiiiiiiiIi [ 0 ] ] = iiiiiiiiiiIi [ 1 ]
 return oO0OOOO0o0
 if 62 - 62: OOO0O0O0ooooo . IIiIiII11i
 if 33 - 33: IIiIiII11i / IIii1I % O00ooooo00
def O0OooOO ( ) :
 OO0Oooo0oOO0O = json . loads ( open ( oo0ooO0oOOOOo ) . read ( ) )
 o0OoOO000ooO0 = len ( OO0Oooo0oOO0O )
 for oo0oooooO0 in OO0Oooo0oOO0O :
  Oo0OoO00oOO0o = oo0oooooO0 [ 0 ]
  O00O0oOO00O00 = oo0oooooO0 [ 1 ]
  i1i1o0oOoOo0 = oo0oooooO0 [ 2 ]
  try :
   o00oooO0Oo = oo0oooooO0 [ 3 ]
   if o00oooO0Oo == None :
    raise
  except :
   if O0 . getSetting ( 'use_thumb' ) == "true" :
    o00oooO0Oo = i1i1o0oOoOo0
   else :
    o00oooO0Oo = ii1I1i1I
  try : O0o0oO = oo0oooooO0 [ 5 ]
  except : O0o0oO = None
  try : Ii1I1i = oo0oooooO0 [ 6 ]
  except : Ii1I1i = None
  if 38 - 38: OOooOOo % II11i + i11iIiiIii + OOo00O0Oo0oO + iIi1IIii11I / i11iIiiIii
  if oo0oooooO0 [ 4 ] == 0 :
   I11I1IIII ( O00O0oOO00O00 , Oo0OoO00oOO0o , i1i1o0oOoOo0 , o00oooO0Oo , '' , '' , '' , 'fav' , O0o0oO , Ii1I1i , o0OoOO000ooO0 )
  else :
   iIi1ii1I1 ( Oo0OoO00oOO0o , O00O0oOO00O00 , oo0oooooO0 [ 4 ] , i1i1o0oOoOo0 , ii1I1i1I , '' , '' , '' , '' , 'fav' )
   if 94 - 94: OOo00O0Oo0oO - IIiIiII11i + Ii1I
   if 59 - 59: iiI1i1 . iIiiiI1IiI1I1 - IIii1I + IIii1I
def oO0o0Oo ( name , url , iconimage , fanart , mode , playlist = None , regexs = None ) :
 o0OO = [ ]
 try :
  if 60 - 60: Ii11111i
  name = name . encode ( 'utf-8' , 'ignore' )
 except :
  pass
 if os . path . exists ( oo0ooO0oOOOOo ) == False :
  IIiI ( 'Making Favorites File' )
  o0OO . append ( ( name , url , iconimage , fanart , mode , playlist , regexs ) )
  IiI1 = open ( oo0ooO0oOOOOo , "w" )
  IiI1 . write ( json . dumps ( o0OO ) )
  IiI1 . close ( )
 else :
  IIiI ( 'Appending Favorites' )
  IiI1 = open ( oo0ooO0oOOOOo ) . read ( )
  i11I1 = json . loads ( IiI1 )
  i11I1 . append ( ( name , url , iconimage , fanart , mode ) )
  iIi1i111II = open ( oo0ooO0oOOOOo , "w" )
  iIi1i111II . write ( json . dumps ( i11I1 ) )
  iIi1i111II . close ( )
  if 65 - 65: oO0o
  if 91 - 91: ooO + oO0oIIII % oO0oIIII - OOO0O0O0ooooo - i11iIiiIii
def OO00Oo00oO ( name ) :
 i11I1 = json . loads ( open ( oo0ooO0oOOOOo ) . read ( ) )
 for i111IiI1I in range ( len ( i11I1 ) ) :
  if i11I1 [ i111IiI1I ] [ 0 ] == name :
   del i11I1 [ i111IiI1I ]
   iIi1i111II = open ( oo0ooO0oOOOOo , "w" )
   iIi1i111II . write ( json . dumps ( i11I1 ) )
   iIi1i111II . close ( )
   break
 xbmc . executebuiltin ( "XBMC.Container.Refresh" )
 if 94 - 94: i11iIiiIii / II11i / IIiIiII11i
 if 9 - 9: iiI1i1 / oO0o / ooOoO + II11i
def o0O0 ( url ) :
 import urlresolver
 oOO0Oooo = urlresolver . HostedMediaFile ( url )
 if oOO0Oooo :
  IiI1iiiIii = urlresolver . resolve ( url )
  II1iOOoOO0O0o0 = IiI1iiiIii
  if isinstance ( II1iOOoOO0O0o0 , list ) :
   for I1i11111i1i11 in II1iOOoOO0O0o0 :
    I1II1 = O0 . getSetting ( 'quality' )
    if I1i11111i1i11 [ 'quality' ] == 'HD' :
     IiI1iiiIii = I1i11111i1i11 [ 'url' ]
     break
    elif I1i11111i1i11 [ 'quality' ] == 'SD' :
     IiI1iiiIii = I1i11111i1i11 [ 'url' ]
    elif I1i11111i1i11 [ 'quality' ] == '1080p' and O0 . getSetting ( '1080pquality' ) == 'true' :
     IiI1iiiIii = I1i11111i1i11 [ 'url' ]
     break
  else :
   IiI1iiiIii = II1iOOoOO0O0o0
 else :
  xbmc . executebuiltin ( "XBMC.Notification(Evilsport,Urlresolver donot support this domain. - ,5000)" )
  IiI1iiiIii = url
 return IiI1iiiIii
 if 89 - 89: o0oOOo0O0Ooo / o0oOOo0O0Ooo
 if 1 - 1: I11i . i11iIiiIii
def OooooOo ( name , mu_playlist , queueVideo = None ) :
 O0o0oO = xbmc . PlayList ( xbmc . PLAYLIST_VIDEO )
 if 48 - 48: Ii1I - ooOoO + O00ooooo00 . OOO0O0O0ooooo + iIiiiI1IiI1I1
 if O0 . getSetting ( 'ask_playlist_items' ) == 'true' and not queueVideo :
  import urlparse
  OO0OOoooo0o = [ ]
  for oo0oooooO0 in mu_playlist :
   IiIi1Ii = urlparse . urlparse ( oo0oooooO0 ) . netloc
   if IiIi1Ii == '' :
    OO0OOoooo0o . append ( name )
   else :
    OO0OOoooo0o . append ( IiIi1Ii )
  iiIIiI11II1 = xbmcgui . Dialog ( )
  i111IiI1I = iiIIiI11II1 . select ( 'Choose a video source' , OO0OOoooo0o )
  if i111IiI1I >= 0 :
   if "&mode=19" in mu_playlist [ i111IiI1I ] :
    if 79 - 79: II1 / I11i . OOO0O0O0ooooo
    xbmc . Player ( ) . play ( o0O0 ( mu_playlist [ i111IiI1I ] . replace ( '&mode=19' , '' ) . replace ( ';' , '' ) ) )
   elif "$doregex" in mu_playlist [ i111IiI1I ] :
    if 79 - 79: Ii1I - ooOoO
    Ii1iiI1 = mu_playlist [ i111IiI1I ] . split ( '&regexs=' )
    if 76 - 76: oO0oIIII * IIii1I
    O00O0oOO00O00 , iIi1i = i1II1I1Iii1 ( Ii1iiI1 [ 1 ] , Ii1iiI1 [ 0 ] )
    iiI1iI = O00O0oOO00O00 . replace ( ';' , '' )
    xbmc . Player ( ) . play ( iiI1iI )
    if 84 - 84: II1 + II11i / iIiiiI1IiI1I1 % Ii11111i % I11i * iIiiiI1IiI1I1
   else :
    O00O0oOO00O00 = mu_playlist [ i111IiI1I ]
    xbmc . Player ( ) . play ( O00O0oOO00O00 )
 elif not queueVideo :
  if 58 - 58: o0oOOo0O0Ooo - oO0o . i11iIiiIii % i11iIiiIii / O00ooooo00 / Ii1I
  O0o0oO . clear ( )
  OO0O0 = 0
  for oo0oooooO0 in mu_playlist :
   OO0O0 += 1
   Ii1ii1IiiiiiI = xbmcgui . ListItem ( '%s) %s' % ( str ( OO0O0 ) , name ) )
   if 77 - 77: i11iIiiIii
   try :
    if "$doregex" in oo0oooooO0 :
     Ii1iiI1 = oo0oooooO0 . split ( '&regexs=' )
     if 20 - 20: iiI1i1 * iIiiiI1IiI1I1
     O00O0oOO00O00 , iIi1i = i1II1I1Iii1 ( Ii1iiI1 [ 1 ] , Ii1iiI1 [ 0 ] )
    elif "&mode=19" in oo0oooooO0 :
     O00O0oOO00O00 = o0O0 ( oo0oooooO0 . replace ( '&mode=19' , '' ) . replace ( ';' , '' ) )
    if O00O0oOO00O00 :
     O0o0oO . add ( O00O0oOO00O00 , Ii1ii1IiiiiiI )
    else :
     raise
   except Exception :
    O0o0oO . add ( oo0oooooO0 , Ii1ii1IiiiiiI )
    pass
    if 56 - 56: OOo00O0Oo0oO . II11i
  xbmc . executebuiltin ( 'playlist.playoffset(video,0)' )
 else :
  if 3 - 3: oO0oIIII + II11i . O00ooooo00 / Ii11111i % II11i
  I1iii = xbmcgui . ListItem ( name )
  O0o0oO . add ( mu_playlist , I1iii )
  if 98 - 98: ooO * IIii1I . oO0oIIII * IIiIiII11i / I11i + iIi1IIii11I
  if 25 - 25: Ii1I
def Iii11111iiI ( name , url ) :
 if O0 . getSetting ( 'save_location' ) == "" :
  xbmc . executebuiltin ( "XBMC.Notification('Evilsport','Choose a location to save files.',15000," + OOooO + ")" )
  O0 . openSettings ( )
 O00O00OoO = { 'url' : url , 'download_path' : O0 . getSetting ( 'save_location' ) }
 downloader . download ( name , O00O00OoO )
 iiIIiI11II1 = xbmcgui . Dialog ( )
 OoOoO00O0 = iiIIiI11II1 . yesno ( 'Evilsport' , 'Do you want to add this file as a source?' )
 if OoOoO00O0 :
  O0OOO00oo ( os . path . join ( O0 . getSetting ( 'save_location' ) , name ) )
  if 67 - 67: OOooOOo
  if 76 - 76: oO0o - iIiiiI1IiI1I1 + Ii11111i + iiI1i1
def i1Iiii ( url , name ) :
 if 87 - 87: ooO / II11i - IIiIiII11i
 oOOoOOO0oOoo = [ 'plugin://plugin.video.genesis/?action=shows_search' , 'plugin://plugin.video.genesis/?action=movies_search' , 'plugin://plugin.video.salts/?mode=search&amp;section=Movies' , 'plugin://plugin.video.salts/?mode=search&amp;section=TV' , 'plugin://plugin.video.muchmovies.hd/?action=movies_search' , 'plugin://plugin.video.viooz.co/?action=root_search' , 'plugin://plugin.video.ororotv/?action=shows_search' , 'plugin://plugin.video.yifymovies.hd/?action=movies_search' , 'plugin://plugin.video.cartoonhdtwo/?description&amp;fanart&amp;iconimage&amp;mode=3&amp;name=Search&amp;url=url' , 'plugin://plugin.video.youtube/kodion/search/list/' , 'plugin://plugin.video.dailymotion_com/?mode=search&amp;url' , 'plugin://plugin.video.vimeo/kodion/search/list/' ]
 if 65 - 65: OOo00O0Oo0oO . Ii1I - oO0oIIII
 if 93 - 93: OOO0O0O0ooooo
 if 4 - 4: iIiiiI1IiI1I1 / iIiiiI1IiI1I1
 if 82 - 82: iiI1i1 / iIi1IIii11I * iiI1i1 % i11iIiiIii * ooOoO
 if 83 - 83: o0oOOo0O0Ooo + Ii11111i - OOooOOo + IIii1I % IIiIiII11i
 if 23 - 23: OOooOOo + oO0oIIII % oO0o % iIiiiI1IiI1I1 % II1
 if 78 - 78: o0oOOo0O0Ooo / IIiIiII11i - IIii1I - i11iIiiIii * OOo00O0Oo0oO
 if 84 - 84: Ii11111i + oO0oIIII + OOooOOo
 if 33 - 33: oO0oIIII
 if 93 - 93: iIi1IIii11I
 if 34 - 34: Ii1I - iIi1IIii11I * IIiIiII11i / OOooOOo
 if 19 - 19: I11i
 OO0OOoooo0o = [ 'Gensis TV' , 'Genesis Movie' , 'Salt movie' , 'salt TV' , 'Muchmovies' , 'viooz' , 'ORoroTV' , 'Yifymovies' , 'cartoonHD' , 'Youtube' , 'DailyMotion' , 'Vimeo' ]
 if 46 - 46: IIii1I . i11iIiiIii - oO0o % OOO0O0O0ooooo / ooOoO * O00ooooo00
 iiIIiI11II1 = xbmcgui . Dialog ( )
 i111IiI1I = iiIIiI11II1 . select ( 'Choose a video source' , OO0OOoooo0o )
 if 66 - 66: OOO0O0O0ooooo
 if i111IiI1I >= 0 :
  url = oOOoOOO0oOoo [ i111IiI1I ]
  if 52 - 52: o0oOOo0O0Ooo * II1
  Ii11iiI ( url )
  if 71 - 71: II11i - OOooOOo - Ii11111i
  if 28 - 28: IIii1I
def iIi1ii1I1 ( name , url , mode , iconimage , fanart , description , genre , date , credits , showcontext = False , regexs = None , reg_url = None , allinfo = { } ) :
 if 7 - 7: OOooOOo % ooO * oO0o
 O0O00 = sys . argv [ 0 ] + "?url=" + urllib . quote_plus ( url ) + "&mode=" + str ( mode ) + "&name=" + urllib . quote_plus ( name ) + "&fanart=" + urllib . quote_plus ( fanart )
 Iii11I1iII1 = True
 if date == '' :
  date = None
 else :
  description += '\n\nDate: %s' % date
 IIi11 = xbmcgui . ListItem ( name , iconImage = "DefaultFolder.png" , thumbnailImage = iconimage )
 if len ( allinfo ) < 1 :
  IIi11 . setInfo ( type = "Video" , infoLabels = { "Title" : name , "Plot" : description , "Genre" : genre , "dateadded" : date , "credits" : credits } )
 else :
  IIi11 . setInfo ( type = "Video" , infoLabels = allinfo )
 IIi11 . setProperty ( "Fanart_Image" , fanart )
 if showcontext :
  o0O0oo0 = [ ]
  iIIIiIi = O0 . getSetting ( 'parentalblocked' )
  iIIIiIi = iIIIiIi == "true"
  iIIi1 = O0 . getSetting ( 'parentalblockedpin' )
  if 75 - 75: ooO % i11iIiiIii + IIii1I
  if len ( iIIi1 ) > 0 :
   if iIIIiIi :
    o0O0oo0 . append ( ( 'Disable Parental Block' , 'XBMC.RunPlugin(%s?mode=55&name=%s)' % ( sys . argv [ 0 ] , urllib . quote_plus ( name ) ) ) )
   else :
    o0O0oo0 . append ( ( 'Enable Parental Block' , 'XBMC.RunPlugin(%s?mode=56&name=%s)' % ( sys . argv [ 0 ] , urllib . quote_plus ( name ) ) ) )
    if 92 - 92: oO0o % OOO0O0O0ooooo
  if showcontext == 'source' :
   if 55 - 55: IIii1I * OOo00O0Oo0oO
   if name in str ( i1iIIIiI1I ) :
    o0O0oo0 . append ( ( 'Remove from Sources' , 'XBMC.RunPlugin(%s?mode=8&name=%s)' % ( sys . argv [ 0 ] , urllib . quote_plus ( name ) ) ) )
    if 85 - 85: IIii1I . ooOoO
    if 54 - 54: oO0oIIII . II1 % IIiIiII11i
  elif showcontext == 'download' :
   o0O0oo0 . append ( ( 'Download' , 'XBMC.RunPlugin(%s?url=%s&mode=9&name=%s)'
 % ( sys . argv [ 0 ] , urllib . quote_plus ( url ) , urllib . quote_plus ( name ) ) ) )
  elif showcontext == 'fav' :
   o0O0oo0 . append ( ( 'Remove from Evilsport Favorites' , 'XBMC.RunPlugin(%s?mode=6&name=%s)'
 % ( sys . argv [ 0 ] , urllib . quote_plus ( name ) ) ) )
  if showcontext == '!!update' :
   ii111I11Ii = (
 '%s?url=%s&mode=17&regexs=%s'
 % ( sys . argv [ 0 ] , urllib . quote_plus ( reg_url ) , regexs )
 )
   o0O0oo0 . append ( ( '[COLOR yellow]!!update[/COLOR]' , 'XBMC.RunPlugin(%s)' % ii111I11Ii ) )
  if not name in OO0O00OooO :
   o0O0oo0 . append ( ( 'Add to Evilsport Favorites' , 'XBMC.RunPlugin(%s?mode=5&name=%s&url=%s&iconimage=%s&fanart=%s&fav_mode=%s)'
 % ( sys . argv [ 0 ] , urllib . quote_plus ( name ) , urllib . quote_plus ( url ) , urllib . quote_plus ( iconimage ) , urllib . quote_plus ( fanart ) , mode ) ) )
  IIi11 . addContextMenuItems ( o0O0oo0 )
 Iii11I1iII1 = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = O0O00 , listitem = IIi11 , isFolder = True )
 return Iii11I1iII1
 if 6 - 6: oO0oIIII
 if 77 - 77: O00ooooo00 + o0oOOo0O0Ooo . iIiiiI1IiI1I1 * Ii11111i / ooO / oO0oIIII
def oOoo ( url , title , media_type = 'video' ) :
 if 57 - 57: OOooOOo / II11i
 if 13 - 13: II1 + o0oOOo0O0Ooo
 import youtubedl
 if not url == '' :
  if media_type == 'audio' :
   youtubedl . single_YD ( url , download = True , audio = True )
  else :
   youtubedl . single_YD ( url , download = True )
 elif xbmc . Player ( ) . isPlaying ( ) == True :
  import YDStreamExtractor
  if YDStreamExtractor . isDownloading ( ) == True :
   if 32 - 32: OOO0O0O0ooooo + Ii1I % IIiIiII11i
   YDStreamExtractor . manageDownloads ( )
  else :
   iI1iI = xbmc . Player ( ) . getPlayingFile ( )
   if 100 - 100: iIi1IIii11I / iIi1IIii11I - Ii11111i % Ii11111i * Ii1I / ooO
   iI1iI = iI1iI . split ( '|User-Agent=' ) [ 0 ]
   Ii1ii1IiiiiiI = { 'url' : iI1iI , 'title' : title , 'media_type' : media_type }
   youtubedl . single_YD ( '' , download = True , dl_info = Ii1ii1IiiiiiI )
 else :
  xbmc . executebuiltin ( "XBMC.Notification(DOWNLOAD,First Play [COLOR yellow]WHILE playing download[/COLOR] ,10000)" )
  if 32 - 32: iIiiiI1IiI1I1 + I11i - Ii1I + I11i / O00ooooo00 * Ii1I
  if 90 - 90: oO0oIIII % Ii1I
def iiii1 ( string ) :
 if isinstance ( string , basestring ) :
  if isinstance ( string , unicode ) :
   string = string . encode ( 'ascii' , 'ignore' )
 return string
 if 60 - 60: iIiiiI1IiI1I1 % Ii1I / OOooOOo % Ii1I * i11iIiiIii / OOo00O0Oo0oO
 if 34 - 34: II11i - Ii11111i
def IIIiIi1iiI ( string , encoding = 'utf-8' ) :
 if isinstance ( string , basestring ) :
  if not isinstance ( string , unicode ) :
   string = unicode ( string , encoding , 'ignore' )
 return string
 if 15 - 15: I11i . OOo00O0Oo0oO
 if 94 - 94: iiI1i1 . iIiiiI1IiI1I1
def oooOoo0OoOO0000 ( s ) : return "" . join ( filter ( lambda i11Ii1iIIIIi : ord ( i11Ii1iIIIIi ) < 128 , s ) )
if 14 - 14: II1 . OOooOOo . iiI1i1
if 50 - 50: iIi1IIii11I * oO0o + I11i - i11iIiiIii + IIiIiII11i * I11i
def i11II ( command ) :
 i11I1 = ''
 try :
  i11I1 = xbmc . executeJSONRPC ( IIIiIi1iiI ( command ) )
 except UnicodeEncodeError :
  i11I1 = xbmc . executeJSONRPC ( iiii1 ( command ) )
  if 69 - 69: II11i - O00ooooo00 % OOo00O0Oo0oO . Ii11111i - Ii11111i
 return IIIiIi1iiI ( i11I1 )
 if 65 - 65: Ii11111i + ooOoO
 if 61 - 61: i11iIiiIii * Ii1I % IIiIiII11i * II11i - II1 - o0oOOo0O0Ooo
def Ii11iiI ( url , give_me_result = None , playlist = False ) :
 if 'audio' in url :
  o0OOo = IIIiIi1iiI ( '{"jsonrpc":"2.0","method":"Files.GetDirectory","params": {"directory":"%s","media":"video", "properties": ["title", "album", "artist", "duration","thumbnail", "year"]}, "id": 1}' ) % url
 else :
  o0OOo = IIIiIi1iiI ( '{"jsonrpc":"2.0","method":"Files.GetDirectory","params":{"directory":"%s","media":"video","properties":[ "plot","playcount","director", "genre","votes","duration","trailer","premiered","thumbnail","title","year","dateadded","fanart","rating","season","episode","studio","mpaa"]},"id":1}' ) % url
 IiI1Ii11Ii = json . loads ( i11II ( o0OOo ) )
 if 99 - 99: OOO0O0O0ooooo . OOooOOo % iiI1i1 - IIiIiII11i / iiI1i1
 if give_me_result :
  return IiI1Ii11Ii
 if IiI1Ii11Ii . has_key ( 'error' ) :
  return
 else :
  if 20 - 20: oO0o * OOo00O0Oo0oO
  for oo0oooooO0 in IiI1Ii11Ii [ 'result' ] [ 'files' ] :
   i1i1I1iiIiIII = { }
   url = oo0oooooO0 [ 'file' ]
   Oo0OoO00oOO0o = oooOoo0OoOO0000 ( oo0oooooO0 [ 'label' ] )
   I11i1iIII = oooOoo0OoOO0000 ( oo0oooooO0 [ 'thumbnail' ] )
   ii1I1i1I = oooOoo0OoOO0000 ( oo0oooooO0 [ 'fanart' ] )
   i1i1I1iiIiIII = dict ( ( k , v ) for k , v in oo0oooooO0 . iteritems ( ) if not v == '0' or not v == - 1 or v == '' )
   i1i1I1iiIiIII . pop ( "file" , None )
   if oo0oooooO0 [ 'filetype' ] == 'file' :
    if playlist :
     OooooOo ( Oo0OoO00oOO0o , url , queueVideo = '1' )
     continue
    else :
     I11I1IIII ( url , Oo0OoO00oOO0o , I11i1iIII , ii1I1i1I , '' , '' , '' , '' , None , '' , total = len ( IiI1Ii11Ii [ 'result' ] [ 'files' ] ) , allinfo = i1i1I1iiIiIII )
     if 68 - 68: OOO0O0O0ooooo
     if oo0oooooO0 [ 'type' ] and oo0oooooO0 [ 'type' ] == 'tvshow' :
      xbmcplugin . setContent ( int ( sys . argv [ 1 ] ) , 'tvshows' )
     elif oo0oooooO0 [ 'episode' ] > 0 :
      xbmcplugin . setContent ( int ( sys . argv [ 1 ] ) , 'episodes' )
      if 76 - 76: I11i
   else :
    iIi1ii1I1 ( Oo0OoO00oOO0o , url , 53 , I11i1iIII , ii1I1i1I , '' , '' , '' , '' , allinfo = i1i1I1iiIiIII )
  xbmcplugin . endOfDirectory ( int ( sys . argv [ 1 ] ) )
  if 99 - 99: OOooOOo
  if 1 - 1: oO0oIIII * oO0o * o0oOOo0O0Ooo + IIiIiII11i
def I11I1IIII ( url , name , iconimage , fanart , description , genre , date , showcontext , playlist , regexs , total , setCookie = "" , allinfo = { } ) :
 if 90 - 90: II11i % IIiIiII11i - IIiIiII11i . IIii1I / Ii11111i + iiI1i1
 o0O0oo0 = [ ]
 iIIIiIi = O0 . getSetting ( 'parentalblocked' )
 iIIIiIi = iIIIiIi == "true"
 iIIi1 = O0 . getSetting ( 'parentalblockedpin' )
 if 89 - 89: Ii1I
 if len ( iIIi1 ) > 0 :
  if iIIIiIi :
   o0O0oo0 . append ( ( 'Disable Parental Block' , 'XBMC.RunPlugin(%s?mode=55&name=%s)' % ( sys . argv [ 0 ] , urllib . quote_plus ( name ) ) ) )
  else :
   o0O0oo0 . append ( ( 'Enable Parental Block' , 'XBMC.RunPlugin(%s?mode=56&name=%s)' % ( sys . argv [ 0 ] , urllib . quote_plus ( name ) ) ) )
   if 87 - 87: OOo00O0Oo0oO % IIiIiII11i
 try :
  name = name . encode ( 'utf-8' )
 except : pass
 Iii11I1iII1 = True
 OOo000o = False
 if regexs :
  iiIIIIiI111 = '17'
  if 'listrepeat' in regexs :
   OOo000o = True
   if 86 - 86: ooOoO % IIii1I / I11i - OOooOOo * oO0oIIII . iIiiiI1IiI1I1
  o0O0oo0 . append ( ( '[COLOR white]!!Download Currently Playing!![/COLOR]' , 'XBMC.RunPlugin(%s?url=%s&mode=21&name=%s)'
 % ( sys . argv [ 0 ] , urllib . quote_plus ( url ) , urllib . quote_plus ( name ) ) ) )
 elif ( any ( x in url for x in IiiIII111iI ) and url . startswith ( 'http' ) ) or url . endswith ( '&mode=19' ) :
  url = url . replace ( '&mode=19' , '' )
  iiIIIIiI111 = '19'
  o0O0oo0 . append ( ( '[COLOR white]!!Download Currently Playing!![/COLOR]' , 'XBMC.RunPlugin(%s?url=%s&mode=21&name=%s)'
 % ( sys . argv [ 0 ] , urllib . quote_plus ( url ) , urllib . quote_plus ( name ) ) ) )
 elif url . endswith ( '&mode=18' ) :
  url = url . replace ( '&mode=18' , '' )
  iiIIIIiI111 = '18'
  o0O0oo0 . append ( ( '[COLOR white]!!Download!![/COLOR]' , 'XBMC.RunPlugin(%s?url=%s&mode=23&name=%s)'
 % ( sys . argv [ 0 ] , urllib . quote_plus ( url ) , urllib . quote_plus ( name ) ) ) )
  if O0 . getSetting ( 'dlaudioonly' ) == 'true' :
   o0O0oo0 . append ( ( '!!Download [COLOR seablue]Audio!![/COLOR]' , 'XBMC.RunPlugin(%s?url=%s&mode=24&name=%s)'
 % ( sys . argv [ 0 ] , urllib . quote_plus ( url ) , urllib . quote_plus ( name ) ) ) )
 elif url . startswith ( 'magnet:?xt=' ) :
  if '&' in url and not '&amp;' in url :
   url = url . replace ( '&' , '&amp;' )
  url = 'plugin://plugin.video.pulsar/play?uri=' + url
  iiIIIIiI111 = '12'
 else :
  iiIIIIiI111 = '12'
  o0O0oo0 . append ( ( '[COLOR white]!!Download Currently Playing!![/COLOR]' , 'XBMC.RunPlugin(%s?url=%s&mode=21&name=%s)'
 % ( sys . argv [ 0 ] , urllib . quote_plus ( url ) , urllib . quote_plus ( name ) ) ) )
 if 'plugin://plugin.video.youtube/play/?video_id=' in url :
  OoOoOoo0OoO0 = url . replace ( 'plugin://plugin.video.youtube/play/?video_id=' , 'https://www.youtube.com/watch?v=' )
  o0O0oo0 . append ( ( '!!Download [COLOR blue]Audio!![/COLOR]' , 'XBMC.RunPlugin(%s?url=%s&mode=24&name=%s)'
 % ( sys . argv [ 0 ] , urllib . quote_plus ( OoOoOoo0OoO0 ) , urllib . quote_plus ( name ) ) ) )
 O0O00 = sys . argv [ 0 ] + "?"
 I1iiI1iiI1i1 = False
 if playlist :
  if O0 . getSetting ( 'add_playlist' ) == "false" :
   O0O00 += "url=" + urllib . quote_plus ( url ) + "&mode=" + iiIIIIiI111
  else :
   O0O00 += "mode=13&name=%s&playlist=%s" % ( urllib . quote_plus ( name ) , urllib . quote_plus ( str ( playlist ) . replace ( ',' , '||' ) ) )
   name = name + '[COLOR magenta] (' + str ( len ( playlist ) ) + ' items )[/COLOR]'
   I1iiI1iiI1i1 = True
 else :
  O0O00 += "url=" + urllib . quote_plus ( url ) + "&mode=" + iiIIIIiI111
 if regexs :
  O0O00 += "&regexs=" + regexs
 if not setCookie == '' :
  O0O00 += "&setCookie=" + urllib . quote_plus ( setCookie )
  if 88 - 88: Ii1I % IIiIiII11i - iiI1i1 % Ii1I + ooO - OOo00O0Oo0oO
 if date == '' :
  date = None
 else :
  description += '\n\nDate: %s' % date
 IIi11 = xbmcgui . ListItem ( name , iconImage = "DefaultVideo.png" , thumbnailImage = iconimage )
 if len ( allinfo ) < 1 :
  IIi11 . setInfo ( type = "Video" , infoLabels = { "Title" : name , "Plot" : description , "Genre" : genre , "dateadded" : date } )
  if 23 - 23: OOO0O0O0ooooo
 else :
  IIi11 . setInfo ( type = "Video" , infoLabels = allinfo )
 IIi11 . setProperty ( "Fanart_Image" , fanart )
 if 9 - 9: iiI1i1 * IIiIiII11i . iIi1IIii11I * i11iIiiIii - OOO0O0O0ooooo
 if ( not I1iiI1iiI1i1 ) and not any ( x in url for x in IiII ) and not '$PLAYERPROXY$=' in url :
  if regexs :
   if 54 - 54: iIiiiI1IiI1I1 * Ii11111i + OOooOOo % O00ooooo00 - OOooOOo + oO0o
   if '$pyFunction:playmedia(' not in urllib . unquote_plus ( regexs ) and 'notplayable' not in urllib . unquote_plus ( regexs ) and 'listrepeat' not in urllib . unquote_plus ( regexs ) :
    if 15 - 15: oO0o * Ii1I + Ii11111i . iiI1i1 % iIiiiI1IiI1I1 - iIi1IIii11I
    IIi11 . setProperty ( 'IsPlayable' , 'true' )
  else :
   IIi11 . setProperty ( 'IsPlayable' , 'true' )
 else :
  IIiI ( 'NOT setting isplayable' + url )
 if showcontext :
  if 13 - 13: oO0o % oO0o % IIiIiII11i % iIiiiI1IiI1I1 * O00ooooo00 % iiI1i1
  if showcontext == 'fav' :
   o0O0oo0 . append (
 ( 'Remove from Evilsport Favorites' , 'XBMC.RunPlugin(%s?mode=6&name=%s)'
 % ( sys . argv [ 0 ] , urllib . quote_plus ( name ) ) )
 )
  elif not name in OO0O00OooO :
   try :
    O0i1I11I = (
 '%s?mode=5&name=%s&url=%s&iconimage=%s&fanart=%s&fav_mode=0'
 % ( sys . argv [ 0 ] , urllib . quote_plus ( name ) , urllib . quote_plus ( url ) , urllib . quote_plus ( iconimage ) , urllib . quote_plus ( fanart ) )
 )
   except :
    O0i1I11I = (
 '%s?mode=5&name=%s&url=%s&iconimage=%s&fanart=%s&fav_mode=0'
 % ( sys . argv [ 0 ] , urllib . quote_plus ( name ) , urllib . quote_plus ( url ) , urllib . quote_plus ( iconimage . encode ( "utf-8" ) ) , urllib . quote_plus ( fanart . encode ( "utf-8" ) ) )
 )
   if playlist :
    O0i1I11I += 'playlist=' + urllib . quote_plus ( str ( playlist ) . replace ( ',' , '||' ) )
   if regexs :
    O0i1I11I += "&regexs=" + regexs
   o0O0oo0 . append ( ( 'Add to Evilsport Favorites' , 'XBMC.RunPlugin(%s)' % O0i1I11I ) )
  IIi11 . addContextMenuItems ( o0O0oo0 )
 if not playlist is None :
  if O0 . getSetting ( 'add_playlist' ) == "false" :
   I1IIi1i1Ii1I1 = name . split ( ') ' ) [ 1 ]
   Ooo0ooo = [
 ( 'Play ' + I1IIi1i1Ii1I1 + ' PlayList' , 'XBMC.RunPlugin(%s?mode=13&name=%s&playlist=%s)'
 % ( sys . argv [ 0 ] , urllib . quote_plus ( I1IIi1i1Ii1I1 ) , urllib . quote_plus ( str ( playlist ) . replace ( ',' , '||' ) ) ) )
 ]
   IIi11 . addContextMenuItems ( Ooo0ooo )
   if 75 - 75: iiI1i1 . Ii11111i - IIii1I * o0oOOo0O0Ooo * OOo00O0Oo0oO
 Iii11I1iII1 = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = O0O00 , listitem = IIi11 , totalItems = total , isFolder = OOo000o )
 if 93 - 93: iIi1IIii11I
 if 18 - 18: iIi1IIii11I
 return Iii11I1iII1
 if 66 - 66: Ii1I * i11iIiiIii + oO0o / Ii11111i
 if 96 - 96: Ii11111i + Ii11111i % ooO % Ii11111i
def IiiI1I ( url , name , iconimage , setresolved = True ) :
 if setresolved :
  Ii11iIII = True
  if '$$LSDirect$$' in url :
   url = url . replace ( '$$LSDirect$$' , '' )
   Ii11iIII = False
   if 58 - 58: OOO0O0O0ooooo
  IIi11 = xbmcgui . ListItem ( name , iconImage = iconimage )
  IIi11 . setInfo ( type = 'Video' , infoLabels = { 'Title' : name } )
  IIi11 . setProperty ( "IsPlayable" , "true" )
  IIi11 . setPath ( url )
  if not Ii11iIII :
   xbmc . Player ( ) . play ( url )
  else :
   xbmcplugin . setResolvedUrl ( int ( sys . argv [ 1 ] ) , True , IIi11 )
   if 91 - 91: OOo00O0Oo0oO / I11i . OOo00O0Oo0oO - OOooOOo + I11i
 else :
  xbmc . executebuiltin ( 'XBMC.RunPlugin(' + url + ')' )
  if 72 - 72: oO0oIIII . ooO * I11i / I11i / OOo00O0Oo0oO
  if 13 - 13: O00ooooo00
def IIo0Oo0oO0oOO00 ( link ) :
 O00O0oOO00O00 = urllib . urlopen ( link )
 Ii1IIII1ii1I = O00O0oOO00O00 . read ( )
 O00O0oOO00O00 . close ( )
 OO0O0OO = Ii1IIII1ii1I . split ( "Jetzt" )
 iiii11IiIiI = OO0O0OO [ 1 ] . split ( 'programm/detail.php?const_id=' )
 i1IiiI = iiii11IiIiI [ 1 ] . split ( '<br /><a href="/' )
 O0OOO0 = i1IiiI [ 0 ] [ 40 : len ( i1IiiI [ 0 ] ) ]
 o0OIi = iiii11IiIiI [ 2 ] . split ( "</a></p></div>" )
 IIi1iiI = o0OIi [ 0 ] [ 17 : len ( o0OIi [ 0 ] ) ]
 IIi1iiI = IIi1iiI . encode ( 'utf-8' )
 return "  - " + IIi1iiI + " - " + O0OOO0
 if 97 - 97: II11i . iiI1i1 / iIiiiI1IiI1I1
 if 83 - 83: iiI1i1 - I11i * Ii1I
def oOo0OOoO0 ( url , regex ) :
 i11I1 = o0O00oooo ( url )
 try :
  OO0O0 = re . findall ( regex , i11I1 ) [ 0 ]
  return OO0O0
 except :
  IIiI ( 'regex failed' )
  IIiI ( regex )
  return
  if 90 - 90: IIiIiII11i * iIiiiI1IiI1I1
  if 75 - 75: I11i - oO0o * i11iIiiIii . II1 - IIiIiII11i . iiI1i1
def I1iI1i11IiI11 ( d , root = "root" , nested = 0 ) :
 if 82 - 82: II11i * o0oOOo0O0Ooo
 i1o0 = lambda o0OO0OO000OO : '<' + o0OO0OO000OO + '>'
 O00o0000OO = lambda o0OO0OO000OO : '</' + o0OO0OO000OO + '>\n'
 if 61 - 61: ooO % O00ooooo00 - OOo00O0Oo0oO . iIi1IIii11I - IIiIiII11i + IIiIiII11i
 II1ii1Ii = lambda oO0o00oOOooO0 , I1iIIIIIi : I1iIIIIIi + i1o0 ( iiIiIiIiiIiI ) + str ( oO0o00oOOooO0 ) + O00o0000OO ( iiIiIiIiiIiI )
 I1iIIIIIi = i1o0 ( root ) + '\n' if root else ""
 if 23 - 23: o0oOOo0O0Ooo / OOo00O0Oo0oO / IIii1I
 for iiIiIiIiiIiI , III in d . iteritems ( ) :
  IiiI = type ( III )
  if nested == 0 : iiIiIiIiiIiI = 'regex'
  if IiiI is list :
   for oO0o00oOOooO0 in III :
    oO0o00oOOooO0 = escape ( oO0o00oOOooO0 )
    I1iIIIIIi = II1ii1Ii ( oO0o00oOOooO0 , I1iIIIIIi )
    if 75 - 75: II1 . Ii11111i + o0oOOo0O0Ooo / oO0oIIII - iIiiiI1IiI1I1 % oO0oIIII
  if IiiI is dict :
   I1iIIIIIi = II1ii1Ii ( '\n' + I1iI1i11IiI11 ( III , None , nested + 1 ) , I1iIIIIIi )
  if IiiI is not list and IiiI is not dict :
   if not III is None : III = escape ( III )
   if 89 - 89: OOo00O0Oo0oO * IIii1I + i11iIiiIii . II1
   if III is None :
    I1iIIIIIi = II1ii1Ii ( III , I1iIIIIIi )
   else :
    if 51 - 51: Ii11111i / iIi1IIii11I + o0oOOo0O0Ooo % oO0o / oO0oIIII
    I1iIIIIIi = II1ii1Ii ( III . encode ( "utf-8" ) , I1iIIIIIi )
    if 25 - 25: OOooOOo
 I1iIIIIIi += O00o0000OO ( root ) if root else ""
 if 25 - 25: iIi1IIii11I * OOo00O0Oo0oO / iiI1i1 / iiI1i1 % OOooOOo
 return I1iIIIIIi
xbmcplugin . setContent ( int ( sys . argv [ 1 ] ) , 'movies' )
if 19 - 19: Ii1I - IIii1I / iIi1IIii11I . o0oOOo0O0Ooo * OOO0O0O0ooooo - OOO0O0O0ooooo
try :
 xbmcplugin . addSortMethod ( int ( sys . argv [ 1 ] ) , xbmcplugin . SORT_METHOD_UNSORTED )
except :
 pass
try :
 xbmcplugin . addSortMethod ( int ( sys . argv [ 1 ] ) , xbmcplugin . SORT_METHOD_LABEL )
except :
 pass
try :
 xbmcplugin . addSortMethod ( int ( sys . argv [ 1 ] ) , xbmcplugin . SORT_METHOD_DATE )
except :
 pass
try :
 xbmcplugin . addSortMethod ( int ( sys . argv [ 1 ] ) , xbmcplugin . SORT_METHOD_GENRE )
except :
 pass
 if 41 - 41: O00ooooo00 - iIiiiI1IiI1I1
O00O00OoO = o0o0OoO0OOO0 ( )
if 48 - 48: iIiiiI1IiI1I1 - ooOoO / o0oOOo0O0Ooo + iIiiiI1IiI1I1
O00O0oOO00O00 = None
Oo0OoO00oOO0o = None
iiIIIIiI111 = None
O0o0oO = None
i1i1o0oOoOo0 = None
ii1I1i1I = OOoO00o
O0o0oO = None
i1iii1IiiiI1i1 = None
Ii1I1i = None
if 37 - 37: IIiIiII11i - O00ooooo00 - ooO + iiI1i1 . IIii1I
try :
 O00O0oOO00O00 = urllib . unquote_plus ( O00O00OoO [ "url" ] ) . decode ( 'utf-8' )
except :
 pass
try :
 Oo0OoO00oOO0o = urllib . unquote_plus ( O00O00OoO [ "name" ] )
except :
 pass
try :
 i1i1o0oOoOo0 = urllib . unquote_plus ( O00O00OoO [ "iconimage" ] )
except :
 pass
try :
 ii1I1i1I = urllib . unquote_plus ( O00O00OoO [ "fanart" ] )
except :
 pass
try :
 iiIIIIiI111 = int ( O00O00OoO [ "mode" ] )
except :
 pass
try :
 O0o0oO = eval ( urllib . unquote_plus ( O00O00OoO [ "playlist" ] ) . replace ( '||' , ',' ) )
except :
 pass
try :
 i1iii1IiiiI1i1 = int ( O00O00OoO [ "fav_mode" ] )
except :
 pass
try :
 Ii1I1i = O00O00OoO [ "regexs" ]
except :
 pass
Oo00oOO00 = ''
try :
 Oo00oOO00 = urllib . unquote_plus ( O00O00OoO [ "playitem" ] )
except :
 pass
 if 21 - 21: II1 . ooOoO - ooO * iIi1IIii11I * ooO
IIiI ( "Mode: " + str ( iiIIIIiI111 ) )
if 45 - 45: OOO0O0O0ooooo * II11i + i11iIiiIii - Ii11111i - IIii1I
if 5 - 5: Ii11111i % IIiIiII11i % ooO % iIi1IIii11I
if not O00O0oOO00O00 is None :
 IIiI ( "URL: " + str ( O00O0oOO00O00 . encode ( 'utf-8' ) ) )
IIiI ( "Name: " + str ( Oo0OoO00oOO0o ) )
if 17 - 17: oO0oIIII + ooOoO + II1 / Ii11111i / ooO
if not Oo00oOO00 == '' :
 IiiIiI = ii11i1 ( '' , data = Oo00oOO00 )
 Oo0OoO00oOO0o , O00O0oOO00O00 , Ii1I1i = iI1Iii ( IiiIiI , None , dontLink = True )
 iiIIIIiI111 = 117
 if 80 - 80: OOooOOo % O00ooooo00 / iiI1i1
if iiIIIIiI111 == None :
 IIiI ( "getSources" )
 o0o00o0 ( )
 xbmcplugin . endOfDirectory ( int ( sys . argv [ 1 ] ) )
 if 56 - 56: O00ooooo00 . i11iIiiIii
elif iiIIIIiI111 == 1 :
 IIiI ( "getData" )
 i11I1 = None
 if Ii1I1i :
  i11I1 = i1II1I1Iii1 ( Ii1I1i , O00O0oOO00O00 )
  O00O0oOO00O00 = ''
  if 15 - 15: ooOoO * Ii1I % OOo00O0Oo0oO / i11iIiiIii - Ii1I + IIiIiII11i
 OoOo ( O00O0oOO00O00 , ii1I1i1I , i11I1 )
 xbmcplugin . endOfDirectory ( int ( sys . argv [ 1 ] ) )
 if 9 - 9: iiI1i1 - Ii1I + OOO0O0O0ooooo / OOo00O0Oo0oO % O00ooooo00
elif iiIIIIiI111 == 2 :
 IIiI ( "getChannelItems" )
 Ii1I1Ii ( Oo0OoO00oOO0o , O00O0oOO00O00 , ii1I1i1I )
 xbmcplugin . endOfDirectory ( int ( sys . argv [ 1 ] ) )
 if 97 - 97: OOooOOo * iIi1IIii11I
elif iiIIIIiI111 == 3 :
 IIiI ( "getSubChannelItems" )
 oO00oooOOoOo0 ( Oo0OoO00oOO0o , O00O0oOO00O00 , ii1I1i1I )
 xbmcplugin . endOfDirectory ( int ( sys . argv [ 1 ] ) )
 if 78 - 78: iiI1i1 . Ii11111i + Ii1I * OOo00O0Oo0oO - O00ooooo00
elif iiIIIIiI111 == 4 :
 IIiI ( "getFavorites" )
 O0OooOO ( )
 xbmcplugin . endOfDirectory ( int ( sys . argv [ 1 ] ) )
 if 27 - 27: oO0oIIII % O00ooooo00 . IIiIiII11i % II11i
elif iiIIIIiI111 == 5 :
 IIiI ( "addFavorite" )
 try :
  Oo0OoO00oOO0o = Oo0OoO00oOO0o . split ( '\\ ' ) [ 1 ]
 except :
  pass
 try :
  Oo0OoO00oOO0o = Oo0OoO00oOO0o . split ( '  - ' ) [ 0 ]
 except :
  pass
 oO0o0Oo ( Oo0OoO00oOO0o , O00O0oOO00O00 , i1i1o0oOoOo0 , ii1I1i1I , i1iii1IiiiI1i1 )
 if 10 - 10: ooO / II1
elif iiIIIIiI111 == 6 :
 IIiI ( "rmFavorite" )
 try :
  Oo0OoO00oOO0o = Oo0OoO00oOO0o . split ( '\\ ' ) [ 1 ]
 except :
  pass
 try :
  Oo0OoO00oOO0o = Oo0OoO00oOO0o . split ( '  - ' ) [ 0 ]
 except :
  pass
 OO00Oo00oO ( Oo0OoO00oOO0o )
 if 50 - 50: i11iIiiIii - II1 . Ii1I + OOO0O0O0ooooo . O00ooooo00
elif iiIIIIiI111 == 7 :
 SportsDevil ( )
 Dutch ( )
 if 91 - 91: OOooOOo . OOo00O0Oo0oO % IIiIiII11i - OOo00O0Oo0oO . Ii1I % i11iIiiIii
elif iiIIIIiI111 == 8 :
 IIiI ( "rmSource" )
 oO000Oo000 ( Oo0OoO00oOO0o )
 if 25 - 25: IIii1I
elif iiIIIIiI111 == 9 :
 IIiI ( "download_file" )
 Iii11111iiI ( Oo0OoO00oOO0o , O00O0oOO00O00 )
 if 63 - 63: iIi1IIii11I
elif iiIIIIiI111 == 10 :
 IIiI ( "getCommunitySources" )
 O0o0O00Oo0o0 ( )
 if 96 - 96: iiI1i1
elif iiIIIIiI111 == 11 :
 IIiI ( "addSource" )
 O0OOO00oo ( O00O0oOO00O00 )
 if 34 - 34: oO0o / o0oOOo0O0Ooo - iIiiiI1IiI1I1 . OOO0O0O0ooooo . Ii11111i
elif iiIIIIiI111 == 12 :
 IIiI ( "setResolvedUrl" )
 if not O00O0oOO00O00 . startswith ( "plugin://plugin" ) or not any ( x in O00O0oOO00O00 for x in IiII ) :
  Ii11iIII = True
  if '$$LSDirect$$' in O00O0oOO00O00 :
   O00O0oOO00O00 = O00O0oOO00O00 . replace ( '$$LSDirect$$' , '' )
   Ii11iIII = False
  OO0O0 = xbmcgui . ListItem ( path = O00O0oOO00O00 )
  if not Ii11iIII :
   xbmc . Player ( ) . play ( O00O0oOO00O00 )
  else :
   xbmcplugin . setResolvedUrl ( int ( sys . argv [ 1 ] ) , True , OO0O0 )
 else :
  if 63 - 63: OOo00O0Oo0oO
  xbmc . executebuiltin ( 'XBMC.RunPlugin(' + O00O0oOO00O00 + ')' )
  if 11 - 11: OOo00O0Oo0oO - IIii1I
elif iiIIIIiI111 == 13 :
 IIiI ( "play_playlist" )
 OooooOo ( Oo0OoO00oOO0o , O0o0oO )
 if 92 - 92: o0oOOo0O0Ooo
elif iiIIIIiI111 == 14 :
 IIiI ( "get_xml_database" )
 i1 ( O00O0oOO00O00 )
 xbmcplugin . endOfDirectory ( int ( sys . argv [ 1 ] ) )
 if 15 - 15: ooO / ooO + IIii1I % II1
elif iiIIIIiI111 == 15 :
 IIiI ( "browse_xml_database" )
 i1 ( O00O0oOO00O00 , True )
 xbmcplugin . endOfDirectory ( int ( sys . argv [ 1 ] ) )
 if 12 - 12: iIi1IIii11I
elif iiIIIIiI111 == 16 :
 IIiI ( "browse_community" )
 O0o0O00Oo0o0 ( O00O0oOO00O00 , browse = True )
 xbmcplugin . endOfDirectory ( int ( sys . argv [ 1 ] ) )
 if 36 - 36: II11i . ooO * II1 - OOooOOo
elif iiIIIIiI111 == 17 or iiIIIIiI111 == 117 :
 IIiI ( "getRegexParsed" )
 if 60 - 60: Ii11111i . OOo00O0Oo0oO / IIii1I + Ii11111i * II11i
 i11I1 = None
 if Ii1I1i and 'listrepeat' in urllib . unquote_plus ( Ii1I1i ) :
  i11i11 , OoOoO00O0 , I1ii11 , Ii1I1i = i1II1I1Iii1 ( Ii1I1i , O00O0oOO00O00 )
  if 82 - 82: i11iIiiIii . IIii1I * iIiiiI1IiI1I1 - iiI1i1 + oO0oIIII
  O0OO = ''
  if 48 - 48: I11i
  if 96 - 96: iIi1IIii11I . II1
  i1I1I1I = I1ii11 [ 'name' ]
  iII1III = Ii1I1i . pop ( i1I1I1I )
  if 58 - 58: iiI1i1 % i11iIiiIii / i11iIiiIii * iIi1IIii11I - II11i
  O00O0oOO00O00 = ''
  import copy
  i11ii111i1ii = ''
  Oo0O0O = 0
  for IiIiiI1ii111 in OoOoO00O0 :
   try :
    Oo0O0O += 1
    i11ii1 = copy . deepcopy ( Ii1I1i )
    if 4 - 4: i11iIiiIii - Ii11111i % I11i * II11i % OOooOOo
    o0OoOoo = i11i11
    oo0oooooO0 = 0
    for oo0oooooO0 in range ( len ( IiIiiI1ii111 ) ) :
     if 75 - 75: OOo00O0Oo0oO * iIiiiI1IiI1I1 + OOo00O0Oo0oO - II1
     if len ( i11ii1 ) > 0 :
      for OooO , oOoO0 in i11ii1 . iteritems ( ) :
       if oOoO0 is not None :
        for Iii1II1ii , ooOo00 in oOoO0 . iteritems ( ) :
         if ooOo00 is not None :
          if 98 - 98: o0oOOo0O0Ooo . IIii1I % II1 % IIiIiII11i - I11i
          if 86 - 86: oO0o . ooO
          if 10 - 10: OOo00O0Oo0oO * oO0oIIII - iIi1IIii11I . iiI1i1 - Ii11111i
          if 94 - 94: iIiiiI1IiI1I1 % ooO + o0oOOo0O0Ooo
          if type ( ooOo00 ) is dict :
           for OoOooO , I1I in ooOo00 . iteritems ( ) :
            if I1I is not None :
             Ii = None
             if isinstance ( IiIiiI1ii111 , tuple ) :
              try :
               Ii = IiIiiI1ii111 [ oo0oooooO0 ] . decode ( 'utf-8' )
              except :
               Ii = IiIiiI1ii111 [ oo0oooooO0 ]
             else :
              try :
               Ii = IiIiiI1ii111 . decode ( 'utf-8' )
              except :
               Ii = IiIiiI1ii111
               if 97 - 97: OOO0O0O0ooooo . II11i / ooOoO . OOO0O0O0ooooo + II1
             if '[' + i1I1I1I + '.param' + str ( oo0oooooO0 + 1 ) + '][DE]' in I1I :
              I1I = I1I . replace ( '[' + i1I1I1I + '.param' + str ( oo0oooooO0 + 1 ) + '][DE]' , unescape ( Ii ) )
             ooOo00 [ OoOooO ] = I1I . replace ( '[' + i1I1I1I + '.param' + str ( oo0oooooO0 + 1 ) + ']' , Ii )
             if 78 - 78: ooOoO + ooO
             if 66 - 66: IIii1I
          else :
           Ii = None
           if isinstance ( IiIiiI1ii111 , tuple ) :
            try :
             Ii = IiIiiI1ii111 [ oo0oooooO0 ] . decode ( 'utf-8' )
            except :
             Ii = IiIiiI1ii111 [ oo0oooooO0 ]
           else :
            try :
             Ii = IiIiiI1ii111 . decode ( 'utf-8' )
            except :
             Ii = IiIiiI1ii111
           if '[' + i1I1I1I + '.param' + str ( oo0oooooO0 + 1 ) + '][DE]' in ooOo00 :
            if 57 - 57: ooO
            ooOo00 = ooOo00 . replace ( '[' + i1I1I1I + '.param' + str ( oo0oooooO0 + 1 ) + '][DE]' , unescape ( Ii ) )
            if 41 - 41: IIii1I * OOo00O0Oo0oO + IIiIiII11i * OOooOOo % ooO / Ii11111i
           oOoO0 [ Iii1II1ii ] = ooOo00 . replace ( '[' + i1I1I1I + '.param' + str ( oo0oooooO0 + 1 ) + ']' , Ii )
           if 63 - 63: O00ooooo00 % i11iIiiIii % ooOoO * II1
           if 40 - 40: IIiIiII11i
     Ii = None
     if isinstance ( IiIiiI1ii111 , tuple ) :
      try :
       Ii = IiIiiI1ii111 [ oo0oooooO0 ] . decode ( 'utf-8' )
      except :
       Ii = IiIiiI1ii111 [ oo0oooooO0 ]
     else :
      try :
       Ii = IiIiiI1ii111 . decode ( 'utf-8' )
      except :
       Ii = IiIiiI1ii111
     if '[' + i1I1I1I + '.param' + str ( oo0oooooO0 + 1 ) + '][DE]' in o0OoOoo :
      o0OoOoo = o0OoOoo . replace ( '[' + i1I1I1I + '.param' + str ( oo0oooooO0 + 1 ) + '][DE]' , Ii )
     o0OoOoo = o0OoOoo . replace ( '[' + i1I1I1I + '.param' + str ( oo0oooooO0 + 1 ) + ']' , escape ( Ii ) )
     if 47 - 47: oO0o
    o0OoOoo = o0OoOoo . replace ( '[' + i1I1I1I + '.param' + str ( 0 ) + ']' , str ( Oo0O0O ) )
    if 65 - 65: OOO0O0O0ooooo + II11i % oO0oIIII * iIiiiI1IiI1I1 / iIi1IIii11I / oO0o
    if 71 - 71: i11iIiiIii / oO0o . Ii1I
    if 33 - 33: Ii1I
    if 39 - 39: o0oOOo0O0Ooo + OOO0O0O0ooooo + iIi1IIii11I * ooOoO % OOO0O0O0ooooo - OOO0O0O0ooooo
    i1I1i1i1I1 = ''
    if 17 - 17: oO0o + II1 % Ii11111i
    if len ( i11ii1 ) > 0 :
     i1I1i1i1I1 = I1iI1i11IiI11 ( i11ii1 , 'lsproroot' )
     i1I1i1i1I1 = i1I1i1i1I1 . split ( '<lsproroot>' ) [ 1 ] . split ( '</lsproroot' ) [ 0 ]
     if 36 - 36: i11iIiiIii + I11i % Ii11111i . iIiiiI1IiI1I1 - iIi1IIii11I
     if 94 - 94: iIiiiI1IiI1I1 % oO0o . ooO . iIi1IIii11I . o0oOOo0O0Ooo
    try :
     i11ii111i1ii += '\n<item>%s\n%s</item>' % ( o0OoOoo , i1I1i1i1I1 )
    except : i11ii111i1ii += '\n<item>%s\n%s</item>' % ( o0OoOoo . encode ( "utf-8" ) , i1I1i1i1I1 )
   except : traceback . print_exc ( file = sys . stdout )
   if 53 - 53: oO0o
   if 84 - 84: o0oOOo0O0Ooo
   if 97 - 97: O00ooooo00
   if 98 - 98: II1 - iIiiiI1IiI1I1 + iIi1IIii11I
   if 98 - 98: OOo00O0Oo0oO . ooO . ooO - Ii11111i
  IIiI ( repr ( i11ii111i1ii ) )
  OoOo ( '' , '' , i11ii111i1ii )
  xbmcplugin . endOfDirectory ( int ( sys . argv [ 1 ] ) )
 else :
  O00O0oOO00O00 , iIi1i = i1II1I1Iii1 ( Ii1I1i , O00O0oOO00O00 )
  if 65 - 65: IIiIiII11i + OOooOOo - oO0oIIII
  if O00O0oOO00O00 :
   if '$PLAYERPROXY$=' in O00O0oOO00O00 :
    O00O0oOO00O00 , Ooooooo = O00O0oOO00O00 . split ( '$PLAYERPROXY$=' )
    print 'proxy' , Ooooooo
    if 12 - 12: II1 + I11i
    o0OoO0000oOO = None
    i1iIIiiIiII = None
    if len ( Ooooooo ) > 0 and '@' in Ooooooo :
     Ooooooo = Ooooooo . split ( ':' )
     o0OoO0000oOO = Ooooooo [ 0 ]
     i1iIIiiIiII = Ooooooo [ 1 ] . split ( '@' ) [ 0 ]
     i11I1iIii1i11 = Ooooooo [ 1 ] . split ( '@' ) [ 1 ]
     iIiiI11II11i = Ooooooo [ 2 ]
    else :
     i11I1iIii1i11 , iIiiI11II11i = Ooooooo . split ( ':' )
     if 98 - 98: OOo00O0Oo0oO - OOo00O0Oo0oO
    Oo0O ( O00O0oOO00O00 , Oo0OoO00oOO0o , i1i1o0oOoOo0 , i11I1iIii1i11 , iIiiI11II11i , o0OoO0000oOO , i1iIIiiIiII )
   else :
    IiiI1I ( O00O0oOO00O00 , Oo0OoO00oOO0o , i1i1o0oOoOo0 , iIi1i )
  else :
   xbmc . executebuiltin ( "XBMC.Notification(Evilsport,Failed to extract regex. - " + "this" + ",4000," + OOooO + ")" )
   if 58 - 58: Ii1I
elif iiIIIIiI111 == 18 :
 IIiI ( "youtubedl" )
 try :
  import youtubedl
 except Exception :
  xbmc . executebuiltin ( "XBMC.Notification(Evilsport,Please [COLOR yellow]install Youtube-dl[/COLOR] module ,10000," ")" )
 ii = youtubedl . single_YD ( O00O0oOO00O00 )
 IiiI1I ( ii , Oo0OoO00oOO0o , i1i1o0oOoOo0 )
 if 98 - 98: OOooOOo * o0oOOo0O0Ooo
elif iiIIIIiI111 == 19 :
 IIiI ( "Genesiscommonresolvers" )
 IiiI1I ( o0O0 ( O00O0oOO00O00 ) , Oo0OoO00oOO0o , i1i1o0oOoOo0 , True )
 if 10 - 10: Ii1I - OOo00O0Oo0oO % ooOoO - II11i - O00ooooo00
elif iiIIIIiI111 == 21 :
 IIiI ( "download current file using youtube-dl service" )
 oOoo ( '' , Oo0OoO00oOO0o , 'video' )
 if 10 - 10: I11i - iiI1i1 . II11i
elif iiIIIIiI111 == 23 :
 IIiI ( "get info then download" )
 oOoo ( O00O0oOO00O00 , Oo0OoO00oOO0o , 'video' )
 if 8 - 8: IIii1I % Ii1I + IIiIiII11i
elif iiIIIIiI111 == 24 :
 IIiI ( "Audio only youtube download" )
 oOoo ( O00O0oOO00O00 , Oo0OoO00oOO0o , 'audio' )
 if 24 - 24: OOooOOo / oO0oIIII / oO0oIIII % ooOoO - Ii1I * Ii1I
elif iiIIIIiI111 == 25 :
 IIiI ( "Searchin Other plugins" )
 i1Iiii ( O00O0oOO00O00 , Oo0OoO00oOO0o )
 xbmcplugin . endOfDirectory ( int ( sys . argv [ 1 ] ) )
 if 58 - 58: oO0o
elif iiIIIIiI111 == 55 :
 IIiI ( "enabled lock" )
 iIIi1 = O0 . getSetting ( 'parentalblockedpin' )
 o0O = xbmc . Keyboard ( '' , 'Enter Pin' )
 o0O . doModal ( )
 if not ( o0O . isConfirmed ( ) == False ) :
  O00oO = o0O . getText ( )
  if O00oO == iIIi1 :
   O0 . setSetting ( 'parentalblocked' , "false" )
   xbmc . executebuiltin ( "XBMC.Notification(Evilsport,Parental Block Disabled,5000," + OOooO + ")" )
  else :
   xbmc . executebuiltin ( "XBMC.Notification(Evilsport,Wrong Pin??,5000," + OOooO + ")" )
 xbmcplugin . endOfDirectory ( int ( sys . argv [ 1 ] ) )
 if 60 - 60: ooOoO
elif iiIIIIiI111 == 56 :
 IIiI ( "disable lock" )
 O0 . setSetting ( 'parentalblocked' , "true" )
 xbmc . executebuiltin ( "XBMC.Notification(Evilsport,Parental block enabled,5000," + OOooO + ")" )
 xbmcplugin . endOfDirectory ( int ( sys . argv [ 1 ] ) )
 if 90 - 90: oO0o
elif iiIIIIiI111 == 53 :
 IIiI ( "Requesting JSON-RPC Items" )
 Ii11iiI ( O00O0oOO00O00 )
 if 37 - 37: oO0o + OOO0O0O0ooooo . OOO0O0O0ooooo * IIiIiII11i % II11i / OOo00O0Oo0oO
 if 18 - 18: II1
if not Oo0Ooo == None :
 print 'setting view mode'
 xbmc . executebuiltin ( "Container.SetViewMode(%s)" % Oo0Ooo )
 if 57 - 57: iIi1IIii11I . oO0o * OOooOOo - II1
# dd678faae9ac167bc83abf78e5cb2f3f0688d3a3
