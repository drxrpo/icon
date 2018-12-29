# -*- coding: utf-8 -*-
# StreamOnDemand Community Edition - Kodi Addon
# Credits: alfa add.on

import re

from core import httptools
from core import scrapertools
from platformcode import logger


def test_video_exists(page_url):
    logger.info("(page_url='%s')" % page_url)

    data = httptools.downloadpage(page_url).data
    if "copyrightsRestricted" in data or "COPYRIGHTS_RESTRICTED" in data:
        return False, "[Okru] File deleted for Copyright"
    elif "notFound" in data:
        return False, "[Okru] File deleted"

    return True, ""


def get_video_url(page_url, premium=False, user="", password="", video_password=""):
    logger.info("url=" + page_url)
    video_urls = []

    data = httptools.downloadpage(page_url).data
    data = scrapertools.decodeHtmlentities(data).replace('\\', '')
    # URL del vídeo
    for type, url in re.findall(r'\{"name":"([^"]+)","url":"([^"]+)"', data, re.DOTALL):
        url = url.replace("%3B", ";").replace("u0026", "&")
        video_urls.append([type + " [okru]", url])

    return video_urls

