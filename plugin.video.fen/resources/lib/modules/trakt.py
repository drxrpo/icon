# -*- coding: utf-8 -*-
import xbmc, xbmcgui, xbmcaddon, xbmcplugin
import os, sys
import requests
from urlparse import parse_qsl
import time
from resources.lib.modules import trakt_cache
from resources.lib.modules.nav_utils import cache_object, build_url, setView, add_dir, notification
from resources.lib.modules.utils import to_utf8
from resources.lib.modules import settings
# from resources.lib.modules.utils import logger

__addon_id__ = 'plugin.video.fen'
__addon__ = xbmcaddon.Addon(id=__addon_id__)
addon_dir = xbmc.translatePath(__addon__.getAddonInfo('path'))
profile_dir = xbmc.translatePath(__addon__.getAddonInfo('profile'))
__url__ = sys.argv[0]
__handle__ = int(sys.argv[1])
dialog = xbmcgui.Dialog()
icon_directory = settings.get_theme()
fanart = os.path.join(addon_dir, "fanart.png")
my_list_icon = os.path.join(icon_directory, 'traktmylists.png')
liked_list_icon = os.path.join(icon_directory, 'traktlikedlists.png')
trakt_icon = os.path.join(icon_directory, 'trakt.png')
window = xbmcgui.Window(10000)

API_ENDPOINT = "https://api-v2launch.trakt.tv"
CLIENT_ID = "793c4e6772d7ccdd66e8f03aeb96a8a968bb9c71ad2b8ce721fd194935b9b1ef"
CLIENT_SECRET = "56bb84ffade5962bc981300cc417edd645283cd54eb97cea8964f26a98225c11"
LIST_PRIVACY_IDS = ('private', 'friends', 'public')

def call_trakt(path, params={}, data=None, is_delete=False, with_auth=True, method=None, pagination=False, page=1):
    def timeout_notification():
        from resources.lib.modules.nav_utils import notification
        notification('Trakt response timeout error', 6000, trakt_icon)
    def send_query():
        if with_auth:
            try:
                expires_at = __addon__.getSetting('trakt_expires_at')
                if time.time() > expires_at:
                    trakt_refresh_token()
            except:
                pass
            token = __addon__.getSetting('trakt_access_token')
            if token:
                headers['Authorization'] = 'Bearer ' + token
        try:
            if method:
                if method == 'post':
                    resp = requests.post("{0}/{1}".format(API_ENDPOINT, path), headers=headers, timeout=timeout)
                elif method == 'delete':
                    resp = requests.delete("{0}/{1}".format(API_ENDPOINT, path), headers=headers, timeout=timeout)
                elif method == 'sort_by_headers':
                    resp = requests.get("{0}/{1}".format(API_ENDPOINT, path), params, headers=headers, timeout=timeout)
            elif data is not None:
                assert not params
                resp = requests.post("{0}/{1}".format(API_ENDPOINT, path), json=data, headers=headers, timeout=timeout)
            elif is_delete:
                resp = requests.delete("{0}/{1}".format(API_ENDPOINT, path), headers=headers, timeout=timeout)
            else:
                resp = requests.get("{0}/{1}".format(API_ENDPOINT, path), params, headers=headers, timeout=timeout)
            return resp
        except requests.exceptions.Timeout as e:
            timeout_notification()
            return None
    params = dict([(k, to_utf8(v)) for k, v in params.items() if v])
    timeout = 10.0
    resp = None
    numpages = 0
    headers = {'Content-Type': 'application/json', 'trakt-api-version': '2', 'trakt-api-key': CLIENT_ID}
    if pagination: params['page'] = page
    response = send_query()
    if with_auth and response.status_code == 401 and dialog.yesno(("Authenticate Trakt"), (
            "You must authenticate with Trakt. Do you want to authenticate now?")) and trakt_authenticate():
        response = send_query()
    else: pass
    response.raise_for_status()
    response.encoding = 'utf-8'
    try: result = response.json()
    except: result = None
    if method == 'sort_by_headers':
        headers = response.headers
        if 'X-Sort-By' in headers and 'X-Sort-How' in headers:
            from resources.lib.modules.utils import sort_list
            result = sort_list(headers['X-Sort-By'], headers['X-Sort-How'], result)
    if pagination: numpages = response.headers["X-Pagination-Page-Count"]
    return (result, numpages) if pagination else result

def trakt_get_device_code():
    data = { 'client_id': CLIENT_ID }
    return call_trakt("oauth/device/code", data=data, with_auth=False)

def trakt_get_device_token(device_codes):
    data = {
        "code": device_codes["device_code"],
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }
    start = time.time()
    expires_in = device_codes["expires_in"]
    progress_dialog = xbmcgui.DialogProgress()
    progress_dialog.create(("Authenticate Trakt"), ("Please go to [B]https://trakt.tv/activate[/B] and enter the code"), "[B]%s[/B]" % str(device_codes["user_code"]))
    try:
        time_passed = 0
        while not xbmc.abortRequested and not progress_dialog.iscanceled() and time_passed < expires_in:            
            try:
                response = call_trakt("oauth/device/token", data=data, with_auth=False)
            except requests.HTTPError, e:
                if e.response.status_code != 400:
                    raise e
                
                progress = int(100 * time_passed / expires_in)
                progress_dialog.update(progress)
                xbmc.sleep(max(device_codes["interval"], 1)*1000)
            else:
                return response
                
            time_passed = time.time() - start
    finally:
        progress_dialog.close()
        del progress_dialog
    return None

def trakt_refresh_token():
    data = {        
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": "urn:ietf:wg:oauth:2.0:oob",
        "grant_type": "refresh_token",
        "refresh_token": __addon__.getSetting('trakt_refresh_token')
    }
    response = call_trakt("oauth/token", data=data, with_auth=False)
    if response:
        __addon__.setSetting('trakt_access_token', response["access_token"])
        __addon__.setSetting('trakt_refresh_token', response["refresh_token"])

def trakt_authenticate():
    code = trakt_get_device_code()
    token = trakt_get_device_token(code)
    if token:
        expires_at = time.time() + 60*60*24*30
        __addon__.setSetting('trakt_expires_at', str(expires_at))
        __addon__.setSetting('trakt_access_token', token["access_token"])
        __addon__.setSetting('trakt_refresh_token', token["refresh_token"])
        __addon__.setSetting('trakt_indicators_active', 'true')
        __addon__.setSetting('watched_indicators', '1')
        xbmc.sleep(1000)
        try:
            user = call_trakt("/users/me", with_auth=True)
            __addon__.setSetting('trakt_user', str(user['username']))
        except: pass
        notification('Trakt Account Authorized', 3000, trakt_icon)
        return True
    notification('Trakt Error Authorizing', 3000, trakt_icon)
    return False

def trakt_remove_authentication():
    data = {"token": __addon__.getSetting('trakt_access_token')}
    try: call_trakt("oauth/revoke", data=data, with_auth=False)
    except: pass
    __addon__.setSetting('trakt_user', '')
    __addon__.setSetting('trakt_expires_at', '')
    __addon__.setSetting('trakt_access_token', '')
    __addon__.setSetting('trakt_refresh_token', '')
    __addon__.setSetting('trakt_indicators_active', 'false')
    __addon__.setSetting('watched_indicators', '0')
    notification('Trakt Account Authorization Reset', 3000)

def trakt_movies_trending(page_no):
    string = "%s_%s" % ('trakt_movies_trending', page_no)
    url = {'path': "movies/trending/%s", "params": {'limit': 20}, "page": page_no}
    return cache_object(get_trakt, string, url, False)

def trakt_movies_anticipated(page_no):
    string = "%s_%s" % ('trakt_movies_anticipated', page_no)
    url = {'path': "movies/anticipated/%s", "params": {'limit': 20}, "page": page_no}
    return cache_object(get_trakt, string, url, False)

def trakt_movies_top10_boxoffice(page_no):
    string = "%s" % 'trakt_movies_top10_boxoffice'
    url = {'path': "movies/boxoffice/%s", 'pagination': False}
    return cache_object(get_trakt, string, url, False)

def trakt_movies_mosts(period, duration, page_no):
    string = "%s_%s_%s_%s" % ('trakt_movies_mosts', period, duration, page_no)
    url = {'path': "movies/%s/%s", "path_insert": (period, duration), "params": {'limit': 20}, "page": page_no}
    return cache_object(get_trakt, string, url, False)

def trakt_movies_related(imdb_id, page_no):
    string = "%s_%s_%s" % ('trakt_movies_related', imdb_id, page_no)
    url = {'path': "movies/%s/related", "path_insert": imdb_id, "params": {'limit': 40}, "page": page_no}
    return cache_object(get_trakt, string, url, False)

def trakt_recommendations(db_type, limit=40):
    return to_utf8(call_trakt("/recommendations/{0}".format(db_type), params={'limit': limit}))

def trakt_tv_trending(page_no):
    string = "%s_%s" % ('trakt_tv_trending', page_no)
    url = {'path': "shows/trending/%s", "params": {'limit': 20}, "page": page_no}
    return cache_object(get_trakt, string, url, False)

def trakt_tv_anticipated(page_no):
    string = "%s_%s" % ('trakt_tv_anticipated', page_no)
    url = {'path': "shows/anticipated/%s", "params": {'limit': 20}, "page": page_no}
    return cache_object(get_trakt, string, url, False)

def trakt_tv_certifications(certification, page_no):
    string = "%s_%s_%s" % ('trakt_tv_certifications', certification, page_no)
    url = {'path': "shows/collected/all?certifications=%s", "path_insert": certification, "params": {'limit': 20}, "page": page_no}
    return cache_object(get_trakt, string, url, False)

def trakt_tv_mosts(period, duration, page_no):
    string = "%s_%s_%s_%s" % ('trakt_tv_mosts', period, duration, page_no)
    url = {'path': "shows/%s/%s", "path_insert": (period, duration), "params": {'limit': 20}, "page": page_no}
    return cache_object(get_trakt, string, url, False)

def trakt_tv_related(imdb_id, page_no):
    string = "%s_%s_%s" % ('trakt_tv_related', imdb_id, page_no)
    url = {'path': "shows/%s/related", "path_insert": imdb_id, "params": {'limit': 40}, "page": page_no}
    return cache_object(get_trakt, string, url, False)

def trakt_get_hidden_items(list_type):
    string = 'trakt_hidden_items_%s' % list_type
    url = {'path': "users/hidden/%s", "path_insert": list_type, "params": {'limit': 1000}, "with_auth": True, "pagination": False}
    return trakt_cache.cache_trakt_object(get_trakt, string, url)

def trakt_watched_unwatched(action, media, media_id, tvdb_id=0, season=None, episode=None, key=None):
    url = "sync/history" if action == 'mark_as_watched' else "sync/history/remove"
    if not key: key = "imdb"
    if media == 'movies': data = {"movies": [{"ids": {"tmdb": media_id}}]}
    elif media == 'episode': data = {"shows": [{"seasons": [{"episodes": [{"number": int(episode)}], "number": int(season)}], "ids": {key: media_id}}]}
    elif media =='shows': data = {"shows": [{"ids": {key: media_id}}]}
    elif media == 'season': data = {"shows": [{"ids": {key: media_id}, "seasons": [{"number": int(season)}]}]}
    result = call_trakt(url, data=data)
    if not media == 'movies':
        if tvdb_id == 0: return
        result_key = 'added' if action == 'mark_as_watched' else 'deleted'
        if not result[result_key]['episodes'] > 0:
            trakt_watched_unwatched(action, media, tvdb_id, tvdb_id, season, episode, key="tvdb")

def trakt_check_passed_list(passed_list):
    if window.getProperty('trakt_reset_passed_list') == 'true':
        passed_list = []
        window.clearProperty('trakt_reset_passed_list')
    return passed_list

def trakt_collection(db_type, page_no, letter, passed_list=[]):
    import ast
    from resources.lib.modules.nav_utils import paginate_list
    from resources.lib.modules.utils import title_key
    passed_list = trakt_check_passed_list(passed_list)
    limit = 40
    key, action, string_insert = ('movie', get_trakt_movie_id, 'movie') if db_type == 'movies' else ('show', get_trakt_tvshow_id, 'tvshow')
    if not passed_list:
        string = "trakt_collection_%s" % string_insert
        url = {"path": "sync/collection/%s", "path_insert": db_type, "params": {'extended':'full'}, "with_auth": True, "pagination": False, "method": "sort_by_headers"}
        data = trakt_cache.cache_trakt_object(get_trakt, string, url)
        data = sorted(data, key=lambda k: title_key(k[key]['title']))
        original_list = [{'media_id': action(i), 'title': i[key]['title']} for i in data]
    else: original_list = ast.literal_eval(passed_list)
    paginated_list, total_pages = paginate_list(original_list, page_no, letter, limit)
    return paginated_list, original_list, total_pages, limit

def trakt_watchlist(db_type, page_no, letter, passed_list=[]):
    import ast
    from resources.lib.modules.nav_utils import paginate_list
    from resources.lib.modules.utils import title_key
    passed_list = trakt_check_passed_list(passed_list)
    limit = 40
    key, action, string_insert = ('movie', get_trakt_movie_id, 'movie') if db_type == 'movies' else ('show', get_trakt_tvshow_id, 'tvshow')
    if not passed_list:
        string = "trakt_watchlist_%s" % string_insert
        url = {"path": "sync/watchlist/%s", "path_insert": db_type, "params": {'extended':'full'}, "with_auth": True, "pagination": False, "method": "sort_by_headers"}
        data = trakt_cache.cache_trakt_object(get_trakt, string, url)
        data = sorted(data, key=lambda k: title_key(k[key]['title']))
        original_list = [{'media_id': action(i), 'title': i[key]['title']} for i in data]
    else: original_list = ast.literal_eval(passed_list)
    paginated_list, total_pages = paginate_list(original_list, page_no, letter, limit)
    return paginated_list, original_list, total_pages, limit

def add_to_list(username, slug, data):
    result = call_trakt("/users/{0}/lists/{1}/items".format(username, slug), data = data)
    if result['added']['shows'] > 0 or result['added']['movies'] > 0:
        notification('Item added to Trakt List', 3000)
    else: notification('Error adding item to Trakt List', 3000)
    return result

def remove_from_list(username, slug, data):
    result = call_trakt("/users/{0}/lists/{1}/items/remove".format(username, slug), data=data)
    if result['deleted']['shows'] > 0 or result['deleted']['movies'] > 0:
        notification('Item removed from Trakt List', 3000)
        xbmc.executebuiltin("Container.Refresh")
    else: notification('Error removing item from Trakt List', 3000)
    return result

def add_to_watchlist(data):
    result = call_trakt("/sync/watchlist", data=data)
    if result['added']['movies'] > 0: db_type = 'movie'
    elif result['added']['shows'] > 0: db_type = 'tvshow'
    else: return notification('Error adding item to Trakt Watchlist', 3000)
    trakt_cache.clear_trakt_collection_watchlist_data('watchlist', db_type)
    notification('Item added to Trakt Watchlist', 6000)
    return result

def remove_from_watchlist(data):
    result = call_trakt("/sync/watchlist/remove", data=data)
    if result['deleted']['movies'] > 0: db_type = 'movie'
    elif result['deleted']['shows'] > 0: db_type = 'tvshow'
    else: return notification('Error removing item from Trakt Watchlist', 3000)
    trakt_cache.clear_trakt_collection_watchlist_data('watchlist', db_type)
    notification('Item removed from Trakt Watchlist', 3000)
    xbmc.executebuiltin("Container.Refresh")
    return result

def add_to_collection(data):
    result = call_trakt("/sync/collection", data=data)
    if result['added']['movies'] > 0: db_type = 'movie'
    elif result['added']['episodes'] > 0: db_type = 'tvshow'
    else: return notification('Error adding item to Trakt Collection', 3000)
    trakt_cache.clear_trakt_collection_watchlist_data('collection', db_type)
    notification('Item added to Trakt Collection', 6000)
    return result

def remove_from_collection(data):
    result = call_trakt("/sync/collection/remove", data=data)
    if result['deleted']['movies'] > 0: db_type = 'movie'
    elif result['deleted']['episodes'] > 0: db_type = 'tvshow'
    else: return notification('Error removing item from Trakt Collection', 3000)
    trakt_cache.clear_trakt_collection_watchlist_data('collection', db_type)
    params = dict(parse_qsl(sys.argv[2].replace('?','')))
    notification('Item removed from Trakt Collection', 3000)
    xbmc.executebuiltin("Container.Refresh")
    return result
    
def trakt_get_next_episodes(include_hidden=False):
    from resources.lib.modules.workers import Thread
    threads = []
    items = []
    def process(item):
        string = 'trakt_view_history_%s' % str(item["show"]["ids"]["trakt"])
        url = {'path': "shows/%s/progress/watched", "path_insert": item["show"]["ids"]["trakt"], "params": {'extended':'full,noseasons'}, "with_auth": True, "pagination": False}
        response = trakt_cache.cache_trakt_object(get_trakt, string, url)
        if response["last_episode"]:
            last_episode = response["last_episode"]
            last_episode["show"] = item["show"]
            last_episode["show"]["last_watched_at"] = item["last_watched_at"]
            items.append(last_episode)
    url = {'path': "users/me/watched/shows?extended=full%s", "with_auth": True, "pagination": False}
    shows = get_trakt_watched_tv(url)
    try: hidden_data = trakt_get_hidden_items("progress_watched")
    except: hidden_data = []
    if include_hidden:
        all_shows = [str(get_trakt_tvshow_id(i)) for i in shows]
        hidden_shows = [str(get_trakt_tvshow_id(i)) for i in hidden_data if i["type"] == "show"]
        return all_shows, hidden_shows
    hidden_shows = [i["show"]["ids"]["trakt"] for i in hidden_data if i["type"] == "show"]
    shows = [i for i in shows if i['show']['ids']['trakt'] not in hidden_shows]
    for item in shows: threads.append(Thread(process, item))
    [i.start() for i in threads]
    [i.join() for i in threads]
    xbmc.sleep(500)
    return items

def hide_unhide_trakt_items(action, db_type, media_id, list_type):
    db_type = 'movies' if db_type in ['movie', 'movies'] else 'shows'
    key = 'tmdb' if db_type == 'movies' else 'imdb'
    url = "users/hidden/{}".format(list_type) if action == 'hide' else "users/hidden/{}/remove".format(list_type)
    data = {db_type: [{'ids': {key: media_id}}]}
    call_trakt(url, data=data)
    trakt_cache.clear_trakt_hidden_data(list_type)

def hide_recommendations(db_type='', imdb_id=''):
    params = dict(parse_qsl(sys.argv[2].replace('?','')))
    db_type = params.get('db_type') if 'db_type' in params else db_type
    imdb_id = params.get('imdb_id') if 'imdb_id' in params else imdb_id
    result = call_trakt("/recommendations/{0}/{1}".format(db_type, imdb_id), method='delete')
    notification('Item hidden from Trakt Recommendations', 3000)
    xbmc.sleep(500)
    xbmc.executebuiltin("Container.Refresh")
    return result

def make_new_trakt_list():
    import urllib
    params = dict(parse_qsl(sys.argv[2].replace('?','')))
    mode = params.get('mode')
    list_title = dialog.input("Name New List", type=xbmcgui.INPUT_ALPHANUM)
    if not list_title: return
    list_name = urllib.unquote(list_title)
    data = {'name': list_name, 'privacy': 'private', 'allow_comments': False}
    call_trakt("users/me/lists", data=data)
    trakt_cache.clear_trakt_list_data('my_lists')
    notification('{}'.format('Trakt list Created', 3000))
    xbmc.executebuiltin("Container.Refresh")

def delete_trakt_list():
    params = dict(parse_qsl(sys.argv[2].replace('?','')))
    user = params.get('user')
    list_slug = params.get('list_slug')
    confirm = dialog.yesno('Are you sure?', 'Continuing will delete this Trakt List')
    if confirm == True:
        url = "users/{0}/lists/{1}".format(user, list_slug)
        call_trakt(url, is_delete=True)
        trakt_cache.clear_trakt_list_data('my_lists')
        notification('List removed from Trakt', 3000)
        xbmc.executebuiltin("Container.Refresh")
    else: return

def search_trakt_lists():
    params = dict(parse_qsl(sys.argv[2].replace('?','')))
    mode = params.get('mode')
    page = params.get('new_page') if 'new_page' in params else '1'
    search_title = params.get('search_title') if 'search_title' in params else dialog.input("Search Trakt Lists", type=xbmcgui.INPUT_ALPHANUM)
    if not search_title: return
    lists, pages = call_trakt("search", params={'type': 'list', 'fields': 'name, description', 'query': search_title, 'limit': 25}, pagination= True, page = page)
    for item in lists:
        try:
            cm = []
            list_info = item["list"]
            try: description = list_info["description"]
            except: decription = ''
            url_params = {'mode': 'trakt.build_trakt_list', 'user': list_info["username"], 'slug': list_info["ids"]["slug"]}
            url = build_url(url_params)
            display = '[B]' + list_info["name"] + '[/B] - [I]by ' + list_info["username"] + ' - ' + str(list_info["item_count"]) + ' items[/I]'
            listitem = xbmcgui.ListItem(display)
            listitem.setArt({'thumb': os.path.join(icon_directory, "search_trakt_lists.png"), 'fanart': fanart})
            cm.append(("Like this List",'XBMC.RunPlugin(%s?mode=%s&user=%s&list_slug=%s)' \
                % (__url__, 'trakt.trakt_like_a_list', list_info["username"], list_info["ids"]["slug"])))
            cm.append(("Add List to Subscriptions",'XBMC.RunPlugin(%s?mode=%s&user=%s&list_slug=%s)' \
                % (__url__, 'trakt.add_list_to_subscriptions', list_info["username"], list_info["ids"]["slug"])))
            listitem.setInfo('video', {'plot': description})
            listitem.addContextMenuItems(cm, replaceItems=False)
            xbmcplugin.addDirectoryItems(handle=__handle__, items=[(url, listitem, True)])
        except: pass
    if pages > page:
        new_page = int(page) + 1
        add_dir({'mode': mode, 'search_title': search_title, 'new_page': str(new_page),
            'foldername': mode}, 'Next Page >>', iconImage='item_next.png')
    xbmcplugin.setContent(__handle__, 'files')
    xbmcplugin.endOfDirectory(__handle__)
    setView('view.main')

def trakt_add_to_list():
    params = dict(parse_qsl(sys.argv[2].replace('?','')))
    tmdb_id = int(params.get('tmdb_id'))
    imdb_id = params.get('imdb_id')
    db_type = params.get('db_type')
    key, media_key, media_id = ('movies', 'tmdb', tmdb_id) if db_type == 'movie' else ('shows', 'imdb', imdb_id)
    selected = get_trakt_list_selection()
    if selected is not None:
        data = {key: [{"ids": {media_key: media_id}}]}
        if selected['user'] == 'Watchlist':
            add_to_watchlist(data)
        elif selected['user'] == 'Collection':
            add_to_collection(data)
        else:
            user = selected['user']
            slug = selected['slug']
            add_to_list(user, slug, data)
            trakt_cache.clear_trakt_list_contents_data(user=user, slug=slug)

def trakt_remove_from_list():
    params = dict(parse_qsl(sys.argv[2].replace('?','')))
    tmdb_id = int(params.get('tmdb_id'))
    imdb_id = params.get('imdb_id')
    db_type = params.get('db_type')
    key, media_key, media_id = ('movies', 'tmdb', tmdb_id) if db_type == 'movie' else ('shows', 'imdb', imdb_id)
    selected = get_trakt_list_selection()
    if selected is not None:
        data = {key: [{"ids": {media_key: media_id}}]}
        if selected['user'] == 'Watchlist':
            remove_from_watchlist(data)
        elif selected['user'] == 'Collection':
            remove_from_collection(data)
        else:
            user = selected['user']
            slug = selected['slug']
            remove_from_list(user, slug, data)
            trakt_cache.clear_trakt_list_contents_data(user=user, slug=slug)

def trakt_like_a_list():
    params = dict(parse_qsl(sys.argv[2].replace('?','')))
    user = params.get('user')
    list_slug = params.get('list_slug')
    try:
        call_trakt("/users/{0}/lists/{1}/like".format(user, list_slug), method='post')
        trakt_cache.clear_trakt_list_data('liked_lists')
        notification('List Item Liked', 3000)
    except: notification('{}'.format('Trakt Error Liking List', 3000))

def trakt_unlike_a_list():
    params = dict(parse_qsl(sys.argv[2].replace('?','')))
    user = params.get('user')
    list_slug = params.get('list_slug')
    try:
        call_trakt("/users/{0}/lists/{1}/like".format(user, list_slug), method='delete')
        trakt_cache.clear_trakt_list_data('liked_lists')
        notification('List Item Unliked', 4500)
        xbmc.executebuiltin("Container.Refresh")
    except: notification('{}'.format('Trakt Error Unliking List', 3000))

def get_trakt_list_selection(list_choice=False):
    name = '%s%s'
    my_lists = sorted([{'name': item["name"], 'display': name % (('[B]PERSONAL:[/B] ' if list_choice else ''), item["name"]), 'user': item["user"]["username"], 'slug': item["ids"]["slug"]} for item in get_trakt_my_lists(build_list=False)], key=lambda k: k['name'])
    if list_choice:
        liked_lists = sorted([{'name': item["list"]["name"], 'display': name % ('[B]LIKED:[/B] ', item["list"]["name"]), 'user': item["list"]["user"]["username"], 'slug': item["list"]["ids"]["slug"]} for item in get_trakt_liked_lists(build_list=False)], key=lambda k: (k['display']))
        my_lists.extend(liked_lists)
    else:
        my_lists.insert(0, {'name': 'Collection', 'display': 'Collection ', 'user': 'Collection', 'slug': 'Collection'})
        my_lists.insert(0, {'name': 'Watchlist', 'display': 'Watchlist ',  'user': 'Watchlist', 'slug': 'Watchlist'})
    selection = dialog.select("Select list", [l["display"] for l in my_lists])
    if selection >= 0: return my_lists[selection]
    else: return None

def get_trakt_my_lists(build_list=True):
    try:
        string = "trakt_my_lists"
        url = {"path": "users/me/lists%s", "with_auth": True, "pagination": False}
        lists = trakt_cache.cache_trakt_object(get_trakt, string, url)
        if not build_list: return lists
        for item in lists:
            cm = []
            url_params = {'mode': 'trakt.build_trakt_list', 'user': item["user"]["username"], 'slug': item["ids"]["slug"]}
            make_new_list_url = {'mode': 'trakt.make_new_trakt_list'}
            delete_list_url = {'mode': 'trakt.delete_trakt_list', 'user': item["user"]["username"], 'list_slug': item["ids"]["slug"]}
            add_to_subscriptions_url = {'mode': 'trakt.add_list_to_subscriptions', 'user': item["user"]["username"], 'list_slug': item["ids"]["slug"]}
            trakt_selection_url = {'mode': 'trakt.add_list_to_menu', 'method': 'add_trakt_external', 'name': item["name"], 'user': item["user"]["username"], 'slug': item["ids"]["slug"]}
            trakt_selection_favourites_url = {'mode': 'trakt.add_list_to_menu', 'method': 'add_trakt_external', 'name': item["name"], 'user': item["user"]["username"], 'slug': item["ids"]["slug"], 'list_name': 'FavouriteList'}
            url = build_url(url_params)
            cm.append(("[B]Make a new Trakt list[/B]",'XBMC.RunPlugin(%s)' % build_url(make_new_list_url)))
            cm.append(("[B]Delete this list[/B]",'XBMC.RunPlugin(%s)' % build_url(delete_list_url)))
            cm.append(("[B]Add this list to Subscriptions[/B]",'XBMC.RunPlugin(%s)' % build_url(add_to_subscriptions_url)))
            cm.append(("[B]Add this list to a Menu[/B]",'XBMC.RunPlugin(%s)' % build_url(trakt_selection_url)))
            listitem = xbmcgui.ListItem(item["name"])
            listitem.setArt({'thumb': my_list_icon, 'fanart': fanart})
            listitem.addContextMenuItems(cm, replaceItems=False)
            xbmcplugin.addDirectoryItem(__handle__, url, listitem, isFolder=True)
            xbmcplugin.addSortMethod(__handle__, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    except: pass
    xbmcplugin.setContent(__handle__, 'files')
    xbmcplugin.endOfDirectory(__handle__)
    setView('view.main')

def get_trakt_liked_lists(build_list=True):
    try:
        string = "trakt_liked_lists"
        url = {"path": "users/likes/lists%s", "pagination": False, "with_auth": True}
        lists = trakt_cache.cache_trakt_object(get_trakt, string, url)
        if not build_list: return lists
        for item in lists:
            cm = []
            url_params = {'mode': 'trakt.build_trakt_list', 'user': item["list"]["user"]["username"], 'slug': item["list"]["ids"]["slug"]}
            unlike_list_url = {'mode': 'trakt.trakt_unlike_a_list', 'user': item["list"]["user"]["username"], 'list_slug': item["list"]["ids"]["slug"]}
            add_to_subscriptions_url = {'mode': 'trakt.add_list_to_subscriptions', 'user': item["list"]["user"]["username"], 'list_slug': item["list"]["ids"]["slug"]}
            trakt_selection_url = {'mode': 'trakt.add_list_to_menu', 'method': 'add_trakt_external', 'name': item["list"]["name"], 'user': item["list"]["user"]["username"], 'slug': item["list"]["ids"]["slug"]}
            trakt_selection_favourites_url = {'mode': 'trakt.add_list_to_menu', 'method': 'add_trakt_external', 'name': item["list"]["name"], 'user': item["list"]["user"]["username"], 'slug': item["list"]["ids"]["slug"], 'list_name': 'FavouriteList'}
            url = build_url(url_params)
            listitem = xbmcgui.ListItem(item["list"]["name"])
            listitem.setArt({'thumb': liked_list_icon, 'fanart': fanart})
            cm.append(("[B]Unlike this list[/B]",'XBMC.RunPlugin(%s)' % build_url(unlike_list_url)))
            cm.append(("[B]Add this list to Subscriptions[/B]",'XBMC.RunPlugin(%s)' % build_url(add_to_subscriptions_url)))
            cm.append(("[B]Add this list to a Menu[/B]",'XBMC.RunPlugin(%s)' % build_url(trakt_selection_url)))
            listitem.addContextMenuItems(cm, replaceItems=False)
            xbmcplugin.addDirectoryItem(__handle__, url, listitem, isFolder=True)
            xbmcplugin.addSortMethod(__handle__, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    except: pass
    xbmcplugin.setContent(__handle__, 'files')
    xbmcplugin.endOfDirectory(__handle__)
    setView('view.main')

def build_trakt_list():
    import ast
    from resources.lib.indexers.movies import Movies
    from resources.lib.indexers.tvshows import TVShows
    from resources.lib.modules.nav_utils import paginate_list
    def _add_misc_dir(url_params, list_name='Next Page >>', info='Navigate to Next Page...', iconImage='item_next.png'):
        listitem = xbmcgui.ListItem(list_name, iconImage=os.path.join(settings.get_theme(), iconImage))
        listitem.setArt({'fanart': __addon__.getAddonInfo('fanart')})
        listitem.setInfo('video', {'title': list_name, 'plot': info})
        if url_params['mode'] == 'build_navigate_to_page': listitem.addContextMenuItems([("[B]Switch Jump To Action[/B]","XBMC.RunPlugin(%s)" % build_url({'mode': 'toggle_jump_to'}))])
        xbmcplugin.addDirectoryItem(handle=__handle__, url=build_url(url_params), listitem=listitem, isFolder=True)
    params = dict(parse_qsl(sys.argv[2].replace('?','')))
    user = params.get('user')
    slug = params.get('slug')
    page_no = int(params.get('new_page', 1))
    letter = params.get('new_letter', 'None')
    passed_list = params.get('passed_list', [])
    limit = 40
    passed_list = trakt_check_passed_list(passed_list)
    try:
        if not passed_list:
            original_list = []
            result = get_trakt_list_contents(user, slug)
            for item in result:
                try:
                    media_type = item['type']
                    key, action = ('movie', get_trakt_movie_id) if media_type == 'movie' else ('show', get_trakt_tvshow_id)
                    original_list.append({'media_type': media_type, 'title': item[key]['title'], 'media_id': action(item)})
                except: pass
        else: original_list = ast.literal_eval(passed_list)
        paginated_list, total_pages = paginate_list(original_list, page_no, letter, limit)
        movie_list = [i['media_id'] for i in paginated_list if i['media_type'] == 'movie']
        show_list = [i['media_id'] for i in paginated_list if i['media_type'] == 'show']
        content = 'movies' if len(movie_list) > len(show_list) else 'tvshows'
        if total_pages > 2: _add_misc_dir({'mode': 'build_navigate_to_page', 'current_page': page_no, 'total_pages': total_pages, 'transfer_mode': 'trakt.build_trakt_list', 'passed_list': original_list}, 'Jump To...', 'Jump To a Certain Page/Letter...', 'item_jump.png')
        if len(movie_list) >= 1: Movies(movie_list).worker()
        if len(show_list) >= 1: TVShows(show_list).worker()
        if len(paginated_list) == limit: _add_misc_dir({'mode': 'trakt.build_trakt_list', 'passed_list': original_list, 'user': user, 'slug': slug, 'new_page': str(page_no + 1), 'new_letter': letter})
        xbmcplugin.setContent(__handle__, content)
        xbmcplugin.endOfDirectory(__handle__)
        setView('view.trakt_list')
    except: notification('List Unavailable', 3000)

def get_trakt_list_contents(user, slug):
    string = "trakt_list_contents_%s_%s" % (user, slug)
    url = {"path": "users/%s/lists/%s/items", "path_insert": (user, slug), "params": {'extended':'full'}, "with_auth": True, "method": "sort_by_headers"}
    return trakt_cache.cache_trakt_object(get_trakt, string, url)

# def trakt_get_calendar():
#     return call_trakt("calendars/my/shows".format(type))

def get_trakt_movie_id(item):
    item = item['movie']['ids'] if 'movie' in item else item['ids']
    if item['tmdb']: return item['tmdb']
    from tikimeta.tmdb import tmdbMoviesExternalID
    tmdb_id = None
    if item['imdb']:
        try:
            meta = tmdbMoviesExternalID('imdb_id', item['imdb'])
            tmdb_id = meta['id']
        except: pass
    return tmdb_id

def get_trakt_tvshow_id(item):
    item = item['show']['ids'] if 'show' in item else item['ids']
    if item['tmdb']: return item['tmdb']
    from tikimeta.tmdb import tmdbTVShowsExternalID
    tmdb_id = None
    if item['imdb']:
        try: 
            meta = tmdbTVShowsExternalID('imdb_id', item['imdb'])
            tmdb_id = meta['id']
        except: tmdb_id = None
    if not tmdb_id:
        if item['tvdb']:
            try: 
                meta = tmdbTVShowsExternalID('tvdb_id', item['tvdb'])
                tmdb_id = meta['id']
            except: tmdb_id = None
    return tmdb_id

def trakt_indicators_movies():
    url = {'path': "sync/watched/movies%s", "with_auth": True, "pagination": False}
    return trakt_cache.cache_trakt_object(process_trakt_watched_movies, 'trakt_indicators_movies', url)

def trakt_indicators_tv():
    url = {'path': "users/me/watched/shows?extended=full%s", "with_auth": True, "pagination": False}
    return trakt_cache.cache_trakt_object(process_trakt_watched_tv, 'trakt_indicators_tv', url)

def process_trakt_watched_movies(url):
    result = get_trakt(url)
    for i in result:
        i.update({'tmdb_id': get_trakt_movie_id(i)})
    result = [(i['tmdb_id'], i['movie']['title']) for i in result if i['tmdb_id'] != None]
    return result

def process_trakt_watched_tv(url):
    result = get_trakt_watched_tv(url)
    for i in result: i.update({'tmdb_id': get_trakt_tvshow_id(i)})
    result = [(i['tmdb_id'], i['show']['aired_episodes'], sum([[(s['number'], e['number']) for e in s['episodes']] for s in i['seasons']], []), i['show']['title']) for i in result if i['tmdb_id'] != None]
    result = [(int(i[0]), int(i[1]), i[2], i[3]) for i in result]
    return result

def get_trakt_watched_tv(url):
    return trakt_cache.cache_trakt_object(get_trakt, 'trakt_watched_shows', url)

def get_trakt(url):
    result = call_trakt(url['path'] % url.get('path_insert', ''), params=url.get('params', {}), data=url.get('data'), is_delete=url.get('is_delete', False), with_auth=url.get('with_auth', False), method=url.get('method'), pagination=url.get('pagination', True), page=url.get('page'))
    return result[0] if url.get('pagination', True) else result

def sync_watched_trakt_to_fen(refresh=False):
    if refresh: window.setProperty('fen_trakt_sync_complete', 'false')
    if window.getProperty('fen_trakt_sync_complete') == 'true': return
    if settings.watched_indicators() in (0, 2): return
    import os
    from datetime import datetime
    from resources.lib.modules.utils import clean_file_name
    try: from sqlite3 import dbapi2 as database
    except ImportError: from pysqlite2 import dbapi2 as database
    not_home_window = xbmc.getInfoLabel('Container.PluginName')
    processed_trakt_tv = []
    compare_trakt_tv = []
    try:
        if not_home_window:
            bg_dialog = xbmcgui.DialogProgressBG()
            bg_dialog.create('Trakt & Fen Watched Status', 'Please Wait')
        WATCHED_DB = os.path.join(profile_dir, "watched_status.db")
        settings.check_database(WATCHED_DB)
        dbcon = database.connect(WATCHED_DB)
        dbcur = dbcon.cursor()
        trakt_watched_movies = trakt_indicators_movies()
        trakt_watched_tv = trakt_indicators_tv()
        process_movies = False
        process_tvshows = False
        dbcur.execute("SELECT media_id FROM watched_status WHERE db_type = ?", ('movie',))
        fen_watched_movies = dbcur.fetchall()
        fen_watched_movies = [int(i[0]) for i in fen_watched_movies]
        compare_trakt_movies = [i[0] for i in trakt_watched_movies]
        process_trakt_movies = trakt_watched_movies
        if not sorted(fen_watched_movies) == sorted(compare_trakt_movies): process_movies = True
        if not_home_window: bg_dialog.update(50, 'Trakt & Fen Watched Status', 'Checking Movies Watched Status')
        xbmc.sleep(100)
        dbcur.execute("SELECT media_id, season, episode FROM watched_status WHERE db_type = ?", ('episode',))
        fen_watched_episodes = dbcur.fetchall()
        fen_watched_episodes = [(int(i[0]), i[1], i[2]) for i in fen_watched_episodes]
        for i in trakt_watched_tv:
            for x in i[2]:
                compare_trakt_tv.append((i[0], x[0], x[1]))
                processed_trakt_tv.append((i[0], x[0], x[1], i[3]))
        if not sorted(fen_watched_episodes) == sorted(compare_trakt_tv): process_tvshows = True
        if not_home_window: bg_dialog.update(100, 'Trakt & Fen Watched Status', 'Checking Episodes Watched Status')
        xbmc.sleep(100)
        if not process_movies and not process_tvshows and not_home_window:
            bg_dialog.close()
        if process_movies:
            dbcur.execute("DELETE FROM watched_status WHERE db_type=?", ('movie',))
            for count, i in enumerate(process_trakt_movies):
                try:
                    if not_home_window: bg_dialog.update(int(float(count) / float(len(trakt_watched_movies)) * 100), 'Trakt & Fen Watched Status', 'Syncing Movie Watched Status')
                    last_played = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    dbcur.execute("INSERT OR IGNORE INTO watched_status VALUES (?, ?, ?, ?, ?, ?)", ('movie', str(i[0]), '', '', last_played, clean_file_name(to_utf8(i[1]))))
                except: pass
        if process_tvshows:
            dbcur.execute("DELETE FROM watched_status WHERE db_type=?", ('episode',))
            for count, i in enumerate(processed_trakt_tv):
                try:
                    if not_home_window: bg_dialog.update(int(float(count) / float(len(processed_trakt_tv)) * 100), 'Trakt & Fen Watched Status', 'Syncing Episode Watched Status')
                    last_played = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    dbcur.execute("INSERT OR IGNORE INTO watched_status VALUES (?, ?, ?, ?, ?, ?)", ('episode', str(i[0]), i[1], i[2], last_played, clean_file_name(to_utf8(i[3]))))
                except: pass
        if process_movies or process_tvshows:
            dbcon.commit()
        if not_home_window:
            bg_dialog.close()
            from resources.lib.modules.nav_utils import notification
            notification('Trakt Watched to Fen Watched Sync Complete', time=4000)
        window.setProperty('fen_trakt_sync_complete', 'true')
        __addon__.setSetting('trakt_indicators_active', 'true')
        if refresh: xbmc.executebuiltin("Container.Refresh")
    except:
        if not_home_window:
            try: bg_dialog.close()
            except: pass
        from resources.lib.modules.nav_utils import notification
        notification('Error getting Trakt Watched Info', time=3500)
        pass

