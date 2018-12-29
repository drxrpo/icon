# -*- coding: utf-8 -*-
# StreamOnDemand Community Edition - Kodi Addon

from core import httptools, scrapertools
from platformcode import logger


def test_video_exists(page_url):
    logger.info("(page_url='%s')" % page_url)
    data = httptools.downloadpage(page_url).data
    if "Page not found" in data or "File was deleted" in data:
        return False, "[vidoza] Video non trovato"
    elif "processing" in data:
        return False, "[vidoza] Video in conversione"

    return True, ""


def get_video_url(page_url, premium=False, user="", password="", video_password=""):
    logger.info("(page_url='%s')" % page_url)
    data = httptools.downloadpage(page_url).data
    video_urls = []
    matches = scrapertools.find_multiple_matches(data, r'file\s*:\s*"([^"]+)"\s*,\s*label:"([^"]+)"')
    for media_url, calidad in matches:
        ext = media_url[-4:]
        video_urls.append(["%s %s [vidoza]" % (ext, calidad), media_url])

    video_urls.reverse()
    for video_url in video_urls:
        logger.info("%s - %s" % (video_url[0], video_url[1]))

    return video_urls
