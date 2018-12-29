import xbmcaddon, base64

Decode = base64.decodestring
MainBase = (Decode('aHR0cDovL3N0ZXB0b2VzcGxhY2UubmV0L2hvbWUueG1s'))
addon = xbmcaddon.Addon('plugin.video.monstermunch')