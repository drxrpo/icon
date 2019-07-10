
import sys
import xbmc, xbmcaddon

USER_AGENT = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'

__addon_id__ = 'plugin.video.fen'
__addon__ = xbmcaddon.Addon(id=__addon_id__)
__url__ = sys.argv[0]

def pool_converter(items):
    '''takes tuple, converts it to a list, and turns first item into the function
        and following items into the arguments'''
    items = list(items)
    func = items.pop(0)
    return func(*items)

def make_day(date, use_words=True):
    from datetime import datetime, timedelta
    import time
    from resources.lib.modules.settings import adjusted_datetime, nextep_airdate_format
    try: date = datetime.strptime(date, '%Y-%m-%d')
    except TypeError: date = datetime(*(time.strptime(date, '%Y-%m-%d')[0:6]))
    date = date + timedelta(days=1)
    today = adjusted_datetime(dt=True)
    day_diff = (date - today).days
    date_format = nextep_airdate_format()
    fallback_format = '%Y-%m-%d'
    try: day = date.strftime(date_format)
    except ValueError: day = date.strftime(fallback_format)
    if use_words:
        if day_diff == -1:
            day = 'YESTERDAY'
        elif day_diff == 0:
            day = 'TODAY'
        elif day_diff == 1:
            day = 'TOMORROW'
        elif day_diff > 1 and day_diff < 7:
            date = date - timedelta(days=1)
            day = date.strftime('%A').upper()
    return day

def batch_replace(s, replace_info):
    for r in replace_info:
        s = str(s).replace(r[0], r[1])
    return s

def clean_file_name(s, use_encoding=False, use_blanks=True):
    hex_entities = [['&#x26;', '&'], ['&#x27;', '\''], ['&#xC6;', 'AE'], ['&#xC7;', 'C'],
                ['&#xF4;', 'o'], ['&#xE9;', 'e'], ['&#xEB;', 'e'], ['&#xED;', 'i'],
                ['&#xEE;', 'i'], ['&#xA2;', 'c'], ['&#xE2;', 'a'], ['&#xEF;', 'i'],
                ['&#xE1;', 'a'], ['&#xE8;', 'e'], ['%2E', '.'], ['&frac12;', '%BD'],
                ['&#xBD;', '%BD'], ['&#xB3;', '%B3'], ['&#xB0;', '%B0'], ['&amp;', '&'],
                ['&#xB7;', '.'], ['&#xE4;', 'A'], ['\xe2\x80\x99', '']]
    special_encoded = [['"', '%22'], ['*', '%2A'], ['/', '%2F'], [':', ','], ['<', '%3C'],
                        ['>', '%3E'], ['?', '%3F'], ['\\', '%5C'], ['|', '%7C']]
    
    special_blanks = [['"', ' '], ['*', ' '], ['/', ' '], [':', ''], ['<', ' '],
                        ['>', ' '], ['?', ' '], ['\\', ' '], ['|', ' '], ['%BD;', ' '],
                        ['%B3;', ' '], ['%B0;', ' '], ["'", ""], [' - ', ' '], ['.', ' ']]
    s = batch_replace(s, hex_entities)
    if use_encoding:
        s = batch_replace(s, special_encoded)
    if use_blanks:
        s = batch_replace(s, special_blanks)
    s = s.strip()
    return s

def to_bytes(text):
    if isinstance(text, text_type):
        text = text.encode("utf-8")
    return text

def to_utf8(obj):
    import copy
    if isinstance(obj, unicode):
        obj = obj.encode('utf-8', 'ignore')
    elif isinstance(obj, dict):
        obj = copy.deepcopy(obj)
        for key, val in obj.items():
            obj[key] = to_utf8(val)
    elif obj is not None and hasattr(obj, "__iter__"):
        obj = obj.__class__([to_utf8(x) for x in obj])
    else: pass
    return obj

def read_from_file(path, silent=False):
    import xbmcvfs
    try:
        f = xbmcvfs.File(path)
        r = f.read()
        f.close()
        return str(r)
    except:
        if not silent:
            print("Could not read from " + path)
        return None

def regex_from_to(text, from_string, to_string, excluding=True):
    import re
    if excluding:
        r = re.search("(?i)" + from_string + "([\S\s]+?)" + to_string, text).group(1)
    else:
        r = re.search("(?i)(" + from_string + "[\S\s]+?" + to_string + ")", text).group(1)
    return r

def regex_get_all(text, start_with, end_with):
    import re
    r = re.findall("(?i)(" + start_with + "[\S\s]+?" + end_with + ")", text)
    return r

def remove_all(elements, list):
    return filter(lambda x: x not in elements, list)

def get_url(url, params=None, referer=None, cookie_jar=None, cache=None, cache_time=3600):
    import urllib2
    req = urllib2.Request(url)
    req.add_header('User-Agent', USER_AGENT)
    if referer:
        req.add_header('Referer', referer)
    if 'akas.imdb' in url:
        req.add_header('Accept-Language', 'en')
    if cookie_jar:
        cj = cookielib.LWPCookieJar()
        try:
            cj.load(cookie_jar, ignore_discard=True)
        except:
            print "Could not load cookie jar file."
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        response = opener.open(req)
        cj.save(cookie_jar, ignore_discard=True)
    else:
        response = urllib2.urlopen(req)
    body = response.read()
    response.close()
    if cache:
        write_to_file(cache_file, body)
    return body

def replace_html_codes(txt):
    import HTMLParser
    import re
    txt = to_utf8(txt)
    txt = re.sub("(&#[0-9]+)([^;^0-9]+)", "\\1;\\2", txt)
    txt = HTMLParser.HTMLParser().unescape(txt)
    txt = txt.replace("&quot;", "\"")
    txt = txt.replace("&amp;", "&")
    return txt

def logger(heading, function):
    xbmc.log('###%s###: %s' % (heading, function), 2)

def int_with_commas(number):
    '''helper to pretty format a number'''
    try:
        number = int(number)
        if number < 0:
            return '-' + int_with_commas(-number)
        result = ''
        while number >= 1000:
            number, number2 = divmod(number, 1000)
            result = ",%03d%s" % (number2, result)
        return "%d%s" % (number, result)
    except Exception:
        return ""

def try_parse_int(string):
    '''helper to parse int from string without erroring on empty or misformed string'''
    try:
        return int(string)
    except Exception:
        return 0

def writeDict(dict, filename, sep):
    with open(filename, "a") as f:
        for i in dict.keys():            
            f.write(i + " " + sep.join([str(x) for x in dict[i]]) + "\n")

def readDict(filename, sep):
    with open(filename, "r") as f:
        dict = {}
        for line in f:
            values = line.split(sep)
            dict[values[0]] = {int(x) for x in values[1:len(values)]}
        return(dict)

def sec2time(sec, n_msec=3):
    ''' Convert seconds to 'D days, HH:MM:SS.FFF' '''
    if hasattr(sec,'__len__'):
        return [sec2time(s) for s in sec]
    m, s = divmod(sec, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)
    if n_msec > 0:
        pattern = '%%02d:%%02d:%%0%d.%df' % (n_msec+3, n_msec)
    else:
        pattern = r'%02d:%02d:%02d'
    if d == 0:
        return pattern % (h, m, s)
    return ('%d days, ' + pattern) % (d, h, m, s)
    
def sort_list(sort_key, sort_direction, list_data):
    reverse = False if sort_direction == 'asc' else True
    if sort_key == 'rank':
        return sorted(list_data, key=lambda x: x['rank'], reverse=reverse)
    elif sort_key == 'added':
        return sorted(list_data, key=lambda x: x['listed_at'], reverse=reverse)
    elif sort_key == 'title':
        return sorted(list_data, key=lambda x: title_key(x[x['type']].get('title')), reverse=reverse)
    elif sort_key == 'released':
        return sorted(list_data, key=lambda x: released_key(x[x['type']]), reverse=reverse)
    elif sort_key == 'runtime':
        return sorted(list_data, key=lambda x: x[x['type']].get('runtime', 0), reverse=reverse)
    elif sort_key == 'popularity':
        return sorted(list_data, key=lambda x: x[x['type']].get('votes', 0), reverse=reverse)
    elif sort_key == 'percentage':
        return sorted(list_data, key=lambda x: x[x['type']].get('rating', 0), reverse=reverse)
    elif sort_key == 'votes':
        return sorted(list_data, key=lambda x: x[x['type']].get('votes', 0), reverse=reverse)
    elif sort_key == 'random':
        import random
        return sorted(list_data, key=lambda k: random.random())
    else:
        return list_data

def released_key(item):
    if 'released' in item:
        return item['released']
    elif 'first_aired' in item:
        return item['first_aired']
    else:
        return 0

def title_key(title):
    import re
    try:
        if title is None: title = ''
        articles = ['the', 'a', 'an']
        match = re.match('^((\w+)\s+)', title.lower())
        if match and match.group(2) in articles: offset = len(match.group(1))
        else: offset = 0

        return title[offset:]
    except: return title

def selection_dialog(dialog_list, function_list, string):
    import xbmcgui
    dialog = xbmcgui.Dialog()
    list_choose = dialog.select("%s" % string, dialog_list)
    if list_choose >= 0:
        return function_list[list_choose]
    else:
        return

def multiselect_dialog(string, dialog_list, function_list=None, preselect= []):
    import xbmcgui
    dialog = xbmcgui.Dialog()
    if not function_list: function_list = dialog_list
    list_choose = dialog.multiselect(string, dialog_list, preselect=preselect)
    if list_choose >= 0:
        return [function_list[i] for i in list_choose]
    else:
        return

def set_results_quality(from_results=False, action=False):
    from urlparse import parse_qsl
    params = dict(parse_qsl(sys.argv[2].replace('?','')))
    from_results = True if 'from_results' in params else False
    action = params.get('action', action)
    open_setting = ('4.4')
    string = 'Please Choose Result Filters:'
    dl = ['Include SD', 'Include 720p', 'Include 1080p', 'Include 4K']
    fl = ['SD', '720p', '1080p', '4K']
    preselect = [fl.index(i) for i in __addon__.getSetting('results_quality').split(', ')]
    filters = multiselect_dialog(string, dl, fl, preselect)
    if not filters: return
    from resources.lib.modules.nav_utils import toggle_setting
    toggle_setting('results_quality', ', '.join(filters))
    if from_results == True:
        xbmc.executebuiltin('Container.Refresh')
    if not action:
        from resources.lib.modules.nav_utils import open_settings
        open_settings(open_setting)
    else: pass

def set_autoplay_quality(action=False, source='autoplay_quality'):
    from urlparse import parse_qsl
    params = dict(parse_qsl(sys.argv[2].replace('?','')))
    action = params.get('action', action)
    open_setting = ('4.2')
    string = 'Please Choose Autoplay Filters'
    dl = ['Include SD', 'Include 720p', 'Include 1080p', 'Include 4K']
    fl = ['SD', '720p', '1080p', '4K']
    preselect = [fl.index(i) for i in __addon__.getSetting('autoplay_quality').split(', ')]
    filters = multiselect_dialog(string, dl, fl, preselect)
    if not filters: return
    from resources.lib.modules.nav_utils import toggle_setting
    toggle_setting('autoplay_quality', ', '.join(filters))
    if not action:
        from resources.lib.modules.nav_utils import open_settings
        open_settings(open_setting)

def open_ext_settings(addon):
    xbmc.sleep(500)
    xbmcaddon.Addon(id=addon).openSettings()

def enable_scrapers():
    from settings import active_scrapers
    from resources.lib.modules.nav_utils import toggle_setting
    scrapers = ['local', 'downloads', 'furk', 'easynews', 'external']
    preselect = [scrapers.index(i) for i in active_scrapers()]
    scrapers_dialog = [i.capitalize() for i in scrapers]
    scraper_choice = multiselect_dialog('Choose Fen Scrapers', scrapers_dialog, scrapers , preselect=preselect)
    if scraper_choice < 0: return
    return [toggle_setting('provider.%s' % i, ('true' if i in scraper_choice else 'false')) for i in scrapers]

def unaired_episode_color_choice():
    from resources.lib.modules.nav_utils import open_settings, toggle_setting
    dialog = 'Please Choose Color for Unaired Episodes'
    chosen_color = color_chooser(dialog, no_color=True)
    if chosen_color: toggle_setting('unaired_episode_colour', chosen_color)
    open_settings('0.4')

def scraper_dialog_color_choice():
    from urlparse import parse_qsl
    from resources.lib.modules.nav_utils import open_settings, toggle_setting
    params = dict(parse_qsl(sys.argv[2].replace('?','')))
    setting, setting_nav = ('int_dialog_highlight', '3.6') if params['setting'] == 'internal' else ('ext_dialog_highlight', '3.7')
    dialog = 'Please Choose Color for Internal Scrapers Progress Dialog Highlight'
    chosen_color = color_chooser(dialog)
    if chosen_color: toggle_setting(setting, chosen_color)
    open_settings(setting_nav)

def toggle_jump_to():
    from resources.lib.modules.nav_utils import toggle_setting, notification
    from resources.lib.modules.settings import nav_jump_use_alphabet
    use_alphabet = nav_jump_use_alphabet()
    (setting, new_action) = ('0', 'PAGE') if use_alphabet == True else ('1', 'ALPHABET')
    toggle_setting(setting_id='nav_jump', setting_value=setting, refresh=True)
    notification('Jump To Action Switched to [B]%s[/B]' % new_action)

def scraper_color_choice():
    from urlparse import parse_qsl
    from resources.lib.modules.nav_utils import open_settings, toggle_setting
    params = dict(parse_qsl(sys.argv[2].replace('?','')))
    choices = [('local', 'provider.local_colour'),
                ('downloads', 'provider.downloads_colour'),
                ('furk', 'provider.furk_colour'),
                ('easynews', 'provider.easynews_colour'),
                ('premium', 'prem.identify'),
                ('torrent', 'torrent.identify')]
    title, setting = [(i[0], i[1]) for i in choices if i[0] == params.get('setting')][0]
    setting_nav = ('3.15') if setting == 'provider.furk_colour' else ('3.21') if setting == 'provider.easynews_colour' else \
                  ('3.28') if setting == 'provider.local_colour' else ('3.35') if setting == 'provider.downloads_colour' else \
                  ('3.51') if setting == 'prem.identify' else ('3.52')
    dialog = 'Please Choose Color for %s Results Highlight' % title.capitalize()
    chosen_color = color_chooser(dialog, no_color=True)
    if chosen_color: toggle_setting(setting, chosen_color)
    open_settings(setting_nav)

def build_add_to_remove_from_list(meta='', media_type='', orig_mode='', from_search=''):
    from urlparse import parse_qsl
    import json
    from resources.lib.modules.nav_utils import build_url
    from resources.lib.modules.settings import watched_indicators
    params = dict(parse_qsl(sys.argv[2].replace('?','')))
    media_type = params.get('media_type', '')
    orig_mode = params.get('orig_mode', '')
    from_search = params.get('from_search', '')
    meta = json.loads(params.get('meta', None))
    main_listing = [('Add to...', 'add'), ('Remove from...', 'remove')]
    mlc = selection_dialog([i[0] for i in main_listing], [i[1] for i in main_listing], 'Choose Add to or Remove from...')
    if mlc == None: return
    string = "Choose Selection to Add Item To" if mlc == 'add' else "Choose Selection to Remove Item From"
    heading = 'Add to ' if mlc == 'add' else 'Remove from '
    listing = [(heading + 'Trakt List', 'trakt'), (heading + 'Fen Favourites', 'favourites'), (heading + 'Fen Subscriptions', 'subscriptions')]
    if media_type == 'tvshow' and watched_indicators() == 0: listing.append((heading + 'Fen Next Episode', 'unwatched_next_episode'))
    if mlc == 'remove': listing.append((heading + 'Cache (Re-cache %s Info)' % ('Movie' if media_type == 'movie' else 'TV Show'), 'refresh'))
    if mlc == 'remove' and watched_indicators() == 1: listing.append(('Remove Fen/Trakt Watched Sync (ReSync Watched Info)', 'resync'))
    choice = selection_dialog([i[0] for i in listing], [i[1] for i in listing], string)
    if choice == None: return
    elif choice == 'trakt': url = {'mode': ('trakt.trakt_add_to_list' if mlc == 'add' else 'trakt.trakt_remove_from_list'), 'tmdb_id': meta["tmdb_id"], 'imdb_id': meta["imdb_id"], 'db_type': media_type}
    elif choice == 'favourites': url = {'mode': ('add_to_favourites' if mlc == 'add' else 'remove_from_favourites'), 'db_type': media_type, 'tmdb_id': meta["tmdb_id"], 'title': meta['title']}
    elif choice == 'subscriptions': url = {'mode': 'subscriptions_add_remove', 'action': mlc, 'db_type': media_type, 'tmdb_id': meta["tmdb_id"], 'orig_mode': orig_mode}
    elif choice == 'unwatched_next_episode': url = {'mode': 'add_next_episode_unwatched', 'action': mlc, 'title': meta["title"], 'tmdb_id': meta["tmdb_id"], 'imdb_id': meta["imdb_id"]}
    elif choice == 'refresh': url = {'mode': 'refresh_cached_data', 'db_type': media_type, 'id_type': 'tmdb_id', 'media_id': meta['tmdb_id']}
    elif choice == 'resync': url = {'mode': 'trakt_sync_watched_to_fen', 'refresh': True}
    xbmc.executebuiltin('XBMC.RunPlugin(%s)' % build_url(url))

def playback_menu(from_results=False, suggestion=None):
    from urlparse import parse_qsl
    from resources.lib.modules.nav_utils import toggle_setting, build_url, open_settings, clear_cache
    from resources.lib.modules import settings
    content = xbmc.getInfoLabel('Container.Content')
    params = dict(parse_qsl(sys.argv[2].replace('?','')))
    from_results = params.get('from_results', from_results)
    suggestion = params.get('suggestion', suggestion)
    autoplay_status, autoplay_toggle, filter_setting = ('On', 'false', 'autoplay_quality') if settings.auto_play() else ('Off', 'true', 'results_quality')
    autoplay_next_status, autoplay_next_toggle = ('On', 'false') if settings.autoplay_next_episode() else ('Off', 'true')
    results_display_status, results_display_toggle = ('Dialog', '0') if settings.use_dialog() else ('Directory', '1')
    prefer_hevc_status, prefer_hevc_toggle = ('On', 'false') if settings.prefer_hevc() else ('Off', 'true')
    auto_resolve_status, auto_resolve_toggle = ('On', 'false') if settings.auto_resolve() else ('Off', 'true')
    active_scrapers = settings.active_scrapers()
    current_scrapers_status = ', '.join([i.capitalize() for i in active_scrapers]) if len(active_scrapers) >= 1 else 'None Active'
    current_filter_status =  ', '.join(settings.quality_filter(filter_setting))
    indicators_status, indicators_toggle = ('Trakt', '0') if settings.watched_indicators() in (1, 2) else ('Fen', '1')
    string = 'Please choose Fen Setting to Change...'
    listing = [('AUTOPLAY: [I]Currently [B]%s[/B][/I]' % autoplay_status, 'toggle_autoplay')]
    if autoplay_status == 'On':
        listing += [('PREFER HEVC IN AUTOPLAY: [I]Currently [B]%s[/B][/I]' % prefer_hevc_status, 'toggle_prefer_hevc')]
        listing += [('AUTOPLAY NEXT EPISODE: [I]Currently [B]%s[/B][/I]' % autoplay_next_status, 'toggle_autoplay_next')]
    listing += [('ENABLE SCRAPERS: [I]Currently [B]%s[/B][/I]' % current_scrapers_status, 'enable_scrapers')]
    if autoplay_status == 'Off':
        listing += [('DISPLAY RESULTS: [I]Currently [B]%s[/B][/I]' % results_display_status, 'toggle_display_results')]
        listing += [('AUTO RESOLVE FURK PACKS: [I]Currently [B]%s[/B][/I]' % auto_resolve_status, 'toggle_auto_resolve')]
    listing += [('QUALITY FILTERS: [I]Currently [B]%s[/B][/I]' % current_filter_status, 'set_filters')]
    listing += [('SWITCH INDICATOR PROVIDER: [I]Currently [B]%s[/B][/I]' % indicators_status, 'toggle_indicators')]
    if settings.watched_indicators() in (1,2): listing += [('CLEAR TRAKT CACHE', 'clear_trakt_cache')]
    if content in ('movies', 'episodes'): listing += [('FURK/EASYNEWS SEARCH: [B][I]%s[/I][/B]' % params.get('suggestion', ''), 'search_directly')]
    listing += [('OPEN EXTERNAL SCRAPER SETTINGS', 'open_scraper_settings')]
    listing += [('OPEN FEN SETTINGS', 'open_fen_settings')]
    listing += [('[B]SAVE SETTINGS AND EXIT[/B]', 'save_and_exit')]
    xbmc.sleep(500)
    choice = selection_dialog([i[0] for i in listing], [i[1] for i in listing], string)
    if choice == 'toggle_autoplay': toggle_setting('auto_play', autoplay_toggle)
    elif choice == 'toggle_prefer_hevc': toggle_setting('prefer_hevc', prefer_hevc_toggle)
    elif choice == 'toggle_autoplay_next': toggle_setting('autoplay_next_episode', autoplay_next_toggle)
    elif choice == 'enable_scrapers': enable_scrapers()
    elif choice == 'toggle_display_results': toggle_setting('use_dialog', results_display_toggle)
    elif choice == 'toggle_auto_resolve': toggle_setting('auto_resolve', auto_resolve_toggle)
    elif choice == 'set_filters': set_autoplay_quality(action=True) if autoplay_status == 'On' else set_results_quality(action=True)
    elif choice == 'toggle_indicators': toggle_setting('watched_indicators', indicators_toggle)
    elif choice == 'clear_trakt_cache': clear_cache('trakt')
    elif choice == 'search_directly': furk_easynews_direct_search_choice(suggestion, from_results)
    elif choice == 'open_scraper_settings': xbmc.executebuiltin('Addon.OpenSettings(%s)' % 'script.module.tikiscrapers')
    elif choice == 'open_fen_settings': open_settings('0.0')
    if choice in ('toggle_indicators', 'clear_trakt_cache') and content in ('movies', 'tvshows', 'seasons', 'episodes'): xbmc.executebuiltin('Container.Refresh')
    if choice in (None, 'save_and_exit', 'toggle_indicators', 'clear_trakt_cache', 'search_directly', 'open_scraper_settings', 'open_fen_settings'): return
    xbmc.executebuiltin('RunPlugin(%s)' % build_url({'mode': 'playback_menu', 'from_results': from_results, 'suggestion': suggestion}))

def furk_easynews_direct_search_choice(suggestion, from_results):
    from resources.lib.modules.nav_utils import build_url
    direct_search_furk_params = {'mode': 'furk.search_furk', 'db_type': 'video', 'suggestion': suggestion}
    direct_search_easynews_params = {'mode': 'easynews.search_easynews', 'suggestion': suggestion}
    choices = [('SEARCH FURK', direct_search_furk_params), ('SEARCH EASYNEWS', direct_search_easynews_params)]
    choice = selection_dialog([i[0] for i in choices], [i[1] for i in choices], 'Choose Direct Search Provider')
    if not choice: xbmc.executebuiltin('RunPlugin(%s)' % build_url({'mode': 'playback_menu', 'from_results': from_results, 'suggestion': suggestion}))
    else: xbmc.executebuiltin('XBMC.Container.Update(%s)' % build_url(choice))

def color_chooser(msg_dialog, no_color=False):
    color_chart = [
          'black', 'white', 'whitesmoke', 'gainsboro', 'lightgray', 'silver', 'darkgray', 'gray', 'dimgray',
          'snow', 'floralwhite', 'ivory', 'beige', 'cornsilk', 'antiquewhite', 'bisque', 'blanchedalmond',
          'burlywood', 'darkgoldenrod', 'ghostwhite', 'azure', 'lightsaltegray', 'lightsteelblue',
          'powderblue', 'lightblue', 'skyblue', 'lightskyblue', 'deepskyblue', 'dodgerblue', 'royalblue',
          'blue', 'mediumblue', 'midnightblue', 'navy', 'darkblue', 'cornflowerblue', 'slateblue', 'slategray',
          'yellowgreen', 'springgreen', 'seagreen', 'steelblue', 'teal', 'fuchsia', 'deeppink', 'darkmagenta',
          'blueviolet', 'darkviolet', 'darkorchid', 'darkslateblue', 'darkslategray', 'indigo', 'cadetblue',
          'darkcyan', 'darkturquoise', 'turquoise', 'cyan', 'paleturquoise', 'lightcyan', 'mintcream', 'honeydew',
          'aqua', 'aquamarine', 'chartreuse', 'greenyellow', 'palegreen', 'lawngreen', 'lightgreen', 'lime',
          'mediumspringgreen', 'mediumturquoise', 'lightseagreen', 'mediumaquamarine', 'mediumseagreen',
          'limegreen', 'darkseagreen', 'forestgreen', 'green', 'darkgreen', 'darkolivegreen', 'olive', 'olivedab',
          'darkkhaki', 'khaki', 'gold', 'goldenrod', 'lightyellow', 'lightgoldenrodyellow', 'lemonchiffon',
          'yellow', 'seashell', 'lavenderblush', 'lavender', 'lightcoral', 'indianred', 'darksalmon',
          'lightsalmon', 'pink', 'lightpink', 'hotpink', 'magenta', 'plum', 'violet', 'orchid', 'palevioletred',
          'mediumvioletred', 'purple', 'marron', 'mediumorchid', 'mediumpurple', 'mediumslateblue', 'thistle',
          'linen', 'mistyrose', 'palegoldenrod', 'oldlace', 'papayawhip', 'moccasin', 'navajowhite', 'peachpuff',
          'sandybrown', 'peru', 'chocolate', 'orange', 'darkorange', 'tomato', 'orangered', 'red', 'crimson',
          'salmon', 'coral', 'firebrick', 'brown', 'darkred', 'tan', 'rosybrown', 'sienna', 'saddlebrown'
          ]
    color_display = ['[COLOR=%s]%s[/COLOR]' % (i, i.capitalize()) for i in color_chart]
    if no_color:
        color_chart.insert(0, 'No Color')
        color_display.insert(0, 'No Color')
    choice = selection_dialog(color_display, color_chart, msg_dialog)
    if not choice: return
    return choice

