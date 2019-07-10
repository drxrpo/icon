import xbmc, xbmcaddon, xbmcgui, xbmcplugin
import sys, os
import json
from datetime import datetime
import time
import _strptime  # fix bug in python import
from resources.lib.modules.workers import Thread
from resources.lib.modules.nav_utils import build_url, setView
from resources.lib.modules.trakt import sync_watched_trakt_to_fen, get_trakt_tvshow_id
from resources.lib.indexers.tvshows import make_fresh_tvshow_meta, build_episode
from resources.lib.modules import settings
try: from sqlite3 import dbapi2 as database
except ImportError: from pysqlite2 import dbapi2 as database
# from resources.lib.modules.utils import logger

__addon_id__ = 'plugin.video.fen'
__addon__ = xbmcaddon.Addon(id=__addon_id__)
__addon_profile__ = xbmc.translatePath(__addon__.getAddonInfo('profile'))
__handle__ = int(sys.argv[1])

WATCHED_DB = os.path.join(__addon_profile__, "watched_status.db")

result = []

def build_next_episode():
    sync_watched_trakt_to_fen()
    try:
        threads = []
        seen = set()
        ep_list = []
        ne_settings = settings.nextep_content_settings()
        ne_display = settings.nextep_display_settings()
        if ne_settings['include_unwatched']:
            for i in get_unwatched_next_episodes(): ep_list.append(i)
        if settings.watched_indicators() in (1, 2):
            from resources.lib.modules.trakt import trakt_get_next_episodes
            info = trakt_get_next_episodes()
            for item in info:
                try:
                    ep_list.append({"tmdb_id": get_trakt_tvshow_id(item), "season": item['season'], "episode": item['number'], "last_played": item['show']['last_watched_at']})
                except: pass
        else:
            settings.check_database(WATCHED_DB)
            dbcon = database.connect(WATCHED_DB)
            dbcur = dbcon.cursor()
            dbcur.execute('''SELECT media_id, season, episode, last_played FROM watched_status WHERE db_type=?''', ('episode',))
            rows = dbcur.fetchall()
            rows = sorted(rows, key = lambda x: (x[0], x[1], x[2]), reverse=True)
            [ep_list.append({"tmdb_id": a, "season": int(b), "episode": int(c), "last_played": d}) for a, b, c, d in rows if not (a in seen or seen.add(a))]
            ep_list = [x for x in ep_list if x['tmdb_id'] not in check_for_next_episode_excludes()]
        ep_list = [i for i in ep_list if not i['tmdb_id'] == None]
        for item in ep_list: threads.append(Thread(process_eps, item, ne_settings, ne_display))
        [i.start() for i in threads]
        [i.join() for i in threads]
        r = [i for i in result if i is not None]
        r = sort_next_eps(r, ne_settings)
        listitems = [i['listitem'] for i in r]
        xbmcplugin.addDirectoryItems(__handle__, listitems, len(listitems))
        xbmcplugin.setContent(__handle__, 'episodes')
        xbmcplugin.endOfDirectory(__handle__)
        setView('view.progress_next_episode')
    except:
        from resources.lib.modules.nav_utils import notification
        notification('Error getting Next Episode Info', time=3500)
        pass

def process_eps(item, ne_settings, ne_display):
    meta = make_fresh_tvshow_meta('tmdb_id', item['tmdb_id'])
    include_unaired = ne_settings['include_unaired']
    try:
        if settings.watched_indicators() in (1, 2):
            resformat = "%Y-%m-%dT%H:%M:%S.%fZ"
            unwatched = item.get('unwatched', False)
            curr_last_played = item.get('last_played', '2000-01-01T00:00:00.000Z')
            season = item['season']
            episode = item['episode']
            season_info = [i for i in meta['season_data'] if i['season_number'] == item['season']][0]
            season = season if episode < season_info['episode_count'] else season_info['season_number'] + 1
            episode = episode + 1 if episode < season_info['episode_count'] else 1
        else:
            resformat = "%Y-%m-%d %H:%M:%S"
            unwatched = item.get('unwatched', False)
            curr_last_played = item.get('last_played', '2000-01-01 00:00:00')
            season_info = [i for i in meta['season_data'] if i['season_number'] == item['season']][0]
            season = item['season'] if item['episode'] < season_info['episode_count'] else season_info['season_number'] + 1
            episode = item['episode'] + 1 if item['episode'] < season_info['episode_count'] else 1
        try: datetime_object = datetime.strptime(curr_last_played, resformat)
        except TypeError: datetime_object = datetime(*(time.strptime(curr_last_played, resformat)[0:6]))
        result.append(build_episode({"season": season, "episode": episode,
            "meta": meta, "curr_last_played_parsed": datetime_object, "action": "next_episode",
            "unwatched": unwatched, "ne_display": ne_display, 'include_unaired': include_unaired}))
    except: pass

def sort_next_eps(result, ne_settings):
    from resources.lib.modules.utils import title_key
    def func(function):
        if ne_settings['sort_key'] == 'name': return title_key(function)
        else: return function
    return sorted(result, key=lambda i:func(i[ne_settings['sort_key']]), reverse=ne_settings['sort_direction'])

def get_unwatched_next_episodes():
    try:
        if settings.watched_indicators() in (1, 2):
            from resources.lib.modules.trakt import call_trakt, get_trakt_tvshow_id
            data = call_trakt("sync/watchlist/shows?extended=full", method='sort_by_headers')
            return [{"tmdb_id": get_trakt_tvshow_id(i), "season": 1, "episode": 0, "unwatched": True} for i in data]
        else:
            settings.check_database(WATCHED_DB)
            dbcon = database.connect(WATCHED_DB)
            dbcur = dbcon.cursor()
            dbcur.execute('''SELECT media_id FROM unwatched_next_episode''')
            unwatched = dbcur.fetchall()
            return [{"tmdb_id": i[0], "season": 1, "episode": 0, "unwatched": True} for i in unwatched]
    except: return []

def add_next_episode_unwatched(action=None, media_id=None, silent=False):
    from urlparse import parse_qsl
    from resources.lib.modules.nav_utils import notification
    from resources.lib.modules.indicators_bookmarks import mark_as_watched_unwatched
    settings.check_database(WATCHED_DB)
    params = dict(parse_qsl(sys.argv[2].replace('?','')))
    media_id = params['tmdb_id'] if not media_id else media_id
    action = params['action'] if not action else action
    if action == 'add': command, line1 = "INSERT OR IGNORE INTO unwatched_next_episode VALUES (?)", '%s Added to Fen Next Episode' % params.get('title')
    else: command, line1 = "DELETE FROM unwatched_next_episode WHERE media_id=?", '%s Removed from Fen Next Episode' % params.get('title')
    dbcon = database.connect(WATCHED_DB)
    dbcon.execute(command, (media_id,))
    dbcon.commit()
    dbcon.close()
    if not silent: notification(line1, time=3500)
    xbmc.sleep(500)
    xbmc.executebuiltin("Container.Refresh")

def add_to_remove_from_next_episode_excludes():
    from urlparse import parse_qsl
    from resources.lib.modules.nav_utils import notification
    settings.check_database(WATCHED_DB)
    params = dict(parse_qsl(sys.argv[2].replace('?','')))
    action = params.get('action')
    media_id = str(params.get('media_id'))
    title = str(params.get('title'))
    dbcon = database.connect(WATCHED_DB)
    if action == 'add':
        dbcon.execute("INSERT INTO exclude_from_next_episode VALUES (?, ?)", (media_id, title))
        line1 = '[B]{}[/B] excluded from Fen Next Episode'.format(title.upper())
    elif action == 'remove':
        dbcon.execute("DELETE FROM exclude_from_next_episode WHERE media_id=?", (media_id,))
        line1 = '[B]{}[/B] included in Fen Next Episode'.format(title.upper())
    dbcon.commit()
    dbcon.close()
    notification('{}'.format(line1), time=5000)
    xbmc.sleep(500)
    xbmc.executebuiltin("Container.Refresh")

def check_for_next_episode_excludes():
    from urlparse import parse_qsl
    from resources.lib.modules.nav_utils import notification
    settings.check_database(WATCHED_DB)
    params = dict(parse_qsl(sys.argv[2].replace('?','')))
    dbcon = database.connect(WATCHED_DB)
    dbcur = dbcon.cursor()
    dbcur.execute('''SELECT media_id FROM exclude_from_next_episode''')
    row = dbcur.fetchall()
    dbcon.close()
    return [str(i[0]) for i in row]

def build_next_episode_manager():
    from urlparse import parse_qsl
    from resources.lib.indexers.tvshows import aired_episode_number_tvshow
    from resources.lib.modules.nav_utils import add_dir
    from resources.lib.modules.indicators_bookmarks import get_watched_status_tvshow
    params = dict(parse_qsl(sys.argv[2].replace('?','')))
    NEXT_EP_UNWATCHED = __addon__.getSetting('nextep.unwatched_colour')
    if not NEXT_EP_UNWATCHED or NEXT_EP_UNWATCHED == '': NEXT_EP_UNWATCHED = 'red'
    VIEW_NEM = __addon__.getSetting('view.main')
    sorted_list = []
    action = params['action']
    if action == 'manage_unwatched':
        tmdb_list = [i['tmdb_id'] for i in get_unwatched_next_episodes()]
        heading = 'Select Show to remove from Fen Next Episode:'
    elif settings.watched_indicators() in (1, 2):
        from resources.lib.modules.trakt import trakt_get_next_episodes
        tmdb_list, exclude_list = trakt_get_next_episodes(include_hidden=True)
        heading = 'Select Show to Hide/Unhide from Trakt Progress:'
    else:
        settings.check_database(WATCHED_DB)
        dbcon = database.connect(WATCHED_DB)
        dbcur = dbcon.cursor()
        dbcur.execute('''SELECT media_id FROM watched_status WHERE db_type=? GROUP BY media_id''', ('episode',))
        rows = dbcur.fetchall()
        tmdb_list = [row[0] for row in rows]
        exclude_list = check_for_next_episode_excludes()
        heading = 'Select Show to Include/Exclude in Fen Next Episode:'
    add_dir({'mode': 'nill'}, '[I][COLOR=grey][B]INFO:[/B][/COLOR] [COLOR=grey2]%s[/COLOR][/I]' % heading, iconImage='settings.png')
    if not tmdb_list:
        from resources.lib.modules.nav_utils import notification
        notification('No Shows Present', time=5000)
    else:
        for tmdb_id in tmdb_list:
            try:
                meta = make_fresh_tvshow_meta('tmdb_id', tmdb_id)
                if action == 'manage_unwatched':
                    action, display = 'remove', '[COLOR=%s][UNWATCHED][/COLOR] %s' % (NEXT_EP_UNWATCHED, meta['title'])
                    url_params = {'mode': 'add_next_episode_unwatched', 'action': 'remove', 'tmdb_id': meta['tmdb_id'], 'title': meta['title']}
                elif settings.watched_indicators() in (1, 2):
                    action, display = 'unhide' if str(meta['tmdb_id']) in exclude_list else 'hide', '[COLOR=red][EXCLUDED][/COLOR] %s' % meta['title'] if str(meta['tmdb_id']) in exclude_list else '[COLOR=green][INCLUDED][/COLOR] %s' % meta['title']
                    url_params = {"mode": "hide_unhide_trakt_items", "action": action, "media_type": "shows", "media_id": meta['imdb_id'], "section": "progress_watched"}
                else:
                    action, display = 'remove' if str(meta['tmdb_id']) in exclude_list else 'add', '[COLOR=red][EXCLUDED][/COLOR] %s' % meta['title'] if str(meta['tmdb_id']) in exclude_list else '[COLOR=green][INCLUDED][/COLOR] %s' % meta['title']
                    url_params = {'mode': 'add_to_remove_from_next_episode_excludes', 'action': action, 'title': meta['title'], 'media_id': meta['tmdb_id']}
                sorted_list.append({'tmdb_id': tmdb_id, 'display': display, 'url_params': url_params, 'meta': json.dumps(meta)})
            except: pass
        sorted_items = sorted(sorted_list, key=lambda k: k['display'])
        for i in sorted_items:
            try:
                cm = []
                meta = json.loads(i['meta'])
                rootname = meta['title'] + " (" + str(meta['year']) + ")"
                meta['rootname'] = rootname
                aired_episodes = aired_episode_number_tvshow(meta)
                playcount, overlay, total_watched, total_unwatched = get_watched_status_tvshow(meta['tmdb_id'], aired_episodes)
                url = build_url(i['url_params'])
                browse_url = build_url({'mode': 'build_season_list', 'meta': i['meta']})
                cm.append(("[B]Browse...[/B]",'XBMC.Container.Update(%s)' % browse_url))
                listitem = xbmcgui.ListItem(i['display'])
                listitem.setProperty('watchedepisodes', str(total_watched))
                listitem.setProperty('unwatchedepisodes', str(total_unwatched))
                listitem.setProperty('totalepisodes', str(aired_episodes))
                listitem.setProperty('totalseasons', str(meta['number_of_seasons']))
                listitem.addContextMenuItems(cm)
                listitem.setArt({'poster': meta['poster'],
                                'fanart': meta['fanart'],
                                'banner': meta['banner'],
                                'clearart': meta['clearart'],
                                'clearlogo': meta['clearlogo'],
                                'landscape': meta['landscape']})
                listitem.setCast(meta['cast'])
                listitem.setInfo(
                    'video', {
                        'title': meta['title'], 'size': '0', 'duration': meta['duration'],
                        'plot': meta['plot'], 'rating': meta['rating'], 'premiered': meta['premiered'],
                        'studio': meta['studio'],'year': meta['year'],
                        'genre': meta['genre'],'imdbnumber': meta['imdb_id'], 'votes': meta['votes'],
                        'playcount': playcount, 'overlay': overlay})
                xbmcplugin.addDirectoryItem(__handle__, url, listitem, isFolder=True)
            except: pass
        xbmcplugin.setContent(__handle__, 'tvshows')
        xbmcplugin.endOfDirectory(__handle__, cacheToDisc=False)
        setView(VIEW_NEM)

def next_episode_color_choice(setting=None):
    from urlparse import parse_qsl
    from resources.lib.modules.utils import color_chooser
    from resources.lib.modules.nav_utils import open_settings
    params = dict(parse_qsl(sys.argv[2].replace('?','')))
    choices = [('Airdate', 'nextep.airdate_colour'),
                ('Unaired', 'nextep.unaired_colour'),
                ('Unwatched', 'nextep.unwatched_colour')]
    prelim_setting = params.get('setting', None) if not setting else setting
    title, setting = [(i[0], i[1]) for i in choices if i[0] == prelim_setting][0]
    dialog = 'Please Choose Color for %s Highlight' % title
    chosen_color = color_chooser(dialog, no_color=True)
    if chosen_color: __addon__.setSetting(setting, chosen_color)
    if params.get('from_settings') == 'true':
        setting_nav = ('2.10') if prelim_setting == 'Airdate' else ('2.11') if prelim_setting == 'Unaired' else ('2.12')
        open_settings(setting_nav)

def next_episode_options_choice(setting=None):
    from urlparse import parse_qsl
    from resources.lib.modules.nav_utils import notification
    from resources.lib.modules.utils import selection_dialog
    params = dict(parse_qsl(sys.argv[2].replace('?','')))
    choices = [('Sort Type', 'nextep.sort_type', [('RECENTLY WATCHED', '0'), ('AIRDATE', '1'), ('TITLE', '2')]),
            ('Sort Order', 'nextep.sort_order', [('DESCENDING', '0'), ('ASCENDING', '1')]),
            ('Include Unaired', 'nextep.include_unaired', [('OFF', 'false'), ('ON', 'true')]),
            ('Include Trakt or Fen Unwatched', 'nextep.include_unwatched', [('OFF', 'false'), ('ON', 'true')]),
            ('Include Airdate in Title', 'nextep.include_airdate', [('OFF', 'false'), ('ON', 'true')]),
            ('Attempt to Make Skin Honor Full Labels', 'nextep.force_display', [('OFF', 'false'), ('ON', 'true')]),
            ('Airdate Format', 'nextep.airdate_format', [('DAY-MONTH-YEAR', '0'), ('YEAR-MONTH-DAY', '1'), ('MONTH-DAY-YEAR', '2')])]
    prelim_setting = params.get('setting') if not setting else setting
    title, setting = [(i[0], i[1]) for i in choices if i[0] == prelim_setting][0]
    string = 'Please Choose Setting for %s' % title
    full_list = [i[2] for i in choices if i[0] == prelim_setting][0]
    dialog_list = [i[0] for i in full_list]
    function_list = [i[1] for i in full_list]
    selection = selection_dialog(dialog_list, function_list, string)
    if not selection: return
    setting_name = [i[0] for i in full_list if i[1] == selection][0]
    __addon__.setSetting(setting, selection)
    notification('%s set to %s' % (title, setting_name), 6000)

def next_episode_context_choice():
    from urlparse import parse_qsl
    from resources.lib.modules.utils import selection_dialog
    from resources.lib.modules.nav_utils import toggle_setting, build_url
    import settings
    params = dict(parse_qsl(sys.argv[2].replace('?','')))
    content_settings = settings.nextep_content_settings()
    display_settings = settings.nextep_display_settings()
    force_display_status = str(display_settings['force_display'])
    toggle_force_display_SETTING = ('nextep.force_display', ('true' if force_display_status == 'False' else 'false'))
    airdate_replacement = [('%d-%m-%Y', 'Day-Month-Year'), ('%Y-%m-%d', 'Year-Month-Day'), ('%m-%d-%Y', 'Month-Day-Year')]
    sort_type_status = ('Recently Watched', 'Airdate', 'Title')[content_settings['sort_type']]
    sort_order_status = ('Descending', 'Ascending')[content_settings['sort_order']]
    toggle_sort_order_SETTING = ('nextep.sort_order', ('0' if sort_order_status == 'Ascending' else '1'))
    unaired_status = str(content_settings['include_unaired'])
    toggle_unaired_SETTING = ('nextep.include_unaired', ('true' if unaired_status == 'False' else 'false'))
    unwatched_status = str(content_settings['include_unwatched'])
    toggle_unwatched_SETTING = ('nextep.include_unwatched', ('true' if unwatched_status == 'False' else 'false'))
    airdate_status = str(display_settings['include_airdate'])
    toggle_airdate_SETTING = ('nextep.include_airdate', ('true' if airdate_status == 'False' else 'false'))
    airdate_format = settings.nextep_airdate_format()
    airdate_format_status = [airdate_format.replace(i[0], i[1]) for i in airdate_replacement if i[0] == airdate_format][0]
    airdate_highlight = display_settings['airdate_colour'].capitalize()
    unaired_highlight = display_settings['unaired_colour'].capitalize()
    unwatched_highlight = display_settings['unwatched_colour'].capitalize()
    choices = [
            ('MANAGE IN PROGRESS SHOWS', 'manage_in_progress'),
            ('SORT TYPE: [I]Currently [B]%s[/B][/I]' % sort_type_status, 'Sort Type'),
            ('SORT ORDER: [I]Currently [B]%s[/B][/I]' % sort_order_status, 'toggle_sort_order'),
            ('INCLUDE UNAIRED EPISODES: [I]Currently [B]%s[/B][/I]' % unaired_status, 'toggle_unaired'),
            ('INCLUDE WATCHLIST/UNWATCHED TV: [I]Currently [B]%s[/B][/I]' % unwatched_status, 'toggle_unwatched'),
            ('INCLUDE AIRDATE: [I]Currently [B]%s[/B][/I]' % airdate_status, 'toggle_airdate'),
            ('ATTEMPT TO MAKE SKIN HONOR FULL LABEL: [I]Currently [B]%s[/B][/I]' % force_display_status, 'toggle_force_display'),
            ('AIRDATE FORMAT: [I]Currently [B]%s[/B][/I]' % airdate_format_status, 'Airdate Format'),
            ('AIRDATE HIGHLIGHT: [I]Currently [B]%s[/B][/I]' % airdate_highlight, 'Airdate'),
            ('UNAIRED HIGHLIGHT: [I]Currently [B]%s[/B][/I]' % unaired_highlight, 'Unaired'),
            ('UNWATCHED HIGHLIGHT: [I]Currently [B]%s[/B][/I]' % unwatched_highlight, 'Unwatched')]
    if settings.watched_indicators() == 0: choices.append(('MANAGE UNWATCHED TV SHOWS', 'manage_unwatched'))
    if settings.watched_indicators() in (1,2): choices.append(('CLEAR TRAKT CACHE', 'clear_cache'))
    string = 'Next Episode Manager'
    dialog_list = [i[0] for i in choices]
    function_list = [i[1] for i in choices]
    choice = selection_dialog(dialog_list, function_list, string)
    if not choice: return
    if choice in ('toggle_sort_order', 'toggle_unaired', 'toggle_unwatched', 'toggle_airdate', 'toggle_force_display'):
        setting = eval(choice + '_SETTING')
        toggle_setting(setting[0], setting[1])
    elif choice == 'clear_cache':
        from resources.lib.modules.nav_utils import clear_cache
        clear_cache('trakt')
    else:
        if choice in ('manage_in_progress', 'manage_unwatched'):
            xbmc.executebuiltin('XBMC.Container.Update(%s)' % build_url({'mode': 'build_next_episode_manager', 'action': choice})); return
        elif choice in ('Airdate','Unaired', 'Unwatched'): function = next_episode_color_choice
        else: function = next_episode_options_choice
        function(choice)
    xbmc.executebuiltin("Container.Refresh")
    xbmc.executebuiltin('RunPlugin(%s)' % build_url({'mode': 'next_episode_context_choice'}))

def nextep_playback_info(tmdb_id, current_season, current_episode, from_library=None):
    from tikimeta import season_episodes_meta
    def build_next_episode_play():
        infoLabels = season_episodes_meta(tmdb_id, season)
        ep_data = infoLabels['episodes']
        ep_data = [i for i in ep_data if int(i['season_number']) == int(season) and int(i['episode_number']) == int(episode)][0]
        query = meta['title'] + ' S%.2dE%.2d' % (int(season), int(episode))
        display_name = '%s - %dx%.2d' % (meta['title'], int(season), int(episode))
        meta.update({'vid_type': 'episode', 'rootname': display_name, "season": season, 'ep_name': ep_data['name'],
                    "episode": episode, 'premiered': ep_data['air_date'], 'plot': ep_data['overview']})
        meta_json = json.dumps(meta)
        url_params = {'mode': 'play_media', 'background': 'true', 'vid_type': 'episode', 'tmdb_id': meta['tmdb_id'],
                    'query': query, 'tvshowtitle': meta['rootname'], 'season': season,
                    'episode': episode, 'meta': meta_json, 'ep_name': ep_data['name']}
        if from_library: url_params.update({'library': 'True', 'plot': ep_data['overview']})
        return build_url(url_params)
    meta = make_fresh_tvshow_meta('tmdb_id',tmdb_id)
    nextep_info = {'pass': True}
    try:
        season_info = [i for i in meta['season_data'] if i['season_number'] == current_season][0]
        season = current_season if current_episode < season_info['episode_count'] else season_info['season_number'] + 1
        episode = current_episode + 1 if current_episode < season_info['episode_count'] else 1
        nextep_info = {'season': season, 'episode': episode, 'url': build_next_episode_play()}
    except: pass
    return nextep_info

def nextep_play(next_ep_info):
    xbmc.executebuiltin("RunPlugin(%s)" % next_ep_info['url'])





