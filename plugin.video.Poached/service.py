# -*- coding: utf-8 -*-

"""
    Poached Addon

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
"""
from resources.lib.modules import log_utils
from resources.lib.modules import control

control.execute('RunPlugin(plugin://%s)' % control.get_plugin_url({'action': 'service'}))

try:
    ModuleVersion = control.addon('script.module.Poached').getAddonInfo('version')
    AddonVersion = control.addon('plugin.video.Poached').getAddonInfo('version')
    # RepoVersion = control.addon('repository.eggman').getAddonInfo('version')

    log_utils.log('######################### Poached ############################', log_utils.LOGNOTICE)
    log_utils.log('####### Current Poached Version Report ######################', log_utils.LOGNOTICE)
    log_utils.log('### Poached Plugin Version: %s ###' % str(AddonVersion), log_utils.LOGNOTICE)
    log_utils.log('### Poached Script Version: %s ###' % str(ModuleVersion), log_utils.LOGNOTICE)
    # log_utils.log('### Eggman Repository Version: %s ###' % str(RepoVersion), log_utils.LOGNOTICE)
    log_utils.log('###############################################################', log_utils.LOGNOTICE)
except:
    log_utils.log('######################### Poached ############################', log_utils.LOGNOTICE)
    log_utils.log('####### Current Poached Versions Report ######################', log_utils.LOGNOTICE)
    log_utils.log('### Error Getting Poached Versions - No Help Will Be Given As This Is Not An Offcial Poached Install. ###', log_utils.LOGNOTICE)
    log_utils.log('###############################################################', log_utils.LOGNOTICE)
