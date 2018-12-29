# -*- coding: utf-8 -*-
# StreamOnDemand Community Edition - Kodi Addon
# by errmax, dr-z3r0
# Rel: 20180127
import re

from core import httptools, servertools
from platformcode import logger
from servers.decrypters import expurl


def find_videos(text):
    encontrados = {
        'https://vcrypt.net/images/logo', 'https://vcrypt.net/css/out',
        'https://vcrypt.net/images/favicon', 'https://vcrypt.net/css/open',
        'http://linkup.pro/js/jquery', 'https://linkup.pro/js/jquery',
        'http://www.rapidcrypt.net/open'
    }
    devuelve = []

    patronvideos = [
        r'(https?://(gestyy|rapidteria|sprysphere)\.com/[a-zA-Z0-9]+)',
        r'(https?://(vcrypt|linkup)\.[^/]+/[^/]+/[a-zA-Z0-9]+)'
    ]

    for patron in patronvideos:
        logger.info(" find_videos #" + patron + "#")
        matches = re.compile(patron).findall(text)

        for url, host in matches:
            if url not in encontrados:
                logger.info("  url=" + url)
                encontrados.add(url)

                if host == 'gestyy':
                    resp = httptools.downloadpage(
                        url,
                        follow_redirects=False,
                        cookies=False,
                        only_headers=True,
                        replace_headers=True,
                        headers={'User-Agent': 'curl/7.59.0'})
                    data = resp.headers.get("location", "")
                else:
                    data = ""
                    while host in url:
                        resp = httptools.downloadpage(
                            url, follow_redirects=False)
                        url = resp.headers.get("location", "")
                        if not url:
                            data = resp.data
                        elif host not in url:
                            data = url
                if data:
                    devuelve.append(data)
            else:
                logger.info("  url duplicada=" + url)

    patron = r"""(https?://(?:www\.)?(?:threadsphere\.bid|adf\.ly|q\.gs|j\.gs|u\.bb|ay\.gy|linkbucks\.com|any\.gs|cash4links\.co|cash4files\.co|dyo\.gs|filesonthe\.net|goneviral\.com|megaline\.co|miniurls\.co|qqc\.co|seriousdeals\.net|theseblogs\.com|theseforums\.com|tinylinks\.co|tubeviral\.com|ultrafiles\.net|urlbeat\.net|whackyvidz\.com|yyv\.co|adfoc\.us|lnx\.lu|sh\.st|href\.li|anonymz\.com|shrink-service\.it|rapidcrypt\.net)/[^"']+)"""

    logger.info(" find_videos #" + patron + "#")
    matches = re.compile(patron).findall(text)

    for url in matches:
        if url not in encontrados:
            logger.info("  url=" + url)
            encontrados.add(url)

            long_url = expurl.expand_url(url)
            if long_url:
                devuelve.append(long_url)
        else:
            logger.info("  url duplicada=" + url)

    ret = servertools.findvideos(str(devuelve)) if devuelve else []
    return ret
