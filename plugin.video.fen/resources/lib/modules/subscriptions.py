import xbmc, xbmcgui, xbmcaddon, xbmcvfs
import os
try: from sqlite3 import dbapi2 as database
except ImportError: from pysqlite2 import dbapi2 as database
from resources.lib.modules.text import to_unicode
from resources.lib.modules.nav_utils import notification
from resources.lib.modules.utils import to_utf8
import tikimeta
from resources.lib.indexers.tvshows import make_fresh_tvshow_meta
from resources.lib.modules import settings
from resources.lib.modules.utils import logger

__addon__ = xbmcaddon.Addon(id='plugin.video.fen')
__addon_profile__ = xbmc.translatePath(__addon__.getAddonInfo('profile'))

class Subscriptions:
    def __init__(self, db_type=None, tmdb_id=None, action=None, orig_mode=None):
        self.sub_database = os.path.join(__addon_profile__, 'subscriptions.db')
        self.db_type = db_type
        self.tmdb_id = tmdb_id
        self.action = action
        self.orig_mode = orig_mode
        if self.db_type: self.path = settings.movies_directory() if self.db_type == 'movie' else settings.tv_show_directory()
        settings.check_database(self.sub_database)

    def add_remove(self):
        self.add_remove_constants()
        if self.check_exists_database() and self.action == 'add':
            return notification('{}'.format('[B]%s[/B] already in Subscriptions' % self.rootname), 4500)
        self.add_remove_movie() if self.db_type == 'movie' else self.add_remove_tvshow()
        if self.orig_mode in ('subscriptions_tvshows', 'subscriptions_movies') and self.action == 'remove':
            xbmc.executebuiltin('Container.Refresh')

    def add_remove_movie(self, silent=False):
        from resources.lib.modules.utils import to_utf8
        from resources.lib.modules.kodi_library import get_library_video
        self.add_remove_database()
        if self.action == 'add':
            in_library = get_library_video('movie', self.title, self.year) if settings.skip_duplicates() else False
            if in_library: return
            self.make_folder()
            self.make_nfo()
            stream_file = self.create_movie_strm_files()
            params = to_utf8({'mode': 'play_media', 'library': 'True', 'query': self.rootname, 'poster': self.meta['poster'], 'year': self.year, 'plot': self.meta['plot'], 'title': self.title, 'tmdb_id': self.meta['tmdb_id'], 'vid_type':'movie'})
            self.make_stream(stream_file, params)
        elif self.action == 'remove':
            self.remove_folder()
        if not silent: notification('{}'.format(self.notify % self.rootname), 4500)

    def add_remove_tvshow(self, silent=False):
        self.add_remove_database()
        if self.action == 'add':
            self.make_folder()
            self.make_nfo()
            self.create_tvshow_strm_files()
        elif self.action == 'remove':
            self.remove_folder()
        if not silent: notification('{}'.format(self.notify % self.rootname), 4500)

    def get_subscriptions(self):
        dbcon = database.connect(self.sub_database)
        dbcur = dbcon.cursor()
        dbcur.execute('''SELECT tmdb_id, title FROM subscriptions WHERE db_type=?''', (self.db_type,))
        result = dbcur.fetchall()
        result = [{'tmdb_id': str(i[0]), 'title': str(to_utf8(i[1]))} for i in result]
        return result

    def clear_subscriptions(self, confirm=True, silent=False):
        if confirm:
            if not self.subscription_choice('Choose Subscriptions to Erase', 'Continuing will erase all your {}'): return
        self.db_type = self.choice[1]
        self.path = settings.movies_directory() if self.db_type == 'movie' else settings.tv_show_directory()
        subscriptions = self.get_subscriptions()
        if len(subscriptions) == 0:
            return notification('{}'.format('%s Subscriptions is already empty' % self.db_type.upper()), 4500)
        self.remove_folder(self.path)
        self.make_folder(self.path)
        dbcon = database.connect(self.sub_database, timeout=40.0)
        dbcur = dbcon.cursor()
        for item in subscriptions:
            dbcur.execute("DELETE FROM subscriptions where db_type=? and tmdb_id=?", (self.db_type, item['tmdb_id']))
        dbcur.execute("VACUUM")
        dbcon.commit()
        dbcon.close()
        if not silent: notification('{}'.format('%s Subscriptions has been cleared' % self.db_type.upper()), 4500)

    def remake_subscriptions(self):
        if not self.subscription_choice('Choose Subscriptions to Remake', 'Continuing will remake all your {}'):
            return
        self.db_type = self.choice[1]
        self.action = 'add'
        self.path = settings.movies_directory() if self.db_type == 'movie' else settings.tv_show_directory()
        subscriptions = self.get_subscriptions()
        if len(subscriptions) == 0:
            return notification('{}'.format('%s Subscriptions is empty' % self.db_type.upper()), 4500)
        self.clear_subscriptions(confirm=False, silent=True)
        bg_dialog = xbmcgui.DialogProgress()
        bg_dialog.create('Please Wait', '')
        for count, item in enumerate(subscriptions, 1):
            display = 'Fen Updating %s' % self.choice[0]
            bg_dialog.update(int(float(count) / float(len(subscriptions)) * 100), 'Please Wait', '%s' % display)
            self.tmdb_id = item['tmdb_id']
            self.add_remove_constants()
            self.add_remove_movie(silent=True) if self.db_type == 'movie' else self.add_remove_tvshow(silent=True)
            xbmc.sleep(300)
        bg_dialog.close()
        notification('All %s remade' % self.choice[0], 4500)

    def update_subscriptions(self):
        from datetime import datetime, timedelta
        from resources.lib.modules.nav_utils import close_all_dialog
        self.db_type = 'tvshow'
        self.action = 'add'
        self.path = settings.tv_show_directory()
        subscriptions = self.get_subscriptions()
        if not subscriptions:
            return notification('{0}'.format('No TV Show Subscriptions to update'), 1200)
        hours = settings.subscription_timer()
        close_all_dialog()
        bg_dialog = xbmcgui.DialogProgressBG()
        bg_dialog.create('Please Wait', 'Preparing Subscription Update...')
        for count, item in enumerate(subscriptions, 1):
            self.tmdb_id = item['tmdb_id']
            self.add_remove_constants()
            self.add_remove_tvshow(silent=True)
            display = 'Fen Updating - [B][I]%s[/I][/B]' % self.rootname
            bg_dialog.update(int(float(count) / float(len(subscriptions)) * 100), 'Please Wait', '%s' % display)
            xbmc.sleep(300)
        __addon__.setSetting('service_time', str(datetime.now() + timedelta(hours=hours)).split('.')[0])
        bg_dialog.close()
        notification('{}'.format('Fen Subscriptions Updated'), 4500)
        if settings.update_library_after_service(): xbmc.executebuiltin('UpdateLibrary(video)')

    def add_list_to_subscriptions(self, user, list_slug):
        if not xbmcgui.Dialog().yesno('Are you sure?','Fen will add all Movies and/or TV Shows from this list to your Fen Subscriptions. Do you wish to continue?'):
            return
        from resources.lib.modules.trakt import call_trakt
        info = []
        self.action = 'add'
        bg_dialog = xbmcgui.DialogProgressBG()
        bg_dialog.create('Please Wait', 'Preparing Trakt List Info...')
        data = call_trakt("users/{0}/lists/{1}/items?extended=full".format(user, list_slug), method='sort_by_headers')
        for count, item in enumerate(data, 1):
            try:
                self.db_type, trakt_type = ('movie', 'movie') if item['type'] == 'movie' else ('tvshow', 'show')
                ids = item[trakt_type]['ids']
                self.tmdb_id = ids['tmdb']
                self.path = settings.movies_directory() if self.db_type == 'movie' else settings.tv_show_directory()
                self.add_remove_constants()
                self.add_remove_movie(silent=True) if self.db_type == 'movie' else self.add_remove_tvshow(silent=True)
                display = 'Adding to Subscriptions: [I][B]%s[/B][/I]' % self.rootname
                bg_dialog.update(int(float(count) / float(len(data)) * 100), 'Please Wait', '%s' % display)
            except: pass
        bg_dialog.close()
        notification('List added to Subscriptions', 4500)
        return True

    def create_movie_strm_files(self):
        return os.path.join(self.folder, self.rootname + '.strm')

    def create_tvshow_strm_files(self):
        from datetime import date
        from resources.lib.modules.utils import to_utf8
        from resources.lib.modules.kodi_library import get_library_video
        skip_duplicates = settings.skip_duplicates()
        season_data = [i for i in self.meta['season_data'] if int(i['season_number']) > 0]
        for i in season_data:
            infoLabels = tikimeta.season_episodes_meta(self.tmdb_id, i['season_number'])
            ep_data = infoLabels['episodes']
            for item in ep_data:
                in_library = get_library_video('episode', self.title, self.year, item['season_number'], item['episode_number']) if skip_duplicates else None
                if not in_library:
                    first_aired = item['air_date'] if 'air_date' in item else None
                    try:
                        d = first_aired.split('-')
                        episode_date = date(int(d[0]), int(d[1]), int(d[2]))
                    except: episode_date = date(2100,10,24)
                    if date.today() > episode_date:
                        display = "%s S%.2dE%.2d" % (self.title, int(item['season_number']), int(item['episode_number']))
                        season_path = os.path.join(self.folder, 'Season ' + str(item['season_number']))
                        self.make_folder(season_path)
                        stream_file = os.path.join(season_path, str(display) + '.strm')
                        params = to_utf8({'mode': 'play_media', 'library': 'True', 'query': self.title, 'year': self.year, 'plot': item['overview'], 'poster': self.meta['poster'], 'season': item['season_number'], 'episode': item['episode_number'], 'ep_name': item['name'], 'premiered': item['air_date'], 'tmdb_id': self.tmdb_id, 'vid_type':'episode'})
                        self.make_stream(stream_file, params)

    def make_folder(self, folder=None):
        folder = self.folder if not folder else folder
        xbmcvfs.mkdir(folder)

    def remove_folder(self, folder=None):
        folder = self.folder if not folder else folder
        xbmcvfs.rmdir(folder, True)

    def make_nfo(self):
        if not xbmcvfs.exists(self.nfo_filepath):
            nfo_file = xbmcvfs.File(self.nfo_filepath, 'w')
            nfo_file.write(self.nfo_content)
            nfo_file.close()

    def make_stream(self, stream_file, params):
        if not xbmcvfs.exists(stream_file):
            from resources.lib.modules.nav_utils import build_url
            file = xbmcvfs.File(stream_file, 'w')
            content = build_url(params)
            file.write(str(content))
            file.close()

    def add_remove_database(self):
        dbcon = database.connect(self.sub_database, timeout=40.0)
        dbcur = dbcon.cursor()
        dbcur.execute(self.db_action, (self.db_type, self.tmdb_id, to_unicode(self.title)))
        dbcon.commit()
        dbcon.close()

    def check_exists_database(self):
        db_object_exists = True
        dbcon = database.connect(self.sub_database, timeout=40.0)
        dbcur = dbcon.cursor()
        dbcur.execute('''SELECT tmdb_id FROM subscriptions WHERE db_type=? AND tmdb_id=?''', (self.db_type, self.tmdb_id))
        try: str(dbcur.fetchone()[0])
        except: db_object_exists = False
        dbcon.close()
        return db_object_exists

    def add_remove_constants(self):
        from resources.lib.modules.utils import clean_file_name
        meta_action = tikimeta.movie_meta if self.db_type == 'movie' else make_fresh_tvshow_meta
        self.meta = meta_action('tmdb_id', self.tmdb_id)
        self.title = clean_file_name(self.meta['title'])
        self.year = self.meta['year'] if 'year' in self.meta else ''
        self.rootname = '{0} ({1})'.format(self.title, self.year) if self.year else self.title
        self.folder = os.path.join(self.path, self.rootname + '/')
        self.nfo_filename = self.rootname + '.nfo' if self.db_type == 'movie' else 'tvshow.nfo'
        self.nfo_filepath = os.path.join(self.folder, self.nfo_filename)
        self.nfo_content = "https://www.themoviedb.org/movie/%s-%s" % (str(self.meta['tmdb_id']), self.title.replace(' ', '-')) if self.db_type == 'movie' else "https://www.imdb.com/title/%s/" % str(self.meta['imdb_id'])
        self.notify = '[B]%s[/B] added to Subscriptions' if self.action == 'add' else '[B]%s[/B] removed from Subscriptions'
        self.db_action = "INSERT OR IGNORE INTO subscriptions VALUES (?, ?, ?)" if self.action == 'add' else "DELETE FROM subscriptions where db_type=? and tmdb_id=? and title=?"

    def subscription_choice(self, heading, message):
        sl = [('Movie Subscriptions', 'movie'), ('TV Show Subscriptions', 'tvshow')]
        choice = xbmcgui.Dialog().select(heading, [i[0] for i in sl])
        if choice < 0: return
        confirm = xbmcgui.Dialog().yesno('Are you sure?', message.format(sl[choice][0]))
        if not confirm: return False
        self.choice = sl[choice]
        return True

def retrieve_subscriptions(db_type, page_no, letter, passed_list=[]):
    import ast
    from resources.lib.modules.nav_utils import paginate_list
    from resources.lib.modules.utils import title_key
    limit = 40
    if not passed_list:
        data = Subscriptions(db_type).get_subscriptions()
        logger('data', data)
        data = sorted(data, key=lambda k: title_key(k['title']))
        original_list = [{'media_id': i['tmdb_id'], 'title': i['title']} for i in data]
    else: original_list = ast.literal_eval(passed_list)
    paginated_list, total_pages = paginate_list(original_list, page_no, letter, limit)
    return paginated_list, original_list, total_pages, limit







    