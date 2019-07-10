#!/usr/bin/python
# -*- coding: utf-8 -*-

'''provides a simple stateless caching system for Kodi addons and plugins'''

import xbmcvfs, xbmcgui, xbmc, xbmcaddon
import datetime
import time
import sqlite3
try: from sqlite3 import dbapi2 as database
except ImportError: from pysqlite2 import dbapi2 as database
from functools import reduce
from resources.lib.modules.utils import to_utf8
from resources.lib.modules import settings
# from resources.lib.modules.utils import logger

__addon_id__ = 'plugin.video.fen'
__addon__ = xbmcaddon.Addon(id=__addon_id__)
profile_dir = xbmc.translatePath(__addon__.getAddonInfo('profile'))
trakt_cache_file = xbmc.translatePath("%s/fen_trakt.db" % profile_dir).decode('utf-8')

window = xbmcgui.Window(10000)


class TraktCache(object):
    '''simple stateless caching system for Kodi'''
    _exit = False
    _auto_clean_interval = datetime.timedelta(hours=4)
    _win = None
    _busy_tasks = []
    _database = None

    def __init__(self):
        '''Initialize our caching class'''
        self._monitor = xbmc.Monitor()
        self.check_cleanup()

    def close(self):
        '''tell any tasks to stop immediately (as we can be called multithreaded) and cleanup objects'''
        self._exit = True
        # wait for all tasks to complete
        while self._busy_tasks:
            xbmc.sleep(25)
        del self._monitor
        self._log_msg("Closed")

    def __del__(self):
        '''make sure close is called'''
        if not self._exit:
            self.close()

    def get(self, endpoint):
        '''
            get object from cache and return the results
            endpoint: the (unique) name of the cache object as reference
        '''
        cur_time = self._get_timestamp(datetime.datetime.now())
        result = None
        # 1: try memory cache first
        result = self._get_mem_cache(endpoint, cur_time)
        # 2: fallback to _database cache
        if result is None:
            result = self._get_db_cache(endpoint, cur_time)

        return result

    def set(self, endpoint, data, expiration=datetime.timedelta(days=30)):
        '''
            set data in cache
        '''
        task_name = "set.%s" % endpoint
        self._busy_tasks.append(task_name)
        expires = self._get_timestamp(datetime.datetime.now() + expiration)

        # memory cache: write to window property
        self._set_mem_cache(endpoint, expires, data)

        # db cache
        if not self._exit:
            self._set_db_cache(endpoint, expires, data)

        # remove this task from list
        self._busy_tasks.remove(task_name)

    def check_cleanup(self):
        '''check if cleanup is needed - public method, may be called by calling addon'''
        cur_time = datetime.datetime.now()
        lastexecuted = window.getProperty("fen_trakt.clean.lastexecuted")
        if not lastexecuted:
            window.setProperty("fen_trakt.clean.lastexecuted", repr(cur_time))
        elif (eval(lastexecuted) + self._auto_clean_interval) < cur_time:
            # cleanup needed...
            self._do_cleanup()

    def _get_mem_cache(self, endpoint, cur_time):
        '''
            get cache data from memory cache
            we use window properties because we need to be stateless
        '''
        result = None
        cachedata = window.getProperty(endpoint.encode("utf-8"))
        if cachedata:
            cachedata = eval(cachedata)
            if cachedata[0] > cur_time:
                result = cachedata[1]
        return result

    def _set_mem_cache(self, endpoint, expires, data):
        '''
            window property cache as alternative for memory cache
            usefull for (stateless) plugins
        '''
        cachedata = (expires, data)
        cachedata_str = repr(cachedata).encode("utf-8")
        window.setProperty(endpoint.encode("utf-8"), cachedata_str)

    def _get_db_cache(self, endpoint, cur_time):
        '''get cache data from sqllite _database'''
        result = None
        query = "SELECT expires, data FROM fen_trakt WHERE id = ?"
        cache_data = self._execute_sql(query, (endpoint,))
        if cache_data:
            cache_data = cache_data.fetchone()
            if cache_data and cache_data[0] > cur_time:
                result = eval(cache_data[1])
                # also set result in memory cache for further access
                self._set_mem_cache(endpoint, cache_data[0], result)
        return result

    def _set_db_cache(self, endpoint, expires, data):
        ''' store cache data in _database '''
        query = "INSERT OR REPLACE INTO fen_trakt(id, expires, data) VALUES (?, ?, ?)"
        data = repr(data)
        self._execute_sql(query, (endpoint, expires, data))

    def _do_cleanup(self):
        '''perform cleanup task'''
        if self._exit or self._monitor.abortRequested():
            return
        self._busy_tasks.append(__name__)
        cur_time = datetime.datetime.now()
        cur_timestamp = self._get_timestamp(cur_time)
        self._log_msg("Running cleanup...")
        if window.getProperty("fentraktcachecleanbusy"):
            return
        window.setProperty("fentraktcachecleanbusy", "busy")

        query = "SELECT id, expires FROM fen_trakt"
        for cache_data in self._execute_sql(query).fetchall():
            if self._exit or self._monitor.abortRequested():
                return
            # always cleanup all memory objects on each interval
            window.clearProperty(cache_data[0].encode("utf-8"))
            # clean up db cache object only if expired
            if cache_data[1] < cur_timestamp:
                query = 'DELETE FROM fen_trakt WHERE id = ?'
                self._execute_sql(query, (cache_data[0],))
                self._log_msg("delete from db %s" % cache_data[0])

        # compact db
        self._execute_sql("VACUUM")

        # remove task from list
        self._busy_tasks.remove(__name__)
        window.setProperty("fen_trakt.clean.lastexecuted", repr(cur_time))
        window.clearProperty("fentraktcachecleanbusy")
        self._log_msg("Auto cleanup done")

    def _get_database(self):
        '''get reference to our sqllite _database - performs basic integrity check'''
        if not xbmcvfs.exists(profile_dir):
            xbmcvfs.mkdirs(profile_dir)
        try:
            connection = sqlite3.connect(trakt_cache_file, timeout=30, isolation_level=None)
            connection.execute('SELECT * FROM fen_trakt LIMIT 1')
            return connection
        except Exception as error:
            # our _database is corrupt or doesn't exist yet, we simply try to recreate it
            if xbmcvfs.exists(trakt_cache_file):
                xbmcvfs.delete(trakt_cache_file)
            try:
                connection = sqlite3.connect(trakt_cache_file, timeout=30, isolation_level=None)
                connection.execute(
                    """CREATE TABLE IF NOT EXISTS fen_trakt(
                    id TEXT UNIQUE, expires INTEGER, data TEXT)""")
                return connection
            except Exception as error:
                self._log_msg("Exception while initializing _database: %s" % str(error), xbmc.LOGWARNING)
                self.close()
                return None

    def _execute_sql(self, query, data=None):
        '''little wrapper around execute and executemany to just retry a db command if db is locked'''
        retries = 0
        result = None
        error = None
        with self._get_database() as _database:
            while not retries == 10:
                if self._exit:
                    return None
                try:
                    if isinstance(data, list):
                        result = _database.executemany(query, data)
                    elif data:
                        result = _database.execute(query, data)
                    else:
                        result = _database.execute(query)
                    return result
                except sqlite3.OperationalError as error:
                    if "_database is locked" in error:
                        self._log_msg("retrying DB commit...")
                        retries += 1
                        self._monitor.waitForAbort(0.5)
                    else:
                        break
                except Exception as error:
                    break
            self._log_msg("_database ERROR ! -- %s" % str(error), xbmc.LOGWARNING)
        return None

    @staticmethod
    def _log_msg(msg, loglevel=xbmc.LOGDEBUG):
        '''helper to send a message to the kodi log'''
        if isinstance(msg, unicode):
            msg = msg.encode('utf-8')
        xbmc.log("Fen Trakt Cache --> %s" % msg, level=loglevel)

    @staticmethod
    def _get_timestamp(date_time):
        '''Converts a datetime object to unix timestamp'''
        return int(time.mktime(date_time.timetuple()))

def cache_trakt_object(function, string, url):
    _cache = TraktCache()
    cache = _cache.get(string)
    if cache: return to_utf8(cache)
    result = function(url)
    _cache.set(string, result, expiration=datetime.timedelta(hours=settings.trakt_cache_duration()))
    return to_utf8(result)

def clear_trakt_watched_data(db_type, media_id=None):
    settings.check_database(trakt_cache_file)
    dbcon = database.connect(trakt_cache_file)
    dbcur = dbcon.cursor()
    if db_type == 'tvshow':
        clear_trakt_next_episode_data(media_id)
        dbcur.execute("DELETE FROM fen_trakt WHERE id=?", ('trakt_watched_shows',))
        dbcon.commit()
        window.clearProperty('trakt_watched_shows')
    action = 'trakt_indicators_movies' if db_type in ('movie', 'movies') else 'trakt_indicators_tv'
    dbcur.execute("DELETE FROM fen_trakt WHERE id=?", (action,))
    dbcon.commit()
    window.clearProperty(action)

def clear_trakt_next_episode_data(media_id=None):
    settings.check_database(trakt_cache_file)
    try:
        dbcon = database.connect(trakt_cache_file)
        dbcur = dbcon.cursor()
        dbcur.execute("SELECT * FROM fen_trakt WHERE id = ?", ('trakt_watched_shows',))
        shows = dbcur.fetchone()[2]
        shows = eval(shows)
        show_ids = [i['show']['ids'] for i in shows]
    except: return
    if media_id:
        try:
            trakt_id = [i['trakt'] for i in show_ids if i['imdb'] == media_id][0]
            dbcur.execute("DELETE FROM fen_trakt WHERE id=?", ('trakt_view_history_%s' % str(trakt_id),))
            dbcon.commit()
            window.clearProperty('trakt_view_history_%s' % str(trakt_id))
        except: pass
        return
    if not media_id:
        trakt_ids = [i['trakt'] for i in show_ids]
        dbcur.execute("DELETE FROM fen_trakt WHERE id LIKE 'trakt_view_history%'")
        dbcon.commit()
        for i in trakt_ids: window.clearProperty('trakt_view_history_%s' % str(i))

def clear_trakt_hidden_data(list_type):
    settings.check_database(trakt_cache_file)
    action = 'trakt_hidden_items_%s' % list_type
    try:
        dbcon = database.connect(trakt_cache_file)
        dbcur = dbcon.cursor()
        dbcur.execute("DELETE FROM fen_trakt WHERE id=?", (action,))
        dbcon.commit()
        window.clearProperty(action)
    except: pass

def clear_trakt_collection_watchlist_data(list_type, db_type):
    settings.check_database(trakt_cache_file)
    action = 'trakt_collection_%s' % db_type if list_type == 'collection' else 'trakt_watchlist_%s' % db_type
    try:
        dbcon = database.connect(trakt_cache_file)
        dbcur = dbcon.cursor()
        dbcur.execute("DELETE FROM fen_trakt WHERE id=?", (action,))
        dbcon.commit()
        window.clearProperty(action)
        window.setProperty('trakt_reset_passed_list', 'true')
    except: pass

def clear_trakt_list_contents_data(clear_all=False, user=None, slug=None):
    from resources.lib.modules.trakt import get_trakt_my_lists, get_trakt_liked_lists
    settings.check_database(trakt_cache_file)
    if clear_all:
        my_lists = [(item["user"]["username"], item["ids"]["slug"]) for item in get_trakt_my_lists(build_list=False)]
        liked_lists = [(item["list"]["user"]["username"], item["list"]["ids"]["slug"]) for item in get_trakt_liked_lists(build_list=False)]
        my_lists.extend(liked_lists)
        try:
            dbcon = database.connect(trakt_cache_file)
            dbcur = dbcon.cursor()
            dbcur.execute("DELETE FROM fen_trakt WHERE id LIKE 'trakt_list_contents%'")
            dbcon.commit()
        except: pass
        for i in my_lists: window.clearProperty('trakt_list_contents_%s_%s' % (i[0], i[1]))
    else:
        action = 'trakt_list_contents_%s_%s' % (user, slug)
        try:
            dbcon = database.connect(trakt_cache_file)
            dbcur = dbcon.cursor()
            dbcur.execute("DELETE FROM fen_trakt WHERE id=?", (action,))
            dbcon.commit()
            window.clearProperty(action)
            window.setProperty('trakt_reset_passed_list', 'true')
        except: pass

def clear_trakt_list_data(list_type):
    settings.check_database(trakt_cache_file)
    action = 'trakt_my_lists' if list_type == 'my_lists' else 'trakt_liked_lists'
    try:
        dbcon = database.connect(trakt_cache_file)
        dbcur = dbcon.cursor()
        dbcur.execute("DELETE FROM fen_trakt WHERE id=?", (action,))
        dbcon.commit()
        window.clearProperty(action)
    except: pass

def clear_all_trakt_cache_data(list_type='progress_watched'):
    try:
        if not xbmcgui.Dialog().yesno('Are you sure?','Fen will Clear the Trakt Cache.'):
            return False
        try: clear_trakt_hidden_data(list_type)
        except: pass
        for i in ('movie', 'tvshow'):
            try: clear_trakt_watched_data(i)
            except: pass
            for j in ('collection', 'watchlist'):
                try: clear_trakt_collection_watchlist_data(j, i)
                except: pass
        try: clear_trakt_list_contents_data(clear_all=True)
        except: pass
        for i in ('my_lists', 'liked_lists'):
            try: clear_trakt_list_data(i)
            except: pass
        return True
    except:
        return False
