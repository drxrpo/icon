# -*- coding: utf-8 -*-

import xbmcaddon
__addon__ = xbmcaddon.Addon(id='script.module.tikimeta')

def logger(heading, function):
    import xbmc
    xbmc.log('###%s###: %s' % (heading, function), 2)

def notification(line1, time=5000, icon=__addon__.getAddonInfo('icon'), sound=False):
    import xbmcgui
    xbmcgui.Dialog().notification('Tiki Meta', line1, icon, time, sound)

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

def try_parse_int(string):
    '''helper to parse int from string without erroring on empty or misformed string'''
    try:
        return int(string)
    except Exception:
        return 0

def tmdbApi():
    tmdb_api = __addon__.getSetting('tmdb_api')
    if not tmdb_api or tmdb_api == '':
        tmdb_api = '1b0d3c6ac6a6c0fa87b55a1069d6c9c8'
    return tmdb_api

def get_fanart_data():
    if __addon__.getSetting('get_fanart_data') in ('false', ''):
        return False
    return True

def fanarttv_client_key():
    return __addon__.getSetting('fanart_client_key')

def cache_function(function, string, url, expiration=24):
    from datetime import timedelta
    from tikimeta.metacache import MetaCache
    metacache = MetaCache()
    data = metacache.get_function(string)
    if data: return to_utf8(data)
    result = function(url).json()
    metacache.set_function(string, result, expiration=timedelta(hours=expiration))
    return to_utf8(result)




