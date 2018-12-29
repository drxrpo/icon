# -*- coding: utf-8 -*-
import sys
l1l111l1_opy_ = sys.version_info [0] == 2
l1ll1lll_opy_ = 2048
l1l1l111_opy_ = 7
def l1l11_opy_ (l11l1l_opy_):
	global l1lll1ll_opy_
	l1ll1l1_opy_ = ord (l11l1l_opy_ [-1])
	l1l11l11_opy_ = l11l1l_opy_ [:-1]
	l111lll_opy_ = l1ll1l1_opy_ % len (l1l11l11_opy_)
	l11111_opy_ = l1l11l11_opy_ [:l111lll_opy_] + l1l11l11_opy_ [l111lll_opy_:]
	if l1l111l1_opy_:
		l111l_opy_ = unicode () .join ([unichr (ord (char) - l1ll1lll_opy_ - (l1l1l_opy_ + l1ll1l1_opy_) % l1l1l111_opy_) for l1l1l_opy_, char in enumerate (l11111_opy_)])
	else:
		l111l_opy_ = str () .join ([chr (ord (char) - l1ll1lll_opy_ - (l1l1l_opy_ + l1ll1l1_opy_) % l1l1l111_opy_) for l1l1l_opy_, char in enumerate (l11111_opy_)])
	return eval (l111l_opy_)
import urllib
import urllib2
import requests
import xbmcgui
import xbmcaddon
import xbmc
import os
import json
import base64
import re
import sys
import time as timenow
import xml.etree.ElementTree as ElementTree
import datetime
import thread
addon  = xbmcaddon.Addon(id=l1l11_opy_ (u"ࠬࡶ࡬ࡶࡩ࡬ࡲ࠳ࡼࡩࡥࡧࡲ࠲ࡷ࡫࡬ࡰࡣࡧࡩࡩࡺࡶࠨ੾"))
l11llll_opy_ = xbmcgui.Dialog()
l1ll_opy_ = xbmc.translatePath(addon.getAddonInfo(l1l11_opy_ (u"࠭ࡰࡳࡱࡩ࡭ࡱ࡫ࠧ੿")))
l11ll111_opy_ = xbmc.translatePath(addon.getAddonInfo(l1l11_opy_ (u"ࠧࡱࡣࡷ࡬ࠬ઀")))
l111l11ll_opy_ = xbmc.translatePath(addon.getAddonInfo(l1l11_opy_ (u"ࠨ࡫ࡦࡳࡳ࠭ઁ")))
class helper(object):
    def __init__(self, username, password, SKIN, debug=False):
        self.l11l_opy_ = addon.getAddonInfo(l1l11_opy_ (u"ࠩࡹࡩࡷࡹࡩࡰࡰࠪં"))
        self.l11l11_opy_ = l1l11_opy_ (u"ࠥࡴࡱࡻࡧࡪࡰ࠱ࡺ࡮ࡪࡥࡰ࠰ࡵࡩࡱࡵࡡࡥࡧࡧࡸࡻࠨઃ")
        self.i = self
        self.title = l1l11_opy_ (u"ࠦࡠࡉࡏࡍࡑࡕࠤࡼ࡮ࡩࡵࡧࡠࡖࡪࡲ࡯ࡢࡦࡨࡨࠥࡡ࠯ࡄࡑࡏࡓࡗࡣ࡛ࡄࡑࡏࡓࡗࠦࡲࡦࡦࡠࡘ࡛ࡡ࠯ࡄࡑࡏࡓࡗࡣࠢ઄")
        self.debug = debug
        self.skin = SKIN
        self.username = username
        self.password = password
        self.l11l1l11l_opy_ = os.path.join(l1ll_opy_, l1l11_opy_ (u"ࠬ࡬ࡡࡷࡱࡵ࡭ࡹ࡫ࡳ࠯ࡶࡻࡸࠬઅ"))
        self.l11l11l1l_opy_ = self.l11l1ll11_opy_()
        self.l11111111_opy_ = self.l11l11l1l_opy_+l1l11_opy_ (u"࠭࠯ࡱࡣࡱࡩࡱࡥࡡࡱ࡫࠱ࡴ࡭ࡶ࠿ࡶࡵࡨࡶࡳࡧ࡭ࡦ࠿ࠨࡷࠫࡶࡡࡴࡵࡺࡳࡷࡪ࠽ࠦࡵࠪઆ")%(self.username,self.password)
        self.l111111ll_opy_  = self.l11l11l1l_opy_+l1l11_opy_ (u"ࠧ࠰ࡧࡱ࡭࡬ࡳࡡ࠳࠰ࡳ࡬ࡵࡅࡵࡴࡧࡵࡲࡦࡳࡥ࠾ࠧࡶࠪࡵࡧࡳࡴࡹࡲࡶࡩࡃࠥࡴࠨࡷࡽࡵ࡫࠽ࡨࡧࡷࡣࡱ࡯ࡶࡦࡡࡦࡥࡹ࡫ࡧࡰࡴ࡬ࡩࡸ࠭ઇ")%(self.username,self.password)
        self.l1l111l_opy_  = self.l11l11l1l_opy_+l1l11_opy_ (u"ࠨ࠱ࡨࡲ࡮࡭࡭ࡢ࠴࠱ࡴ࡭ࡶ࠿ࡶࡵࡨࡶࡳࡧ࡭ࡦ࠿ࠨࡷࠫࡶࡡࡴࡵࡺࡳࡷࡪ࠽ࠦࡵࠩࡸࡾࡶࡥ࠾ࡩࡨࡸࡤࡼ࡯ࡥࡡࡦࡥࡹ࡫ࡧࡰࡴ࡬ࡩࡸ࠭ઈ")%(self.username,self.password)
        self.l1lllllll1_opy_ = self.l11l11l1l_opy_+l1l11_opy_ (u"ࠩ࠲ࡴࡱࡧࡹࡦࡴࡢࡥࡵ࡯࠮ࡱࡪࡳࡃࡺࡹࡥࡳࡰࡤࡱࡪࡃࠥࡴࠨࡳࡥࡸࡹࡷࡰࡴࡧࡁࠪࡹࠦࡢࡥࡷ࡭ࡴࡴ࠽ࡨࡧࡷࡣࡸ࡯࡭ࡱ࡮ࡨࡣࡩࡧࡴࡢࡡࡷࡥࡧࡲࡥࠧࡵࡷࡶࡪࡧ࡭ࡠ࡫ࡧࡁࠬઉ")%(self.username,self.password)
        self.l11l1l111_opy_ = False
        self.l1l11111_opy_ = self.l111ll1l1_opy_()
        self.l1lllll111_opy_ = None
        self.l11111ll1_opy_ = None
        self.l1ll11l1l1_opy_ = None
        self.l1lll11111_opy_ = None
        self.l1ll1lll11_opy_ = None
        self.l1lll1ll1l_opy_ = None
        if self.l1l11111_opy_ is None:
            self.l1l11111_opy_ = []
    def l111ll1l1_opy_(self):
        try:
            if os.path.exists(self.l11l1l11l_opy_):
                with open(self.l11l1l11l_opy_, l1l11_opy_ (u"ࠪࡶࡧ࠭ઊ")) as f:
                    return json.load(f)
            else:
                self.l1l11111_opy_ = None
        except:
            self.l1l11111_opy_ = None
            l11llll_opy_.ok(self.title,l1l11_opy_ (u"ࠫࡠࡉࡏࡍࡑࡕࠤࡷ࡫ࡤ࡞࡝ࡅࡡࡊࡸࡲࡰࡴࠣࡻ࡮ࡺࡨࠡࡴࡨࡥࡩ࡯࡮ࡨࠢࡩࡥࡻࡵࡲࡪࡶࡨࡷࠦࡡ࠯ࡃ࡟࡞࠳ࡈࡕࡌࡐࡔࡠࠫઋ"),l1l11_opy_ (u"ࠬ࠭ઌ"),l1l11_opy_ (u"࠭ࡓࡰ࡯ࡨࡸ࡭࡯࡮ࡨࠢࡺࡩࡳࡺࠠࡸࡴࡲࡲ࡬࠴࠮ࠡࡒ࡯ࡩࡦࡹࡥࠡࡶࡵࡽࠥࡧࡧࡢ࡫ࡱ࠲ࠬઍ"))
    def l1llllll11_opy_(self, l1111l11l_opy_):
        try:
            with open(self.l11l1l11l_opy_, l1l11_opy_ (u"ࠧࡸࡤࠪ઎")) as f:
                f.write(json.dumps(l1111l11l_opy_))
        except:
            l11llll_opy_.ok(self.title,l1l11_opy_ (u"ࠨ࡝ࡆࡓࡑࡕࡒࠡࡴࡨࡨࡢࡡࡂ࡞ࡇࡵࡶࡴࡸࠠࡸ࡫ࡷ࡬ࠥࡹࡡࡷ࡫ࡱ࡫ࠥ࡬ࡡࡷࡱࡵ࡭ࡹ࡫ࡳࠢ࡝࠲ࡆࡢࡡ࠯ࡄࡑࡏࡓࡗࡣࠧએ"),l1l11_opy_ (u"ࠩࠪઐ"),l1l11_opy_ (u"ࠪࡗࡴࡳࡥࡵࡪ࡬ࡲ࡬ࠦࡷࡦࡰࡷࠤࡼࡸ࡯࡯ࡩ࠱࠲ࠥࡖ࡬ࡦࡣࡶࡩࠥࡺࡲࡺࠢࡤ࡫ࡦ࡯࡮࠯ࠩઑ"))
    def l1l1ll11_opy_(self, name, url, l11ll1ll_opy_, i):
        l1llll111l_opy_ = False
        url = url.replace(self.l11l11l1l_opy_, l1l11_opy_ (u"ࠫࠬ઒")).replace(l1l11_opy_ (u"ࠬ࠵ࠧઓ")+self.username,l1l11_opy_ (u"࠭ࠧઔ")).replace(l1l11_opy_ (u"ࠧ࠰ࠩક")+self.password+l1l11_opy_ (u"ࠨ࠱ࠪખ"),l1l11_opy_ (u"ࠩࠪગ")).replace(l1l11_opy_ (u"ࠪ࠳ࡱ࡯ࡶࡦࠩઘ"),l1l11_opy_ (u"ࠫࠬઙ")).replace(l1l11_opy_ (u"ࠬ࠵࡭ࡰࡸ࡬ࡩࠬચ"),l1l11_opy_ (u"࠭ࠧછ"))
        for idx,item in enumerate(self.l1l11111_opy_):
            if name in item:
                l1llll111l_opy_ = True
                break
        if not l1llll111l_opy_:
            ll_opy_ = l11llll_opy_.select(self.title,[l1l11_opy_ (u"ࠢࡂࡦࡧࠤࡹࡵࠠࡇࡣࡹࡳࡷ࡯ࡴࡦࡵࠥજ")])
            if ll_opy_ == 0:
                url = url.encode(l1l11_opy_ (u"ࠨࡪࡨࡼࠬઝ"))
                url = base64.b64encode(url)
                l11ll1ll_opy_ = l11ll1ll_opy_.encode(l1l11_opy_ (u"ࠩ࡫ࡩࡽ࠭ઞ"))
                l11ll1ll_opy_ = base64.b64encode(l11ll1ll_opy_)
                self.l1l11111_opy_.append((name,url,l11ll1ll_opy_))
                self.l1llllll11_opy_(self.l1l11111_opy_)
                return False
        else:
            ll_opy_ = l11llll_opy_.select(self.title,[l1l11_opy_ (u"ࠥࡖࡪࡳ࡯ࡷࡧࠣࡪࡷࡵ࡭ࠡࡈࡤࡺࡴࡸࡩࡵࡧࡶࠦટ")])
            if ll_opy_ == 0:
                del self.l1l11111_opy_[idx]
                self.l1llllll11_opy_(self.l1l11111_opy_)
                return True
    def l1ll11ll1l_opy_(self):
        req = urllib2.Request(self.l11111111_opy_)
        req.add_header(l1l11_opy_ (u"࡚ࠦࡹࡥࡳ࠯ࡄ࡫ࡪࡴࡴࠣઠ") , l1l11_opy_ (u"ࠧࡘࡥ࡭ࡱࡤࡨࡪࡪࠠࡌࡱࡧ࡭ࠥࡇࡤࡥࡱࡱࠤࡧࡿࠠࡎࡣࡼࡪࡦ࡯ࡲࠡࡸࡨࡶࠥࠨડ") + self.l11l_opy_)
        response = urllib2.urlopen(req)
        link=response.read()
        l1ll1l1l11_opy_ = json.loads(link.decode(l1l11_opy_ (u"࠭ࡵࡵࡨ࠻ࠫઢ")))
        response.close()
        if l1ll1l1l11_opy_:
            return l1ll1l1l11_opy_
    def l1111111l_opy_(self):
        try:
            l1lll11lll_opy_ = self.l1ll11ll1l_opy_()
            userinfo = l1lll11lll_opy_[l1l11_opy_ (u"ࠢࡶࡵࡨࡶࡤ࡯࡮ࡧࡱࠥણ")]
            auth = userinfo[l1l11_opy_ (u"ࠣࡣࡸࡸ࡭ࠨત")]
            return auth
        except:
            return l1l11_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡋࡲࡳࡱࡵࠦથ")
    def l111lllll_opy_(self):
        try:
            l1lll11lll_opy_ = self.l1ll11ll1l_opy_()
            userinfo = l1lll11lll_opy_[l1l11_opy_ (u"ࠥࡹࡸ࡫ࡲࡠ࡫ࡱࡪࡴࠨદ")]
            status = userinfo[l1l11_opy_ (u"ࠦࡸࡺࡡࡵࡷࡶࠦધ")]
            return status
        except:
            return l1l11_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡇࡵࡶࡴࡸࠢન")
    def l11ll_opy_(self):
        if self.username == l1l11_opy_ (u"࠭ࠧ઩") or self.password == l1l11_opy_ (u"ࠧࠨપ"):
            l11llll_opy_.ok(self.title,l1l11_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠ࡭ࡱࡪ࡫࡮ࡴࡧࠡ࡫ࡱ࠲࠳࠭ફ"),l1l11_opy_ (u"ࠩࡑࡳ࡛ࠥࡳࡦࡴࡱࡥࡲ࡫ࠠࡰࡴࠣࡔࡦࡹࡳࡸࡱࡵࡨࠥࡶࡲࡰࡸ࡬ࡨࡪࡪࠡࠨબ"),l1l11_opy_ (u"ࠪࡔࡱ࡫ࡡࡴࡧࠣࡴࡷࡵࡶࡪࡦࡨࠤࡾࡵࡵࡳࠢࡘࡷࡪࡸ࡮ࡢ࡯ࡨࠤࡦࡴࡤࠡࡒࡤࡷࡸࡽ࡯ࡳࡦ࠱ࠫભ"))
            return 0
        auth = self.l1111111l_opy_()
        if auth == l1l11_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡆࡴࡵࡳࡷ࠭મ"):
            l11llll_opy_.ok(self.title, l1l11_opy_ (u"ࠬࡋࡲࡳࡱࡵ࡙ࠥࠥ࡯࡮ࡧࡷ࡬࡮ࡴࡧࠡࡹࡨࡲࡹࠦࡷࡳࡱࡱ࡫ࠥࡽࡩࡵࡪࠣࡰࡴ࡭ࡩ࡯ࠢࡳࡶࡴࡩࡥࡴࡵ࠱ࠫય"),l1l11_opy_ (u"࠭ࡐ࡭ࡧࡤࡷࡪࠦࡣࡩࡧࡦ࡯ࠥࡨࡡࡤ࡭ࠣࡰࡦࡺࡥࡳ࠰ࠪર"))
            return 0
        if auth == 1:
            status = self.l111lllll_opy_()
            if status == l1l11_opy_ (u"ࠧࡃࡣࡱࡲࡪࡪࠧ઱"):
                l11llll_opy_.ok(self.title, l1l11_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠ࡭ࡱࡪ࡫࡮ࡴࡧࠡ࡫ࡱ࠲࠳࠭લ"),l1l11_opy_ (u"ࠩࡄࡧࡨࡵࡵ࡯ࡶࠣࡷࡹࡧࡴࡶࡵࠣ࡭ࡸࠦࡳࡩࡱࡺ࡭ࡳ࡭࠺ࠡ࡝ࡆࡓࡑࡕࡒࠡࡴࡨࡨࡢࡡࡂ࡞ࡄࡤࡲࡳ࡫ࡤ࡜࠱ࡅࡡࡠ࠵ࡃࡐࡎࡒࡖࡢ࠭ળ"))
                return 0
            elif status == l1l11_opy_ (u"ࠪࡈ࡮ࡹࡡࡣ࡮ࡨࡨࠬ઴"):
                l11llll_opy_.ok(self.title, l1l11_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣࡰࡴ࡭ࡧࡪࡰࡪࠤ࡮ࡴ࠮࠯ࠩવ"),l1l11_opy_ (u"ࠬࡇࡣࡤࡱࡸࡲࡹࠦࡳࡵࡣࡷࡹࡸࠦࡩࡴࠢࡶ࡬ࡴࡽࡩ࡯ࡩ࠽ࠤࡠࡉࡏࡍࡑࡕࠤࡷ࡫ࡤ࡞࡝ࡅࡡࡘࡻࡳࡱࡧࡱࡨࡪࡪ࡛࠰ࡄࡠ࡟࠴ࡉࡏࡍࡑࡕࡡࠬશ"), l1l11_opy_ (u"࠭ࡐ࡭ࡧࡤࡷࡪࠦࡣࡩࡧࡦ࡯ࠥࡿ࡯ࡶࡴࠣ࡭ࡳࡼ࡯ࡪࡥࡨࡷࠦ࠭ષ"))
                return 0
            return 1
        if auth != 1:
            l11llll_opy_.ok(self.title, l1l11_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦ࡬ࡰࡩࡪ࡭ࡳ࡭ࠠࡪࡰ࠱࠲ࠬસ"),l1l11_opy_ (u"ࠨࡒ࡯ࡩࡦࡹࡥࠡࡴࡨ࠱ࡪࡴࡴࡦࡴ࡙ࠣࡸ࡫ࡲ࡯ࡣࡰࡩࠥࡧ࡮ࡥࠢࡓࡥࡸࡹࡷࡰࡴࡧ࠲ࠬહ"),l1l11_opy_ (u"ࠩࡕࡩࡲ࡫࡭ࡣࡧࡵ࠰ࠥࡨ࡯ࡵࡪ࡙ࠣࡸ࡫ࡲ࡯ࡣࡰࡩࠥࡧ࡮ࡥࠢࡓࡥࡸࡹࡷࡰࡴࡧࠤ࡮ࡹࠠࡤࡣࡶࡩ࠲ࡹࡥ࡯ࡵ࡬ࡸ࡮ࡼࡥ࠯ࠩ઺"))
            return 0
    def l1lll1l_opy_(self):
        try:
            code = l1l11_opy_ (u"ࠪࠫ઻")
            l1lll11_opy_ = l1l11_opy_ (u"઼ࠫࠬ")
            url = l1l11_opy_ (u"ࠬ࡮ࡴࡵࡲ࠽࠳࠴ࡺࡡࡳࡩࡨࡸࡨࡸࡥࡢࡶࡨࡷ࠳ࡩ࡯࡮࠱ࡤࡨࡩࡵ࡮࠰ࡴࡨࡰࡴࡧࡤࡦࡦ࠲ࡶࡸࡹ࠮ࡵࡺࡷࠫઽ")
            request = requests.get(url, headers={l1l11_opy_ (u"࠭ࡕࡴࡧࡵ࠱ࡆ࡭ࡥ࡯ࡶࠪા"): l1l11_opy_ (u"ࠧࡎࡱࡽ࡭ࡱࡲࡡ࠰࠷࠱࠴ࠬિ"), l1l11_opy_ (u"ࠨࡃࡦࡧࡪࡶࡴࠨી"): l1l11_opy_ (u"ࠩࡷࡩࡽࡺ࠯ࡩࡶࡰࡰ࠱ࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲ࡼ࡭ࡺ࡭࡭࠭ࡻࡱࡱ࠲ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳ࡽࡳ࡬࠼ࡳࡀ࠴࠳࠿ࠬࠫ࠱࠭࠿ࡶࡃ࠰࠯࠺ࠪુ")})
            content = request.content
            code = request.status_code
            if code == 200:
                l1lll11_opy_ = re.compile(l1l11_opy_ (u"ࠪࡶࡸࡹ࠽ࠣࠪ࠱࠯ࡄ࠯ࠢࠨૂ")).findall(content)
                for i in l1lll11_opy_:
                    l1lll11_opy_ = i
                    return l1lll11_opy_
        except:
            return l1l11_opy_ (u"ࠫࠬૃ")
    def l1l1_opy_(self):
        try:
            self.l11l1l1ll_opy_()
            code = l1l11_opy_ (u"ࠬ࠭ૄ")
            l1ll11ll_opy_ = l1l11_opy_ (u"࠭ࠧૅ")
            url = l1l11_opy_ (u"ࠧࡩࡶࡷࡴ࠿࠵࠯ࡵࡣࡵ࡫ࡪࡺࡣࡳࡧࡤࡸࡪࡹ࠮ࡤࡱࡰ࠳ࡦࡪࡤࡰࡰ࠲ࡶࡪࡲ࡯ࡢࡦࡨࡨ࠴ࡴࡥࡸࡵࡢࡪࡪ࡫ࡤ࠯ࡶࡻࡸࠬ૆")
            request = requests.get(url, headers={l1l11_opy_ (u"ࠨࡗࡶࡩࡷ࠳ࡁࡨࡧࡱࡸࠬે"): l1l11_opy_ (u"ࠩࡐࡳࡿ࡯࡬࡭ࡣ࠲࠹࠳࠶ࠧૈ"), l1l11_opy_ (u"ࠪࡅࡨࡩࡥࡱࡶࠪૉ"): l1l11_opy_ (u"ࠫࡹ࡫ࡸࡵ࠱࡫ࡸࡲࡲࠬࡢࡲࡳࡰ࡮ࡩࡡࡵ࡫ࡲࡲ࠴ࡾࡨࡵ࡯࡯࠯ࡽࡳ࡬࠭ࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡸ࡮࡮࠾ࡵࡂ࠶࠮࠺࠮࠭࠳࠯ࡁࡱ࠾࠲࠱࠼ࠬ૊")})
            code = request.status_code
            if code == 200:
                l1ll11ll_opy_ = request.content
                return l1ll11ll_opy_
        except:
            return l1l11_opy_ (u"ࠬ࠭ો")
    def l1l1111l_opy_(self, l1llll1_opy_=False):
        l1ll1ll11l_opy_ = []
        if l1llll1_opy_:
            request = urllib2.Request(l1llll1_opy_, headers={l1l11_opy_ (u"࠭ࡕࡴࡧࡵ࠱ࡆ࡭ࡥ࡯ࡶࠪૌ"): self.l11l11_opy_+l1l11_opy_ (u"ࠧ࠰્ࠩ")+self.l11l_opy_, l1l11_opy_ (u"ࠣࡃࡦࡧࡪࡶࡴࠣ૎") : l1l11_opy_ (u"ࠤࡤࡴࡵࡲࡩࡤࡣࡷ࡭ࡴࡴ࠯ࡹ࡯࡯ࠦ૏")})
        else:
            request = urllib2.Request(self.l1l111l_opy_, headers={l1l11_opy_ (u"࡙ࠪࡸ࡫ࡲ࠮ࡃࡪࡩࡳࡺࠧૐ"): self.l11l11_opy_+l1l11_opy_ (u"ࠫ࠴࠭૑")+self.l11l_opy_, l1l11_opy_ (u"ࠧࡇࡣࡤࡧࡳࡸࠧ૒") : l1l11_opy_ (u"ࠨࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳ࡽࡳ࡬ࠣ૓")})
        try:
            u = urllib2.urlopen(request)
        except:
            xbmc.executebuiltin(l1l11_opy_ (u"ࠢࡅ࡫ࡤࡰࡴ࡭࠮ࡄ࡮ࡲࡷࡪ࠮ࡢࡶࡵࡼࡨ࡮ࡧ࡬ࡰࡩࠬࠦ૔"))
            l11llll_opy_.ok(self.title,l1l11_opy_ (u"ࠨ࡝ࡆࡓࡑࡕࡒࠡࡴࡨࡨࡢࡡࡂ࡞ࡇࡵࡶࡴࡸࠡࠡࡕࡲࡱࡪࡺࡨࡪࡰࡪࠤࡼ࡫࡮ࡵࠢࡺࡶࡴࡴࡧࠡࡹ࡫ࡩࡳࠦࡴࡳࡻ࡬ࡲ࡬ࠦࡴࡰࠢࡦࡳࡳࡴࡥࡤࡶࠣࡸࡴࠦ࡯ࡶࡴࠣࡷࡪࡸࡶࡦࡴࡶ࠲ࡠ࠵ࡂ࡞࡝࠲ࡇࡔࡒࡏࡓ࡟ࠪ૕"),l1l11_opy_ (u"ࠩࠪ૖"),l1l11_opy_ (u"ࠪࡔࡱ࡫ࡡࡴࡧࠣࡧ࡭࡫ࡣ࡬ࠢࡥࡥࡨࡱࠠ࡭ࡣࡷࡩࡷ࠴ࠧ૗"))
            sys.exit(0)
        tree = ElementTree.parse(u)
        l1ll1lll1l_opy_ = tree.getroot()
        for l1ll11lll1_opy_ in tree.findall(l1l11_opy_ (u"ࠦࡨ࡮ࡡ࡯ࡰࡨࡰࠧ૘")):
            title = l1ll11lll1_opy_.find(l1l11_opy_ (u"ࠧࡺࡩࡵ࡮ࡨࠦ૙")).text
            title = base64.b64decode(title)
            title = title.replace(l1l11_opy_ (u"࡛࠭ࡄࡑࡏࡓࡗࠦࡷࡩ࡫ࡷࡩࡢ࠭૚"),l1l11_opy_ (u"ࠧ࡜ࡅࡒࡐࡔࡘࠠࡣ࡮ࡤࡧࡰࡣࠧ૛"))
            if title == l1l11_opy_ (u"ࠨࡃ࡯ࡰࠬ૜"):
                continue
            l1lll1ll11_opy_ = l1ll11lll1_opy_.find(l1l11_opy_ (u"ࠤࡳࡰࡦࡿ࡬ࡪࡵࡷࡣࡺࡸ࡬ࠣ૝")).text
            l11ll1ll_opy_ = l1l11_opy_ (u"ࠪࠫ૞")
            l1ll1ll11l_opy_.append(self.Category(title,l1lll1ll11_opy_,l11ll1ll_opy_))
        return l1ll1ll11l_opy_
    def l11l1ll11_opy_(self):
        try:
            code = l1l11_opy_ (u"ࠫࠬ૟")
            url = l1l11_opy_ (u"ࠬ࡮ࡴࡵࡲ࠽࠳࠴ࡺࡡࡳࡩࡨࡸࡨࡸࡥࡢࡶࡨࡷ࠳ࡩ࡯࡮࠱ࡤࡨࡩࡵ࡮࠰ࡴࡨࡰࡴࡧࡤࡦࡦ࠲ࡰࡴ࡭࡯ࡴ࠰ࡷࡼࡹ࠭ૠ")
            request = requests.get(url, headers={l1l11_opy_ (u"࠭ࡕࡴࡧࡵ࠱ࡆ࡭ࡥ࡯ࡶࠪૡ"): l1l11_opy_ (u"ࠧࡎࡱࡽ࡭ࡱࡲࡡ࠰࠷࠱࠴ࠬૢ"), l1l11_opy_ (u"ࠨࡃࡦࡧࡪࡶࡴࠨૣ"): l1l11_opy_ (u"ࠩࡷࡩࡽࡺ࠯ࡩࡶࡰࡰ࠱ࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲ࡼ࡭ࡺ࡭࡭࠭ࡻࡱࡱ࠲ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳ࡽࡳ࡬࠼ࡳࡀ࠴࠳࠿ࠬࠫ࠱࠭࠿ࡶࡃ࠰࠯࠺ࠪ૤")})
            content = request.content
            code = request.status_code
            if code == 200:
                return content
            else:
                return l1l11_opy_ (u"ࠪ࡬ࡹࡺࡰ࠻࠱࠲ࡶࡪࡲ࡯ࡢࡦࡨࡨࡳࡵࡷ࠯ࡥࡲࡱ࠿࠸࠰࠹࠸ࠪ૥")
        except:
            return l1l11_opy_ (u"ࠫ࡭ࡺࡴࡱ࠼࠲࠳ࡷ࡫࡬ࡰࡣࡧࡩࡩࡴ࡯ࡸ࠰ࡦࡳࡲࡀ࠲࠱࠺࠹ࠫ૦")
    def l11l1l1ll_opy_(self):
        if sys.argv[0] != l1l11_opy_ (u"ࠬࡶ࡬ࡶࡩ࡬ࡲ࠿࠵࠯ࠨ૧")+self.l11l11_opy_+l1l11_opy_ (u"࠭࠯ࠨ૨"):
            l11llll_opy_.ok(self.title,l1l11_opy_ (u"ࠧࡆࡴࡵࡳࡷ࡚ࠧࠠࡱࡸࠤ࡭ࡧࡶࡦࠢࡥࡩࡪࡴࠠࡥࡧࡷࡩࡨࡺࡥࡥࠢࡷࡶࡾ࡯࡮ࡨࠢࡷࡳࠥࡹࡴࡦࡣ࡯ࠤࡴࡻࡲࠡࡣࡧࡨࡴࡴ࠮ࠨ૩"),l1l11_opy_ (u"ࠨࡐ࡬ࡧࡪࠦࡴࡳࡻ࠱࠲࠳࠭૪"),l1l11_opy_ (u"ࠩࡑࡳࡼࠦࡧࡰࠢࡩࡹࡨࡱࠠࡺࡱࡸࡶࡸ࡫࡬ࡧ࠰ࠪ૫"))
            sys.exit()
    def l11lll1l_opy_(self):
        l1lll1llll_opy_ = []
        request = urllib2.Request(self.l111111ll_opy_, headers={l1l11_opy_ (u"࡙ࠪࡸ࡫ࡲ࠮ࡃࡪࡩࡳࡺࠧ૬"): self.l11l11_opy_+l1l11_opy_ (u"ࠫ࠴࠭૭")+self.l11l_opy_, l1l11_opy_ (u"ࠧࡇࡣࡤࡧࡳࡸࠧ૮") : l1l11_opy_ (u"ࠨࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳ࡽࡳ࡬ࠣ૯")})
        try:
            u = urllib2.urlopen(request)
        except:
            xbmc.executebuiltin(l1l11_opy_ (u"ࠢࡅ࡫ࡤࡰࡴ࡭࠮ࡄ࡮ࡲࡷࡪ࠮ࡢࡶࡵࡼࡨ࡮ࡧ࡬ࡰࡩࠬࠦ૰"))
            l11llll_opy_.ok(self.title,l1l11_opy_ (u"ࠨ࡝ࡆࡓࡑࡕࡒࠡࡴࡨࡨࡢࡡࡂ࡞ࡇࡵࡶࡴࡸࠡࠡࡕࡲࡱࡪࡺࡨࡪࡰࡪࠤࡼ࡫࡮ࡵࠢࡺࡶࡴࡴࡧࠡࡹ࡫ࡩࡳࠦࡴࡳࡻ࡬ࡲ࡬ࠦࡴࡰࠢࡦࡳࡳࡴࡥࡤࡶࠣࡸࡴࠦ࡯ࡶࡴࠣࡷࡪࡸࡶࡦࡴࡶ࠲ࡠ࠵ࡂ࡞࡝࠲ࡇࡔࡒࡏࡓ࡟ࠪ૱"),l1l11_opy_ (u"ࠩࠪ૲"),l1l11_opy_ (u"ࠪࡔࡱ࡫ࡡࡴࡧࠣࡧ࡭࡫ࡣ࡬ࠢࡥࡥࡨࡱࠠ࡭ࡣࡷࡩࡷ࠴ࠧ૳"))
            sys.exit(0)
        tree = ElementTree.parse(u)
        l1ll1lll1l_opy_ = tree.getroot()
        for category in tree.findall(l1l11_opy_ (u"ࠦࡨ࡮ࡡ࡯ࡰࡨࡰࠧ૴")):
            title = category.find(l1l11_opy_ (u"ࠧࡺࡩࡵ࡮ࡨࠦ૵")).text
            title = base64.b64decode(title)
            title = title.replace(l1l11_opy_ (u"࠭ࡷࡩ࡫ࡷࡩࠬ૶"),l1l11_opy_ (u"ࠧࡣ࡮ࡤࡧࡰ࠭૷"))
            if title == l1l11_opy_ (u"ࠨࡃ࡯ࡰࠬ૸"):
                continue
            l1lll111l1_opy_ = category.find(l1l11_opy_ (u"ࠤࡳࡰࡦࡿ࡬ࡪࡵࡷࡣࡺࡸ࡬ࠣૹ")).text
            l11ll1ll_opy_ = l1l11_opy_ (u"ࠪࠫૺ")
            l1lll1llll_opy_.append(self.Category(title,l1lll111l1_opy_,l11ll1ll_opy_))
        return l1lll1llll_opy_
    class Category(object):
        def __init__(self, name, url, l11ll1ll_opy_):
            self.name = name
            self.url = url
            self.l11ll1ll_opy_ = l11ll1ll_opy_
        def __repr__(self):
            return l1l11_opy_ (u"ࠫࡈࡧࡴࡦࡩࡲࡶࡾ࠮࡮ࡢ࡯ࡨࡁࠪࡹࠬࠡࡷࡵࡰࡂࠫࡳ࠭ࠢ࡬ࡧࡴࡴ࠽ࠦࡵࠬࠫૻ") \
                   % (self.name, self.url, self.l11ll1ll_opy_)
    def l1llll1l_opy_(self, url):
        self.l11l1l1ll_opy_()
        l1ll11ll11_opy_ = []
        request = urllib2.Request(url, headers={l1l11_opy_ (u"࡛ࠬࡳࡦࡴ࠰ࡅ࡬࡫࡮ࡵࠩૼ"): self.l11l11_opy_+l1l11_opy_ (u"࠭࠯ࠨ૽")+self.l11l_opy_, l1l11_opy_ (u"ࠢࡂࡥࡦࡩࡵࡺࠢ૾") : l1l11_opy_ (u"ࠣࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡸ࡮࡮ࠥ૿")})
        u = urllib2.urlopen(request)
        tree = ElementTree.parse(u)
        l1ll1lll1l_opy_ = tree.getroot()
        l1ll11l1ll_opy_ = 0
        for channel in tree.findall(l1l11_opy_ (u"ࠤࡦ࡬ࡦࡴ࡮ࡦ࡮ࠥ଀")):
            title = channel.find(l1l11_opy_ (u"ࠥࡸ࡮ࡺ࡬ࡦࠤଁ")).text
            title = base64.b64decode(title)
            title = title.partition(l1l11_opy_ (u"ࠦࡠࠨଂ"))
            l1ll1ll111_opy_ = channel.find(l1l11_opy_ (u"ࠧࡹࡴࡳࡧࡤࡱࡤࡻࡲ࡭ࠤଃ")).text
            l1llll1ll1_opy_ = channel.find(l1l11_opy_ (u"ࠨࡤࡦࡵࡦࡣ࡮ࡳࡡࡨࡧࠥ଄")).text
            l11ll1_opy_ = title[1]+title[2]
            l11ll1_opy_ = l11ll1_opy_.partition(l1l11_opy_ (u"ࠢ࡞ࠤଅ"))
            l11ll1_opy_ = l11ll1_opy_[2]
            l11ll1_opy_ = l11ll1_opy_.partition(l1l11_opy_ (u"ࠣࠢࠣࠤࠧଆ"))
            l11ll1_opy_ = l11ll1_opy_[2]
            l11l1l1l1_opy_ = l1l11_opy_ (u"ࠤࠨࡷࠧଇ")%(title[0]+title[1]+title[2])
            l11l1l1l1_opy_ = l11l1l1l1_opy_.partition(l1l11_opy_ (u"ࠥ࡟࠴ࡉࡏࡍࡑࡕࡡࠧଈ"))
            l1llllll_opy_ = l11l1l1l1_opy_[2].partition(l1l11_opy_ (u"ࠦࠥ࠱ࠠࠣଉ"))
            l1llllll_opy_ = l1llllll_opy_[2].partition(l1l11_opy_ (u"ࠧࠦࠠࠡࠤଊ"))
            l1llllll_opy_ = l1llllll_opy_[0]
            l11l1l1l1_opy_ = l11l1l1l1_opy_[0]+l11l1l1l1_opy_[1]
            desc = channel.find(l1l11_opy_ (u"ࠨࡤࡦࡵࡦࡶ࡮ࡶࡴࡪࡱࡱࠦଋ")).text
            if l1l11_opy_ (u"ࠧࡨࡧࡷࡣࡻࡵࡤࡠࡵࡷࡶࡪࡧ࡭ࡴࠩଌ") in url:
                if desc:
                    desc = base64.b64decode(desc)
                    l11ll1_opy_ = desc.partition(l1l11_opy_ (u"ࠨࡆࡘࡖࡆ࡚ࡉࡐࡐ࠽ࠤࠬ଍"))
                    l11ll1_opy_ = l11ll1_opy_[2].partition(l1l11_opy_ (u"ࠤ࡟ࡲࠧ଎"))
                    l11ll1_opy_ = l11ll1_opy_[0]
                    l11ll1_opy_ = l1l11_opy_ (u"ࠥ࡟ࡇࡣ࡛ࡄࡑࡏࡓࡗࠦࡲࡦࡦࡠࡈ࡚ࡘࡁࡕࡋࡒࡒ࠿࡛ࠦ࠰ࡅࡒࡐࡔࡘ࡝ࠣଏ")+l1l11_opy_ (u"ࠦࡠࡉࡏࡍࡑࡕࠤࡧࡲࡡࡤ࡭ࡠࠦଐ")+l11ll1_opy_+l1l11_opy_ (u"ࠧࡡ࠯ࡃ࡟࡞࠳ࡈࡕࡌࡐࡔࡠࠦ଑")
                    l11llll1_opy_ = desc.partition(l1l11_opy_ (u"࠭ࡇࡆࡐࡕࡉ࠿ࠦࠧ଒"))
                    l11llll1_opy_ = l11llll1_opy_[2].partition(l1l11_opy_ (u"ࠢ࡝ࡰࠥଓ"))
                    l11llll1_opy_ = l11llll1_opy_[0]
                    l11llll1_opy_ = l1l11_opy_ (u"ࠣ࡝ࡅࡡࡠࡉࡏࡍࡑࡕࠤ࡬ࡸࡥࡦࡰࡠࡋࡊࡔࡒࡆ࠼ࠣ࡟࠴ࡉࡏࡍࡑࡕࡡࠧଔ")+l1l11_opy_ (u"ࠤ࡞ࡇࡔࡒࡏࡓࠢࡥࡰࡦࡩ࡫࡞ࠤକ")+l11llll1_opy_+l1l11_opy_ (u"ࠥ࡟࠴ࡈ࡝࡜࠱ࡆࡓࡑࡕࡒ࡞ࠤଖ")
                    l1lll11l_opy_ = desc.partition(l1l11_opy_ (u"ࠫࡕࡒࡏࡕ࠼ࠣࠫଗ"))
                    l1lll11l_opy_ = l1lll11l_opy_[2].partition(l1l11_opy_ (u"ࠧࡢ࡮ࠣଘ"))
                    l1lll11l_opy_ = l1lll11l_opy_[0]
                    l1ll11_opy_ = l1l11_opy_ (u"ࠨࡦࡢ࡮ࡶࡩࠧଙ")
                else:
                    l1lll11l_opy_ = l1l11_opy_ (u"ࠢࡧࡣ࡯ࡷࡪࠨଚ")
                    l11llll1_opy_ = l1l11_opy_ (u"ࠣࠤଛ")
                    l1ll11_opy_ = l1l11_opy_ (u"ࠤࡩࡥࡱࡹࡥࠣଜ")
                    l11ll1_opy_ = l1l11_opy_ (u"ࠥࠦଝ")
            else:
                if desc:
                    desc = base64.b64decode(desc)
                    lolol = desc.partition(l1l11_opy_ (u"ࠦ࠭ࠦࠢଞ"))
                    l1llll1l11_opy_ = lolol[0]
                    lolol = lolol[2].partition(l1l11_opy_ (u"ࠧ࠯࡜࡯ࠤଟ"))
                    l11111lll_opy_ = desc.partition(l1l11_opy_ (u"ࠨࠩ࡝ࡰࠥଠ"))
                    l11111lll_opy_ = l11111lll_opy_[2].partition(l1l11_opy_ (u"ࠢࠩࠤଡ"))
                    l11l11l11_opy_ = l11111lll_opy_[0]
                    l11l11l11_opy_ = l11l11l11_opy_.partition(l1l11_opy_ (u"ࠣ࡟ࠣࠦଢ"))
                    l11l11l11_opy_ = l11l11l11_opy_[2].partition(l1l11_opy_ (u"ࠤ࡟ࡲࠧଣ"))
                    l11llll1_opy_ = l11l11l11_opy_[0]
                    l1lll11l_opy_ = lolol[0]
                    l1ll11_opy_ = l11111lll_opy_[2].partition(l1l11_opy_ (u"ࠥࠤࠧତ"))
                    l1ll11_opy_ = l1ll11_opy_[2].partition(l1l11_opy_ (u"ࠦ࠮ࡢ࡮ࠣଥ"))
                    l1ll11_opy_ = l1ll11_opy_[0]
                else:
                    l1lll11l_opy_ = l1l11_opy_ (u"ࠧ࡬ࡡ࡭ࡵࡨࠦଦ")
                    l11llll1_opy_ = l1l11_opy_ (u"ࠨࠢଧ")
                    l1ll11_opy_ = l1l11_opy_ (u"ࠢࡧࡣ࡯ࡷࡪࠨନ")
                    l11ll1_opy_ = l1l11_opy_ (u"ࠣࠤ଩")
            if not l1llll1ll1_opy_ or l1llll1ll1_opy_.lower() == l1l11_opy_ (u"ࠩࡱࡳࡳ࡫ࠧପ"):
                l1llll1ll1_opy_ = l1l11_opy_ (u"ࠪࡶࡪࡲ࡯ࡢࡦࡨࡨࡹࡼ࠯࡯ࡱ࡯ࡳ࡬ࡵ࠮ࡱࡰࡪࠫଫ")
            l1ll11l1ll_opy_ = l1ll11l1ll_opy_ + 1
            l1ll11ll11_opy_.append(self.Channel(l1ll11l1ll_opy_, l11l1l1l1_opy_, l1llll1ll1_opy_, l1ll1ll111_opy_, l11ll1_opy_, l1lll11l_opy_, l1llllll_opy_, l11llll1_opy_, l1ll11_opy_))
        return l1ll11ll11_opy_
    def l11l1l1_opy_(self):
        l1ll11ll11_opy_ = []
        l1ll11l1ll_opy_ = 0
        for channel in self.l1l11111_opy_:
            l11l1l1l1_opy_ = channel[0]
            l1ll1ll111_opy_ = channel[1]
            l1ll1ll111_opy_ = base64.b64decode(l1ll1ll111_opy_)
            l1ll1ll111_opy_ = l1ll1ll111_opy_.decode(l1l11_opy_ (u"ࠫ࡭࡫ࡸࠨବ"))
            if l1l11_opy_ (u"ࠬ࠴࡭ࡱ࠶ࠪଭ") in l1ll1ll111_opy_:
                l1ll1ll111_opy_ = self.l11l11l1l_opy_+l1l11_opy_ (u"࠭࠯࡮ࡱࡹ࡭ࡪ࠵ࠧମ")+self.username+l1l11_opy_ (u"ࠧ࠰ࠩଯ")+self.password+l1l11_opy_ (u"ࠨ࠱ࠪର")+l1ll1ll111_opy_
            else:
                l1ll1ll111_opy_ = self.l11l11l1l_opy_+l1l11_opy_ (u"ࠩ࠲ࡰ࡮ࡼࡥ࠰ࠩ଱")+self.username+l1l11_opy_ (u"ࠪ࠳ࠬଲ")+self.password+l1l11_opy_ (u"ࠫ࠴࠭ଳ")+l1ll1ll111_opy_
            l1llll1ll1_opy_ = channel[2]
            l1llll1ll1_opy_ = base64.b64decode(l1llll1ll1_opy_)
            l1llll1ll1_opy_ = l1llll1ll1_opy_.decode(l1l11_opy_ (u"ࠬ࡮ࡥࡹࠩ଴"))
            l11ll1_opy_ = l1l11_opy_ (u"࠭ࠧଵ")
            l1lll11l_opy_ = l1l11_opy_ (u"ࠢࡧࡣ࡯ࡷࡪࠨଶ")
            l1llllll_opy_ = l1l11_opy_ (u"ࠨࠩଷ")
            l11llll1_opy_ = l1l11_opy_ (u"ࠩࠪସ")
            l1ll11_opy_ = l1l11_opy_ (u"ࠥࡪࡦࡲࡳࡦࠤହ")
            l1ll11l1ll_opy_ = l1ll11l1ll_opy_ + 1
            l1ll11ll11_opy_.append(self.Channel(l1ll11l1ll_opy_, l11l1l1l1_opy_, l1llll1ll1_opy_, l1ll1ll111_opy_, l11ll1_opy_, l1lll11l_opy_, l1llllll_opy_, l11llll1_opy_, l1ll11_opy_))
        return l1ll11ll11_opy_
    def l1ll1lllll_opy_(self, l1lllll1l1_opy_, l111lll1l_opy_):
        if l1lllll1l1_opy_ == l1l11_opy_ (u"ࠫࡳࡨࡡࠨ଺"):
            l111lll1l_opy_ = l111lll1l_opy_.replace(l1l11_opy_ (u"ࠬ࡮ࡡࡸ࡭ࡶࠫ଻"),l1l11_opy_ (u"࠭ࡡࡵ࡮ࡤࡲࡹࡧ଼ࠧ"))
            l111lll1l_opy_ = l111lll1l_opy_.replace(l1l11_opy_ (u"ࠧࡤࡧ࡯ࡸ࡮ࡩࡳࠨଽ"),l1l11_opy_ (u"ࠨࡤࡲࡷࡹࡵ࡮ࠨା"))
            l111lll1l_opy_ = l111lll1l_opy_.replace(l1l11_opy_ (u"ࠩࡱࡩࡹࡹࠧି"),l1l11_opy_ (u"ࠪࡦࡷࡵ࡯࡬࡮ࡼࡲࠬୀ"))
            l111lll1l_opy_ = l111lll1l_opy_.replace(l1l11_opy_ (u"ࠫࡧࡵࡢࡤࡣࡷࡷࠬୁ"),l1l11_opy_ (u"ࠬࡩࡨࡢࡴ࡯ࡳࡹࡺࡥࠨୂ"))
            l111lll1l_opy_ = l111lll1l_opy_.replace(l1l11_opy_ (u"࠭ࡢࡶ࡮࡯ࡷࠬୃ"),l1l11_opy_ (u"ࠧࡤࡪ࡬ࡧࡦ࡭࡯ࠨୄ"))
            l111lll1l_opy_ = l111lll1l_opy_.replace(l1l11_opy_ (u"ࠨࡥࡤࡺࡦࡲࡩࡦࡴࡶࠫ୅"),l1l11_opy_ (u"ࠩࡦࡰࡪࡼࡥ࡭ࡣࡱࡨࠬ୆"))
            l111lll1l_opy_ = l111lll1l_opy_.replace(l1l11_opy_ (u"ࠪࡱࡦࡼࡥࡳ࡫ࡦ࡯ࡸ࠭େ"),l1l11_opy_ (u"ࠫࡩࡧ࡬࡭ࡣࡶࠫୈ"))
            l111lll1l_opy_ = l111lll1l_opy_.replace(l1l11_opy_ (u"ࠬࡴࡵࡨࡩࡨࡸࡸ࠭୉"),l1l11_opy_ (u"࠭ࡤࡦࡰࡹࡩࡷ࠭୊"))
            l111lll1l_opy_ = l111lll1l_opy_.replace(l1l11_opy_ (u"ࠧࡳࡱࡦ࡯ࡪࡺࡳࠨୋ"),l1l11_opy_ (u"ࠨࡪࡲࡹࡸࡺ࡯࡯ࠩୌ"))
            l111lll1l_opy_ = l111lll1l_opy_.replace(l1l11_opy_ (u"ࠩࡳࡥࡨ࡫ࡲࡴ୍ࠩ"),l1l11_opy_ (u"ࠪ࡭ࡳࡪࡩࡢࡰࡤࠫ୎"))
            l111lll1l_opy_ = l111lll1l_opy_.replace(l1l11_opy_ (u"ࠫࡨࡲࡩࡱࡲࡨࡶࡸ࠭୏"),l1l11_opy_ (u"ࠬࡲࡡࠡࡥ࡯࡭ࡵࡶࡥࡳࡵࠪ୐"))
            l111lll1l_opy_ = l111lll1l_opy_.replace(l1l11_opy_ (u"࠭࡬ࡢ࡭ࡨࡶࡸ࠭୑"),l1l11_opy_ (u"ࠧ࡭ࡣࠣࡰࡦࡱࡥࡳࡵࠪ୒"))
            l111lll1l_opy_ = l111lll1l_opy_.replace(l1l11_opy_ (u"ࠨࡹࡤࡶࡷ࡯࡯ࡳࡵࠪ୓"),l1l11_opy_ (u"ࠩࡪࡳࡱࡪࡥ࡯ࠢࡶࡸࡦࡺࡥࠨ୔"))
            l111lll1l_opy_ = l111lll1l_opy_.replace(l1l11_opy_ (u"ࠪ࡫ࡷ࡯ࡺࡻ࡮࡬ࡩࡸ࠭୕"),l1l11_opy_ (u"ࠫࡲ࡫࡭ࡱࡪ࡬ࡷࠬୖ"))
            l111lll1l_opy_ = l111lll1l_opy_.replace(l1l11_opy_ (u"ࠬ࡮ࡥࡢࡶࠪୗ"),l1l11_opy_ (u"࠭࡭ࡪࡣࡰ࡭ࠬ୘"))
            l111lll1l_opy_ = l111lll1l_opy_.replace(l1l11_opy_ (u"ࠧࡣࡷࡦ࡯ࡸ࠭୙"),l1l11_opy_ (u"ࠨ࡯࡬ࡰࡼࡧࡵ࡬ࡧࡨࠫ୚"))
            l111lll1l_opy_ = l111lll1l_opy_.replace(l1l11_opy_ (u"ࠩࡷ࡭ࡲࡨࡥࡳࡹࡲࡰࡻ࡫ࡳࠨ୛"),l1l11_opy_ (u"ࠪࡱ࡮ࡴ࡮ࡦࡵࡲࡸࡦ࠭ଡ଼"))
            l111lll1l_opy_ = l111lll1l_opy_.replace(l1l11_opy_ (u"ࠫ࡭ࡵࡲ࡯ࡧࡷࡷࠬଢ଼"),l1l11_opy_ (u"ࠬࡴࡥࡸࠢࡲࡶࡱ࡫ࡡ࡯ࡵࠪ୞"))
            l111lll1l_opy_ = l111lll1l_opy_.replace(l1l11_opy_ (u"࠭࡫࡯࡫ࡦ࡯ࡸ࠭ୟ"),l1l11_opy_ (u"ࠧ࡯ࡧࡺࠤࡾࡵࡲ࡬ࠩୠ"))
            l111lll1l_opy_ = l111lll1l_opy_.replace(l1l11_opy_ (u"ࠨࡶ࡫ࡹࡳࡪࡥࡳࠩୡ"),l1l11_opy_ (u"ࠩࡲ࡯ࡱࡧࡨࡰ࡯ࡤࠤࡨ࡯ࡴࡺࠩୢ"))
            l111lll1l_opy_ = l111lll1l_opy_.replace(l1l11_opy_ (u"ࠪࡱࡦ࡭ࡩࡤࠩୣ"),l1l11_opy_ (u"ࠫࡴࡸ࡬ࡢࡰࡧࡳࠬ୤"))
            l111lll1l_opy_ = l111lll1l_opy_.replace(l1l11_opy_ (u"ࠬ࠽࠶ࡦࡴࡶࠫ୥"),l1l11_opy_ (u"࠭ࡰࡩ࡫࡯ࡥࡩ࡫࡬ࡱࡪ࡬ࡥࠬ୦"))
            l111lll1l_opy_ = l111lll1l_opy_.replace(l1l11_opy_ (u"ࠧࡴࡷࡱࡷࠬ୧"),l1l11_opy_ (u"ࠨࡲ࡫ࡳࡪࡴࡩࡹࠩ୨"))
            l111lll1l_opy_ = l111lll1l_opy_.replace(l1l11_opy_ (u"ࠩࡷࡶࡦ࡯࡬ࠡࡤ࡯ࡥࡿ࡫ࡲࡴࠩ୩"),l1l11_opy_ (u"ࠪࡴࡴࡸࡴ࡭ࡣࡱࡨࠬ୪"))
            l111lll1l_opy_ = l111lll1l_opy_.replace(l1l11_opy_ (u"ࠫࡰ࡯࡮ࡨࡵࠪ୫"),l1l11_opy_ (u"ࠬࡹࡡࡤࡴࡤࡱࡪࡴࡴࡰࠩ୬"))
            l111lll1l_opy_ = l111lll1l_opy_.replace(l1l11_opy_ (u"࠭ࡳࡱࡷࡵࡷࠬ୭"),l1l11_opy_ (u"ࠧࡴࡣࡱࠤࡦࡴࡴࡰࡰ࡬ࡳࠬ୮"))
            l111lll1l_opy_ = l111lll1l_opy_.replace(l1l11_opy_ (u"ࠨࡴࡤࡴࡹࡵࡲࡴࠩ୯"),l1l11_opy_ (u"ࠩࡷࡳࡷࡵ࡮ࡵࡱࠪ୰"))
            l111lll1l_opy_ = l111lll1l_opy_.replace(l1l11_opy_ (u"ࠪ࡮ࡦࢀࡺࠨୱ"),l1l11_opy_ (u"ࠫࡺࡺࡡࡩࠩ୲"))
            l111lll1l_opy_ = l111lll1l_opy_.replace(l1l11_opy_ (u"ࠬࡽࡩࡻࡣࡵࡨࡸ࠭୳"),l1l11_opy_ (u"࠭ࡷࡢࡵ࡫࡭ࡳ࡭ࡴࡰࡰࠪ୴"))
            return l111lll1l_opy_
        elif l1lllll1l1_opy_ == l1l11_opy_ (u"ࠧ࡯ࡨ࡯ࠫ୵"):
            l111lll1l_opy_ = l111lll1l_opy_.replace(l1l11_opy_ (u"ࠨࡥࡤࡶࡩ࡯࡮ࡢ࡮ࡶࠫ୶"),l1l11_opy_ (u"ࠩࡤࡶ࡮ࢀ࡯࡯ࡣࠪ୷"))
            l111lll1l_opy_ = l111lll1l_opy_.replace(l1l11_opy_ (u"ࠪࡪࡦࡲࡣࡰࡰࡶࠫ୸"),l1l11_opy_ (u"ࠫࡦࡺ࡬ࡢࡰࡷࡥࠬ୹"))
            l111lll1l_opy_ = l111lll1l_opy_.replace(l1l11_opy_ (u"ࠬࡸࡡࡷࡧࡱࡷࠬ୺"),l1l11_opy_ (u"࠭ࡢࡢ࡮ࡷ࡭ࡲࡵࡲࡦࠩ୻"))
            l111lll1l_opy_ = l111lll1l_opy_.replace(l1l11_opy_ (u"ࠧࡣ࡫࡯ࡰࡸ࠭୼"),l1l11_opy_ (u"ࠨࡤࡸࡪ࡫ࡧ࡬ࡰࠩ୽"))
            l111lll1l_opy_ = l111lll1l_opy_.replace(l1l11_opy_ (u"ࠩࡳࡥࡳࡺࡨࡦࡴࡶࠫ୾"),l1l11_opy_ (u"ࠪࡧࡦࡸ࡯࡭࡫ࡱࡥࠬ୿"))
            l111lll1l_opy_ = l111lll1l_opy_.replace(l1l11_opy_ (u"ࠫࡧ࡫ࡡࡳࡵࠪ஀"),l1l11_opy_ (u"ࠬࡩࡨࡪࡥࡤ࡫ࡴ࠭஁"))
            l111lll1l_opy_ = l111lll1l_opy_.replace(l1l11_opy_ (u"࠭ࡢࡦࡰࡪࡥࡱࡹࠧஂ"),l1l11_opy_ (u"ࠧࡤ࡫ࡱࡧ࡮ࡴ࡮ࡢࡶ࡬ࠫஃ"))
            l111lll1l_opy_ = l111lll1l_opy_.replace(l1l11_opy_ (u"ࠨࡤࡵࡳࡼࡴࡳࠨ஄"),l1l11_opy_ (u"ࠩࡦࡰࡪࡼࡥ࡭ࡣࡱࡨࠬஅ"))
            l111lll1l_opy_ = l111lll1l_opy_.replace(l1l11_opy_ (u"ࠪࡧࡴࡽࡢࡰࡻࡶࠫஆ"),l1l11_opy_ (u"ࠫࡩࡧ࡬࡭ࡣࡶࠫஇ"))
            l111lll1l_opy_ = l111lll1l_opy_.replace(l1l11_opy_ (u"ࠬࡨࡲࡰࡰࡦࡳࡸ࠭ஈ"),l1l11_opy_ (u"࠭ࡤࡦࡰࡹࡩࡷ࠭உ"))
            l111lll1l_opy_ = l111lll1l_opy_.replace(l1l11_opy_ (u"ࠧ࡭࡫ࡲࡲࡸ࠭ஊ"),l1l11_opy_ (u"ࠨࡦࡨࡸࡷࡵࡩࡵࠩ஋"))
            l111lll1l_opy_ = l111lll1l_opy_.replace(l1l11_opy_ (u"ࠩࡳࡥࡨࡱࡥࡳࡵࠪ஌"),l1l11_opy_ (u"ࠪ࡫ࡷ࡫ࡥ࡯ࠢࡥࡥࡾ࠭஍"))
            l111lll1l_opy_ = l111lll1l_opy_.replace(l1l11_opy_ (u"ࠫࡹ࡫ࡸࡢࡰࡶࠫஎ"),l1l11_opy_ (u"ࠬ࡮࡯ࡶࡵࡷࡳࡳ࠭ஏ"))
            l111lll1l_opy_ = l111lll1l_opy_.replace(l1l11_opy_ (u"࠭ࡣࡰ࡮ࡷࡷࠬஐ"),l1l11_opy_ (u"ࠧࡪࡰࡧ࡭ࡦࡴࡡࡱࡱ࡯࡭ࡸ࠭஑"))
            l111lll1l_opy_ = l111lll1l_opy_.replace(l1l11_opy_ (u"ࠨ࡬ࡤ࡫ࡺࡧࡲࡴࠩஒ"),l1l11_opy_ (u"ࠩ࡭ࡥࡨࡱࡳࡰࡰࡹ࡭ࡱࡲࡥࠨஓ"))
            l111lll1l_opy_ = l111lll1l_opy_.replace(l1l11_opy_ (u"ࠪࡧ࡭࡯ࡥࡧࡵࠪஔ"),l1l11_opy_ (u"ࠫࡰࡧ࡮ࡴࡣࡶࠤࡨ࡯ࡴࡺࠩக"))
            l111lll1l_opy_ = l111lll1l_opy_.replace(l1l11_opy_ (u"ࠬࡪ࡯࡭ࡲ࡫࡭ࡳࡹࠧ஖"),l1l11_opy_ (u"࠭࡭ࡪࡣࡰ࡭ࠬ஗"))
            l111lll1l_opy_ = l111lll1l_opy_.replace(l1l11_opy_ (u"ࠧࡷ࡫࡮࡭ࡳ࡭ࡳࠨ஘"),l1l11_opy_ (u"ࠨ࡯࡬ࡲࡳ࡫ࡳࡰࡶࡤࠫங"))
            l111lll1l_opy_ = l111lll1l_opy_.replace(l1l11_opy_ (u"ࠩࡳࡥࡹࡸࡩࡰࡶࡶࠫச"),l1l11_opy_ (u"ࠪࡲࡪࡽࠠࡦࡰࡪࡰࡦࡴࡤࠨ஛"))
            l111lll1l_opy_ = l111lll1l_opy_.replace(l1l11_opy_ (u"ࠫࡸࡧࡩ࡯ࡶࡶࠫஜ"),l1l11_opy_ (u"ࠬࡴࡥࡸࠢࡲࡶࡱ࡫ࡡ࡯ࡵࠪ஝"))
            l111lll1l_opy_ = l111lll1l_opy_.replace(l1l11_opy_ (u"࠭ࡧࡪࡣࡱࡸࡸ࠭ஞ"),l1l11_opy_ (u"ࠧ࡯ࡻࠣ࡫࡮ࡧ࡮ࡵࡵࠪட"))
            l111lll1l_opy_ = l111lll1l_opy_.replace(l1l11_opy_ (u"ࠨ࡬ࡨࡸࡸ࠭஠"),l1l11_opy_ (u"ࠩࡱࡽࠥࡰࡥࡵࡵࠪ஡"))
            l111lll1l_opy_ = l111lll1l_opy_.replace(l1l11_opy_ (u"ࠪࡶࡦ࡯ࡤࡦࡴࡶࠫ஢"),l1l11_opy_ (u"ࠫࡴࡧ࡫࡭ࡣࡱࡨࠬண"))
            l111lll1l_opy_ = l111lll1l_opy_.replace(l1l11_opy_ (u"ࠬ࡫ࡡࡨ࡮ࡨࡷࠬத"),l1l11_opy_ (u"࠭ࡰࡩ࡫࡯ࡥࡩ࡫࡬ࡱࡪ࡬ࡥࠬ஥"))
            l111lll1l_opy_ = l111lll1l_opy_.replace(l1l11_opy_ (u"ࠧࡴࡶࡨࡩࡱ࡫ࡲࡴࠩ஦"),l1l11_opy_ (u"ࠨࡲ࡬ࡸࡹࡹࡢࡶࡴࡪ࡬ࠬ஧"))
            l111lll1l_opy_ = l111lll1l_opy_.replace(l1l11_opy_ (u"ࠩࡦ࡬ࡦࡸࡧࡦࡴࡶࠫந"),l1l11_opy_ (u"ࠪࡰࡴࡹࠠࡢࡰࡪࡩࡱ࡫ࡳࠨன"))
            l111lll1l_opy_ = l111lll1l_opy_.replace(l1l11_opy_ (u"ࠫ࠹࠿ࡥࡳࡵࠪப"),l1l11_opy_ (u"ࠬࡹࡡ࡯ࠢࡩࡶࡦࡴࡣࡪࡵࡦࡳࠬ஫"))
            l111lll1l_opy_ = l111lll1l_opy_.replace(l1l11_opy_ (u"࠭ࡳࡦࡣ࡫ࡥࡼࡱࡳࠨ஬"),l1l11_opy_ (u"ࠧࡴࡧࡤࡸࡹࡲࡥࠨ஭"))
            l111lll1l_opy_ = l111lll1l_opy_.replace(l1l11_opy_ (u"ࠨࡴࡤࡱࡸ࠭ம"),l1l11_opy_ (u"ࠩࡶࡸ࠳ࠦ࡬ࡰࡷ࡬ࡷࠬய"))
            l111lll1l_opy_ = l111lll1l_opy_.replace(l1l11_opy_ (u"ࠪࡦࡺࡩࡣࡢࡰࡨࡩࡷࡹࠧர"),l1l11_opy_ (u"ࠫࡹࡧ࡭ࡱࡣࠣࡦࡦࡿࠧற"))
            l111lll1l_opy_ = l111lll1l_opy_.replace(l1l11_opy_ (u"ࠬࡺࡩࡵࡣࡱࡷࠬல"),l1l11_opy_ (u"࠭ࡴࡦࡰࡱࡩࡸࡹࡥࡦࠩள"))
            l111lll1l_opy_ = l111lll1l_opy_.replace(l1l11_opy_ (u"ࠧࡳࡧࡧࡷࡰ࡯࡮ࡴࠩழ"),l1l11_opy_ (u"ࠨࡹࡤࡷ࡭࡯࡮ࡨࡶࡲࡲࠬவ"))
            return l111lll1l_opy_
        elif l1lllll1l1_opy_ == l1l11_opy_ (u"ࠩࡱ࡬ࡱ࠭ஶ"):
            l111lll1l_opy_ = l111lll1l_opy_.replace(l1l11_opy_ (u"ࠪࡨࡺࡩ࡫ࡴࠩஷ"),l1l11_opy_ (u"ࠫࡦࡴࡡࡩࡧ࡬ࡱࠬஸ"))
            l111lll1l_opy_ = l111lll1l_opy_.replace(l1l11_opy_ (u"ࠬࡩ࡯ࡺࡱࡷࡩࡸ࠭ஹ"),l1l11_opy_ (u"࠭ࡡࡳ࡫ࡽࡳࡳࡧࠧ஺"))
            l111lll1l_opy_ = l111lll1l_opy_.replace(l1l11_opy_ (u"ࠧࡣࡴࡸ࡭ࡳࡹࠧ஻"),l1l11_opy_ (u"ࠨࡤࡲࡷࡹࡵ࡮ࠨ஼"))
            l111lll1l_opy_ = l111lll1l_opy_.replace(l1l11_opy_ (u"ࠩࡶࡥࡧࡸࡥࡴࠩ஽"),l1l11_opy_ (u"ࠪࡦࡺ࡬ࡦࡢ࡮ࡲࠫா"))
            l111lll1l_opy_ = l111lll1l_opy_.replace(l1l11_opy_ (u"ࠫ࡫ࡲࡡ࡮ࡧࡶࠫி"),l1l11_opy_ (u"ࠬࡩࡡ࡭ࡩࡤࡶࡾ࠭ீ"))
            l111lll1l_opy_ = l111lll1l_opy_.replace(l1l11_opy_ (u"࠭ࡨࡶࡴࡵ࡭ࡨࡧ࡮ࡦࡵࠪு"),l1l11_opy_ (u"ࠧࡤࡣࡵࡳࡱ࡯࡮ࡢࠩூ"))
            l111lll1l_opy_ = l111lll1l_opy_.replace(l1l11_opy_ (u"ࠨࡤ࡯ࡥࡨࡱࡨࡢࡹ࡮ࡷࠬ௃"),l1l11_opy_ (u"ࠩࡦ࡬࡮ࡩࡡࡨࡱࠪ௄"))
            l111lll1l_opy_ = l111lll1l_opy_.replace(l1l11_opy_ (u"ࠪࡥࡻࡧ࡬ࡢࡰࡦ࡬ࡪ࠭௅"),l1l11_opy_ (u"ࠫࡨࡵ࡬ࡰࡴࡤࡨࡴ࠭ெ"))
            l111lll1l_opy_ = l111lll1l_opy_.replace(l1l11_opy_ (u"ࠬࡨ࡬ࡶࡧࠣ࡮ࡦࡩ࡫ࡦࡶࡶࠫே"),l1l11_opy_ (u"࠭ࡣࡰ࡮ࡸࡱࡧࡻࡳࠨை"))
            l111lll1l_opy_ = l111lll1l_opy_.replace(l1l11_opy_ (u"ࠧࡴࡶࡤࡶࡸ࠭௉"),l1l11_opy_ (u"ࠨࡦࡤࡰࡱࡧࡳࠨொ"))
            l111lll1l_opy_ = l111lll1l_opy_.replace(l1l11_opy_ (u"ࠩࡵࡩࡩࠦࡷࡪࡰࡪࡷࠬோ"),l1l11_opy_ (u"ࠪࡨࡪࡺࡲࡰ࡫ࡷࠫௌ"))
            l111lll1l_opy_ = l111lll1l_opy_.replace(l1l11_opy_ (u"ࠫࡴ࡯࡬ࡦࡴࡶ்ࠫ"),l1l11_opy_ (u"ࠬ࡫ࡤ࡮ࡱࡱࡸࡴࡴࠧ௎"))
            l111lll1l_opy_ = l111lll1l_opy_.replace(l1l11_opy_ (u"࠭ࡰࡢࡰࡷ࡬ࡪࡸࡳࠨ௏"),l1l11_opy_ (u"ࠧࡧ࡮ࡲࡶ࡮ࡪࡡࠨௐ"))
            l111lll1l_opy_ = l111lll1l_opy_.replace(l1l11_opy_ (u"ࠨ࡭࡬ࡲ࡬ࡹࠧ௑"),l1l11_opy_ (u"ࠩ࡯ࡳࡸࠦࡡ࡯ࡩࡨࡰࡪࡹࠧ௒"))
            l111lll1l_opy_ = l111lll1l_opy_.replace(l1l11_opy_ (u"ࠪࡻ࡮ࡲࡤࠨ௓"),l1l11_opy_ (u"ࠫࡲ࡯࡮࡯ࡧࡶࡳࡹࡧࠧ௔"))
            l111lll1l_opy_ = l111lll1l_opy_.replace(l1l11_opy_ (u"ࠬࡩࡡ࡯ࡣࡧ࡭ࡪࡴࡳࠨ௕"),l1l11_opy_ (u"࠭࡭ࡰࡰࡷࡶࡪࡧ࡬ࠨ௖"))
            l111lll1l_opy_ = l111lll1l_opy_.replace(l1l11_opy_ (u"ࠧࡱࡴࡨࡨࡦࡺ࡯ࡳࡵࠪௗ"),l1l11_opy_ (u"ࠨࡰࡤࡷ࡭ࡼࡩ࡭࡮ࡨࠫ௘"))
            l111lll1l_opy_ = l111lll1l_opy_.replace(l1l11_opy_ (u"ࠩࡧࡩࡻ࡯࡬ࡴࠩ௙"),l1l11_opy_ (u"ࠪࡲࡪࡽࠠ࡫ࡧࡵࡷࡪࡿࠧ௚"))
            l111lll1l_opy_ = l111lll1l_opy_.replace(l1l11_opy_ (u"ࠫ࡮ࡹ࡬ࡢࡰࡧࡩࡷࡹࠧ௛"),l1l11_opy_ (u"ࠬࡴࡹࠡ࡫ࡶࡰࡦࡴࡤࡦࡴࡶࠫ௜"))
            l111lll1l_opy_ = l111lll1l_opy_.replace(l1l11_opy_ (u"࠭ࡲࡢࡰࡪࡩࡷࡹࠧ௝"),l1l11_opy_ (u"ࠧ࡯ࡻࠣࡶࡦࡴࡧࡦࡴࡶࠫ௞"))
            l111lll1l_opy_ = l111lll1l_opy_.replace(l1l11_opy_ (u"ࠨࡵࡨࡲࡦࡺ࡯ࡳࡵࠪ௟"),l1l11_opy_ (u"ࠩࡲࡸࡹࡧࡷࡢࠩ௠"))
            l111lll1l_opy_ = l111lll1l_opy_.replace(l1l11_opy_ (u"ࠪࡪࡱࡿࡥࡳࡵࠪ௡"),l1l11_opy_ (u"ࠫࡵ࡮ࡩ࡭ࡣࡧࡩࡱࡶࡨࡪࡣࠪ௢"))
            l111lll1l_opy_ = l111lll1l_opy_.replace(l1l11_opy_ (u"ࠬࡶࡥ࡯ࡩࡸ࡭ࡳࡹࠧ௣"),l1l11_opy_ (u"࠭ࡰࡪࡶࡷࡷࡧࡻࡲࡨࡪࠪ௤"))
            l111lll1l_opy_ = l111lll1l_opy_.replace(l1l11_opy_ (u"ࠧࡴࡪࡤࡶࡰࡹࠧ௥"),l1l11_opy_ (u"ࠨࡵࡤࡲࠥࡰ࡯ࡴࡧࠪ௦"))
            l111lll1l_opy_ = l111lll1l_opy_.replace(l1l11_opy_ (u"ࠩࡥࡰࡺ࡫ࡳࠨ௧"),l1l11_opy_ (u"ࠪࡷࡹ࠴ࠠ࡭ࡱࡸ࡭ࡸ࠭௨"))
            l111lll1l_opy_ = l111lll1l_opy_.replace(l1l11_opy_ (u"ࠫࡱ࡯ࡧࡩࡶࡱ࡭ࡳ࡭ࠧ௩"),l1l11_opy_ (u"ࠬࡺࡡ࡮ࡲࡤࠤࡧࡧࡹࠨ௪"))
            l111lll1l_opy_ = l111lll1l_opy_.replace(l1l11_opy_ (u"࠭࡭ࡢࡲ࡯ࡩࠥࡲࡥࡢࡨࡶࠫ௫"),l1l11_opy_ (u"ࠧࡵࡱࡵࡳࡳࡺ࡯ࠨ௬"))
            l111lll1l_opy_ = l111lll1l_opy_.replace(l1l11_opy_ (u"ࠨࡥࡤࡲࡺࡩ࡫ࡴࠩ௭"),l1l11_opy_ (u"ࠩࡹࡥࡳࡩ࡯ࡶࡸࡨࡶࠬ௮"))
            l111lll1l_opy_ = l111lll1l_opy_.replace(l1l11_opy_ (u"ࠪࡧࡦࡶࡩࡵࡣ࡯ࡷࠬ௯"),l1l11_opy_ (u"ࠫࡼࡧࡳࡩ࡫ࡱ࡫ࡹࡵ࡮ࠨ௰"))
            l111lll1l_opy_ = l111lll1l_opy_.replace(l1l11_opy_ (u"ࠬࡰࡥࡵࡵࠪ௱"),l1l11_opy_ (u"࠭ࡷࡪࡰࡱ࡭ࡵ࡫ࡧࠨ௲"))
            return l111lll1l_opy_
        elif l1lllll1l1_opy_ == l1l11_opy_ (u"ࠧ࡮࡮ࡥࠫ௳"):
            l111lll1l_opy_ = l111lll1l_opy_.replace(l1l11_opy_ (u"ࠨࡦ࡬ࡥࡲࡵ࡮ࡥࡤࡤࡧࡰࡹࠧ௴"),l1l11_opy_ (u"ࠩࡤࡶ࡮ࢀ࡯࡯ࡣࠪ௵"))
            l111lll1l_opy_ = l111lll1l_opy_.replace(l1l11_opy_ (u"ࠪࡦࡷࡧࡶࡦࡵࠪ௶"),l1l11_opy_ (u"ࠫࡦࡺ࡬ࡢࡰࡷࡥࠬ௷"))
            l111lll1l_opy_ = l111lll1l_opy_.replace(l1l11_opy_ (u"ࠬࡵࡲࡪࡱ࡯ࡩࡸ࠭௸"),l1l11_opy_ (u"࠭ࡢࡢ࡮ࡷ࡭ࡲࡵࡲࡦࠩ௹"))
            l111lll1l_opy_ = l111lll1l_opy_.replace(l1l11_opy_ (u"ࠧࡳࡧࡧࠤࡸࡵࡸࠨ௺"),l1l11_opy_ (u"ࠨࡤࡲࡷࡹࡵ࡮ࠨ௻"))
            l111lll1l_opy_ = l111lll1l_opy_.replace(l1l11_opy_ (u"ࠩࡦࡹࡧࡹࠧ௼"),l1l11_opy_ (u"ࠪࡧ࡭࡯ࡣࡢࡩࡲࠤࡨࡻࡢࡴࠩ௽"))
            l111lll1l_opy_ = l111lll1l_opy_.replace(l1l11_opy_ (u"ࠫࡼ࡮ࡩࡵࡧࠣࡷࡴࡾࠧ௾"),l1l11_opy_ (u"ࠬࡩࡨࡪࡥࡤ࡫ࡴࠦࡷࡩ࡫ࡷࡩࠥࡹ࡯ࡹࠩ௿"))
            l111lll1l_opy_ = l111lll1l_opy_.replace(l1l11_opy_ (u"࠭ࡲࡦࡦࡶࠫఀ"),l1l11_opy_ (u"ࠧࡤ࡫ࡱࡧ࡮ࡴ࡮ࡢࡶ࡬ࠫఁ"))
            l111lll1l_opy_ = l111lll1l_opy_.replace(l1l11_opy_ (u"ࠨ࡫ࡱࡨ࡮ࡧ࡮ࡴࠩం"),l1l11_opy_ (u"ࠩࡦࡰࡪࡼࡥ࡭ࡣࡱࡨࠬః"))
            l111lll1l_opy_ = l111lll1l_opy_.replace(l1l11_opy_ (u"ࠪࡶࡴࡩ࡫ࡪࡧࡶࠫఄ"),l1l11_opy_ (u"ࠫࡨࡵ࡬ࡰࡴࡤࡨࡴ࠭అ"))
            l111lll1l_opy_ = l111lll1l_opy_.replace(l1l11_opy_ (u"ࠬࡺࡩࡨࡧࡵࡷࠬఆ"),l1l11_opy_ (u"࠭ࡤࡦࡶࡵࡳ࡮ࡺࠧఇ"))
            l111lll1l_opy_ = l111lll1l_opy_.replace(l1l11_opy_ (u"ࠧ࡮ࡣࡵࡰ࡮ࡴࡳࠨఈ"),l1l11_opy_ (u"ࠨ࡯࡬ࡥࡲ࡯ࠧఉ"))
            l111lll1l_opy_ = l111lll1l_opy_.replace(l1l11_opy_ (u"ࠩࡤࡷࡹࡸ࡯ࡴࠩఊ"),l1l11_opy_ (u"ࠪ࡬ࡴࡻࡳࡵࡱࡱࠫఋ"))
            l111lll1l_opy_ = l111lll1l_opy_.replace(l1l11_opy_ (u"ࠫࡷࡵࡹࡢ࡮ࡶࠫఌ"),l1l11_opy_ (u"ࠬࡱࡡ࡯ࡵࡤࡷࠥࡩࡩࡵࡻࠪ఍"))
            l111lll1l_opy_ = l111lll1l_opy_.replace(l1l11_opy_ (u"࠭ࡡ࡯ࡩࡨࡰࡸ࠭ఎ"),l1l11_opy_ (u"ࠧ࡭ࡣࠣࡥࡳ࡭ࡥ࡭ࡵࠪఏ"))
            l111lll1l_opy_ = l111lll1l_opy_.replace(l1l11_opy_ (u"ࠨࡦࡲࡨ࡬࡫ࡲࡴࠩఐ"),l1l11_opy_ (u"ࠩ࡯ࡥࠥࡪ࡯ࡥࡩࡨࡶࡸ࠭఑"))
            l111lll1l_opy_ = l111lll1l_opy_.replace(l1l11_opy_ (u"ࠪࡦࡷ࡫ࡷࡦࡴࡶࠫఒ"),l1l11_opy_ (u"ࠫࡲ࡯࡬ࡸࡣࡸ࡯ࡪ࡫ࠧఓ"))
            l111lll1l_opy_ = l111lll1l_opy_.replace(l1l11_opy_ (u"ࠬࡺࡷࡪࡰࡶࠫఔ"),l1l11_opy_ (u"࠭࡭ࡪࡰࡱࡩࡸࡵࡴࡢࠩక"))
            l111lll1l_opy_ = l111lll1l_opy_.replace(l1l11_opy_ (u"ࠧ࡮ࡧࡷࡷࠬఖ"),l1l11_opy_ (u"ࠨࡰࡼࠤࡲ࡫ࡴࡴࠩగ"))
            l111lll1l_opy_ = l111lll1l_opy_.replace(l1l11_opy_ (u"ࠩࡼࡥࡳࡱࡥࡦࡵࠪఘ"),l1l11_opy_ (u"ࠪࡲࡾࠦࡹࡢࡰ࡮ࡩࡪࡹࠧఙ"))
            l111lll1l_opy_ = l111lll1l_opy_.replace(l1l11_opy_ (u"ࠫࡦࡺࡨ࡭ࡧࡷ࡭ࡨࡹࠧచ"),l1l11_opy_ (u"ࠬࡵࡡ࡬࡮ࡤࡲࡩ࠭ఛ"))
            l111lll1l_opy_ = l111lll1l_opy_.replace(l1l11_opy_ (u"࠭ࡰࡩ࡫࡯ࡰ࡮࡫ࡳࠨజ"),l1l11_opy_ (u"ࠧࡱࡪ࡬ࡰࡦࡪࡥ࡭ࡲ࡫࡭ࡦ࠭ఝ"))
            l111lll1l_opy_ = l111lll1l_opy_.replace(l1l11_opy_ (u"ࠨࡲ࡬ࡶࡦࡺࡥࡴࠩఞ"),l1l11_opy_ (u"ࠩࡳ࡭ࡹࡺࡳࡣࡷࡵ࡫࡭࠭ట"))
            l111lll1l_opy_ = l111lll1l_opy_.replace(l1l11_opy_ (u"ࠪࡧࡦࡸࡤࡪࡰࡤࡰࡸ࠭ఠ"),l1l11_opy_ (u"ࠫࡸࡺ࠮ࠡ࡮ࡲࡹ࡮ࡹࠧడ"))
            l111lll1l_opy_ = l111lll1l_opy_.replace(l1l11_opy_ (u"ࠬࡶࡡࡥࡴࡨࡷࠬఢ"),l1l11_opy_ (u"࠭ࡳࡢࡰࠣࡨ࡮࡫ࡧࡰࠩణ"))
            l111lll1l_opy_ = l111lll1l_opy_.replace(l1l11_opy_ (u"ࠧࡨ࡫ࡤࡲࡹࡹࠧత"),l1l11_opy_ (u"ࠨࡵࡤࡲࠥ࡬ࡲࡢࡰࡦ࡭ࡸࡩ࡯ࠨథ"))
            l111lll1l_opy_ = l111lll1l_opy_.replace(l1l11_opy_ (u"ࠩࡰࡥࡷ࡯࡮ࡦࡴࡶࠫద"),l1l11_opy_ (u"ࠪࡷࡪࡧࡴࡵ࡮ࡨࠫధ"))
            l111lll1l_opy_ = l111lll1l_opy_.replace(l1l11_opy_ (u"ࠫࡷࡧࡹࡴࠩన"),l1l11_opy_ (u"ࠬࡺࡡ࡮ࡲࡤࠤࡧࡧࡹࠨ఩"))
            l111lll1l_opy_ = l111lll1l_opy_.replace(l1l11_opy_ (u"࠭ࡲࡢࡰࡪࡩࡷࡹࠧప"),l1l11_opy_ (u"ࠧࡵࡧࡻࡥࡸ࠭ఫ"))
            l111lll1l_opy_ = l111lll1l_opy_.replace(l1l11_opy_ (u"ࠨࡤ࡯ࡹࡪࠦࡪࡢࡻࡶࠫబ"),l1l11_opy_ (u"ࠩࡷࡳࡷࡵ࡮ࡵࡱࠪభ"))
            l111lll1l_opy_ = l111lll1l_opy_.replace(l1l11_opy_ (u"ࠪࡲࡦࡺࡩࡰࡰࡤࡰࡸ࠭మ"),l1l11_opy_ (u"ࠫࡼࡧࡳࡩ࡫ࡱ࡫ࡹࡵ࡮ࠨయ"))
            return l111lll1l_opy_
        return l111lll1l_opy_
    def l111l11_opy_(self, l1lllll1l1_opy_, l111ll11l_opy_=None):
        l1ll1l111l_opy_ = {}
        l11l1111l_opy_ = l1l11_opy_ (u"ࠧ࠮ࠩ࠲࠴࠶࠸࠺࠼࠷࠹࠻࠳ࠤࠧర")
        if l111ll11l_opy_:
            l111ll11l_opy_=self.l1ll1lllll_opy_(l1lllll1l1_opy_,l111ll11l_opy_.lower()).split(l1l11_opy_ (u"࠭ࠠࡁࠢࠪఱ"))
        try:
            url = l1l11_opy_ (u"ࠧࡩࡶࡷࡴ࠿࠵࠯ࡴࡲࡲࡶࡹࡹ࠮ࡦࡵࡳࡲ࠳࡭࡯࠯ࡥࡲࡱ࠴࠭ల")+l1lllll1l1_opy_+l1l11_opy_ (u"ࠨ࠱ࡥࡳࡹࡺ࡯࡮࡮࡬ࡲࡪ࠵ࡳࡤࡱࡵࡩࡸ࠭ళ")
            l1lll1l1ll_opy_ = timenow.time()
            if self.l1lllll111_opy_ is not None and self.l11111ll1_opy_ is not None and l1lll1l1ll_opy_ - self.l11111ll1_opy_ < 60 and self.l1ll11l1l1_opy_ == url:
                l111l11l1_opy_ = self.l1lllll111_opy_
            else:
                req = urllib2.Request(url)
                response = urllib2.urlopen(req)
                l111l11l1_opy_ = response.read()
                self.l1lllll111_opy_ = l111l11l1_opy_
                self.l11111ll1_opy_ = l1lll1l1ll_opy_
                self.l1ll11l1l1_opy_ = url
            data = urllib2.unquote(str(l111l11l1_opy_)).split(l1l11_opy_ (u"ࠩࠩࠫఴ")+l1lllll1l1_opy_+l1l11_opy_ (u"ࠪࡣࡸࡥ࡬ࡦࡨࡷࠫవ"))
            for i in range(1,len(data)):
                l11l11lll_opy_ = data[i][data[i].find(l1l11_opy_ (u"ࠫࡂ࠭శ"))+1:].replace(l1l11_opy_ (u"ࠬࡤࠧష"),l1l11_opy_ (u"࠭ࠧస"))
                l11l11lll_opy_ = re.sub(l1l11_opy_ (u"ࡲࠣࠨࠫ࠲࠯ࡅࠩࠧࠤహ"), l1l11_opy_ (u"ࠣࠨࠥ఺"), l11l11lll_opy_)
                time =  l11l11lll_opy_[l11l11lll_opy_.rfind(l1l11_opy_ (u"ࠩࠫࠫ఻")):l11l11lll_opy_.rfind(l1l11_opy_ (u"఼ࠪ࠭ࠬ"))+1].strip()
                score =  l11l11lll_opy_[0:l11l11lll_opy_.rfind(l1l11_opy_ (u"ࠫ࠭࠭ఽ"))].strip()
                l1lll11l1l_opy_ = l11l11lll_opy_[l11l11lll_opy_.rfind(l1l11_opy_ (u"ࠬ࡭ࡡ࡮ࡧࡌࡨࠬా"))+7:].strip()
                if l1lll11l1l_opy_ == l1l11_opy_ (u"࠭ࠧి"):
                    continue
                l1ll1l1111_opy_ = l1l11_opy_ (u"ࠧࠨీ")
                l1lll1l1l1_opy_ = l1l11_opy_ (u"ࠨ࠲ࠪు")
                l111ll111_opy_ = l1l11_opy_ (u"ࠩࠪూ")
                l11l11111_opy_ = l1l11_opy_ (u"ࠪ࠴ࠬృ")
                if (l1l11_opy_ (u"ࠫࠥࡧࡴࠡࠩౄ") not in score):
                    l111l1ll1_opy_ = score.split(l1l11_opy_ (u"ࠬࠦࠠࠨ౅"))
                    l1ll1l1111_opy_ = l111l1ll1_opy_[0][0:l111l1ll1_opy_[0].rfind(l1l11_opy_ (u"࠭ࠠࠨె"))].lstrip(l11l1111l_opy_)
                    l111ll111_opy_ = l111l1ll1_opy_[1][0:l111l1ll1_opy_[1].rfind(l1l11_opy_ (u"ࠧࠡࠩే"))].lstrip(l11l1111l_opy_)
                    l1lll1l1l1_opy_ = l111l1ll1_opy_[0][l111l1ll1_opy_[0].rfind(l1l11_opy_ (u"ࠨࠢࠪై"))+1:].strip()
                    l11l11111_opy_ = l111l1ll1_opy_[1][l111l1ll1_opy_[1].rfind(l1l11_opy_ (u"ࠩࠣࠫ౉"))+1:].strip()
                else:
                    l111l1ll1_opy_ = score.split(l1l11_opy_ (u"ࠪࠤࡦࡺࠠࠨొ"))
                    l1ll1l1111_opy_ = l111l1ll1_opy_[0].lstrip(l11l1111l_opy_)
                    l111ll111_opy_ = l111l1ll1_opy_[1].lstrip(l11l1111l_opy_)
                if not l111ll11l_opy_:
                    l1ll1l111l_opy_[l1lll11l1l_opy_] = [l1l11_opy_ (u"ࠫࠬో"),l1l11_opy_ (u"ࠬ࠭ౌ"),l1l11_opy_ (u"్࠭ࠧ"),l1l11_opy_ (u"ࠧࠨ౎"),l1l11_opy_ (u"ࠨࠩ౏")]
                    l1ll1l111l_opy_[l1lll11l1l_opy_][0] = l1ll1l1111_opy_
                    l1ll1l111l_opy_[l1lll11l1l_opy_][1] = l1lll1l1l1_opy_
                    l1ll1l111l_opy_[l1lll11l1l_opy_][2] = l111ll111_opy_
                    l1ll1l111l_opy_[l1lll11l1l_opy_][3] = l11l11111_opy_
                    l1ll1l111l_opy_[l1lll11l1l_opy_][4] = time
                elif l1ll1l1111_opy_.lower() in l111ll11l_opy_ or l111ll111_opy_.lower() in l111ll11l_opy_:
                    l1ll1l111l_opy_[l1lll11l1l_opy_] = [l1l11_opy_ (u"ࠩࠪ౐"),l1l11_opy_ (u"ࠪࠫ౑"),l1l11_opy_ (u"ࠫࠬ౒"),l1l11_opy_ (u"ࠬ࠭౓"),l1l11_opy_ (u"࠭ࠧ౔")]
                    l1ll1l111l_opy_[l1lll11l1l_opy_][0] = l1ll1l1111_opy_
                    l1ll1l111l_opy_[l1lll11l1l_opy_][1] = l1lll1l1l1_opy_
                    l1ll1l111l_opy_[l1lll11l1l_opy_][2] = l111ll111_opy_
                    l1ll1l111l_opy_[l1lll11l1l_opy_][3] = l11l11111_opy_
                    l1ll1l111l_opy_[l1lll11l1l_opy_][4] = time
                    return l1lll1l1l1_opy_,l11l11111_opy_,time
        except Exception as e:
            raise e
        return None,None,None
    l1l11_opy_ (u"ࠧࠨࠩࠍࠤࠥࠦࠠࡥࡧࡩࠤ࡬࡫ࡴࡠࡱࡧࡨࡸ࠮ࡳࡦ࡮ࡩ࠰ࠥࡲࡥࡢࡩࡸࡩ࠱ࠦࡴࡦࡣࡰࡣ࡫࡯࡬ࡵࡧࡵ࠭࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࡪࡨࠣࡸࡪࡧ࡭ࡠࡨ࡬ࡰࡹ࡫ࡲ࠻ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡵࡧࡤࡱࡤ࡬ࡩ࡭ࡶࡨࡶࡂࡺࡥࡢ࡯ࡢࡪ࡮ࡲࡴࡦࡴ࠱ࡰࡴࡽࡥࡳࠪࠬ࠲ࡸࡶ࡬ࡪࡶࠫࠫࠥࡆࠠࠨࠫࠍࠤࠥࠦࠠࠡࠢࠣࠤࡪࡲࡳࡦ࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡴࡨࡸࡺࡸ࡮ࠋࠌࠣࠤࠥࠦࠠࠡࠢࠣࡸࡷࡿ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡵࡳ࡮ࠣࡁࠥ࠭ࡨࡵࡶࡳ࠾࠴࠵ࡪࡴࡱࡱࡳࡩࡪࡳ࠯ࡥࡲࡱ࠴ࡧࡰࡪ࠱ࡲࡨࡩࡹ࠯ࠨ࠭࡯ࡩࡦ࡭ࡵࡦ࠭ࠪࡃࡴࡪࡤࡕࡻࡳࡩࡂࡍࡡ࡮ࡧࠩࡳࡩࡪࡆࡰࡴࡰࡥࡹࡃࡁ࡮ࡧࡵ࡭ࡨࡧ࡮ࠨࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡰࡦࡧࡷࡤࡩࡵࡳࡴࡨࡲࡹࡥࡴࡪ࡯ࡨࠤࡂࠦࡴࡪ࡯ࡨࡲࡴࡽ࠮ࡵ࡫ࡰࡩ࠭࠯ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥ࡯ࡦࠡࡵࡨࡰ࡫࠴࡯ࡥࡦࡶࡣࡨࡧࡣࡩࡧࠣ࡭ࡸࠦ࡮ࡰࡶࠣࡒࡴࡴࡥࠡࡣࡱࡨࠥࡹࡥ࡭ࡨ࠱ࡳࡩࡪࡳࡠࡥࡤࡧ࡭࡫࡟ࡵ࡫ࡰࡩࠥ࡯ࡳࠡࡰࡲࡸࠥࡔ࡯࡯ࡧࠣࡥࡳࡪࠠࡰࡦࡧࡷࡤࡩࡵࡳࡴࡨࡲࡹࡥࡴࡪ࡯ࡨࠤ࠲ࠦࡳࡦ࡮ࡩ࠲ࡴࡪࡤࡴࡡࡦࡥࡨ࡮ࡥࡠࡶ࡬ࡱࡪࠦ࠼ࠡ࠸࠳ࠤࡦࡴࡤࠡࡵࡨࡰ࡫࠴࡯ࡥࡦࡶࡣࡨࡧࡣࡩࡧࡢࡹࡷࡲࠠ࠾࠿ࠣࡹࡷࡲ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡳࡩࡪࡳࡠ࡬ࡶࡳࡳࠦ࠽ࠡࡵࡨࡰ࡫࠴࡯ࡥࡦࡶࡣࡨࡧࡣࡩࡧࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡧ࡯ࡷࡪࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡲࡨࡩࡹ࡟࡫ࡵࡲࡲࠥࡃࠠ࡫ࡵࡲࡲ࠳ࡲ࡯ࡢࡦࡶࠬࡷ࡫ࡱࡶࡧࡶࡸࡸ࠴ࡧࡦࡶࠫࡹࡷࡲࠬࠡࡪࡨࡥࡩ࡫ࡲࡴ࠿ࡾࠦࡏࡹ࡯࡯ࡑࡧࡨࡸ࠳ࡁࡑࡋ࠰ࡏࡪࡿࠢ࠻ࠤ࠸࠶ࡧ࡬ࡣࡣ࠳ࡩ࠱࠼࠹࠷࠸࠯࠷࠼࠵࠶࠭ࡢ࠶ࡧ࠵࠲࠶࠸ࡢࡦ࠶࠵ࡧ࠽ࡦࡦ࠺࠸ࠦࢂ࠯࠮ࡤࡱࡱࡸࡪࡴࡴࠪࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡸ࡫࡬ࡧ࠰ࡲࡨࡩࡹ࡟ࡤࡣࡦ࡬ࡪࠦ࠽ࠡࡱࡧࡨࡸࡥࡪࡴࡱࡱࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡳࡦ࡮ࡩ࠲ࡴࡪࡤࡴࡡࡦࡥࡨ࡮ࡥࡠࡶ࡬ࡱࡪࠦ࠽ࠡࡱࡧࡨࡸࡥࡣࡶࡴࡵࡩࡳࡺ࡟ࡵ࡫ࡰࡩࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡴࡧ࡯ࡪ࠳ࡵࡤࡥࡵࡢࡧࡦࡩࡨࡦࡡࡸࡶࡱࠦ࠽ࠡࡷࡵࡰࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡨࡲࡶࠥ࡭ࡡ࡮ࡧࠣ࡭ࡳࠦ࡯ࡥࡦࡶࡣ࡯ࡹ࡯࡯࠼ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡎ࡯࡮ࡧࡗࡩࡦࡳࠠ࠾ࠢࡪࡥࡲ࡫࡛ࠨࡊࡲࡱࡪ࡚ࡥࡢ࡯ࠪࡡ࠳ࡲ࡯ࡸࡧࡵࠬ࠮ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡃࡺࡥࡾ࡚ࡥࡢ࡯ࠣࡁࠥ࡭ࡡ࡮ࡧ࡞ࠫࡆࡽࡡࡺࡖࡨࡥࡲ࠭࡝࠯࡮ࡲࡻࡪࡸࠨࠪࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤ࡮࡬ࠠࠩࡣࡱࡽ࠭ࡽ࡯ࡳࡦࠣ࡭ࡳࠦࡈࡰ࡯ࡨࡘࡪࡧ࡭ࠡࡨࡲࡶࠥࡽ࡯ࡳࡦࠣ࡭ࡳࠦࡴࡦࡣࡰࡣ࡫࡯࡬ࡵࡧࡵ࠭ࠥࡵࡲࠡࡣࡱࡽ࠭ࡽ࡯ࡳࡦࠣ࡭ࡳࠦࡁࡸࡣࡼࡘࡪࡧ࡭ࠡࡨࡲࡶࠥࡽ࡯ࡳࡦࠣ࡭ࡳࠦࡴࡦࡣࡰࡣ࡫࡯࡬ࡵࡧࡵ࠭࠮ࡀࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡐࡰ࡫ࡱࡸࡘࡶࡲࡦࡣࡧࡌࡴࡳࡥࠡ࠿ࠣ࡫ࡦࡳࡥ࡜ࠩࡒࡨࡩࡹࠧ࡞࡝࠳ࡡࡠ࠭ࡐࡰ࡫ࡱࡸࡘࡶࡲࡦࡣࡧࡌࡴࡳࡥࠨ࡟ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡓࡳ࡮ࡴࡴࡔࡲࡵࡩࡦࡪࡁࡸࡣࡼࠤࡂࠦࡧࡢ࡯ࡨ࡟ࠬࡕࡤࡥࡵࠪࡡࡠ࠶࡝࡜ࠩࡓࡳ࡮ࡴࡴࡔࡲࡵࡩࡦࡪࡁࡸࡣࡼࠫࡢࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࡕࡶࡦࡴࡏ࡭ࡳ࡫ࠠ࠾ࠢࡪࡥࡲ࡫࡛ࠨࡑࡧࡨࡸ࠭࡝࡜࠲ࡠ࡟ࠬࡕࡶࡦࡴࡏ࡭ࡳ࡫ࠧ࡞ࠌࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡗࡱࡨࡪࡸࡌࡪࡰࡨࠤࡂࠦࡧࡢ࡯ࡨ࡟ࠬࡕࡤࡥࡵࠪࡡࡠ࠶࡝࡜ࠩࡘࡲࡩ࡫ࡲࡍ࡫ࡱࡩࠬࡣࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡲࡦࡶࡸࡶࡳࠦࡐࡰ࡫ࡱࡸࡘࡶࡲࡦࡣࡧࡌࡴࡳࡥ࠭ࡒࡲ࡭ࡳࡺࡓࡱࡴࡨࡥࡩࡇࡷࡢࡻ࠯ࡓࡻ࡫ࡲࡍ࡫ࡱࡩ࠱࡛࡮ࡥࡧࡵࡐ࡮ࡴࡥࠋࠢࠣࠤࠥࠦࠠࠡࠢࡨࡼࡨ࡫ࡰࡵࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡧࡳࠡࡧ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡵࡥ࡮ࡹࡥࠡࡧࠍࠤࠥࠦࠠࠡࠢࠣࠤࡷ࡫ࡴࡶࡴࡱࠤࡓࡵ࡮ࡦ࠮ࡑࡳࡳ࡫ࠬࡏࡱࡱࡩ࠱ࡔ࡯࡯ࡧࠍࠤࠥࠦࠠࠡࠢࠣࠤౕࠬ࠭ࠧ")
    def l1lll11ll1_opy_(self, l1111ll1l_opy_):
        req = urllib2.Request(self.l1lllllll1_opy_+l1111ll1l_opy_)
        req.add_header(l1l11_opy_ (u"ࠣࡗࡶࡩࡷ࠳ࡁࡨࡧࡱࡸౖࠧ") , l1l11_opy_ (u"ࠤࡕࡩࡱࡵࡡࡥࡧࡧࠤࡐࡵࡤࡪࠢࡄࡨࡩࡵ࡮ࠡࡤࡼࠤࡒࡧࡹࡧࡣ࡬ࡶࠥࡼࡥࡳࠢࠥ౗") + self.l11l_opy_)
        response = urllib2.urlopen(req)
        link=response.read()
        l1ll1l1l11_opy_ = json.loads(link.decode(l1l11_opy_ (u"ࠪࡹࡹ࡬࠸ࠨౘ")))[l1l11_opy_ (u"ࠫࡪࡶࡧࡠ࡮࡬ࡷࡹ࡯࡮ࡨࡵࠪౙ")]
        response.close()
        if l1ll1l1l11_opy_:
            return l1ll1l1l11_opy_
    def l1l1l1l1_opy_(self, l1111ll1l_opy_):
        try:
            l1ll1l1l11_opy_ = self.l1lll11ll1_opy_(l1111ll1l_opy_)
            for item in l1ll1l1l11_opy_:
                if item[l1l11_opy_ (u"ࠬ࡮ࡡࡴࡡࡤࡶࡨ࡮ࡩࡷࡧࠪౚ")] != 0:
                    return True
            return False
        except:
            return False
    def l1ll1l_opy_(self, l1111ll1l_opy_, l1lllll11l_opy_, i):
        try:
            xbmc.executebuiltin(l1l11_opy_ (u"ࠨࡄࡪࡣ࡯ࡳ࡬࠴ࡃ࡭ࡱࡶࡩ࠭ࡨࡵࡴࡻࡧ࡭ࡦࡲ࡯ࡨࠫࠥ౛"))
            l111111l1_opy_ = []
            l1ll1l1l11_opy_ = self.l1lll11ll1_opy_(l1111ll1l_opy_)
            for item in l1ll1l1l11_opy_:
                if item[l1l11_opy_ (u"ࠧࡩࡣࡶࡣࡦࡸࡣࡩ࡫ࡹࡩࠬ౜")] != 0:
                    l111111l1_opy_.append(item)
            if l111111l1_opy_:
                d = l11l11ll1_opy_(l1l11_opy_ (u"ࠨ࡝ࡅࡡࠬౝ")+self.title+l1l11_opy_ (u"ࠩࠣ࠱࡚ࠥࡖࡄࡣࡷࡧ࡭ࡻࡰࠡࡨࡲࡶࠥࡡ࠯ࡃ࡟ࠪ౞")+l1lllll11l_opy_,l111111l1_opy_,l1111ll1l_opy_,self.i)
                d.doModal()
                l1111l_opy_ = d.l1111l_opy_
                l111_opy_ = d.l111_opy_
                l1111l1ll_opy_ = d.l1111l1ll_opy_
                l1lll1l111_opy_ = d.l1lll1l111_opy_
                del d
                if l1111l_opy_ is not None:
                    xbmc.executebuiltin(l1l11_opy_ (u"ࠥࡅࡨࡺࡩࡷࡣࡷࡩ࡜࡯࡮ࡥࡱࡺࠬࡧࡻࡳࡺࡦ࡬ࡥࡱࡵࡧࠪࠤ౟"))
                    i.l1l11l1l_opy_(l1111l_opy_, l111_opy_, l1111l1ll_opy_, l1lll1l111_opy_)
        except:
            xbmc.executebuiltin(l1l11_opy_ (u"ࠦࡉ࡯ࡡ࡭ࡱࡪ࠲ࡈࡲ࡯ࡴࡧࠫࡦࡺࡹࡹࡥ࡫ࡤࡰࡴ࡭ࠩࠣౠ"))
            pass
    class Channel(object):
        def __init__(self, id, title, logo=None, l1l1l1l_opy_=None, l11ll1_opy_=l1l11_opy_ (u"ࠧࠨౡ"), l1lll11l_opy_=l1l11_opy_ (u"ࠨࠢౢ"), l1llllll_opy_=l1l11_opy_ (u"ࠢࠣౣ"), l11llll1_opy_=l1l11_opy_ (u"ࠣࠤ౤"), l1ll11_opy_=l1l11_opy_ (u"ࠤࠥ౥")):
            self.id = id
            self.title = title
            self.logo = logo
            self.l1l1l1l_opy_ = l1l1l1l_opy_
            self.l11ll1_opy_ = l11ll1_opy_
            self.l1lll11l_opy_ = l1lll11l_opy_
            self.l1llllll_opy_ = l1llllll_opy_
            self.l11llll1_opy_ = l11llll1_opy_
            self.l1ll11_opy_ = l1ll11_opy_
        def isPlayable(self):
            return hasattr(self, l1l11_opy_ (u"ࠪࡷࡹࡸࡥࡢ࡯ࡘࡶࡱ࠭౦")) and self.l1l1l1l_opy_
        def __eq__(self, other):
            return self.id == other.id
        def __repr__(self):
            return l1l11_opy_ (u"ࠫࡈ࡮ࡡ࡯ࡰࡨࡰ࠭࡯ࡤ࠾ࠧࡶ࠰ࠥࡺࡩࡵ࡮ࡨࡁࠪࡹࠬࠡ࡮ࡲ࡫ࡴࡃࠥࡴ࠮ࠣࡷࡹࡸࡥࡢ࡯ࡘࡶࡱࡃࠥࡴ࠮ࠣࡲࡴࡽࡰࡳࡱࡪࡸ࡮ࡺ࡬ࡦ࠿ࠨࡷ࠱ࠦ࡮ࡰࡹࡳࡶࡴ࡭ࡤࡦࡵࡦࡁࠪࡹࠬࠡࡥ࡫ࡲࡵࡸ࡯ࡨࡶ࡬ࡱࡪࡲࡥࡧࡶࡀࠩࡸ࠲ࠠ࡯ࡧࡻࡸࡵࡸ࡯ࡨࡶ࡬ࡸࡱ࡫࠽ࠦࡵ࠯ࠤࡳ࡫ࡸࡵࡲࡵࡳ࡬ࡪࡥࡴࡥࡀࠩࡸ࠯ࠧ౧") \
                   % (self.id, self.title, self.logo, self.l1l1l1l_opy_, self.l11ll1_opy_, self.l1lll11l_opy_, self.l1llllll_opy_, self.l11llll1_opy_, self.l1ll11_opy_)
class l11l11ll1_opy_(xbmcgui.WindowXMLDialog):
    l1ll1l1ll1_opy_ = 1000
    l1lll111ll_opy_ = 1001
    l1111l1l1_opy_ = 9999
    l111l111l_opy_ = 6969
    l1ll11llll_opy_ = 1
    l1lll11l11_opy_ = 2
    l1lll1111l_opy_ = 3
    l111l1l1l_opy_ = 4
    l111l1lll_opy_ = 7
    l111111_opy_ = 9
    l1lll1_opy_ = 10
    l1111llll_opy_ = 100
    l1lll1l1_opy_ = 92
    l1l1lll1_opy_ = 117
    l1llll11l1_opy_ = 61467
    def __new__(cls,title,l111111l1_opy_,l1111ll1l_opy_,instance,l111l1l11_opy_=True):
        return super(l11l11ll1_opy_, cls).__new__(cls, l1l11_opy_ (u"ࠬࡹࡣࡳ࡫ࡳࡸ࠲ࡸࡥ࡭ࡱࡤࡨࡪࡪࡣࡢࡶࡦ࡬ࡺࡶ࠮ࡹ࡯࡯ࠫ౨"), l11ll111_opy_, instance.skin)
    def __init__(self,title,l111111l1_opy_,l1111ll1l_opy_,instance,l111l1l11_opy_=True):
        super(l11l11ll1_opy_, self).__init__()
        self.title = title
        self.l111111l1_opy_ = l111111l1_opy_
        self.index = -1
        self.action = None
        self.l111l1l11_opy_ = l111l1l11_opy_
        self.l1lll1l11l_opy_ = False
        self.l111l1111_opy_ = False
        self.l1llll1111_opy_ = False
        self.init = False
        self.l1111ll1l_opy_ = l1111ll1l_opy_
        self.l1111l_opy_ = None
        self.l111_opy_ = None
        self.l1111l1ll_opy_ = None
        self.l1lll1l111_opy_ = None
        self.i = instance
        self.skin = self.i.skin
        if self.skin == l1l11_opy_ (u"࠭ࡄࡢࡴ࡮ࠫ౩"):
            self.l1llll1l1l_opy_ = l1l11_opy_ (u"ࠧࡥࡣࡵ࡯࡬ࡸࡥࡺࠩ౪")
        else:
            self.l1llll1l1l_opy_ = l1l11_opy_ (u"ࠨࡤ࡯ࡥࡨࡱࠧ౫")
    def onInit(self):
        if self.init:
            return
        control = self.getControl(l11l11ll1_opy_.l1lll111ll_opy_)
        control.setLabel(self.title)
        items = list()
        index = 0
        for item in self.l111111l1_opy_:
            label = item[l1l11_opy_ (u"ࠩࡷ࡭ࡹࡲࡥࠨ౬")]
            label = base64.b64decode(label).replace(l1l11_opy_ (u"ࠪ࠳ࠬ౭"),l1l11_opy_ (u"ࠫ࠲࠭౮"))
            label = l1l11_opy_ (u"ࠬࡡࡂ࡞ࠩ౯")+label+l1l11_opy_ (u"࡛࠭࠰ࡄࡠࠫ౰")
            if label == l1l11_opy_ (u"ࠢࠣ౱"):
                label = l1l11_opy_ (u"ࠣ࡝ࡅࡡࡓࡵࠠࡱࡴࡲ࡫ࡷࡧ࡭ࠡࡣࡹࡥ࡮ࡲࡡࡣ࡮ࡨ࡟࠴ࡈ࡝ࠣ౲")
            l1lllll1ll_opy_ = item[l1l11_opy_ (u"ࠩࡧࡩࡸࡩࡲࡪࡲࡷ࡭ࡴࡴࠧ౳")]
            l1lllll1ll_opy_ = base64.b64decode(l1lllll1ll_opy_).replace(l1l11_opy_ (u"ࠪ࠳ࠬ౴"),l1l11_opy_ (u"ࠫ࠲࠭౵"))
            if l1lllll1ll_opy_ == l1l11_opy_ (u"ࠧࠨ౶"):
                l1lllll1ll_opy_ = l1l11_opy_ (u"ࠨࡎࡰࠢࡳࡶࡴ࡭ࡲࡢ࡯ࠣࡥࡻࡧࡩ࡭ࡣࡥࡰࡪࠨ౷")
            l1llll11ll_opy_ = l1l11_opy_ (u"ࠢࠣ౸")
            name = label
            l11ll1ll_opy_ = l1l11_opy_ (u"ࠨࠩ౹")
            l11111l1l_opy_ = l1l11_opy_ (u"ࠩࠪ౺")#self.l11111l11_opy_(label)
            l1ll1l11l1_opy_ = int(item[l1l11_opy_ (u"ࠪࡷࡹࡧࡲࡵࡡࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬ౻")])
            l1ll1ll1l1_opy_ = int(item[l1l11_opy_ (u"ࠫࡸࡺ࡯ࡱࡡࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬ౼")])
            l1111ll11_opy_ = int((l1ll1ll1l1_opy_-l1ll1l11l1_opy_)/60) + 5
            l1111l111_opy_ = datetime.datetime.utcfromtimestamp(int(l1ll1l11l1_opy_)).strftime(l1l11_opy_ (u"࡙ࠬࠫ࠮ࠧࡰ࠱ࠪࡪ࠺ࠦࡊ࠰ࠩࡒ࠭౽"))
            url = self.i.l11l11l1l_opy_+l1l11_opy_ (u"࠭࠯ࡵ࡫ࡰࡩࡸ࡮ࡩࡧࡶ࠲ࠩࡸ࠵ࠥࡴ࠱ࠨࡷ࠴ࠫࡳ࠰ࠧࡶ࠲ࡹࡹࠧ౾") %(self.i.username,self.i.password,l1111ll11_opy_,l1111l111_opy_,self.l1111ll1l_opy_)
            item = xbmcgui.ListItem(l1l11_opy_ (u"ࠧࠨ౿"), name, l11ll1ll_opy_)
            item.setProperty(l1l11_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧಀ"), str(index))
            index = index + 1
            item.setProperty(l1l11_opy_ (u"ࠩࡓࡶࡴ࡭ࡲࡢ࡯ࡑࡥࡲ࡫ࠧಁ"), l1l11_opy_ (u"ࠥ࡟ࡈࡕࡌࡐࡔࠣࠩࡸࡣࠥࡴ࡝࠲ࡇࡔࡒࡏࡓ࡟ࠥಂ") % (self.l1llll1l1l_opy_, label))
            item.setProperty(l1l11_opy_ (u"ࠫࡕࡲ࡯ࡵࠩಃ"), l1l11_opy_ (u"ࠧࡡࡃࡐࡎࡒࡖࠥࠫࡳ࡞ࠧࡶ࡟࠴ࡉࡏࡍࡑࡕࡡࠧ಄") % (self.l1llll1l1l_opy_, l1lllll1ll_opy_))
            item.setProperty(l1l11_opy_ (u"࠭ࡵ࡯࡫ࡻࡗࡹࡧࡲࡵࡖ࡬ࡱࡪ࠭ಅ"), str(l1ll1l11l1_opy_))
            item.setProperty(l1l11_opy_ (u"ࠧࡶࡴ࡯ࠫಆ"),url)
            try:
                start = datetime.datetime.strptime(datetime.datetime.fromtimestamp(l1ll1l11l1_opy_).strftime(l1l11_opy_ (u"ࠨࠧ࡜࠱ࠪࡳ࠭ࠦࡦࠣࠩࡍࡀࠥࡎ࠼ࠨࡗ࠳ࠫࡦࠨಇ")),l1l11_opy_ (u"ࠩࠨ࡝࠲ࠫ࡭࠮ࠧࡧࠤࠪࡎ࠺ࠦࡏ࠽ࠩࡘ࠴ࠥࡧࠩಈ"))
            except TypeError:
                start = datetime.datetime(*(timenow.strptime(datetime.datetime.fromtimestamp(l1ll1l11l1_opy_).strftime(l1l11_opy_ (u"ࠪࠩ࡞࠳ࠥ࡮࠯ࠨࡨࠥࠫࡈ࠻ࠧࡐ࠾࡙ࠪ࠮ࠦࡨࠪಉ")), l1l11_opy_ (u"ࠫࠪ࡟࠭ࠦ࡯࠰ࠩࡩࠦࠥࡉ࠼ࠨࡑ࠿ࠫࡓ࠯ࠧࡩࠫಊ"))[0:6]))
            try:
                end = datetime.datetime.strptime(datetime.datetime.fromtimestamp(l1ll1ll1l1_opy_).strftime(l1l11_opy_ (u"࡙ࠬࠫ࠮ࠧࡰ࠱ࠪࡪࠠࠦࡊ࠽ࠩࡒࡀࠥࡔ࠰ࠨࡪࠬಋ")),l1l11_opy_ (u"࡚࠭ࠥ࠯ࠨࡱ࠲ࠫࡤࠡࠧࡋ࠾ࠪࡓ࠺ࠦࡕ࠱ࠩ࡫࠭ಌ"))
            except TypeError:
                end = datetime.datetime(*(timenow.strptime(datetime.datetime.fromtimestamp(l1ll1ll1l1_opy_).strftime(l1l11_opy_ (u"࡛ࠧࠦ࠰ࠩࡲ࠳ࠥࡥࠢࠨࡌ࠿ࠫࡍ࠻ࠧࡖ࠲ࠪ࡬ࠧ಍")), l1l11_opy_ (u"ࠨࠧ࡜࠱ࠪࡳ࠭ࠦࡦࠣࠩࡍࡀࠥࡎ࠼ࠨࡗ࠳ࠫࡦࠨಎ"))[0:6]))
            now = datetime.datetime.now()
            if now > start:
                l1ll1ll1ll_opy_ = datetime.timedelta(-1)
                l111lll11_opy_ = now - start
            else:
                l1ll1ll1ll_opy_ = start - now
                l111lll11_opy_ = datetime.timedelta(0)
            day = self.l111ll1ll_opy_(start)
            l11l111l1_opy_ = start.strftime(l1l11_opy_ (u"ࠤࠨࡍ࠿ࠫࡍࠡࠧࡳࠦಏ"))
            l11l111l1_opy_ = l1l11_opy_ (u"ࠥࠩࡸࠦࠥࡴࠤಐ") % (day,l11l111l1_opy_)
            if self.skin == l1l11_opy_ (u"ࠫࡉࡧࡲ࡬ࠩ಑"):
                item.setProperty(l1l11_opy_ (u"࡙ࠬࡴࡢࡴࡷࡘ࡮ࡳࡥࠨಒ"), l1l11_opy_ (u"ࠨ࡛ࡄࡑࡏࡓࡗࠦࡤࡢࡴ࡮࡫ࡷ࡫ࡹ࡞ࠤಓ")+l11l111l1_opy_+l1l11_opy_ (u"ࠢ࡜࠱ࡆࡓࡑࡕࡒ࡞ࠤಔ"))
            else:
                item.setProperty(l1l11_opy_ (u"ࠨࡕࡷࡥࡷࡺࡔࡪ࡯ࡨࠫಕ"), l11l111l1_opy_)
            l1llllll1l_opy_ = l1l11_opy_ (u"ࠤࡇࡹࡷࡧࡴࡪࡱࡱ࠾ࠥࡡࡂ࡞࡝ࡆࡓࡑࡕࡒࠡ࡮࡬ࡱࡪ࡭ࡲࡦࡧࡱࡡࠪࡪ࡛࠰ࡅࡒࡐࡔࡘ࡝࡜࠱ࡅࡡࠥࡳࡩ࡯ࡷࡷࡩࡸࠨಖ") % (l1111ll11_opy_ - 5)
            item.setProperty(l1l11_opy_ (u"ࠪࡈࡺࡸࡡࡵ࡫ࡲࡲࠬಗ"), l1llllll1l_opy_)
            item.setProperty(l1l11_opy_ (u"ࠫࡕࡸ࡯ࡨࡴࡤࡱࡎࡳࡡࡨࡧࠪಘ"), l1l11_opy_ (u"ࠬ࠭ಙ"))
            items.append(item)
        if self.l111l1l11_opy_ == True:
            items = sorted(items, key=lambda x: x.getProperty(l1l11_opy_ (u"࠭ࡵ࡯࡫ࡻࡗࡹࡧࡲࡵࡖ࡬ࡱࡪ࠭ಚ")), reverse=True)
        if self.l1lll1l11l_opy_ == True:
            items = sorted(items, key=lambda x: x.getProperty(l1l11_opy_ (u"ࠧࡑࡴࡲ࡫ࡷࡧ࡭ࡏࡣࡰࡩࠬಛ")))
        l1llll1lll_opy_ = self.getControl(l11l11ll1_opy_.l1ll1l1ll1_opy_)
        l1llll1lll_opy_.addItems(items)
        self.setFocus(l1llll1lll_opy_)
        self.init = True
        thread.start_new_thread(self.l1ll1llll1_opy_, ())
    def onAction(self, action):
        l1llll1lll_opy_ = self.getControl(self.l1ll1l1ll1_opy_)
        self.id = self.getFocusId(self.l1ll1l1ll1_opy_)
        item = l1llll1lll_opy_.getSelectedItem()
        if action.getId() in [self.l111111_opy_, self.l1lll1l1_opy_, self.l1l1lll1_opy_, self.l1lll1_opy_]:
            self.index = -1
            self.close()
        elif action.getId() in [self.l111l1lll_opy_, self.l1111llll_opy_]:
            self.index = int(item.getProperty(l1l11_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧಜ")))
            self.l1111l_opy_ = item.getProperty(l1l11_opy_ (u"ࠩࡸࡶࡱ࠭ಝ"))
            self.l111_opy_ = item.getProperty(l1l11_opy_ (u"ࠪࡔࡷࡵࡧࡳࡣࡰࡒࡦࡳࡥࠨಞ"))
            self.l1111l1ll_opy_ = item.getProperty(l1l11_opy_ (u"ࠫࡕࡲ࡯ࡵࠩಟ"))
            self.l1lll1l111_opy_ = item.getProperty(l1l11_opy_ (u"ࠬࡖࡲࡰࡩࡵࡥࡲࡏ࡭ࡢࡩࡨࠫಠ"))
            self.close()
        else:
            self.index = -1
    def onClick(self, controlId):
        if controlId == self.l1ll1l1ll1_opy_:
            l1llll1lll_opy_ = self.getControl(self.l1ll1l1ll1_opy_)
            self.id = self.getFocusId(self.l1ll1l1ll1_opy_)
            item = l1llll1lll_opy_.getSelectedItem()
            if item:
                self.index = int(item.getProperty(l1l11_opy_ (u"࠭ࡩ࡯ࡦࡨࡼࠬಡ")))
                self.l1111l_opy_ = item.getProperty(l1l11_opy_ (u"ࠧࡶࡴ࡯ࠫಢ"))
                self.l111_opy_ = item.getProperty(l1l11_opy_ (u"ࠨࡒࡵࡳ࡬ࡸࡡ࡮ࡐࡤࡱࡪ࠭ಣ"))
                self.l1111l1ll_opy_ = item.getProperty(l1l11_opy_ (u"ࠩࡓࡰࡴࡺࠧತ"))
                self.l1lll1l111_opy_ = item.getProperty(l1l11_opy_ (u"ࠪࡔࡷࡵࡧࡳࡣࡰࡍࡲࡧࡧࡦࠩಥ"))
                self.close()
            else:
                self.index = -1
    def onFocus(self, controlId):
        pass
    def l111ll1ll_opy_(self, l111llll1_opy_):
        if l111llll1_opy_:
            today = datetime.datetime.today()
            l1lll1lll1_opy_ = today + datetime.timedelta(days=1)
            l1ll1l1l1l_opy_ = today - datetime.timedelta(days=1)
            if today.date() == l111llll1_opy_.date():
                return l1l11_opy_ (u"࡙ࠫࡵࡤࡢࡻࠪದ")
            elif l1lll1lll1_opy_.date() == l111llll1_opy_.date():
                return l1l11_opy_ (u"࡚ࠬ࡯࡮ࡱࡵࡶࡴࡽࠧಧ")
            elif l1ll1l1l1l_opy_.date() == l111llll1_opy_.date():
                return l1l11_opy_ (u"࡙࠭ࡦࡵࡷࡩࡷࡪࡡࡺࠩನ")
            else:
                return l111llll1_opy_.strftime(l1l11_opy_ (u"ࠢࠦࡃࠥ಩"))
    def l1ll1llll1_opy_(self):
        l1ll1l11ll_opy_ = self.getControl(l11l11ll1_opy_.l1ll1l1ll1_opy_)
        l1111lll1_opy_ = l1ll1l11ll_opy_.size()
        for i in range(l1111lll1_opy_):
            l1llllllll_opy_ = l1ll1l11ll_opy_.getListItem(i).getProperty(l1l11_opy_ (u"ࠨࡒࡵࡳ࡬ࡸࡡ࡮ࡐࡤࡱࡪ࠭ಪ"))
            l1llllllll_opy_ = l1llllllll_opy_.replace(l1l11_opy_ (u"ࠩ࡞ࡇࡔࡒࡏࡓࠢࡥࡰࡦࡩ࡫࡞ࠩಫ"),l1l11_opy_ (u"ࠪࠫಬ")).replace(l1l11_opy_ (u"ࠫࡠࡉࡏࡍࡑࡕࠤࡩࡧࡲ࡬ࡩࡵࡩࡾࡣࠧಭ"),l1l11_opy_ (u"ࠬ࠭ಮ")).replace(l1l11_opy_ (u"࡛࠭࠰ࡅࡒࡐࡔࡘ࡝ࠨಯ"),l1l11_opy_ (u"ࠧࠨರ")).replace(l1l11_opy_ (u"ࠨ࡝ࡅࡡࠬಱ"),l1l11_opy_ (u"ࠩࠪಲ")).replace(l1l11_opy_ (u"ࠪ࡟࠴ࡈ࡝ࠨಳ"),l1l11_opy_ (u"ࠫࠬ಴"))
            url = l1l11_opy_ (u"ࠧ࡮ࡴࡵࡲ࠽࠳࠴ࡧࡰࡪ࠰ࡷ࡬ࡪࡳ࡯ࡷ࡫ࡨࡨࡧ࠴࡯ࡳࡩ࠲࠷࠴ࡹࡥࡢࡴࡦ࡬࠴ࡳࡵ࡭ࡶ࡬ࡃ࡮ࡴࡣ࡭ࡷࡧࡩࡤࡧࡤࡶ࡮ࡷࡁࡹࡸࡵࡦࠨࡳࡥ࡬࡫࠽࠲ࠨࡴࡹࡪࡸࡹ࠾ࠧࡶࠪࡱࡧ࡮ࡨࡷࡤ࡫ࡪࡃࡥ࡯࠯ࡘࡗࠫࡧࡰࡪࡡ࡮ࡩࡾࡃ࠶ࡢ࠳ࡦ࠼ࡩ࠻࠸ࡦ࠴࠷ࡦ࠷࠿࠰ࡣ࠻ࡩࡩ࠽ࡨ࠱ࡣ࠴ࡦ࠽࠷࠺ࡣ࠱࠺ࡨࠦವ")%(urllib.quote_plus(l1llllllll_opy_))
            req = urllib2.Request(url)
            req.add_header(l1l11_opy_ (u"ࠨࡕࡴࡧࡵ࠱ࡆ࡭ࡥ࡯ࡶࠥಶ") , l1l11_opy_ (u"ࠢࡎࡱࡽ࡭ࡱࡲࡡ࠰࠷࠱࠴ࠥ࠮ࡗࡪࡰࡧࡳࡼࡹࠠࡏࡖࠣ࠺࠳࠷ࠩࠡࡃࡳࡴࡱ࡫ࡗࡦࡤࡎ࡭ࡹ࠵࠵࠴࠹࠱࠷࠻ࠦࠨࡌࡊࡗࡑࡑ࠲ࠠ࡭࡫࡮ࡩࠥࡍࡥࡤ࡭ࡲ࠭ࠥࡉࡨࡳࡱࡰࡩ࠴࠺࠱࠯࠲࠱࠶࠷࠸࠸࠯࠲ࠣࡗࡦ࡬ࡡࡳ࡫࠲࠹࠸࠽࠮࠴࠸ࠥಷ"))
            response = urllib2.urlopen(req)
            link=response.read()
            try:
                l11l111ll_opy_ = json.loads(link.decode(l1l11_opy_ (u"ࠨࡷࡷࡪ࠽࠭ಸ")))[l1l11_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࡵࠪಹ")][0][l1l11_opy_ (u"ࠪࡦࡦࡩ࡫ࡥࡴࡲࡴࡤࡶࡡࡵࡪࠪ಺")]
                l1ll1l1lll_opy_ = l1ll1l11ll_opy_.getListItem(i).setProperty(l1l11_opy_ (u"ࠫࡕࡸ࡯ࡨࡴࡤࡱࡎࡳࡡࡨࡧࠪ಻"), l1l11_opy_ (u"ࠬ࡮ࡴࡵࡲ࠽࠳࠴࡯࡭ࡢࡩࡨ࠲ࡹࡳࡤࡣ࠰ࡲࡶ࡬࠵ࡴ࠰ࡲ࠲ࡻ࠼࠾࠰࠰಼ࠩ")+l11l111ll_opy_)
            except:
                l1ll1l1lll_opy_ = l1ll1l11ll_opy_.getListItem(i).setProperty(l1l11_opy_ (u"࠭ࡐࡳࡱࡪࡶࡦࡳࡉ࡮ࡣࡪࡩࠬಽ"), l1l11_opy_ (u"ࠧࡳࡧ࡯ࡳࡦࡪࡥࡥࡶࡹ࠳ࡳࡵ࡬ࡰࡩࡲ࠲ࡵࡴࡧࠨಾ"))
            response.close()
        return
    def close(self):
        if not self.l111l1111_opy_:
            self.l111l1111_opy_ = True
        super(l11l11ll1_opy_, self).close()