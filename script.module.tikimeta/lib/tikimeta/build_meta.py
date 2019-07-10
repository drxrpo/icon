# -*- coding: utf-8 -*-

import xbmcaddon
from tikimeta import tmdb
from tikimeta import fanarttv
from tikimeta.metacache import MetaCache
from tikimeta.utils import to_utf8, try_parse_int
from tikimeta.utils import get_fanart_data as gfd
# from tikimeta.utils import logger

get_fanart_data = gfd()

__addon__ = xbmcaddon.Addon("script.module.tikimeta")
icon_image = __addon__.getAddonInfo('icon')
fanart = __addon__.getAddonInfo('fanart')

def getMovieMeta(id_type, media_id, hours=720):
    from datetime import timedelta
    metacache = MetaCache()
    meta = None
    def tmdb_meta():
        data = tmdb.tmdbMovies
        result = tmdb.tmdbMoviesExternalID
        return data(media_id) if id_type == 'tmdb_id' else data(result(id_type, media_id)['id'])
    def fanarttv_meta(fanart_id):
        if get_fanart_data: return fanarttv.get('movies', fanart_id)
        else: return None
    def cached_meta():
        return metacache.get('movie', id_type, media_id)
    def set_cache_meta():
        metacache.set('movie', meta, timedelta(hours=hours))
    def delete_cache_meta():
        metacache.delete('movie', 'tmdb_id', meta['tmdb_id'])
    meta = cached_meta()
    if meta and get_fanart_data and not meta.get('fanart_added', False):
        try:
            meta = fanarttv.add('movies', meta['tmdb_id'], meta)
            delete_cache_meta()
            set_cache_meta()
        except: pass
    if not meta:
        try:
            tmdb_data = tmdb_meta()
            fanarttv_data = fanarttv_meta(tmdb_data['id'])
            meta = buildMeta('movie', tmdb_data, fanarttv_data)
            set_cache_meta()
        except: pass
    return meta

def getTVShowMeta(id_type, media_id, hours=168):
    from datetime import timedelta
    metacache = MetaCache()
    meta = None
    def tmdb_meta():
        data = tmdb.tmdbTVShows
        result = tmdb.tmdbTVShowsExternalID
        return data(media_id) if id_type == 'tmdb_id' else data(result(id_type, media_id)['id'])
    def fanarttv_meta(fanart_id):
        if get_fanart_data: return fanarttv.get('tv', fanart_id)
        else: return None
    def cached_meta():
        return metacache.get('tvshow', id_type, media_id)
    def set_cache_meta():
        metacache.set('tvshow', meta, timedelta(hours=hours))
    def delete_cache_meta():
        metacache.delete('tvshow', 'tmdb_id', meta['tmdb_id'])
    meta = cached_meta()
    if meta and get_fanart_data and not meta.get('fanart_added', False):
        try:
            meta = fanarttv.add('tv', meta['tvdb_id'], meta)
            delete_cache_meta()
            set_cache_meta()
        except: pass
    if not meta:
        try:
            data = tmdb_meta()
            fanarttv_data = fanarttv_meta(data['external_ids']['tvdb_id'])
            meta = buildMeta('tvshow', data, fanarttv_data)
            set_cache_meta()
        except: pass
    return meta

def getSeasonEpisodesMeta(media_id, season_no, hours=24):
    metacache = MetaCache()
    meta = None
    data = metacache.get('season', 'tmdb_id', media_id, season_no)
    if data: return data
    try:
        from datetime import timedelta
        meta = tmdb.tmdbSeasonEpisodes(media_id, season_no)
        meta['tmdb_id'] = media_id
        metacache.set('season', meta, timedelta(hours=hours), season_no)
    except: pass
    return meta

def buildMeta(db_type, data, fanarttv_data=None):
    meta = {}
    writer = []
    meta['cast'] = []
    meta['castandrole'] = []
    meta['studio'] = []
    meta['all_trailers'] = []
    meta['certification'] = ''
    meta['director'] = ''
    meta['premiered'] = ''
    meta['writer'] = ''
    meta['trailer'] = ''
    meta['tmdb_id'] = data['id'] if 'id' in data else ''
    meta['imdb_id'] = data.get('imdb_id', '') if db_type == 'movie' else data['external_ids'].get('imdb_id', '')
    meta['tvdb_id'] = data['external_ids'].get('tvdb_id', 'None')
    meta['poster'] = "http://image.tmdb.org/t/p/original%s" % data.get('poster_path') if data.get('poster_path') else icon_image
    meta['fanart'] = "http://image.tmdb.org/t/p/original%s" % data.get('backdrop_path') if data.get('backdrop_path') else fanart
    if fanarttv_data:
        meta['banner'] = fanarttv_data['banner']
        meta['clearart'] = fanarttv_data['clearart']
        meta['clearlogo'] = fanarttv_data['clearlogo']
        meta['landscape'] = fanarttv_data['landscape']
        meta['fanart_added'] = True
    else:
        meta['banner'] = ''
        meta['clearart'] = ''
        meta['clearlogo'] = ''
        meta['landscape'] = ''
        meta['fanart_added'] = False
    try: meta['year'] = try_parse_int(data['release_date'].split('-')[0]) if db_type == 'movie' else try_parse_int(data['first_air_date'].split('-')[0])
    except: meta['year'] = ''
    meta['duration'] = int(data['runtime'] * 60) if data.get('runtime') else ''
    meta['rating'] = data['vote_average'] if 'vote_average' in data else ''
    try: meta['genre'] = ', '.join([item['name'] for item in data['genres']])
    except: meta['genre'] == []
    meta['plot'] = to_utf8(data['overview']) if 'overview' in data else ''
    meta['title'] = to_utf8(data['title']) if db_type == 'movie' else to_utf8(data['name'])
    meta['tagline'] = to_utf8(data['tagline']) if 'tagline' in data else ''
    meta['votes'] = data['vote_count'] if 'vote_count' in data else ''
    meta['season_data'] = data['seasons'] if 'seasons' in data else ''
    meta['rootname'] = '{0} ({1})'.format(meta['title'], meta['year'])
    if db_type == 'movie':
        if data.get('production_companies'): meta['studio'] = [item['name'] for item in data['production_companies']]
        if data.get('release_date'): meta['premiered'] = data['release_date']
    else:
        try: meta['episode_run_time'] = min(data['episode_run_time']) * 60 if 'episode_run_time' in data else ''
        except: meta['episode_run_time'] = 30
        if data.get('networks', None):
            try: meta['studio'] = [item['name'] for item in data['networks']]
            except: meta['studio'] = []
        if data.get('first_air_date', None): meta['premiered'] = data.get('first_air_date', '')
        if data.get('number_of_seasons', None): meta['number_of_seasons'] = data.get('number_of_seasons', '')
        if data.get('number_of_episodes', None): meta['number_of_episodes'] = data.get('number_of_episodes', '')
        if data.get('last_episode_to_air', None): meta['last_episode_to_air'] = data.get('last_episode_to_air', '')
        if data.get('next_episode_to_air', None): meta['next_episode_to_air'] = data.get('next_episode_to_air', '')
        if data.get('in_production', None): meta['in_production'] = data.get('in_production', False) # True, False
        if data.get('status', None): meta['status'] = data.get('status', 'Ended') # Returning Series, Ended
    if 'release_dates' in data:
        for rel_info in data['release_dates']['results']:
            if rel_info['iso_3166_1'] == 'US':
                meta['certification'] = rel_info['release_dates'][0]['certification']
    if 'credits' in data:
        if 'cast' in data['credits']:
            for cast_member in data['credits']['cast']:
                cast_thumb = ''
                if cast_member['profile_path']:
                    cast_thumb = 'http://image.tmdb.org/t/p/original%s' % cast_member['profile_path']
                meta['cast'].append({'name': cast_member['name'], 'role': cast_member['character'], 'thumbnail': cast_thumb})
                meta['castandrole'].append((cast_member['name'], cast_member['character']))
        if 'crew' in data['credits']:
            for crew_member in data['credits']['crew']:
                cast_thumb = ''
                if crew_member['profile_path']:
                    cast_thumb = 'http://image.tmdb.org/t/p/original%s' % crew_member['profile_path']
                if crew_member['job'] in ['Author', 'Writer', 'Screenplay', 'Characters']:
                    writer.append(crew_member['name'])
                if crew_member['job'] == 'Director':
                    meta['director'] = crew_member['name']
            if writer: meta['writer'] = ', '.join(writer)
    if 'videos' in data:
        meta['all_trailers'] = data['videos']['results']
        for video in data['videos']['results']:
            if video['site'] == 'YouTube' and video['type'] == 'Trailer' or video['type'] == 'Teaser':
                meta['trailer'] = 'plugin://plugin.video.youtube/play/?video_id=%s' % video['key']
                break
    return to_utf8(meta)