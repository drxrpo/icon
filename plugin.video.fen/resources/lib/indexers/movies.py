import xbmc, xbmcgui, xbmcplugin, xbmcaddon
import sys, os
import json
from urlparse import parse_qsl
from resources.lib.modules.nav_utils import build_url, setView, remove_unwanted_info_keys
from resources.lib.modules.indicators_bookmarks import get_watched_status, get_resumetime
from resources.lib.modules.trakt import sync_watched_trakt_to_fen, get_trakt_movie_id
from resources.lib.modules import workers
from resources.lib.modules import settings
import tikimeta
# from resources.lib.modules.utils import logger

__addon_id__ = 'plugin.video.fen'
__addon__ = xbmcaddon.Addon(id=__addon_id__)
__handle__ = int(sys.argv[1])
dialog = xbmcgui.Dialog()
not_widget = xbmc.getInfoLabel('Container.PluginName')

class Movies:
    def __init__(self, _list=None, idtype=None, action=None):
        self.list = [] if not _list else _list
        self.items = []
        self.new_page = None
        self.total_pages = None
        self.id_type = 'tmdb_id' if not idtype else idtype
        self.action = action
        sync_watched_trakt_to_fen()

    def fetch_list(self):
        try:
            params = dict(parse_qsl(sys.argv[2].replace('?','')))
            worker = True
            mode = params.get('mode')
            page_no = int(params.get('new_page', 1))
            letter = params.get('new_letter', 'None')
            search_name = ''
            content_type = 'movies'
            var_module = 'tmdb' if 'tmdb' in self.action else 'trakt' if 'trakt' in self.action else 'imdb' if 'imdb' in self.action else ''
            try: exec('from resources.lib.modules.%s import %s as function' % (var_module, self.action))
            except: pass
            if self.action in ('tmdb_movies_popular','tmdb_movies_blockbusters','tmdb_movies_in_theaters',
                'tmdb_movies_top_rated','tmdb_movies_upcoming','tmdb_movies_latest_releases','tmdb_movies_premieres',
                'trakt_movies_trending','trakt_movies_anticipated','trakt_movies_top10_boxoffice'):
                data = function(page_no)
                if 'tmdb' in self.action:
                    for item in data['results']: self.list.append(item['id'])
                else:
                    for item in data: self.list.append(get_trakt_movie_id(item))
                if self.action not in ('trakt_movies_top10_boxoffice'): self.new_page = {'mode': mode, 'action': self.action, 'new_page': str((data['page'] if 'tmdb' in self.action else page_no) + 1), 'foldername': self.action}
            elif self.action in ('trakt_collection', 'trakt_watchlist'):
                data, passed_list, total_pages, limit = function('movies', page_no, letter, params.get('passed_list', ''))
                self.list = [i['media_id'] for i in data]
                if total_pages > 1: self.total_pages = total_pages
                if len(data) == limit: self.new_page = {'mode': mode, 'action': self.action, 'new_page': str(page_no + 1), 'new_letter': letter, 'passed_list': passed_list, 'foldername': self.action}
            elif self.action == 'imdb_movies_oscar_winners':
                self.id_type = 'imdb_id'
                self.list = function(page_no)
                self.new_page = {'mode': mode, 'action': self.action, 'new_page': str(page_no + 1), 'foldername': self.action}
            elif self.action == ('trakt_movies_mosts'):
                for item in (function(params['period'], params['duration'], page_no)): self.list.append(get_trakt_movie_id(item))
                self.new_page = {'mode': mode, 'action': self.action, 'period': params['period'], 'duration': params['duration'], 'new_page': str(page_no + 1), 'foldername': self.action}
            elif self.action == 'tmdb_movies_genres':
                genre_id = params['genre_id'] if 'genre_id' in params else self.multiselect_genres(params.get('genre_list'))
                if not genre_id: return
                data = function(genre_id, page_no)
                self.list = [i['id'] for i in data['results']]
                if data['page'] < data['total_pages']: self.new_page = {'mode': mode, 'action': self.action, 'new_page': str(data['page'] + 1), 'genre_id': genre_id, 'foldername': genre_id}
            elif self.action == 'tmdb_movies_languages':
                language = params['language']
                if not language: return
                data = function(language, page_no)
                self.list = [i['id'] for i in data['results']]
                if data['page'] < data['total_pages']: self.new_page = {'mode': mode, 'action': self.action, 'new_page': str(data['page'] + 1), 'language': language, 'foldername': language}
            elif self.action == 'tmdb_movies_year':
                data = function(params['year'], page_no)
                self.list = [i['id'] for i in data['results']]
                if data['page'] < data['total_pages']: self.new_page = {'mode': mode, 'action': self.action, 'new_page': str(data['page'] + 1), 'year': params.get('year'), 'foldername': params.get('year')}
            elif self.action == 'tmdb_movies_certifications':
                data = function(params['certification'], page_no)
                self.list = [i['id'] for i in data['results']]
                if data['page'] < data['total_pages']: self.new_page = {'mode': mode, 'action': self.action, 'new_page': str(data['page'] + 1), 'certification': params.get('certification'), 'foldername': params.get('certification')}
            elif self.action in ('favourites_movies', 'subscriptions_movies', 'kodi_library_movies', 'watched_movies'):
                (var_module, import_function) = ('favourites', 'retrieve_favourites') if 'favourites' in self.action else ('subscriptions', 'retrieve_subscriptions') if 'subscriptions' in self.action else ('indicators_bookmarks', 'get_watched_items') if 'watched' in self.action else ('kodi_library', 'retrieve_kodi_library') if 'library' in self.action else ''
                try: exec('from resources.lib.modules.%s import %s as function' % (var_module, import_function))
                except: return
                if self.action == 'kodi_library_movies': self.id_type = 'imdb_id'
                data, passed_list, total_pages, limit = function('movie', page_no, letter, params.get('passed_list', ''))
                self.list = [i['media_id'] for i in data]
                if total_pages > 1: self.total_pages = total_pages
                if len(data) == limit: self.new_page = {'mode': mode, 'action': self.action, 'new_page': str(page_no + 1), 'new_letter': letter, 'passed_list': passed_list, 'foldername': self.action}
            elif self.action == 'in_progress_movies':
                from resources.lib.modules.in_progress import in_progress_movie as function
                self.list = function('movie')
                xbmcplugin.addSortMethod(__handle__, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
            elif self.action == 'tmdb_movies_similar':
                data = function(params['tmdb_id'], page_no)
                self.list = [i['id'] for i in data['results']]
                if data['page'] < data['total_pages']: self.new_page = {'mode': mode, 'action': self.action, 'new_page': str(data['page'] + 1), 'foldername': self.action, 'tmdb_id': params.get('tmdb_id')}
            elif self.action == 'trakt_movies_related':
                for item in function(params['imdb_id'], page_no): self.list.append(get_trakt_movie_id(item))
                self.new_page = {'mode': mode, 'action': self.action, 'new_page': str(int((params.get('new_page') if 'new_page' in params else 1)) + 1), 'foldername': self.action, 'imdb_id': params.get('imdb_id')}
            elif self.action == 'trakt_recommendations':
                for item in function('movies'): self.list.append(item['ids']['tmdb'])
            elif self.action == 'tmdb_popular_people':
                import os
                worker = False
                icon_directory = settings.get_theme()
                data = function(page_no)
                for item in data['results']:
                    cm = []
                    actor_poster = "http://image.tmdb.org/t/p/original%s" % item['profile_path'] if item['profile_path'] else os.path.join(icon_directory, 'app_logo.png')
                    url_params = {'mode': 'build_movie_list', 'action': 'tmdb_movies_actor_roles', 'actor_id': item['id']}
                    url = build_url(url_params)
                    cm.append(("[B]Extended Info[/B]", 'RunScript(script.extendedinfo,info=extendedactorinfo,id=%s)' % item['id']))
                    listitem = xbmcgui.ListItem(item['name'])
                    listitem.setArt({'poster': actor_poster, 'fanart':  __addon__.getAddonInfo('fanart')})
                    listitem.addContextMenuItems(cm)
                    xbmcplugin.addDirectoryItem(__handle__, url, listitem, isFolder=True)
                if data['page'] < data['total_pages']: self.new_page = {'mode': mode, 'action': self.action, 'new_page': str(int(data['page']) + 1), 'foldername': self.action}
            elif self.action == 'tmdb_movies_actor_roles':
                data, passed_list, total_pages, limit = function(params['actor_id'], page_no, letter, params.get('passed_list', ''))
                self.list = [i['media_id'] for i in data]
                if total_pages > 1: self.total_pages = total_pages
                if len(data) == limit: self.new_page = {'mode': mode, 'action': self.action, 'new_page': str(page_no + 1), 'new_letter': letter, 'passed_list': passed_list, 'actor_id': params['actor_id'], 'foldername': self.action}
            elif self.action in ('tmdb_movies_search', 'tmdb_movies_people_search'):
                import urllib
                if params.get('query') == 'NA':
                    search_title = dialog.input("Search Fen", type=xbmcgui.INPUT_ALPHANUM)
                    search_name = urllib.unquote(search_title)
                else: search_name = urllib.unquote(params.get('query'))
                if not search_name: return
                if self.action == 'tmdb_movies_people_search': 
                    data, passed_list, total_pages, limit = function(search_name, page_no, letter, params.get('passed_list', ''))
                    if total_pages > 1: self.total_pages = total_pages
                    if len(data) == limit: self.new_page = {'mode': mode, 'action': self.action, 'new_page': str(page_no + 1), 'new_letter': letter, 'passed_list': passed_list, 'query': search_name, 'foldername': search_name}
                else:
                    data = function(search_name, page_no)
                    if self.action == 'tmdb_movies_search':
                        if data['page'] < data['total_pages']: self.new_page = {'mode': mode, 'action': self.action, 'new_page': str(int(data['page']) + 1), 'query': search_name, 'foldername': search_name}
                self.list = [i['id'] for i in data['results']] if self.action == 'tmdb_movies_search' else [i['media_id'] for i in data]
            if self.total_pages:
                url_params = {'mode': 'build_navigate_to_page', 'db_type': 'Movies', 'current_page': page_no, 'total_pages': self.total_pages, 'transfer_mode': mode, 'transfer_action': self.action, 'passed_list': passed_list, 'foldername': self.action, 'query': search_name, 'actor_id': params.get('actor_id', '')}
                self.add_dir(url_params, 'Jump To...', 'Jump To a Certain Page/Letter...', 'item_jump.png')
            if worker: self.worker()
            if self.new_page: self.add_dir(self.new_page)
        except: pass
        xbmcplugin.setContent(__handle__, content_type)
        xbmcplugin.endOfDirectory(__handle__)
        setView('view.movies')

    def build_movie_content(self):
        watched_indicators = settings.watched_indicators()
        all_trailers = settings.all_trailers()
        for i in sorted(self.items, key=lambda k: k['item_no']):
            try:
                cm = []
                if not 'rootname' in i: i['rootname'] = '{0} ({1})'.format(i['title'], i['year'])
                meta_json = json.dumps(i)
                url_params = {'mode': 'play_media', 'vid_type': 'movie', 'query': i['rootname'], 'tmdb_id': i['tmdb_id'], 'meta': meta_json}
                url = build_url(url_params)
                from_search = 'true' if self.action in ('tmdb_movies_search', 'tmdb_movies_people_search') else 'false'
                playback_params = {'mode': 'playback_menu', 'suggestion': i['rootname']}
                hide_recommended_params = {'mode': 'trakt.hide_recommendations', 'db_type': 'movies', 'imdb_id': i['imdb_id']}
                watched_title = 'Trakt' if watched_indicators in (1, 2) else "Fen"
                (state, action) = ('Watched', 'mark_as_watched') if i['playcount'] == 0 else ('Unwatched', 'mark_as_unwatched')
                (state2, action2) = ('Watched', 'mark_as_watched') if state == 'Unwatched' else ('Unwatched', 'mark_as_unwatched')
                watched_unwatched_params = {"mode": "mark_movie_as_watched_unwatched", "action": action, "media_id": i['tmdb_id'], "from_search": from_search, "title": i['title'], "year": i['year']}
                add_remove_params = {"mode": "build_add_to_remove_from_list", "meta": meta_json, "media_type": "movie", "from_search": from_search, "orig_mode": self.action}
                sim_rel_params = {"mode": "similar_related_choice", "db_type": "movies" , "tmdb_id": i['tmdb_id'], "imdb_id": i['imdb_id'], "from_search": from_search}
                (trailer_params, trailer_title) = ({'mode': 'play_trailer', 'url': i['trailer'], 'all_trailers': json.dumps(i['all_trailers'])}, 'Choose Trailer') if (all_trailers and i.get('all_trailers', False)) else ({'mode': 'play_trailer', 'url': i['trailer']}, 'Trailer')
                exit_list_params = {"mode": "navigator.main", "action": "MovieList"}
                listitem = xbmcgui.ListItem(i['title'])
                listitem.setProperty("resumetime", get_resumetime('movie', i['tmdb_id']))
                cm.append(("[B]Mark %s %s[/B]" % (state, watched_title),"XBMC.RunPlugin(%s)" % build_url(watched_unwatched_params)))
                if listitem.getProperty("resumetime") != '0.000000': cm.append(("[B]Mark %s %s[/B]" % (state2, watched_title), 'XBMC.RunPlugin(%s)' % build_url({"mode": "mark_movie_as_watched_unwatched", "action": action2, "media_id": i['tmdb_id'], "from_search": from_search, "title": i['title'], "year": i['year']})))
                cm.append(("[B]Options[/B]","XBMC.RunPlugin(%s)" % build_url(playback_params)))
                cm.append(("[B]Add/Remove[/B]","XBMC.RunPlugin(%s)" % build_url(add_remove_params)))
                cm.append(("[B]Similar/Related[/B]","XBMC.RunPlugin(%s)" % build_url(sim_rel_params)))
                if i['trailer']: cm.append(("[B]%s[/B]" % trailer_title,"XBMC.RunPlugin(%s)" % build_url(trailer_params)))
                if self.action == 'trakt_recommendations': cm.append(("[B]Hide from Recommendations[/B]", "XBMC.RunPlugin(%s)" % build_url(hide_recommended_params)))
                cm.append(("[B]Extended Info[/B]", 'RunScript(script.extendedinfo,info=extendedinfo,id=%s)' % i['tmdb_id']))
                cm.append(("[B]Exit Movie List[/B]","XBMC.Container.Refresh(%s)" % build_url(exit_list_params)))
                listitem.addContextMenuItems(cm)
                listitem.setCast(i['cast'])
                listitem.setArt({'poster': i['poster'], 'fanart': i['fanart'], 'banner': i['banner'], 'clearlogo': i['clearlogo'], 'landscape': i['landscape']})
                listitem.setInfo('Video', remove_unwanted_info_keys(i))
                if not not_widget:
                    listitem.setProperty("fen_widget", 'true')
                    listitem.setProperty("fen_playcount", str(i['playcount']))
                xbmcplugin.addDirectoryItem(__handle__, url, listitem, isFolder=False)
            except: pass

    def set_info(self, item_no, item):
        meta = tikimeta.movie_meta(self.id_type, item)
        playcount, overlay = get_watched_status('movie', meta['tmdb_id'])
        self.items.append({'item_no': item_no, 'mediatype': 'movie', 'trailer': meta['trailer'],
            'title': meta['title'], 'size': '0', 'duration': meta['duration'],
            'plot': meta['plot'], 'rating': meta['rating'], 'premiered': meta['premiered'], 
            'studio': meta['studio'],'year': meta['year'], 'tmdb_id': meta['tmdb_id'],
            'genre': meta['genre'],'tagline': meta['tagline'], 'code': meta['imdb_id'],
            'imdbnumber': meta['imdb_id'], 'imdb_id': meta['imdb_id'], 'all_trailers': meta.get('all_trailers', []),
            'director': meta['director'], 'writer': meta['writer'], 'votes': meta['votes'],
            'playcount': playcount, 'overlay': overlay, 'cast': meta['cast'], 'mpaa': meta['certification'],
            'poster': meta['poster'], 'fanart': meta['fanart'], 'banner': meta['banner'],
            'clearlogo': meta['clearlogo'], 'landscape': meta['landscape']})

    def worker(self):
        threads = []
        self.watched_indicators = settings.watched_indicators()
        self.all_trailers = settings.all_trailers()
        for item_position, item in enumerate(self.list): threads.append(workers.Thread(self.set_info, item_position, item))
        [i.start() for i in threads]
        [i.join() for i in threads]
        self.build_movie_content()

    def multiselect_genres(self, genre_list):
        import os
        dialog = xbmcgui.Dialog()
        genre_list = json.loads(genre_list)
        choice_list = []
        icon_directory = settings.get_theme()
        for genre, value in sorted(genre_list.items()):
            listitem = xbmcgui.ListItem(genre, '', iconImage=os.path.join(icon_directory, value[1]))
            listitem.setProperty('genre_id', value[0])
            choice_list.append(listitem)
        chosen_genres = dialog.multiselect("Select Genres to Include in Search", choice_list, useDetails=True)
        if not chosen_genres: return
        genre_ids = [choice_list[i].getProperty('genre_id') for i in chosen_genres]
        return ','.join(genre_ids)

    def add_dir(self, url_params, list_name='Next Page >>', info='Navigate to Next Page...', iconImage='item_next.png'):
        icon = os.path.join(settings.get_theme(), iconImage)
        url = build_url(url_params)
        listitem = xbmcgui.ListItem(list_name, iconImage=icon)
        listitem.setArt({'fanart': __addon__.getAddonInfo('fanart')})
        listitem.setInfo('video', {'title': list_name, 'plot': info})
        if url_params['mode'] == 'build_navigate_to_page':
            listitem.addContextMenuItems([("[B]Switch Jump To Action[/B]","XBMC.RunPlugin(%s)" % build_url({'mode': 'toggle_jump_to'}))])
        xbmcplugin.addDirectoryItem(handle=__handle__, url=url, listitem=listitem, isFolder=True)
