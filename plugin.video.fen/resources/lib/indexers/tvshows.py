import xbmc, xbmcgui, xbmcplugin, xbmcaddon
import sys, os
import json
from urlparse import parse_qsl
from datetime import date
from resources.lib.modules.nav_utils import build_url, setView, remove_unwanted_info_keys
from resources.lib.modules.indicators_bookmarks import get_watched_status, get_resumetime, \
                                            get_watched_status_season, get_watched_status_tvshow
from resources.lib.modules.trakt import sync_watched_trakt_to_fen, get_trakt_tvshow_id
from resources.lib.modules import workers
from resources.lib.modules import settings
import tikimeta
# from resources.lib.modules.utils import logger

__addon_id__ = 'plugin.video.fen'
__addon__ = xbmcaddon.Addon(id=__addon_id__)
__handle__ = int(sys.argv[1])
dialog = xbmcgui.Dialog()
not_widget = xbmc.getInfoLabel('Container.PluginName')
window = xbmcgui.Window(10000)

class TVShows:
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
            content_type = 'tvshows'
            var_module = 'tmdb' if 'tmdb' in self.action else 'trakt' if 'trakt' in self.action else 'imdb' if 'imdb' in self.action else ''
            try: exec('from resources.lib.modules.%s import %s as function' % (var_module, self.action))
            except: pass
            if self.action in ('tmdb_tv_popular','tmdb_tv_top_rated', 'tmdb_tv_premieres','tmdb_tv_upcoming',
                'tmdb_tv_airing_today','tmdb_tv_on_the_air','trakt_tv_anticipated','trakt_tv_trending'):
                data = function(page_no)
                if 'tmdb' in self.action:
                    for item in data['results']: self.list.append(item['id'])
                else:
                    for item in data: self.list.append(get_trakt_tvshow_id(item))
                self.new_page = {'mode': mode, 'action': self.action, 'new_page': str((data['page'] if 'tmdb' in self.action else page_no) + 1), 'foldername': self.action}
            elif self.action in ('trakt_collection', 'trakt_watchlist'):
                data, passed_list, total_pages, limit = function('shows', page_no, letter, params.get('passed_list', ''))
                self.list = [i['media_id'] for i in data]
                if total_pages > 1: self.total_pages = total_pages
                if len(data) == limit: self.new_page = {'mode': mode, 'action': self.action, 'new_page': str(page_no + 1), 'new_letter': letter, 'passed_list': passed_list, 'foldername': self.action}
            elif self.action == ('trakt_tv_mosts'):
                for item in function(params['period'], params['duration'], page_no): self.list.append((get_trakt_tvshow_id(item)))
                self.new_page = {'mode': mode, 'action': self.action, 'period': params['period'], 'duration': params['duration'], 'new_page': str(page_no + 1), 'foldername': self.action}
            elif self.action == 'tmdb_tv_genres':
                genre_id = params['genre_id'] if 'genre_id' in params else self.multiselect_genres(params.get('genre_list'))
                if not genre_id: return
                data = function(genre_id, page_no)
                self.list = [i['id'] for i in data['results']]
                if data['page'] < data['total_pages']: self.new_page = {'mode': mode, 'action': self.action, 'new_page': str(data['page'] + 1), 'genre_id': genre_id, 'foldername': genre_id}
            elif self.action == 'tmdb_tv_languages':
                language = params['language']
                if not language: return
                data = function(language, page_no)
                self.list = [i['id'] for i in data['results']]
                if data['page'] < data['total_pages']: self.new_page = {'mode': mode, 'action': self.action, 'new_page': str(data['page'] + 1), 'language': language, 'foldername': language}
            elif self.action == 'tmdb_tv_networks':
                data = function(params['network_id'], page_no)
                self.list = [i['id'] for i in data['results']]
                if data['page'] < data['total_pages']: self.new_page = {'mode': mode, 'action': self.action, 'new_page': str(data['page'] + 1), 'network_id': params['network_id'], 'foldername': params['network_id']}
            elif self.action == 'trakt_tv_certifications':
                for item in function(params['certification'], page_no): self.list.append((get_trakt_tvshow_id(item)))
                self.new_page = {'mode': mode, 'action': self.action, 'new_page': str(page_no + 1), 'foldername': params['certification'], 'certification': params['certification']}
            elif self.action == 'tmdb_tv_year':
                data = function(params['year'], page_no)
                self.list = [i['id'] for i in data['results']]
                if data['page'] < data['total_pages']: self.new_page = {'mode': mode, 'action': self.action, 'new_page': str(page_no + 1), 'year': params['year'], 'foldername': params['year']}
            elif self.action in ('favourites_tvshows', 'subscriptions_tvshows', 'kodi_library_tvshows', 'watched_tvshows'):
                (var_module, import_function) = ('favourites', 'retrieve_favourites') if 'favourites' in self.action else ('subscriptions', 'retrieve_subscriptions') if 'subscriptions' in self.action else ('indicators_bookmarks', 'get_watched_items') if 'watched' in self.action else ('kodi_library', 'retrieve_kodi_library') if 'library' in self.action else ''
                try: exec('from resources.lib.modules.%s import %s as function' % (var_module, import_function))
                except: pass
                if self.action == 'kodi_library_tvshows': self.id_type = 'tvdb_id'
                data, passed_list, total_pages, limit = function('tvshow', page_no, letter, params.get('passed_list', ''))
                self.list = [i['media_id'] for i in data]
                if total_pages > 1: self.total_pages = total_pages
                if len(data) == limit: self.new_page = {'mode': mode, 'action': self.action, 'new_page': str(page_no + 1), 'new_letter': letter, 'passed_list': passed_list, 'foldername': self.action}
            elif self.action =='in_progress_tvshows':
                from resources.lib.modules.in_progress import in_progress_tvshow as function
                self.list = function('tvshow')
                xbmcplugin.addSortMethod(__handle__, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
            elif self.action == 'tmdb_tv_similar':
                data = function(params['tmdb_id'], page_no)
                self.list = [i['id'] for i in data['results']]
                if data['page'] < data['total_pages']: self.new_page = {'mode': mode, 'action': self.action, 'new_page': str(data['page'] + 1), 'tmdb_id': params['tmdb_id'], 'foldername': self.action}
            elif self.action == 'trakt_tv_related':
                for item in function(params['imdb_id'], page_no): self.list.append(get_trakt_tvshow_id(item))
                self.new_page = {'mode': mode, 'action': self.action, 'new_page': str(page_no + 1), 'foldername': self.action, 'imdb_id': params['imdb_id']}
            elif self.action == 'trakt_recommendations':
                for item in function('shows'): self.list.append(get_trakt_tvshow_id(item))
            elif self.action == 'tmdb_popular_people':
                import os
                worker = False
                icon_directory = settings.get_theme()
                data = function(page_no)
                for item in data['results']:
                    cm = []
                    actor_poster = "http://image.tmdb.org/t/p/original%s" % item['profile_path'] if item['profile_path'] else os.path.join(icon_directory, 'app_logo.png')
                    url_params = {'mode': 'build_tvshow_list', 'action': 'tmdb_tv_actor_roles', 'actor_id': item['id']}
                    cm.append(("[B]Extended Info[/B]", 'RunScript(script.extendedinfo,info=extendedactorinfo,id=%s)' % item['id']))
                    url = build_url(url_params)
                    listitem = xbmcgui.ListItem(item['name'])
                    listitem.setArt({'poster': actor_poster, 'fanart':  __addon__.getAddonInfo('fanart')})
                    listitem.addContextMenuItems(cm)
                    xbmcplugin.addDirectoryItem(__handle__, url, listitem, isFolder=True)
                if data['page'] < data['total_pages']: self.new_page = {'mode': mode, 'action': self.action, 'new_page': str(int(data['page']) + 1), 'foldername': self.action}
            elif self.action == 'tmdb_tv_actor_roles':
                data, passed_list, total_pages, limit = function(params['actor_id'], page_no, letter, params.get('passed_list', ''))
                self.list = [i['media_id'] for i in data]
                if total_pages > 1: self.total_pages = total_pages
                if len(data) == limit: self.new_page = {'mode': mode, 'action': self.action, 'new_page': str(page_no + 1), 'passed_list': passed_list, 'actor_id': params['actor_id'], 'foldername': self.action}
            elif self.action in ('tmdb_tv_search', 'tmdb_tv_people_search'):
                import urllib
                if params.get('query') == 'NA':
                    search_title = dialog.input("Search Fen", type=xbmcgui.INPUT_ALPHANUM)
                    search_name = urllib.unquote(search_title)
                else: search_name = urllib.unquote(params.get('query'))
                if not search_name: return
                if self.action == 'tmdb_tv_people_search': 
                    data, passed_list, total_pages, limit = function(search_name, page_no, params.get('passed_list', ''))
                    if total_pages > 1: self.total_pages = total_pages
                    if len(data) == limit: self.new_page = {'mode': mode, 'action': self.action, 'new_page': str(page_no + 1), 'passed_list': passed_list, 'query': search_name, 'foldername': search_name}
                else:
                    data = function(search_name, page_no)
                    if data['page'] < data['total_pages']: self.new_page = {'mode': mode, 'action': self.action, 'new_page': str(data['page'] + 1), 'query': search_name, 'foldername': search_name}
                self.list = [i['id'] for i in data['results']] if self.action == 'tmdb_tv_search' else [i['media_id'] for i in data]
            if self.total_pages:
                url_params = {'mode': 'build_navigate_to_page', 'db_type': 'TV Shows', 'current_page': page_no, 'total_pages': self.total_pages, 'transfer_mode': mode, 'transfer_action': self.action, 'passed_list': passed_list, 'foldername': self.action, 'query': search_name, 'actor_id': params.get('actor_id', '')}
                self.add_dir(url_params, 'Jump To...', 'Jump To a Certain Page/Letter...', 'item_jump.png')
            if worker: self.worker()
            if self.new_page: self.add_dir(self.new_page)
        except: pass
        xbmcplugin.setContent(__handle__, content_type)
        xbmcplugin.endOfDirectory(__handle__)
        setView('view.tvshows')

    def build_tvshow_content(self):
        watched_indicators = settings.watched_indicators()
        all_trailers = settings.all_trailers()
        for i in sorted(self.items, key=lambda k: k['item_no']):
            try:
                cm = []
                item_no = i['item_no']
                if not 'rootname' in i: i['rootname'] = '{0} ({1})'.format(i['title'], i['year'])
                meta = i['meta']
                del i['meta']
                meta_json = json.dumps(meta)
                url_params = {'mode': 'build_season_list', 'meta': meta_json, 'tmdb_id': i['tmdb_id']}
                url = build_url(url_params)
                from_search = 'true' if self.action in ('tmdb_tv_search', 'tmdb_tv_people_search') else 'false'
                hide_recommended_params = {'mode': 'trakt.hide_recommendations', 'db_type': 'shows', 'imdb_id': i['imdb_id']}
                playback_menu_params = {'mode': 'playback_menu'}
                watched_title = 'Trakt' if watched_indicators in (1, 2) else "Fen"
                watched_params = {"mode": "mark_tv_show_as_watched_unwatched", "action": 'mark_as_watched', "title": i['title'], "year": i['year'], "media_id": i['tmdb_id'], "imdb_id": i["imdb_id"], "tvdb_id": meta["tvdb_id"], "from_search": from_search}
                unwatched_params = {"mode": "mark_tv_show_as_watched_unwatched", "action": 'mark_as_unwatched', "title": i['title'], "year": i['year'], "media_id": i['tmdb_id'], "imdb_id": i["imdb_id"], "tvdb_id": meta["tvdb_id"], "from_search": from_search}
                add_remove_params = {"mode": "build_add_to_remove_from_list", "media_type": "tvshow", "meta": meta_json, "from_search": from_search, "orig_mode": self.action}
                sim_rel_params = {'mode': 'similar_related_choice', 'db_type': 'tv', 'tmdb_id': i['tmdb_id'], 'imdb_id': i['imdb_id'], 'from_search': from_search}
                exit_list_params = {"mode": "navigator.main", "action": "TVShowList"}
                (trailer_params, trailer_title) = ({'mode': 'play_trailer', 'url': i['trailer'], 'all_trailers': json.dumps(i['all_trailers'])}, 'Choose Trailer') if (all_trailers and i.get('all_trailers', False)) else ({'mode': 'play_trailer', 'url': i['trailer']}, 'Trailer')
                cm.append(("[B]Mark Watched %s[/B]" % watched_title, "XBMC.RunPlugin(%s)" % build_url(watched_params)))
                cm.append(("[B]Mark Unwatched %s[/B]" % watched_title, "XBMC.RunPlugin(%s)" % build_url(unwatched_params)))
                cm.append(("[B]Add/Remove[/B]", "XBMC.RunPlugin(%s)" % build_url(add_remove_params)))
                cm.append(("[B]Similar/Related[/B]", "XBMC.RunPlugin(%s)" % build_url(sim_rel_params)))
                if self.action == 'trakt_recommendations': cm.append(("[B]Hide from Recommendations[/B]", "XBMC.RunPlugin(%s)" % build_url(hide_recommended_params)))
                cm.append(("[B]Options[/B]",'XBMC.RunPlugin(%s)' % build_url(playback_menu_params)))
                if i['trailer']: cm.append(("[B]%s[/B]" % trailer_title,"XBMC.RunPlugin(%s)" % build_url(trailer_params)))
                cm.append(("[B]Extended Info[/B]", 'RunScript(script.extendedinfo,info=extendedtvinfo,id=%s)' % i['tmdb_id']))
                cm.append(("[B]Exit TV Show List[/B]","XBMC.Container.Refresh(%s)" % build_url(exit_list_params)))
                listitem = xbmcgui.ListItem(i['title'])
                listitem.setProperty('watchedepisodes', i['total_watched'])
                listitem.setProperty('unwatchedepisodes', i['total_unwatched'])
                listitem.setProperty('totalepisodes', i['total_episodes'])
                listitem.setProperty('totalseasons', i['total_seasons'])
                listitem.addContextMenuItems(cm)
                listitem.setCast(i['cast'])
                listitem.setArt({'poster': i['poster'], 'fanart': i['fanart'], 'banner': i['banner'], 'clearlogo': i['clearlogo'], 'landscape': i['landscape']})
                listitem.setInfo('video', remove_unwanted_info_keys(i))
                xbmcplugin.addDirectoryItem(__handle__, url, listitem, isFolder=True)
            except: pass

    def set_info(self, item_no, item):
        meta = make_fresh_tvshow_meta(self.id_type, item)
        if not meta: return
        aired_episodes = aired_episode_number_tvshow(meta)
        playcount, overlay, total_watched, total_unwatched = get_watched_status_tvshow(meta.get('tmdb_id'), aired_episodes)
        self.items.append({'item_no': item_no, 'mediatype': 'tvshow', 'trailer': str(meta.get('trailer')),
            'tvdb_id': meta.get('tvdb_id'),'title': meta.get('title'), 'size': '0', 'duration': meta.get('episode_run_time'),
            'plot': meta.get('plot'), 'rating': meta.get('rating'), 'premiered': meta.get('premiered'),
            'studio': meta.get('studio'),'year': meta.get('year'), 'code': meta.get('imdb_id'), 'episode': str(meta.get('number_of_episodes', 0)),
            'imdbnumber': meta.get('imdb_id'), 'imdb_id': meta.get('imdb_id'), 'tvshowtitle': meta.get('title'),
            'genre': meta.get('genre'), 'votes': meta.get('votes'),'playcount': playcount, 'overlay': overlay,
            'cast': meta.get('cast'), 'meta': meta, 'tmdb_id': meta.get('tmdb_id'), 'all_trailers': meta.get('all_trailers', []),
            'total_episodes': str(aired_episodes), 'total_seasons': str(meta.get('number_of_seasons')),
            'total_watched': str(total_watched), 'total_unwatched': str(total_unwatched),
            'poster': meta.get('poster'), 'fanart': meta.get('fanart'), 'banner': meta.get('banner'),
            'clearart': meta.get('clearart'), 'clearlogo': meta.get('clearlogo'), 'landscape': meta.get('landscape')})

    def worker(self):
        threads = []
        for item_position, item in enumerate(self.list): threads.append(workers.Thread(self.set_info, item_position, item))
        [i.start() for i in threads]
        [i.join() for i in threads]
        self.build_tvshow_content()

    def multiselect_genres(self, genre_list):
        import os
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
        if url_params['mode'] == 'build_navigate_to_page': listitem.addContextMenuItems([("[B]Switch Jump To Action[/B]","XBMC.RunPlugin(%s)" % build_url({'mode': 'toggle_jump_to'}))])
        xbmcplugin.addDirectoryItem(handle=__handle__, url=url, listitem=listitem, isFolder=True)

def build_season_list():
    params = dict(parse_qsl(sys.argv[2].replace('?','')))
    meta = json.loads(params.get('meta')) if 'meta' in params else tikimeta.tvshow_meta('tmdb_id', params.get('tmdb_id'))
    show_specials = settings.show_specials()
    use_season_title = settings.use_season_title()
    season_data = [i for i in meta['season_data'] if i['season_number'] > 0] if not show_specials else meta['season_data']
    watched_indicators = settings.watched_indicators()
    for item in season_data:
        try:
            cm = []
            plot = item['overview'] if item['overview'] != '' else meta['plot']
            title = item['name'] if use_season_title else 'Season %s' % str(item['season_number'])
            season_poster = "http://image.tmdb.org/t/p/original%s" % item['poster_path'] if item['poster_path'] is not None else meta['poster']
            aired_episodes = aired_episode_number_season(meta, item['season_number'])
            playcount, overlay, watched, unwatched = get_watched_status_season(meta['tmdb_id'], item['season_number'], aired_episodes)
            watched_title = 'Trakt' if watched_indicators in (1, 2) else "Fen"
            watched_params = {"mode": "mark_season_as_watched_unwatched", "action": 'mark_as_watched', "title": meta['title'], "year": meta['year'], "media_id": meta['tmdb_id'], "imdb_id": meta["imdb_id"], "tvdb_id": meta["tvdb_id"], "season": item['season_number']}
            unwatched_params = {"mode": "mark_season_as_watched_unwatched", "action": 'mark_as_unwatched', "title": meta['title'], "year": meta['year'], "media_id": meta['tmdb_id'], "imdb_id": meta["imdb_id"], "tvdb_id": meta["tvdb_id"], "season": item['season_number']}
            playback_menu_params = {'mode': 'playback_menu'}
            cm.append(("[B]Mark Watched %s[/B]" % watched_title,'XBMC.RunPlugin(%s)' % build_url(watched_params)))
            cm.append(("[B]Mark Unwatched %s[/B]" % watched_title,'XBMC.RunPlugin(%s)' % build_url(unwatched_params)))
            cm.append(("[B]Options[/B]",'XBMC.RunPlugin(%s)' % build_url(playback_menu_params)))
            cm.append(("[B]Extended Info[/B]", 'RunScript(script.extendedinfo,info=extendedtvinfo,id=%s)' % meta['tmdb_id']))
            url_params = {'mode': 'build_episode_list', 'tmdb_id': meta['tmdb_id'], 'season': str(item['season_number']), 'season_id': item['id']}
            url = build_url(url_params)
            listitem = xbmcgui.ListItem(title)
            listitem.setProperty('watchedepisodes', str(watched))
            listitem.setProperty('unwatchedepisodes', str(unwatched))
            listitem.setProperty('totalepisodes', str(item['episode_count']))
            listitem.addContextMenuItems(cm)
            listitem.setArt({'poster': season_poster, 'fanart': meta['fanart'], 'banner': meta['banner'], 'clearlogo': meta['clearlogo'], 'landscape': meta['landscape']})
            listitem.setCast(meta['cast'])
            listitem.setInfo(
                'video', {'mediatype': 'tvshow', 'trailer': str(meta['trailer']),
                    'title': meta.get('title'), 'size': '0', 'duration': meta.get('episode_run_time'), 'plot': plot,
                    'rating': meta.get('rating'), 'premiered': meta.get('premiered'), 'studio': meta.get('studio'),
                    'year': meta.get('year'),'genre': meta.get('genre'), 'code': meta.get('imdb_id'),
                    'tvshowtitle': meta.get('title'), 'imdbnumber': meta.get('imdb_id'),'votes': meta.get('votes'),
                    'episode': str(item['episode_count']),'playcount': playcount, 'overlay': overlay})
            xbmcplugin.addDirectoryItem(__handle__, url, listitem, isFolder=True)
        except: pass
    xbmcplugin.setContent(__handle__, 'seasons')
    xbmcplugin.endOfDirectory(__handle__)
    setView('view.seasons')
    window.setProperty('fen_media_meta', json.dumps(meta))

def build_episode_list():
    UNAIRED_EPISODE_COLOUR = settings.unaired_episode_colour()
    if not UNAIRED_EPISODE_COLOUR or UNAIRED_EPISODE_COLOUR == '': UNAIRED_EPISODE_COLOUR = 'red'
    params = dict(parse_qsl(sys.argv[2].replace('?','')))
    try: meta = json.loads(window.getProperty('fen_media_meta'))
    except: meta = tikimeta.tvshow_meta('tmdb_id', params.get('tmdb_id'))
    thumb_path = 'http://image.tmdb.org/t/p/original%s'
    cast = []
    infoLabels = tikimeta.season_episodes_meta(meta['tmdb_id'], params.get('season'))
    watched_indicators = settings.watched_indicators()
    try:
        for item in infoLabels['credits']['cast']:
            cast_thumb = "http://image.tmdb.org/t/p/original%s" % item["profile_path"] if 'profile_path' in item else ''
            cast.append({"name": item["name"], "role": item["character"], "thumbnail": cast_thumb})
    except: pass
    for i in infoLabels['episodes']:
        try:
            cm = []
            guest_stars = get_guest_stars(i['guest_stars'])
            first_aired = i['air_date'] if 'air_date' in i else None
            writer = ', '.join([c['name'] for c in i['crew'] if c['job'] == 'Writer'])
            director = ', '.join([c['name'] for c in i['crew'] if c['job'] == 'Director'])
            thumb = thumb_path % i['still_path'] if i.get('still_path', None) != None else meta['fanart']
            playcount, overlay = get_watched_status('episode', meta['tmdb_id'], i['season_number'], i['episode_number'])
            query = meta['title'] + ' S%.2dE%.2d' % (int(i['season_number']), int(i['episode_number']))
            display_name = '%s - %dx%.2d' % (meta['title'], int(i['season_number']), int(i['episode_number']))
            meta.update({'vid_type': 'episode', 'rootname': display_name, 'season': i['season_number'],
                        'episode': i['episode_number'], 'premiered': first_aired, 'ep_name': i['name'],
                        'plot': i['overview']})
            meta_json = json.dumps(meta)
            url_params = {'mode': 'play_media', 'vid_type': 'episode', 'tmdb_id': meta['tmdb_id'],
                        'query': query, 'tvshowtitle': meta['rootname'], 'season': i['season_number'],
                        'episode': i['episode_number'], 'meta': meta_json}
            url = build_url(url_params)
            try:
                d = first_aired.split('-')
                episode_date = date(int(d[0]), int(d[1]), int(d[2]))
            except: episode_date = date(2000,01,01) if i['season_number'] == 0 else None
            current_adjusted_date = settings.adjusted_datetime()
            display = '%dx%.2d - %s' % (i['season_number'], i['episode_number'], i['name'])
            cad = True
            if not episode_date or current_adjusted_date < episode_date:
                cad = False
                display = '[I][COLOR={}]{}[/COLOR][/I]'.format(UNAIRED_EPISODE_COLOUR, display)
            listitem = xbmcgui.ListItem(display)
            listitem.setProperty("resumetime", get_resumetime('episode', meta['tmdb_id'], i['season_number'], i['episode_number']))
            (state, action) = ('Watched', 'mark_as_watched') if playcount == 0 else ('Unwatched', 'mark_as_unwatched')
            (state2, action2) = ('Watched', 'mark_as_watched') if state == 'Unwatched' else ('Unwatched', 'mark_as_unwatched')
            playback_menu_params = {'mode': 'playback_menu', 'suggestion': query}
            watched_title = 'Trakt' if watched_indicators in (1, 2) else "Fen"
            watched_unwatched_params = {"mode": "mark_episode_as_watched_unwatched", "action": action, "media_id": meta['tmdb_id'], "imdb_id": meta["imdb_id"], "tvdb_id": meta["tvdb_id"], "season": i['season_number'], "episode": i['episode_number'],  "title": meta['title'], "year": meta['year']}
            if cad: cm.append(("[B]Mark %s %s[/B]" % (state, watched_title),'XBMC.RunPlugin(%s)' % build_url(watched_unwatched_params)))
            if cad and listitem.getProperty("resumetime") != '0.000000': cm.append(("[B]Mark %s %s[/B]" % (state2, watched_title),'XBMC.RunPlugin(%s)' % build_url({"mode": "mark_episode_as_watched_unwatched", "action": action2, "media_id": meta['tmdb_id'], "imdb_id": meta["imdb_id"], "season": i['season_number'], "episode": i['episode_number'],  "title": meta['title'], "year": meta['year']})))
            cm.append(("[B]Options[/B]",'XBMC.RunPlugin(%s)' % build_url(playback_menu_params)))
            cm.append(("[B]Extended Info[/B]", 'RunScript(script.extendedinfo,info=extendedtvinfo,id=%s)' % meta['tmdb_id']))
            listitem.addContextMenuItems(cm)
            listitem.setArt({'poster': meta['poster'], 'fanart': meta['fanart'], 'thumb':thumb, 'banner': meta['banner'], 'clearlogo': meta['clearlogo'], 'landscape': meta['landscape']})
            listitem.setCast(cast + guest_stars)
            listitem.setInfo(
                'video', {'mediatype': 'episode', 'trailer': str(meta.get('trailer')), 'title': i['name'],
                'tvshowtitle': meta.get('title'), 'size': '0', 'plot': i['overview'],
                'premiered': first_aired, 'genre': meta.get('genre'), 'season':i['season_number'],
                'episode': i['episode_number'], 'duration': meta.get('episode_run_time'),
                'rating': i['vote_average'], 'votes': i['vote_count'],'writer': writer,
                'director': director, 'playcount': playcount, 'overlay': overlay})
            if not not_widget:
                listitem.setProperty("fen_widget", 'true')
                listitem.setProperty("fen_playcount", str(playcount))
            xbmcplugin.addDirectoryItem(__handle__, url, listitem, isFolder=False)
        except: pass
    xbmcplugin.setContent(__handle__, 'episodes')
    xbmcplugin.endOfDirectory(__handle__)
    setView('view.episodes')

def build_episode(item):
    from resources.lib.modules.utils import make_day
    def check_for_unaired():
        try:
            d = first_aired.split('-')
            episode_date = date(int(d[0]), int(d[1]), int(d[2]))
        except: episode_date = None
        current_adjusted_date = settings.adjusted_datetime()
        unaired = False
        if not episode_date or current_adjusted_date < episode_date:
            unaired = True
        return unaired
    def build_display():
        if display_info:
            display_first_aired = make_day(first_aired)
            airdate = '[[COLOR=%s]%s[/COLOR]] ' % (display_info['airdate_colour'], display_first_aired) if display_info['include_airdate'] else ''
            highlight_color = display_info['unwatched_colour'] if item.get('unwatched', False) else display_info['unaired_colour'] if unaired else ''
            italics_open, italics_close = ('[I]', '[/I]') if highlight_color else ('', '')
            episode_info = '%s[COLOR=%s]%dx%.2d - %s[/COLOR]%s' % (italics_open, highlight_color, info['season_number'], info['episode_number'], info['name'], italics_close)
            display = '%s%s: %s' % (airdate, meta['title'], episode_info)
            tvshow_display = display if display_info['force_display'] else meta['title']
        else:
            display = '%s: %dx%.2d - %s' % (meta['title'].upper(), info['season_number'], info['episode_number'], info['name'])
            tvshow_display = meta['title']
        return display, tvshow_display
    try:
        display_info = item.get('ne_display', None)
        thumb_path = 'http://image.tmdb.org/t/p/original%s'
        cm = []
        watched_indicators = settings.watched_indicators()
        action = item.get('action', '')
        meta = item['meta']
        info = [i for i in tikimeta.season_episodes_meta(meta['tmdb_id'], item['season'])['episodes'] if i['episode_number'] == item['episode']][0]
        first_aired = info['air_date']
        unaired = check_for_unaired()
        if unaired and not item.get('include_unaired', False): return
        guest_stars = get_guest_stars(info['guest_stars'])
        writer = ', '.join([i['name'] for i in info['crew'] if i['job'] == 'Writer'])
        director = ', '.join([i['name'] for i in info['crew'] if i['job'] == 'Director'])
        thumb = thumb_path % info['still_path'] if info.get('still_path', None) != None else meta['fanart']
        playcount, overlay = get_watched_status('episode', meta['tmdb_id'], info['season_number'], info['episode_number'])
        query = meta['title'] + ' S%.2dE%.2d' % (info['season_number'], info['episode_number'])
        display, tvshow_display = build_display()
        listitem = xbmcgui.ListItem(display)
        listitem.setProperty("resumetime", get_resumetime('episode', meta['tmdb_id'], info['season_number'], info['episode_number']))
        rootname = '{0} ({1})'.format(meta['title'], meta['year'])
        meta.update({'vid_type': 'episode', 'rootname': rootname, 'season': info['season_number'],
                    'episode': info['episode_number'], 'premiered': first_aired, 'ep_name': info['name'],
                    'plot': info['overview']})
        meta_json = json.dumps(meta)
        url_params = {'mode': 'play_media', 'vid_type': 'episode', 'tmdb_id': meta['tmdb_id'], 'query': query,
                'tvshowtitle': meta['rootname'], 'season': info['season_number'],
                'episode': info['episode_number'], 'meta': meta_json}
        url = build_url(url_params)
        browse_url = build_url({'mode': 'build_season_list', 'meta': meta_json})
        playback_menu_params = {'mode': 'playback_menu', 'suggestion': query}
        watched_title = 'Trakt' if watched_indicators in (1, 2) else "Fen"
        watched_params = {"mode": "mark_episode_as_watched_unwatched", "action": "mark_as_watched", "media_id": meta['tmdb_id'], "imdb_id": meta["imdb_id"], "tvdb_id": meta["tvdb_id"], "season": info['season_number'], "episode": info['episode_number'],  "title": meta['title'], "year": meta['year']}
        if action == 'next_episode': nextep_manage_params = {"mode": "next_episode_context_choice"}
        cm.append(("[B]Mark Watched %s[/B]" % watched_title,'XBMC.RunPlugin(%s)' % build_url(watched_params)))
        if listitem.getProperty("resumetime") != '0.000000': cm.append(("[B]Mark Unwatched %s[/B]" % watched_title,'XBMC.RunPlugin(%s)' % build_url({"mode": "mark_episode_as_watched_unwatched", "action": "mark_as_unwatched", "media_id": meta['tmdb_id'], "imdb_id": meta["imdb_id"], "season": info['season_number'], "episode": info['episode_number'],  "title": meta['title'], "year": meta['year']})))
        if action == 'next_episode':
            cm.append(("[B]Next Episode Manager[/B]",'XBMC.RunPlugin(%s)'% build_url(nextep_manage_params)))
            cm.append(("[B]Refresh List[/B]",'XBMC.Container.Refresh()'))
        cm.append(("[B]Browse...[/B]",'XBMC.Container.Update(%s)' % browse_url))
        cm.append(("[B]Options[/B]",'XBMC.RunPlugin(%s)' % build_url(playback_menu_params)))
        cm.append(("[B]Extended Info[/B]", 'RunScript(script.extendedinfo,info=extendedtvinfo,id=%s)' % meta['tmdb_id']))
        listitem.setArt({'poster': meta['poster'], 'fanart': meta['fanart'], 'thumb':thumb, 'banner': meta['banner'], 'clearlogo': meta['clearlogo'], 'landscape': meta['landscape']})
        listitem.addContextMenuItems(cm)
        listitem.setCast(meta['cast'] + guest_stars)
        listitem.setInfo(
            'video', {'mediatype': 'episode', 'trailer': str(meta.get('trailer')), 'title': info['name'],
            'tvshowtitle': tvshow_display, 'size': '0', 'plot': info['overview'], 'premiered': first_aired,
            'writer': writer, 'director': director, 'season':info['season_number'], 'genre': meta.get('genre'),
            'episode': info['episode_number'], 'rating': info['vote_average'], 'votes': info['vote_count'],
            'duration': meta.get('episode_run_time'), 'playcount': playcount, 'overlay': overlay})
        if not not_widget:
            listitem.setProperty("fen_widget", 'true')
            listitem.setProperty("fen_playcount", str(playcount))
        return {'listitem': (url, listitem, False), 'curr_last_played_parsed': item.get('curr_last_played_parsed', ''), 'order': item.get('order', ''), 'name': query, 'first_aired': first_aired}
    except: pass

def make_fresh_tvshow_meta(id_type, media_id):
    def make_refresh_property():
        window.setProperty('fen_refresh_complete_%s' % media_id, 'true')
        return meta
    meta = tikimeta.tvshow_meta(id_type, media_id)
    if window.getProperty('fen_refresh_complete_%s' % media_id) == 'true': return meta
    if not meta.get('status', None) or meta.get('status') in ('Ended', 'Canceled', 'Pilot'): return make_refresh_property()
    if not meta.get('in_production', False): return make_refresh_property()
    if not meta.get('next_episode_to_air', None): return make_refresh_property()
    if meta.get('status') in ('Returning Series', 'In Production'):
        try:
            next_episode = meta['next_episode_to_air']
            next_airdate = next_episode.get('air_date', None)
            if not next_airdate: return make_refresh_property()
            d = next_airdate.split('-')
            next_episode_date = date(int(d[0]), int(d[1]), int(d[2]))
            current_adjusted_date = settings.adjusted_datetime()
            if current_adjusted_date > next_episode_date:
                from resources.lib.modules.nav_utils import refresh_cached_data
                if refresh_cached_data('tvshow', id_type, media_id, from_list=True):
                    meta = tikimeta.tvshow_meta(id_type, media_id)
                    return make_refresh_property()
            else: return make_refresh_property()
        except: make_refresh_property()
    else: return make_refresh_property()

def get_guest_stars(info):
    guest_stars = []
    for item in info:
        cast_thumb = "http://image.tmdb.org/t/p/original%s" % item["profile_path"] if 'profile_path' in item else ''
        guest_stars.append({"name": item["name"], "role": item["character"], "thumbnail": cast_thumb})
    guest_stars = [i for n, i in enumerate(guest_stars) if i not in guest_stars[n + 1:]]
    return guest_stars

def aired_episode_number_tvshow(meta):
    try:
        season_data = meta['season_data']
        total_seasons = meta['number_of_seasons']
        total_episodes = meta['number_of_episodes']
        if not 'next_episode_to_air' in meta:
            return total_episodes
        else:
            next_episode_seas_number = meta['next_episode_to_air']['season_number']
            next_episode_ep_number = meta['next_episode_to_air']['episode_number']
            if next_episode_seas_number > total_seasons:
                return total_episodes
            else:
                aired_episodes = 0
                for item in season_data:
                    if total_seasons > item['season_number'] > 0:
                        no_eps = item['episode_count']
                        aired_episodes += no_eps
                aired_episodes += next_episode_ep_number-1
                return aired_episodes
    except: return 0

def aired_episode_number_season(meta, season):
    try:
        season_data = meta['season_data']
        season_info = [i for i in season_data if i['season_number'] == season][0]
        if not 'next_episode_to_air' in meta:
            return season_info['episode_count']
        else:
            next_episode_seas_number = meta['next_episode_to_air']['season_number']
            next_episode_ep_number = meta['next_episode_to_air']['episode_number']
            if season != next_episode_seas_number:
                return season_info['episode_count']
            else:
                return next_episode_ep_number-1
    except: return 0

