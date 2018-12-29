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

import os
import xbmc
import re

import sfile

def add(name, cmd, thumb = None):
    if thumb == None:
        thumb = ''  
  
    uName = name.upper()

    faves = getFavourites()
    found = False

    writeFile(faves, 'favourites.bak') 

    newEntry = 'name="%s" thumb="%s">%s' % (name, thumb, cmd)

    for i, fave in enumerate(faves):
        try:
            name = re.compile('name="(.+?)"').findall(fave)[0]
        
            if name.upper() == uName:            
                found    = True            
                faves[i] = newEntry
                break
        except:
            pass

    if not found:
        faves.append(newEntry)

    writeFile(faves)



def remove(name, cmd, thumb=None):
    if thumb == None:
        thumb = ''  
  
    uName = name.upper()

    faves    = getFavourites()
    newFaves = []

    writeFile(faves, 'favourites.bak') 

    newEntry = 'name="%s" thumb="%s">%s' % (name, thumb, cmd)

    for fave in faves:
        try:
            name = re.compile('name="(.+?)"').findall(fave)[0]
        
            if name.upper() == uName:
                continue

            newFaves.append(fave)
        except:
            pass

    writeFile(newFaves)


    
def getFavourites():
    xml  = '<favourites></favourites>'
    path = 'special://profile/favourites.xml'

    if sfile.exists(path):  
        xml = sfile.read(path)

    return re.compile('<favourite(.+?)</favourite>').findall(xml)


def writeFile(faves, filename = 'favourites.xml'):
    path = 'special://profile/%s' % filename
    f    = sfile.file(path, 'w')

    f.write('<favourites>')
    for fave in faves:
        f.write('\n\t<favourite ')
        f.write(fave)
        f.write('</favourite>')
    f.write('\n</favourites>')            
    f.close()