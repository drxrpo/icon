# -*- coding: utf-8 -*-
#
# Copyright (C) 2014 Sean Poyser and Richard Dean (write2dixie@gmail.com)
#
#      Modified for FTV Guide (09/2014 onwards)
#      by Thomas Geppert [bluezed] - bluezed.apps@gmail.com
#
#      Modified for Vader TV Guide (2016)
#      by primaeval - primaeval.dev@gmail.com
#
# This Program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2, or (at your option)
# any later version.
#
# This Program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with XBMC; see the file COPYING. If not, write to
# the Free Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.
# http://www.gnu.org/copyleft/gpl.html
#

import os
import xbmc
import xbmcgui
import xbmcaddon
import xbmcvfs


def deleteDB():
    try:
        xbmc.log("[script.tvguide.Vader] Deleting database...", xbmc.LOGDEBUG)
        dbPath = xbmc.translatePath(xbmcaddon.Addon(id = 'script.tvguide.Vader').getAddonInfo('profile'))
        dbPath = os.path.join(dbPath, 'source.db')

        delete_file(dbPath)

        passed = not os.path.exists(dbPath)

        if passed:
            xbmc.log("[script.tvguide.Vader] Deleting database...PASSED", xbmc.LOGDEBUG)
        else:
            xbmc.log("[script.tvguide.Vader] Deleting database...FAILED", xbmc.LOGDEBUG)

        return passed

    except Exception, e:
        xbmc.log('[script.tvguide.Vader] Deleting database...EXCEPTION', xbmc.LOGDEBUG)
        return False

def delete_file(filename):
    tries = 10
    while os.path.exists(filename) and tries > 0:
        try:
            os.remove(filename)
            break
        except:
            tries -= 1

if __name__ == '__main__':
    if len(sys.argv) > 1:
        mode = int(sys.argv[1])

        if mode in [1,2,6]:
            if deleteDB():
                d = xbmcgui.Dialog()
                d.ok('[COLOR red]TV[/COLOR] [COLOR white]Guide[/COLOR]', '[COLOR green]Reset has been Successful[/COLOR]', 'Please now restart [COLOR red]TV[/COLOR] [COLOR white]Guide[/COLOR]')
            else:
                d = xbmcgui.Dialog()
                d.ok('[COLOR red]TV[/COLOR] [COLOR white]Guide[/COLOR]', 'Failed to delete database.', 'Database may be locked,', 'Restart Kodi and Try Again')
        elif mode in [5]:
            if deleteDB():
                d = xbmcgui.Dialog()
                d.ok('[COLOR red]TV[/COLOR] [COLOR white]Guide[/COLOR]', '[COLOR green]All DONE[/COLOR]', 'All addons.ini files have been deleted')
            else:
                d = xbmcgui.Dialog()
                d.ok('[COLOR red]TV[/COLOR] [COLOR white]Guide[/COLOR]', '[COLOR green]All DONE[/COLOR]', 'Addons.ini files have been deleted')
        elif mode in [7,8]:
            if deleteDB():
                d = xbmcgui.Dialog()
                d.ok('[COLOR red]TV[/COLOR] [COLOR white]Guide[/COLOR]', '[COLOR green]Category Order Changed[/COLOR]', 'Please Click [COLOR red]Cancel[/COLOR] in settings to complete')
            else:
                d = xbmcgui.Dialog()
                d.ok('[COLOR red]TV[/COLOR] [COLOR white]Guide[/COLOR]', '[COLOR green]Category Order Changed[/COLOR]', 'Please Click [COLOR red]Cancel[/COLOR] in settings to complete')	
        if mode == 1:
            xbmcvfs.delete('special://profile/addon_data/script.tvguide.Vader/guide.xml')
            xbmcvfs.delete('special://profile/addon_data/script.tvguide.Vader/guide.xml.md5')
        if mode == 2:
            xbmcvfs.delete('special://profile/addon_data/script.tvguide.Vader/addons.ini')
            xbmcvfs.delete('special://profile/addon_data/script.tvguide.Vader/addons.ini.local')
            xbmcvfs.delete('special://profile/addon_data/script.tvguide.Vader/category_count.ini')
            xbmcvfs.delete('special://profile/addon_data/script.tvguide.Vader/categories.ini')
            xbmcvfs.delete('special://profile/addon_data/script.tvguide.Vader/custom_stream_urls.ini')
            xbmcvfs.delete('special://profile/addon_data/script.tvguide.Vader/channel_id_title.ini')
            xbmcvfs.delete('special://profile/addon_data/script.tvguide.Vader/mapping.ini')
            xbmcvfs.delete('special://profile/addon_data/script.tvguide.Vader/custom_stream_urls_autosave.ini')
            xbmcvfs.delete('special://profile/addon_data/script.tvguide.Vader/icons.ini')
            xbmcvfs.delete('special://profile/addon_data/script.tvguide.Vader/folders.list')
            xbmcvfs.delete('special://profile/addon_data/script.tvguide.Vader/tvdb.pickle')
            xbmcvfs.delete('special://profile/addon_data/script.tvguide.Vader/tvdb_banners.pickle')
            xbmcvfs.delete('special://profile/addon_data/script.tvguide.Vader/settings.xml')
            xbmcvfs.delete('special://profile/addon_data/script.tvguide.Vader/guide.xml')
            xbmcvfs.delete('special://profile/addon_data/script.tvguide.Vader/guide.xml.md5')
            xbmcvfs.delete('special://profile/addon_data/script.tvguide.Vader/subscriptions.ini')
            xbmcvfs.delete('special://profile/addon_data/script.tvguide.Vader/channels.ini')
            xbmcvfs.delete('special://profile/addon_data/script.tvguide.Vader/synopsis_search.list')
            xbmcvfs.delete('special://profile/addon_data/script.tvguide.Vader/title_search.list')
            dirs, files = xbmcvfs.listdir('special://profile/addon_data/script.tvguide.Vader/')
            for f in files:
                xbmcvfs.delete('special://profile/addon_data/script.tvguide.Vader/%s' % f)				
        if mode == 3:
            xbmcvfs.delete('special://profile/addon_data/script.tvguide.Vader/tvdb.pickle')
            xbmcvfs.delete('special://profile/addon_data/script.tvguide.Vader/tvdb_banners.pickle')
        if mode in [2,4]:
            dirs, files = xbmcvfs.listdir('special://profile/addon_data/script.tvguide.Vader/logos')
            for f in files:
                xbmcvfs.delete('special://profile/addon_data/script.tvguide.Vader/logos/%s' % f)
        if mode == 5:
            xbmcvfs.delete('special://profile/addon_data/script.tvguide.Vader/addons.ini')
            xbmcvfs.delete('special://profile/addon_data/script.tvguide.Vader/addons.ini.local')
            xbmcvfs.delete('special://profile/addons_custom.ini')			
        if mode == 6:
            xbmcvfs.delete('special://profile/addon_data/script.tvguide.Vader/synopsis_search.list')
            xbmcvfs.delete('special://profile/addon_data/script.tvguide.Vader/title_search.list')
        if mode == 7:
            xbmcvfs.delete('special://home/userdata/addon_data/script.tvguide.Vader/settings.xml')
        if mode == 8:
            xbmcvfs.copy('special://home/addons/script.tvguide.Vader/resources/cat.xml','special://profile/addon_data/script.tvguide.Vader/settings.xml')
