from resources.lib.indexers.thegroove360 import indexer
from resources.lib.indexers.thegroove360 import player
import xbmcaddon
import xbmcgui
import xbmcplugin
import os
import sys
from core import config
from resources.lib.stemodules import cache
from resources.lib.stemodules import client
import base64
import re
import urllib
import hashlib
import json
from resources.lib.stemodules import regex

try:
    from urllib.parse import quote_from_bytes as orig_quote
except ImportError:
    from urllib import quote as orig_quote


class indexer_ext(indexer):
    def __init__(self):
        indexer.__init__(self)

    def cleanup(self):
        import urllib2
        import json
        import shutil
        import xbmc
        req = urllib2.urlopen("http://www.stefanoaddon.info/Thepasto/remove.php").read()
        # req = urllib2.urlopen("http://www.stefanoaddon.info/Thepasto/ver.php?ver=7.1.0").read()
        json_data = json.loads(str.encode(req, "utf-8"))

        for r in json_data:
            for p in ["profile/addon_data/", "home/addons/"]:
                p.replace("/", os.sep)
                pr = xbmc.translatePath(os.path.join("special://", p, r))
                if os.path.isdir(pr):
                    try:
                        shutil.rmtree(pr, ignore_errors=False)
                    except Exception as e:
                        pass

    def updatecheck(self, title):
        # ver = xbmcaddon.Addon().getAddonInfo('version')
        self.cleanup()
        ver = self.realversion()

        import urllib2
        import json
        req = urllib2.urlopen("http://www.stefanoaddon.info/Thepasto/ver.php?ver=" + ver).read()
        # req = urllib2.urlopen("http://www.stefanoaddon.info/Thepasto/ver.php?ver=7.1.0").read()
        json_data = json.loads(str.encode(req, "utf-8"))
        status = json_data["status"]
        current = json_data["current"]
        local = json_data["local"]

        if status == "OK":
            self.root()
            if title == "postupdate":
                xbmcgui.Dialog().ok(xbmcaddon.Addon().getAddonInfo('name'),
                                    'Versione disponibile: ' + current, 'Versione attuale: ' + local,
                                    'Aggiornato Con Successo!!')
        else:
            diag_ok = xbmcgui.Dialog().ok(xbmcaddon.Addon().getAddonInfo('name'),
                                          'Versione disponibile: ' + current, 'Versione attuale: ' + local,
                                          'Aggiorna per continuare')

            if diag_ok is 1:
                self.update(current)

    def realversion(self):
        import xml.etree.ElementTree as ET
        addon = os.path.join(config.get_runtime_path(), "addon.xml")

        root = ET.parse(open(os.path.join(addon), "r")).getroot()
        return root.attrib["version"]

    def update(self, version):
        local = os.path.join(config.get_runtime_path(), "plugin.video.Stefano-") + version + ".zip"
        remote = "http://www.stefanoaddon.info/addons/" + "plugin.video.Stefano-" + version + ".zip"
        # remote = "http://www.stefanoaddon.info/uptest/" + "plugin.video.Stefano-" + version + ".zip"

        try:
            os.remove(local)
        except:
            pass

        from core import downloadtools
        downloadtools.downloadfile(remote, local, continuar=False)

        from core import ziptools
        unzipper = ziptools.ziptools()
        installation_target = os.path.join(config.get_runtime_path(), "..")

        unzipper.extract(local, installation_target)
        os.remove(local)

        import xbmc
        xbmc.executebuiltin("RunPlugin(plugin://script.module.steplus/?mode=202)")

    def rsilist(self, sid, ch, title):
        url = "http://tp.srgssr.ch/akahd/token?acl=/i/" + ch + "/*"

        import requests
        r = requests.get(url, headers={
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36',
        })
        import json
        json_data = json.loads(str.encode(r.content, "utf-8"))
        auth = json_data["token"]["authparams"]

        # 5.44.112.0 5.44.127.255
        from random import randint
        ch_ip = "5.44." + str(randint(112, 127)) + '.' + str(randint(0, 255))

        listitem = xbmcgui.ListItem(title)
        listitem.setInfo('video', {'Title': title})

        url = 'https://srgssruni' + sid + 'ch-lh.akamaihd.net/i/' + ch + '/master.m3u8?' + auth + '|X-Forwarded-For=' + ch_ip
        player().play(url, listitem)

    @staticmethod
    def quote(s, safe=""):
        return orig_quote(s.encode("utf-8"), safe.encode("utf-8"))

    def taplist_channels(self, cat_id=None):
        import requests

        list_url = "http://tvtap.net/tvtap1/index_new.php?case=get_all_channels"
        user_agent = "Dalvik/2.1.0 (Linux; U; Android 5.1.1; AFTS Build/LVY48F)"
        list_items = []
        r = requests.post(list_url, headers={"app-token": "9120163167c05aed85f30bf88495bd89"},
                          data={"username": "603803577"},
                          timeout=15)
        ch = r.json()

        for c in ch["msg"]["channels"]:
            if c["cat_id"] == cat_id:
                image = "http://tvtap.net/tvtap1/{0}|User-Agent={1}".format(self.quote(c.get("img"), "/"),
                                                                            self.quote(user_agent))
                li = xbmcgui.ListItem(c["channel_name"].rstrip("."))
                li.setProperty("IsPlayable", "true")
                li.setArt({"thumb": image, "icon": image})
                li.setInfo(type="Video",
                           infoLabels={"Title": c["channel_name"].rstrip("."), "mediatype": "video", "PlayCount": 0})
                try:
                    li.setContentLookup(False)
                except AttributeError:
                    pass
                # url = sys.argv[1].url_for(self.play, ch_id=c["pk_id"])
                url = "plugin://plugin.video.Stefano?action=taplay&subid=" + c["pk_id"]
                list_items.append((url, li, False))

        xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_LABEL)
        xbmcplugin.addDirectoryItems(int(sys.argv[1]), list_items)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

    def taplay(self, ch_id):
        list_url = "http://tvtap.net/tvtap1/index_new.php?case=get_all_channels"
        token_url = "http://tvtap.net/tvtap1/index_new.php?case=get_channel_link_with_token_tvtap"
        user_agent = "Dalvik/2.1.0 (Linux; U; Android 5.1.1; AFTS Build/LVY48F)"
        player_user_agent = "mediaPlayerhttp/2.1 (Linux;Android 5.1) ExoPlayerLib/2.6.1"
        # 178.132.6.54 81.171.8.162
        key = b"19087321"

        import requests
        r = requests.post(list_url, headers={"app-token": "9120163167c05aed85f30bf88495bd89"},
                          data={"username": "603803577"},
                          timeout=15)
        ch = r.json()
        for c in ch["msg"]["channels"]:
            if c["pk_id"] == ch_id:
                selected_channel = c
                break

        title = selected_channel.get("channel_name")
        image = "http://tvtap.net/tvtap1/{0}|User-Agent={1}".format(self.quote(c.get("img"), "/"),
                                                                    self.quote(user_agent))

        r = requests.post(token_url, headers={"app-token": "9120163167c05aed85f30bf88495bd89"},
                          data={"channel_id": ch_id, "username": "603803577"}, timeout=15)
        r.raise_for_status()

        from lib.sambatools.smb.utils.pyDes import des, PAD_PKCS5
        from base64 import b64decode, urlsafe_b64encode
        links = []
        for stream in r.json()["msg"]["channel"][0].keys():
            if "stream" in stream or "chrome_cast" in stream:
                d = des(key)
                link = d.decrypt(b64decode(r.json()["msg"]["channel"][0][stream]), padmode=PAD_PKCS5)
                if link:
                    link = link.decode("utf-8")
                    if not link == "dummytext" and link not in links:
                        links.append(link)

        link = links[(len(links) - 1)]

        if link.startswith("http"):
            media_url = "{0}|User-Agent={1}".format(link, self.quote(player_user_agent))
        else:
            media_url = link

        if "playlist.m3u8" in media_url:
            from resources.lib.indexers.thegroove360 import player
            player().play(media_url)

        else:
            li = xbmcgui.ListItem(title, path=media_url)
            li.setArt({"thumb": image, "icon": image})
            xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, li)
