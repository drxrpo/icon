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

import os
import json

import iptv_utils
import iptv2

 
GETTEXT = iptv_utils.GETTEXT


ACTION_BACK          = 92
ACTION_PARENT_DIR    = 9
ACTION_PREVIOUS_MENU = 10



def setProperty(label, text):
    xbmcgui.Window(10000).setProperty(label, text)


def clearProperty(label):
    xbmcgui.Window(10000).setProperty(label, None)


def getDuration(info):
    try:
        duration = int(info['duration_secs'])
        h = duration / 3600
        m = ((duration % 3600) + 30) / 60

        # minute can end up as 60 due to rounding, therefore correct if necessary
        if m == 60:
            h += 1
            m = 0

        return '[B]%s[/B] %02d%s %02d%s' % (GETTEXT(37007), h, GETTEXT(37014), m, GETTEXT(37015))
    except:
        'Unavailable'


class BrowseDialog(xbmcgui.WindowXMLDialog):
    def __new__(cls, params):
        addonID = params['addonID']
        skin    = iptv_utils.GetSetting('SKIN')
        path    = os.path.join(iptv_utils.GetAddonInfo('path', addonID), 'resources', 'skins', skin)

        return super(BrowseDialog, cls).__new__(cls, 'browseDialog.xml', path)
        

    def __init__(self, params):
        super(BrowseDialog, self).__init__()
        self.params = params
        self.option = None


    def close(self):
        clearProperty('FL_BR_FANART')
        clearProperty('FL_BR_IMAGE')
        clearProperty('FL_BR_TITLE')
        clearProperty('FL_BR_DURATION')
        clearProperty('FL_BR_RELEASEDATE')
        clearProperty('FL_BR_RATING')
        clearProperty('FL_BR_GENRE')
        clearProperty('FL_BR_DIRECTOR')
        clearProperty('FL_BR_BITRATE')
        clearProperty('FL_BR_PLOT')
        clearProperty('FL_BR_CAST')
        xbmcgui.WindowXMLDialog.close(self)


    def GetVODInfo(self):
        stream_id = self.params['url']

        info = iptv2.GetVODInfo(stream_id)['info']

        category_id = None
        url = self.params['url']
        if ':' in url:
            try:
                category_id = url.split(':')[-1] #use to get cast, genre, rating

                response = iptv2.GetSeriesByCategoryID(category_id)

                items = ['genre', 'cast']

                for item in items:
                    info[item] = response[item]

            except:
                pass

        return info

        
    def onInit(self):
        try:
            title  = self.params.get('title',  '')
            image  = self.params.get('image',  '')
            fanart = self.params.get('fanart', '')

            #setProperty('FL_BR_FANART',   fanart)
            setProperty('FL_BR_IMAGE',    image)
            setProperty('FL_BR_TITLE',   '[B]%s[/B]'  % title.upper())

            stream_id = self.params['url']

            info = self.GetVODInfo()

            setProperty('FL_BR_DURATION', getDuration(info))
            self.setText('RELEASEDATE', GETTEXT(37005), info)
            self.setText('RATING',      GETTEXT(37006), info)
            self.setText('GENRE',       GETTEXT(37008), info)
            self.setText('DIRECTOR',    GETTEXT(37009), info)
            self.setText('BITRATE',     GETTEXT(37010), info)
            self.setText('PLOT',        GETTEXT(37012), info)
            self.setText('CAST',        GETTEXT(37013), info)
        except Exception as e:
            iptv_utils.DialogOK("%r" % e)



    def setText(self, id, label, info):
        infoL = 'FL_BR_%s' % id
        item  = '%s:' % id
        try:    text  = '[B]%s[/B] %s' % (label, info[id.lower()].replace(' / ', ', '))
        except: text = ' '
        setProperty(infoL, text)

           
    def onAction(self, action):  
        actionID = action.getId()

        if actionID in [ACTION_PARENT_DIR, ACTION_PREVIOUS_MENU, ACTION_BACK]:
            return self.close()
        

    def onClick(self, controlID):
        close = controlID in [5015, 5016, 5017, 5018]

        if controlID == 5015:
            self.option = 'PLAY'

        elif controlID == 5016:
            pass

        elif controlID == 5017:
            self.option = 'DOWNLOAD'

        elif controlID == 5018:
            self.option = 'TRAILER'

        if close:
            return self.close()
        

    def onFocus(self, controlID):
        pass


def show(addonID, params):
    if xbmcgui.Window(10000).getProperty('FL_R') == 'true':
        params['addonID'] = addonID

        dlg = BrowseDialog(params)
        dlg.doModal()
        option = dlg.option
        del dlg

        return option
    else:
        #return 'JUST_PLAY'
        return 'PLAY'