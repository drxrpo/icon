# -*- coding: utf-8 -*-
# StreamOnDemand Community Edition - Kodi Addon
# Credits: alfa add-on

from core import httptools
from core import scrapertools
from platformcode import logger


def test_video_exists(page_url):
    logger.info("(page_url='%s')" % page_url)
    try:
        response = httptools.downloadpage(page_url)
    except:
        pass

    if not response.data or "urlopen error [Errno 1]" in str(response.code):
        from core import config
        if config.is_xbmc():
            return False, "[Rapidvideo] works only on Kodi 17"
        elif config.get_platform() == "plex":
            return False, "[Rapidvideo] Update Plex for this connector"
        elif config.get_platform() == "mediaserver":
            return False, "[Rapidvideo] Mediaserver version 2.7.9 or above is needed"

    if "Object not found" in response.data:
        return False, "[Rapidvideo] File do not exist"
    if response.code == 500:
        return False, "[Rapidvideo] Server not available. Try later."

    return True, ""

def get_video_url(page_url, premium=False, user="", password="", video_password=""):
    logger.info("url=" + page_url)
    video_urls = []
    data = httptools.downloadpage(page_url).data
    patron = 'https://www.rapidvideo.com/e/[^"]+'
    match = scrapertools.find_multiple_matches(data, patron)
    for url1 in match:
       res = scrapertools.find_single_match(url1, '=(\w+)')
       data = httptools.downloadpage(url1).data
       url = scrapertools.find_single_match(data, 'source src="([^"]+)')
       ext = scrapertools.get_filename_from_url(url)[-4:]
       video_urls.append(['%s %s [rapidvideo]' % (ext, res), url])

    return video_urls
