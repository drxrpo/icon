import sys
from urlparse import parse_qsl
# from resources.lib.modules.utils import logger

params = dict(parse_qsl(sys.argv[2].replace('?','')))
mode = params.get('mode')

if not mode or 'navigator.' in mode:
    from resources.lib.indexers.navigator import Navigator
    if not mode or mode == 'navigator.main': Navigator(params.get('action', 'RootList')).main_lists()
    else: exec('Navigator().%s()' % mode.split('.')[1])
elif 'furk.' in mode:
    exec('from resources.lib.indexers.furk import %s as function' % mode.split('.')[1])
    function()
elif 'easynews.' in mode:
    exec('from resources.lib.indexers.easynews import %s as function' % mode.split('.')[1])
    function()
elif 'trakt.' in mode or 'trakt_' in mode:
    if 'trakt.' in mode:
        if mode == 'trakt.add_list_to_menu':
            from resources.lib.indexers.navigator import Navigator
            Navigator().adjust_main_lists()
        elif mode == 'trakt.add_list_to_subscriptions':
            from resources.lib.modules.subscriptions import Subscriptions
            Subscriptions().add_list_to_subscriptions(params.get('user'), params.get('list_slug'))
        else:
            exec('from resources.lib.modules.trakt import %s as function' % mode.split('.')[1])
            function()
    else:
        if mode == 'trakt_sync_watched_to_fen':
            from ast import literal_eval
            from resources.lib.modules.trakt import sync_watched_trakt_to_fen
            sync_watched_trakt_to_fen(literal_eval(params['refresh']))
        elif mode == 'hide_unhide_trakt_items':
            from resources.lib.modules.trakt import hide_unhide_trakt_items
            hide_unhide_trakt_items(params['action'], params['media_type'], params['media_id'], params['section'])
        elif mode == 'trakt_authenticate':
            from resources.lib.modules.trakt import trakt_authenticate
            trakt_authenticate()
        elif mode == 'trakt_remove_authentication':
            from resources.lib.modules.trakt import trakt_remove_authentication
            trakt_remove_authentication()
elif 'build' in mode:
    if mode == 'build_movie_list':
        from resources.lib.indexers.movies import Movies
        Movies(action=params.get('action')).fetch_list()
    elif mode == 'build_tvshow_list':
        from resources.lib.indexers.tvshows import TVShows
        TVShows(action=params.get('action')).fetch_list()
    elif mode == 'build_season_list':
        from resources.lib.indexers.tvshows import build_season_list
        build_season_list()
    elif mode == 'build_episode_list':
        from resources.lib.indexers.tvshows import build_episode_list
        build_episode_list()
    elif mode == 'build_next_episode':
        from resources.lib.modules.next_episode import build_next_episode
        build_next_episode()
    elif mode == 'build_in_progress_episode':
        from resources.lib.modules.in_progress import build_in_progress_episode
        build_in_progress_episode()
    elif mode == 'build_add_to_remove_from_list':
        from resources.lib.modules.utils import build_add_to_remove_from_list
        build_add_to_remove_from_list()
    elif mode == 'build_navigate_to_page':
        from resources.lib.modules.nav_utils import build_navigate_to_page
        build_navigate_to_page()
    elif mode == 'build_next_episode_manager':
        from resources.lib.modules.next_episode import build_next_episode_manager
        build_next_episode_manager()
    elif mode == 'build_kodi_library_recently_added':
        from resources.lib.modules.kodi_library import build_kodi_library_recently_added
        build_kodi_library_recently_added(params['db_type'])
elif '_play' in mode or 'play_' in mode and not 'autoplay' in mode:
    from ast import literal_eval
    if mode in ('play_media'):
        from resources.lib.modules.sources import Sources
        Sources().playback_prep(params.get('vid_type'), params.get('tmdb_id'), params.get('query'),
            params.get('tvshowtitle'), params.get('season'), params.get('episode'), params.get('ep_name'),
            params.get('plot'), params.get('meta'), literal_eval(params.get('library', 'False')), params.get('background'))
    elif mode == 'play_display_results':
        from resources.lib.modules.sources import Sources
        Sources().display_results()
    elif mode == 'play_file':
        from resources.lib.modules.sources import Sources
        Sources().play_file(params['title'], params['source'])
    elif mode == 'play_auto':
        from resources.lib.modules.sources import Sources
        Sources().play_auto()
    elif mode == 'play_auto_nextep':
        from resources.lib.modules.sources import Sources
        Sources().play_auto_nextep()
    elif mode == 'media_play':
        from resources.lib.modules.player import FenPlayer
        FenPlayer().run()
    elif mode == 'play_trailer':
        from resources.lib.modules.nav_utils import play_trailer
        play_trailer(params.get('url'), params.get('all_trailers', []))
elif 'choice' in mode:
    if mode == 'scraper_color_choice':
        from resources.lib.modules.utils import scraper_color_choice
        scraper_color_choice()
    elif mode == 'external_color_choice':
        from resources.lib.modules.utils import external_color_choice
        external_color_choice()
    elif mode == 'next_episode_color_choice':
        from resources.lib.modules.next_episode import next_episode_color_choice
        next_episode_color_choice()
    elif mode == 'next_episode_options_choice':
        from resources.lib.modules.next_episode import next_episode_options_choice
        next_episode_options_choice()
    elif mode == 'next_episode_context_choice':
        from resources.lib.modules.next_episode import next_episode_context_choice
        next_episode_context_choice()
    elif mode == 'unaired_episode_color_choice':
        from resources.lib.modules.utils import unaired_episode_color_choice
        unaired_episode_color_choice()
    elif mode == 'scraper_dialog_color_choice':
        from resources.lib.modules.utils import scraper_dialog_color_choice
        scraper_dialog_color_choice()
    elif mode == 'similar_related_choice':
        from resources.lib.modules.nav_utils import similar_related_choice
        similar_related_choice()
elif 'favourites' in mode:
    if mode == 'my_furk_audio_favourites':
        from resources.lib.indexers.furk import my_furk_audio_favourites
        my_furk_audio_favourites()
    else:
        from resources.lib.modules.favourites import Favourites
        exec('Favourites().%s()' % mode)
elif 'subscriptions' in mode:
    from resources.lib.modules.subscriptions import Subscriptions
    if mode == 'subscriptions_add_remove':
        Subscriptions(params.get('db_type'), params.get('tmdb_id'), params.get('action'), params.get('orig_mode')).add_remove()
    else:
        exec('Subscriptions().%s()' % mode)
elif 'watched_unwatched' in mode:
    if mode == 'mark_as_watched_unwatched':
        from resources.lib.modules.indicators_bookmarks import mark_as_watched_unwatched
        mark_as_watched_unwatched()
    elif mode == 'mark_movie_as_watched_unwatched':
        from resources.lib.modules.indicators_bookmarks import mark_movie_as_watched_unwatched
        mark_movie_as_watched_unwatched()
    elif mode == 'mark_tv_show_as_watched_unwatched':
        from resources.lib.modules.indicators_bookmarks import mark_tv_show_as_watched_unwatched
        mark_tv_show_as_watched_unwatched()
    elif mode == 'mark_season_as_watched_unwatched':
        from resources.lib.modules.indicators_bookmarks import mark_season_as_watched_unwatched
        mark_season_as_watched_unwatched()
    elif mode == 'mark_episode_as_watched_unwatched':
        from resources.lib.modules.indicators_bookmarks import mark_episode_as_watched_unwatched
        mark_episode_as_watched_unwatched()
elif 'toggle' in mode:
    if mode == 'toggle_setting':
        from resources.lib.modules.nav_utils import toggle_setting
        toggle_setting()
    elif mode == 'toggle_jump_to':
        from resources.lib.modules.utils import toggle_jump_to
        toggle_jump_to()
    elif mode == 'toggle_provider':
        from resources.lib.modules.utils import toggle_provider
        toggle_provider()
elif 'history' in mode:
    if mode == 'search_history':
        from resources.lib.modules.history import search_history
        search_history()
    elif mode == 'clear_search_history':
        from resources.lib.modules.history import clear_search_history
        clear_search_history()
    elif mode == 'remove_from_history':
        from resources.lib.modules.history import remove_from_history
        remove_from_history()
##EXTRA MODES##
elif mode == 'container_update':
    from resources.lib.modules.nav_utils import container_update
    container_update()
elif mode == 'open_settings':
    from resources.lib.modules.nav_utils import open_settings
    open_settings(params.get('query'))
elif mode == 'resolveurl_settings':
    try: import resolveurl
    except: pass
    resolveurl.display_settings()
elif mode == 'external_settings':
    from resources.lib.modules.utils import open_ext_settings
    open_ext_settings(params['ext_addon'])
elif mode == 'add_next_episode_unwatched':
    from resources.lib.modules.next_episode import add_next_episode_unwatched
    add_next_episode_unwatched()
elif mode == 'add_to_remove_from_next_episode_excludes':
    from resources.lib.modules.next_episode import add_to_remove_from_next_episode_excludes
    add_to_remove_from_next_episode_excludes()
elif mode == 'set_results_quality':
    from resources.lib.modules.utils import set_results_quality
    set_results_quality()
elif mode == 'set_autoplay_quality':
    from resources.lib.modules.utils import set_autoplay_quality
    set_autoplay_quality()
elif mode == 'playback_menu':
    from resources.lib.modules.utils import playback_menu
    playback_menu()
elif mode == 'playback_kodi_library_menu':
    from resources.lib.modules.utils import playback_kodi_library_menu
    playback_kodi_library_menu()
elif mode == 'refresh_cached_data':
    from resources.lib.modules.nav_utils import refresh_cached_data
    refresh_cached_data()
elif mode == 'clear_cache':
    from resources.lib.modules.nav_utils import clear_cache
    clear_cache(params.get('cache'))
elif mode == 'open_ext_settings':
    from resources.lib.modules.utils import open_ext_settings
    open_ext_settings(params.get("addon"))
elif mode == 'show_text':
    from resources.lib.modules.nav_utils import show_text
    show_text()
elif mode == 'download_file':
    from resources.lib.modules import downloader
    if params.get('db_type') in ('archive', 'furk_file', 'easynews_file'):
        downloader.download(params['name'], params['image'], params['url'])
    else:
        import json
        from resources.lib.modules import sources
        downloader.download(params['name'], params['image'], sources.Sources().resolve_sources(json.loads(params['source'])[0], True))

