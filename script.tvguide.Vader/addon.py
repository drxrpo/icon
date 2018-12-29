# -*- coding: utf-8 -*-
#
#      Copyright (C) 2012 Tommy Winther
#      http://tommy.winther.nu
#
#      Modified for FTV Guide (09/2014 onwards)
#      by Thomas Geppert [bluezed] - bluezed.apps@gmail.com
#
#      Modified for TV Guide Fullscreen (2016)
#      by primaeval - primaeval.dev@gmail.com
#
#  This Program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2, or (at your option)
#  any later version.
#
#  This Program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this Program; see the file LICENSE.txt.  If not, write to
#  the Free Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.
#  http://www.gnu.org/copyleft/gpl.html
#

import sys
import xbmc,xbmcaddon,xbmcvfs
import os
import stat
import base64,time,datetime
import xbmcplugin,xbmcgui,urllib,urllib2,re,time,datetime,string,StringIO,logging,random,array,htmllib

ADDON = xbmcaddon.Addon(id='script.tvguide.Vader')

file_name = 'Special://home/addons/plugin.video.VADER/addon.xml'
if xbmcvfs.exists(file_name):
    xbmcvfs.rename('Special://home/addons/script.tvguide.Vader/resources/skins/Default','Special://home/addons/script.tvguide.Vader/resources/skins/Default_BASIC')
    xbmcvfs.rename('Special://home/addons/script.tvguide.Vader/resources/skins/VADER','Special://home/addons/script.tvguide.Vader/resources/skins/Default')
if ADDON.getSetting('cat.source') == "0":
    xbmcvfs.copy('http://localhost:62555/getCategories','special://profile/addon_data/script.tvguide.Vader/categories.ini')
elif ADDON.getSetting('cat.source') == "1":
    xbmcvfs.copy((base64.decodestring('aHR0cDovL3R2c3RyZWFtZXJzLm5ldC9zbXVyZi9WR3VpZGUvQWx0ZXJuYXRpdmUvY2F0ZWdvcmllcy5pbmk=')),'special://profile/addon_data/script.tvguide.Vader/categories.ini')

if len(sys.argv) > 1:
    category = sys.argv[1]
    if category:
        ADDON.setSetting('category',category)

if len(sys.argv) > 2:
    source = ADDON.getSetting('source.source')
    new_source = sys.argv[2]
    if new_source != source:
        ADDON.setSetting('source.source',new_source)

assets = [
('special://profile/addon_data/script.tvguide.Vader/actions.json','special://home/addons/script.tvguide.Vader/resources/actions.json'),
]
for (dst,src) in assets:
    if not xbmcvfs.exists(dst):
        xbmcvfs.copy(src,dst)

try:
    import gui
    w = gui.TVGuide()
    w.doModal()
    del w

except:
    import sys
    import traceback as tb
    (etype, value, traceback) = sys.exc_info()
    tb.print_exception(etype, value, traceback)
