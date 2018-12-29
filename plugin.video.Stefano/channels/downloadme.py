# -*- coding: utf-8 -*-
# StreamOnDemand Community Edition - Kodi Addon
# ------------------------------------------------------------
# Stefano.- XBMC Plugin
# Canale downloadme
# http://www.mimediacenter.info/foro/viewforum.php?f=36
# Version: 201804162230
# ------------------------------------------------------------
import re

from core import httptools, scrapertools
from core.item import Item
from platformcode import logger
from core import servertools
from core.tmdb import infoSod
from servers.decrypters import expurl

__channel__ = "downloadme"

host = "https://downloadme.altervista.org"

headers = [['Referer', host]]


def mainlist(item):
    logger.info("[downloadme.py] mainlist")

    # Main options
    itemlist = [Item(channel=__channel__,
                     action="peliculas",
                     title="[COLOR azure]Film[/COLOR]",
                     url="%s/category/film/" % host,
                     extra="movie",
                     thumbnail="http://orig03.deviantart.net/6889/f/2014/079/7/b/movies_and_popcorn_folder_icon_by_matheusgrilo-d7ay4tw.png"),
                Item(channel=__channel__,
                     action="categorie",
                     title="[COLOR azure]Categorie[/COLOR]",
                     url="%s/" % host,
                     extra="movie",
                     thumbnail="http://orig03.deviantart.net/6889/f/2014/079/7/b/movies_and_popcorn_folder_icon_by_matheusgrilo-d7ay4tw.png")]

    return itemlist

def peliculas(item):
    logger.info("[downloadme.py] peliculas")
    itemlist = []

    data = httptools.downloadpage(item.url, headers=headers).data
    patron = '<figure class=[^<]+<a href="([^"]+)" title="(.*?)">'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedtitle in matches:
        scrapedtitle = scrapedtitle.split("&#8211;")[0]
        scrapedtitle = scrapedtitle.split(" Download")[0]
        scrapedthumbnail = ""
        itemlist.append(infoSod(
            Item(channel=__channel__,
                 action="findvideos",
                 fulltitle=scrapedtitle,
                 show=scrapedtitle,
                 title=scrapedtitle,
                 url=scrapedurl,
                 viewmode="movie_with_plot",
                 thumbnail=scrapedthumbnail), tipo="movie"))

    nextpage_regex = '<a class="next page-numbers" href="([^"]+)">'
    next_page = scrapertools.find_single_match(data, nextpage_regex)
    if next_page != "":
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas",
                 title="[COLOR orange]Successivo >>[/COLOR]",
                 url="%s" % next_page,
                 extra=item.extra,
                 thumbnail="http://2.bp.blogspot.com/-fE9tzwmjaeQ/UcM2apxDtjI/AAAAAAAAeeg/WKSGM2TADLM/s1600/pager+old.png"))
    return itemlist


def categorie(item):
    logger.info("[downloadme.py] peliculas")
    itemlist = []

    if item.url == "":
        item.url = host

    data = httptools.downloadpage(item.url, headers=headers).data
    patron = '<li .*? menu-item-type-taxonomy menu-item-object-category menu-item-.*?"><a href="([^"]+)">([^<]+)<\/a><\/li>'
    matches = re.compile(patron, re.DOTALL).findall(data)

    for scrapedurl, scrapedtitle in matches:
        itemlist.append(
            Item(channel=__channel__,
                 action="peliculas",
                 fulltitle=scrapedtitle,
                 show=scrapedtitle,
                 title=scrapedtitle,
                 url=scrapedurl,
                 extra=item.extra,
                 viewmode="movie_with_plot",
                 Folder=True))

    return itemlist

def findvideos(item):
    logger.info("Stefano.downloadme findvideos")
    itemlist = []

    # Carica la pagina 
    data = httptools.downloadpage(item.url, headers=headers).data

    if 'velociterium' in data:

        resp = httptools.downloadpage(
             data, follow_redirects=False)
        data = resp.headers.get("location", "")


    itemlist = servertools.find_video_items(data=data)

    for videoitem in itemlist:
        videoitem.title = item.title + videoitem.title
        videoitem.fulltitle = item.fulltitle
        videoitem.thumbnail = item.thumbnail
        videoitem.show = item.show
        videoitem.plot = item.plot
        videoitem.channel = __channel__

    return itemlist

