# ------------------------------------------------------------
# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# Stefano Thegroove 360
# Copyright 2018 https://stefanoaddon.info
#
# Distribuito sotto i termini di GNU General Public License v3 (GPLv3)
# http://www.gnu.org/licenses/gpl-3.0.html
# ------------------------------------------------- -----------
# Questo file fa parte di Stefano Thegroove 360.
#
# Stefano Thegroove 360 ​​è un software gratuito: puoi ridistribuirlo e / o modificarlo
# è sotto i termini della GNU General Public License come pubblicata da
# la Free Software Foundation, o la versione 3 della licenza, o
# (a tua scelta) qualsiasi versione successiva.
#
# Stefano Thegroove 360 ​​è distribuito nella speranza che possa essere utile,
# ma SENZA ALCUNA GARANZIA; senza nemmeno la garanzia implicita di
# COMMERCIABILITÀ o IDONEITÀ PER UN PARTICOLARE SCOPO. Vedere il
# GNU General Public License per maggiori dettagli.
#
# Dovresti aver ricevuto una copia della GNU General Public License
# insieme a Stefano Thegroove 360. In caso contrario, vedi <http://www.gnu.org/licenses/>.
# ------------------------------------------------- -----------
# Client for Stefano Thegroove 360
#------------------------------------------------------------



import xbmcplugin,xbmcgui,sys,os,re,urllib,urllib2

from resources.lib.modules import client
from resources.lib.modules import control
from resources.lib.modules import workers

syshandle = int(sys.argv[1])

class youtube_menu(object):
    def __init__(self):
        self.agent = 'VGFudHJ1bUFkZG9uQWdlbnQ='.decode('base64')
        self.key_id = 'QUl6YVN5QTU2ckhCQXlLMENsMFA0dURNXzEyc05Pd1VtQWFhczhF'.decode('base64')

    def openMenuFile(self, menuFile):
        req = urllib2.Request(menuFile)
        req.add_header('User-Agent', self.agent)
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        return link

    def processMenuFile(self, menuFile):
        link = self.openMenuFile(menuFile).replace('\n','').replace('\r','')
        match = re.compile('name="(.+?)".+?ection="(.+?)".+?earch="(.+?)".+?ubid="(.+?)".+?laylistid="(.+?)".+?hannelid="(.+?)".+?ideoid="(.+?)".+?con="(.+?)".+?anart="(.+?)".+?escription="(.+?)"').findall(link)
        return match

    def addMenuItem(self, name, action, subid, iconimage, fanart, description='', isFolder=True):
        u=sys.argv[0] + "?action=" + action + "&subid=" + subid
        liz=control.item(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo(type="Video", infoLabels={"Title": name, "Plot": description})
        liz.setProperty('fanart_image', fanart)
        control.addItem(handle=syshandle,url=u,listitem=liz,isFolder=isFolder)

    def addSectionItem(self, name, iconimage, fanart):
        u=sys.argv[0]+"?action=sectionItem"
        liz=control.item(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setProperty('fanart_image', fanart)
        control.addItem(handle=syshandle,url=u,listitem=liz,isFolder=False)

    def addSearchItem(self, name, search_id, icon, fanart):
        work_url = "plugin://plugin.video.youtube/kodion/search/query/?q="+search_id+"/"
        liz=control.item(name)
        liz.setInfo( type="Video", infoLabels={ "Title": name })
        liz.setArt({ 'thumb': icon, 'banner' : 'DefaultVideo.png', 'fanart': fanart })
#        liz.setPath(work_url)
        control.addItem(handle=syshandle,url=work_url,listitem=liz,isFolder=True)

    def addChannelItem(self, name, channel_id, icon, fanart):
        work_url = "plugin://plugin.video.youtube/channel/"+channel_id+"/"
        liz=control.item(name)
        liz.setInfo( type="Video", infoLabels={ "Title": name })
        liz.setArt({ 'thumb': icon, 'banner' : 'DefaultVideo.png', 'fanart': fanart })
#        liz.setPath(work_url)
        control.addItem(handle=syshandle,url=work_url,listitem=liz,isFolder=True)

    def addPlaylistItem(self, name, playlist_id, icon, fanart):
        work_url = "plugin://plugin.video.youtube/playlist/"+playlist_id+"/"
        liz=control.item(name)
        liz.setInfo( type="Video", infoLabels={ "Title": name })
        liz.setArt({ 'thumb': icon, 'banner' : 'DefaultVideo.png', 'fanart': fanart })
#        liz.setPath(work_url)
        control.addItem(handle=syshandle,url=work_url,listitem=liz,isFolder=True)

    def addVideoItem(self, name, video_id, icon, fanart):
        work_url = "plugin://plugin.video.youtube/play/?video_id="+video_id
        liz=control.item(name)
        liz.setInfo( type="Video", infoLabels={ "Title": name })
        liz.setArt({ 'thumb': icon, 'banner' : 'DefaultVideo.png', 'fanart': fanart })
#        liz.setPath(work_url)
        liz.setProperty('IsPlayable', 'true')
        control.addItem(handle=syshandle,url=work_url,listitem=liz,isFolder=True)
