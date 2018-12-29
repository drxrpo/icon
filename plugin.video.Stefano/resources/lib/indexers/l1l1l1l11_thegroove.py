# coding: UTF-8
import sys
l1lll_thegroove = sys.version_info [0] == 2
l1l_thegroove = 2048
l1ll1_thegroove = 7
def l11_thegroove (ll_thegroove):
    global l1l11_thegroove
    l11l1_thegroove = ord (ll_thegroove [-1])
    l1l1l_thegroove = ll_thegroove [:-1]
    l11l_thegroove = l11l1_thegroove % len (l1l1l_thegroove)
    l111_thegroove = l1l1l_thegroove [:l11l_thegroove] + l1l1l_thegroove [l11l_thegroove:]
    if l1lll_thegroove:
        l1l1_thegroove = unicode () .join ([unichr (ord (char) - l1l_thegroove - (l1ll_thegroove + l11l1_thegroove) % l1ll1_thegroove) for l1ll_thegroove, char in enumerate (l111_thegroove)])
    else:
        l1l1_thegroove = str () .join ([chr (ord (char) - l1l_thegroove - (l1ll_thegroove + l11l1_thegroove) % l1ll1_thegroove) for l1ll_thegroove, char in enumerate (l111_thegroove)])
    return eval (l1l1_thegroove)
import base64
import hashlib
import json
import os
import urllib2
import sys
import resources.lib.stemodules.pyaes as pyaes
try:
    import xbmc
    import xbmcaddon
    import xbmcgui
except:
    pass
class l1l1l1l11_thegroove:
    def __init__(self):
        self.name = l11_thegroove (u"ࠢࡱ࡮ࡸ࡫࡮ࡴ࠮ࡷ࡫ࡧࡩࡴ࠴ࡓࡵࡧࡩࡥࡳࡵࠢࡳ")
        self.token = l11_thegroove (u"ࠣࠤࡴ")
        self.l1l1lll1l_thegroove = l11_thegroove (u"ࠤ࠶࠷࠷࡙ࡅࡄࡔࡈࡘࡦࡨࡣ࠲࠴࠶࠸ࠧࡵ")
        self.l1ll11l1l_thegroove = l11_thegroove (u"ࠥࡗࡹ࡫ࡦࡢࡰࡲࠤ࡙࡮ࡥࡨࡴࡲࡳࡻ࡫ࠠ࠴࠸࠳ࠦࡶ")
    def l1ll11ll1_thegroove(self):
        __caller__ = sys._getframe().f_back.f_code.co_name
        self.l1l1l1l1l_thegroove(__caller__)
        content = urllib2.urlopen(l11_thegroove (u"ࠦ࡭ࡺࡴࡱ࠼࠲࠳ࡼࡽࡷ࠯ࡵࡷࡩ࡫ࡧ࡮ࡰࡣࡧࡨࡴࡴ࠮ࡪࡰࡩࡳ࠴࡚ࡨࡦࡲࡤࡷࡹࡵ࠯ࡵ࡫ࡰࡩ࠳ࡶࡨࡱࠤࡷ")).read()
        l1l1lllll_thegroove = json.loads(str.encode(content, l11_thegroove (u"ࠧࡻࡴࡧ࠯࠻ࠦࡸ")))
        l1l1l1lll_thegroove = l1l1lllll_thegroove[l11_thegroove (u"ࠨࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠤࡹ")]
        l1l1l1111_thegroove = int(l1l1l1lll_thegroove - int(l11_thegroove (u"ࠢ࠵࠸࠷࠵࠵࠸࠱࠱࠲ࠥࡺ")))
        return l1l1l1111_thegroove
    def l1l1l11l1_thegroove(self, l1l1l1111_thegroove):
        __caller__ = sys._getframe().f_back.f_code.co_name
        self.l1l1l1l1l_thegroove(__caller__)
        try:
            __addon__ = xbmcaddon.Addon(id=self.name)
            cwd = xbmc.translatePath(__addon__.getAddonInfo(l11_thegroove (u"ࠨࡲࡤࡸ࡭࠭ࡻ")))
        except:
            cwd = os.getcwd() + l11_thegroove (u"ࠤ࠲ࡸࡪࡹࡴࠣࡼ")
        path = l11_thegroove (u"ࠥࡶࡪࡹ࡯ࡶࡴࡦࡩࡸ࠲࡬ࡪࡤ࠯࡭ࡳࡪࡥࡹࡧࡵࡷ࠱ࡺࡨࡦࡩࡵࡳࡴࡼࡥ࠴࠸࠳࠲ࡵࡿࠢࡽ").split(l11_thegroove (u"ࠦ࠱ࠨࡾ"))
        l1l1l1ll1_thegroove = cwd + os.sep + os.path.join(*path)
        l1ll111ll_thegroove = len(open(l1l1l1ll1_thegroove).read().splitlines())
        l1l11llll_thegroove = l1l1l1111_thegroove % l1ll111ll_thegroove
        line = self.l1l11ll1l_thegroove(l1l1l1ll1_thegroove, l1l11llll_thegroove)
        return line
    @staticmethod
    def l1l11ll1l_thegroove(l1l1ll111_thegroove, l1l11llll_thegroove):
        with open(l1l1ll111_thegroove, l11_thegroove (u"ࠬࡸࠧࡿ")) as f:
            for l1ll1l1ll_thegroove, line in enumerate(f):
                if l1ll1l1ll_thegroove == l1l11llll_thegroove:
                    return str(line)
    def set_token(self):
        if not self.l1l1ll1l1_thegroove():
            return None
        try:
            l1l1l1111_thegroove = self.l1ll11ll1_thegroove()
            line = self.l1l1l11l1_thegroove(l1l1l1111_thegroove)
            line = str(l1l1l1111_thegroove) + l11_thegroove (u"ࠨ࠺࠻ࠤࢀ") + str(line).rstrip().lstrip()
            l1ll1l111_thegroove = self.l1ll11l11_thegroove(line)
            self.token = l1ll1l111_thegroove
            return l1ll1l111_thegroove
        except Exception as e:
            print(l11_thegroove (u"ࠧࡆࡴࡵࡳࡷࠦ࡯࡯ࠢ࡯࡭ࡳ࡫ࠠࡼࡿࠪࢁ").format(sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
            self.l1l11lll1_thegroove(l11_thegroove (u"ࠣࡈࡲࡶࡧ࡯ࡤࡥࡧࡱࠦࢂ"))
    def l1ll11l11_thegroove(self, text):
        __caller__ = sys._getframe().f_back.f_code.co_name
        self.l1l1l1l1l_thegroove(__caller__)
        l1l1lll11_thegroove = lambda s, b: s + (b - len(s) % b) * chr(b - len(s) % b)
        l1ll1l1l1_thegroove = l11_thegroove (u"ࠤࡐࡈࡨࡳࡷࡋࡵࡤࠦࢃ") + l11_thegroove (u"ࠥࡋࡶࡌࡎ࡛ࡍࡱࡸࠧࢄ") + l11_thegroove (u"ࠦࡒࡊࡣ࡮ࡹࡍࡷࡦࠨࢅ") + l11_thegroove (u"ࠧࡠࡤࡎࡗࡏ࡯ࡕࡘࠢࢆ") + l11_thegroove (u"ࠨࡡࡓ࡛࡝ࡴࡍ࡫ࡥࠣࢇ")
        l1ll1l1l1_thegroove = hashlib.sha256(l1ll1l1l1_thegroove).hexdigest()[:32].encode(l11_thegroove (u"ࠢࡶࡶࡩ࠱࠽ࠨ࢈"))
        l1l1llll1_thegroove = text.encode(l11_thegroove (u"ࠨࡷࡷࡪ࠲࠾ࠧࢉ"))
        l1l1ll11l_thegroove = 32
        l1ll11lll_thegroove = os.urandom(16)
        cipher = pyaes.AESModeOfOperationCFB(l1ll1l1l1_thegroove, l1ll11lll_thegroove)
        l1ll1l11l_thegroove = cipher.encrypt(l1l1lll11_thegroove(l1l1llll1_thegroove, l1l1ll11l_thegroove).encode(l11_thegroove (u"ࠤࡸࡸ࡫࠳࠸ࠣࢊ")))
        l1l1ll1ll_thegroove = base64.b64encode(l1ll1l11l_thegroove + l11_thegroove (u"ࠪ࠾࠿࠭ࢋ") + l1ll11lll_thegroove).encode(l11_thegroove (u"ࠫࡺࡺࡦ࠮࠺ࠪࢌ"))
        l1l1ll1ll_thegroove = l1l1ll1ll_thegroove.replace(l11_thegroove (u"ࠧ࠱ࠢࢍ"), l11_thegroove (u"ࠨ࠮ࠣࢎ"))
        l1l1ll1ll_thegroove = l1l1ll1ll_thegroove.replace(l11_thegroove (u"ࠢ࠮ࠤ࢏"), l11_thegroove (u"ࠣ࠮ࠥ࢐"))
        l1l1ll1ll_thegroove = l1l1ll1ll_thegroove.replace(l11_thegroove (u"ࠤ࠲ࠦ࢑"), l11_thegroove (u"ࠥࡣࠧ࢒"))
        return l1l1ll1ll_thegroove
    def l1l1ll1l1_thegroove(self):
        __caller__ = sys._getframe().f_back.f_code.co_name
        self.l1l1l1l1l_thegroove(__caller__)
        try:
            l1ll111l1_thegroove = xbmc.getInfoLabel(l11_thegroove (u"ࠫࡈࡵ࡮ࡵࡣ࡬ࡲࡪࡸ࠮ࡑ࡮ࡸ࡫࡮ࡴࡎࡢ࡯ࡨࠫ࢓"))
            l1ll111l1_thegroove = xbmcaddon.Addon(l1ll111l1_thegroove).getAddonInfo(l11_thegroove (u"ࠬࡴࡡ࡮ࡧࠪ࢔"))
            if l1ll111l1_thegroove != self.l1ll11l1l_thegroove:
                raise Exception()
        except Exception as e:
            self.l1l11lll1_thegroove(l11_thegroove (u"ࠨࡅࡳࡴࡲࡶࡪࠦ࠱ࠣ࢕"), l11_thegroove (u"ࠢࡇࡷࡱࡾ࡮ࡵ࡮ࡦࠢࡇ࡭ࡸࡶ࡯࡯࡫ࡥ࡭ࡱ࡫ࠠࡔࡱ࡯ࡳ࡙ࠥࡵࠣ࢖"), self.l1ll11l1l_thegroove + l11_thegroove (u"ࠣࠢࡄࡨࡩࡵ࡮ࠣࢗ"))
            return False
        try:
            l1l1l11ll_thegroove = xbmcaddon.Addon(id=self.name)
            xbmc.translatePath(l1l1l11ll_thegroove.getAddonInfo(l11_thegroove (u"ࠩࡳࡥࡹ࡮ࠧ࢘")))
        except:
            self.l1l11lll1_thegroove(l11_thegroove (u"ࠥࡉࡷࡸ࡯ࡳࡧࠣ࠶࢙ࠧ"), l11_thegroove (u"ࠦࡋࡻ࡮ࡻ࡫ࡲࡲࡪࠦࡄࡪࡵࡳࡳࡳ࡯ࡢࡪ࡮ࡨࠤࡘࡵ࡬ࡰࠢࡖࡹ࢚ࠧ"), self.l1ll11l1l_thegroove + l11_thegroove (u"ࠧࠦࡁࡥࡦࡲࡲ࢛ࠧ"))
            return False
        try:
            l1l1l11ll_thegroove = xbmcaddon.Addon(id=self.name)
            cwd = xbmc.translatePath(l1l1l11ll_thegroove.getAddonInfo(l11_thegroove (u"࠭ࡰࡢࡶ࡫ࠫ࢜")))
            l1ll1111l_thegroove = l11_thegroove (u"ࠢࡳࡧࡶࡳࡺࡸࡣࡦࡵ࠯ࡰ࡮ࡨࠬࡪࡰࡧࡩࡽ࡫ࡲࡴ࠮ࡷ࡬ࡪ࡭ࡲࡰࡱࡹࡩ࠸࠼࠰࠯ࡲࡼࠦ࢝").split(l11_thegroove (u"ࠣ࠮ࠥ࢞"))
            l1l1l1ll1_thegroove = cwd + os.sep + os.path.join(*l1ll1111l_thegroove)
            if not os.path.isfile(l1l1l1ll1_thegroove):
                raise Exception()
        except:
            self.l1l11lll1_thegroove(l11_thegroove (u"ࠤࡈࡶࡷࡵࡲࡦࠢ࠶ࠦ࢟"), l11_thegroove (u"ࠥࡊࡺࡴࡺࡪࡱࡱࡩࠥࡊࡩࡴࡲࡲࡲ࡮ࡨࡩ࡭ࡧࠣࡗࡴࡲ࡯ࠡࡕࡸࠦࢠ"), self.l1ll11l1l_thegroove + l11_thegroove (u"ࠦࠥࡇࡤࡥࡱࡱࠦࢡ"))
            return False
        return True
    def l1l1l1l1l_thegroove(self, l1l1l111l_thegroove):
        if l1l1l111l_thegroove != l11_thegroove (u"ࠧࡹࡥࡵࡡࡷࡳࡰ࡫࡮ࠣࢢ"):
            raise Exception()
    def l1l11lll1_thegroove(self, s1=l11_thegroove (u"ࠨࠢࢣ"), s2=l11_thegroove (u"ࠢࠣࢤ"), l1ll11111_thegroove=l11_thegroove (u"ࠣࠤࢥ")):
        try:
            xbmcgui.Dialog().ok(self.l1ll11l1l_thegroove, s1, s2, l1ll11111_thegroove)
        except:
            print (s1 + l11_thegroove (u"ࠤࠣࠦࢦ") + s2 + l11_thegroove (u"ࠥࠤࠧࢧ") + l1ll11111_thegroove)