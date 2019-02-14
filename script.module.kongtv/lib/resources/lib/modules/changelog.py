# -*- coding: UTF-8 -*-

def get():

		import xbmc,xbmcgui,xbmcaddon,xbmcvfs,os
		addonInfo = xbmcaddon.Addon().getAddonInfo
		addonPath = xbmc.translatePath(addonInfo('path'))
		changelogfile = os.path.join(addonPath, 'changelog.txt')
		r = open(changelogfile)
		text = r.read()

		id = 10147
		xbmc.executebuiltin('ActivateWindow(%d)' % id)
		xbmc.sleep(500)
		win = xbmcgui.Window(id)
		retry = 50
		while (retry > 0):
			try:
				xbmc.sleep(10)
				retry -= 1
				win.getControl(1).setLabel('KongTv  v%s' %(xbmcaddon.Addon().getAddonInfo('version')))
				win.getControl(5).setText(text)
				return
			except:
				pass


