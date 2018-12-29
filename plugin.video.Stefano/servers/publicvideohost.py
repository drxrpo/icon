# -*- coding: utf-8 -*-
# StreamOnDemand Community Edition - Kodi Addon
# ------------------------------------------------------------
# streamondemand - XBMC Plugin
# Conector for publicvideohost.org
# http://www.mimediacenter.info/foro/viewforum.php?f=36
# by DrZ3r0
# ------------------------------------------------------------

import re

from core import httptools
from platformcode import logger


def get_video_url(page_url, premium=False, user="", password="", video_password=""):
    logger.info("[publicvideohost.py] url=" + page_url)
    video_urls = []

    data = httptools.downloadpage(page_url).data

    # URL del vídeo
    for url in re.findall(r'playlist: \[\{\s*file: "([^"]+)",', data, re.DOTALL):
        video_urls.append([".flv" + " [publicvideohost]", url])

    return video_urls
