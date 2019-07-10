# -*- coding: utf-8 -*-

import xbmcaddon
import requests, time
from tikimeta.utils import tmdbApi
# from tikimeta.utils import logger

tmdb_api = tmdbApi()

def tmdbMovies(tmdb_id):
    url = 'https://api.themoviedb.org/3/movie/%s?api_key=%s&language=en-US&append_to_response=external_ids,videos,credits,release_dates' % (tmdb_id, tmdb_api)
    return getTmdb(url).json()

def tmdbMoviesExternalID(external_source, external_id):
    from tikimeta.utils import cache_function
    string = "%s_%s_%s" % ('tmdbMoviesExternalID', external_source, external_id)
    url = 'https://api.themoviedb.org/3/find/%s?api_key=%s&external_source=%s' % (external_id, tmdb_api, external_source)
    return cache_function(getTmdb, string, url)['movie_results'][0]

def tmdbMoviesTitleYear(title, year):
    from tikimeta.utils import cache_function
    string = "%s_%s_%s" % ('tmdbMoviesTitleYear', title, year)
    url = 'https://api.themoviedb.org/3/search/movie?api_key=%s&language=en-US&query=%s&year=%s&page=%s' % (tmdb_api, title, year)
    result = cache_function(string, url)
    return result['results'][0]

def tmdbTVShows(tmdb_id):
    url = 'https://api.themoviedb.org/3/tv/%s?api_key=%s&language=en-US&append_to_response=external_ids,videos,credits' % (tmdb_id, tmdb_api)
    return getTmdb(url).json()

def tmdbTVShowsExternalID(external_source, external_id):
    from tikimeta.utils import cache_function
    string = "%s_%s_%s" % ('tmdbTVShowsExternalID', external_source, external_id)
    url = 'https://api.themoviedb.org/3/find/%s?api_key=%s&external_source=%s' % (external_id, tmdb_api, external_source)
    return cache_function(getTmdb, string, url)['tv_results'][0]

def tmdbTVShowsTitleYear(title, year):
    from tikimeta.utils import cache_function
    string = "%s_%s_%s" % ('tmdbTVShowsTitleYear', title, year)
    url = 'https://api.themoviedb.org/3/search/tv?api_key=%s&query=%s&first_air_date_year=%s&language=en-US' % (tmdb_api, title, year)
    return cache_function(get_tmdb, string, url)['results'][0]

def tmdbSeasonEpisodes(tmdb_id, season_no):
    url = 'https://api.themoviedb.org/3/tv/%s/season/%s?api_key=%s&language=en-US&append_to_response=credits' % (tmdb_id, int(season_no), tmdb_api)
    return getTmdb(url).json()

def getTmdb(url):
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

