# -*- coding: utf-8 -*-
# StreamOnDemand Community Edition - Kodi Addon
# by DrZ3r0

import urllib

from platformcode import logger
from core import scrapertools
from lib.aadecode import decode as aadecode


def test_video_exists(page_url):
    logger.info("(page_url='%s')" % page_url)

    data = scrapertools.cache_page(page_url)

    if "This video doesn't exist." in data:
        return False, 'Il video non è stato trovato.'

    return True, ""


def get_video_url(page_url, premium=False, user="", password="", video_password=""):
    logger.info("url=" + page_url)
    video_urls = []

    headers = [
        ['User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0'],
        ['Accept-Encoding', 'gzip, deflate'],
        ['Referer', page_url]
    ]

    data = scrapertools.cache_page(page_url, headers=headers)
    text_encode = scrapertools.find_single_match(data, "split\('\|'\)\)\)\s*(.*?)</script>")

    if text_encode:
        text_decode = aadecode(text_encode)

        # URL del video
        patron = "'([^']+)"
        media_url = scrapertools.find_single_match(text_decode, patron)

        video_urls.append([media_url[-4:] + " [Videowood]", media_url + '|' + urllib.urlencode(dict(headers))])

    return video_urls
