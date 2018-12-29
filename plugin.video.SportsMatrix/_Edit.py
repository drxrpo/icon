import xbmcaddon
# 2018-04-11 
#####--Addon details--#####
'''change name to that of your addon, same as file name'''
addon = xbmcaddon.Addon('plugin.video.SportsMatrix') 


####--Route to text file--######
'''change Mainbase URL link to the URL of your 1st text file or home text file and encode using encoder'''
MainBase = 'aHR0cHM6Ly9wYXN0ZWJpbi5jb20vcmF3LzF0Qjc2M3Vk'

####---API Keys--####
'''if you are to use own api key and wish to use it in addon for all insert here also in settings is a place to enter the key Edit UseTMDB to False api key requires encoding  '''
UseTMDB  = True
TMDB_api = 'd2779ce965c0f5c2c3917840e9f218b7'

#####--Art Work--#####
'''Change these paths if you wish to use custom art work for hard coded sections favorites,settings,history, DailyMotion or YouTube icons, 5 icons are already stored but you may wish to use your own to change you can either replace the icons in the resources/art folder remember to keep the name the same or put a URL in the paths below. If you wish to use custom fanart for theses sections enter a URL in to the path else the standard fanart will be used'''
DailyMotionIcon   = 'https://www.shareicon.net/download/2017/04/14/883927_circle_512x512.png'
DailyMotionFanart = 'https://s3.eu-central-1.amazonaws.com/centaur-wp/designweek/prod/content/uploads/2015/03/dailymotion-01-1002x564.jpg'
FavoriteIcon      = 'http://www.iconarchive.com/download/i85575/graphicloads/100-flat/favourite-2.ico'
FavoriteFanart    = 'https://img00.deviantart.net/8bb7/i/2012/349/2/b/techno_wallpaper_2_0_hd_by_gredius-d5o48do.jpg'
HistoryIcon       = 'https://cdn3.iconfinder.com/data/icons/google-material-design-icons/48/ic_history_48px-512.png'
HistoryFanart     = 'http://getwallpapers.com/wallpaper/full/8/2/a/159732.jpg'
SettingIcon       = 'http://www.icons101.com/icon_png/size_512/id_82902/Settings.png'
SettingFanart     = 'http://www.reuun.com/data/out/113/403452827-settings-wallpapers.jpg'
YouTubeIcon       = 'https://upload.wikimedia.org/wikipedia/commons/thumb/5/52/YouTube_social_white_circle_%282017%29.svg/2000px-YouTube_social_white_circle_%282017%29.svg.png' #channel listings only text file and hard code YouTube Search 
YouTubeFanart     = 'http://wallsfield.com/wp-content/uploads/2015/03/youtube-700x329.jpg'
'''You tube search list does not pull any fanart if default will be standard fanart of addon if you would like to use custom enter url in between speech marks empty speech marks will use default'''
YT_SearchFanart = 'http://wallsfield.com/wp-content/uploads/2015/03/youtube-700x329.jpg'


#####--Hard Coding settings--###
'''use text files as source of content and menu's it is possible to use a mixture of both'''
HCS_text = True
'''use hard coded directories change to true if you want to use other methods of adding content other then text files'''
HCS_addDir = False

'''#####-----Update notes -------#######
2018-04-11 Added TMDB settings 
2018-04-09 Added option for History Icon and fanart'''