#!/usr/bin/python
# -*- coding: utf-8 -*-
"""

    Copyright (C) 2018

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

    -------------------------------------------------------------

    Version:
        2018-05-19:
            Updated documentation in Header
            Added ability to disable service after updating API Keys (reduces load on Kodi startup)
            Removed old stuff

    Variables To Change:
        current_version             = Increase this by one each time you need to update the root_xml or api keys
        enable_notifications        = Set this to False to not notify the user when the API keys are updated
        disable_after_update        = Set this to True to disable this service after it updates the userdata
                                        settings until next install/update
        updated_root_xml            = Same as your settings.xml
        updated_tvdb_api_key        = Same as your settings.xml
        updated_tmdb_api_key        = Same as your settings.xml
        updated_trakt_api_id        = Same as your settings.xml
        updated_trakt_api_secret    = Same as your settings.xml
        updated_TRAKT_ACCESS_TOKEN  = Same as your settings.xml
        updated_TRAKT_EXPIRES_AT    = Same as your settings.xml
        updated_TRAKT_REFRESH_TOKEN = Same as your settings.xml
        updated_lastfm_api_key      = Same as your settings.xml
        updated_lastfm_secret       = Same as your settings.xml
        updated_search_db_location  = Same as your settings.xml


    Usage:
        Set the current_version to a number higher than existing (if any) 'update_ver'
            setting in your addon. If this is the first time using this, you can leave
            current_version at 1.
        When the service runs, it checks if the current_version below is greater than
            the 'update_ver' setting. If it is, it updates the settings for your addon
            in userdata to the updated entries you entered below.
        If it is not greater (meaning, current same as updated_ver) then it just ignores

        If you want to let the end user know you updated something, set the
            "enable_notification" to True, otherwise set it to False


"""

import os,re,traceback
import xbmc,xbmcaddon,xbmcgui


addon_id   = xbmcaddon.Addon().getAddonInfo('id')
addon_name = xbmcaddon.Addon().getAddonInfo('name')
addon_icon = xbmcaddon.Addon().getAddonInfo('icon')
ownAddon   = xbmcaddon.Addon(id=addon_id)

addons_root= xbmc.translatePath('special://home/addons').decode('utf-8')
addon_path = os.path.join(addons_root, addon_id)

#######################################################################
# My New Settings
current_version             = '0'
enable_notification         = True
disable_after_update        = True
updated_root_xml            = 'file://main.xml'
updated_tvdb_api_key        = ''
updated_tmdb_api_key        = ''
updated_trakt_api_id        = ''
updated_trakt_api_secret    = ''
updated_TRAKT_ACCESS_TOKEN  = ''
updated_TRAKT_EXPIRES_AT    = ''
updated_TRAKT_REFRESH_TOKEN = ''
updated_lastfm_api_key      = ''
updated_lastfm_secret       = ''
updated_search_db_location  = ''
#######################################################################


def main():
    try:
        update_version = ownAddon.getSetting('update_ver')
        if update_version == '':
            update_version = '0'
        if int(current_version) > int(update_version):
            ownAddon.setSetting('root_xml', updated_root_xml)
            ownAddon.setSetting('tvdb_api_key', updated_tvdb_api_key)
            ownAddon.setSetting('tmdb_api_key', updated_tmdb_api_key)
            ownAddon.setSetting('trakt_api_client_id',
                                updated_trakt_api_id)
            ownAddon.setSetting('trakt_api_client_secret',
                                updated_trakt_api_secret)
            ownAddon.setSetting('TRAKT_ACCESS_TOKEN', '')
            ownAddon.setSetting('TRAKT_EXPIRES_AT', '')
            ownAddon.setSetting('TRAKT_REFRESH_TOKEN', '')
            ownAddon.setSetting('lastfm_api_key',
                                updated_lastfm_api_key)
            ownAddon.setSetting('lastfm_secret', updated_lastfm_secret)
            ownAddon.setSetting('search_db_location',
                                updated_search_db_location)

            ownAddon.setSetting('update_ver', current_version)

            if enable_notification:
                xbmcgui.Dialog().notification(addon_name,
                        'Updated API keys', addon_icon)
    except:
        pass
    if disable_after_update:
        disable_this()


def disable_this():
    addonxml_path = os.path.join(addon_path, 'addon.xml')
    xml_content = openfile(addonxml_path)
    if re.search('point="xbmc.service"', xml_content):
        xml_content = xml_content.replace('point="xbmc.service"',
                'point="xbmc.jen"')
        savefile(addonxml_path, xml_content)
    else:
        pass


def openfile(path_to_the_file):
    try:
        fh = open(path_to_the_file, 'rb')
        contents = fh.read()
        fh.close()
        return contents
    except:
        print('Wont open: %s' % (filename))
        return None


def savefile(path_to_the_file, content):
    try:
        fh = open(path_to_the_file, 'wb')
        fh.write(content)
        fh.close()
    except:
        print('Wont save: %s' % (filename))


if __name__ == '__main__':
    main()