# # -*- coding: utf-8 -*-
# from tikimeta.utils import logger

def movie_meta(id_type, media_id, hours=720):
    from tikimeta.build_meta import getMovieMeta
    return getMovieMeta(id_type, media_id, hours)

def tvshow_meta(id_type, media_id, hours=168):
    from tikimeta.build_meta import getTVShowMeta
    return getTVShowMeta(id_type, media_id, hours)

def season_episodes_meta(media_id, season_no, hours=24):
    from tikimeta.build_meta import getSeasonEpisodesMeta
    return getSeasonEpisodesMeta(media_id, season_no, hours)

def delete_cache_item(db_type, id_type, media_id):
    from tikimeta.metacache import MetaCache
    return MetaCache().delete(db_type, id_type, media_id)

def delete_meta_cache():
    try:
        import xbmcgui
        if not xbmcgui.Dialog().yesno('Are you sure?','Tiki Meta will Clear all Metadata.'):
            return False
        from tikimeta.metacache import MetaCache
        MetaCache().delete_all()
        return True
    except:
        return False