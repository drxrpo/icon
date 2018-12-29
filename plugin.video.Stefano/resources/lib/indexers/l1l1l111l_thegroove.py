# coding: UTF-8
import sys
l1ll1_thegroove = sys.version_info [0] == 2
l1l_thegroove = 2048
l1l1l_thegroove = 7
def l11_thegroove (ll_thegroove):
    global l11ll_thegroove
    l11l1_thegroove = ord (ll_thegroove [-1])
    l1l11_thegroove = ll_thegroove [:-1]
    l111_thegroove = l11l1_thegroove % len (l1l11_thegroove)
    l1lll_thegroove = l1l11_thegroove [:l111_thegroove] + l1l11_thegroove [l111_thegroove:]
    if l1ll1_thegroove:
        l1l1_thegroove = unicode () .join ([unichr (ord (char) - l1l_thegroove - (l1ll_thegroove + l11l1_thegroove) % l1l1l_thegroove) for l1ll_thegroove, char in enumerate (l1lll_thegroove)])
    else:
        l1l1_thegroove = str () .join ([chr (ord (char) - l1l_thegroove - (l1ll_thegroove + l11l1_thegroove) % l1l1l_thegroove) for l1ll_thegroove, char in enumerate (l1lll_thegroove)])
    return eval (l1l1_thegroove)
import base64
import hashlib
import json
import os
import urllib2
import sys
# try:
#    from Cryptodome import Random
#    from Cryptodome.Cipher import AES
#except:
import resources.lib.stemodules.pyaes as pyaes
try:
    import xbmc
    import xbmcaddon
    import xbmcgui
except:
    pass
class l1l1l111l_thegroove:
    def __init__(self):
        self.name = l11_thegroove (u"ࠢࡱ࡮ࡸ࡫࡮ࡴ࠮ࡷ࡫ࡧࡩࡴ࠴ࡓࡵࡧࡩࡥࡳࡵࠢࡳ")
        self.token = l11_thegroove (u"ࠣࠤࡴ")
        self.l1l1lll11_thegroove = l11_thegroove (u"ࠤ࠶࠷࠷࡙ࡅࡄࡔࡈࡘࡦࡨࡣ࠲࠴࠶࠸ࠧࡵ")
        self.l1ll11l11_thegroove = l11_thegroove (u"ࠥࡗࡹ࡫ࡦࡢࡰࡲࠤ࡙࡮ࡥࡨࡴࡲࡳࡻ࡫ࠠ࠴࠸࠳ࠦࡶ")
        self.result = l11_thegroove (u"ࠦࠧࡷ")
    def l1ll11l1l_thegroove(self):
        __caller__ = sys._getframe().f_back.f_code.co_name
        self.l1l11l1ll_thegroove(__caller__)
        content = urllib2.urlopen(l11_thegroove (u"ࠧ࡮ࡴࡵࡲ࠽࠳࠴ࡽࡷࡸ࠰ࡶࡸࡪ࡬ࡡ࡯ࡱࡤࡨࡩࡵ࡮࠯࡫ࡱࡪࡴ࠵ࡔࡩࡧࡳࡥࡸࡺ࡯࠰ࡶ࡬ࡱࡪ࠴ࡰࡩࡲࠥࡸ")).read()
        l1l1l1111_thegroove = json.loads(str.encode(content, l11_thegroove (u"ࠨࡵࡵࡨ࠰࠼ࠧࡹ")))
        l1l1l1l11_thegroove = l1l1l1111_thegroove[l11_thegroove (u"ࠢࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠥࡺ")]
        l1l111lll_thegroove = int(l1l1l1l11_thegroove - int(l11_thegroove (u"ࠣ࠶࠹࠸࠶࠶࠲࠲࠲࠳ࠦࡻ")))
        return l1l111lll_thegroove
    def l1l11l1l1_thegroove(self, l1l111lll_thegroove):
        __caller__ = sys._getframe().f_back.f_code.co_name
        self.l1l11l1ll_thegroove(__caller__)
        try:
            __addon__ = xbmcaddon.Addon(id=self.name)
            cwd = xbmc.translatePath(__addon__.getAddonInfo(l11_thegroove (u"ࠩࡳࡥࡹ࡮ࠧࡼ")))
        except:
            cwd = os.getcwd() + l11_thegroove (u"ࠥ࠳ࡹ࡫ࡳࡵࠤࡽ")
        path = l11_thegroove (u"ࠦࡷ࡫ࡳࡰࡷࡵࡧࡪࡹࠬ࡭࡫ࡥ࠰࡮ࡴࡤࡦࡺࡨࡶࡸ࠲ࡴࡩࡧࡪࡶࡴࡵࡶࡦ࠵࠹࠴࠳ࡶࡹࠣࡾ").split(l11_thegroove (u"ࠧ࠲ࠢࡿ"))
        l1l11llll_thegroove = cwd + os.sep + os.path.join(*path)
        l1ll111l1_thegroove = len(open(l1l11llll_thegroove).read().splitlines())
        l1l1llll1_thegroove = l1l111lll_thegroove % l1ll111l1_thegroove
        line = self.l1l111l1l_thegroove(l1l11llll_thegroove, l1l1llll1_thegroove)
        return line
    @staticmethod
    def l1l111l1l_thegroove(l1l1l1l1l_thegroove, l1l1llll1_thegroove):
        try:
            with open(l1l1l1l1l_thegroove, l11_thegroove (u"࠭ࡲࠨࢀ")) as f:
                for l1ll1l1l1_thegroove, line in enumerate(f):
                    if l1ll1l1l1_thegroove == l1l1llll1_thegroove:
                        return str(line)
        except Exception as e:
            print(l11_thegroove (u"ࠧࡆࡴࡵࡳࡷࠦ࡯࡯ࠢ࡯࡭ࡳ࡫ࠠࡼࡿࠪࢁ").format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
    def set_token(self):
        if not self.l1l1l1lll_thegroove():
            return None
        try:
            l1l111lll_thegroove = self.l1ll11l1l_thegroove()
            line = self.l1l11l1l1_thegroove(l1l111lll_thegroove)
            line = str(l1l111lll_thegroove) + l11_thegroove (u"ࠣ࠼࠽ࠦࢂ") + str(line).rstrip().lstrip()
            l1l1l11ll_thegroove = self.l1ll111ll_thegroove(line)
            self.token = l1l1l11ll_thegroove
            return l1l1l11ll_thegroove
        except Exception as e:
            print(l11_thegroove (u"ࠩࡈࡶࡷࡵࡲࠡࡱࡱࠤࡱ࡯࡮ࡦࠢࡾࢁࠬࢃ").format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
            self.l1l111ll1_thegroove(l11_thegroove (u"ࠥࡊࡴࡸࡢࡪࡦࡧࡩࡳࠨࢄ"))
    def set_result(self, data):
        if not self.l1l1l1lll_thegroove():
            return None
        self.result = self.l1l11l111_thegroove(data)
    def l1ll111ll_thegroove(self, text):
        __caller__ = sys._getframe().f_back.f_code.co_name
        self.l1l11l1ll_thegroove(__caller__)
        l1l1ll1ll_thegroove = lambda s, b: s + (b - len(s) % b) * chr(b - len(s) % b)
        l1ll1l11l_thegroove = l11_thegroove (u"ࠦࡒࡊࡣ࡮ࡹࡍࡷࡦࠨࢅ") + l11_thegroove (u"ࠧࡍࡱࡇࡐ࡝ࡏࡳࡺࠢࢆ") + l11_thegroove (u"ࠨࡍࡅࡥࡰࡻࡏࡹࡡࠣࢇ") + l11_thegroove (u"࡛ࠢࡦࡐ࡙ࡑࡱࡐࡓࠤ࢈") + l11_thegroove (u"ࠣࡣࡕ࡝࡟ࡶࡈࡦࡧࠥࢉ")
        l1ll1l11l_thegroove = hashlib.sha256(l1ll1l11l_thegroove).hexdigest()[:32].encode(l11_thegroove (u"ࠤࡸࡸ࡫࠳࠸ࠣࢊ"))
        l1l1lll1l_thegroove = text.encode(l11_thegroove (u"ࠪࡹࡹ࡬࠭࠹ࠩࢋ"))
        l1l1l1ll1_thegroove = 32
        #except:
        l1ll11ll1_thegroove = os.urandom(16)
        l1l11ll11_thegroove = pyaes.AESModeOfOperationCFB(l1ll1l11l_thegroove, l1ll11ll1_thegroove)
        l1ll1l111_thegroove = l1l11ll11_thegroove.encrypt(l1l1ll1ll_thegroove(l1l1lll1l_thegroove, l1l1l1ll1_thegroove).encode(l11_thegroove (u"ࠦࡺࡺࡦ࠮࠺ࠥࢌ")))
        l1l1ll11l_thegroove = base64.b64encode(l1ll1l111_thegroove + l11_thegroove (u"ࠬࡀ࠺ࠨࢍ") + l1ll11ll1_thegroove).encode(l11_thegroove (u"࠭ࡵࡵࡨ࠰࠼ࠬࢎ"))
        l1l1ll11l_thegroove = l1l1ll11l_thegroove.replace(l11_thegroove (u"ࠢࠬࠤ࢏"), l11_thegroove (u"ࠣ࠰ࠥ࢐"))
        l1l1ll11l_thegroove = l1l1ll11l_thegroove.replace(l11_thegroove (u"ࠤ࠰ࠦ࢑"), l11_thegroove (u"ࠥ࠰ࠧ࢒"))
        l1l1ll11l_thegroove = l1l1ll11l_thegroove.replace(l11_thegroove (u"ࠦ࠴ࠨ࢓"), l11_thegroove (u"ࠧࡥࠢ࢔"))
        return l1l1ll11l_thegroove
    def l1l11l111_thegroove(self, data):
        __caller__ = sys._getframe().f_back.f_code.co_name
        self.l1l11l1ll_thegroove(__caller__)
        data = data.replace(l11_thegroove (u"ࠨ࠮ࠣ࢕"), l11_thegroove (u"ࠢࠬࠤ࢖"))
        data = data.replace(l11_thegroove (u"ࠣ࠮ࠥࢗ"), l11_thegroove (u"ࠤ࠰ࠦ࢘"))
        data = data.replace(l11_thegroove (u"ࠥࡣ࢙ࠧ"), l11_thegroove (u"ࠦ࠴ࠨ࢚"))
        try:
            res = base64.b64decode(data).split(l11_thegroove (u"ࠬࡀ࠺ࠨ࢛"))
            l1ll11ll1_thegroove = res[len(res) - 1]
            l1l1l11l1_thegroove = l11_thegroove (u"࠭ࠧ࢜")
            for i in range(0, (len(res) - 1)):
                l1l1l11l1_thegroove += res[i]
            l1ll1l11l_thegroove = l11_thegroove (u"ࠢࡎࡆࡦࡱࡼࡐࡳࡢࠤ࢝") + l11_thegroove (u"ࠣࡉࡴࡊࡓࡠࡋ࡯ࡶࠥ࢞") + l11_thegroove (u"ࠤࡐࡈࡨࡳࡷࡋࡵࡤࠦ࢟") + l11_thegroove (u"ࠥ࡞ࡩࡓࡕࡍ࡭ࡓࡖࠧࢠ") + l11_thegroove (u"ࠦࡦࡘ࡙࡛ࡲࡋࡩࡪࠨࢡ")
            l1ll1l11l_thegroove = hashlib.sha256(l1ll1l11l_thegroove).hexdigest()[:32].encode(l11_thegroove (u"ࠧࡻࡴࡧ࠯࠻ࠦࢢ"))
            l1l11ll11_thegroove = pyaes.AESModeOfOperationCFB(l1ll1l11l_thegroove, l1ll11ll1_thegroove)
            l1ll11lll_thegroove = l1l11ll11_thegroove.decrypt(l1l1l11l1_thegroove)
            sep = base64.b64encode(l11_thegroove (u"ࠨࠪࠫࠤࢣ")).encode(l11_thegroove (u"ࠢࡶࡶࡩ࠱࠽ࠨࢤ"))
            result, l1l11lll1_thegroove, l1l1ll111_thegroove = l1ll11lll_thegroove.split(str(sep))
            __addon__ = xbmcaddon.Addon(id=self.name)
            cwd = xbmc.translatePath(__addon__.getAddonInfo(l11_thegroove (u"ࠨࡲࡤࡸ࡭࠭ࢥ")))
            path = l11_thegroove (u"ࠤࡵࡩࡸࡵࡵࡳࡥࡨࡷ࠱ࡲࡩࡣ࠮࡬ࡲࡩ࡫ࡸࡦࡴࡶ࠰ࡹ࡮ࡥࡨࡴࡲࡳࡻ࡫࠳࠷࠲࠱ࡴࡾࠨࢦ").split(l11_thegroove (u"ࠥ࠰ࠧࢧ"))
            l1l11llll_thegroove = cwd + os.sep + os.path.join(*path)
            l1l1ll1l1_thegroove = self.l1l111l1l_thegroove(l1l11llll_thegroove, int(l1l11lll1_thegroove))
            l1l1ll1l1_thegroove = str(l1l1ll1l1_thegroove).rstrip().lstrip().encode(l11_thegroove (u"ࠦࡺࡺࡦ࠮࠺ࠥࢨ"))
            if hashlib.md5(l1l1ll1l1_thegroove).hexdigest() == l1l1ll111_thegroove:
                return result
            else:
                self.l1l111ll1_thegroove(l11_thegroove (u"ࠧࡋࡲࡳࡱࡵࡩࠥ࠺࠰࠶ࠤࢩ"), l11_thegroove (u"ࠨࡉ࡮ࡲࡲࡷࡸ࡯ࡢࡪ࡮ࡨࠤࡈࡵ࡭ࡱ࡮ࡨࡸࡦࡸࡥࠡࡎࡤࠤࡗ࡯ࡣࡩ࡫ࡨࡷࡹࡧࠢࢪ"))
        except Exception as e:
            self.l1l111ll1_thegroove(l11_thegroove (u"ࠢࡆࡴࡵࡳࡷ࡫ࠠ࠵࠲࠶ࠦࢫ"), l11_thegroove (u"ࠣࡋࡰࡴࡴࡹࡳࡪࡤ࡬ࡰࡪࠦࡃࡰ࡯ࡳࡰࡪࡺࡡࡳࡧࠣࡐࡦࠦࡒࡪࡥ࡫࡭ࡪࡹࡴࡢࠤࢬ"))
            print(l11_thegroove (u"ࠩࡈࡶࡷࡵࡲࠡࡱࡱࠤࡱ࡯࡮ࡦࠢࡾࢁࠬࢭ").format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
        return None
    def l1l1l1lll_thegroove(self, skip=False):
        if skip is False:
            __caller__ = sys._getframe().f_back.f_code.co_name
            self.l1l11l1ll_thegroove(__caller__)
        try:
            l1ll1111l_thegroove = xbmc.getInfoLabel(l11_thegroove (u"ࠪࡇࡴࡴࡴࡢ࡫ࡱࡩࡷ࠴ࡐ࡭ࡷࡪ࡭ࡳࡔࡡ࡮ࡧࠪࢮ"))
            l1ll1111l_thegroove = xbmcaddon.Addon(l1ll1111l_thegroove).getAddonInfo(l11_thegroove (u"ࠫࡳࡧ࡭ࡦࠩࢯ"))
            if l1ll1111l_thegroove != self.l1ll11l11_thegroove:
                raise Exception()
        except Exception as e:
            self.l1l111ll1_thegroove(l11_thegroove (u"ࠧࡋࡲࡳࡱࡵࡩࠥ࠷ࠢࢰ"), l11_thegroove (u"ࠨࡆࡶࡰࡽ࡭ࡴࡴࡥࠡࡆ࡬ࡷࡵࡵ࡮ࡪࡤ࡬ࡰࡪࠦࡓࡰ࡮ࡲࠤࡘࡻࠢࢱ"), self.l1ll11l11_thegroove + l11_thegroove (u"ࠢࠡࡃࡧࡨࡴࡴࠢࢲ"))
            return False
        try:
            l1l11ll1l_thegroove = xbmcaddon.Addon(id=self.name)
            xbmc.translatePath(l1l11ll1l_thegroove.getAddonInfo(l11_thegroove (u"ࠨࡲࡤࡸ࡭࠭ࢳ")))
        except:
            self.l1l111ll1_thegroove(l11_thegroove (u"ࠤࡈࡶࡷࡵࡲࡦࠢ࠵ࠦࢴ"), l11_thegroove (u"ࠥࡊࡺࡴࡺࡪࡱࡱࡩࠥࡊࡩࡴࡲࡲࡲ࡮ࡨࡩ࡭ࡧࠣࡗࡴࡲ࡯ࠡࡕࡸࠦࢵ"), self.l1ll11l11_thegroove + l11_thegroove (u"ࠦࠥࡇࡤࡥࡱࡱࠦࢶ"))
            return False
        try:
            l1l11ll1l_thegroove = xbmcaddon.Addon(id=self.name)
            cwd = xbmc.translatePath(l1l11ll1l_thegroove.getAddonInfo(l11_thegroove (u"ࠬࡶࡡࡵࡪࠪࢷ")))
            l1ll11111_thegroove = l11_thegroove (u"ࠨࡲࡦࡵࡲࡹࡷࡩࡥࡴ࠮࡯࡭ࡧ࠲ࡩ࡯ࡦࡨࡼࡪࡸࡳ࠭ࡶ࡫ࡩ࡬ࡸ࡯ࡰࡸࡨ࠷࠻࠶࠮ࡱࡻࠥࢸ").split(l11_thegroove (u"ࠢ࠭ࠤࢹ"))
            l1l11llll_thegroove = cwd + os.sep + os.path.join(*l1ll11111_thegroove)
            if not os.path.isfile(l1l11llll_thegroove):
                raise Exception()
        except:
            self.l1l111ll1_thegroove(l11_thegroove (u"ࠣࡇࡵࡶࡴࡸࡥࠡ࠵ࠥࢺ"), l11_thegroove (u"ࠤࡉࡹࡳࢀࡩࡰࡰࡨࠤࡉ࡯ࡳࡱࡱࡱ࡭ࡧ࡯࡬ࡦࠢࡖࡳࡱࡵࠠࡔࡷࠥࢻ"), self.l1ll11l11_thegroove + l11_thegroove (u"ࠥࠤࡆࡪࡤࡰࡰࠥࢼ"))
            return False
        return True
    def l1l11l1ll_thegroove(self, l1l11l11l_thegroove):
        if l1l11l11l_thegroove != l11_thegroove (u"ࠦࡸ࡫ࡴࡠࡶࡲ࡯ࡪࡴࠢࢽ") and l1l11l11l_thegroove != l11_thegroove (u"ࠧࡹࡥࡵࡡࡵࡩࡸࡻ࡬ࡵࠤࢾ"):
            raise Exception()
    def l1l111ll1_thegroove(self, s1=l11_thegroove (u"ࠨࠢࢿ"), s2=l11_thegroove (u"ࠢࠣࣀ"), l1l1lllll_thegroove=l11_thegroove (u"ࠣࠤࣁ")):
        try:
            xbmcgui.Dialog().ok(self.l1ll11l11_thegroove, s1, s2, l1l1lllll_thegroove)
        except:
            print (s1 + l11_thegroove (u"ࠤࠣࠦࣂ") + s2 + l11_thegroove (u"ࠥࠤࠧࣃ") + l1l1lllll_thegroove)