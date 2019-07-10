import xbmc, xbmcaddon, xbmcgui, xbmcplugin
import sys, os
from urlparse import parse_qsl
import json
from datetime import datetime, date, timedelta
from resources.lib.modules.text import to_unicode
from resources.lib.modules.trakt_cache import clear_trakt_watched_data
from resources.lib.modules import settings
try: from sqlite3 import dbapi2 as database
except ImportError: from pysqlite2 import dbapi2 as database
# from resources.lib.modules.utils import logger

__addon_id__ = 'plugin.video.fen'
__addon__ = xbmcaddon.Addon(id=__addon_id__)
addon_dir = xbmc.translatePath(__addon__.getAddonInfo('path'))
profile_dir = xbmc.translatePath(__addon__.getAddonInfo('profile'))
__url__ = sys.argv[0]
__handle__ = int(sys.argv[1])

window = xbmcgui.Window(10000)
WATCHED_DB = os.path.join(profile_dir, "watched_status.db")

def get_resumetime(db_type, tmdb_id, season='', episode=''):
    try: resumetime = str((int(round(float(detect_bookmark(db_type, tmdb_id, season, episode)[0])))/float(100))*2400)
    except: resumetime = '0'
    return resumetime

def set_bookmark(db_type, media_id, curr_time, total_time, season='', episode='', from_search='false'):
    settings.check_database(WATCHED_DB)
    erase_bookmark(db_type, media_id, season, episode)
    adjusted_current_time = curr_time - 4
    resume_point = round(float(adjusted_current_time/total_time*100),1)
    dbcon = database.connect(WATCHED_DB)
    dbcur = dbcon.cursor()
    dbcur.execute("INSERT INTO progress VALUES (?, ?, ?, ?, ?, ?)", (db_type, media_id, season, episode, str(resume_point), str(curr_time)))
    dbcon.commit()
    if settings.sync_kodi_library_watchstatus():
        from resources.lib.modules.kodi_library import set_bookmark_kodi_library
        set_bookmark_kodi_library(db_type, media_id, curr_time, season, episode)
    refresh_container(from_search)

def detect_bookmark(db_type, media_id, season='', episode=''):
    settings.check_database(WATCHED_DB)
    dbcon = database.connect(WATCHED_DB)
    dbcon.row_factory = database.Row
    dbcur = dbcon.cursor()
    dbcur.execute("SELECT * FROM progress WHERE (db_type = ? and media_id = ? and season = ? and episode = ?)", (db_type, media_id, season, episode))
    for row in dbcur:
        resume_point = row['resume_point']
        curr_time = row['curr_time']
    return resume_point, curr_time

def erase_bookmark(db_type, media_id, season='', episode=''):
    settings.check_database(WATCHED_DB)
    dbcon = database.connect(WATCHED_DB)
    dbcur = dbcon.cursor()
    dbcur.execute("DELETE FROM progress where db_type=? and media_id=? and season = ? and episode = ?", (db_type, media_id, season, episode))
    dbcon.commit()

def get_watched_status(db_type, media_id, season='', episode=''):
    try:
        if settings.watched_indicators() in (1, 2):
            if db_type == 'movie':
                from resources.lib.modules.trakt import trakt_indicators_movies
                watched = [i[0] for i in trakt_indicators_movies()]
                if media_id in watched: return 1, 7
                return 0, 6
            else:
                from resources.lib.modules.trakt import trakt_indicators_tv
                watched = trakt_indicators_tv()
                watched = [i[2] for i in watched if i[0] == media_id]
                if watched:
                    watched = [i for i in watched[0] if i[0] == season and i[1] == episode]
                    if watched: return 1, 7
                return 0, 6
        else:
            settings.check_database(WATCHED_DB)
            dbcon = database.connect(WATCHED_DB)
            dbcur = dbcon.cursor()
            dbcur.execute("SELECT * FROM watched_status WHERE (db_type = ? and media_id = ? and season = ? and episode = ?)", (db_type, media_id, season, episode))
            watched = dbcur.fetchone()
            dbcon.close()
            if watched: return 1, 7
            else: return 0, 6
    except: return 0, 6

def get_watched_status_tvshow(media_id, aired_eps):
    playcount, overlay = 0, 6
    watched, unwatched = 0, aired_eps
    def get_playcount_overlay(use_trakt):
        try:
            if use_trakt:
                watched = [i for i in watched_info if i[0] == media_id and i[1] == len(i[2])]
                if watched:
                    playcount, overlay = 1, 7
            else:
                if watched_info == aired_eps and not aired_eps == 0:
                    playcount, overlay = 1, 7
        except: pass
        return playcount, overlay
    def get_watched_episode_totals(use_trakt):
        try:
            if use_trakt:
                watched = len([i[2] for i in watched_info if i[0] == media_id][0])
                unwatched = aired_eps - watched
            else:
                watched = watched_info
                unwatched = aired_eps - watched
        except: pass
        return watched, unwatched
    try:
        if settings.watched_indicators() in (1, 2):
            from resources.lib.modules.trakt import trakt_indicators_tv
            use_trakt = True
            watched_info = trakt_indicators_tv()
        else:
            use_trakt = False
            settings.check_database(WATCHED_DB)
            dbcon = database.connect(WATCHED_DB)
            dbcur = dbcon.cursor()
            dbcur.execute("SELECT * FROM watched_status WHERE (db_type = ? and media_id = ?)", ('episode', media_id))
            watched_info = len(dbcur.fetchall())
            dbcon.close()
        watched, unwatched = get_watched_episode_totals(use_trakt)
        playcount, overlay = get_playcount_overlay(use_trakt)
    except: pass
    return playcount, overlay, watched, unwatched

def get_watched_status_season(media_id, season, aired_eps):
    def get_playcount_overlay(use_trakt):
        try:
            if use_trakt:
                watched = [i[2] for i in watched_info if i[0] == media_id]
                if watched:
                    if len([i for i in watched[0] if i[0] == season]) == aired_eps:
                        playcount, overlay = 1, 7
            else:
                if watched_info == aired_eps and not aired_eps == 0:
                    playcount, overlay = 1, 7
        except: pass
        return playcount, overlay
    def get_watched_episode_totals(use_trakt):
        try:
            if use_trakt:
                watched = [i[2] for i in watched_info if i[0] == media_id]
                if watched:
                    watched = len([i for i in watched[0] if i[0] == season])
                unwatched = aired_eps - watched
            else:
                watched = watched_info
                unwatched = aired_eps - watched
        except: pass
        return watched, unwatched
    playcount, overlay = 0, 6
    watched, unwatched = 0, aired_eps
    try:
        if settings.watched_indicators() in (1, 2):
            from resources.lib.modules.trakt import trakt_indicators_tv
            use_trakt = True
            watched_info = trakt_indicators_tv()
        else:
            use_trakt = False
            settings.check_database(WATCHED_DB)
            dbcon = database.connect(WATCHED_DB)
            dbcur = dbcon.cursor()
            dbcur.execute("SELECT * FROM watched_status WHERE (db_type = ? and media_id = ? and season = ?)", ('episode', media_id, season))
            watched_info = len(dbcur.fetchall())
            dbcon.close()
        watched, unwatched = get_watched_episode_totals(use_trakt)
        playcount, overlay = get_playcount_overlay(use_trakt)
    except: pass
    return playcount, overlay, watched, unwatched

def get_watched_items(db_type, page_no, letter, passed_list=[]):
    import ast
    from resources.lib.modules.nav_utils import paginate_list
    from resources.lib.modules.utils import title_key, to_utf8
    watched_indicators = settings.watched_indicators()
    limit = 40
    if db_type == 'tvshow':
        from resources.lib.indexers.tvshows import aired_episode_number_tvshow
        if watched_indicators in (1, 2):
            if not passed_list:
                from resources.lib.modules.trakt import trakt_indicators_tv
                data = trakt_indicators_tv()
                data = sorted(data, key=lambda tup: title_key(tup[3]))
                original_list = [{'media_id': i[0], 'title': i[3]} for i in data if i[1] == len(i[2])]
            else: original_list = ast.literal_eval(passed_list)
        else:
            if not passed_list:
                from resources.lib.indexers.tvshows import make_fresh_tvshow_meta
                settings.check_database(WATCHED_DB)
                dbcon = database.connect(WATCHED_DB)
                dbcur = dbcon.cursor()
                dbcur.execute("SELECT media_id, title FROM watched_status WHERE db_type = ?", ('episode',))
                rows = dbcur.fetchall()
                dbcon.close()
                watched_list = list(set(to_utf8([(i[0], i[1]) for i in rows])))
                data = []
                for item in watched_list:
                    watched = get_watched_status_tvshow(item[0], aired_episode_number_tvshow(make_fresh_tvshow_meta('tmdb_id', item[0])))
                    if watched[0] == 1: data.append(item)
                    else: pass
                data = sorted(data, key=lambda tup: title_key(tup[1]))
                original_list = [{'media_id': i[0], 'title': i[1]} for i in data]
            else: original_list = ast.literal_eval(passed_list)
    else:
        if watched_indicators in (1, 2):
            if not passed_list:
                from resources.lib.modules.trakt import trakt_indicators_movies
                data = trakt_indicators_movies()
                data = sorted(data, key=lambda tup: title_key(tup[1]))
                original_list = [{'media_id': i[0], 'title': i[1]} for i in data]
            else: original_list = ast.literal_eval(passed_list)
            
        else:
            if not passed_list:
                settings.check_database(WATCHED_DB)
                dbcon = database.connect(WATCHED_DB)
                dbcur = dbcon.cursor()
                dbcur.execute("SELECT media_id, title FROM watched_status WHERE db_type = ?", (db_type,))
                rows = dbcur.fetchall()
                dbcon.close()
                data = to_utf8([(i[0], i[1]) for i in rows])
                data = sorted(data, key=lambda tup: title_key(tup[1]))
                original_list = [{'media_id': i[0], 'title': i[1]} for i in data]
            else: original_list = ast.literal_eval(passed_list)
    paginated_list, total_pages = paginate_list(original_list, page_no, letter, limit)
    return paginated_list, original_list, total_pages, limit

def mark_episode_as_watched_unwatched(params=None):
    from resources.lib.modules.next_episode import add_next_episode_unwatched
    params = dict(parse_qsl(sys.argv[2].replace('?',''))) if not params else params
    action = 'mark_as_watched' if params.get('action') == 'mark_as_watched' else 'mark_as_unwatched'
    media_id = params.get('media_id')
    tvdb_id = int(params.get('tvdb_id', '0'))
    imdb_id = params.get('imdb_id')
    season = int(params.get('season'))
    episode = int(params.get('episode'))
    title = params.get('title')
    year = params.get('year')
    from_search = params.get('from_search', 'false')
    watched_indicators = settings.watched_indicators()
    if season == 0:
        from resources.lib.modules.nav_utils import notification
        notification('Specials cannot be marked as %s' % ('Watched' if action == 'mark_as_watched' else 'Unwatched'), time=5000); return
    if watched_indicators in (1, 2):
        from resources.lib.modules.trakt import trakt_watched_unwatched
        trakt_watched_unwatched(action, 'episode', imdb_id, tvdb_id, season, episode)
        clear_trakt_watched_data('tvshow', imdb_id)
        erase_bookmark('episode', media_id, season, episode)
    if watched_indicators in (0, 1):
        mark_as_watched_unwatched('episode', media_id, action, season, episode, title)
    if action == 'mark_as_watched': add_next_episode_unwatched('remove', media_id, silent=True)
    if settings.sync_kodi_library_watchstatus():
        from resources.lib.modules.kodi_library import mark_as_watched_unwatched_kodi_library
        mark_as_watched_unwatched_kodi_library('episode', action, title, year, season, episode)
    refresh_container(from_search)

def mark_season_as_watched_unwatched():
    from resources.lib.modules.next_episode import add_next_episode_unwatched
    params = dict(parse_qsl(sys.argv[2].replace('?','')))
    action = 'mark_as_watched' if params.get('action') == 'mark_as_watched' else 'mark_as_unwatched'
    season = int(params.get('season'))
    title = params.get('title')
    year = params.get('year')
    media_id = params.get('media_id')
    tvdb_id = int(params.get('tvdb_id', '0'))
    imdb_id = params.get('imdb_id')
    watched_indicators = settings.watched_indicators()
    if season == 0:
        from resources.lib.modules.nav_utils import notification
        notification('Specials cannot be marked as %s' % ('Watched' if action == 'mark_as_watched' else 'Unwatched'), time=5000); return
    if watched_indicators in (1, 2):
        from resources.lib.modules.trakt import trakt_watched_unwatched
        trakt_watched_unwatched(action, 'season', imdb_id, tvdb_id, season)
        clear_trakt_watched_data('tvshow', imdb_id)
    if watched_indicators in (0, 1):
        import tikimeta
        bg_dialog = xbmcgui.DialogProgressBG()
        bg_dialog.create('Please Wait', '')
        infoLabels = tikimeta.season_episodes_meta(media_id, season)
        ep_data = infoLabels['episodes']
        count = 1
        se_list = []
        for item in ep_data:
            season_number = item['season_number']
            ep_number = item['episode_number']
            season_ep = '%.2d<>%.2d' % (season_number, ep_number)
            display = 'Updating - S%.2dE%.2d' % (season_number, ep_number)
            try:
                first_aired = item['air_date']
                d = first_aired.split('-')
                episode_date = date(int(d[0]), int(d[1]), int(d[2]))
            except: episode_date = date(2100,10,24)
            if not settings.adjusted_datetime() > episode_date: continue
            display = 'Updating - S%.2dE%.2d' % (season_number, ep_number)
            bg_dialog.update(int(float(count) / float(len(ep_data)) * 100), 'Please Wait', '%s' % display)
            count += 1
            mark_as_watched_unwatched('episode', media_id, action, season_number, ep_number, title)
            se_list.append(season_ep)
        bg_dialog.close()
    if action == 'mark_as_watched': add_next_episode_unwatched('remove', media_id, silent=True)
    if settings.sync_kodi_library_watchstatus():
        from resources.lib.modules.kodi_library import get_library_video, batch_mark_episodes_as_watched_unwatched_kodi_library
        in_library = get_library_video('tvshow', title, year)
        if not in_library: xbmc.executebuiltin("Container.Refresh"); return
        ep_dict = {'action': action, 'tvshowid': in_library['tvshowid'], 'season_ep_list': se_list}
        if batch_mark_episodes_as_watched_unwatched_kodi_library(in_library, ep_dict):
            from resources.lib.modules.nav_utils import notification
            notification('Kodi Library Sync Complete', time=5000)
    refresh_container()

def mark_tv_show_as_watched_unwatched():
    from resources.lib.modules.next_episode import add_next_episode_unwatched
    params = dict(parse_qsl(sys.argv[2].replace('?','')))
    action = 'mark_as_watched' if params.get('action') == 'mark_as_watched' else 'mark_as_unwatched'
    media_id = params.get('media_id')
    tvdb_id = int(params.get('tvdb_id', '0'))
    imdb_id = params.get('imdb_id')
    from_search = params.get('from_search', 'false')
    watched_indicators = settings.watched_indicators()
    if watched_indicators in (1, 2):
        from resources.lib.modules.trakt import trakt_watched_unwatched
        trakt_watched_unwatched(action, 'shows', imdb_id, tvdb_id)
        clear_trakt_watched_data('tvshow', imdb_id)
    if watched_indicators in (0, 1):
        import tikimeta
        from resources.lib.indexers.tvshows import make_fresh_tvshow_meta
        title = params.get('title', '')
        year = params.get('year', '')
        bg_dialog = xbmcgui.DialogProgressBG()
        bg_dialog.create('Please Wait', '')
        se_list = []
        count = 1
        s_data = make_fresh_tvshow_meta('tmdb_id', media_id)
        season_data = s_data['season_data']
        total = sum([i['episode_count'] for i in season_data if i['season_number'] > 0])
        for item in season_data:
            season_number = int(item['season_number'])
            if season_number <= 0: continue
            season_id = item['id']
            infoLabels = tikimeta.season_episodes_meta(media_id, season_number)
            ep_data = infoLabels['episodes']
            for item in ep_data:
                season_number = item['season_number']
                ep_number = item['episode_number']
                season_ep = '%.2d<>%.2d' % (int(season_number), int(ep_number))
                display = 'Updating - S%.2dE%.2d' % (int(season_number), int(ep_number))
                bg_dialog.update(int(float(count)/float(total)*100), 'Please Wait', '%s' % display)
                count += 1
                try:
                    first_aired = item['air_date']
                    d = first_aired.split('-')
                    episode_date = date(int(d[0]), int(d[1]), int(d[2]))
                except: episode_date = date(2100,10,24)
                if not settings.adjusted_datetime() > episode_date: continue
                mark_as_watched_unwatched('episode', media_id, action, season_number, ep_number, title)
                se_list.append(season_ep)
        bg_dialog.close()
    if action == 'mark_as_watched': add_next_episode_unwatched('remove', media_id, silent=True)
    if settings.sync_kodi_library_watchstatus():
        from resources.lib.modules.kodi_library import get_library_video, batch_mark_episodes_as_watched_unwatched_kodi_library
        in_library = get_library_video('tvshow', title, year)
        if not in_library: refresh_container(from_search); return
        from resources.lib.modules.nav_utils import notification
        notification('Browse back to Kodi Home Screen!!', time=7000)
        xbmc.sleep(8500)
        ep_dict = {'action': action, 'tvshowid': in_library['tvshowid'], 'season_ep_list': se_list}
        if batch_mark_episodes_as_watched_unwatched_kodi_library(in_library, ep_dict):
            notification('Kodi Library Sync Complete', time=5000)
    refresh_container(from_search)

def mark_movie_as_watched_unwatched(params=None):
    params = dict(parse_qsl(sys.argv[2].replace('?',''))) if not params else params
    action = params.get('action')
    db_type = 'movie'
    media_id = params.get('media_id')
    title = params.get('title')
    year = params.get('year')
    from_search = params.get('from_search', 'false')
    watched_indicators = settings.watched_indicators()
    if watched_indicators in (1, 2):
        from resources.lib.modules.trakt import trakt_watched_unwatched
        trakt_watched_unwatched(action, 'movies', media_id)
        clear_trakt_watched_data(db_type)
        erase_bookmark(db_type, media_id)
    if watched_indicators in (0, 1):
        mark_as_watched_unwatched(db_type, media_id, action, title=title)
    if settings.sync_kodi_library_watchstatus():
        from resources.lib.modules.kodi_library import mark_as_watched_unwatched_kodi_library
        mark_as_watched_unwatched_kodi_library(db_type, action, title, year)
    refresh_container(from_search)

def mark_as_watched_unwatched(db_type='', media_id='', action='', season='', episode='', title=''):
    try:
        settings.check_database(WATCHED_DB)
        last_played = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        dbcon = database.connect(WATCHED_DB, timeout=40.0)
        erase_bookmark(db_type, media_id, season, episode)
        if action == 'mark_as_watched':
            dbcon.execute("INSERT OR IGNORE INTO watched_status VALUES (?, ?, ?, ?, ?, ?)", (db_type, media_id, season, episode, last_played, to_unicode(title)))
        elif action == 'mark_as_unwatched':
            dbcon.execute("DELETE FROM watched_status WHERE (db_type = ? and media_id = ? and season = ? and episode = ?)", (db_type, media_id, season, episode))
        dbcon.commit()
    except:
        from resources.lib.modules.nav_utils import notification
        notification('Error Marking Watched in Fen', time=5000)

def refresh_container(from_search='false'):
    if from_search == 'true': return
    xbmc.executebuiltin("Container.Refresh")
