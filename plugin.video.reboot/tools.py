import xbmc,xbmcplugin,xbmcaddon,xbmcgui,urllib,urllib2,re,sys,os,time,socket,gzip
from StringIO import StringIO
try:
    from sqlite3 import dbapi2 as database
except:
    from pysqlite2 import dbapi2 as database
module_log_enabled=False; http_debug_log_enabled=False; LIST="list"; THUMBNAIL="thumbnail"; MOVIES="movies"; TV_SHOWS="tvshows"; SEASONS="seasons"; EPISODES="episodes"; OTHER="other"; 
ALL_VIEW_CODES={
    'list': {
        'skin.confluence': 50, # List
        'skin.aeon.nox': 50, # List
        'skin.droid': 50, # List
        'skin.quartz': 50, # List
        'skin.re-touched': 50, # List
        'skin.durexonfluence': 50, # List
        'skin.hybrid.dev': 50, # List
    },
    'thumbnail': {
        'skin.confluence': 500, # Thumbnail
        'skin.aeon.nox': 500, # Wall
        'skin.droid': 51, # Big icons
        'skin.quartz': 51, # Big icons
        'skin.re-touched': 500, #Thumbnail
        'skin.durexonfluence': 500, # Thumbnail
        'skin.hybrid.dev': 500, # Thumbnail
    },
    'movies': {
        'skin.confluence': 500, # Thumbnail 515, # Media Info 3
        'skin.aeon.nox': 500, # Wall
        'skin.droid': 51, # Big icons
        'skin.quartz': 52, # Media info
        'skin.re-touched': 500, #Thumbnail
        'skin.durexonfluence': 500, # Thumbnail
        'skin.hybrid.dev': 500, # Thumbnail
    },
    'tvshows': {
        'skin.confluence': 500, # Thumbnail 515, # Media Info 3
        'skin.aeon.nox': 500, # Wall
        'skin.droid': 51, # Big icons
        'skin.quartz': 52, # Media info
        'skin.re-touched': 500, #Thumbnail
        'skin.durexonfluence': 500, # Thumbnail
        'skin.hybrid.dev': 500, # Thumbnail
    },
    'seasons': {
        'skin.confluence': 50, # List
        'skin.aeon.nox': 50, # List
        'skin.droid': 50, # List
        'skin.quartz': 52, # Media info
        'skin.re-touched': 50, # List
        'skin.durexonfluence': 50, # List
        'skin.hybrid.dev': 50, # List
    },
    'episodes': {
        'skin.confluence': 504, # Media Info
        'skin.aeon.nox': 518, # Infopanel
        'skin.droid': 50, # List
        'skin.quartz': 52, # Media info
        'skin.re-touched': 550, # Wide
        'skin.durexonfluence': 550, # Wide
        'skin.hybrid.dev': 550, # Wide
    },
}
def get_runtime_path(): _log("get_runtime_path"); dev=xbmc.translatePath(__settings__.getAddonInfo('Path')); _log("get_runtime_path ->'"+str(dev)+"'"); return dev
def get_setting(name): _log("get_setting name='"+name+"'"); dev=__settings__.getSetting(name); _log("get_setting ->'"+str(dev)+"'"); return dev
def set_setting(name,value): _log("set_setting name='"+name+"','"+value+"'"); __settings__.setSetting( name,value )
def log(message): xbmc.log(message)
def get_params():
    _log("get_params"); param_string=sys.argv[2]; _log("get_params "+str(param_string)); commands={}
    if param_string:
        split_commands=param_string[param_string.find('?') + 1:].split('&')
        for command in split_commands:
            _log("get_params command="+str(command))
            if len(command) > 0:
                if "=" in command: split_command=command.split('='); key=split_command[0]; value=urllib.unquote_plus(split_command[1]); commands[key]=value
                else: commands[command]=""
    _log("get_params "+repr(commands))
    return commands
def Get_Params():
    param = []
    paramstring = sys.argv[2]
    if len(paramstring) >= 2:
        params = sys.argv[2]
        cleanedparams = params.replace('?','')
        if (params[len(params)-1] == '/'):
            params = params[0:len(params)-2]
        pairsofparams = cleanedparams.split('&')
        param = {}
        for i in range(len(pairsofparams)):
            splitparams = {}
            splitparams = pairsofparams[i].split('=')
            if (len(splitparams)) == 2:
                param[splitparams[0].lower()] = splitparams[1]
    return param
def close_item_list(): _log("close_item_list"); xbmcplugin.endOfDirectory(handle=int(sys.argv[1]),succeeded=True)
def add_item(action="",title="",plot="",url="",thumbnail="",fanart="",show="",episode="",extra="",page="",info_labels=None,isPlayable=False,folder=True):
    _log("add_item action=["+action+"] title=["+title+"] url=["+url+"] thumbnail=["+thumbnail+"] fanart=["+fanart+"] show=["+show+"] episode=["+episode+"] extra=["+extra+"] page=["+page+"] isPlayable=["+str(isPlayable)+"] folder=["+str(folder)+"]")
    listitem=xbmcgui.ListItem(title,iconImage="DefaultVideo.png",thumbnailImage=thumbnail)
    if info_labels is None: info_labels={"Title":title,"FileName":title,"Plot":plot}
    listitem.setInfo( "video", info_labels )
    if fanart!="": listitem.setProperty('fanart_image',fanart); xbmcplugin.setPluginFanart(int(sys.argv[1]),fanart)
    if url.startswith("plugin://"): itemurl=url; listitem.setProperty('IsPlayable','true'); xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=itemurl,listitem=listitem,isFolder=folder)
    elif isPlayable: listitem.setProperty("Video","true"); listitem.setProperty('IsPlayable','true'); itemurl='%s?action=%s&title=%s&url=%s&thumbnail=%s&plot=%s&extra=%s&page=%s' % (sys.argv[0],action,urllib.quote_plus(title),urllib.quote_plus(url),urllib.quote_plus(thumbnail),urllib.quote_plus(plot),urllib.quote_plus(extra),urllib.quote_plus(page)); xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=itemurl,listitem=listitem,isFolder=folder)
    else: itemurl='%s?action=%s&title=%s&url=%s&thumbnail=%s&plot=%s&extra=%s&page=%s' % (sys.argv[0],action,urllib.quote_plus(title),urllib.quote_plus(url),urllib.quote_plus(thumbnail),urllib.quote_plus(plot),urllib.quote_plus(extra),urllib.quote_plus(page)); xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=itemurl,listitem=listitem,isFolder=folder)
def set_view(view_mode, view_code=0):
    _log("set_view view_mode='"+view_mode+"', view_code="+str(view_code))
    # Set the content for extended library views if needed
    #if view_mode==MOVIES: _log("set_view content is movies"); xbmcplugin.setContent( int(sys.argv[1]) ,"movies" )
    if view_mode==TV_SHOWS: _log("set_view content is tvshows"); xbmcplugin.setContent( int(sys.argv[1]) ,"tvshows" )
    elif view_mode==SEASONS: _log("set_view content is seasons"); xbmcplugin.setContent( int(sys.argv[1]) ,"seasons" )
    elif view_mode==EPISODES: _log("set_view content is episodes"); xbmcplugin.setContent( int(sys.argv[1]) ,"episodes" )
    skin_name=xbmc.getSkinDir() # Reads skin name
    _log("set_view skin_name='"+skin_name+"'")
    try:
        if view_code==0:
            _log("set_view view mode is "+view_mode)
            view_codes=ALL_VIEW_CODES.get(view_mode)
            view_code=view_codes.get(skin_name)
            _log("set_view view code for "+view_mode+" in "+skin_name+" is "+str(view_code))
            xbmc.executebuiltin("Container.SetViewMode("+str(view_code)+")")
        else:
            _log("set_view view code forced to "+str(view_code))
            xbmc.executebuiltin("Container.SetViewMode("+str(view_code)+")")
    except:
        _log("Unable to find view code for view mode "+str(view_mode)+" and skin "+skin_name)
def open_settings_dialog(): _log("open_settings_dialog"); __settings__.openSettings()
def _log(message): # Write this module messages on XBMC log
    if module_log_enabled: xbmc.log("plugintools."+message)
def find_single_match(text,pattern): # Parse string and extracts first match as a string
    _log("find_single_match pattern="+pattern); result=""
    try: matches=re.findall(pattern,text,flags=re.DOTALL); result=matches[0]
    except: result=""
    return result
def Wipe_Cache():
    xbmc_cache_path = os.path.join(xbmc.translatePath('special://home'), 'cache')
    packages_cache_path = xbmc.translatePath(os.path.join('special://home/addons', 'packages'))
    if os.path.exists(xbmc_cache_path)==True:
        for root, dirs, files in os.walk(xbmc_cache_path):
            file_count = 0
            file_count += len(files)
            if file_count > 0:
                for f in files:
                    try:
                        os.unlink(os.path.join(root, f))
                    except:
                        pass
                for d in dirs:
                    try:
                        shutil.rmtree(os.path.join(root, d))
                    except:
                        pass
    if os.path.exists(packages_cache_path)==True:
        for root, dirs, files in os.walk(packages_cache_path):
            file_count = 0
            file_count += len(files)
            if file_count > 0:
                for f in files:
                    try:
                        os.unlink(os.path.join(root, f))
                    except:
                        pass
                for d in dirs:
                    try:
                        shutil.rmtree(os.path.join(root, d))
                    except:
                        pass
    if xbmc.getCondVisibility('system.platform.ATV2'):
        atv2_cache_a = os.path.join('/private/var/mobile/Library/Caches/AppleTV/Video/', 'Other')
        for root, dirs, files in os.walk(atv2_cache_a):
            file_count = 0
            file_count += len(files)
            if file_count > 0:
                for f in files:
                    os.unlink(os.path.join(root, f))
                for d in dirs:
                    shutil.rmtree(os.path.join(root, d))
        atv2_cache_b = os.path.join('/private/var/mobile/Library/Caches/AppleTV/Video/', 'LocalAndRental')        
        for root, dirs, files in os.walk(atv2_cache_b):
            file_count = 0
            file_count += len(files)
            if file_count > 0:
                for f in files:
                    os.unlink(os.path.join(root, f))
                for d in dirs:
                    shutil.rmtree(os.path.join(root, d))
    # Set path to script.module.simple.downloader cache files
    downloader_cache_path = os.path.join(xbmc.translatePath('special://profile/addon_data/script.module.simple.downloader'), '')
    if os.path.exists(downloader_cache_path)==True:    
        for root, dirs, files in os.walk(downloader_cache_path):
            file_count = 0
            file_count += len(files)
            if file_count > 0:
                for f in files:
                    os.unlink(os.path.join(root, f))
                for d in dirs:
                    shutil.rmtree(os.path.join(root, d))
    # Set path to script.image.music.slideshow cache files
    imageslideshow_cache_path = os.path.join(xbmc.translatePath('special://profile/addon_data/script.image.music.slideshow/cache'), '')
    if os.path.exists(imageslideshow_cache_path)==True:    
        for root, dirs, files in os.walk(imageslideshow_cache_path):
            file_count = 0
            file_count += len(files)
            if file_count > 0:
                for f in files:
                    os.unlink(os.path.join(root, f))
                for d in dirs:
                    shutil.rmtree(os.path.join(root, d))
    # Set path to BBC iPlayer cache files
    iplayer_cache_path= os.path.join(xbmc.translatePath('special://profile/addon_data/plugin.video.iplayer/iplayer_http_cache'), '')
    if os.path.exists(iplayer_cache_path)==True:    
        for root, dirs, files in os.walk(iplayer_cache_path):
            file_count = 0
            file_count += len(files)
            if file_count > 0:
                for f in files:
                    os.unlink(os.path.join(root, f))
                for d in dirs:
                    shutil.rmtree(os.path.join(root, d))
    itv_cache_path = os.path.join(xbmc.translatePath('special://profile/addon_data/plugin.video.itv/Images'), '')
    if os.path.exists(itv_cache_path)==True:    
        for root, dirs, files in os.walk(itv_cache_path):
            file_count = 0
            file_count += len(files)
            if file_count > 0:
                for f in files:
                    os.unlink(os.path.join(root, f))
                for d in dirs:
                    shutil.rmtree(os.path.join(root, d))
    navix_cache_path= os.path.join(xbmc.translatePath('special://profile/addon_data/script.navi-x/cache'), '')
    if os.path.exists(navix_cache_path)==True:    
        for root, dirs, files in os.walk(navix_cache_path):
            file_count = 0
            file_count += len(files)
            if file_count > 0:
                for f in files:
                    os.unlink(os.path.join(root, f))
                for d in dirs:
                    shutil.rmtree(os.path.join(root, d))
    phoenix_cache_path= os.path.join(xbmc.translatePath('special://profile/addon_data/plugin.video.phstreams/Cache'), '')
    if os.path.exists(phoenix_cache_path)==True:    
        for root, dirs, files in os.walk(phoenix_cache_path):
            file_count = 0
            file_count += len(files)
            if file_count > 0:
                for f in files:
                    os.unlink(os.path.join(root, f))
                for d in dirs:
                    shutil.rmtree(os.path.join(root, d))
    ramfm_cache_path= os.path.join(xbmc.translatePath('special://profile/addon_data/plugin.audio.ramfm/cache'), '')
    if os.path.exists(ramfm_cache_path)==True:    
        for root, dirs, files in os.walk(ramfm_cache_path):
            file_count = 0
            file_count += len(files)
            if file_count > 0:
                for f in files:
                    os.unlink(os.path.join(root, f))
                for d in dirs:
                    shutil.rmtree(os.path.join(root, d))
    wtf_cache_path = os.path.join(xbmc.translatePath('special://profile/addon_data/plugin.video.whatthefurk/cache'), '')
    if os.path.exists(wtf_cache_path)==True:    
        for root, dirs, files in os.walk(wtf_cache_path):
            file_count = 0
            file_count += len(files)
            if file_count > 0:
                for f in files:
                    os.unlink(os.path.join(root, f))
                for d in dirs:
                    shutil.rmtree(os.path.join(root, d))
    try:
        genesisCache = os.path.join(xbmc.translatePath('special://profile/addon_data/plugin.video.genesis'), 'cache.db')
        dbcon = database.connect(genesisCache)
        dbcur = dbcon.cursor()
        dbcur.execute("DROP TABLE IF EXISTS rel_list")
        dbcur.execute("VACUUM")
        dbcon.commit()
        dbcur.execute("DROP TABLE IF EXISTS rel_lib")
        dbcur.execute("VACUUM")
        dbcon.commit()
    except:
        pass

f=open(os.path.join(os.path.dirname(__file__),"addon.xml")); data=f.read(); f.close()
addon_id=find_single_match(data,'id="([^"]+)"')
if addon_id=="": addon_id=find_single_match(data,"id='([^']+)'")
__settings__=xbmcaddon.Addon(id=addon_id); __language__=__settings__.getLocalizedString