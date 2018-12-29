#V 3.0.0
import xbmc , xbmcaddon , xbmcgui , xbmcplugin , requests , urllib , urllib2 , json , os , re , sys , datetime , urlresolver , random , liveresolver , base64
import requests
import downloader as Get_Files
import extract
import time
if 64 - 64: i11iIiiIii
VVeve = 'plugin.video.TheJukeBox'
VeevVee = xbmcaddon . Addon ( id = VVeve )
VevVevVVevVevVev = xbmcaddon . Addon ( ) . getAddonInfo
iiiii = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + VVeve , 'fanart.png' ) )
eeeevVV = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + VVeve , 'fanart.png' ) )
II1 = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + VVeve , 'icon.png' ) )
Veveveeeeeevev = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + VVeve + '/resources/art' , 'next.png' ) )
I1IiiI = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + VVeve + '/resources' , 'rd.txt' ) )
IIi1IiiiI1Ii = 'http://matsbuilds.uk/pin'
I11i11Ii = xbmcaddon . Addon ( ) . getSetting ( 'enable_meta' )
eVeveveVe = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.89 Safari/537.36'
VVVeev = base64 . b64decode ( 'aHR0cDovL21hdHNidWlsZHMudWsvanVrZWJveGluZm8vaW5mby50eHQ=' )
Veeeeveveve = xbmc . translatePath ( 'special://home/userdata/addon_data/' + VVeve )
IiIi11iIIi1Ii = xbmc . translatePath ( os . path . join ( 'special://home/userdata/Database' , 'jukebox.db' ) )
VeevV = xbmc . translatePath ( os . path . join ( 'special://home/addons' , 'repository.Goliath' ) )
IiI = '[B][COLOR red]T[/COLOR][COLOR white]he[/COLOR] [COLOR red]J[/COLOR][COLOR white]ukeBox[/COLOR][/B]'
eeVe = xbmc . translatePath ( os . path . join ( 'special://home/addons/' + VVeve , 'search.jpg' ) )
Ve = open ( IiIi11iIIi1Ii , 'a' )
Ve . close ( )
if 67 - 67: VeveveeVV . I1iII1iiII
if 28 - 28: Ii11111i * iiI1i1
if not os . path . exists ( VeevV ) :
 i1I1ii1II1iII = xbmcgui . Dialog ( ) . yesno ( IiI , 'This Add-on requires [COLOR red]Goliaths Repo[/COLOR] to be installed to work correctly would you like to install it now?' , '' , yeslabel = '[B][COLOR white]YES[/COLOR][/B]' , nolabel = '[B][COLOR grey]NO[/COLOR][/B]' )
 if i1I1ii1II1iII == 1 :
  eeeVeveeeveVVVV = xbmc . translatePath ( os . path . join ( 'special://home/addons' , 'packages' ) )
  if not os . path . exists ( eeeVeveeeveVVVV ) :
   os . makedirs ( eeeVeveeeveVVVV )
  VeveV = base64 . b64decode ( b'aHR0cDovL21hdHNidWlsZHMudWsvcmVwby9yZXBvc2l0b3J5LkdvbGlhdGgtMi4wLjAuemlw' )
  eeveVev = xbmcgui . DialogProgress ( )
  eeveVev . create ( IiI , "" , "" , "Downloading [COLOR red]Goliaths Repo[/COLOR]" )
  eeevev = os . path . join ( eeeVeveeeveVVVV , 'repo.zip' )
  if 88 - 88: VevVeeveVeve . II1iI . i1iIii1Ii1II
  try :
   os . remove ( eeevev )
  except :
   pass
   if 1 - 1: VevVeeeevev
  Get_Files . download ( VeveV , eeevev , eeveVev )
  Veeev = xbmc . translatePath ( os . path . join ( 'special://home' , 'addons' ) )
  time . sleep ( 2 )
  eeveVev . update ( 0 , "" , "Installing [COLOR red]Golitaths Repo[/COLOR] Please Wait" , "" )
  extract . all ( eeevev , Veeev , eeveVev )
  xbmc . executebuiltin ( "UpdateAddonRepos" )
  xbmc . executebuiltin ( "UpdateLocalAddons" )
  if 89 - 89: I111i1i1111i - Ii1Ii1iiii11 % I1I1i1
  if 18 - 18: iiIIIIi1i1 / VVeVeeevevee - iI1 + VVeeV % eeVevevee - Vevevevee
  if 3 - 3: eVeevVe + eeveVeevVeeevV
  if 81 - 81: I1I1i1 * Vevevevee * iI1 - eeVevevee - Ii1Ii1iiii11
def VeeVevVV ( ) :
 if not os . path . exists ( Veeeeveveve ) :
  os . mkdir ( Veeeeveveve )
 iiiIi ( VVVeev , 'GlobalCompare' )
 IiIIIiI1I1 = VeVevevev ( IIiiIiI1 )
 iiIiIIi = re . compile ( '<item>(.+?)</item>' ) . findall ( IiIIIiI1I1 )
 for eeVeeevV in iiIiIIi :
  VeeVev = re . compile ( '<title>(.+?)</title>.+?folder>(.+?)</folder>.+?thumbnail>(.+?)</thumbnail>.+?fanart>(.+?)</fanart>' ) . findall ( eeVeeevV )
  for II11iiii1Ii , VeveV , VVeveVee , iiiii in VeeVev :
   VeveevVe ( II11iiii1Ii , VeveV , 1 , VVeveVee , iiiii )
 VeveevVe ( '[B][COLOR red]S[/COLOR][COLOR white]earch[/COLOR][/B] [B][COLOR red]J[/COLOR][COLOR white]ukeBox[/COLOR][/B]' , VeveV , 5 , eeVe , eeeevVV )
 xbmc . executebuiltin ( 'Container.SetViewMode(500)' )
 if 78 - 78: I1iII1iiII - VVeeV * VevVeeeevev + Ii1Ii1iiii11 + eeVevevee + eeVevevee
def I11I11i1I ( name , url , iconimage , fanart ) :
 ii11i1iIII = Ii1I ( name )
 VeevVee . setSetting ( 'tv' , ii11i1iIII )
 IiIIIiI1I1 = VeVevevev ( url )
 Veeveev ( IiIIIiI1I1 )
 if '<message>' in IiIIIiI1I1 :
  VVVeev = re . compile ( '<message>(.+?)</message>' ) . findall ( IiIIIiI1I1 ) [ 0 ]
  iiiIi ( VVVeev , ii11i1iIII )
 if '<intro>' in IiIIIiI1I1 :
  III1ii1iII = re . compile ( '<intro>(.+?)</intro>' ) . findall ( IiIIIiI1I1 ) [ 0 ]
  eeeveeeeeVev ( III1ii1iII )
 if 'XXX>yes</XXX' in IiIIIiI1I1 : ADULT_CHECK ( IiIIIiI1I1 )
 iiIiIIi = re . compile ( '<item>(.+?)</item>' ) . findall ( IiIIIiI1I1 )
 for eeVeeevV in iiIiIIi :
  i11Iiii ( name , url , iconimage , fanart , eeVeeevV )
  if 23 - 23: Ii1Ii1iiii11 . VevVeeveVeve
def i11Iiii ( name , url , iconimage , fanart , item ) :
 try :
  if '<folder>' in item : VeevVevVVVee ( name , url , iconimage , fanart , item )
  else : eVeVeeVeeveev ( name , url , iconimage , fanart , item )
 except : pass
 if 61 - 61: Ii1Ii1iiii11 / VevVeeeevev + eeveVeevVeeevV * iiIIIIi1i1 / iiIIIIi1i1
 if 75 - 75: iiI1i1 / Ii11111i - VeveveeVV / I111i1i1111i . VevVeeveVeve - iiI1i1
 if 71 - 71: VVeVeeevevee + VVeeV * VVeVeeevevee - VevVeeeevev * Ii1Ii1iiii11
def eVeVeeVeeveev ( name , url , iconimage , fanart , item ) :
 I1IiiI = ''
 VeeeevVeeevevev = re . compile ( '<link>(.+?)</link>' ) . findall ( item )
 VeeVev = re . compile ( '<title>(.+?)</title>.+?link>(.+?)</link>.+?thumbnail>(.+?)</thumbnail>.+?fanart>(.+?)</fanart>' ) . findall ( item )
 for name , ee , iconimage , fanart in VeeVev :
  if 'youtube.com/playlist?' in ee :
   ii11I = ee . split ( 'list=' ) [ 1 ]
   VeveevVe ( name , ee , VeeevVVeveVV , iconimage , fanart , description = ii11I )
 if len ( VeeeevVeeevevev ) == 1 :
  VeeVev = re . compile ( '<title>(.+?)</title>.+?link>(.+?)</link>.+?thumbnail>(.+?)</thumbnail>.+?fanart>(.+?)</fanart>' ) . findall ( item )
  for name , url , iconimage , fanart in VeeVev :
   try :
    I1IiiI = RDCHECK ( url )
    ii11i1 = url . split ( '/' ) [ 2 ] . replace ( 'www.' , '' )
    if 'SportsDevil' in url : ii11i1 = ''
   except : pass
   if '.ts' in url : IIIii1II1II ( name , url , 16 , iconimage , fanart , description = '' )
   if '<meta>' in item :
    i1I1iI = re . compile ( '<meta>(.+?)</meta>' ) . findall ( item ) [ 0 ]
    eeevVeeVVeev ( name + I1IiiI , url , 2 , iconimage , 10 , i1I1iI , isFolder = False )
   else :
    IIIii1II1II ( name + I1IiiI , url , 2 , iconimage , fanart )
 elif len ( VeeeevVeeevevev ) > 1 :
  name = re . compile ( '<title>(.+?)</title>' ) . findall ( item ) [ 0 ]
  iconimage = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( item ) [ 0 ]
  fanart = re . compile ( '<fanart>(.+?)</fanart>' ) . findall ( item ) [ 0 ]
  if '.ts' in url : IIIii1II1II ( name , url , 16 , iconimage , fanart , description = '' )
  if '<meta>' in item :
   i1I1iI = re . compile ( '<meta>(.+?)</meta>' ) . findall ( item ) [ 0 ]
   eeevVeeVVeev ( name , url , 3 , iconimage , len ( VeeeevVeeevevev ) , i1I1iI , isFolder = True )
  else :
   VeveevVe ( name , url , 3 , iconimage , fanart )
   if 92 - 92: eeVevevee . iI1 + Ii1Ii1iiii11
   if 28 - 28: iiI1i1 * i1iIii1Ii1II - Ii1Ii1iiii11 * Vevevevee * VVeeV / VevVeeeevev
def VeeVevVeVVVV ( name , url , iconimage ) :
 i1Ii = ''
 ii11i1iIII = Ii1I ( name )
 VeevVee . setSetting ( 'tv' , ii11i1iIII )
 IiIIIiI1I1 = VeVevevev ( url )
 eevevVVevevVeV = re . compile ( '<title>.*?' + re . escape ( name ) + '.*?</title>(.+?)</item>' , re . DOTALL ) . findall ( IiIIIiI1I1 ) [ 0 ]
 iconimage = re . compile ( '<thumbnail>(.+?)</thumbnail>' ) . findall ( eevevVVevevVeV ) [ 0 ]
 VeeeevVeeevevev = [ ]
 if '<link>' in eevevVVevevVeV :
  VVVVevVVeVevVev = re . compile ( '<link>(.+?)</link>' ) . findall ( eevevVVevevVeV )
  for VevVeeveveveeVevev in VVVVevVVeVevVev :
   VeeeevVeeevevev . append ( VevVeeveveveeVevev )
 if '<sportsdevil>' in eevevVVevevVeV :
  eVev = re . compile ( '<sportsdevil>(.+?)</sportsdevil>' ) . findall ( eevevVVevevVeV )
  for Ii1iIiII1ii1 in eVev :
   Ii1iIiII1ii1 = 'plugin://plugin.video.SportsDevil/?mode=1&amp;item=catcher%3dstreams%26url=' + Ii1iIiII1ii1
   VeeeevVeeevevev . append ( Ii1iIiII1ii1 )
 eeVeeeeveveveVV = 1
 for IiIIIiI1I1 in VeeeevVeeevevev :
  if '(' in IiIIIiI1I1 :
   IiIIIiI1I1 = IiIIIiI1I1 . split ( '(' )
   i1Ii = IiIIIiI1I1 [ 1 ] . replace ( ')' , '' )
   IiIIIiI1I1 = IiIIIiI1I1 [ 0 ]
  I1IiiI = RDCHECK ( IiIIIiI1I1 )
  ii11i1 = IiIIIiI1I1 . split ( '/' ) [ 2 ] . replace ( 'www.' , '' )
  if i1Ii <> '' : name = "Link " + str ( eeVeeeeveveveVV ) + ' | ' + i1Ii + I1IiiI
  else : name = "Link " + str ( eeVeeeeveveveVV ) + ' | ' + ii11i1 + I1IiiI
  eeVeeeeveveveVV = eeVeeeeveveveVV + 1
  eeevVeeVVeev ( name , IiIIIiI1I1 , 2 , iconimage , 10 , '' , isFolder = False , description = VeevVee . getSetting ( 'tv' ) )
  if 59 - 59: VevVeeveVeve + Ii11111i * I111i1i1111i + iiI1i1
def VeevVevVVVee ( name , url , iconimage , fanart , item ) :
 VeeVev = re . compile ( '<title>(.+?)</title>.+?folder>(.+?)</folder>.+?thumbnail>(.+?)</thumbnail>.+?fanart>(.+?)</fanart>' ) . findall ( item )
 for name , url , iconimage , fanart in VeeVev :
  if 'youtube.com/channel/' in url :
   ii11I = url . split ( 'channel/' ) [ 1 ]
   VeveevVe ( name , url , VeeevVVeveVV , iconimage , fanart , description = ii11I )
  elif 'youtube.com/user/' in url :
   ii11I = url . split ( 'user/' ) [ 1 ]
   VeveevVe ( name , url , VeeevVVeveVV , iconimage , fanart , description = ii11I )
  elif 'youtube.com/playlist?' in url :
   ii11I = url . split ( 'list=' ) [ 1 ]
   VeveevVe ( name , url , VeeevVVeveVV , iconimage , fanart , description = ii11I )
  elif 'plugin://' in url :
   VeevVeVeveveVVeve = HTMLParser ( )
   url = VeevVeVeveveVVeve . unescape ( url )
   VeveevVe ( name , url , VeeevVVeveVV , iconimage , fanart )
  else :
   VeveevVe ( name , url , 1 , iconimage , fanart )
   if 80 - 80: iiIIIIi1i1 + VVeVeeevevee - VVeVeeevevee % eeVevevee
def VeVVeveeeve ( ) :
 II11i1I11Ii1i = xbmc . Keyboard ( '' , '[B][COLOR red]Search[/COLOR][/B]' )
 II11i1I11Ii1i . doModal ( )
 if ( II11i1I11Ii1i . isConfirmed ( ) ) :
  ii11I = II11i1I11Ii1i . getText ( )
  ii11I = ii11I . upper ( )
 else : quit ( )
 IiIIIiI1I1 = VeVevevev ( 'http://matsbuilds.uk/Menus/anewEvolvemenu/search.xml' )
 VevevevVeveVVev = re . compile ( '<link>(.+?)</link>' ) . findall ( IiIIIiI1I1 )
 for VeveV in VevevevVeveVVev :
  try :
   IiIIIiI1I1 = VeVevevev ( VeveV )
   VeveeeevVeveeev = re . compile ( '<item>(.+?)</item>' ) . findall ( IiIIIiI1I1 )
   for eeVeeevV in VeveeeevVeveeev :
    iiIiIIi = re . compile ( '<title>(.+?)</title>' ) . findall ( eeVeeevV )
    for eeeveVe in iiIiIIi :
     eeeveVe = eeeveVe . upper ( )
     if ii11I in eeeveVe :
      i11Iiii ( II11iiii1Ii , VeveV , VVeveVee , iiiii , eeVeeevV )
  except : pass
  if 89 - 89: I111i1i1111i
def VVeveVeVVeveVVev ( url ) :
 eVevVVeeevVV = "ShowPicture(%s)" % url
 xbmc . executebuiltin ( eVevVVeeevVV )
 if 65 - 65: VVeeV . I1iII1iiII / VeveveeVV - VVeeV
def iii1i1iiiiIi ( name , url , iconimage , description ) :
 if description : name = description
 try :
  if 'plugin://plugin.video.SportsDevil/' in url :
   Iiii ( name , url , iconimage )
  elif '.ts' in url :
   url = 'plugin://plugin.video.f4mTester/?streamtype=TSDOWNLOADER&amp;name=' + name + '&amp;url=' + url
   url = url . replace ( '|' , '' )
   Iiii ( name , url , iconimage )
  elif urlresolver . HostedMediaFile ( url ) . valid_url ( ) :
   url = urlresolver . HostedMediaFile ( url ) . resolve ( )
   VVevVeVeveevev ( name , url , iconimage )
  elif liveresolver . isValid ( url ) == True :
   url = liveresolver . resolve ( url )
   VVevVeVeveevev ( name , url , iconimage )
  else : VVevVeVeveevev ( name , url , iconimage )
 except :
  eeVVevVeveeVeeV ( eVVVeevevVeveveVe ( 'The JukeBox' ) , 'Stream Unavailable' , '3000' , II1 )
  if 34 - 34: VeveveeVV + VVeVeeevevee + i1iIii1Ii1II
def eeeveeeeeVev ( url ) :
 if urlresolver . HostedMediaFile ( url ) . valid_url ( ) :
  url = urlresolver . HostedMediaFile ( url ) . resolve ( )
 xbmc . Player ( ) . play ( url )
 if 16 - 16: eeVevevee . VeveveeVV . eeVevevee % I1I1i1 - II1iI - I1iII1iiII
def VVevVeVeveevev ( name , url , iconimage ) :
 I111IIIiIii = True
 eVevevevevVVeevev = xbmcgui . ListItem ( name , iconImage = iconimage , thumbnailImage = iconimage ) ; eVevevevevVVeevev . setInfo ( type = "Video" , infoLabels = { "Title" : name } )
 I111IIIiIii = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = url , listitem = eVevevevevVVeevev )
 eVevevevevVVeevev . setPath ( url )
 xbmcplugin . setResolvedUrl ( int ( sys . argv [ 1 ] ) , True , eVevevevevVVeevev )
 if 27 - 27: II1iI % II1iI
def Iiii ( name , url , iconimage ) :
 xbmc . executebuiltin ( 'Dialog.Close(all,True)' )
 I111IIIiIii = True
 eVevevevevVVeevev = xbmcgui . ListItem ( name , iconImage = "DefaultFolder.png" , thumbnailImage = iconimage ) ; eVevevevevVVeevev . setInfo ( type = "Video" , infoLabels = { "Title" : name } )
 I111IIIiIii = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = url , listitem = eVevevevevVVeevev )
 xbmc . Player ( ) . play ( url , eVevevevevVVeevev , False )
 if 1 - 1: VevVeeeevev - iiIIIIi1i1 . iI1 . VevVeeeevev / i1iIii1Ii1II + iI1
def Vee ( url ) :
 xbmc . executebuiltin ( "PlayMedia(%s)" % url )
 if 62 - 62: VVeVeeevevee / VevVeeeevev + VVeeV / VevVeeeevev . VevVeeveVeve
def VeVevevev ( url ) :
 eeVVeeeeee = urllib2 . Request ( url )
 eeVVeeeeee . add_header ( base64 . b64decode ( 'VXNlci1BZ2VudA==' ) , base64 . b64decode ( 'dTM0ODczZWpyZGU4dTkyM2pxdzlkaXUy' ) )
 II1I = urllib2 . urlopen ( eeVVeeeeee )
 IiIIIiI1I1 = II1I . read ( )
 II1I . close ( )
 IiIIIiI1I1 = IiIIIiI1I1 . replace ( '<fanart></fanart>' , '<fanart>x</fanart>' ) . replace ( '<thumbnail></thumbnail>' , '<thumbnail>x</thumbnail>' ) . replace ( '<utube>' , '<link>https://www.youtube.com/watch?v=' ) . replace ( '</utube>' , '</link>' )
 if '{' in IiIIIiI1I1 :
  eVevVVeeevVV = IiIIIiI1I1 [ : : - 1 ]
  eVevVVeeevVV = eVevVVeeevVV . replace ( '}' , '' ) . replace ( '{' , '' ) . replace ( ',' , '' ) . replace ( ']' , '' ) . replace ( '[' , '' )
  eVevVVeeevVV = eVevVVeeevVV + '=='
  IiIIIiI1I1 = eVevVVeeevVV . decode ( 'base64' )
 if url <> VVVeev : IiIIIiI1I1 = IiIIIiI1I1 . replace ( '\n' , '' ) . replace ( '\r' , '' )
 print IiIIIiI1I1
 return IiIIIiI1I1
 if 84 - 84: Vevevevee . i11iIiiIii . Vevevevee * I1I1i1 - iI1
def ii ( url ) :
 eeVVeeeeee = urllib2 . Request ( url )
 eeVVeeeeee . add_header ( base64 . b64decode ( 'VXNlci1BZ2VudA==' ) , base64 . b64decode ( 'dTM0ODczZWpyZGU4dTkyM2pxdzlkaXUy' ) )
 II1I = urllib2 . urlopen ( eeVVeeeeee )
 IiIIIiI1I1 = II1I . read ( )
 II1I . close ( )
 return IiIIIiI1I1
 if 81 - 81: eVeevVe % eeVevevee . I1I1i1 / Ii1Ii1iiii11
def iiiIiI ( url ) :
 eeVVeeeeee = urllib2 . Request ( url )
 eeVVeeeeee . add_header ( 'User-Agent' , 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3' )
 II1I = urllib2 . urlopen ( eeVVeeeeee )
 IiIIIiI1I1 = II1I . read ( )
 II1I . close ( )
 IiIIIiI1I1 = IiIIIiI1I1 . replace ( '\n' , '' ) . replace ( '\r' , '' )
 return IiIIIiI1I1
 if 91 - 91: eeVevevee % iiI1i1 % I1iII1iiII
 if 20 - 20: VVeVeeevevee % VVeeV / VVeeV + VVeeV
def III1IiiI ( ) :
 iI = [ ]
 i1 = sys . argv [ 2 ]
 if len ( i1 ) >= 2 :
  IIIII11I1IiI = sys . argv [ 2 ]
  i1I = IIIII11I1IiI . replace ( '?' , '' )
  if ( IIIII11I1IiI [ len ( IIIII11I1IiI ) - 1 ] == '/' ) :
   IIIII11I1IiI = IIIII11I1IiI [ 0 : len ( IIIII11I1IiI ) - 2 ]
  VeVV = i1I . split ( '&' )
  iI = { }
  for eeVeeeeveveveVV in range ( len ( VeVV ) ) :
   eeVVVev = { }
   eeVVVev = VeVV [ eeVeeeeveveveVV ] . split ( '=' )
   if ( len ( eeVVVev ) ) == 2 :
    iI [ eeVVVev [ 0 ] ] = eeVVVev [ 1 ]
 return iI
 if 65 - 65: VeveveeVV
def eeVVevVeveeVeeV ( title , message , ms , nart ) :
 xbmc . executebuiltin ( "XBMC.notification(" + title + "," + message + "," + ms + "," + nart + ")" )
 if 68 - 68: VVeVeeevevee % eVeevVe
def Ii1I ( string ) :
 eeVevevVVev = re . compile ( '(\[.+?\])' ) . findall ( string )
 for i11111IIIII in eeVevevVVev : string = string . replace ( i11111IIIII , '' )
 return string
 if 19 - 19: I111i1i1111i * iiI1i1
def eVVVeevevVeveveVe ( string ) :
 string = string . split ( ' ' )
 ii111iI1iIi1 = ''
 for VVV in string :
  eeevVVeev = '[B][COLOR red]' + VVV [ 0 ] . upper ( ) + '[/COLOR][COLOR white]' + VVV [ 1 : ] + '[/COLOR][/B] '
  ii111iI1iIi1 = ii111iI1iIi1 + eeevVVeev
 return ii111iI1iIi1
 if 47 - 47: eVeevVe + I111i1i1111i * i1iIii1Ii1II / eeveVeevVeeevV - eeVevevee % I1iII1iiII
def eeevVeeVVeev ( name , url , mode , iconimage , itemcount , metatype , isFolder = False , description = '' ) :
 if isFolder == True : VeevVee . setSetting ( 'favtype' , 'folder' )
 else : VeevVee . setSetting ( 'favtype' , 'link' )
 if I11i11Ii == 'true' :
  IIi11i1i1iI1 = name
  name = Ii1I ( name )
  iiiIi1 = ""
  i1I1ii11i1Iii = ""
  I1IiiiiI = [ ]
  eevV = eval ( base64 . b64decode ( 'bWV0YWhhbmRsZXJzLk1ldGFEYXRhKHRtZGJfYXBpX2tleT0iZDk1NWQ4ZjAyYTNmMjQ4MGE1MTg4MWZlNGM5NmYxMGUiKQ==' ) )
  IiII = { }
  if metatype == 'movie' :
   ii1iII1II = name . partition ( '(' )
   if len ( ii1iII1II ) > 0 :
    iiiIi1 = ii1iII1II [ 0 ]
    i1I1ii11i1Iii = ii1iII1II [ 2 ] . partition ( ')' )
   if len ( i1I1ii11i1Iii ) > 0 :
    i1I1ii11i1Iii = i1I1ii11i1Iii [ 0 ]
   IiII = eevV . get_meta ( 'movie' , name = iiiIi1 , year = i1I1ii11i1Iii )
   if not IiII [ 'trailer' ] == '' : I1IiiiiI . append ( ( eVVVeevevVeveveVe ( 'Play Trailer' ) , 'XBMC.RunPlugin(%s)' % addon . build_plugin_url ( { 'mode' : 11 , 'url' : IiII [ 'trailer' ] } ) ) )
  elif metatype == 'tvep' :
   eeeveVe = VeevVee . getSetting ( 'tv' )
   if '<>' in url :
    print url
    Iii1I1I11iiI1 = url . split ( '<>' ) [ 0 ]
    I1I1i1I = url . split ( '<>' ) [ 1 ]
    ii1I = url . split ( '<>' ) [ 2 ]
    VeveVev = url . split ( '<>' ) [ 3 ]
    eVevVevVVevV = url . split ( '<>' ) [ 4 ]
    VV = url . split ( '<>' ) [ 5 ]
    IiII = eevV . get_episode_meta ( I1I1i1I , imdb_id = Iii1I1I11iiI1 , season = ii1I , episode = VeveVev , air_date = '' , episode_title = '' , overlay = '' )
   else :
    VeVeV = re . compile ( 'Season (.+?) Episode (.+?)\)' ) . findall ( name )
    for Ii1I1i , VVI1iI1ii1II in VeVeV :
     IiII = eevV . get_episode_meta ( eeeveVe , imdb_id = '' , season = Ii1I1i , episode = VVI1iI1ii1II , air_date = '' , episode_title = '' , overlay = '' )
  try :
   if IiII [ 'cover_url' ] == '' : iconimage = iconimage
   else : iconimage = IiII [ 'cover_url' ]
  except : pass
  VevVevVVVVee = sys . argv [ 0 ] + "?url=" + urllib . quote_plus ( url ) + "&mode=" + str ( mode ) + "&name=" + urllib . quote_plus ( name ) + "&description=" + str ( description ) + "&fanart=" + urllib . quote_plus ( iiiii ) + "&iconimage=" + urllib . quote_plus ( iconimage )
  I111IIIiIii = True
  eVevevevevVVeevev = xbmcgui . ListItem ( IIi11i1i1iI1 , iconImage = iconimage , thumbnailImage = iconimage )
  eVevevevevVVeevev . setInfo ( type = "Video" , infoLabels = IiII )
  eVevevevevVVeevev . setProperty ( "IsPlayable" , "true" )
  eVevevevevVVeevev . addContextMenuItems ( I1IiiiiI , replaceItems = False )
  if not IiII . get ( 'backdrop_url' , '' ) == '' : eVevevevevVVeevev . setProperty ( 'fanart_image' , IiII [ 'backdrop_url' ] )
  else : eVevevevevVVeevev . setProperty ( 'fanart_image' , iiiii )
  eVeeVev = VeevVee . getSetting ( 'favlist' )
  Ii1I1Ii = [ ]
  Ii1I1Ii . append ( ( eVVVeevevVeveveVe ( 'Stream Information' ) , 'XBMC.Action(Info)' ) )
  if eVeeVev == 'yes' : Ii1I1Ii . append ( ( '[COLOR red]Remove From Favs? [/COLOR]' , 'XBMC.RunPlugin(%s?mode=21&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
  else : Ii1I1Ii . append ( ( '[COLOR red]Add To Favs[/COLOR]' , 'XBMC.RunPlugin(%s?mode=20&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
  eVevevevevVVeevev . addContextMenuItems ( Ii1I1Ii , replaceItems = False )
  I111IIIiIii = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = VevVevVVVVee , listitem = eVevevevevVVeevev , isFolder = isFolder , totalItems = itemcount )
  return I111IIIiIii
 else :
  if isFolder :
   VeveevVe ( name , url , mode , iconimage , iiiii , description = '' )
  else :
   IIIii1II1II ( name , url , mode , iconimage , iiiii , description = '' )
   if 69 - 69: II1iI / Ii1Ii1iiii11 . Vevevevee * eVeevVe % VVeeV - Ii1Ii1iiii11
def VeveevVe ( name , url , mode , iconimage , fanart , description = '' ) :
 VeevVee . setSetting ( 'favtype' , 'folder' )
 VevVevVVVVee = sys . argv [ 0 ] + "?url=" + urllib . quote_plus ( url ) + "&mode=" + str ( mode ) + "&name=" + urllib . quote_plus ( name ) + "&description=" + str ( description ) + "&fanart=" + urllib . quote_plus ( fanart ) + "&iconimage=" + urllib . quote_plus ( iconimage )
 I111IIIiIii = True
 eVevevevevVVeevev = xbmcgui . ListItem ( name , iconImage = "DefaultFolder.png" , thumbnailImage = iconimage )
 eVevevevevVVeevev . setInfo ( type = "Video" , infoLabels = { "Title" : name , 'plot' : description } )
 eVevevevevVVeevev . setProperty ( 'fanart_image' , fanart )
 if 'youtube.com/channel/' in url :
  VevVevVVVVee = 'plugin://plugin.video.youtube/channel/' + description + '/'
 if 'youtube.com/user/' in url :
  VevVevVVVVee = 'plugin://plugin.video.youtube/user/' + description + '/'
 if 'youtube.com/playlist?' in url :
  VevVevVVVVee = 'plugin://plugin.video.youtube/playlist/' + description + '/'
 if 'plugin://' in url :
  VevVevVVVVee = url
 Ii1I1Ii = [ ]
 eVeeVev = VeevVee . getSetting ( 'favlist' )
 if eVeeVev == 'yes' : Ii1I1Ii . append ( ( '[COLOR red]Remove From Favs?[/COLOR]' , 'XBMC.RunPlugin(%s?mode=21&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
 else : Ii1I1Ii . append ( ( '[COLOR red]Add To Favs?[/COLOR]' , 'XBMC.RunPlugin(%s?mode=20&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
 eVevevevevVVeevev . addContextMenuItems ( Ii1I1Ii , replaceItems = False )
 I111IIIiIii = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = VevVevVVVVee , listitem = eVevevevevVVeevev , isFolder = True )
 return I111IIIiIii
 if 13 - 13: VVeeV . i11iIiiIii
def eVVeeevevVeveve ( name , url , mode , iconimage , fanart , description = '' ) :
 VeevVee . setSetting ( 'favtype' , 'link' )
 VevVevVVVVee = sys . argv [ 0 ] + "?url=" + urllib . quote_plus ( url ) + "&mode=" + str ( mode ) + "&name=" + urllib . quote_plus ( name ) + "&description=" + str ( description ) + "&fanart=" + urllib . quote_plus ( fanart ) + "&iconimage=" + urllib . quote_plus ( iconimage )
 I111IIIiIii = True
 eVevevevevVVeevev = xbmcgui . ListItem ( name , iconImage = "DefaultFolder.png" , thumbnailImage = iconimage )
 eVevevevevVVeevev . setProperty ( 'fanart_image' , fanart )
 Ii1I1Ii = [ ]
 eVeeVev = VeevVee . getSetting ( 'favlist' )
 if eVeeVev == 'yes' : Ii1I1Ii . append ( ( '[COLOR red]Remove from Favs?[/COLOR]' , 'XBMC.RunPlugin(%s?mode=21&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
 else : Ii1I1Ii . append ( ( '[COLOR red]Add to Favs[/COLOR]' , 'XBMC.RunPlugin(%s?mode=20&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
 eVevevevevVVeevev . addContextMenuItems ( Ii1I1Ii , replaceItems = False )
 I111IIIiIii = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = VevVevVVVVee , listitem = eVevevevevVVeevev , isFolder = False )
 return I111IIIiIii
 if 98 - 98: VVeVeeevevee + Vevevevee + iiIIIIi1i1 % Ii11111i
def IIIii1II1II ( name , url , mode , iconimage , fanart , description = '' ) :
 VeevVee . setSetting ( 'favtype' , 'link' )
 VevVevVVVVee = sys . argv [ 0 ] + "?url=" + urllib . quote_plus ( url ) + "&mode=" + str ( mode ) + "&name=" + urllib . quote_plus ( name ) + "&description=" + str ( description ) + "&fanart=" + urllib . quote_plus ( fanart ) + "&iconimage=" + urllib . quote_plus ( iconimage )
 I111IIIiIii = True
 eVevevevevVVeevev = xbmcgui . ListItem ( name , iconImage = "DefaultFolder.png" , thumbnailImage = iconimage )
 eVevevevevVVeevev . setProperty ( 'fanart_image' , fanart )
 eVevevevevVVeevev . setProperty ( "IsPlayable" , "true" )
 Ii1I1Ii = [ ]
 eVeeVev = VeevVee . getSetting ( 'favlist' )
 if eVeeVev == 'yes' : Ii1I1Ii . append ( ( '[COLOR red]Remove from Favs?[/COLOR]' , 'XBMC.RunPlugin(%s?mode=21&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
 else : Ii1I1Ii . append ( ( '[COLOR red]Add to Favs?[/COLOR]' , 'XBMC.RunPlugin(%s?mode=20&name=%s&url=%s&iconimage=%s)' % ( sys . argv [ 0 ] , name , url , iconimage ) ) )
 eVevevevevVVeevev . addContextMenuItems ( Ii1I1Ii , replaceItems = False )
 I111IIIiIii = xbmcplugin . addDirectoryItem ( handle = int ( sys . argv [ 1 ] ) , url = VevVevVVVVee , listitem = eVevevevevVVeevev , isFolder = False )
 return I111IIIiIii
IIiiIiI1 = base64 . b64decode ( 'aHR0cDovL3d3dy5tYXRzYnVpbGRzLnVrL1RoZUp1a2VCb3hNZW51L211c2ljbWVudTAxLnR4dA==' )
def iiiIi ( url , name ) :
 eeeeeeevVeveveve = ii ( url )
 if len ( eeeeeeevVeveveve ) > 1 :
  eeeVeveeeveVVVV = Veeeeveveve
  VeV = os . path . join ( os . path . join ( eeeVeveeeveVVVV , '' ) , name + '.txt' )
  if not os . path . exists ( VeV ) :
   file ( VeV , 'w' ) . close ( )
  eeVevVevVeveeVVV = open ( VeV )
  eVVeevVeveve = eeVevVevVeveeVVV . read ( )
  if eVVeevVeveve == eeeeeeevVeveveve : pass
  else :
   iIiIi11 ( '[B][COLOR red]T[/COLOR][COLOR white]he[/COLOR] [COLOR red]J[/COLOR][COLOR white]ukeBox INFO[/COLOR][/B]' , eeeeeeevVeveveve )
   VVViiiiI = open ( VeV , "w" )
   VVViiiiI . write ( eeeeeeevVeveveve )
   VVViiiiI . close ( )
   if 62 - 62: Ii11111i * II1iI
def iIiIi11 ( heading , text ) :
 id = 10147
 xbmc . executebuiltin ( 'ActivateWindow(%d)' % id )
 xbmc . sleep ( 500 )
 eVVVeeevVeveV = xbmcgui . Window ( id )
 iIII1I111III = 50
 while ( iIII1I111III > 0 ) :
  try :
   xbmc . sleep ( 10 )
   iIII1I111III -= 1
   eVVVeeevVeveV . getControl ( 1 ) . setLabel ( heading )
   eVVVeeevVeveV . getControl ( 5 ) . setText ( text )
   return
  except :
   pass
   if 20 - 20: Ii1Ii1iiii11 . VevVeeveVeve % VVeVeeevevee * I1iII1iiII
   if 98 - 98: II1iI % VVeeV * Ii11111i
def VeiIIiIi1 ( url , fanart ) :
 VeevVee . setSetting ( 'favlist' , 'yes' )
 eevVeveev = None
 file = open ( IiIi11iIIi1Ii , 'r' )
 eevVeveev = file . read ( ) . replace ( '\n' , '' ) . replace ( '\r' , '' )
 iiIiIIi = re . compile ( "<item>(.+?)</item>" , re . DOTALL ) . findall ( eevVeveev )
 for eeVeeevV in iiIiIIi :
  i11Iiii ( II11iiii1Ii , url , II1 , fanart , eeVeeevV )
 VeevVee . setSetting ( 'favlist' , 'no' )
 if 37 - 37: I1I1i1 * iI1 % i11iIiiIii % eeveVeevVeeevV + VVeeV
def VVeVVeveeveev ( name , url , iconimage , fanart ) :
 ii1I1 = VeevVee . getSetting ( 'favtype' )
 url = url . replace ( ' ' , '%20' )
 iconimage = iconimage . replace ( ' ' , '%20' )
 if '<>' in url :
  Iii1I1I11iiI1 = url . split ( '<>' ) [ 0 ]
  ii1I = url . split ( '<>' ) [ 1 ]
  VeveVev = url . split ( '<>' ) [ 2 ]
  eVevVevVVevV = url . split ( '<>' ) [ 3 ]
  VV = url . split ( '<>' ) [ 4 ]
  eVevVVeeevVV = '<FAV><item>\n<title>' + name + '</title>\n<meta>tvep</meta>\n<nan>tvshow</nan>\n<showyear>' + eVevVevVVevV + '</showyear>\n<imdb>' + Iii1I1I11iiI1 + '</imdb>\n<season>' + ii1I + '</season>\n<episode>' + VeveVev + '</episode>\n<episodeyear>' + VV + '</episodeyear>\n<thumbnail>' + iconimage + '</thumbnail>\n<fanart>' + fanart + '</fanart></item></FAV>\n'
 elif len ( url ) == 9 :
  eVevVVeeevVV = '<FAV><item>\n<title>' + name + '</title>\n<meta>movie</meta>\n<nan>movie</nan>\n<imdb>' + url + '</imdb>\n' + '<thumbnail>' + iconimage + '</thumbnail>\n<fanart>' + fanart + '</fanart></item></FAV>\n'
 else :
  eVevVVeeevVV = '<FAV><item>\n<title>' + name + '</title>\n<' + ii1I1 + '>' + url + '</' + ii1I1 + '>\n' + '<thumbnail>' + iconimage + '</thumbnail>\n<fanart>' + fanart + '</fanart></item></FAV>\n'
 Ve = open ( IiIi11iIIi1Ii , 'a' )
 Ve . write ( eVevVVeeevVV )
 Ve . close ( )
 if 93 - 93: VeveveeVV % iiI1i1 . VVeVeeevevee / II1iI - eVeevVe / II1iI
def II1IiiIi1i ( name , url , iconimage ) :
 print name
 eevVeveev = None
 file = open ( IiIi11iIIi1Ii , 'r' )
 eevVeveev = file . read ( )
 iiI11ii1I1 = ''
 iiIiIIi = re . compile ( '<item>(.+?)</item>' , re . DOTALL ) . findall ( eevVeveev )
 for VeeVev in iiIiIIi :
  eVevVVeeevVV = '\n<FAV><item>\n' + VeeVev + '</item>\n'
  if name in VeeVev :
   print 'xxxxxxxxxxxxxxxxx'
   eVevVVeeevVV = eVevVVeeevVV . replace ( 'item' , ' ' )
  iiI11ii1I1 = iiI11ii1I1 + eVevVVeeevVV
 file = open ( IiIi11iIIi1Ii , 'w' )
 file . truncate ( )
 file . write ( iiI11ii1I1 )
 file . close ( )
 xbmc . executebuiltin ( 'Container.Refresh' )
 if 82 - 82: VevVeeveVeve % iI1 / VevVeeeevev + I111i1i1111i / Ii1Ii1iiii11 / eVeevVe
 if 70 - 70: iiIIIIi1i1
def Veeveev ( link ) :
 try :
  eVVeVeveeveV = re . compile ( '<layouttype>(.+?)</layouttype>' ) . findall ( link ) [ 0 ]
  if eVVeVeveeveV == 'thumbnail' : xbmc . executebuiltin ( 'Container.SetViewMode(500)' )
  else : xbmc . executebuiltin ( 'Container.SetViewMode(50)' )
 except : pass
 if 93 - 93: Vevevevee * Ii11111i + eeveVeevVeeevV
 if 33 - 33: VeveveeVV * Ii1Ii1iiii11 - eVeevVe % eVeevVe
IIIII11I1IiI = III1IiiI ( ) ; VeveV = None ; II11iiii1Ii = None ; VeeevVVeveVV = None ; I11I = None ; VVeveVee = None ; I11iIi1i1II11 = None
try : I11I = urllib . unquote_plus ( IIIII11I1IiI [ "site" ] )
except : pass
try : VeveV = urllib . unquote_plus ( IIIII11I1IiI [ "url" ] )
except : pass
try : II11iiii1Ii = urllib . unquote_plus ( IIIII11I1IiI [ "name" ] )
except : pass
try : VeeevVVeveVV = int ( IIIII11I1IiI [ "mode" ] )
except : pass
try : VVeveVee = urllib . unquote_plus ( IIIII11I1IiI [ "iconimage" ] )
except : pass
try : iiiii = urllib . unquote_plus ( IIIII11I1IiI [ "fanart" ] )
except : pass
try : I11iIi1i1II11 = str ( IIIII11I1IiI [ "description" ] )
except : pass
if 47 - 47: Ii11111i . I111i1i1111i
if VeeevVVeveVV == None or VeveV == None or len ( VeveV ) < 1 : VeeVevVV ( )
elif VeeevVVeveVV == 1 : I11I11i1I ( II11iiii1Ii , VeveV , VVeveVee , iiiii )
elif VeeevVVeveVV == 2 : iii1i1iiiiIi ( II11iiii1Ii , VeveV , VVeveVee , I11iIi1i1II11 )
elif VeeevVVeveVV == 3 : VeeVevVeVVVV ( II11iiii1Ii , VeveV , VVeveVee )
elif VeeevVVeveVV == 4 : VVevVeVeveevev ( II11iiii1Ii , VeveV , VVeveVee )
elif VeeevVVeveVV == 5 : VeVVeveeeve ( )
elif VeeevVVeveVV == 11 : Vee ( VeveV )
elif VeeevVVeveVV == 15 : SCRAPEMOVIE ( II11iiii1Ii , VeveV , VVeveVee )
elif VeeevVVeveVV == 16 : Iiii ( II11iiii1Ii , VeveV , VVeveVee )
if 26 - 26: VVeeV % I1I1i1
elif VeeevVVeveVV == 20 : VVeVVeveeveev ( II11iiii1Ii , VeveV , VVeveVee , iiiii )
elif VeeevVVeveVV == 21 : II1IiiIi1i ( II11iiii1Ii , VeveV , VVeveVee )
elif VeeevVVeveVV == 22 : VeiIIiIi1 ( VeveV , iiiii )
if 76 - 76: Vevevevee * eeVevevee
if 52 - 52: VVeVeeevevee
if 19 - 19: II1iI
if 25 - 25: VVeeV / eeveVeevVeeevV
xbmcplugin . endOfDirectory ( int ( sys . argv [ 1 ] ) )
# dd678faae9ac167bc83abf78e5cb2f3f0688d3a3
