#########################################################################
#########################################################################
####                                                                 ####
####               Too lazy to figure it out yourself?               ####
####                                                                 ####
#########################################################################
#########################################################################

#       Copyright (C) 2018
#
#  This Program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2, or (at your option)
#  any later version.
#
#  This Progr`am is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with XBMC; see the file COPYING.  If not, write to
#  the Free Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.
#  http://www.gnu.org/copyleft/gpl.htm
#

import xbmcgui

import sys
import inspect
import re
import datetime
import time

import iptv_utils

import base64

GETTEXT = iptv_utils.GETTEXT

WHERES_THE_MATCH = 'http://www.wheresthematch.com/tv/home.asp?showdatestart=%s&showdateend=%s&sportid=%d'


def log(text):
    iptv_utils.log(text, True)


def _Darts():
    #url = 'http://www.skysports.com/darts/schedule'
    #match = re.compile('<div class="score-sub" style="width:56px">(.+?)</div> <div class="score-comp">(.+?)</div> <div class="score-side" style="width:360px">(.+?)</div> <ul class="score-sublinks"> <li class="score-tv"><img src=".+?" title="(.+?)"></li>').findall(response)

    url = 'http://www.skysports.com/watch/darts-on-sky'

    response = iptv_utils.GetURL(url, maxSec=43200, clean=True)

    match = re.compile('style20 box">(.+?)</h3>.+?<strong>(.+?)</strong>.+?caption">(.+?)</p>').findall(response)

    responses = []
    for date, title, channels in match:
        channels = [c.strip() for c in channels.split(',')]
        responses.append((title, date, '', '[CR]'.join(channels)))

    return PopulateResults(responses, [])


def _NBA():
    sport_id = 23

    start = datetime.datetime.now()
    end   = start + datetime.timedelta(days=7)

    start = start.strftime('%Y%m%d')
    end   = end.strftime('%Y%m%d')

    url = WHERES_THE_MATCH % (start, end, sport_id)

    response = iptv_utils.GetURL(url, maxSec=43200, clean=True)

    match = re.compile('<span class="fixture"> <em class="">(.+?)</em> <em class="">v</em> <em class="">(.+?)</em></span> <span class="ground "><span class="time-channel "><strong>WHEN:</strong>.+?<strong>TV CHANNEL:</strong>(.+?)</span></span>.+?<td class="start-details"> <span>(.+?)</span><span class="time"><em>(.+?)</em></span>').findall(response)

    blurred = re.compile('<span class="fixture"> <em class="blurred-not-selectable">(.+?)</em> <em class="blurred-not-selectable">v</em> <em class="blurred-not-selectable">(.+?)</em></span> <span class="ground blurred-not-selectable"><span class="time-channel blurred-not-selectable"><strong>WHEN:</strong>.+?<strong>TV CHANNEL:</strong>(.+?)</span></span>.+?<td class="start-details"> <span>(.+?)</span><span class="time"><em>(.+?)</em></span>').findall(response)

    match.extend(blurred)

    results = []
    #title = '[COLOR white]%s[/COLOR]' % GETTEXT(30017)
    #result          = {}
    #result['title'] = title
    #result['desc']  = title
    #results.append(result)

    responses = []
    for home, away, channel, date, time in match:
        title = GETTEXT(30018) % (home.strip(), away.strip())
        responses.append((title, date, time, channel))

    return PopulateResults(responses, results)


def _NHL():
    return []


def _MLB():
    return []


def _UFC():
    return []


def _Rugby_Union():
    return []


def _Rugby_League():
    return [] 


def _Tennis():
    sport_id = 17

    start = datetime.datetime.now()
    end   = start + datetime.timedelta(days=7)

    start = start.strftime('%Y%m%d')
    end   = end.strftime('%Y%m%d')

    url = WHERES_THE_MATCH % (start, end, sport_id)

    response = iptv_utils.GetURL(url, maxSec=43200, clean=True)

    match = re.compile('<span class="fixture"><a class=" eventlink" href=".+?"><strong class="">(.+?)</strong></a></span> <em class="">(.+?)</em> <span class="ground "><span class="time-channel ">.+?</span></span> </td> <td class="away-team"></td> <td class="start-details"> <span>(.+?)</span><span class="time"><em>(.+?)</em></span>.+?<span class="channel-name">(.+?)</span>').findall(response)

    blurred = re.compile('<span class="fixture"><a class="disable-link eventlink" href=".+?"><strong class="blurred-not-selectable">(.+?)</strong></a></span> <em class="blurred-not-selectable">(.+?)</em> <span class="ground blurred-not-selectable"><span class="time-channel blurred-not-selectable">(.+?)</span></span>.+?<td class="start-details"> <span>(.+?)</span><span class="time"><em>(.+?)</em></span>').findall(response)

    for competition, event, channel, date, time in blurred:
        match.append((competition, event, date, time, channel.split(' on ', 1)[-1]))

    responses = []
    for competition, event, date, time, channel in match:
        title = '%s, %s' % (competition.strip(), event.strip())
        responses.append((title, date, time, channel))

    return PopulateResults(responses, [])


def _Wrestling():
    return []


def _Horse_Racing():
    return []


def _Boxing():
    return []


def _Motorsport():
    return []


def _Golf():
    return []


def _Moto_GP():
    return []


def _Cycling():
    return []


def _Hockey():
    return []


def Listings():
    functions = inspect.getmembers(sys.modules[__name__], inspect.isfunction)
    functions = [f for f in functions if f[0].startswith('_')]

    options = ['[COLOR white]%s[/COLOR]' % f[0][1:].replace('_', ' ') for f in functions] 

    title = '[COLOR white]Sport Schedules[/COLOR]'

    choice = xbmcgui.Dialog().select(title, options)

    if choice < 0:
        raise iptv_utils.EmptyListException(text='', reason='Selection cancelled')

    try:    return functions[choice][1]()
    except Exception as e:
        iptv_utils.log(e, True)
        iptv_utils.DialogOK('ERROR')


def PopulateResults(responses, results):
    for title, line1, line2, line3 in responses:
        title = title.strip()
        line1 = line1.strip()
        line2 = line2.strip()
        line3 = line3.strip()

        result = {}

        plot = []
        if title:
            plot.append('[COLOR skyblue]%s[/COLOR]' % title)
        if line1:
            plot.append(line1)
        if line2:
            plot.append(line2)
        if line3:
            plot.append('[COLOR yellow]%s[/COLOR]' % line3)
        plot = '[CR]'.join(plot)

        result['title'] = '[COLOR white]%s[/COLOR]' % title
        result['desc']  = '[COLOR white]%s[/COLOR]' % title
        result['plot']  = plot

        results.append(result)

    return results
