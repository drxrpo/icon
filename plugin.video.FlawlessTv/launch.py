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

import iptv_utils


if iptv_utils.API == 2:
    import iptv2 as iptv
else:
    import iptv

def _checkCreds(dialogOnly=False):
    if iptv_utils.GetSetting('DEBUG') == 'true':
        return True
    try:
        info = iptv.GetAccountInfo(maxSec=0, dialogOnly=dialogOnly)['user_info']
        return info['auth'] == 1
    except Exception as e:
        pass

    return False


# exits if no creds
def checkCreds_():
    return _checkCreds()


# loops if no creds
def checkCreds():
    creds = _checkCreds()

    retry = 4

    while not creds and retry > 0:
        retry -= 1
        creds = _checkCreds(retry < 1) 

    return creds


def main(addonID, param=None):
    try:
        iptv_utils.CheckSettings()  
        if not checkCreds():
            return

        import application
        app = application.Application(addonID)
        xbmcgui.Window(10000).setProperty('FL_R', 'true')
        app.run(param)
        xbmcgui.Window(10000).clearProperty('FL_R')
        del app
    except Exception, e:
        iptv_utils.log('******************* ERROR IN MAIN *******************')
        iptv_utils.log(str(e))
        raise


if __name__ == '__main__':
    addonID  = sys.argv[1]

    while xbmc.getCondVisibility('Window.IsActive(okdialog)'):
        xbmc.sleep(100)
   
    if len(sys.argv) == 2:
        main(addonID)
    else:
        main(addonID, sys.argv[2])