import xbmc, xbmcaddon, xbmcgui, xbmcplugin
import os, sys
from resources.lib.modules.nav_utils import setView
from resources.lib.indexers.tvshows import build_episode, aired_episode_number_tvshow
import settings
try:
    from sqlite3 import dbapi2 as database
except ImportError:
    from pysqlite2 import dbapi2 as database
# from resources.lib.modules.utils import logger

__addon_id__ = 'plugin.video.fen'
__addon__ = xbmcaddon.Addon(id=__addon_id__)
addon_dir = xbmc.translatePath(__addon__.getAddonInfo('path'))
__addon_profile__ = xbmc.translatePath(__addon__.getAddonInfo('profile'))
__url__ = sys.argv[0]
__handle__ = int(sys.argv[1])

WATCHED_DB = os.path.join(__addon_profile__, 'watched_status.db')

def in_progress_movie(db_type=None):
    settings.check_database(WATCHED_DB)
    dbcon = database.connect(WATCHED_DB)
    dbcur = dbcon.cursor()
    dbcur.execute('''SELECT media_id FROM progress WHERE db_type=?''', ('movie',))
    rows = dbcur.fetchall()
    return [i[0] for i in rows if not i[0] == '']

def in_progress_tvshow(db_type=None):
    from resources.lib.indexers.tvshows import make_fresh_tvshow_meta
    items = []
    if settings.watched_indicators() in (1, 2):
        from resources.lib.modules.trakt import trakt_indicators_tv
        items = trakt_indicators_tv()
        items = [i[0] for i in items if not i[1] == len(i[2])]
    else:
        settings.check_database(WATCHED_DB)
        from resources.lib.modules.indicators_bookmarks import get_watched_status_tvshow
        dbcon = database.connect(WATCHED_DB)
        dbcur = dbcon.cursor()
        dbcur.execute('''SELECT media_id FROM watched_status WHERE db_type=?''', ('episode',))
        rows1 = dbcur.fetchall()
        in_progress_result = list(set([i[0] for i in rows1]))
        for i in in_progress_result:
            meta = make_fresh_tvshow_meta('tmdb_id', i)
            watched_status = get_watched_status_tvshow(meta['tmdb_id'], aired_episode_number_tvshow(meta))
            if not watched_status[0] == 1: items.append(i)
    return items

def build_in_progress_episode():
    from resources.lib.indexers.tvshows import make_fresh_tvshow_meta
    from resources.lib.modules.workers import Thread
    def process_eps(item):
        listitem = build_episode({"season": int(item[1]), "episode": int(item[2]), "meta": make_fresh_tvshow_meta('tmdb_id', item[0])})['listitem']
        xbmcplugin.addDirectoryItem(__handle__, listitem[0], listitem[1], isFolder=listitem[2])
    settings.check_database(WATCHED_DB)
    threads = []
    dbcon = database.connect(WATCHED_DB)
    dbcur = dbcon.cursor()
    dbcur.execute('''SELECT media_id, season, episode FROM progress WHERE db_type=?''', ('episode',))
    rows = dbcur.fetchall()
    for item in rows: threads.append(Thread(process_eps, item))
    [i.start() for i in threads]
    [i.join() for i in threads]
    xbmcplugin.setContent(__handle__, 'episodes')
    xbmcplugin.endOfDirectory(__handle__)
    setView('view.progress_next_episode')

    