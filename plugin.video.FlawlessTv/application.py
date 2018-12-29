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

import main
functionality = main

import xbmc
import xbmcgui

import os
import threading
import datetime
import json

import favourite

import iptv_utils


ACTION_SELECT     = 7
ACTION_PARENT_DIR = 9
ACTION_BACK       = 92
ACTION_LCLICK     = 100
ACTION_RCLICK     = 101
ACTION_CONTEXT    = 117

ESC = 61467

MAINLIST   = 49
SECONDLIST = 69
NOWNEXT    = 79
WIDELIST   = 89
LATESTLIST = 99
SHOWSLIST  = 109
ALLLISTS   = [MAINLIST, SECONDLIST, NOWNEXT, WIDELIST, LATESTLIST, SHOWSLIST]

VIDEOWINDOW = 3010  
LISTBACK    = -999

GETTEXT = iptv_utils.GETTEXT


def DialogOK(line1, line2='', line3=''):
    iptv_utils.DialogOK(str(line1), str(line2), str(line3))


def Log(text):
    iptv_utils.log(text, True)

def log(text):
    iptv_utils.log(text, True)



class Application(xbmcgui.WindowXML):
    def __new__(cls, addonID):
        skin = iptv_utils.GetSetting('SKIN')
        if not skin:
            skin = 'Default'
        path = os.path.join(iptv_utils.GetAddonInfo('path', addonID), 'resources', 'skins', skin)
        return super(Application, cls).__new__(cls, 'main.xml', path)

    def __init__(self, addonID):        
        super(Application, self).__init__()

        #in case it was set whilst addon not running
        xbmcgui.Window(10000).clearProperty('FL_RL')

        self.ADDONID         = addonID
        self.properties      = {}        
        self.lists           = [] 
        self.start           = None           
        self.param           = None
        self.params          = {}
        self.secondIndex     = {}
        self.context         = False
        self.busy            = None
        self.faves           = self.getFavourites()
        self.showBack        = False
        self.timer           = None
        self.counter         = 0
        self.activeList      = MAINLIST
        self.secondList      = SECONDLIST
        self.twoListMode     = False
        self.twoListUpdate   = None
        self.listPosition    = -2
        self.gotLatest       = False
        self.cache           = {}
        self.inOnAction      = False


    def onInit(self):
        self.refreshLists()
        self.clearList()

        if self.start:
            self.lists.append([]) 
            start      = self.start
            self.start = None
            self.onParams(start)
            self.twoListUpdate = datetime.datetime.now() + datetime.timedelta(seconds=0.0)
            return
            
        if len(self.lists) < 1:
            if self.param is None:
                self.param = 'init'
            self.onParams(self.param)
            xbmc.sleep(100)
            self.setListItem(MAINLIST, functionality.INITIAL_ITEM)
            self.twoListUpdate = datetime.datetime.now() + datetime.timedelta(seconds=0.0)
            return

        #add new list so we can just call onBack        
        self.newList()
        self.onBack()


    def setListItem(self, list, item):
        try:
            if xbmc.getCondVisibility('Control.IsVisible(%d)' % (list-1)):
                ctrl = self.getControl(list)
                self.setFocus(ctrl)
                ctrl.selectItem(item)
                while ctrl.getSelectedPosition() != item:
                    xbmc.sleep(100)
        except:
            pass

        
    def run(self, param=''):
        self.start = param

        if self.start and self.start.startswith('_Playable'):
            #this will be a Playable item called from Favourites menu
            self.newList()
            self.windowed = False
            xbmcgui.Window(10000).clearProperty('FL_R')
            self.onParams(self.start.replace('_Playable', ''), isFolder=False)
            self.close()
            return

        self.doModal()

              
    def close(self):
        self.stopTimer()
        xbmcgui.WindowXML.close(self)


    def resetTimer(self):
        try:
            self.stopTimer()
            if not xbmcgui.Window(10000).getProperty('FL_R'):
                return
            self.timer = threading.Timer(0.5, self.onTimer) 
            self.timer.start()
        except Exception, e:
            pass
        

    def stopTimer(self):
        if not self.timer:
            return

        try:
            self.timer.cancel()
            del self.timer
            self.timer = None
        except Exception as e:
            pass


    def hasExpired(self, when):
        if when is None:
            return False

        return when - datetime.datetime.now() < datetime.timedelta(seconds=0)


    def hasListMoved(self):
        if not self.hasExpired(self.twoListUpdate):
            return False

        posn = self.getControl(MAINLIST).getSelectedPosition()

        if self.listPosition == -1:
            self.listPosition = posn

        if self.listPosition == posn:
            return False

        self.listPosition = posn

        self.params[self.param] = posn

        return True



    def onTimer(self):
        self.counter += 1

        self.updateTwoListMode()
     
        if xbmcgui.Window(10000).getProperty('FL_RL') == 'true':
            self.doRelaunch()
            return

        self.resetTimer()


    def doRefresh(self):
        self.newList()
        self.onBack()


    def doRelaunch(self):
        self.stopTimer()
        xbmcgui.Window(10000).clearProperty('FL_RL')
        iptv_utils.Launch()
        self.close()


    def onFocus(self, controlId):
        #self.focusID = controlId
        pass
        

    def openSettings(self, addonID):
        functionality.ShowSettings(addonID)


    def onAction(self, action):
        if self.inOnAction:
            return

        self.inOnAction = True
        self.stopTimer()
        self._onAction(action)
        self.resetTimer()
        self.inOnAction = False
        

    def _onAction(self, action):
        #see here https://github.com/xbmc/xbmc/blob/master/xbmc/guilib/Key.h for the full list

        try:    id = self.getFocus().getId()
        except: id = None

        if id == self.secondList:
            self.twoListUpdate = None
        else:
            self.twoListUpdate = datetime.datetime.now() + datetime.timedelta(seconds=0.5)

        actionId = action.getId()
        buttonId = action.getButtonCode()

        if actionId != 107:
            pass
            #actionId += self.counter / 1000
            #iptv_utils.Log('onAction actionID %d' % actionId)
            #iptv_utils.Log('onAction buttonID %d' % buttonId)

        if actionId in [ACTION_CONTEXT, ACTION_RCLICK]:
            return self.onContextMenu()
            
        if actionId in [ACTION_PARENT_DIR, ACTION_BACK] or buttonId in [ESC]:
            self.clearTwoListMode()
            return self.onBack()

        select = (actionId == ACTION_SELECT) or (actionId == ACTION_LCLICK)

        if not select:
            return

        self.twoListUpdate = datetime.datetime.now() + datetime.timedelta(seconds=0)

        liz = None
        if id == self.secondList or id == LATESTLIST:
            ctrl = self.getControl(id)
            liz  = ctrl.getSelectedItem()
            self.secondIndex[id] = ctrl.getSelectedPosition()
        
        if id == self.activeList:
            liz = self.getSelectedItem()

        if liz:
            self.listPosition = -2
            param      = liz.getProperty('Param')
            image      = liz.getProperty('Image')
            mode       = int(liz.getProperty('Mode'))
            altMode    = int(liz.getProperty('AltMode'))
            isFolder   = liz.getProperty('IsFolder')   == 'true'
            isPlayable = liz.getProperty('IsPlayable') == 'true'
            
            if mode == LISTBACK:
                return self.onBack()

            if mode == functionality.BROWSE_VOD:
                self.twoListUpdate = None
                
            if int(liz.getProperty('ListID')) != MAINLIST:
                if altMode:
                    param = 'mode=%d' % altMode
                    isFolder = True

                elif not functionality.isSearchMode(param):
                    return

            if param:
                self.params[self.param] = self.getControl(MAINLIST).getSelectedPosition()
                self.param = param

                #self.stopTimer()
                self.onParams(param, isFolder)

                #if mode == functionality.BROWSE_VOD:
                #    self.twoListUpdate = None
                    
                #self.resetTimer()

        if id == VIDEOWINDOW:   
            xbmc.executebuiltin('Action(fullscreen)')  
        
                                 
    def onClick(self, controlId):        
        #iptv_utils.Log('onClick %d' % controlId)        
        pass


    def clearTwoListMode(self):
        try:
            self.getControl(self.secondList).reset()
            self.twoListUpdate = None
            #self.listPosition  = -1
        except:
            pass


    def onBack(self): 
        self.refreshLists()

        try:    self.lists.pop()
        except: pass


        if len(self.lists) == 0:
            self.close()
            return

        self.list = self.lists[-1]

        if len(self.list) == 0:
            #addon must have originally been started with a
            #parameter therefore reset to initial position
            self.lists = []
            self.onInit()
            return

        param = self.list[0]
            
        if hasattr(functionality, 'onBack'):
           functionality.onBack(self, param)
           
        self.addItems(self.list)
        self.resetFocuses(param)

        self.checkLatest()


    def resetFocuses(self, param):
        if param not in self.params:
            return

        try:
            index = self.params[param]
            self.param = param
            self.setListItem(MAINLIST, index)
            self.updateTwoListMode(liz=None, force=True) 
            for id in self.secondIndex:
                index = self.secondIndex[id]
                self.setListItem(id, index)
        except:
            pass


    def getFavourites(self):
        faves = str(favourite.getFavourites())
        return faves


    def updateFavourite(self, liz, add=True):
        name       = liz.getLabel()
        param      = liz.getProperty('Param')
        thumb      = liz.getProperty('Image')
        isPlayable = liz.getProperty('IsPlayable') == 'true'

        if isPlayable:
            param = '_Playable' + param
 
        cmd = 'RunScript(%s,%s)' % (self.ADDONID, param)

        if add:
            favourite.add(name, cmd, thumb)
        else:
            favourite.remove(name, cmd, thumb)

        self.faves = self.getFavourites()

        return True

                        
    def onContextMenu(self):
        if self.context:           
            return

        try:
            id     = self.getFocus().getId()
            ctrl   = self.getControl(id)
            liz    = ctrl.getSelectedItem()
            menu   = liz.getProperty('ContextMenu')
            #prefix = 'Container(%d).' % int(xbmc.getInfoLabel('System.CurrentControlId'))
            #prefix = 'Container(%d).' % id
            #menu   = xbmc.getInfoLabel('%sListItem.Property(ContextMenu)' % prefix)
            menu   = json.loads(menu)
        except Exception as e:
            iptv_utils.DialogOK(e)
            return

        #fave = xbmc.getInfoLabel('%sListItem.Property(Fave)' % prefix)
        fave = liz.getProperty('Fave')
        if fave == 'true':
            #param = xbmc.getInfoLabel('%sListItem.Property(Param)' % prefix)
            param = liz.getProperty('Param')
            #iptv_utils.DialogOK(param)
            #xbmc.sleep(500)
            if param in self.faves:
                label  = GETTEXT(30037)
                param  = 'STD:REMOVEFAVOURITE'
            else:
                label = GETTEXT(30036)
                param = 'STD:ADDFAVOURITE'

            menu.insert(0, [label, param])
       
        replaceItems = liz.getProperty('ReplaceItems') == 'true'
        
        if not replaceItems:
            menu = list(menu + self.getSTDMenu(liz))   

        if len(menu) < 1:
            return

        import contextmenus
        self.context = True
        params       = contextmenus.showMenu(self.ADDONID, menu, False)
        self.context = False

        if not params:
            return

        if self.trySTDMenu(params):
            return

        if params == 'STD:ADDFAVOURITE':
            return self.updateFavourite(liz, add=True)

        if params == 'STD:REMOVEFAVOURITE':
            return self.updateFavourite(liz, add=False)
           
        self.onParams(params, isFolder=False)

        self.updateTwoListMode(liz=None, force=True) 
        

    def showControl(self, id, show):
        try:    self.getControl(id).setVisible(show)
        except: pass
        
        
    def getProgress(self):
        try:    return self.busy.getControl(10)
        except: return None
        
        
    def showBusy(self):
        self.busy = xbmcgui.WindowXMLDialog('DialogBusy.xml', '')
        self.busy.show()
        progress = self.getProgress()
        if progress:
            progress.setVisible(False)        
        
        
    def closeBusy(self):    
        if self.busy:
            self.busy.close()
            self.busy = None


    def newList(self):
        self.list = []
        self.lists.append(self.list)        


    def getSelectedItem(self):
        try:
            return self.getActiveList().getSelectedItem()
        except: 
            return None


    def setControlImage(self, id, image):
        if image == None:
            return

        control = self.getControl(id)
        if not control:
            return

        if 'http' in image:
            image = image.replace(' ', '%20')

        try:    control.setImage(image)
        except: pass

            
    def clearList(self):
        #xbmcgui.WindowXML.clearList(self)  
        self.getActiveList().reset()


    def getSTDMenu(self, liz):
        std = []
        return std


    def trySTDMenu(self, params):
        if params == 'STD:SETTINGS':
            self.addonSettings()
            return True

        return False


    def addonSettings(self):
        iptv_utils.OpenSettings(focus=None, addonID=self.ADDONID)
        return True
        
        
    def setProperty(self, property, value):
        self.properties[property] = value
        #xbmcgui.Window(xbmcgui.getCurrentWindowId()).setProperty(property, value)
        xbmcgui.Window(10000).setProperty(property, value)
        
        
    def clearProperty(self, property):
        del self.properties[property]
        xbmcgui.Window(10000).clearProperty(property)        
        
        
    def clearAllProperties(self):
        for property in self.properties:
            xbmcgui.Window(10000).clearProperty(property)
            
        self.properties = {} 


    def writeListsToFile(self, text=None):
        import sfile
        file = os.path.join(iptv_utils.PROFILE, 'lists.txt')

        if text:
            sfile.append(file, '%s\n' % text)
        for list in self.lists:
            sfile.append(file, '\r\n----------------------------------------------------------------------------------\r\n')
            sfile.append(file, str(list))
            sfile.append(file, '\r\n----------------------------------------------------------------------------------\r\n')


    def removeListItem(self):
        try:    
            # first element is actually the current list we want to populate
            # therefore remove the previous one
            self.lists.pop(-2)
        except:
            pass


    def addDir(self, name, mode, url='', image=None, isFolder=True, isPlayable=False, totalItems=0, contextMenu=None, replaceItems=False, infoLabels=None, listID=None, altMode=None, fave=False):
        if image is None:
            image = ''

        if contextMenu is None:
            contextMenu = []

        #iptv_utils.log(contextMenu, True)

        if infoLabels is None:
            infoLabels = {}

        if listID is None:
            listID = MAINLIST

        item = {}
        item['Name']         = name
        item['Mode']         = mode
        item['AltMode']      = altMode if altMode else 0
        item['Url']          = url
        item['Image']        = image
        item['IsFolder']     = isFolder
        item['IsPlayable']   = isPlayable
        item['ContextMenu']  = contextMenu
        item['ReplaceItems'] = replaceItems
        item['ListID']       = listID
        item['InfoLabels']   = dict(infoLabels)
        item['Fave']         = fave 

        self.list.append(item)
        
        progress = self.getProgress()
        if not progress:
            return
            
        if totalItems == 0:
            progress.setVisible(False)
        else:
            progress.setVisible(True)
            nItems = float(len(self.list) - 1) # subtract params'
            if self.showBack:
                nItems -= 1 # subtract params' and 'back' items
            perc   = 100 * nItems / totalItems            
            progress.setPercent(perc)


    def getActiveList(self):
        return self.getControl(self.activeList)


    def refreshLists(self):
        for id in ALLLISTS:
            # subtracting one will hide the whole group
            if id == LATESTLIST:
                show = len(self.lists) <= 1

                try:
                    liz = self.getSelectedItem()
                    if liz:
                        mode = int(liz.getProperty('Mode'))
                        if mode == functionality.DOWNLOADS:
                            show = False
                except:
                    pass

                self.showControl(id-1, show)
            else:
                self.showControl(id-1, id == self.activeList)

                if id != MAINLIST:
                    try:    self.getControl(id).reset()
                    except: pass



    def checkLatest(self):
        if len(self.lists) > 1:
            return self.hideLatest()

        liz = self.getSelectedItem()
            
        if liz is None:
            return self.showLatest()

        listID = int(liz.getProperty('ListID'))
        
        showLatest = listID == MAINLIST

        if showLatest:
            return self.showLatest()

        self.hideLatest()


    def hideLatest(self):
        self.showControl(LATESTLIST-1, False)


    def showLatest(self):
        if self.gotLatest:
            return

        self.gotLatest = True

        self.refreshLists()
        self.showControl(LATESTLIST-1, True)

        params = 'mode=%d' % functionality.LATEST

        self.verifyCachedLists(params)

        if params not in self.cache:
            #if we get here then we need to get the new list
            self.list = []
            try:
                self.showBusy()
                functionality.onParams(self, params)
            except iptv_utils.EmptyListException as e:
                pass

            listItems = self.listItemsFromList(self.list)
            timeout   = 60

            self.cache[params] = [listItems, datetime.datetime.now() + datetime.timedelta(minutes=timeout)]

        listItems = self.cache[params][0]

        list = self.getControl(LATESTLIST)

        list.reset()
        list.addItems(listItems)

        self.closeBusy()


    def setActiveList(self, listID, refresh=True):
        listID = int(listID)

        if listID == self.activeList:
            return

        self.activeList = listID

        if refresh:
            self.refreshLists()


    def listItemsFromList(self, theList):
        listID = self.activeList
 
        listItems = []
        
        for item in theList:
            name         = item['Name']
            mode         = item['Mode']
            altMode      = item['AltMode']
            url          = item['Url']
            image        = item['Image']
            isFolder     = item['IsFolder']
            isPlayable   = item['IsPlayable']
            contextMenu  = item['ContextMenu']
            replaceItems = item['ReplaceItems']
            listID       = item['ListID'] 
            infoLabels   = item['InfoLabels']
            fave         = item['Fave']

            #liz = xbmcgui.ListItem(' : esaeler rof ton ,noisrev ateB'[::-1] + name, iconImage=image, thumbnailImage=image)
            liz = xbmcgui.ListItem(name, iconImage=image, thumbnailImage=image)

            liz.setProperty('UCBTitle',      '[B]%s[/B]' % name.upper())
            liz.setProperty('Mode',         str(mode))
            liz.setProperty('AltMode',      str(altMode))
            liz.setProperty('Param',        url)
            liz.setProperty('Image',        image)
            liz.setProperty('ListID',       str(listID))
            liz.setProperty('IsFolder',     'true'  if isFolder     else 'false')
            liz.setProperty('IsPlayable',   'true'  if isPlayable   else 'false')
            liz.setProperty('ReplaceItems', 'true'  if replaceItems else 'false')
            liz.setProperty('Fave',         'true'  if fave         else 'false')
            liz.setProperty('ContextMenu',   json.dumps(contextMenu))
  
            if infoLabels and (len(infoLabels) > 0):
                liz.setInfo(type='', infoLabels=infoLabels)
                #each infolabel is set as a property, this allow user-defined infoLabels
                #that can be accessed in the skin xml via: $INFO[Window.Property(USERDEFINED)]
                for item in infoLabels:     
                    liz.setProperty(item, infoLabels[item])

            listItems.append(liz)

        return listItems

        

    def addItems(self, theList): 
        #not '0' because first item in list is the params item
        listItems = self.listItemsFromList(theList[1:])
             
        self.clearList()
        self.getActiveList().addItems(listItems)

        try:    self.setFocus(self.getActiveList())
        except: pass

        if self.timer == None:
            self.resetTimer()


    def verifyCachedLists(self, params):
        if params not in self.cache:
            return

        when    = self.cache[params][1]
        expired = when - datetime.datetime.now() < datetime.timedelta(seconds=0)

        if expired:
            del self.cache[params]


    def updateTwoListMode(self, liz=None, force=False):
        self.stopTimer()
        self._updateTwoListMode(liz, force)
        self.resetTimer()


    def _updateTwoListMode(self, liz, force):
        if liz is None:
            if not self.hasListMoved():
                if not force:
                    return
                
            liz = self.getSelectedItem()
            
        if liz is None:
            return

        self.checkLatest()

        listID = int(liz.getProperty('ListID'))
        
        twoListMode = listID != MAINLIST

        if twoListMode:
            self.secondList = listID

        self.refreshLists()
        self.showControl(self.secondList-1, twoListMode)

        if not twoListMode:
            self.clearTwoListMode()
            if not force:
                return
            
        params = liz.getProperty('Param')

        self.verifyCachedLists(params)

        if params not in self.cache:
            #if we get here then we need to get the new list
            self.list = []
            try:
                if not functionality.isSearchMode(params):
                    self.showBusy()
                    functionality.onParams(self, params)
            except iptv_utils.EmptyListException as e:
                pass

            listItems = self.listItemsFromList(self.list)
            timeout   = 60
            # special case - do not cache Downloads (in case user deletes)
            download = '?mode=%d&' % functionality.DOWNLOADS
            if download in params:
                timeout = -1

            self.cache[params] = [listItems, datetime.datetime.now() + datetime.timedelta(minutes=timeout)]

        listItems = self.cache[params][0]

        list = self.getControl(self.secondList)
        list.addItems(listItems)

        self.closeBusy()


    def handleSearchMode(self, params):
        self.list = []
        try:
            self.showBusy()
            functionality.onParams(self, params)
        except iptv_utils.EmptyListException as e:
            if not e.text:
                self.closeBusy()
                return
            iptv_utils.DialogOK(e.text)
       
        liz    = self.getSelectedItem()
        listID = int(liz.getProperty('ListID'))
        
        self.showControl(self.secondList-1, True)

        listItems = self.listItemsFromList(self.list)
        self.cache[params] = [listItems, datetime.datetime.now() + datetime.timedelta(days=14)]

        listItems = self.cache[params][0]

        list = self.getControl(listID)
        list.reset()
        list.addItems(listItems)
        self.closeBusy()
         

    def onParams(self, params, isFolder=True):
        try:
            id      = self.getFocus().getId()
            ctrl    = self.getControl(id)
            refocus = ctrl.getSelectedPosition()
        except:
            refocus = None

        if isFolder:
            refocus = None

            if functionality.isSearchMode(params):
                return self.handleSearchMode(params)
                
            self.newList() 
            #store params as first item in list
            self.list.append(params)
            if self.showBack:
                #add the '..' item
                self.addDir('Previous menu', LISTBACK, image='DefaultFolderBack.png', contextMenu=[('Add-on settings', 'STD:SETTINGS')], replaceItems=True)

            self.showBusy()

        #call into the "real" addon

        emptyList = False
        try:    
            functionality.onParams(self, params)
        except iptv_utils.EmptyListException as e:
            emptyList = True
            if isFolder and e.text:
                iptv_utils.DialogOK(e.text)

        self.closeBusy()

        if isFolder:
            self.addItems(self.list)
            if emptyList and len(self.lists) > 1: #don't go back from the first list
                self.onBack()
        
        if refocus:
            self.setListItem(ctrl, refocus)

        try:    self.checkLatest()
        except: pass


    def setResolvedUrl(self, url, success=True, listItem=None, windowed=False, subtitles=''):
        if success and len(url) > 0:
            if not listItem:
                listItem = xbmcgui.ListItem(url)
            pl = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)

            pl.clear()
            pl.add(url, listItem)
            
            xbmc.Player().play(pl, windowed=False)
            if subtitles:
                xbmc.Player().setSubtitles(subtitles)



    def containerRefresh(self):
        self.lists.pop()
        self.onParams(self.list[0], True)
