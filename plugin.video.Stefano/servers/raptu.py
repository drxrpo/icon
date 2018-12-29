# -*- coding: utf-8 -*-
# StreamOnDemand Community Edition - Kodi Addon

from core import httptools
from platformcode import logger
from core import scrapertools


def test_video_exists(page_url):
    logger.info("(page_url='%s')" % page_url)
    try:
        response = httptools.downloadpage(page_url)
    except:
        pass

    if not response.data or "urlopen error [Errno 1]" in str(response.code):
        from core import config
        if config.is_xbmc():
            return False, "[Raptu] Questo connettore funziona solo da Kodi 17"
        elif config.get_platform() == "plex":
            return False, "[Raptu] Questo connettore non funziona con la versione di Plex, provare ad aggiornare"
        elif config.get_platform() == "mediaserver":
            return False, "[Raptu] Questo connettore richiede aggiornamento alla versione 2.7.9 o superiore di python"

    if "Object not found" in response.data:
        return False, "[Raptu] Il file non esiste o è stato cancellato"

    return True, ""


def get_video_url(page_url, premium=False, user="", password="", video_password=""):
    logger.info("(page_url='%s')" % page_url)

    data = httptools.downloadpage(page_url).data
    video_urls = []
    # Detección de subtítulos
    subtitulo = ""
    videos = scrapertools.find_multiple_matches(data, '"file"\s*:\s*"([^"]+)","label"\s*:\s*"([^"]+)"')
    for video_url, calidad in videos:
        video_url = video_url.replace("\\", "")
        extension = scrapertools.get_filename_from_url(video_url)[-4:]
        if ".srt" in extension:
            subtitulo = "https://www.raptu.com" + video_url
        else:
            video_urls.append(["%s %s [raptu]" % (extension, calidad), video_url, 0, subtitulo])

    try:
        video_urls.sort(key=lambda it: int(it[0].split("p ", 1)[0].rsplit(" ")[1]))
    except:
        pass
    for video_url in video_urls:
        logger.info(" %s - %s" % (video_url[0], video_url[1]))

    return video_urls
