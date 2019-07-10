# -*- coding: utf-8 -*-
import xbmc, xbmcaddon
import sys, os
# from resources.lib.modules.utils import logger


__addon_id__ = 'plugin.video.fen'
__addon__ = xbmcaddon.Addon(id=__addon_id__)
__url__ = sys.argv[0]
__handle__ = int(sys.argv[1])
addon_dir = xbmc.translatePath(__addon__.getAddonInfo('path'))
profile_dir = xbmc.translatePath(__addon__.getAddonInfo('profile'))
icon_image = __addon__.getAddonInfo('icon')
fanart = __addon__.getAddonInfo('fanart')

def build_navigate_to_page():
    import xbmcgui
    import json
    import ast
    from urlparse import parse_qsl
    from resources.lib.modules.settings import get_theme, nav_jump_use_alphabet
    use_alphabet = nav_jump_use_alphabet()
    params = dict(parse_qsl(sys.argv[2].replace('?','')))
    if use_alphabet:
        start_list = [chr(i) for i in range(97,123)]
        choice_list = [xbmcgui.ListItem(i.upper(), "[I]Jump to %s Starting with '%s'[/I]" % (params.get('db_type'), i.upper()), iconImage=os.path.join(get_theme(), 'item_jump.png')) for i in start_list]
    else:
        start_list = [str(i) for i in range(1, int(params.get('total_pages'))+1)]
        start_list.remove(params.get('current_page'))
        choice_list = [xbmcgui.ListItem('Page %s' % i, '[I]Jump to Page %s[/I]' % i, iconImage=os.path.join(get_theme(), 'item_jump.png')) for i in start_list]
    chosen_start = xbmcgui.Dialog().select('Fen', choice_list, useDetails=True)
    xbmc.sleep(500)
    if chosen_start < 0: return
    new_start = start_list[chosen_start]
    if use_alphabet:
        new_page = ''
        new_letter = new_start
    else:
        new_page = new_start
        new_letter = None
    final_params = {'mode': params.get('transfer_mode', ''),
                    'action': params.get('transfer_action', ''),
                    'new_page': new_page,
                    'new_letter': new_letter,
                    'passed_list': params.get('passed_list', ''),
                    'query': params.get('query', ''),
                    'actor_id': params.get('actor_id', '')}
    url_params = {'mode': 'container_update', 'final_params': json.dumps(final_params)}
    xbmc.executebuiltin('XBMC.RunPlugin(%s)' % build_url(url_params))

def paginate_list(item_list, page, letter, limit=20):
    def _get_start_index(letter):
        if letter == 't':
            try:
                beginswith_tuple = ('s', 'the s', 'a s', 'an s')
                indexes = [i for i,v in enumerate(title_list) if v.startswith(beginswith_tuple)]
                start_index = indexes[-1:][0] + 1
            except: start_index = None
        else:
            beginswith_tuple = (letter, 'the %s' % letter, 'a %s' % letter, 'an %s' % letter)
            try: start_index = next(i for i,v in enumerate(title_list) if v.startswith(beginswith_tuple))
            except: start_index = None
        return start_index
    if letter != 'None':
        import itertools
        total_tries = 26
        title_list = [i['title'].lower() for i in item_list]
        start_list = [chr(i) for i in range(97,123)]
        letter_index = start_list.index(letter)
        test_list = [element for element in list(itertools.chain.from_iterable([val for val in itertools.izip_longest(start_list[letter_index:], start_list[:letter_index][::-1])])) if element != None]
        for i in test_list:
            start_index = _get_start_index(i)
            if start_index: break
        item_list = item_list[start_index:]
    pages = [item_list[i:i+limit] for i in range(0, len(item_list), limit)]
    total_pages = len(item_list)/limit + 1
    return pages[page - 1], total_pages

def container_update():
    from urlparse import parse_qsl
    import json
    params = dict(parse_qsl(sys.argv[2].replace('?','')))
    xbmc.sleep(500)
    xbmc.executebuiltin('XBMC.Container.Update(%s)' % build_url(json.loads(params['final_params'])))

def get_kodi_version():
    return int(xbmc.getInfoLabel("System.BuildVersion")[0:2])

def show_busy_dialog():
    if get_kodi_version() >= 18: xbmc.executebuiltin('ActivateWindow(busydialognocancel)')
    else: xbmc.executebuiltin('ActivateWindow(busydialog)')

def hide_busy_dialog():
    if get_kodi_version() >= 18: xbmc.executebuiltin('Dialog.Close(busydialognocancel)')
    else: xbmc.executebuiltin('Dialog.Close(busydialog)')

def close_all_dialog():
    xbmc.executebuiltin('Dialog.Close(all,true)')

def sleep(time):
    xbmc.sleep(time)

def play_trailer(url, all_trailers=[]):
    if all_trailers:
        import xbmcgui
        import json
        from resources.lib.modules.utils import clean_file_name, to_utf8
        all_trailers = to_utf8(json.loads(all_trailers))
        video_choice = xbmcgui.Dialog().select("Youtube Videos...", [clean_file_name(i['name']) for i in all_trailers])
        if video_choice < 0: return
        url = 'plugin://plugin.video.youtube/play/?video_id=%s' % all_trailers[video_choice].get('key')
    try: xbmc.executebuiltin('RunPlugin(%s)' % url)
    except: notification('Error Playing Trailer')

def show_text(heading=None, text_file=None):
    import xbmcgui
    from urlparse import parse_qsl
    params = dict(parse_qsl(sys.argv[2].replace('?','')))
    heading = params.get('heading') if 'heading' in params else heading
    text_file = params.get('text_file') if 'text_file' in params else text_file
    text = open(text_file).read()
    try: xbmcgui.Dialog().textviewer(heading, text)
    except: return

def open_settings(query):
    try:
        xbmc.sleep(500)
        kodi_version = get_kodi_version()
        button = (-100) if kodi_version <= 17 else (100)
        control = (-200) if kodi_version <= 17 else (80)
        hide_busy_dialog()
        menu, function = query.split('.')
        xbmc.executebuiltin('Addon.OpenSettings(%s)' % __addon_id__)
        xbmc.executebuiltin('SetFocus(%i)' % (int(menu) - button))
        xbmc.executebuiltin('SetFocus(%i)' % (int(function) - control))
    except: return

def toggle_setting(setting_id=None, setting_value=None, refresh=False):
    if not setting_id:
        from urlparse import parse_qsl
        params = dict(parse_qsl(sys.argv[2].replace('?','')))
        setting_id = params.get('setting_id')
        setting_value = params.get('setting_value')
        refresh = params.get('refresh')
    __addon__.setSetting(setting_id, setting_value)
    if refresh:
        xbmc.executebuiltin('Container.Refresh')

def build_url(query):
    import urllib
    from resources.lib.modules.utils import to_utf8
    return __url__ + '?' + urllib.urlencode(to_utf8(query))

def notification(line1, time=5000, icon=icon_image, sound=False):
    import xbmcgui
    xbmcgui.Dialog().notification('Fen', line1, icon, time, sound)

def add_dir(url_params, list_name, iconImage='DefaultFolder.png', fanartImage=None, isFolder=True):
    import xbmcgui, xbmcplugin
    from resources.lib.modules.settings import get_theme
    icon = os.path.join(get_theme(), iconImage)
    fanArt = fanart if fanartImage == None else fanartImage
    info = url_params.get('info', '')
    url = build_url(url_params)
    listitem = xbmcgui.ListItem(list_name, iconImage=icon)
    listitem.setArt({'fanart': fanArt})
    listitem.setInfo('video', {'title': list_name, 'plot': info})
    xbmcplugin.addDirectoryItem(handle=__handle__, url=url, listitem=listitem, isFolder=isFolder)

def setView(view_type):
    from resources.lib.modules.settings import check_database
    try: from sqlite3 import dbapi2 as database
    except: from pysqlite2 import dbapi2 as database
    try:
        VIEWS_DB = os.path.join(profile_dir, "views.db")
        check_database(VIEWS_DB)
        dbcon = database.connect(VIEWS_DB)
        dbcur = dbcon.cursor()
        dbcur.execute("SELECT view_id FROM views WHERE view_type = ?", (str(view_type),))
        view_id = dbcur.fetchone()[0]
        xbmc.sleep(250)
        return xbmc.executebuiltin("Container.SetViewMode(%s)" % str(view_id))
    except: return

def similar_related_choice():
    from urlparse import parse_qsl
    from resources.lib.modules.utils import selection_dialog
    import tikimeta
    params = dict(parse_qsl(sys.argv[2].replace('?','')))
    db_type = params.get('db_type')
    (meta_type, action) = ('movie', tikimeta.movie_meta) if db_type == 'movies' else ('tvshow', tikimeta.tvshow_meta)
    imdb_id = params.get('imdb_id') if 'tt' in params.get('imdb_id') else action('tmdb_id', params.get('tmdb_id'))['imdb_id']
    dl = ['Similar','Related'] if imdb_id else ['Similar']
    fl = ['tmdb_%s_similar' % db_type,'trakt_%s_related' % db_type] if imdb_id else ['tmdb_%s_similar' % db_type]
    string = 'Please Choose Movie Search Option:' if db_type == 'movie' else 'Please Choose TV Show Search Option:'
    mode = 'build_%s_list' % meta_type
    choice = selection_dialog(dl, fl, string)
    if not choice: return
    try:
        sim_rel_params = {'mode': mode, 'action': choice, 'tmdb_id': params.get('tmdb_id'), 'imdb_id': imdb_id, 'from_search': params.get('from_search')}
        xbmc.executebuiltin('XBMC.Container.Update(%s)' % build_url(sim_rel_params))
    except: return

def cache_object(function, string, url, json=True, expiration=24):
    from datetime import timedelta
    from resources.lib.modules import fen_cache
    from resources.lib.modules.utils import to_utf8
    _cache = fen_cache.FenCache()
    cache = _cache.get(string)
    if cache: return to_utf8(cache)
    if json: result = function(url).json()
    else: result = function(url)
    _cache.set(string, result, expiration=timedelta(hours=expiration))
    return to_utf8(result)

def refresh_cached_data(db_type=None, id_type=None, media_id=None, from_list=False):
    from urlparse import parse_qsl
    import tikimeta
    params = dict(parse_qsl(sys.argv[2].replace('?','')))
    try:
        tikimeta.delete_cache_item(params.get('db_type', db_type), params.get('id_type', id_type), params.get('media_id', media_id))
        if params.get('from_list', from_list): return True
        notification('Cache refreshed for item')
        xbmc.executebuiltin('Container.Refresh')
    except:
        if params.get('from_list', from_list): return False
        notification('Refreshing of Cache failed for item', 4500)

def remove_unwanted_info_keys(dict_item):
    remove = ('fanart_added', 'art', 'cast', 'imdb_id', 'item_no', 'poster', 'rootname', 'tmdb_id', 'tvdb_id',
        'all_trailers', 'total_episodes', 'total_seasons', 'total_watched', 'total_unwatched', 'poster',
        'fanart', 'banner', 'clearlogo', 'clearart', 'landscape')
    for k in remove: dict_item.pop(k, None)
    return dict_item

def clear_cache(cache):
    if cache == 'meta':
        from tikimeta import delete_meta_cache
        if not delete_meta_cache(): return
        description = 'Meta Data'
    elif cache == 'providers':
        from tikiscrapers import deleteProviderCache
        if not deleteProviderCache(): return
        description = 'External Results'
    elif cache == 'trakt':
        from resources.lib.modules.trakt_cache import clear_all_trakt_cache_data
        if not clear_all_trakt_cache_data(): return
        description = 'Trakt Cache'
    else:
        import xbmcgui, xbmcvfs
        LIST_DATABASE = os.path.join(profile_dir, 'fen_cache.db')
        if not xbmcvfs.exists(LIST_DATABASE): return
        if not xbmcgui.Dialog().yesno('Are you sure?','Fen will Clear all List Data.'): return
        try: from sqlite3 import dbapi2 as database
        except ImportError: from pysqlite2 import dbapi2 as database
        from resources.lib.modules.settings import media_lists
        media_lists = media_lists()
        window = xbmcgui.Window(10000)
        dbcon = database.connect(LIST_DATABASE)
        dbcur = dbcon.cursor()
        sql = """SELECT id from fencache where id LIKE """
        for item in media_lists: sql = sql + "'" + item + "'" + ' OR id LIKE '
        sql = sql[:-12]
        dbcur.execute(sql)
        results = dbcur.fetchall()
        remove_list = [str(i[0]) for i in results]
        for item in remove_list:
            dbcur.execute("""DELETE FROM fencache WHERE id=?""", (item,))
            window.clearProperty(item)
        dbcon.commit()
        dbcon.close()
        description = 'List Data'
    notification('%s Cleared' % description)



