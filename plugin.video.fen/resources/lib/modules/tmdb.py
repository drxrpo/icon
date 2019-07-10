# -*- coding: utf-8 -*-
import xbmcaddon
import requests, time
from resources.lib.modules.nav_utils import cache_object
from resources.lib.modules.settings import tmdb_api
# from resources.lib.modules.utils import logger

tmdb_api = tmdb_api()

def tmdb_movies_popular(page_no):
    string = "%s_%s" % ('tmdb_movies_popular', page_no)
    url = 'https://api.themoviedb.org/3/movie/popular?api_key=%s&language=en-US&page=%s' % (tmdb_api, page_no)
    return cache_object(get_tmdb, string, url)

def tmdb_movies_blockbusters(page_no):
    string = "%s_%s" % ('tmdb_movies_blockbusters', page_no)
    url = 'https://api.themoviedb.org/3/discover/movie?api_key=%s&language=en-US&sort_by=revenue.desc&page=%s' % (tmdb_api, page_no)
    return cache_object(get_tmdb, string, url)

def tmdb_movies_in_theaters(page_no):
    string = "%s_%s" % ('tmdb_movies_in_theaters', page_no)
    url = 'https://api.themoviedb.org/3/movie/now_playing?api_key=%s&language=en-US&page=%s' % (tmdb_api, page_no)
    return cache_object(get_tmdb, string, url)

def tmdb_movies_premieres(page_no):
    current_date, previous_date = get_dates(31, reverse=True)
    string = "%s_%s" % ('tmdb_movies_premieres', page_no)
    url = 'https://api.themoviedb.org/3/discover/movie?api_key=%s&language=en-US&region=US&release_date.gte=%s&release_date.lte=%s&with_release_type=1|2|3&page=%s' % (tmdb_api, previous_date, current_date, page_no)
    return cache_object(get_tmdb, string, url)

def tmdb_movies_latest_releases(page_no):
    current_date, previous_date = get_dates(31, reverse=True)
    string = "%s_%s" % ('tmdb_movies_latest_releases', page_no)
    url = 'https://api.themoviedb.org/3/discover/movie?api_key=%s&language=en-US&region=US&release_date.gte=%s&release_date.lte=%s&with_release_type=4|5&page=%s' % (tmdb_api, previous_date, current_date, page_no)
    return cache_object(get_tmdb, string, url)

def tmdb_movies_top_rated(page_no):
    string = "%s_%s" % ('tmdb_movies_top_rated', page_no)
    url = 'https://api.themoviedb.org/3/movie/top_rated?api_key=%s&language=en-US&page=%s' % (tmdb_api, page_no)
    return cache_object(get_tmdb, string, url)

def tmdb_movies_upcoming(page_no):
    current_date, future_date = get_dates(31, reverse=False)
    string = "%s_%s" % ('tmdb_movies_upcoming', page_no)
    url = 'https://api.themoviedb.org/3/discover/movie?api_key=%s&language=en-US&region=US&release_date.gte=%s&release_date.lte=%s&with_release_type=3|2|1&page=%s' % (tmdb_api, current_date, future_date, page_no)
    return cache_object(get_tmdb, string, url)

def tmdb_movies_genres(genre_id, page_no):
    string = "%s_%s_%s" % ('tmdb_movies_genres', genre_id, page_no)
    url = 'https://api.themoviedb.org/3/discover/movie?api_key=%s&with_genres=%s&sort_by=popularity.desc&page=%s' % (tmdb_api, genre_id, page_no)
    return cache_object(get_tmdb, string, url)

def tmdb_movies_languages(language, page_no):
    string = "%s_%s_%s" % ('tmdb_movies_languages', language, page_no)
    url = 'https://api.themoviedb.org/3/discover/movie?api_key=%s&language=en-US&sort_by=popularity.desc&with_original_language=%s&page=%s' % (tmdb_api, language, page_no)
    return cache_object(get_tmdb, string, url)

def tmdb_movies_certifications(certification, page_no):
    string = "%s_%s_%s" % ('tmdb_movies_certifications', certification, page_no)
    url = 'https://api.themoviedb.org/3/discover/movie?api_key=%s&language=en-US&sort_by=popularity.desc&certification_country=US&certification=%s&page=%s' % (tmdb_api, certification, page_no)
    return cache_object(get_tmdb, string, url)

def tmdb_movies_year(year, page_no):
    string = "%s_%s_%s" % ('tmdb_movies_year', year, page_no)
    url = 'https://api.themoviedb.org/3/discover/movie?api_key=%s&language=en-US&sort_by=popularity.desc&certification_country=US&primary_release_year=%s&page=%s' % (tmdb_api, year, page_no)
    return cache_object(get_tmdb, string, url)

def tmdb_popular_people(page_no):
    string = "%s_%s" % ('popular_people', page_no)
    url = 'https://api.themoviedb.org/3/person/popular?api_key=%s&language=en-US&page=%s' % (tmdb_api, page_no)
    return cache_object(get_tmdb, string, url)

def tmdb_movies_similar(tmdb_id, page_no):
    string = "%s_%s_%s" % ('tmdb_movies_similar', tmdb_id, page_no)
    url = 'https://api.themoviedb.org/3/movie/%s/similar?api_key=%s&language=en-US&page=%s' % (tmdb_id, tmdb_api, page_no)
    return cache_object(get_tmdb, string, url)

def tmdb_movies_actor_roles(actor_id, page_no, letter, passed_list=[]):
    import ast
    from resources.lib.modules.nav_utils import paginate_list
    from resources.lib.modules.utils import title_key
    limit = 40
    if not passed_list:
        string = "%s_%s" % ('tmdb_movies_people_search_movie_credits', actor_id)
        url = 'https://api.themoviedb.org/3/person/%s/movie_credits?api_key=%s&language=en-US' % (int(actor_id), tmdb_api)
        data = cache_object(get_tmdb, string, url, 4)['cast']
        data = sorted(data, key=lambda k: title_key(k['title']))
        original_list = [{'media_id': i['id'], 'title': i['title']} for i in data]
    else: original_list = ast.literal_eval(passed_list)
    if page_no == 'None':
        return original_list
    paginated_list, total_pages = paginate_list(original_list, page_no, letter, limit)
    return paginated_list, original_list, total_pages, limit

def tmdb_movies_search(term, page_no):
    from resources.lib.modules.history import add_to_search_history
    add_to_search_history(term, 'movie_queries')
    string = "%s_%s_%s" % ('tmdb_movies_search', term, page_no)
    url = 'https://api.themoviedb.org/3/search/movie?api_key=%s&language=en-US&query=%s&page=%s' % (tmdb_api, term, page_no)
    return cache_object(get_tmdb, string, url, 4)

def tmdb_movies_people_search(term, page_no, letter, passed_list=[], actor_id=None):
    import xbmcgui
    import ast
    from resources.lib.modules.nav_utils import paginate_list
    limit = 40
    if not passed_list:
        dialog = xbmcgui.Dialog()
        string = "%s_%s" % ('tmdb_movies_people_search_actor_data', term)
        url = 'https://api.themoviedb.org/3/search/person?api_key=%s&language=en-US&query=%s&page=%s' % (tmdb_api, term, page_no)
        result1 = cache_object(get_tmdb, string, url, 4)
        info = result1['results']
        actor_list = []
        if len(info) > 1:
            for item in info:
                try: known_for_list = [i['title'] for i in item['known_for']]
                except: known_for_list = None
                known_for = '[I]%s[/I]' % ', '.join(known_for_list) if known_for_list else '[I]Movie Actor[/I]'
                listitem = xbmcgui.ListItem(item['name'], known_for, iconImage='http://image.tmdb.org/t/p/w300/%s' % item['profile_path'])
                listitem.setProperty('id', str(item['id']))
                actor_list.append(listitem)
            selection = dialog.select("Select Person", actor_list, useDetails=True)
            if selection >= 0: actor_id = int(actor_list[selection].getProperty('id'))
            else: return
        else: actor_id = [item['id'] for item in info][0]
        original_list = tmdb_movies_actor_roles(actor_id, 'None', letter, passed_list)
    else: original_list = ast.literal_eval(passed_list)
    paginated_list, total_pages = paginate_list(original_list, page_no, letter, limit)
    return paginated_list, original_list, total_pages, limit

def tmdb_tv_popular(page_no):
    string = "%s_%s" % ('tmdb_tv_popular', page_no)
    url = 'https://api.themoviedb.org/3/tv/popular?api_key=%s&language=en-US&page=%s' % (tmdb_api, page_no)
    return cache_object(get_tmdb, string, url)

def tmdb_tv_premieres(page_no):
    current_date, previous_date = get_dates(31, reverse=True)
    string = "%s_%s" % ('tmdb_tv_premieres', page_no)
    url = 'https://api.themoviedb.org/3/discover/tv?api_key=%s&language=en-US&sort_by=popularity.desc&first_air_date.gte=%s&first_air_date.lte=%s&page=%s' % (tmdb_api, previous_date, current_date, page_no)
    return cache_object(get_tmdb, string, url)

def tmdb_tv_upcoming(page_no):
    current_date, future_date = get_dates(31, reverse=False)
    string = "%s_%s" % ('tmdb_tv_upcoming', page_no)
    url = 'https://api.themoviedb.org/3/discover/tv?api_key=%s&language=en-US&sort_by=popularity.desc&first_air_date.gte=%s&first_air_date.lte=%s&include_null_first_air_dates=true&page=%s' % (tmdb_api, current_date, future_date, page_no)
    return cache_object(get_tmdb, string, url)

def tmdb_tv_top_rated(page_no):
    string = "%s_%s" % ('tmdb_tv_top_rated', page_no)
    url = 'https://api.themoviedb.org/3/tv/top_rated?api_key=%s&language=en-US&page=%s' % (tmdb_api, page_no)
    return cache_object(get_tmdb, string, url)

def tmdb_tv_airing_today(page_no):
    import json
    from resources.lib.modules.utils import to_utf8
    string = "%s_%s" % ('tmdb_tv_airing_today', page_no)
    url = 'https://api.themoviedb.org/3/tv/airing_today?api_key=%s&timezone=America/Edmonton&language=en-US&page=%s' % (tmdb_api, page_no)
    return cache_object(get_tmdb, string, url, expiration=24)

def tmdb_tv_on_the_air(page_no):
    string = "%s_%s" % ('tmdb_tv_on_the_air', page_no)
    url = 'https://api.themoviedb.org/3/tv/on_the_air?api_key=%s&language=en-US&page=%s' % (tmdb_api, page_no)
    return cache_object(get_tmdb, string, url)

def tmdb_tv_genres(genre_id, page_no):
    string = "%s_%s_%s" % ('tmdb_tv_genres', genre_id, page_no)
    url = 'https://api.themoviedb.org/3/discover/tv?api_key=%s&with_genres=%s&sort_by=popularity.desc&include_null_first_air_dates=false&page=%s' % (tmdb_api, genre_id, page_no)
    return cache_object(get_tmdb, string, url)

def tmdb_tv_languages(language, page_no):
    string = "%s_%s_%s" % ('tmdb_tv_languages', language, page_no)
    url = 'https://api.themoviedb.org/3/discover/tv?api_key=%s&language=en-US&sort_by=popularity.desc&include_null_first_air_dates=false&with_original_language=%s&page=%s' % (tmdb_api, language, page_no)
    return cache_object(get_tmdb, string, url)

def tmdb_tv_year(year, page_no):
    string = "%s_%s_%s" % ('tmdb_tv_year', year, page_no)
    url = 'https://api.themoviedb.org/3/discover/tv?api_key=%s&language=en-US&sort_by=popularity.desc&include_null_first_air_dates=false&first_air_date_year=%s&page=%s' % (tmdb_api, year, page_no)
    return cache_object(get_tmdb, string, url)

def tmdb_tv_networks(network_id, page_no):
    string = "%s_%s_%s" % ('tmdb_tv_networks', network_id, page_no)
    url = 'https://api.themoviedb.org/3/discover/tv?api_key=%s&language=en-US&sort_by=popularity.desc&include_null_first_air_dates=false&with_networks=%s&page=%s' % (tmdb_api, network_id, page_no)
    return cache_object(get_tmdb, string, url)

def tmdb_tv_similar(tmdb_id, page_no):
    string = "%s_%s_%s" % ('tmdb_tv_similar', tmdb_id, page_no)
    url = 'https://api.themoviedb.org/3/tv/%s/similar?api_key=%s&language=en-US&page=%s' % (tmdb_id, tmdb_api, page_no)
    return cache_object(get_tmdb, string, url)

def tmdb_tv_actor_roles(actor_id, page_no, letter, passed_list=[]):
    import ast
    from resources.lib.modules.nav_utils import paginate_list
    from resources.lib.modules.utils import title_key
    limit = 40
    if not passed_list:
        string = "%s_%s" % ('tmdb_tv_actor_roles', actor_id)
        url = 'https://api.themoviedb.org/3/person/%s/tv_credits?api_key=%s&language=en-US' % (int(actor_id), tmdb_api)
        data = cache_object(get_tmdb, string, url, 4)['cast']
        data = sorted(data, key=lambda k: title_key(k['name']))
        original_list = [{'media_id': i['id'], 'title': i['name']} for i in data]
    else: original_list = ast.literal_eval(passed_list)
    if page_no == 'None':
        return original_list
    paginated_list, total_pages = paginate_list(original_list, page_no, letter, limit)
    return paginated_list, original_list, total_pages, limit

def tmdb_tv_search(term, page_no):
    from resources.lib.modules.history import add_to_search_history
    add_to_search_history(term, 'tvshow_queries')
    string = "%s_%s_%s" % ('tmdb_tv_search', term, page_no)
    url = 'https://api.themoviedb.org/3/search/tv?api_key=%s&language=en-US&query=%s&page=%s' % (tmdb_api, term, page_no)
    return cache_object(get_tmdb, string, url, 4)

def tmdb_tv_people_search(term, page_no, letter, passed_list=[], actor_id=None):
    import xbmcgui
    import ast
    from resources.lib.modules.nav_utils import paginate_list
    limit = 40
    if not passed_list:
        dialog = xbmcgui.Dialog()
        string = "%s_%s" % ('tmdb_movies_people_search_actor_data', term)
        url = 'https://api.themoviedb.org/3/search/person?api_key=%s&language=en-US&query=%s&page=%s' % (tmdb_api, term, page_no)
        result1 = cache_object(get_tmdb, string, url, 4)
        info = result1['results']
        actor_list = []
        if len(info) > 1:
            for item in info:
                try: known_for_list = [i['name'] for i in item['known_for']]
                except: known_for_list = None
                known_for = 'TV Shows: [I]%s[/I]' % ', '.join(known_for_list) if known_for_list else 'TV Show Actor'
                listitem = xbmcgui.ListItem(item['name'], str(known_for), iconImage='http://image.tmdb.org/t/p/w300/%s' % item['profile_path'])
                listitem.setProperty('id', str(item['id']))
                actor_list.append(listitem)
            selection = dialog.select("Select Person", actor_list, useDetails=True)
            if selection >= 0:
                actor_id = int(actor_list[selection].getProperty('id'))
            else: return
        else:
            actor_id = [item['id'] for item in info][0]
        original_list = tmdb_tv_actor_roles(actor_id, 'None', letter, passed_list)
    else: original_list = ast.literal_eval(passed_list)
    paginated_list, total_pages = paginate_list(original_list, page_no, letter, limit)
    return paginated_list, original_list, total_pages, limit

def get_dates(days, reverse=True):
    import datetime
    current_date = datetime.date.today()
    if reverse: new_date = (current_date - datetime.timedelta(days=days)).strftime('%Y-%m-%d')
    else: new_date = (current_date + datetime.timedelta(days=days)).strftime('%Y-%m-%d')
    return str(current_date), new_date

def get_tmdb(url):
    try:
        def request(url):
            result = requests.get(url)
            response = result.status_code
            return str(response), result
        for i in range(15):
            response, result = request(url)
            if response == '200':
                return result
            elif response == '429':
                time.sleep(10)
                pass
            else:
                return
    except: pass
