# -*- coding: utf-8 -*-

import sys
import urlparse
from tikiscrapers.modules import control

params = dict(urlparse.parse_qsl(sys.argv[2].replace('?', '')))
mode = params.get('mode')

def ModuleChoice():
    from tikiscrapers import providerSources
    sourceList = sorted(providerSources())
    control.idle()
    select = control.selectDialog([i for i in sourceList])
    if select == -1:
        control.openSettings('0.1')
        return
    module_choice = sourceList[select]
    control.setSetting('module.provider', module_choice)
    control.openSettings('0.1')

def enableDisableScrapers(folder, open_id):
    from tikiscrapers import scrapersStatus
    enabled, disabled = scrapersStatus(folder)
    all_sources = sorted(enabled + disabled)
    preselect = [all_sources.index(i) for i in enabled]
    control.idle()
    chosen = control.multiSelectDialog('Enable/Disable Scrapers', [i.upper() for i in all_sources], function_list=all_sources, preselect=preselect)
    if not chosen:
        return control.openSettings(open_id)
    for i in all_sources:
        if i in chosen:
            control.setSetting('provider.' + i, 'true')
        else:
            control.setSetting('provider.' + i, 'false')
    control.openSettings(open_id)

def toggleAll(sourceList, setting, open_id=None):
    for i in sourceList:
        source_setting = 'provider.' + i
        control.setSetting(source_setting, setting)
    if open_id: control.openSettings(open_id)

def clearSettings():
    if not control.yesnoDialog('Are You Sure?', 'Tiki Scrapers will Clear Your Settings File.', ''):
        return control.openSettings('5.4')
    import os
    addon_data = control.dataPath
    files = control.listDir(addon_data)[1]
    for file in files:
        control.logger('file', file)
        if file == 'settings.xml':
            settings_file = os.path.join(addon_data, file)
            break
        else: pass
    new_settings_file = control.openFile(settings_file, 'w')
    content = '<settings version="2">\n</settings>'
    new_settings_file.write(content)
    new_settings_file.close
    control.infoDialog('Tiki Scrapers Settings Cleared')
    control.openSettings('5.4')


################################################################

if mode == "TikiScraperSettings":
    control.openSettings('0.0')

elif mode == "ModuleChoice":
    ModuleChoice()

elif mode == "toggleAll":
    from tikiscrapers import scraperNames
    sourcelist = scraperNames(params['folder'])
    toggleAll(sourcelist, params['setting'], params['open_id'])

elif mode == "enableDisableScrapers":
    enableDisableScrapers(params['folder'], params['open_id'])
    
elif mode == 'activateExternalscrapers':
    from tikiscrapers.modules.external_import import ExternalImporter
    ExternalImporter().importExternal()
    
elif mode == 'removeExternalscrapers':
    from tikiscrapers.modules.external_import import ExternalImporter
    ExternalImporter().removeExternal()
    
elif mode == 'clearProviderCache':
    from tikiscrapers import deleteProviderCache
    action = deleteProviderCache()
    if action == 'success': control.infoDialog('Tiki Scrapers Results Cleared')
    elif action == 'failure': control.infoDialog('Error Clearing Results Cache')
    control.openSettings('5.1')

elif mode == 'clearSettings':
    clearSettings()
