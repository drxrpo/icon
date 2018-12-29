# -*- coding: utf-8 -*-

import urllib
import urlparse

from core import httptools
from core import scrapertools
from platformcode import logger


def test_video_exists(page_url):
    logger.info("(page_url='%s')" % page_url)
    data = httptools.downloadpage(page_url).data
    if "The file is being converted" in data or "Please try again later" in data:
        return False, "File in caricamento"
    elif "no longer exists" in data:
        return False, "File eliminato"
    return True, ""


def get_video_url(page_url, premium=False, user="", password="", video_password=""):
    logger.info("(page_url='%s')" % page_url)
    video_urls = []
    data = httptools.downloadpage(page_url).data

    page_url_post = scrapertools.find_single_match(data, r'<Form id="[^"]*" method="POST" action="([^"]+)">')
    post = urllib.urlencode(
        {k: v for k, v in scrapertools.find_multiple_matches(data, r'name="([^"]+)" value="([^"]*)"')})

    import xbmc
    xbmc.sleep(6 * 1000)

    page_url_post = urlparse.urljoin(page_url, page_url_post)

    data = httptools.downloadpage(page_url_post, post).data

    videourls = scrapertools.find_multiple_matches(data, r'source\s*:\s*"([^"]+)"')
    for videourl in videourls:
        ext = scrapertools.get_filename_from_url(videourl)[-4:]
        videourl = videourl.replace("%3F", "?") + \
                   "|User-Agent=Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:58.0) Gecko/20100101 Firefox/58.0"
        video_urls.append([ext + " [nowvideo]", videourl])
    return video_urls
