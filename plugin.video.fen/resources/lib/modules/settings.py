import xbmc, xbmcaddon
import os
# from resources.lib.modules.utils import logger

__addon__ = xbmcaddon.Addon(id='plugin.video.fen')
ADDON_PATH = xbmc.translatePath(__addon__.getAddonInfo('path'))
DATA_PATH = xbmc.translatePath(__addon__.getAddonInfo('profile'))

def addon_installed(addon_id):
    if xbmc.getCondVisibility('System.HasAddon(%s)' % addon_id): return True
    else: return False

def get_theme():
    if __addon__.getSetting('theme_installed') == 'true':
        theme = __addon__.getSetting('fen.theme').lower()
        result = os.path.join(xbmcaddon.Addon('script.tiki.artwork').getAddonInfo('path'), 'resources', 'media', theme)
    elif addon_installed('script.tiki.artwork'):
        __addon__.setSetting('theme_installed', 'true')
        theme = __addon__.getSetting('fen.theme').lower()
        if theme in ['-', '']: theme = 'light'
        result = os.path.join(xbmcaddon.Addon('script.tiki.artwork').getAddonInfo('path'), 'resources', 'media', theme)
    else: result = 'null'
    return result

def tmdb_api():
    tmdb_api = __addon__.getSetting('tmdb_api')
    if not tmdb_api or tmdb_api == '':
        tmdb_api = '1b0d3c6ac6a6c0fa87b55a1069d6c9c8'
    return tmdb_api

def check_database(database):
    import xbmcvfs
    if not xbmcvfs.exists(database): initialize_databases()

def use_dialog():
    if __addon__.getSetting('use_dialog') == "1": return True
    else: return False

def addon():
    return __addon__

def show_specials():
    if __addon__.getSetting('show_specials') == 'true': return True
    else: return False

def adjusted_datetime(string=False, dt=False):
    from datetime import datetime, timedelta
    d = datetime.utcnow() + timedelta(hours=int(__addon__.getSetting('datetime.offset')))
    if dt: return d
    d = datetime.date(d)
    if string:
        try: d = d.strftime('%Y-%m-%d')
        except ValueError: d = d.strftime('%Y-%m-%d')
    else: return d
    
def movies_directory():
    return xbmc.translatePath(__addon__.getSetting('movies_directory'))
    
def tv_show_directory():
    return xbmc.translatePath(__addon__.getSetting('tv_shows_directory'))

def download_directory(db_type):
    setting = 'movie_download_directory' if db_type == 'movie' \
        else 'tvshow_download_directory' if db_type == 'episode' \
        else 'furk_file_download_directory' if db_type in ('furk_file', 'archive') \
        else 'easynews_file_download_directory'
    if __addon__.getSetting(setting) != '': return xbmc.translatePath( __addon__.getSetting(setting))
    else: return False

def quality_filter(setting):
    return __addon__.getSetting(setting).split(', ')

def include_prerelease_results():
    if __addon__.getSetting('include_prerelease_results') == "true": return True
    else: return False

def include_local_in_filter():
    if __addon__.getSetting('include_local_in_filter') == "true": return True
    else: return False

def include_downloads_in_filter():
    if __addon__.getSetting('include_downloads_in_filter') == "true": return True
    else: return False

def include_uncached_results():
    if __addon__.getSetting('include_uncached_results') == "true": return True
    else: return False

def auto_play():
    if __addon__.getSetting('auto_play') == "true": return True
    else: return False

def auto_resolve():
    if __addon__.getSetting('auto_resolve') == "true": return True
    else: return False

def autoplay_next_episode():
    if auto_play() and __addon__.getSetting('autoplay_next_episode') == "true": return True
    else: return False

def autoplay_next_check_threshold():
    return int(__addon__.getSetting('autoplay_next_check_threshold'))

def nextep_threshold():
    return float(__addon__.getSetting('nextep.threshold'))

def prefer_hevc():
    if __addon__.getSetting('prefer_hevc') == "true": return True
    else: return False

def sync_kodi_library_watchstatus():
    if __addon__.getSetting('sync_kodi_library_watchstatus') == "true": return True
    else: return False
    
def trakt_cache_duration():
    duration = (1, 24, 168)
    return duration[int(__addon__.getSetting('trakt_cache_duration'))]

def watched_indicators():
    if __addon__.getSetting('trakt_user') == '': return 0
    elif __addon__.getSetting('watched_indicators') == '0': return 0
    elif __addon__.getSetting('watched_indicators') == '1' and __addon__.getSetting('sync_fen_watchstatus') == 'true': return 1
    else: return 2

def check_library():
    if __addon__.getSetting('check_library') == "true" and __addon__.getSetting('auto_play') != "true": return True
    else: return False

def check_downloads():
    if __addon__.getSetting('check_downloads') == "true" and __addon__.getSetting('auto_play') != "true": return True
    else: return False

def subscription_update():
    if __addon__.getSetting('subscription_update') == "true": return True
    else: return False

def skip_duplicates():
    if __addon__.getSetting('skip_duplicates') == "true": return True
    else: return False

def update_library_after_service():
    if __addon__.getSetting('update_library_after_service') == "true": return True
    else: return False

def results_sort_order():
    results_sort_order = __addon__.getSetting('results.sort_order')
    if results_sort_order == '0': return ('quality_rank', 'name_rank', 'size')
    elif results_sort_order == '1': return ('name_rank', 'quality_rank', 'size')
    else: return ('', '', '')

def local_sorted_first():
    if __addon__.getSetting('results.sort_local_first') == "true": return True
    else: return False

def downloads_sorted_first():
    if __addon__.getSetting('results.sort_downloads_first') == "true": return True
    else: return False

def provider_color(provider):
    return __addon__.getSetting('provider.%s_colour' % provider)

def active_scrapers():
    settings = ['provider.local', 'provider.downloads', 'provider.furk', 'provider.easynews', 'provider.external']
    return [i.split('.')[1] for i in settings if __addon__.getSetting(i) == 'true']

def show_filenames():
    if __addon__.getSetting('results.show_filenames') == 'true': return True
    return False

def subscription_timer():
    hours_list = [1, 2, 4, 6, 8, 10, 12, 14, 15, 18, 24]
    return hours_list[int(__addon__.getSetting('subscription_timer'))]

def auto_resume():
    if __addon__.getSetting('auto_resume') == '1': return True
    if __addon__.getSetting('auto_resume') == '2' and auto_play(): return True
    else: return False

def set_resume():
    return float(__addon__.getSetting('resume.threshold'))

def set_watched():
    return float(__addon__.getSetting('watched.threshold'))

def nav_jump_use_alphabet():
    if __addon__.getSetting('nav_jump') == '0': return False
    else: return True

def all_trailers():
    if __addon__.getSetting('all_trailers') == "true": return True
    else: return False

def use_season_title():
    if __addon__.getSetting('use_season_title') == "true": return True
    else: return False

def unaired_episode_colour():
    unaired_episode_colour = __addon__.getSetting('unaired_episode_colour')
    if not unaired_episode_colour or unaired_episode_colour == '': unaired_episode_colour = 'red'
    return unaired_episode_colour

def nextep_airdate_format():
    date_format = __addon__.getSetting('nextep.airdate_format')
    if date_format == '0': return '%d-%m-%Y'
    elif date_format == '1': return '%Y-%m-%d'
    elif date_format == '2': return '%m-%d-%Y'
    else: return '%Y-%m-%d'

def nextep_display_settings():
    from ast import literal_eval
    include_airdate = True
    force_display = False
    airdate_colour = 'magenta'
    unaired_colour = 'red'
    unwatched_colour = 'darkgoldenrod'
    try: include_airdate = literal_eval(__addon__.getSetting('nextep.include_airdate').title())
    except: pass
    try: force_display = literal_eval(__addon__.getSetting('nextep.force_display').title())
    except: pass
    try: airdate_colour = __addon__.getSetting('nextep.airdate_colour')
    except: pass
    try: unaired_colour = __addon__.getSetting('nextep.unaired_colour')
    except: pass
    try: unwatched_colour = __addon__.getSetting('nextep.unwatched_colour')
    except: pass
    return {'include_airdate': include_airdate, 'force_display': force_display, 'airdate_colour': airdate_colour,
            'unaired_colour': unaired_colour, 'unwatched_colour': unwatched_colour}

def nextep_content_settings():
    from ast import literal_eval
    sort_type = int(__addon__.getSetting('nextep.sort_type'))
    sort_order = int(__addon__.getSetting('nextep.sort_order'))
    sort_direction = True if sort_order == 0 else False
    sort_key = 'curr_last_played_parsed' if sort_type == 0 else 'first_aired' if sort_type == 1 else 'name'
    include_unaired = literal_eval(__addon__.getSetting('nextep.include_unaired').title())
    include_unwatched = literal_eval(__addon__.getSetting('nextep.include_unwatched').title())
    return {'sort_key': sort_key, 'sort_direction': sort_direction, 'sort_type': sort_type, 'sort_order':sort_order,
            'include_unaired': include_unaired, 'include_unwatched': include_unwatched}

def create_directory(dir_path, dir_name=None):
    if dir_name:
        dir_path = os.path.join(dir_path, dir_name)
    dir_path = dir_path.strip()
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    return dir_path

def initialize_databases():
    import xbmcvfs
    if not xbmcvfs.exists(DATA_PATH): xbmcvfs.mkdirs(DATA_PATH)
    NAVIGATOR_DB = os.path.join(DATA_PATH, "navigator.db")
    WATCHED_DB = os.path.join(DATA_PATH, "watched_status.db")
    FAVOURITES_DB = os.path.join(DATA_PATH, "favourites.db")
    SUBSCRIPTIONS_DB = os.path.join(DATA_PATH, "subscriptions.db")
    VIEWS_DB = os.path.join(DATA_PATH, "views.db")
    TRAKT_DB = os.path.join(DATA_PATH, "fen_trakt.db")
    FEN_DB = os.path.join(DATA_PATH, "fen_cache.db")
    if not xbmcvfs.exists(NAVIGATOR_DB):
        try: from sqlite3 import dbapi2 as database
        except ImportError: from pysqlite2 import dbapi2 as database
        dbcon = database.connect(NAVIGATOR_DB)
        dbcon.execute("""CREATE TABLE IF NOT EXISTS navigator
                          (list_name text, list_type text, list_contents text) 
                       """)
        dbcon.close()
    if not xbmcvfs.exists(WATCHED_DB):
        try: from sqlite3 import dbapi2 as database
        except: from pysqlite2 import dbapi2 as database
        dbcon = database.connect(WATCHED_DB)
        dbcon.execute("""CREATE TABLE IF NOT EXISTS progress
                          (db_type text, media_id text, season integer, episode integer,
                          resume_point text, curr_time text,
                          unique(db_type, media_id, season, episode)) 
                       """)
        dbcon.execute("""CREATE TABLE IF NOT EXISTS watched_status
                          (db_type text, media_id text, season integer,
                          episode integer, last_played text, title text,
                          unique(db_type, media_id, season, episode)) 
                       """)
        dbcon.execute("""CREATE TABLE IF NOT EXISTS exclude_from_next_episode
                          (media_id text, title text) 
                       """)
        dbcon.execute("""CREATE TABLE IF NOT EXISTS unwatched_next_episode
                          (media_id text) 
                       """)
        dbcon.close()
    if not xbmcvfs.exists(FAVOURITES_DB):
        try:from sqlite3 import dbapi2 as database
        except ImportError:from pysqlite2 import dbapi2 as database
        dbcon = database.connect(FAVOURITES_DB)
        dbcon.execute("""CREATE TABLE IF NOT EXISTS favourites
                          (db_type text, tmdb_id text, title text, unique (db_type, tmdb_id)) 
                       """)
        dbcon.close()
    if not xbmcvfs.exists(SUBSCRIPTIONS_DB):
        try: from sqlite3 import dbapi2 as database
        except ImportError: from pysqlite2 import dbapi2 as database
        dbcon = database.connect(SUBSCRIPTIONS_DB)
        dbcon.execute("""CREATE TABLE IF NOT EXISTS subscriptions
                          (db_type text, tmdb_id text, title text, unique (db_type, tmdb_id)) 
                       """)
        dbcon.close()
    if not xbmcvfs.exists(VIEWS_DB):
        try: from sqlite3 import dbapi2 as database
        except ImportError: from pysqlite2 import dbapi2 as database
        dbcon = database.connect(VIEWS_DB)
        dbcon.execute("""CREATE TABLE IF NOT EXISTS views
                          (view_type text, view_id text, unique (view_type)) 
                       """)
        dbcon.close()
    if not xbmcvfs.exists(TRAKT_DB):
        try: from sqlite3 import dbapi2 as database
        except ImportError: from pysqlite2 import dbapi2 as database
        dbcon = database.connect(TRAKT_DB)
        dbcon.execute("""CREATE TABLE IF NOT EXISTS fen_trakt
                           (id text UNIQUE, expires integer, data text)
                            """)
        dbcon.close()
    if not xbmcvfs.exists(FEN_DB):
        try: from sqlite3 import dbapi2 as database
        except ImportError: from pysqlite2 import dbapi2 as database
        dbcon = database.connect(FEN_DB)
        dbcon.execute("""CREATE TABLE IF NOT EXISTS fencache
                           (id text UNIQUE, expires integer, data text, checksum integer)
                            """)
        dbcon.close()
    return True

def refresh_icon():
    import xbmcvfs, xbmcgui
    try: from sqlite3 import dbapi2 as database
    except ImportError: from pysqlite2 import dbapi2 as database
    from resources.lib.modules.nav_utils import notification
    try:
        icon_path = xbmc.translatePath(os.path.join(ADDON_PATH, 'icon.png'))
        thumbs_folder = xbmc.translatePath('special://thumbnails')
        TEXTURE_DB = xbmc.translatePath(os.path.join('special://database', 'Textures13.db'))
        dbcon = database.connect(TEXTURE_DB)
        dbcur = dbcon.cursor()
        dbcur.execute("""SELECT cachedurl FROM texture WHERE url = ?""", (icon_path,))
        image = dbcur.fetchone()[0]
        dbcon.close()
        removal_path = os.path.join(thumbs_folder, image)
        if xbmcgui.Dialog().yesno("Fen", 'Add-on Icon about to be refreshed.', 'Continue?', '', 'No', 'Yes'):
            xbmcvfs.delete(removal_path)
            xbmc.sleep(200)
            xbmc.executebuiltin('ReloadSkin()')
            xbmc.sleep(500)
            notice = '[B]Success!![/B] Icon refreshed.'
        else: return
    except:
        notice = '[B]Error!![/B] deleting icon from database'
    notification(notice)

def media_lists():
    return (
        'tmdb_movies_popular%',
        'tmdb_movies_blockbusters%',
        'tmdb_movies_in_theaters%',
        'tmdb_movies_top_rated%',
        'tmdb_movies_upcoming%',
        'tmdb_movies_latest_releases%',
        'tmdb_movies_premieres%',
        'trakt_movies_trending%',
        'trakt_movies_anticipated%',
        'trakt_movies_top10_boxoffice%',
        'trakt_movies_top10_boxoffice%',
        'imdb_movies_oscar_winners%',
        'tmdb_popular_people%'
        'trakt_movies_mosts%',
        'tmdb_movies_genres%',
        'tmdb_movies_languages%',
        'tmdb_movies_year%',
        'tmdb_movies_certifications%',
        'tmdb_movies_similar%',
        'trakt_movies_related%',
        'tmdb_movies_actor_roles%',
        'tmdb_movies_search%',
        'tmdb_movies_people_search%',
        'tmdb_tv_popular%',
        'tmdb_tv_top_rated%',
        'tmdb_tv_premieres%',
        'tmdb_tv_upcoming%',
        'tmdb_tv_airing_today%',
        'tmdb_tv_on_the_air%',
        'trakt_tv_anticipated%',
        'trakt_tv_trending%',
        'trakt_tv_mosts%',
        'tmdb_tv_genres%',
        'tmdb_tv_languages%',
        'tmdb_tv_networks%',
        'trakt_tv_certifications%',
        'tmdb_tv_year%',
        'tmdb_tv_similar%',
        'trakt_tv_related%',
        'tmdb_tv_actor_roles%',
        'tmdb_tv_search%',
        'tmdb_tv_people_search%',
        )
