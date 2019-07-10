#!/usr/bin/python
# -*- coding: utf-8 -*-

import xbmc, xbmcvfs
import os
import datetime
import time
import sqlite3 as database
# from tikimeta.utils import logger


class MetaCache():
    def __init__(self):
        self.datapath = xbmc.translatePath("special://userdata/addon_data/script.module.tikimeta")
        self.dbfile = os.path.join(self.datapath, "metacache.db")
        self._check_database()

    def get(self, db_type, id_type, media_id, season_no=None):
        result = None
        try:
            current_time = self._get_timestamp(datetime.datetime.now())
            dbcon = database.connect(self.dbfile)
            dbcur = dbcon.cursor()
            if db_type in ('movie', 'tvshow'):
                dbcur.execute("SELECT meta, expires FROM metadata WHERE db_type = ? AND %s = ?" % id_type, (str(db_type), str(media_id)))
            else:
                dbcur.execute("SELECT meta, expires FROM season_metadata WHERE tmdb_id = ? AND season_no = ?", (str(media_id), str(season_no)))
            cache_data = dbcur.fetchone()
            if cache_data:
                if cache_data[1] > current_time:
                    result = eval(cache_data[0])
                else:
                    if db_type in ('movie', 'tvshow'):
                        dbcur.execute("DELETE FROM metadata WHERE db_type = ? AND %s = ?" % id_type, (str(db_type), str(media_id)))
                    else:
                        dbcur.execute("DELETE FROM season_metadata WHERE tmdb_id = ? AND season_no = ?", (str(media_id), str(season_no)))
                    dbcon.commit()
                    dbcon.close()
        except: pass
        return result

    def set(self, db_type, meta, expiration=datetime.timedelta(days=30), season_no=None):
        try:
            expires = self._get_timestamp(datetime.datetime.now() + expiration)
            dbcon = database.connect(self.dbfile)
            dbcur = dbcon.cursor()
            if db_type in ('movie', 'tvshow'):
                dbcur.execute("INSERT INTO metadata VALUES (?, ?, ?, ?, ?, ?)", (str(db_type), str(meta['tmdb_id']), str(meta['imdb_id']), str(meta['tvdb_id']), repr(meta), int(expires)))
            else:
                dbcur.execute("INSERT INTO season_metadata VALUES (?, ?, ?, ?)", (str(meta['tmdb_id']), str(season_no), repr(meta), int(expires)))
            dbcon.commit()
            dbcon.close()
        except: return

    def get_function(self, string):
        self._check_function_cache_table()
        result = None
        try:
            current_time = self._get_timestamp(datetime.datetime.now())
            dbcon = database.connect(self.dbfile)
            dbcur = dbcon.cursor()
            dbcur.execute("SELECT string_id, data, expires FROM function_cache WHERE string_id = ?", (string,))
            cache_data = dbcur.fetchone()
            if cache_data:
                if cache_data[2] > current_time:
                    result = eval(cache_data[1])
                else:
                    dbcur.execute("DELETE FROM function_cache WHERE string_id = ?", (string,))
                    dbcon.commit()
                    dbcon.close()
        except: pass
        return result

    def set_function(self, string, result, expiration=datetime.timedelta(days=1)):
        self._check_function_cache_table()
        try:
            expires = self._get_timestamp(datetime.datetime.now() + expiration)
            dbcon = database.connect(self.dbfile)
            dbcur = dbcon.cursor()
            dbcur.execute("INSERT INTO function_cache VALUES (?, ?, ?)", (string, repr(result), int(expires)))
            dbcon.commit()
            dbcon.close()
        except: return

    def delete(self, db_type, id_type, media_id):
        self._check_function_cache_table()
        try:
            dbcon = database.connect(self.dbfile)
            dbcur = dbcon.cursor()
            dbcur.execute("DELETE FROM metadata WHERE db_type = ? AND %s = ?" % id_type, (str(db_type), str(media_id)))
            if db_type == 'tvshow':
                dbcur.execute("DELETE FROM season_metadata WHERE tmdb_id = ?", (str(media_id),))
            dbcon.commit()
            dbcon.close()
        except: return

    def delete_all(self):
        self._check_function_cache_table()
        dbcon = database.connect(self.dbfile)
        dbcur = dbcon.cursor()
        for i in ('metadata', 'season_metadata', 'function_cache'):
            dbcur.execute("DELETE FROM %s" % i)
        dbcur.execute("VACUUM")
        dbcon.commit()
        dbcon.close()

    def _check_database(self):
        if not xbmcvfs.exists(self.datapath):
            xbmcvfs.mkdirs(self.datapath)
        if not xbmcvfs.exists(self.dbfile):
            dbcon = database.connect(self.dbfile)
            self._check_metadata_cache_table(dbcon)
            self._check_season_metadata_cache_table(dbcon)
            self._check_function_cache_table(dbcon)
            dbcon.close()

    def _check_metadata_cache_table(self, dbcon=None):
        if not dbcon: dbcon = database.connect(self.dbfile)
        dbcon.execute("""CREATE TABLE IF NOT EXISTS metadata
                          (db_type text not null, tmdb_id text not null, imdb_id text, tvdb_id text,
                          meta text, expires integer, unique (db_type, tmdb_id))
                       """)

    def _check_season_metadata_cache_table(self, dbcon=None):
        if not dbcon: dbcon = database.connect(self.dbfile)
        dbcon.execute("""CREATE TABLE IF NOT EXISTS season_metadata
                          (tmdb_id text not null, season_no text not null, meta text,
                          expires integer, unique (tmdb_id, season_no))
                       """)

    def _check_function_cache_table(self, dbcon=None):
        if not dbcon: dbcon = database.connect(self.dbfile)
        dbcon.execute("""CREATE TABLE IF NOT EXISTS function_cache
                         (string_id text not null, data text,
                         expires integer, unique (string_id))
                      """)

    def _get_timestamp(self, date_time):
        return int(time.mktime(date_time.timetuple()))

