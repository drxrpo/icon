# -*- coding: utf-8 -*-
#
#      Copyright (C) 2013 Tommy Winther
#      http://tommy.winther.nu
#
#      Modified for FTV Guide (09/2014 onwards)
#      by Thomas Geppert [bluezed] - bluezed.apps@gmail.com
#
#      Modified for TV Guide Fullscreen (2016)
#      by primaeval - primaeval.dev@gmail.com
#
#  This Program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2, or (at your option)
#  any later version.
#
#  This Program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this Program; see the file LICENSE.txt.  If not, write to
#  the Free Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.
#  http://www.gnu.org/copyleft/gpl.html
#

import os
import threading
import datetime
from dateutil import tz
import time
from xml.etree import ElementTree
import re

from strings import *
#from guideTypes import *
from fileFetcher import *

import xbmc
import xbmcgui
import xbmcvfs
import xbmcaddon
import sqlite3
import HTMLParser
import xml.etree.ElementTree as ET
import requests
from itertools import chain

import resources.lib.pytz as pytz

from resources.lib.pytz import timezone
try:
    import dateutil.parser
except:
    xbmc.log('[script.tvguide.Vader] ...failed to load dateutil try local', xbmc.LOGNOTICE)
    import resources.lib.dateutil.parser


import traceback
import calendar

import sys
# sys.setdefaultencoding() does not exist, here!
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')


from sdAPI import SdAPI
from utils import *

SETTINGS_TO_CHECK = ['source', 'xmltv.type', 'xmltv.file', 'xmltv.url', 'xmltv.logo.folder', 'logos.source', 'logos.folder', 'logos.url', 'source.source', 'yo.countries' , 'tvguide.co.uk.systemid']


def UTCToLocal(utc_dt):
    # get integer timestamp to avoid precision lost
    timestamp = calendar.timegm(utc_dt.timetuple())
    local_dt = datetime.datetime.fromtimestamp(timestamp)
    assert utc_dt.resolution >= datetime.timedelta(microseconds=1)
    return local_dt.replace(microsecond=utc_dt.microsecond)

def log(x):
    xbmc.log(repr(x))


class SourceException(Exception):
    pass


class SourceUpdateCanceledException(SourceException):
    pass


class SourceNotConfiguredException(SourceException):
    pass


class DatabaseSchemaException(sqlite3.DatabaseError):
    pass


class Database(object):
    SOURCE_DB = 'source.db'
    CHANNELS_PER_PAGE = int(ADDON.getSetting('channels.per.page'))

    def __init__(self,force=False):
        xbmc.log('[script.tvguide.Vader] ...database started', xbmc.LOGNOTICE)

        self.conn = None
        self.eventQueue = list()
        self.event = threading.Event()
        self.eventResults = dict()
        self.force = force

        self.source = instantiateSource(force)

        self.updateInProgress = False
        self.updateFailed = False
        self.settingsChanged = None
        self.alreadyTriedUnlinking = False
        self.channelList = list()
        self.category = "Any"

        profilePath = xbmc.translatePath(ADDON.getAddonInfo('profile'))
        if not os.path.exists(profilePath):
            os.makedirs(profilePath)
        self.databasePath = os.path.join(profilePath, Database.SOURCE_DB)

        threading.Thread(name='Database Event Loop', target=self.eventLoop).start()


    def eventLoop(self):
        print 'Database.eventLoop() >>>>>>>>>> starting...'
        while True:
            self.event.wait()
            self.event.clear()

            event = self.eventQueue.pop(0)

            command = event[0]
            callback = event[1]

            print 'Database.eventLoop() >>>>>>>>>> processing command: ' + command.__name__

            try:
                result = command(*event[2:])
                self.eventResults[command.__name__] = result

                if callback:
                    if self._initialize == command:
                        threading.Thread(name='Database callback', target=callback, args=[result]).start()
                    else:
                        threading.Thread(name='Database callback', target=callback).start()

                if self._close == command:
                    del self.eventQueue[:]
                    break

            except Exception as detail:
                xbmc.log('Database.eventLoop() >>>>>>>>>> exception! %s = %s' % (detail,command.__name__), xbmc.LOGERROR)
                if str(detail) in 'database disk image is malformed':
                    import ResetDatabase, sys
                    ResetDatabase.deleteDB()
                    sys.exit()

                xbmc.executebuiltin("ActivateWindow(Home)")

        print 'Database.eventLoop() >>>>>>>>>> exiting...'

    def _invokeAndBlockForResult(self, method, *args):
        sqlite3.register_adapter(datetime.datetime, self.adapt_datetime)
        sqlite3.register_converter('timestamp', self.convert_datetime)
        event = [method, None]
        event.extend(args)
        self.eventQueue.append(event)
        self.event.set()
        while not method.__name__ in self.eventResults:
            time.sleep(0.02)
        result = self.eventResults.get(method.__name__)
        del self.eventResults[method.__name__]
        return result

    def initialize(self, callback, cancel_requested_callback=None):
        self.eventQueue.append([self._initialize, callback, cancel_requested_callback])
        self.event.set()

    def _initialize(self, cancel_requested_callback):
        sqlite3.register_adapter(datetime.datetime, self.adapt_datetime)
        sqlite3.register_converter('timestamp', self.convert_datetime)

        self.alreadyTriedUnlinking = False
        while True:
            if cancel_requested_callback is not None and cancel_requested_callback():
                break

            try:
                self.conn = sqlite3.connect(self.databasePath, detect_types=sqlite3.PARSE_DECLTYPES)
                self.conn.execute('PRAGMA foreign_keys = ON')
                self.conn.row_factory = sqlite3.Row

                # create and drop dummy table to check if database is locked
                c = self.conn.cursor()
                c.execute('CREATE TABLE IF NOT EXISTS database_lock_check(id TEXT PRIMARY KEY)')
                c.execute('DROP TABLE database_lock_check')
                c.close()

                self._createTables()
                self.settingsChanged = self._wasSettingsChanged(ADDON)
                break

            except sqlite3.OperationalError:
                if cancel_requested_callback is None:
                    xbmc.log('[script.tvguide.Vader] Database is locked, bailing out...', xbmc.LOGDEBUG)
                    break
                else:  # ignore 'database is locked'
                    xbmc.log('[script.tvguide.Vader] Database is locked, retrying...', xbmc.LOGDEBUG)

            except sqlite3.DatabaseError:
                self.conn = None
                if self.alreadyTriedUnlinking:
                    xbmc.log('[script.tvguide.Vader] Database is broken and unlink() failed', xbmc.LOGDEBUG)
                    break
                else:
                    try:
                        os.unlink(self.databasePath)
                    except OSError:
                        pass
                    self.alreadyTriedUnlinking = True
                    xbmcgui.Dialog().ok(ADDON.getAddonInfo('name'), strings(DATABASE_SCHEMA_ERROR_1),
                                        strings(DATABASE_SCHEMA_ERROR_2), strings(DATABASE_SCHEMA_ERROR_3))

        return self.conn is not None

    def close(self, callback=None):
        self.eventQueue.append([self._close, callback])
        self.event.set()

    def _close(self):
        try:
            # rollback any non-commit'ed changes to avoid database lock
            if self.conn:
                self.conn.rollback()
        except sqlite3.OperationalError:
            pass  # no transaction is active
        if self.conn:
            self.conn.close()

    def _wasSettingsChanged(self, addon):
        #gType = GuideTypes()
        #if int(addon.getSetting('xmltv.type')) == gType.CUSTOM_FILE_ID:
        #    settingsChanged = addon.getSetting('xmltv.refresh') == 'true'
        #else:
        settingsChanged = False
        noRows = True
        count = 0
        settingsChanged = addon.getSetting('xmltv.refresh') == 'true'

        c = self.conn.cursor()
        c.execute('SELECT * FROM settings')
        for row in c:
            noRows = False
            key = row['key']
            if SETTINGS_TO_CHECK.count(key):
                count += 1
                if row['value'] != addon.getSetting(key):
                    settingsChanged = True

        if count != len(SETTINGS_TO_CHECK):
            settingsChanged = True

        if settingsChanged or noRows:
            for key in SETTINGS_TO_CHECK:
                value = addon.getSetting(key)
                if value:
                    value = value.decode('utf-8', 'ignore')
                c.execute('INSERT OR IGNORE INTO settings(key, value) VALUES (?, ?)', [key, value])
                if not c.rowcount:
                    c.execute('UPDATE settings SET value=? WHERE key=?', [value, key])
            self.conn.commit()

        c.close()
        print 'Settings changed: ' + str(settingsChanged)
        return settingsChanged

    def _isCacheExpired(self, date):
        programsLastUpdated = None

        if self.settingsChanged:
            return True

        # check if channel data is up-to-date in database
        try:
            c = self.conn.cursor()
            c.execute('SELECT channels_updated FROM sources WHERE id=?', [self.source.KEY])
            row = c.fetchone()
            if not row:
                return True
            channelsLastUpdated = row['channels_updated']
            c.close()
        except TypeError:
            return True


        # check if program data is up-to-date in database
        dateStr = date.strftime('%Y-%m-%d')
        c = self.conn.cursor()
        #c.execute('SELECT programs_updated FROM updates WHERE source=? AND date=?', [self.source.KEY, dateStr])
        c.execute('SELECT programs_updated FROM updates WHERE source=?', [self.source.KEY])
        row = c.fetchone()
        if row:
            programsLastUpdated = row['programs_updated']
        else:
            programsLastUpdated = datetime.datetime.fromtimestamp(0)
        c.close()


        return self.source.isUpdated(channelsLastUpdated, programsLastUpdated)


    def updateChannelAndProgramListCaches(self, callback, date=datetime.datetime.now(), progress_callback=None,
                                          clearExistingProgramList=True):
        self.eventQueue.append(
            [self._updateChannelAndProgramListCaches, callback, date, progress_callback, clearExistingProgramList])
        self.event.set()

    def _updateChannelAndProgramListCaches(self, date, progress_callback, clearExistingProgramList):
        # todo workaround service.py 'forgets' the adapter and convert set in _initialize.. wtf?!

        sqlite3.register_adapter(datetime.datetime, self.adapt_datetime)
        sqlite3.register_converter('timestamp', self.convert_datetime)

        lock = 'special://profile/addon_data/script.tvguide.Vader/db.lock'
        if xbmcvfs.exists(lock):
            xbmc.log('[script.tvguide.Vader] db currently locked...', xbmc.LOGDEBUG)

            return
        xbmc.log('[script.tvguide.Vader] Updating chan & programs ...', xbmc.LOGDEBUG)

        isCacheExpired = self._isCacheExpired(date)
        needReset = self.source.needReset
        ch_list = self._getChannelList(onlyVisible=False)
        if len(ch_list) == 0:
            needReset = True

        if not isCacheExpired and not needReset and not self.force:
            return
        else:
            # if the xmltv data needs to be loaded the database
            # should be reset to avoid ghosting!
            self.updateInProgress = True
            c = self.conn.cursor()
            c.execute("DELETE FROM updates")
            c.execute("UPDATE sources SET channels_updated=0")
            self.conn.commit()
            c.close()
            self.source.needReset = False
        xbmcvfs.File(lock,'wb')
        self.updateInProgress = True
        self.updateFailed = False
        dateStr = date.strftime('%Y-%m-%d')
        c = self.conn.cursor()
        try:
            xbmc.log('[script.tvguide.Vader] Updating caches...', xbmc.LOGDEBUG)
            if progress_callback:
                progress_callback(0)

            getData = True
            ch_list = []
            if self.source.KEY == "sdirect":
                ch_list = self._getChannelList(onlyVisible=False)
                if len(ch_list) == 0:
                    getData = False
            else:
                ch_list = self._getChannelList(onlyVisible=True)

            if self.settingsChanged:
                c.execute('DELETE FROM channels WHERE source=?', [self.source.KEY])
                c.execute('DELETE FROM programs WHERE source=?', [self.source.KEY])
                c.execute("DELETE FROM updates WHERE source=?", [self.source.KEY])
            self.settingsChanged = False  # only want to update once due to changed settings

            if clearExistingProgramList:
                c.execute("DELETE FROM updates WHERE source=?",
                          [self.source.KEY])  # cascades and deletes associated programs records
            else:
                c.execute("DELETE FROM updates WHERE source=? AND date=?",
                          [self.source.KEY, dateStr])  # cascades and deletes associated programs records

            # programs updated
            c.execute("INSERT INTO updates(source, date, programs_updated) VALUES(?, ?, ?)",
                      [self.source.KEY, dateStr, datetime.datetime.now()])
            updatesId = c.lastrowid

            imported = imported_channels = imported_programs = 0

            if getData == True:
                xbmcvfs.delete('special://profile/addon_data/script.tvguide.Vader/category_count.ini')
                catchup = ADDON.getSetting('catchup.text')
                channel = Channel("catchup", catchup, '', "special://home/addons/plugin.video.%s/icon.png" % catchup.lower(), "catchup", ADDON.getSetting('catchup.channel') == 'true')
                c.execute(
                    'INSERT OR IGNORE INTO channels(id, title, logo, stream_url, visible, weight, source) VALUES(?, ?, ?, ?, ?, (CASE ? WHEN -1 THEN (SELECT COALESCE(MAX(weight)+1, 0) FROM channels WHERE source=?) ELSE ? END), ?)',
                    [channel.id, channel.title, channel.logo, channel.streamUrl, channel.visible, channel.weight,
                     self.source.KEY, channel.weight, self.source.KEY])
                for item in self.source.getDataFromExternal(date, ch_list, progress_callback):
                    # xbmc.log('[script.tvguide.Vader] ...' + str(self.source.KEY)  + '... ' + str(), xbmc.LOGNOTICE)

                    imported += 1

                    if imported % 10000 == 0:
                        try:
                            self.conn.commit()
                        except:
                            import traceback
                            xbmc.log('[script.tvguide.Vader] ' + str(item), xbmc.LOGNOTICE)
                            tb = traceback.format_exc()
                            xbmc.log('[script.tvguide.Vader] ' + str(tb), xbmc.LOGNOTICE)
                            break


                    if isinstance(item, Channel):
                        imported_channels += 1
                        channel = item
                        c.execute(
                            'INSERT OR IGNORE INTO channels(id, title, logo, stream_url, visible, weight, source) VALUES(?, ?, ?, ?, ?, (CASE ? WHEN -1 THEN (SELECT COALESCE(MAX(weight)+1, 0) FROM channels WHERE source=?) ELSE ? END), ?)',
                            [channel.id, channel.title, channel.logo, channel.streamUrl, channel.visible, channel.weight,
                             self.source.KEY, channel.weight, self.source.KEY])
                        if not c.rowcount:
                            if ADDON.getSetting('logos.keep') == 'true':
                                c.execute(
                                    'UPDATE channels SET title=?, stream_url=?, visible=(CASE ? WHEN -1 THEN visible ELSE ? END), weight=(CASE ? WHEN -1 THEN weight ELSE ? END) WHERE id=? AND source=?',
                                    [channel.title, channel.streamUrl, channel.weight, channel.visible,
                                     channel.weight, channel.weight, channel.id, self.source.KEY])
                            else:
                                c.execute(
                                    'UPDATE channels SET title=?, logo=?, stream_url=?, visible=(CASE ? WHEN -1 THEN visible ELSE ? END), weight=(CASE ? WHEN -1 THEN weight ELSE ? END) WHERE id=? AND source=?',
                                    [channel.title, channel.logo, channel.streamUrl, channel.weight, channel.visible,
                                     channel.weight, channel.weight, channel.id, self.source.KEY])

                    elif isinstance(item, Program):
                        imported_programs += 1
                        program = item
                        if isinstance(program.channel, Channel):
                            channel = program.channel.id
                        else:
                            channel = program.channel
                        try:
                            c.execute(
                            'INSERT OR REPLACE INTO programs(channel, title, sub_title, start_date, end_date, description, categories, image_large, image_small, season, episode, is_movie, language, source, updates_id) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                            [channel, program.title, program.sub_title, program.startDate, program.endDate, program.description, program.categories,
                             program.imageLarge, program.imageSmall, program.season, program.episode, program.is_movie,
                             program.language, self.source.KEY, updatesId])
                        except:
                            import traceback
                            xbmc.log('[script.tvguide.Vader] ' + str(item), xbmc.LOGNOTICE)
                            tb = traceback.format_exc()
                            xbmc.log('[script.tvguide.Vader] ' + str(tb), xbmc.LOGNOTICE)
                            pass

                # channels updated
                c.execute("UPDATE sources SET channels_updated=? WHERE id=?", [datetime.datetime.now(), self.source.KEY])
                self.conn.commit()

            #if imported_channels == 0 or imported_programs == 0:
            if imported_programs == 0:
                self.updateFailed = True

        except SourceUpdateCanceledException:
            # force source update on next load
            c.execute('UPDATE sources SET channels_updated=? WHERE id=?', [0, self.source.KEY])
            c.execute("DELETE FROM updates WHERE source=?",
                      [self.source.KEY])  # cascades and deletes associated programs records
            self.conn.commit()

        except Exception:
            import traceback as tb
            import sys

            (etype, value, traceback) = sys.exc_info()
            tb.print_exception(etype, value, traceback)

            try:
                self.conn.rollback()
            except sqlite3.OperationalError:
                pass  # no transaction is active

            try:
                # invalidate cached data
                c.execute('UPDATE sources SET channels_updated=? WHERE id=?', [0, self.source.KEY])
                self.conn.commit()
            except sqlite3.OperationalError:
                pass  # database is locked

            self.updateFailed = True
        finally:
            self.updateInProgress = False
            c.close()
        xbmcvfs.delete(lock)

    def updateProgramList(self, callback, programList, channel):
        self.eventQueue.append(
            [self._updateProgramList, callback, programList, channel])
        self.event.set()

    def _updateProgramList(self, programList, channel):
        # todo workaround service.py 'forgets' the adapter and convert set in _initialize.. wtf?!
        sqlite3.register_adapter(datetime.datetime, self.adapt_datetime)
        sqlite3.register_converter('timestamp', self.convert_datetime)

        c = self.conn.cursor()
        c.execute('DELETE FROM programs WHERE source=? AND channel=? ', [self.source.KEY, channel.id])
        updatesId = 1 #TODO why?
        for program in programList:
            c.execute(
                'INSERT OR REPLACE INTO programs(channel, title, sub_title, start_date, end_date, description, categories, image_large, image_small, season, episode, is_movie, language, source, updates_id) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                [channel.id, program.title, program.sub_title, program.startDate, program.endDate, program.description, program.categories,
                 program.imageLarge, program.imageSmall, program.season, program.episode, program.is_movie,
                 program.language, self.source.KEY, updatesId])

        self.conn.commit()


    def setCategory(self,category):
        self.category = category
        self.channelList = None

    def getEPGView(self, channelStart, date=datetime.datetime.now(), progress_callback=None,
                   clearExistingProgramList=True,category=None):
        result = self._invokeAndBlockForResult(self._getEPGView, channelStart, date, progress_callback,
                                               clearExistingProgramList, category)

        if self.updateFailed:
            raise SourceException('No channels or programs imported')

        return result

    def getQuickEPGView(self, channelStart, date=datetime.datetime.now(), progress_callback=None,
                   clearExistingProgramList=True,category=None):
        result = self._invokeAndBlockForResult(self._getQuickEPGView, channelStart, date, progress_callback,
                                               clearExistingProgramList, category)

        if self.updateFailed:
            raise SourceException('No channels or programs imported')

        return result

    def _getEPGView(self, channelStart, date, progress_callback, clearExistingProgramList, category):
        self._updateChannelAndProgramListCaches(date, progress_callback, clearExistingProgramList)

        channels = self._getChannelList(onlyVisible=True)

        if channelStart < 0:
            channelStart = len(channels) - 1
        elif channelStart > len(channels) - 1:
            channelStart = 0
        channelEnd = channelStart + Database.CHANNELS_PER_PAGE
        channelsOnPage = channels[channelStart: channelEnd]

        programs = self._getProgramList(channelsOnPage, date)

        return [channelStart, channelsOnPage, programs]

    def _getQuickEPGView(self, channelStart, date, progress_callback, clearExistingProgramList, category):
        self._updateChannelAndProgramListCaches(date, progress_callback, clearExistingProgramList)

        channels = self._getChannelList(onlyVisible=True)

        if channelStart < 0:
            channelStart = len(channels) - 1
        elif channelStart > len(channels) - 1:
            channelStart = 0
        channelEnd = channelStart + 3
        channelsOnPage = channels[channelStart: channelEnd]

        programs = self._getProgramList(channelsOnPage, date)

        return [channelStart, channelsOnPage, programs]

    def getNumberOfChannels(self):
        channels = self.getChannelList()
        return len(channels)

    def getNextChannel(self, currentChannel):
        channels = self.getChannelList()
        idx = channels.index(currentChannel)
        idx += 1
        if idx > len(channels) - 1:
            idx = 0
        return channels[idx]

    def getPreviousChannel(self, currentChannel):
        channels = self.getChannelList()
        idx = channels.index(currentChannel)
        idx -= 1
        if idx < 0:
            idx = len(channels) - 1
        return channels[idx]

    def deleteLineup(self, callback, lineup):
        self.eventQueue.append([self._deleteLineup, callback, lineup])
        self.event.set()

    def _deleteLineup(self, lineup):
        c = self.conn.cursor()
        # delete channels associated with the lineup
        xbmc.log('[%s] Removing Channels for lineup: %s' % (
            ADDON.getAddonInfo('id'), str(lineup)), xbmc.LOGDEBUG)
        c.execute('DELETE FROM channels WHERE source=? AND lineup=?', [self.source.KEY, lineup])

        c.execute("UPDATE sources SET channels_updated=? WHERE id=?",
                  [datetime.datetime.now(), self.source.KEY])
        self.conn.commit()

    def saveLineup(self, callback, channelList, lineup):
        self.eventQueue.append([self._saveLineup, callback, channelList, lineup])
        self.event.set()

    def _saveLineup(self, channelList, lineup):
        c = self.conn.cursor()
        # delete removed channels
        c.execute('SELECT * FROM channels WHERE source=? AND lineup=?',
                  [self.source.KEY, lineup])
        to_delete = []
        for row in c:
            station_id = row['id']
            found = False
            for channel in channelList:
                if channel.id == station_id:
                    found = True
                    break
            if not found:
                xbmc.log('[%s] Removing Channel: %s from lineup: %s' % (
                    ADDON.getAddonInfo('id'), str(station_id), str(lineup)), xbmc.LOGDEBUG)
                to_delete.append(station_id)

        if to_delete:
            c.execute('DELETE FROM channels WHERE id IN (%s)' %
                      ','.join('?' * len(to_delete)), to_delete)

        # Add new channels
        for channel in channelList:
            xbmc.log('[%s] Adding Channel: %s from lineup: %s' % (
                ADDON.getAddonInfo('id'), str(channel.id), str(lineup)), xbmc.LOGDEBUG)

            logo = get_logo(channel)
            c.execute(
                'INSERT OR IGNORE INTO channels(id, title, logo, stream_url, visible, weight, source, lineup) VALUES(?, ?, ?, ?, ?, (CASE ? WHEN -1 THEN (SELECT COALESCE(MAX(weight)+1, 0) FROM channels WHERE source=?) ELSE ? END), ?, ?)',
                [channel.id, channel.title, logo, '', True, -1, self.source.KEY, -1, self.source.KEY, lineup])

        c.execute("UPDATE sources SET channels_updated=? WHERE id=?",
                  [datetime.datetime.now(), self.source.KEY])
        self.conn.commit()
    def getLineupChannels(self, lineup):
        result = self._invokeAndBlockForResult(self._getLineupChannels, lineup)
        return result

    def _getLineupChannels(self, lineup):
        c = self.conn.cursor()
        channelList = list()
        c.execute('SELECT * FROM channels WHERE source=? AND lineup=? ORDER BY title',
                  [self.source.KEY, lineup])


        for row in c:
            channel = Channel(row['id'], row['title'], row['lineup'], row['logo'], row['stream_url'],
                              row['visible'], row['weight'])
            channelList.append(channel)
        c.close()
        return channelList

    def saveChannelList(self, callback, channelList):
        self.eventQueue.append([self._saveChannelList, callback, channelList])
        self.event.set()

    def _saveChannelList(self, channelList):
        c = self.conn.cursor()
        for idx, channel in enumerate(channelList):
            c.execute(
                'INSERT OR IGNORE INTO channels(id, title, logo, stream_url, visible, weight, source) VALUES(?, ?, ?, ?, ?, (CASE ? WHEN -1 THEN (SELECT COALESCE(MAX(weight)+1, 0) FROM channels WHERE source=?) ELSE ? END), ?)',
                [channel.id, channel.title, channel.logo, channel.streamUrl, channel.visible, channel.weight,
                 self.source.KEY, channel.weight, self.source.KEY])
            if not c.rowcount:
                c.execute(
                    'UPDATE channels SET title=?, logo=?, stream_url=?, visible=?, weight=(CASE ? WHEN -1 THEN weight ELSE ? END) WHERE id=? AND source=?',
                    [channel.title, channel.logo, channel.streamUrl, channel.visible, channel.weight, channel.weight,
                     channel.id, self.source.KEY])

        c.execute("UPDATE sources SET channels_updated=? WHERE id=?", [datetime.datetime.now(), self.source.KEY])
        self.channelList = None
        self.conn.commit()

    def exportChannelList(self):
        channelsList = self.getChannelList(False,True)
        channels = [channel.title for channel in channelsList]
        f = xbmcvfs.File('special://profile/addon_data/script.tvguide.Vader/channels.ini','wb')
        for channel in sorted(channels):
            f.write("%s=nothing\n" % channel.encode("utf8"))
        f.close()

    def exportChannelIdList(self):
        channelsList = self.getChannelList(False,True)
        channels = [(channel.id,channel.title) for channel in channelsList]
        f = xbmcvfs.File('special://profile/addon_data/script.tvguide.Vader/channel_id_title.ini','wb')
        for channel in sorted(channels,key=lambda x: x[1].lower()):
            f.write("%s=%s\n" % (channel[0].encode("utf8"),channel[1].encode("utf8")))
        f.close()

    def getChannelList(self, onlyVisible=True, all=False):
        result = self._invokeAndBlockForResult(self._getChannelList, onlyVisible, all)
        return result

    def _getChannelList(self, onlyVisible, all=False):
        c = self.conn.cursor()
        channelList = list()
        if onlyVisible:
            c.execute('SELECT * FROM channels WHERE source=? AND visible=? ORDER BY weight', [self.source.KEY, 1])
        else:
            c.execute('SELECT * FROM channels WHERE source=? ORDER BY weight', [self.source.KEY])
        for row in c:
            channel = Channel(row['id'], row['title'], row['lineup'], row['logo'], row['stream_url'], row['visible'], row['weight'])
            channelList.append(channel)

        if all == False and self.category and self.category != "Any":
            f = xbmcvfs.File('special://profile/addon_data/script.tvguide.Vader/categories.ini','rb')
            lines = f.read().splitlines()
            f.close()
            filter = []
            seen = set()
            for line in lines:
                if "=" not in line:
                    continue
                name,cat = line.split('=')
                if cat == self.category:
                    if name not in seen:
                        filter.append(name)
                    seen.add(name)

            NONE = "0"
            SORT = "1"
            CATEGORIES = "2"
            new_channels = []
            if ADDON.getSetting('channel.filter.sort') == CATEGORIES:
                for filter_name in filter:
                    for channel in channelList:
                        if channel.title == filter_name:
                            new_channels.append(channel)
                if new_channels:
                    channelList = new_channels
            else:
                for channel in channelList:
                    if channel.title in filter:
                        new_channels.append(channel)
                if new_channels:
                    if ADDON.getSetting('channel.filter.sort') == SORT:
                        channelList = sorted(new_channels, key=lambda channel: channel.title.lower())
                    else:
                        channelList = new_channels
        c.close()
        return channelList


    def programSearch(self, search):
        return self._invokeAndBlockForResult(self._programSearch, search)

    def _programSearch(self, search):
        programList = []
        now = datetime.datetime.now()
        days = int(ADDON.getSetting('listing.days'))
        startTime = now - datetime.timedelta(hours=int(ADDON.getSetting('listing.hours')))
        endTime = now + datetime.timedelta(days=days)
        c = self.conn.cursor()
        channelList = self._getChannelList(True)
        search = "%%%s%%" % search
        for channel in channelList:

            if ADDON.getSetting('program.search.plot') == 'true':
                try: c.execute('SELECT * FROM programs WHERE channel=? AND source=? AND start_date>=? AND end_date<=? AND (title LIKE ? OR description LIKE ?)',
                          [channel.id, self.source.KEY, startTime, endTime, search, search])
                except: return
            else:
                try: c.execute('SELECT * FROM programs WHERE channel=? AND source=? AND title LIKE ?',
                          [channel.id, self.source.KEY,search])
                except: return
            for row in c:
                program = Program(channel, title=row['title'], sub_title=row['sub_title'], startDate=row['start_date'], endDate=row['end_date'],
                              description=row['description'], categories=row['categories'],
                              imageLarge=row['image_large'], imageSmall=row['image_small'], season=row['season'], episode=row['episode'],
                              is_movie=row['is_movie'], language=row['language'])
                programList.append(program)
        c.close()
        return programList

    def descriptionSearch(self, search):
        return self._invokeAndBlockForResult(self._descriptionSearch, search)

    def _descriptionSearch(self, search):
        programList = []
        now = datetime.datetime.now()
        days = int(ADDON.getSetting('listing.days'))
        startTime = now - datetime.timedelta(hours=int(ADDON.getSetting('listing.hours')))
        endTime = now + datetime.timedelta(days=days)
        c = self.conn.cursor()
        channelList = self._getChannelList(True)
        search = "%%%s%%" % search
        for channel in channelList:

            try: c.execute('SELECT * FROM programs WHERE channel=? AND source=? AND description LIKE ? AND start_date>=? AND end_date<=? ',
                      [channel.id, self.source.KEY,search, startTime, endTime])
            except: return
            for row in c:
                program = Program(channel, title=row['title'], sub_title=row['sub_title'], startDate=row['start_date'], endDate=row['end_date'],
                              description=row['description'], categories=row['categories'],
                              imageLarge=row['image_large'], imageSmall=row['image_small'], season=row['season'], episode=row['episode'],
                              is_movie=row['is_movie'], language=row['language'])
                programList.append(program)
        c.close()
        return programList

    def programCategorySearch(self, search):
        return self._invokeAndBlockForResult(self._programCategorySearch, search)

    def _programCategorySearch(self, search):
        programList = []
        now = datetime.datetime.now()
        days = int(ADDON.getSetting('listing.days'))
        startTime = now - datetime.timedelta(hours=int(ADDON.getSetting('listing.hours')))
        endTime = now + datetime.timedelta(days=days)
        c = self.conn.cursor()
        channelList = self._getChannelList(True)
        search = "%%%s%%" % search
        for channel in channelList:
            try: c.execute('SELECT * FROM programs WHERE channel=? AND source=? AND categories LIKE ? AND start_date>=? AND end_date<=? ',
                      [channel.id, self.source.KEY,search, startTime, endTime])
            except: return
            for row in c:
                program = Program(channel, title=row['title'], sub_title=row['sub_title'], startDate=row['start_date'], endDate=row['end_date'],
                              description=row['description'], categories=row['categories'],
                              imageLarge=row['image_large'], imageSmall=row['image_small'], season=row['season'], episode=row['episode'],
                              is_movie=row['is_movie'], language=row['language'])
                programList.append(program)
        c.close()
        return programList

    def getChannelListing(self, channel):
        return self._invokeAndBlockForResult(self._getChannelListing, channel)

    def _getChannelListing(self, channel):
        now = datetime.datetime.now()
        days = int(ADDON.getSetting('listing.days'))
        endTime = now + datetime.timedelta(days=days)
        programList = []
        c = self.conn.cursor()
        try: c.execute('SELECT * FROM programs WHERE channel=? AND end_date>? AND start_date<?',
                  [channel.id,now,endTime])
        except: return
        for row in c:
            program = Program(channel, title=row['title'], sub_title=row['sub_title'], startDate=row['start_date'], endDate=row['end_date'],
                              description=row['description'], categories=row['categories'],
                          imageLarge=row['image_large'], imageSmall=row['image_small'], season=row['season'], episode=row['episode'],
                          is_movie=row['is_movie'], language=row['language'])
            programList.append(program)
        c.close()

        return programList

    def channelSearch(self, search):
        return self._invokeAndBlockForResult(self._channelSearch, search)

    def _channelSearch(self, search):
        programList = []
        now = datetime.datetime.now()
        c = self.conn.cursor()
        channels = self._getChannelList(True)
        channelIds = [cc.id for cc in channels]
        channelMap = dict()
        ids = []
        for cc in channels:
            if cc.id:
                channelMap[cc.id] = cc
                search = search.replace(' ','.*')
                if re.search(search,cc.title,flags=re.I):
                    ids.append(cc.id)
        if not ids:
            return
        ids_string = '\',\''.join(ids)
        c.execute('SELECT * FROM programs WHERE channel IN (\'' + ids_string + '\') AND source=? AND start_date<=? AND end_date>=? ',
                  [self.source.KEY, now, now])
        for row in c:
            program = Program(channelMap[row['channel']], title=row['title'], sub_title=row['sub_title'], startDate=row['start_date'], endDate=row['end_date'],
                          description=row['description'], categories=row['categories'],
                          imageLarge=row['image_large'], imageSmall=row['image_small'], season=row['season'], episode=row['episode'],
                          is_movie=row['is_movie'], language=row['language'])
            programList.append(program)
        c.close()
        return programList

    def getNowList(self):
        return self._invokeAndBlockForResult(self._getNowList)

    def _getNowList(self):
        programList = []
        now = datetime.datetime.now()
        channels = self._getChannelList(True)
        channelIds = [c.id for c in channels]
        channelMap = dict()
        for cc in channels:
            if cc.id:
                channelMap[cc.id] = cc

        c = self.conn.cursor()
        c.execute(
            'SELECT DISTINCT p.*' +
            'FROM programs p, channels c WHERE p.channel IN (\'' + ('\',\''.join(channelIds)) + '\') AND p.channel=c.id AND p.source=? AND p.end_date >= ? AND p.start_date <= ?' +
            'ORDER BY c.weight',
            [self.source.KEY, now, now])

        for row in c:
            notification_scheduled = ''
            autoplay_scheduled = ''
            autoplaywith_scheduled = ''
            program = Program(channelMap[row['channel']], title=row['title'], sub_title=row['sub_title'], startDate=row['start_date'], endDate=row['end_date'],
                              description=row['description'], categories=row['categories'],
                              imageLarge=row['image_large'], imageSmall=row['image_small'], season=row['season'], episode=row['episode'],
                              is_movie=row['is_movie'], language=row['language'],
                              notificationScheduled=notification_scheduled, autoplayScheduled=autoplay_scheduled, autoplaywithScheduled=autoplaywith_scheduled)
            programList.append(program)
        c.close()
        return programList

    def getNextList(self):
        return self._invokeAndBlockForResult(self._getNextList)

    def _getNextList(self):
        programList = []
        now = datetime.datetime.now()
        c = self.conn.cursor()
        channelList = self._getChannelList(True)
        for channel in channelList:
            try: c.execute('SELECT * FROM programs WHERE channel=? AND source=? AND start_date >= ? AND end_date >= ?',
                      [channel.id, self.source.KEY,now,now])
            except: return
            row = c.fetchone()
            if row:
                program = Program(channel, title=row['title'], sub_title=row['sub_title'], startDate=row['start_date'], endDate=row['end_date'],
                              description=row['description'], categories=row['categories'],
                              imageLarge=row['image_large'], imageSmall=row['image_small'], season=row['season'], episode=row['episode'],
                              is_movie=row['is_movie'], language=row['language'])
                programList.append(program)
        c.close()
        return programList


    def getCurrentProgram(self, channel):
        return self._invokeAndBlockForResult(self._getCurrentProgram, channel)

    def _getCurrentProgram(self, channel):
        """

        @param channel:
        @type channel: source.Channel
        @return:
        """
        program = None
        now = datetime.datetime.now()
        c = self.conn.cursor()
        try: c.execute('SELECT * FROM programs WHERE channel=? AND source=? AND start_date <= ? AND end_date >= ?',
                  [channel.id, self.source.KEY, now, now])
        except Exception as detail:
            return
        row = c.fetchone()
        if row:
            try:
                program = Program(channel, title=row['title'], sub_title=row['sub_title'], startDate=row['start_date'], endDate=row['end_date'],
                              description=row['description'], categories=row['categories'],
                              imageLarge=row['image_large'], imageSmall=row['image_small'], season=row['season'], episode=row['episode'],
                              is_movie=row['is_movie'], language=row['language'])
            except Exception as detail:
                return
        c.close()

        return program

    def getNextProgram(self, program):
        return self._invokeAndBlockForResult(self._getNextProgram, program)

    def _getNextProgram(self, program):
        try:
            nextProgram = None
            c = self.conn.cursor()
            c.execute(
                'SELECT * FROM programs WHERE channel=? AND source=? AND start_date >= ? ORDER BY start_date ASC LIMIT 1',
                [program.channel.id, self.source.KEY, program.endDate])
            row = c.fetchone()
            if row:
                nextProgram = Program(program.channel, title=row['title'], sub_title=row['sub_title'], startDate=row['start_date'], endDate=row['end_date'],
                              description=row['description'], categories=row['categories'],
                              imageLarge=row['image_large'], imageSmall=row['image_small'], season=row['season'], episode=row['episode'],
                              is_movie=row['is_movie'], language=row['language'])
            c.close()

            return nextProgram
        except:
            return

    def getPreviousProgram(self, program):
        return self._invokeAndBlockForResult(self._getPreviousProgram, program)

    def _getPreviousProgram(self, program):
        try:
            previousProgram = None
            c = self.conn.cursor()
            c.execute(
                'SELECT * FROM programs WHERE channel=? AND source=? AND end_date <= ? ORDER BY start_date DESC LIMIT 1',
                [program.channel.id, self.source.KEY, program.startDate])
            row = c.fetchone()
            if row:
                previousProgram = Program(program.channel, title=row['title'], sub_title=row['sub_title'], startDate=row['start_date'], endDate=row['end_date'],
                              description=row['description'], categories=row['categories'],
                              imageLarge=row['image_large'], imageSmall=row['image_small'], season=row['season'], episode=row['episode'],
                              is_movie=row['is_movie'], language=row['language'])
            c.close()
            return previousProgram
        except:
            return

    def _getProgramList(self, channels, startTime):
        """

        @param channels:
        @type channels: list of source.Channel
        @param startTime:
        @type startTime: datetime.datetime
        @return:
        """
        endTime = startTime + datetime.timedelta(hours=2)
        programList = list()

        channelMap = dict()
        for c in channels:
            if c.id:
                channelMap[c.id] = c

        if not channels:
            return []

        c = self.conn.cursor()
        #once
        #TODO always, notifications,autoplays
        c.execute(
            'SELECT p.*, ' +
            '(SELECT 1 FROM notifications n WHERE n.channel=p.channel AND n.program_title=p.title AND n.source=p.source AND n.type=0 AND n.start_date=p.start_date) AS notification_scheduled_once, '+
            '(SELECT 1 FROM notifications n WHERE n.channel=p.channel AND n.program_title=p.title AND n.source=p.source AND n.type=1 ) AS notification_scheduled_always, '+
            '(SELECT 1 FROM autoplays a WHERE a.channel=p.channel AND a.program_title=p.title AND a.source=p.source AND a.type=0 AND a.start_date=p.start_date) AS autoplay_scheduled_once, '+
            '(SELECT 1 FROM autoplays a WHERE a.channel=p.channel AND a.program_title=p.title AND a.source=p.source AND a.type=1 ) AS autoplay_scheduled_always, '+
            '(SELECT 1 FROM autoplaywiths w WHERE w.channel=p.channel AND w.program_title=p.title AND w.source=p.source AND w.type=0 AND w.start_date=p.start_date) AS autoplaywith_scheduled_once, '+
            '(SELECT 1 FROM autoplaywiths w WHERE w.channel=p.channel AND w.program_title=p.title AND w.source=p.source AND w.type=1 ) AS autoplaywith_scheduled_always '+
            'FROM programs p WHERE p.channel IN (\'' + ('\',\''.join(channelMap.keys())) + '\') AND p.source=? AND p.end_date > ? AND p.start_date < ?',
            [self.source.KEY, startTime, endTime])

        for row in c:
            notification_scheduled = row['notification_scheduled_once'] or row['notification_scheduled_always']
            autoplay_scheduled = row['autoplay_scheduled_once'] or row['autoplay_scheduled_always']
            autoplaywith_scheduled = row['autoplaywith_scheduled_once'] or row['autoplaywith_scheduled_always']
            program = Program(channelMap[row['channel']], title=row['title'], sub_title=row['sub_title'], startDate=row['start_date'], endDate=row['end_date'],
                              description=row['description'], categories=row['categories'],
                              imageLarge=row['image_large'], imageSmall=row['image_small'], season=row['season'], episode=row['episode'],
                              is_movie=row['is_movie'], language=row['language'],
                              notificationScheduled=notification_scheduled, autoplayScheduled=autoplay_scheduled, autoplaywithScheduled=autoplaywith_scheduled)
            programList.append(program)
        return programList

    def _isProgramListCacheExpired(self, date=datetime.datetime.now()):
        # check if data is up-to-date in database
        dateStr = date.strftime('%Y-%m-%d')
        c = self.conn.cursor()
        c.execute('SELECT programs_updated FROM updates WHERE source=? AND date=?', [self.source.KEY, dateStr])
        row = c.fetchone()
        today = datetime.datetime.now()
        expired = row is None or row['programs_updated'].day != today.day
        c.close()
        return expired

    def setCustomStreamUrl(self, channel, stream_url):
        if stream_url is not None:
            self._invokeAndBlockForResult(self._setCustomStreamUrl, channel, stream_url)
            # no result, but block until operation is done

    def _setCustomStreamUrl(self, channel, stream_url):
        if stream_url is not None:
            image = ""
            if ADDON.getSetting("addon.logos") == "true":
                file_name = 'special://profile/addon_data/script.tvguide.Vader/icons.ini'
                f = xbmcvfs.File(file_name)
                items = f.read().splitlines()
                f.close()
                for item in items:
                    if item.startswith('['):
                        pass
                    elif item.startswith('#'):
                        pass
                    else:
                        url_icon = item.rsplit('|',1)
                        if len(url_icon) == 2:
                            url = url_icon[0]
                            icon = url_icon[1]
                            if url == stream_url:
                                if icon and icon != "nothing":
                                    image = icon.rstrip('/')
            c = self.conn.cursor()
            if image:
                c.execute('UPDATE OR REPLACE channels SET logo=? WHERE id=?' , (image, channel.id))
            c.execute("DELETE FROM custom_stream_url WHERE channel=?", [channel.id])
            c.execute("INSERT INTO custom_stream_url(channel, stream_url) VALUES(?, ?)",
                      [channel.id, stream_url.decode('utf-8', 'ignore')])
            self.conn.commit()
            c.close()

    def setAltCustomStreamUrl(self, channel, title, stream_url):
        if stream_url is not None:
            self._invokeAndBlockForResult(self._setAltCustomStreamUrl, channel, title, stream_url)
            # no result, but block until operation is done

    def _setAltCustomStreamUrl(self, channel, title, stream_url):
        if stream_url is not None:
            c = self.conn.cursor()
            #c.execute("DELETE FROM alt_custom_stream_url WHERE channel=?", [channel.id])
            c.execute("INSERT OR REPLACE INTO alt_custom_stream_url(channel, title, stream_url) VALUES(?, ?, ?)",
                      [channel.id, title.decode('utf-8', 'ignore'), stream_url.decode('utf-8', 'ignore')])
            self.conn.commit()
            c.close()

    def setCustomStreamUrls(self, stream_urls):
        if stream_urls is not None:
            self._invokeAndBlockForResult(self._setCustomStreamUrls, stream_urls)
            # no result, but block until operation is done

    def _setCustomStreamUrls(self, stream_urls):
        if stream_urls is not None:
            c = self.conn.cursor()
            for (id,stream_url) in stream_urls:
                c.execute("DELETE FROM custom_stream_url WHERE channel=?", [id])
                c.execute("INSERT OR REPLACE INTO custom_stream_url(channel, stream_url) VALUES(?, ?)",
                          [id, stream_url.decode('utf-8', 'ignore')])
            self.conn.commit()
            c.close()

    def setAltCustomStreamUrls(self, stream_urls):
        if stream_urls is not None:
            self._invokeAndBlockForResult(self._setAltCustomStreamUrls, stream_urls)
            # no result, but block until operation is done

    def _setAltCustomStreamUrls(self, stream_urls):
        if stream_urls is not None:
            c = self.conn.cursor()
            for (id,title,stream_url) in stream_urls:
                #c.execute("DELETE FROM alt_custom_stream_url WHERE channel=?", [id])
                c.execute("INSERT OR REPLACE INTO alt_custom_stream_url(channel, title, stream_url) VALUES(?, ?, ?)",
                          [id, title.decode('utf-8', 'ignore'), stream_url.decode('utf-8', 'ignore')])
            self.conn.commit()
            c.close()

    def getCustomStreamUrl(self, channel):
        return self._invokeAndBlockForResult(self._getCustomStreamUrl, channel)

    def _getCustomStreamUrl(self, channel):
        if not channel:
            return
        c = self.conn.cursor()
        c.execute("SELECT stream_url FROM custom_stream_url WHERE channel=?", [channel.id])
        stream_url = c.fetchone()
        c.close()

        if stream_url:
            return stream_url[0]
        else:
            return None

    def getAltCustomStreamUrl(self, channel):
        return self._invokeAndBlockForResult(self._getAltCustomStreamUrl, channel)

    def _getAltCustomStreamUrl(self, channel):
        if not channel:
            return
        c = self.conn.cursor()
        c.execute("SELECT DISTINCT stream_url, title FROM alt_custom_stream_url WHERE channel=?", [channel.id])
        stream_url = []
        for row in c:
            stream_url.append((row["stream_url"],row["title"],))
        return stream_url

    def getCustomStreamUrls(self):
        return self._invokeAndBlockForResult(self._getCustomStreamUrls)

    def _getCustomStreamUrls(self):
        c = self.conn.cursor()
        c.execute("SELECT * FROM custom_stream_url")
        stream_urls = []
        for row in c:
            stream_urls.append((row["channel"],row["stream_url"]))
        return stream_urls

    def getAltCustomStreamUrls(self):
        return self._invokeAndBlockForResult(self._getAltCustomStreamUrls)

    def _getAltCustomStreamUrls(self):
        c = self.conn.cursor()
        c.execute("SELECT * FROM alt_custom_stream_url")
        stream_urls = []
        for row in c:
            log(row)
            stream_urls.append((row["channel"],row["title"],row["stream_url"]))
        return stream_urls

    def deleteCustomStreamUrl(self, channel):
        self.eventQueue.append([self._deleteCustomStreamUrl, None, channel])
        self.event.set()

    def _deleteCustomStreamUrl(self, channel):
        c = self.conn.cursor()
        c.execute("DELETE FROM custom_stream_url WHERE channel=?", [channel.id])
        self.conn.commit()
        c.close()

    def clearCustomStreamUrls(self):
        self.eventQueue.append([self._clearCustomStreamUrls, None])
        self.event.set()

    def _clearCustomStreamUrls(self):
        c = self.conn.cursor()
        c.execute("DELETE FROM custom_stream_url")
        self.conn.commit()
        c.close()

    def clearAltCustomStreamUrls(self):
        self.eventQueue.append([self._clearAltCustomStreamUrls, None])
        self.event.set()

    def _clearAltCustomStreamUrls(self):
        c = self.conn.cursor()
        c.execute("DELETE FROM alt_custom_stream_url")
        self.conn.commit()
        c.close()

    def deleteAltCustomStreamUrl(self, url):
        self.eventQueue.append([self._deleteAltCustomStreamUrl, None, url])
        self.event.set()

    def _deleteAltCustomStreamUrl(self, url):
        c = self.conn.cursor()
        c.execute("DELETE FROM alt_custom_stream_url WHERE stream_url=?", [url])
        self.conn.commit()
        c.close()

    def getStreamUrl(self, channel):
        customStreamUrl = self.getCustomStreamUrl(channel)
        if customStreamUrl:
            return customStreamUrl
        else:
            return None

    def getAltStreamUrl(self, channel):
        return self.getAltCustomStreamUrl(channel)

    @staticmethod
    def adapt_datetime(ts):
        # http://docs.python.org/2/library/sqlite3.html#registering-an-adapter-callable
        return time.mktime(ts.timetuple())

    @staticmethod
    def convert_datetime(ts):
        try:
            return datetime.datetime.fromtimestamp(float(ts))
        except ValueError:
            return None

    def _createTables(self):
        c = self.conn.cursor()

        try:
            c.execute('SELECT major, minor, patch FROM version')
            (major, minor, patch) = c.fetchone()
            version = [major, minor, patch]
        except sqlite3.OperationalError:
            version = [0, 0, 0]

        try:
            if version < [1, 3, 0]:
                c.execute('CREATE TABLE IF NOT EXISTS custom_stream_url(channel TEXT, stream_url TEXT)')
                c.execute('CREATE TABLE version (major INTEGER, minor INTEGER, patch INTEGER)')
                c.execute('INSERT INTO version(major, minor, patch) VALUES(1, 3, 0)')
                # For caching data
                c.execute('CREATE TABLE sources(id TEXT PRIMARY KEY, channels_updated TIMESTAMP)')
                c.execute(
                    'CREATE TABLE updates(id INTEGER PRIMARY KEY, source TEXT, date TEXT, programs_updated TIMESTAMP)')
                c.execute(
                    'CREATE TABLE channels(id TEXT, title TEXT, logo TEXT, stream_url TEXT, source TEXT, visible BOOLEAN, weight INTEGER, PRIMARY KEY (id, source), FOREIGN KEY(source) REFERENCES sources(id) ON DELETE CASCADE)')
                c.execute(
                    'CREATE TABLE programs(channel TEXT, title TEXT, start_date TIMESTAMP, end_date TIMESTAMP, description TEXT, image_large TEXT, image_small TEXT, source TEXT, updates_id INTEGER, FOREIGN KEY(channel, source) REFERENCES channels(id, source) ON DELETE CASCADE, FOREIGN KEY(updates_id) REFERENCES updates(id) ON DELETE CASCADE)')
                c.execute('CREATE INDEX program_list_idx ON programs(source, channel, start_date, end_date)')
                c.execute('CREATE INDEX start_date_idx ON programs(start_date)')
                c.execute('CREATE INDEX end_date_idx ON programs(end_date)')
                # For active setting
                c.execute('CREATE TABLE settings(key TEXT PRIMARY KEY, value TEXT)')
                # For notifications
                c.execute(
                    "CREATE TABLE notifications(channel TEXT, program_title TEXT, source TEXT, FOREIGN KEY(channel, source) REFERENCES channels(id, source) ON DELETE CASCADE)")
            if version < [1, 3, 1]:
                # Recreate tables with FOREIGN KEYS as DEFERRABLE INITIALLY DEFERRED
                c.execute('UPDATE version SET major=1, minor=3, patch=1')
                c.execute('DROP TABLE channels')
                c.execute('DROP TABLE programs')
                c.execute(
                    'CREATE TABLE channels(id TEXT, title TEXT, logo TEXT, stream_url TEXT, source TEXT, visible BOOLEAN, weight INTEGER, PRIMARY KEY (id, source), FOREIGN KEY(source) REFERENCES sources(id) ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED)')
                c.execute(
                    'CREATE TABLE programs(channel TEXT, title TEXT, start_date TIMESTAMP, end_date TIMESTAMP, description TEXT, image_large TEXT, image_small TEXT, source TEXT, updates_id INTEGER, FOREIGN KEY(channel, source) REFERENCES channels(id, source) ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED, FOREIGN KEY(updates_id) REFERENCES updates(id) ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED)')
                c.execute('CREATE INDEX program_list_idx ON programs(source, channel, start_date, end_date)')
                c.execute('CREATE INDEX start_date_idx ON programs(start_date)')
                c.execute('CREATE INDEX end_date_idx ON programs(end_date)')

            if version < [1, 3, 2]:
                # Recreate tables with seasons, episodes and is_movie
                c.execute('UPDATE version SET major=1, minor=3, patch=2')
                c.execute('DROP TABLE programs')
                c.execute(
                    'CREATE TABLE programs(channel TEXT, title TEXT, start_date TIMESTAMP, end_date TIMESTAMP, description TEXT, image_large TEXT, image_small TEXT, season TEXT, episode TEXT, is_movie TEXT, language TEXT, source TEXT, updates_id INTEGER, FOREIGN KEY(channel, source) REFERENCES channels(id, source) ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED, FOREIGN KEY(updates_id) REFERENCES updates(id) ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED)')
                c.execute('CREATE INDEX program_list_idx ON programs(source, channel, start_date, end_date)')
                c.execute('CREATE INDEX start_date_idx ON programs(start_date)')
                c.execute('CREATE INDEX end_date_idx ON programs(end_date)')
            if version < [1, 3, 3]:
                c.execute('UPDATE version SET major=1, minor=3, patch=3')
                c.execute('DROP TABLE IF EXISTS notifications')
                c.execute('DROP TABLE IF EXISTS autoplays')
                c.execute('DROP TABLE IF EXISTS autoplaywiths')
                c.execute(
                    "CREATE TABLE IF NOT EXISTS notifications(channel TEXT, program_title TEXT, source TEXT, start_date TIMESTAMP, type TEXT, FOREIGN KEY(channel, source) REFERENCES channels(id, source) ON DELETE CASCADE)")
                c.execute(
                    "CREATE TABLE IF NOT EXISTS autoplays(channel TEXT, program_title TEXT, source TEXT, start_date TIMESTAMP, type TEXT, FOREIGN KEY(channel, source) REFERENCES channels(id, source) ON DELETE CASCADE)")
                c.execute(
                    "CREATE TABLE IF NOT EXISTS autoplaywiths(channel TEXT, program_title TEXT, source TEXT, start_date TIMESTAMP, type TEXT, FOREIGN KEY(channel, source) REFERENCES channels(id, source) ON DELETE CASCADE)")
            if version < [1, 3, 4]:
                c.execute('UPDATE version SET major=1, minor=3, patch=4')
                c.execute('DROP TABLE programs')
                c.execute(
                    'CREATE TABLE programs(channel TEXT, title TEXT, start_date TIMESTAMP, end_date TIMESTAMP, description TEXT, image_large TEXT, image_small TEXT, season TEXT, episode TEXT, is_movie TEXT, language TEXT, source TEXT, updates_id INTEGER, UNIQUE (channel, start_date, end_date), FOREIGN KEY(channel, source) REFERENCES channels(id, source) ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED, FOREIGN KEY(updates_id) REFERENCES updates(id) ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED)')
            if version < [1, 3, 5]:
                c.execute('UPDATE version SET major=1, minor=3, patch=5')
                c.execute('DROP TABLE channels')
                c.execute(
                    'CREATE TABLE channels(id TEXT, title TEXT, logo TEXT, stream_url TEXT, source TEXT, lineup TEXT, visible BOOLEAN, weight INTEGER, PRIMARY KEY (id, source), FOREIGN KEY(source) REFERENCES sources(id) ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED)')
            if version < [1, 3, 6]:
                c.execute('UPDATE version SET major=1, minor=3, patch=6')
                c.execute('DROP TABLE programs')
                c.execute(
                    'CREATE TABLE programs(channel TEXT, title TEXT, start_date TIMESTAMP, end_date TIMESTAMP, description TEXT, image_large TEXT, image_small TEXT, season TEXT, episode TEXT, is_movie TEXT, language TEXT, source TEXT, updates_id INTEGER, UNIQUE (channel, start_date, end_date), FOREIGN KEY(channel, source) REFERENCES channels(id, source) ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED, FOREIGN KEY(updates_id) REFERENCES updates(id) ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED)')
                c.execute('CREATE INDEX program_list_idx ON programs(source, channel, start_date, end_date)')
                c.execute('CREATE INDEX start_date_idx ON programs(start_date)')
                c.execute('CREATE INDEX end_date_idx ON programs(end_date)')
            if version < [1, 3, 7]:
                c.execute('UPDATE version SET major=1, minor=3, patch=7')
                c.execute('CREATE TABLE IF NOT EXISTS alt_custom_stream_url(channel TEXT, stream_url TEXT)')
            if version < [1, 3, 8]:
                c.execute('UPDATE version SET major=1, minor=3, patch=8')
                c.execute('DROP TABLE alt_custom_stream_url')
                c.execute('CREATE TABLE IF NOT EXISTS alt_custom_stream_url(channel TEXT, title TEXT, stream_url TEXT)')
            if version < [1, 3, 9]:
                c.execute('UPDATE version SET major=1, minor=3, patch=9')
                c.execute('ALTER TABLE alt_custom_stream_url RENAME TO alt_custom_stream_url_old')
                c.execute('CREATE TABLE IF NOT EXISTS alt_custom_stream_url(channel TEXT, title TEXT, stream_url TEXT, PRIMARY KEY (channel, stream_url))')
                c.execute('INSERT INTO alt_custom_stream_url SELECT * FROM alt_custom_stream_url_old')
                c.execute('DROP TABLE alt_custom_stream_url_old')
            if version < [1, 4, 0]:
                c.execute('UPDATE version SET major=1, minor=4, patch=0')
                c.execute('DROP TABLE programs')
                c.execute(
                    'CREATE TABLE programs(channel TEXT, title TEXT, sub_title TEXT, start_date TIMESTAMP, end_date TIMESTAMP, description TEXT, categories TEXT, image_large TEXT, image_small TEXT, season TEXT, episode TEXT, is_movie TEXT, language TEXT, source TEXT, updates_id INTEGER, UNIQUE (channel, start_date, end_date), FOREIGN KEY(channel, source) REFERENCES channels(id, source) ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED, FOREIGN KEY(updates_id) REFERENCES updates(id) ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED)')
                c.execute('CREATE INDEX program_list_idx ON programs(source, channel, start_date, end_date)')
                c.execute('CREATE INDEX start_date_idx ON programs(start_date)')
                c.execute('CREATE INDEX end_date_idx ON programs(end_date)')

            # make sure we have a record in sources for this Source
            c.execute("INSERT OR IGNORE INTO sources(id, channels_updated) VALUES(?, ?)", [self.source.KEY, 0])

            self.conn.commit()
            c.close()

        #except sqlite3.OperationalError, ex:
        except Exception as detail:
            xbmc.log("(script.tvguide.Vader) %s" % detail, xbmc.LOGERROR)
            dialog = xbmcgui.Dialog()
            dialog.notification('script.tvguide.Vader', 'database exception %s' % detail, xbmcgui.NOTIFICATION_ERROR , 5000)
            #raise DatabaseSchemaException(detail)

    def addNotification(self, program,type):
        self._invokeAndBlockForResult(self._addNotification, program,type)
        # no result, but block until operation is done

    def _addNotification(self, program,type):
        """
        @type program: source.program
        """
        c = self.conn.cursor()
        c.execute("INSERT INTO notifications(channel, program_title, source, start_date, type) VALUES(?, ?, ?, ?, ?)",
                  [program.channel.id, program.title, self.source.KEY, program.startDate, type])
        self.conn.commit()
        c.close()

    def removeNotification(self, program):
        self._invokeAndBlockForResult(self._removeNotification, program)
        # no result, but block until operation is done

    def _removeNotification(self, program):
        """
        @type program: source.program
        """
        c = self.conn.cursor()
        c.execute("DELETE FROM notifications WHERE channel=? AND program_title=? AND source=?",
                  [program.channel.id, program.title, self.source.KEY])
        self.conn.commit()
        c.close()

    def getFullNotifications(self, daysLimit=2):
        return self._invokeAndBlockForResult(self._getFullNotifications, daysLimit)

    def _getFullNotifications(self, daysLimit):
        start = datetime.datetime.now()
        end = start + datetime.timedelta(days=daysLimit)
        programList = list()
        c = self.conn.cursor()
        #once
        c.execute("SELECT DISTINCT c.id, c.title as channel_title,c.lineup,c.logo,c.stream_url,c.visible,c.weight, p.* FROM programs p, channels c, notifications a WHERE c.id = p.channel AND a.type = 0 AND p.title = a.program_title AND a.start_date = p.start_date")
        for row in c:
            channel = Channel(row["id"], row["channel_title"], row['lineup'], row["logo"], row["stream_url"], row["visible"], row["weight"])
            program = Program(channel, title=row['title'], sub_title=row['sub_title'], startDate=row['start_date'], endDate=row['end_date'],
                            description=row['description'], categories=row['categories'],
                            imageLarge=row["image_large"],imageSmall=row["image_small"],
                            season=row["season"],episode=row["episode"],is_movie=row["is_movie"],language=row["language"],notificationScheduled=True)
            programList.append(program)
        #always
        c.execute("SELECT DISTINCT c.id, c.title as channel_title,c.lineup,c.logo,c.stream_url,c.visible,c.weight, p.* FROM programs p, channels c, notifications a WHERE c.id = p.channel AND a.type = 1 AND p.title = a.program_title AND p.start_date >= ? AND p.end_date <= ?", [start,end])
        #c.execute("SELECT DISTINCT c.id, c.title as channel_title,c.logo,c.stream_url,c.visible,c.weight, p.* FROM programs p, channels c, notifications a WHERE c.id = p.channel AND a.type = 1 AND p.title = a.program_title")
        for row in c:
            channel = Channel(row["id"], row["channel_title"], row['lineup'], row["logo"], row["stream_url"], row["visible"], row["weight"])
            program = Program(channel, title=row['title'], sub_title=row['sub_title'], startDate=row['start_date'], endDate=row['end_date'],
                            description=row['description'], categories=row['categories'],
                            imageLarge=row["image_large"],imageSmall=row["image_small"],
                            season=row["season"],episode=row["episode"],is_movie=row["is_movie"],language=row["language"],notificationScheduled=True)
            programList.append(program)
        c.close()
        return programList

    def isNotificationRequiredForProgram(self, program):
        return self._invokeAndBlockForResult(self._isNotificationRequiredForProgram, program)

    def _isNotificationRequiredForProgram(self, program):
        """
        @type program: source.program
        """
        c = self.conn.cursor()
        c.execute("SELECT 1 FROM notifications WHERE channel=? AND program_title=? AND source=?",
                  [program.channel.id, program.title, self.source.KEY])
        result = c.fetchone()
        c.close()

        return result

    def clearAllNotifications(self):
        self._invokeAndBlockForResult(self._clearAllNotifications)
        # no result, but block until operation is done

    def _clearAllNotifications(self):
        c = self.conn.cursor()
        c.execute('DELETE FROM notifications')
        self.conn.commit()
        c.close()

    def addAutoplay(self, program, type):
        self._invokeAndBlockForResult(self._addAutoplay, program, type)
        # no result, but block until operation is done

    def _addAutoplay(self, program, type):
        """
        @type program: source.program
        """
        c = self.conn.cursor()
        c.execute("INSERT INTO autoplays(channel, program_title, source, start_date, type) VALUES(?, ?, ?, ?, ?)",
                  [program.channel.id, program.title, self.source.KEY, program.startDate, type])
        self.conn.commit()
        c.close()

    def removeAutoplay(self, program):
        self._invokeAndBlockForResult(self._removeAutoplay, program)
        # no result, but block until operation is done

    def _removeAutoplay(self, program):
        """
        @type program: source.program
        """
        c = self.conn.cursor()
        c.execute("DELETE FROM autoplays WHERE channel=? AND program_title=? AND source=?",
                  [program.channel.id, program.title, self.source.KEY])
        self.conn.commit()
        c.close()

    def getFullAutoplays(self, daysLimit=2):
        return self._invokeAndBlockForResult(self._getFullAutoplays, daysLimit)

    def _getFullAutoplays(self, daysLimit):
        start = datetime.datetime.now()
        end = start + datetime.timedelta(days=daysLimit)
        programList = list()
        c = self.conn.cursor()
        if not c:
            return
        #once
        c.execute("SELECT DISTINCT c.id, c.title as channel_title,c.lineup,c.logo,c.stream_url,c.visible,c.weight, p.* FROM programs p, channels c, autoplays a WHERE c.id = p.channel AND a.type = 0 AND p.title = a.program_title AND a.start_date = p.start_date")
        for row in c:
            channel = Channel(row["id"], row["channel_title"], row['lineup'], row["logo"], row["stream_url"], row["visible"], row["weight"])
            program = Program(channel, title=row['title'], sub_title=row['sub_title'], startDate=row['start_date'], endDate=row['end_date'],
                            description=row['description'], categories=row['categories'],
                            imageLarge=row["image_large"],imageSmall=row["image_small"],
                            season=row["season"],episode=row["episode"],is_movie=row["is_movie"],language=row["language"],autoplayScheduled=True)
            programList.append(program)
        #always
        c.execute("SELECT DISTINCT c.id, c.title as channel_title,c.lineup,c.logo,c.stream_url,c.visible,c.weight, p.* FROM programs p, channels c, autoplays a WHERE c.id = p.channel AND a.type = 1 AND p.title = a.program_title AND p.start_date >= ? AND p.end_date <= ?", [start,end])
        for row in c:
            channel = Channel(row["id"], row["channel_title"], row['lineup'], row["logo"], row["stream_url"], row["visible"], row["weight"])
            program = Program(channel, title=row['title'], sub_title=row['sub_title'], startDate=row['start_date'], endDate=row['end_date'],
                            description=row['description'], categories=row['categories'],
                            imageLarge=row["image_large"],imageSmall=row["image_small"],
                            season=row["season"],episode=row["episode"],is_movie=row["is_movie"],language=row["language"],autoplayScheduled=True)
            programList.append(program)
        c.close()
        return programList

    def addAutoplaywith(self, program, type):
        self._invokeAndBlockForResult(self._addAutoplaywith, program, type)
        # no result, but block until operation is done

    def _addAutoplaywith(self, program, type):
        """
        @type program: source.program
        """
        c = self.conn.cursor()
        c.execute("INSERT INTO autoplaywiths(channel, program_title, source, start_date, type) VALUES(?, ?, ?, ?, ?)",
                  [program.channel.id, program.title, self.source.KEY, program.startDate, type])
        self.conn.commit()
        c.close()

    def removeAutoplaywith(self, program):
        self._invokeAndBlockForResult(self._removeAutoplaywith, program)
        # no result, but block until operation is done

    def _removeAutoplaywith(self, program):
        """
        @type program: source.program
        """
        c = self.conn.cursor()
        c.execute("DELETE FROM autoplaywiths WHERE channel=? AND program_title=? AND source=?",
                  [program.channel.id, program.title, self.source.KEY])
        self.conn.commit()
        c.close()

    def getFullAutoplaywiths(self, daysLimit=2):
        return self._invokeAndBlockForResult(self._getFullAutoplaywiths, daysLimit)

    def _getFullAutoplaywiths(self, daysLimit):
        start = datetime.datetime.now()
        end = start + datetime.timedelta(days=daysLimit)
        programList = list()
        c = self.conn.cursor()
        #once
        c.execute("SELECT DISTINCT c.id, c.title as channel_title,c.lineup,c.logo,c.stream_url,c.visible,c.weight, p.* FROM programs p, channels c, autoplaywiths a WHERE c.id = p.channel AND a.type = 0 AND p.title = a.program_title AND a.start_date = p.start_date")
        for row in c:
            channel = Channel(row["id"], row["channel_title"], row["lineup"], row["logo"], row["stream_url"], row["visible"], row["weight"])
            program = Program(channel, title=row['title'], sub_title=row['sub_title'], startDate=row['start_date'], endDate=row['end_date'],
                            description=row['description'], categories=row['categories'],
                            imageLarge=row["image_large"],imageSmall=row["image_small"],
                            season=row["season"],episode=row["episode"],is_movie=row["is_movie"],language=row["language"],autoplaywithScheduled=True)
            programList.append(program)
        #always
        c.execute("SELECT DISTINCT c.id, c.title as channel_title,c.lineup,c.logo,c.stream_url,c.visible,c.weight, p.* FROM programs p, channels c, autoplaywiths a WHERE c.id = p.channel AND a.type = 1 AND p.title = a.program_title AND p.start_date >= ? AND p.end_date <= ?", [start,end])
        for row in c:
            channel = Channel(row["id"], row["channel_title"], row['lineup'], row["logo"], row["stream_url"], row["visible"], row["weight"])
            program = Program(channel, title=row['title'], sub_title=row['sub_title'], startDate=row['start_date'], endDate=row['end_date'],
                            description=row['description'], categories=row['categories'],
                            imageLarge=row["image_large"],imageSmall=row["image_small"],
                            season=row["season"],episode=row["episode"],is_movie=row["is_movie"],language=row["language"],autoplaywithScheduled=True)
            programList.append(program)
        c.close()
        return programList

    def isAutoplayRequiredForProgram(self, program):
        return self._invokeAndBlockForResult(self._isAutoplayRequiredForProgram, program)

    def _isAutoplayRequiredForProgram(self, program):
        """
        @type program: source.program
        """
        c = self.conn.cursor()
        c.execute("SELECT 1 FROM autoplays WHERE channel=? AND program_title=? AND source=?",
                  [program.channel.id, program.title, self.source.KEY])
        result = c.fetchone()
        c.close()

        return result

    def clearAllAutoplays(self):
        self._invokeAndBlockForResult(self._clearAllAutoplays)
        # no result, but block until operation is done

    def _clearAllAutoplays(self):
        c = self.conn.cursor()
        c.execute('DELETE FROM autoplays')
        self.conn.commit()
        c.close()

    def clearAllAutoplaywiths(self):
        self._invokeAndBlockForResult(self._clearAllAutoplaywiths)
        # no result, but block until operation is done

    def _clearAllAutoplaywiths(self):
        c = self.conn.cursor()
        c.execute('DELETE FROM autoplaywiths')
        self.conn.commit()
        c.close()


class Source(object):
    def getDataFromExternal(self, date, ch_list, progress_callback=None):
        """
        Retrieve data from external as a list or iterable. Data may contain both Channel and Program objects.
        The source may choose to ignore the date parameter and return all data available.

        @param date: the date to retrieve the data for
        @param progress_callback:
        @return:
        """
        return None

    def isUpdated(self, channelsLastUpdated, programsLastUpdated=None):
        today = datetime.datetime.now()

        if channelsLastUpdated is None or channelsLastUpdated.day != today.day:
            return True

        if programsLastUpdated is None or programsLastUpdated.day != today.day:
            return True

        return False


class XMLTVSource(Source):
    PLUGIN_DATA = xbmc.translatePath(os.path.join('special://profile', 'addon_data', 'script.tvguide.Vader'))
    KEY = 'xmltv'
    INI_TYPE_FILE = 0
    INI_TYPE_URL = 1
    INI_FILE = 'addons.ini'
    LOGO_SOURCE_FOLDER = 1
    LOGO_SOURCE_URL = 2
    XMLTV_SOURCE_FILE = 0
    XMLTV_SOURCE_URL = 1
    CATEGORIES_TYPE_FILE = 0
    CATEGORIES_TYPE_URL = 1

    def __init__(self, addon, force):
        #gType = GuideTypes()

        self.needReset = False
        self.fetchError = False
        self.xmltvType = int(addon.getSetting('xmltv.type'))
        self.xmltv2Type = int(addon.getSetting('xmltv2.type'))
        self.xmltvInterval = int(addon.getSetting('xmltv.interval'))
        self.logoSource = int(addon.getSetting('logos.source'))
        self.addonsType = int(addon.getSetting('addons.ini.type'))
        self.categoriesType = int(addon.getSetting('categories.ini.type'))
        self.mappingType = int(addon.getSetting('mapping.ini.type'))
        self.m3uType = int(addon.getSetting('mapping.m3u.type'))

        # make sure the folder in the user's profile exists or create it!
        if not os.path.exists(XMLTVSource.PLUGIN_DATA):
            os.makedirs(XMLTVSource.PLUGIN_DATA)

        if self.logoSource == XMLTVSource.LOGO_SOURCE_FOLDER:
            self.logoFolder = addon.getSetting('logos.folder')
        elif self.logoSource == XMLTVSource.LOGO_SOURCE_URL:
            self.logoFolder = addon.getSetting('logos.url')
        else:
            self.logoFolder = ""

        # if self.xmltvType == XMLTVSource.XMLTV_SOURCE_FILE:
        #     #customFile = str(addon.getSetting('xmltv.file'))
        #     '''
        #     if os.path.exists(customFile):
        #         # uses local file provided by user!
        #         xbmc.log('[script.tvguide.Vader] Use local file: %s' % customFile, xbmc.LOGDEBUG)
        #         self.xmltvFile = customFile
        #     else:
        #         # Probably a remote file
        #         xbmc.log('[script.tvguide.Vader] Use remote file: %s' % customFile, xbmc.LOGDEBUG)
        #         self.updateLocalFile(customFile, addon, force=force)
        #         self.xmltvFile = customFile #os.path.join(XMLTVSource.PLUGIN_DATA, customFile.split('/')[-1])
        #     '''
        #     self.xmltvFile = self.updateLocalFile(addon.getSetting('xmltv.file'), addon, force=force)
        # else:
        #     self.xmltvFile = self.updateLocalFile(addon.getSetting('xmltv.url'), addon, force=force)
        #
        self.xmltvFile = ''

        self.xmltv2File = ''
        # if ADDON.getSetting('xmltv2.enabled') == 'true':
        #     if self.xmltv2Type == XMLTVSource.XMLTV_SOURCE_FILE:
        #         '''
        #         customFile = str(addon.getSetting('xmltv2.file'))
        #         if os.path.exists(customFile):
        #             # uses local file provided by user!
        #             xbmc.log('[script.tvguide.Vader] Use local file: %s' % customFile, xbmc.LOGDEBUG)
        #             self.xmltv2File = customFile
        #         else:
        #             # Probably a remote file
        #             xbmc.log('[script.tvguide.Vader] Use remote file: %s' % customFile, xbmc.LOGDEBUG)
        #             self.updateLocalFile(customFile, addon, force=force)
        #             self.xmltv2File = customFile #os.path.join(XMLTVSource.PLUGIN_DATA, customFile.split('/')[-1])
        #         '''
        #         self.xmltv2File = self.updateLocalFile(addon.getSetting('xmltv2.file'), addon, force=force)
        #     else:
        #         self.xmltv2File = self.updateLocalFile(addon.getSetting('xmltv2.url'), addon, force=force)

        if addon.getSetting('categories.ini.enabled') == 'true':
            if self.categoriesType == XMLTVSource.CATEGORIES_TYPE_FILE:
                customFile = str(addon.getSetting('categories.ini.file'))
            else:
                customFile = str(addon.getSetting('categories.ini.url'))
            if customFile:
                self.updateLocalFile(customFile, addon, True, force=force)

        if addon.getSetting('mapping.ini.enabled') == 'true':
            if self.mappingType == XMLTVSource.INI_TYPE_FILE:
                customFile = str(addon.getSetting('mapping.ini.file'))
            else:
                customFile = str(addon.getSetting('mapping.ini.url'))
            if customFile:
                self.updateLocalFile(customFile, addon, True, force=force)
        if addon.getSetting('mapping.m3u.enabled') == 'true':
            if self.m3uType == XMLTVSource.INI_TYPE_FILE:
                customFile = str(addon.getSetting('mapping.m3u.file'))
            else:
                customFile = str(addon.getSetting('mapping.m3u.url'))
            if customFile:
                self.updateLocalFile(customFile, addon, True, force=force)

        d = xbmcgui.Dialog()
        subscription_streams = {}
        if (ADDON.getSetting('addons.ini.subscriptions') == "true"):
            file_name = 'special://home/userdata/addon_data/script.tvguide.Vader/subscriptions.ini'
            f = xbmcvfs.File(file_name,"rb")
            data = f.read()
            f.close()
            name_sub = re.findall('(.*?)=(.*)',data)
            for (name,sub) in name_sub:
                f = xbmcvfs.File(sub,"rb")
                if not f:
                    continue
                data = f.read()
                f.close
                if not data:
                    d.notification("TV Guide","%s - %s" % (name,sub), xbmcgui.NOTIFICATION_ERROR)
                name_stream = re.findall(r'#EXTINF:.*,(.*?)\n(.*?)\n',data,flags=(re.MULTILINE))
                for name,stream in name_stream:
                    if name and stream:
                        name = re.sub('[\|=:\\\/]','',name)
                        subscription_streams[name.strip()] = stream.strip()


        path = "special://profile/addon_data/script.tvguide.Vader/addons.ini"
        if not xbmcvfs.exists(path):
            f = xbmcvfs.File(path,"w")
            f.close()

        addons_ini = "special://profile/addon_data/script.tvguide.Vader/addons.ini"
        addons_ini_local = addons_ini+".local"
        if addon.getSetting('addons.ini.enabled') == 'true':
            if self.addonsType == XMLTVSource.INI_TYPE_FILE:
                customFile = str(addon.getSetting('addons.ini.file'))
            else:
                customFile = str(addon.getSetting('addons.ini.url'))
            if customFile:
                success = xbmcvfs.copy(addons_ini,addons_ini_local)
                success = xbmcvfs.copy(customFile,addons_ini)

        if (ADDON.getSetting('addons.ini.subscriptions') == "true") or (ADDON.getSetting('addons.ini.overwrite') == "1"):
            streams = {}
            streams["script.tvguide.Vader"] = {}
            if (ADDON.getSetting('addons.ini.enabled') == "true") and (ADDON.getSetting('addons.ini.overwrite') == "1"):
                filenames = [addons_ini_local,addons_ini]
            else:
                filenames = [addons_ini]
            for filename in filenames:
                f = xbmcvfs.File(filename,"rb")
                if f:
                    data = f.read()
                    f.close()
                else:
                    continue
                if not data:
                    continue
                lines = data.splitlines()
                for line in lines:
                    match = re.search('^\[(.*?)\]$',line)
                    if match:
                        addon = match.group(1)
                        if addon not in streams:
                            streams[addon] = {}
                    elif line.startswith('#'):
                        pass
                    else:
                        name_stream = line.split('=',1)
                        if len(name_stream) == 2:
                            (name,stream) = name_stream
                            name = name.replace(':','')
                            try:
                                streams[addon][name] = stream
                            except:
                                pass
            if (ADDON.getSetting('addons.ini.subscriptions') == "true"):
                for name in subscription_streams:
                    if name:
                        streams["script.tvguide.Vader"][name] = subscription_streams[name]

            f = xbmcvfs.File(addons_ini,"wb")
            for addon in sorted(streams):
                if streams[addon]:
                    s = "[%s]\n" % addon
                    f.write(s)
                for name in sorted(streams[addon]):
                    stream = streams[addon][name]
                    s = "%s=%s\n" % (name,stream)
                    f.write(s)
            f.close()

        # if not self.xmltvFile or not xbmcvfs.exists(self.xmltvFile):
        #     raise SourceNotConfiguredException()
        #if not self.xmltv2File or not xbmcvfs.exists(self.xmltv2File):
        #    raise SourceNotConfiguredException()



    def updateLocalFile(self, name, addon, isIni=False, force=False):
        return
        fileName = os.path.basename(name)
        path = os.path.join(XMLTVSource.PLUGIN_DATA, fileName)
        fetcher = FileFetcher(name, addon)
        retVal = fetcher.fetchFile(force)
        if retVal == fetcher.FETCH_OK and not isIni:
            self.needReset = True
        elif retVal == fetcher.FETCH_ERROR:
            xbmcgui.Dialog().ok(strings(FETCH_ERROR_TITLE), strings(FETCH_ERROR_LINE1), strings(FETCH_ERROR_LINE2))
        return path

    def getDataFromExternal(self, date, ch_list, progress_callback=None):
        # if not xbmcvfs.exists(self.xmltvFile):
        #     raise SourceNotConfiguredException()
        # if (ADDON.getSetting('xmltv2.enabled') == 'true') and xbmcvfs.exists(self.xmltv2File):
        #     for v in chain(self.getDataFromExternal2(self.xmltvFile, date, ch_list, progress_callback), self.getDataFromExternal2(self.xmltv2File, date, ch_list, progress_callback)):
        #         yield v
        # else:
        #     for v in chain(self.getDataFromExternal2(self.xmltvFile, date, ch_list, progress_callback)):
        #         yield v

        tries = 0
        streams = None
        streamsTxt = 'Not Ready'
        while tries < 5 and streams == None:
            try:
                xbmc.log('[script.tvguide.Vader] trying to get stream list ' + str(tries), xbmc.LOGNOTICE)

                streamsTxt = requests.get('http://localhost:62555/getStreams').text
                xbmc.log('[script.tvguide.Vader] got streams', xbmc.LOGNOTICE)

                streams = json.loads(streamsTxt)
                credsTxt = requests.get('http://localhost:62555/getCreds').text
                xbmc.log('[script.tvguide.Vader] got creds', xbmc.LOGNOTICE)

                creds = json.loads(credsTxt)
                username = creds['username']
                password = creds['password']
            except:
                time.sleep(2)
                tries = tries + 1
                # tb = traceback.format_exc()
                xbmc.log('[script.tvguide.Vader] ' + str(tb), xbmc.LOGNOTICE)
                xbmc.log('[script.tvguide.Vader] streams response: ' + streamsTxt, xbmc.LOGNOTICE )
                pass

        from HTMLParser import HTMLParser
        h = HTMLParser()
        valid_streams = []
        for stream in streams:

            cid = str(stream['id'])
            valid_streams.append(cid)
            title = stream['stream_display_name']
            streamUrl = None
            visible = 1
            logo = stream['stream_icon']
            result = Channel(cid, title, '', logo, streamUrl, visible)
            yield result

        today = datetime.datetime.utcnow()
        epgLimit = ADDON.getSetting('epg.limit6')
        if epgLimit == 'true':
            epgLimit = True
        else:
            epgLimit = False

        if epgLimit == True:
            try:
                subDays = today - datetime.timedelta(hours=6)
                epgStart = subDays.strftime("%Y%m%d%H%M%S")
                addDays = today + datetime.timedelta(hours=6)
                epgEnd = addDays.strftime("%Y%m%d%H%M%S")
            except:
                tb = traceback.format_exc()
                xbmc.log('[script.tvguide.Vader] ' + str(tb), xbmc.LOGNOTICE)

        else:
            if ADDON.getSetting('epg.forward') == "0":
                addDays = today + datetime.timedelta(days=1)
            elif ADDON.getSetting('epg.forward') == "1":
                addDays = today + datetime.timedelta(days=3)
            elif ADDON.getSetting('epg.forward') == "2":
                addDays = today + datetime.timedelta(days=5)
            if ADDON.getSetting('epg.back') == "0":
                subDays = today - datetime.timedelta(days=1)
            elif ADDON.getSetting('epg.back') == "1":
                subDays = today - datetime.timedelta(days=2)
            elif ADDON.getSetting('epg.back') == "2":
                subDays = today - datetime.timedelta(days=3)
            epgStart = subDays.strftime("%Y%m%d000000")
            epgEnd = addDays.strftime("%Y%m%d%H%M%S")
        dialog = xbmcgui.DialogProgressBG()

        i = 0

        # for stream_id in valid_streams:
        #     epgUrl = 'http://vaders.tv/epg?gzip=true&start={epgStart}&end={epgEnd}&stream_id={stream_id}'.format(stream_id=stream_id,epgStart=epgStart, epgEnd=epgEnd)
        epgUrl = 'http://vapi.vaders.tv/epg/channels?username={username}&password={password}&start={epgStart}&end={epgEnd}'.format(epgStart=epgStart, epgEnd=epgEnd, username=username, password=password)

        # xbmc.log('[script.tvguide.Vader] ' + str(epgUrl), xbmc.LOGNOTICE)

        programsReq = requests.get(epgUrl, timeout=120)
        programsReq.encoding = 'utf-8'
        programsText = programsReq.text

        # programsText = unicode(programsText, 'utf-8')
        xbmc.log('[script.tvguide.Vader] downloaded json txt', xbmc.LOGNOTICE)

        channels = json.loads(programsText, encoding='utf-8')

        xbmc.log('[script.tvguide.Vader] loaded json epg', xbmc.LOGNOTICE)
        totalCount = len(channels)
        dialog.create('EPG Updater', 'Updating EPG...')
        del programsText
        del programsReq

        for channel in channels:
            i = i + 1

            try:
                    cid = str(channel['id'])
                    if cid in valid_streams:
                        for program in channel['programs']:
                            if 'title' in program:
                                title = program['title']

                                # xbmc.log('adding : ' + str(title), xbmc.LOGNOTICE)
                                try:
                                    dialog.update(int(self.percentage(i, totalCount)), 'Loading EPG Data From Server',
                                              'Updating...')
                                except:
                                    pass
                                sub_title = None


                                startTime =  dateutil.parser.parse(program['start'])
                                stopTime =  dateutil.parser.parse(program['stop'])

                                startTimeLocal = UTCToLocal(startTime)
                                stopTimeLocal = UTCToLocal(stopTime)

                                startTime = time.mktime(startTimeLocal.timetuple())
                                stopTime = time.mktime(stopTimeLocal.timetuple())


                                if 'desc' in program:
                                    description = program['desc']
                                else:
                                    description = None
                                catString = ''
                                if 'category' in program:
                                    categoriesList = program['category']
                                    if type(categoriesList) == type(list()):
                                        for category in categoriesList:
                                            if  type(category) == type(dict()):
                                                try:
                                                    catString = catString + str(category['content'].encode('utf-8').decode('ascii', 'ignore'))
                                                except:
                                                    tb = traceback.format_exc()
                                                    xbmc.log('[script.tvguide.Vader] ' + str(tb), xbmc.LOGNOTICE)
                                                    pass
                                            else:
                                                catString = catString + str(category)

                                    else:
                                        catString = categoriesList



                                smallIcon = None
                                if 'icon' in program:
                                    smallIcon = program['icon']['src']

                                if description and type(description) == type(unicode()):
                                    description = h.unescape(description)


                                result = Program(cid, title, sub_title, startTime,stopTime, description, catString, imageSmall=smallIcon,
                                                 season = None, episode = None, is_movie = None, language= None)
                                yield result
                #
                    # else:
                    #     xbmc.log('[script.tvguide.Vader] ' + str(program), xbmc.LOGNOTICE)
            except:
                if dialog:
                    dialog.close()
                # xbmc.log('[script.tvguide.Vader] ' + str(program), xbmc.LOGNOTICE)
                tb = traceback.format_exc()
                xbmc.log('[script.tvguide.Vader] ' + str(tb), xbmc.LOGNOTICE)



        dialog.close()




    # def getDataFromExternal2(self, xmltvFile, date, ch_list, progress_callback=None):
    #     if xbmcvfs.exists(xmltvFile):
    #         f = FileWrapper(xmltvFile)
    #         if f:
    #             context = ElementTree.iterparse(f, events=("start", "end"))
    #             size = f.size
    #             return self.parseXMLTV(context, f, size, self.logoFolder, progress_callback)


    def percentage(self, part, whole):
        return 100 * float(part) / float(whole)

    def isUpdated(self, channelsLastUpdated, programsLastUpdated=None):
        today = datetime.datetime.now()

        if channelsLastUpdated is None or channelsLastUpdated.day != today.day:
            return True


        if programsLastUpdated is None or programsLastUpdated.day != today.day:
            return True

        return False



    def parseXMLTVDate(self, origDateString):
        if origDateString.find(' ') != -1:
            # get timezone information
            dateParts = origDateString.split()
            if len(dateParts) == 2:
                dateString = dateParts[0]
                offset = dateParts[1]
                if len(offset) == 5:
                    offSign = offset[0]
                    offHrs = int(offset[1:3])
                    offMins = int(offset[-2:])
                    td = datetime.timedelta(minutes=offMins, hours=offHrs)
                else:
                    td = datetime.timedelta(seconds=0)
            elif len(dateParts) == 1:
                dateString = dateParts[0]
                td = datetime.timedelta(seconds=0)
            else:
                return None

            # normalize the given time to UTC by applying the timedelta provided in the timestamp
            try:
                t_tmp = datetime.datetime.strptime(dateString, '%Y%m%d%H%M%S')
            except TypeError:
                # xbmc.log('[script.tvguide.Vader] strptime error with this date: %s' % dateString, xbmc.LOGDEBUG)
                t_tmp = datetime.datetime.fromtimestamp(time.mktime(time.strptime(dateString, '%Y%m%d%H%M%S')))
            if offSign == '+':
                t = t_tmp - td
            elif offSign == '-':
                t = t_tmp + td
            else:
                t = t_tmp

            # get the local timezone offset in seconds
            is_dst = time.daylight and time.localtime().tm_isdst > 0
            utc_offset = - (time.altzone if is_dst else time.timezone)
            td_local = datetime.timedelta(seconds=utc_offset)

            t = t + td_local

            return t

        else:
            return None

    def parseXMLTV(self, context, f, size, logoFolder, progress_callback):
        import datetime
        try:
            throwaway = datetime.datetime.strptime('20110101','%Y%m%d') #BUG FIX http://stackoverflow.com/questions/16309650/python-importerror-for-strptime-in-spyder-for-windows-7
        except:
            tb = traceback.format_exc()
            xbmc.log('[script.tvguide.Vader] ' + str(tb), xbmc.LOGNOTICE)
            pass
        event, root = context.next()
        elements_parsed = 0

        data = xbmcvfs.File('special://profile/addon_data/script.tvguide.Vader/channel_id_shortcut.ini','rb').read()
        id_shortcuts = {}
        if data:
            lines = data.splitlines()
            for line in lines:
                id_shortcut = line.split("=")
                if len(id_shortcut) == 2:
                    id_shortcuts[id_shortcut[0]] = id_shortcut[1]
        if self.logoSource == XMLTVSource.LOGO_SOURCE_FOLDER:
            dirs, files = xbmcvfs.listdir(logoFolder)
            logos = [file[:-4] for file in files if file.endswith(".png")]
        if ADDON.getSetting('update.progress') == 'true':
            d = xbmcgui.DialogProgressBG()
            d.create('TV Guide', "parsing xmltv")
        category_count = {}
        for event, elem in context:
            if event == "end":
                result = None
                if elem.tag == "programme":
                    channel = elem.get("channel").replace("'", "")  # Make ID safe to use as ' can cause crashes!
                    description = elem.findtext("desc")
                    date = elem.findtext("date")
                    iconElement = elem.find("icon")
                    icon = None
                    if iconElement is not None:
                        icon = iconElement.get("src")
                    if not description:
                        description = strings(NO_DESCRIPTION)

                    season = None
                    episode = None
                    is_movie = None
                    title = elem.findtext('title')
                    sub_title = elem.findtext('sub-title')
                    category = elem.findall('category')
                    category_list = []
                    for c in category:
                        txt = c.text
                        if txt:
                            if txt in category_count:
                                category_count[txt] = category_count[txt] + 1
                            else:
                                category_count[txt] = 1
                            category_list.append(txt)
                    categories = ','.join(category_list)
                    if ADDON.getSetting('xmltv.date') == 'true' and date and re.match("^[0-9]{4}$",date):
                        is_movie = "Movie"
                        title = "%s (%s)" % (title,date)
                    language = elem.find("title").get("lang")

                    episode_num = elem.findtext("episode-num")
                    meta_categories = elem.findall("category")
                    for category in meta_categories:
                        if "movie" in category.text.lower() or channel.lower().find("sky movies") != -1 \
                                or "film" in category.text.lower():
                            is_movie = "Movie"
                            break

                    if episode_num is not None:
                        episode_num = unicode.encode(unicode(episode_num), 'ascii','ignore')
                        if str.find(episode_num, ".") != -1:
                            splitted = str.split(episode_num, ".")
                            if splitted[0] != "":
                                #TODO fix dk format
                                try:
                                    season = int(splitted[0]) + 1
                                    is_movie = None # fix for misclassification
                                    if str.find(splitted[1], "/") != -1:
                                        episode = int(splitted[1].split("/")[0]) + 1
                                    elif splitted[1] != "":
                                        episode = int(splitted[1]) + 1
                                except:
                                    episode = ""
                                    season = ""

                        elif str.find(episode_num.lower(), "season") != -1 and episode_num != "Season ,Episode ":
                            pattern = re.compile(r"Season\s(\d+).*?Episode\s+(\d+).*",re.I|re.U)
                            match = re.search(pattern,episode_num)
                            if match:
                                season = int(match.group(1))
                                episode = int(match.group(2))
                        else:
                            pattern = re.compile(r"S([0-9]+)E([0-9]+)",re.I|re.U)
                            match = re.search(pattern,episode_num)
                            if match:
                                season = int(match.group(1))
                                episode = int(match.group(2))
                    if channel in id_shortcuts:
                        cid = id_shortcuts[channel]
                    else:
                        cid = channel
                    result = Program(cid, title, sub_title, self.parseXMLTVDate(elem.get('start')),
                                     self.parseXMLTVDate(elem.get('stop')), description, categories, imageSmall=icon,
                                     season = season, episode = episode, is_movie = is_movie, language= language)

                elif elem.tag == "channel":
                    logo = ''
                    cid = elem.get("id").replace("'", "")  # Make ID safe to use as ' can cause crashes!
                    title = elem.findtext("display-name")
                    use_thelogodb = False
                    if ADDON.getSetting('thelogodb') == "2":
                        use_thelogodb = True
                    else:
                        iconElement = elem.find("icon")
                        icon = None
                        if iconElement is not None:
                            icon = iconElement.get("src")
                        logo = ''
                        if icon and ADDON.getSetting('xmltv.logos'):
                            logo = icon
                        if logoFolder:
                            logoFile = os.path.join(logoFolder, title + '.png')
                            if self.logoSource == XMLTVSource.LOGO_SOURCE_URL:
                                logo = logoFile.replace(' ', '%20')
                            #elif xbmcvfs.exists(logoFile): #BUG case insensitive match but won't load image
                            #    logo = logoFile
                            else:
                                #TODO use hash or db
                                t = re.sub(r' ','',title.lower())
                                t = re.escape(t)
                                titleRe = "^%s" % t
                                for l in sorted(logos):
                                    logox = re.sub(r' ','',l.lower())
                                    if re.match(titleRe,logox):
                                        logo = os.path.join(logoFolder, l + '.png')
                                        break

                    if use_thelogodb or (not logo and ADDON.getSetting('thelogodb') == "1"):
                        if ADDON.getSetting('logos.keep') == 'false':
                            logo = getLogo(title,False,False)

                    streamElement = elem.find("stream")
                    streamUrl = None
                    if streamElement is not None:
                        streamUrl = streamElement.text
                    visible = elem.get("visible")
                    if visible == "0":
                        visible = False
                    else:
                        visible = True
                    if cid in id_shortcuts:
                        cid = id_shortcuts[cid]
                    result = Channel(cid, title, '', logo, streamUrl, visible)
                    channel = title

                if result:
                    elements_parsed += 1
                    if progress_callback and elements_parsed % 500 == 0:
                        percent = 100.0 / size * f.tell()
                        if ADDON.getSetting('update.progress') == 'true':
                            d.update(int(percent), message=channel)
                        if not progress_callback(percent):
                            raise SourceUpdateCanceledException()
                    yield result

            root.clear()
        f.close()
        if ADDON.getSetting('update.progress') == 'true':
            d.update(100, message="Done")
            d.close()
        f = xbmcvfs.File('special://profile/addon_data/script.tvguide.Vader/category_count.ini',"wb")
        for c in sorted(category_count):
            s = "%s=%s\n" % (c, category_count[c])
            f.write(s.encode("utf8"))
        f.close()

class FileWrapper(object):
    def __init__(self, filename):
        self.vfsfile = xbmcvfs.File(filename,"rb")
        self.size = self.vfsfile.size()
        self.bytesRead = 0

    def close(self):
        self.vfsfile.close()

    def read(self, byteCount):
        self.bytesRead += byteCount
        return self.vfsfile.read(byteCount)

    def tell(self):
        return self.bytesRead



def instantiateSource(force):
    source_arg = ADDON.getSetting("source")
    if source_arg:
        source = source_arg
    else:
        source = ADDON.getSetting("source.source")
    if source == "xmltv":
        return XMLTVSource(ADDON,force)
