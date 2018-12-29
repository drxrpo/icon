# -*- coding: utf-8 -*-
# StreamOnDemand Community Edition - Kodi Addon

import urllib
import urlparse

import xbmc
from core import httptools, scrapertools
from platformcode import logger


def test_video_exists(page_url):
    logger.info("(page_url='%s')" % page_url)

    data = httptools.downloadpage(page_url).data

    if "Not Found" in data or "File Does not Exist" in data:
        return False, "[Vidto.me] File non trovato"

    return True, ""


def get_video_url(page_url, premium=False, user="", password="", video_password=""):
    logger.info("url=" + page_url)

    if 'vidtome.co' in page_url:
        return vidtomeco(page_url)
    else:
        return vidtome(page_url)


def vidtome(page_url):

    data = httptools.downloadpage(page_url).data
    # Extrae la URL
    # {file:"http://188.240.220.186/drjhpzy4lqqwws4phv3twywfxej5nwmi4nhxlriivuopt2pul3o4bkge5hxa/video.mp4",label:"240p"}
    video_urls = []
    media_urls = scrapertools.find_multiple_matches(data, '\{file\s*:\s*"([^"]+)",label\s*:\s*"([^"]+)"\}')
    for media_url, label in media_urls:
        ext = scrapertools.get_filename_from_url(media_url)[-4:]
        video_urls.append(["%s (%s) [vidto.me]" % (ext, label), media_url])

    video_urls.reverse()
    for video_url in video_urls:
        logger.info("%s - %s" % (video_url[0], video_url[1]))

    return video_urls


def vidtomeco(page_url):
    data = httptools.downloadpage(page_url).data.replace('"', "'")

    page_url_post = scrapertools.find_single_match(data, "<Form method='POST' action='([^']+)'>")
    page_url_post = urlparse.urljoin(page_url, page_url_post)
    post_data = urllib.urlencode({k: v for k, v in scrapertools.find_multiple_matches(data, "name='([^']+)' value='([^']*)'")})

    xbmc.sleep(6000)

    data = httptools.downloadpage(page_url_post, post=post_data, headers={'Referer': page_url}).data.replace('"', "'")

    video_urls = []
    media_urls = scrapertools.find_multiple_matches(data, "source\s*:\s*'([^']+?)',[^,]+?,\s*height\s*:\s*([^,]+?),")
    for media_url, label in media_urls:
        ext = scrapertools.get_filename_from_url(media_url)[-4:]
        video_urls.append(["%s (%s) [vidto.me]" % (ext, label), media_url])

    video_urls.reverse()
    for video_url in video_urls:
        logger.info("%s - %s" % (video_url[0], video_url[1]))

    return video_urls
