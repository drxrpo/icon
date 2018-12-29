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
import calendar
from datetime import datetime
import os
import sys
import time
import re
from traceback import format_exc
import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin
import xbmcvfs
import json
from resources.lib.helper import helper
addon = xbmcaddon.Addon(id=l1l11_opy_ (u"ࠫࡵࡲࡵࡨ࡫ࡱ࠲ࡻ࡯ࡤࡦࡱ࠱ࡶࡪࡲ࡯ࡢࡦࡨࡨࡹࡼࠧࠀ"))
l11llll_opy_ = xbmcgui.Dialog()
l11ll111_opy_ = xbmc.translatePath(addon.getAddonInfo(l1l11_opy_ (u"ࠬࡶࡡࡵࡪࠪࠁ")))
l1ll_opy_ = xbmc.translatePath(addon.getAddonInfo(l1l11_opy_ (u"࠭ࡰࡳࡱࡩ࡭ࡱ࡫ࠧࠂ")))
l1ll111_opy_ = xbmc.translatePath(os.path.join(l11ll111_opy_, l1l11_opy_ (u"ࠧࡳࡧࡶࡳࡺࡸࡣࡦࡵࠪࠃ"), l1l11_opy_ (u"ࠨ࡮࡬ࡦࠬࠄ"), l1l11_opy_ (u"ࠩࡦࡰࡪࡧࡲࡠࡥࡤࡧ࡭࡫࠮ࡱࡻࠪࠅ")))
l1l1lll1_opy_ = 117
l1lll1l1_opy_ = 92
l1lll1_opy_ = 10
l111111_opy_ = 9
if not xbmcvfs.exists(l1ll_opy_):
    xbmcvfs.mkdir(l1ll_opy_)
xbmc.executebuiltin(l1l11_opy_ (u"ࠥ࡜ࡇࡓࡃ࠯ࡔࡸࡲࡘࡩࡲࡪࡲࡷࠬࠧࠆ")+l1ll111_opy_+l1l11_opy_ (u"ࠦ࠮ࠨࠇ"))
username = addon.getSetting(l1l11_opy_ (u"ࠬࡻࡳࡦࡴࡱࡥࡲ࡫ࠧࠈ"))
password = addon.getSetting(l1l11_opy_ (u"࠭ࡰࡢࡵࡶࡻࡴࡸࡤࠨࠉ"))
SKIN = addon.getSetting(l1l11_opy_ (u"ࠧࡴ࡭࡬ࡲࠬࠊ"))
l1ll11l_opy_ = addon.getSetting(l1l11_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡤࡣࡷࡧ࡭ࡻࡰࠨࠋ"))
if SKIN == l1l11_opy_ (u"ࠩࡸࡲࡸ࡫ࡴࠨࠌ"):
    l1l_opy_ = l11llll_opy_.yesno(l1l11_opy_ (u"ࠪ࡟ࡈࡕࡌࡐࡔࠣࡻ࡭࡯ࡴࡦ࡟ࡕࡩࡱࡵࡡࡥࡧࡧࠤࡠ࠵ࡃࡐࡎࡒࡖࡢࡡࡃࡐࡎࡒࡖࠥࡸࡥࡥ࡟ࡗ࡚ࡠ࠵ࡃࡐࡎࡒࡖࡢ࠭ࠍ"), l1l11_opy_ (u"ࠦࡕࡲࡥࡢࡵࡨࠤࡸ࡫࡬ࡦࡥࡷࠤࡦࠦࡳ࡬࡫ࡱࠤࡹ࡮ࡥ࡮ࡧࠣࡽࡴࡻࠠࡸࡱࡸࡰࡩࠦ࡬ࡪ࡭ࡨࠤࡹࡵࠠࡶࡵࡨ࠲ࠧࠎ"), l1l11_opy_ (u"ࠧࠨࠏ"), l1l11_opy_ (u"ࠨࠢࠐ"), l1l11_opy_ (u"ࠢࡅࡣࡵ࡯࡚ࠥࡨࡦ࡯ࡨࠦࠑ"), l1l11_opy_ (u"ࠣࡎ࡬࡫࡭ࡺࠠࡕࡪࡨࡱࡪࠨࠒ"))
    if l1l_opy_:
        addon.setSetting(l1l11_opy_ (u"ࠩࡶ࡯࡮ࡴࠧࠓ"), l1l11_opy_ (u"ࠪࡐ࡮࡭ࡨࡵࠩࠔ"))
        SKIN = l1l11_opy_ (u"ࠫࡑ࡯ࡧࡩࡶࠪࠕ")
    if not l1l_opy_:
        addon.setSetting(l1l11_opy_ (u"ࠬࡹ࡫ࡪࡰࠪࠖ"), l1l11_opy_ (u"࠭ࡄࡢࡴ࡮ࠫࠗ"))
        SKIN = l1l11_opy_ (u"ࠧࡅࡣࡵ࡯ࠬ࠘")
helper = helper(username,password,SKIN)
if l1ll11l_opy_ == l1l11_opy_ (u"ࠨࡷࡱࡷࡪࡺࠧ࠙"):
    l1l_opy_ = l11llll_opy_.yesno(helper.title + l1l11_opy_ (u"ࠤࠣ࠱ࠥࡋ࡮ࡢࡤ࡯ࡩ࡚ࠥࡖࠡࡅࡤࡸࡨ࡮ࡵࡱࡁࠥࠚ"), l1l11_opy_ (u"࡛ࠥࡴࡻ࡬ࡥࠢࡼࡳࡺࠦ࡬ࡪ࡭ࡨࠤࡹࡵࠠࡦࡰࡤࡦࡱ࡫ࠠࡕࡘࠣࡇࡦࡺࡣࡩࡷࡳࡃࠥࡖ࡬ࡦࡣࡶࡩࠥࡸࡥࡢࡦࠣࡸ࡭࡫ࠠࡵࡧࡵࡱࡸࠦࡢࡦ࡮ࡲࡻࠥࡨࡥࡧࡱࡵࡩࠥࡶࡲࡰࡥࡨࡩࡩ࡯࡮ࡨ࠰ࠥࠛ"), l1l11_opy_ (u"ࠦࡇࡿࠠࡺࡱࡸ࠰ࠥࡺࡨࡦࠢࡸࡷࡪࡸࠠࡦࡰࡤࡦࡱ࡯࡮ࡨࠢࡗ࡚ࠥࡉࡡࡵࡥ࡫ࡹࡵ࠲ࠠࡺࡱࡸࠤࡦࡸࡥࠡࡣࡪࡶࡪ࡫ࡩ࡯ࡩࠣࡸࡴࠦࡴࡩࡧࠣࡪࡴࡲ࡬ࡰࡹ࡬ࡲ࡬ࠦࡴࡦࡴࡰࡷ࠳࡙ࠦࡰࡷ࠯ࠤࡹ࡮ࡥࠡࡧࡱࡨࠥࡻࡳࡦࡴࠣࡥࡷ࡫ࠠࡳࡧࡶࡴࡴࡴࡳࡪࡤ࡯ࡩࠥࡧ࡮ࡥࠢ࡯࡭ࡦࡨ࡬ࡦࠢࡩࡳࡷࠦࡵࡴ࡫ࡱ࡫ࠥࡺࡨࡦࠢࡗ࡚ࠥࡉࡡࡵࡥ࡫ࡹࡵࠦࡦࡦࡣࡷࡹࡷ࡫࠮ࠡࡖ࡫ࡩ࡚ࠥࡖࠡࡅࡤࡸࡨ࡮ࡵࡱࠢࡩࡩࡦࡺࡵࡳࡧࠣࡻ࡮ࡲ࡬ࠡࡤࡨࠤࡸࡧࡶࡪࡰࡪࠤࡷ࡫ࡣࡰࡴࡧ࡭ࡳ࡭ࡳࠡࡶࡲࠤࡾࡵࡵࡳࠢࡳࡩࡷࡹ࡯࡯ࡣ࡯ࠤࡩ࡫ࡶࡪࡥࡨࠤࡸࡺ࡯ࡳࡣࡪࡩࠥࡧ࡮ࡥࠢࡺ࡭ࡱࡲࠠࡣࡧࠣ࡬ࡪࡲࡤࠡࡱࡱࠤࡾࡵࡵࡳࠢࡧࡩࡻ࡯ࡣࡦࠢࡩࡳࡷࠦࡵࡱࠢࡷࡳࠥ࠸࠴ࠡࡪࡲࡹࡷࡹࠠࡧࡱࡵࠤࡾࡵࡵࡳࠢࡲࡻࡳࠦࡰࡦࡴࡶࡳࡳࡧ࡬ࠡࡸ࡬ࡩࡼ࡯࡮ࡨ࠰ࠣ࡝ࡴࡻࠠࡢࡴࡨࠤࡦࡩ࡫࡯ࡱࡺࡰࡪࡪࡧࡪࡰࡪࠤࡾࡵࡵࠡࡪࡤࡺࡪࠦࡦࡶ࡮࡯ࠤࡦࡴࡤࠡࡧࡻࡴࡱ࡯ࡣࡪࡶࠣࡴࡪࡸ࡭ࡪࡵࡶ࡭ࡴࡴࡳࠡࡨࡵࡳࡲࠦࡴࡩࡧࠣࡶ࡮࡭ࡨࡵࡨࡸࡰࠥࡩ࡯ࡱࡻࡵ࡭࡬࡮ࡴࠡࡱࡺࡲࡪࡸࡳࠡࡶࡲࠤࡻ࡯ࡥࡸࠢࡤࡲࡩࠦࡳࡵࡱࡵࡩࠥࡺࡨࡦ࡫ࡵࠤࡨࡵ࡮ࡵࡧࡱࡸࠥࡵ࡮ࠡࡻࡲࡹࡷࠦࡤࡦࡸ࡬ࡧࡪࠦࡦࡰࡴࠣࡹࡵࠦࡴࡰࠢ࠵࠸ࠥ࡮࡯ࡶࡴࡶ࠲ࠥ࡟࡯ࡶࠢࡤࡧࡰࡴ࡯ࡸ࡮ࡨࡨ࡬࡫ࠠࡵࡪࡤࡸࠥࡽࡥࠡࡶࡤ࡯ࡪࠦ࡮ࡰࠢࡵࡩࡦࡹ࡯࡯ࡣࡥ࡭ࡱ࡯ࡴࡺࠢࡩࡳࡷࠦࡹࡰࡷ࠯ࠤࡹ࡮ࡥࠡࡷࡶࡩࡷࠦࡨࡰ࡮ࡧ࡭ࡳ࡭ࠠࡢࡰࡧ࠳ࡴࡸࠠࡸࡣࡷࡧ࡭࡯࡮ࡨࠢࡷ࡬ࡪࡹࡥࠡࡴࡨࡧࡴࡸࡤࡪࡰࡪࡷ࠳ࠨࠜ"), l1l11_opy_ (u"ࠧࠨࠝ"), l1l11_opy_ (u"ࠨࡎࡰࠤࠞ"), l1l11_opy_ (u"࡚ࠢࡧࡶ࠰ࠥࡏࠠࡂࡩࡵࡩࡪࠨࠟ"))
    if l1l_opy_:
        addon.setSetting(l1l11_opy_ (u"ࠨࡧࡱࡥࡧࡲࡥࡤࡣࡷࡧ࡭ࡻࡰࠨࠠ"), l1l11_opy_ (u"ࠩࡷࡶࡺ࡫ࠧࠡ"))
        l1ll11l_opy_ = l1l11_opy_ (u"ࠪࡸࡷࡻࡥࠨࠢ")
    if not l1l_opy_:
        addon.setSetting(l1l11_opy_ (u"ࠫࡪࡴࡡࡣ࡮ࡨࡧࡦࡺࡣࡩࡷࡳࠫࠣ"), l1l11_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫࠤ"))
        l1ll11l_opy_ = l1l11_opy_ (u"࠭ࡦࡢ࡮ࡶࡩࠬࠥ")
class l111ll_opy_(xbmcgui.WindowXML):
    def __init__(self, *args, **kwargs):
        self.l11l11l_opy_ = None
        self.l1ll111l_opy_ = []
        self.l1ll1_opy_ = None
        self.l1l1ll1l_opy_ = []
        self.l11l1lll_opy_ = -1
        self.l1ll11l1_opy_ = -1
        self.l1l1llll_opy_ = l1l11_opy_ (u"ࠧࠨࠦ")
        self.l11lll_opy_ = False
        self.l1ll1l11_opy_ = None
        self.l11ll1l_opy_ = [helper.l1l111l_opy_]
        self.l1l11111_opy_ = None
        self.l1l1ll1_opy_ = False
        self.l1l1l11l_opy_ = None
        self.l1ll1ll_opy_ = False
        self.l1ll1l1l_opy_ = 210
        self.categories = helper.l11lll1l_opy_()
        self.skin = SKIN
        self.l111ll1_opy_ = l1ll11l_opy_
        if self.skin == l1l11_opy_ (u"ࠨࡆࡤࡶࡰ࠭ࠧ"):
            self.l111l1_opy_ = l1l11_opy_ (u"ࠩࡧࡥࡷࡱࡧࡳࡧࡼࠫࠨ")
        else:
            self.l111l1_opy_ = l1l11_opy_ (u"ࠪࡦࡱࡧࡣ࡬ࠩࠩ")
        xbmcgui.WindowXML.__init__(self, *args, **kwargs)
        self.l1111l1_opy_ = (9, 10, 92, 216, 247, 257, 275, 61467, 61448)
    def onInit(self):
        self.window = xbmcgui.Window(xbmcgui.getCurrentWindowId())
        self.l11l11l_opy_ = self.window.getControl(210)
        self.l1ll1_opy_ = self.window.getControl(230)
        self.l11lll11_opy_ = addon.getSetting(l1l11_opy_ (u"ࠫࡸ࡮࡯ࡸࡥ࡫ࡥࡳࡴࡥ࡭ࡰࡤࡱࡪ࠭ࠪ")) == l1l11_opy_ (u"ࠬࡺࡲࡶࡧࠪࠫ")
        self.l1l11ll_opy_ = addon.getSetting(l1l11_opy_ (u"࠭ࡰࡢࡴࡨࡲࡹࡧ࡬ࡰࡥ࡮ࠫࠬ")) == l1l11_opy_ (u"ࠧࡵࡴࡸࡩࠬ࠭")
        self.l1lll_opy_ = addon.getSetting(l1l11_opy_ (u"ࠨࡲࡤࡶࡪࡴࡴࡢ࡮ࡦࡳࡩ࡫ࠧ࠮"))
        self.l1l11lll_opy_()
        self.l1l111_opy_()
        self.l1l11ll1_opy_()
        if self.l1ll1ll_opy_:
            self.l11l11l_opy_.reset()
            self.l11l11l_opy_.addItems(self.l1ll111l_opy_)
            self.l11l11l_opy_.getListItem(self.l11l1lll_opy_).setProperty(l1l11_opy_ (u"ࠩࡦࡰ࡮ࡩ࡫ࡦࡦࠪ࠯"), l1l11_opy_ (u"ࠪࡸࡷࡻࡥࠨ࠰"))
            self.l11l11l_opy_.selectItem(self.l11l1lll_opy_)
            if l1l11_opy_ (u"ࠫ࡬࡫ࡴࡠࡸࡲࡨࡤࡩࡡࡵࡧࡪࡳࡷ࡯ࡥࡴࠩ࠱") in self.l1l1llll_opy_:
                self.l1ll1111_opy_()
            elif l1l11_opy_ (u"ࠬ࡭ࡥࡵࡡࡹࡳࡩࡥࡳࡵࡴࡨࡥࡲࡹࠧ࠲") in self.l1l1llll_opy_:
                self.l1l1ll_opy_(self.l1l1llll_opy_)
            else:
                self.l11lllll_opy_()
            self.l1ll1_opy_.reset()
            self.l1ll1_opy_.addItems(self.l1l1ll1l_opy_)
            self.l1ll1_opy_.selectItem(self.l1ll11l1_opy_)
        xbmc.executebuiltin(l1l11_opy_ (u"ࠨࡄࡪࡣ࡯ࡳ࡬࠴ࡃ࡭ࡱࡶࡩ࠭ࡨࡵࡴࡻࡧ࡭ࡦࡲ࡯ࡨࠫࠥ࠳"))
        try:
            self.setFocus(self.window.getControl(self.l1ll1l1l_opy_))
        except:
            pass
    def l1l111_opy_(self):
        try:
            l1lll11_opy_ = helper.l1lll1l_opy_()
            control = self.window.getControl(99)
            if control and not l1lll11_opy_ == l1l11_opy_ (u"ࠧࠨ࠴"):
                control.setLabel(l1lll11_opy_)
        except:
            pass
    def l1l11lll_opy_(self):
        try:
            l1ll11ll_opy_ = helper.l1l1_opy_()
            control = self.window.getControl(9968)
            if control and not l1ll11ll_opy_ == l1l11_opy_ (u"ࠨࠩ࠵"):
                control.setLabel(l1ll11ll_opy_)
            else:
                control = self.window.getControl(9969)
                control.setVisible(False)
        except:
            pass
    def l1l11ll1_opy_(self):
        l1l11_opy_ (u"ࠤࠥࠦࡑ࡯ࡳࡵࠢࡦࡥࡹ࡫ࡧࡰࡴ࡬ࡩࡸࠨࠢࠣ࠶")
        xbmc.executebuiltin(l1l11_opy_ (u"ࠥࡅࡨࡺࡩࡷࡣࡷࡩ࡜࡯࡮ࡥࡱࡺࠬࡧࡻࡳࡺࡦ࡬ࡥࡱࡵࡧࠪࠤ࠷"))
        self.l1ll111l_opy_ = []
        if helper.l1l11111_opy_:
            listitem = xbmcgui.ListItem(l1l11_opy_ (u"ࠫࡠࡉࡏࡍࡑࡕࠤࡱ࡯࡭ࡦ࡟࡞ࡆࡢࡌࡁࡗࡕ࡞࠳ࡇࡣ࡛࠰ࡅࡒࡐࡔࡘ࡝ࠨ࠸"))
            listitem.setProperty(l1l11_opy_ (u"ࠬࡻࡲ࡭ࠩ࠹"), l1l11_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲࡥࡦࡢࡸࡲࡶ࡮ࡺࡥࡴࠩ࠺"))
            listitem.setProperty(l1l11_opy_ (u"ࠧࡪࡥࡲࡲࠬ࠻"), l1l11_opy_ (u"ࠨࠩ࠼"))
            self.l1ll111l_opy_.append(listitem)
            self.l1l1ll1_opy_ = True
        for category in helper.l11lll1l_opy_():
            listitem = xbmcgui.ListItem(category.name)
            listitem.setProperty(l1l11_opy_ (u"ࠩࡸࡶࡱ࠭࠽"), category.url)
            listitem.setProperty(l1l11_opy_ (u"ࠪ࡭ࡨࡵ࡮ࠨ࠾"), category.l11ll1ll_opy_)
            self.l1ll111l_opy_.append(listitem)
        self.l11l11l_opy_.addItems(self.l1ll111l_opy_)
        xbmc.executebuiltin(l1l11_opy_ (u"ࠦࡉ࡯ࡡ࡭ࡱࡪ࠲ࡈࡲ࡯ࡴࡧࠫࡦࡺࡹࡹࡥ࡫ࡤࡰࡴ࡭ࠩࠣ࠿"))
    def l1ll1111_opy_(self, l1llll1_opy_=False):
        l1l11_opy_ (u"ࠧࠨࠢ࡭࡫ࡶࡸࠥࡼ࡯ࡥࠢࡦࡥࡹ࡫ࡧࡰࡴ࡬ࡩࡸࠨࠢࠣࡀ")
        xbmc.executebuiltin(l1l11_opy_ (u"ࠨࡁࡤࡶ࡬ࡺࡦࡺࡥࡘ࡫ࡱࡨࡴࡽࠨࡣࡷࡶࡽࡩ࡯ࡡ࡭ࡱࡪ࠭ࠧࡁ"))
        self.l1l1ll1l_opy_ = []
        l11llll_opy_.ok(helper.title,l1l11_opy_ (u"ࠧ࡜ࡅࡒࡐࡔࡘࠠࡳࡧࡧࡡࡠࡈ࡝ࡗࡑࡇࠤࡨࡵ࡭ࡪࡰࡪࠤࡸࡵ࡯࡯࠰࠱࠲ࡠ࠵ࡂ࡞࡝࠲ࡇࡔࡒࡏࡓ࡟ࠪࡂ"),l1l11_opy_ (u"ࠨࠩࡃ"),l1l11_opy_ (u"ࠩࠪࡄ"))
        return
        if l1llll1_opy_:
            self.l1ll1_opy_.reset()
            if not l1l11_opy_ (u"ࠪ࡫ࡪࡺ࡟ࡷࡱࡧࡣࡨࡧࡴࡦࡩࡲࡶ࡮࡫ࡳࠨࡅ") in l1llll1_opy_:
                listitem = xbmcgui.ListItem(l1l11_opy_ (u"ࠫ࠳࠴࠮ࠨࡆ"))
                listitem.setProperty(l1l11_opy_ (u"ࠬࡻࡲ࡭ࠩࡇ"), self.l11ll1l_opy_[-2])
                listitem.setProperty(l1l11_opy_ (u"࠭࡬ࡰࡩࡲࠫࡈ"), l1l11_opy_ (u"ࠧࠨࡉ"))
                listitem.setProperty(l1l11_opy_ (u"ࠨࡰࡲࡻࡤࡶࡲࡰࡩࡷ࡭ࡹࡲࡥࠨࡊ"), l1l11_opy_ (u"ࠩࠪࡋ"))
                listitem.setProperty(l1l11_opy_ (u"ࠪࡲࡴࡽ࡟ࡱࡴࡲ࡫ࡹ࡯ࡴ࡭ࡧࠪࡌ"), l1l11_opy_ (u"ࠫࠬࡍ"))
                listitem.setProperty(l1l11_opy_ (u"ࠬࡴࡥࡹࡶࡢࡴࡷࡵࡧࡵ࡫ࡷࡰࡪ࠭ࡎ"), l1l11_opy_ (u"࠭ࠧࡏ"))
                listitem.setProperty(l1l11_opy_ (u"ࠧ࡯ࡱࡺࡣࡨ࡮࡮ࡱࡴࡲ࡫ࡩ࡫ࡳࡤࠩࡐ"), l1l11_opy_ (u"ࠨࡨࡤࡰࡸ࡫ࠧࡑ"))
                listitem.setProperty(l1l11_opy_ (u"ࠩࡱࡩࡽࡺ࡟ࡤࡪࡱࡴࡷࡵࡧࡥࡧࡶࡧࠬࡒ"), l1l11_opy_ (u"ࠪࡪࡦࡲࡳࡦࠩࡓ"))
                listitem.setProperty(l1l11_opy_ (u"ࠫ࡮ࡹࡐ࡭ࡣࡼࡥࡧࡲࡥࠨࡔ"), l1l11_opy_ (u"ࠬࡺࡲࡶࡧࠪࡕ"))
                listitem.setProperty(l1l11_opy_ (u"࠭ࡨࡢࡵࡑࡳࡼ࠭ࡖ"),l1l11_opy_ (u"ࠧࡧࡣ࡯ࡷࡪ࠭ࡗ"))
                listitem.setProperty(l1l11_opy_ (u"ࠨࡪࡤࡷࡓ࡫ࡸࡵࠩࡘ"),l1l11_opy_ (u"ࠩࡩࡥࡱࡹࡥࠨ࡙"))
                listitem.setProperty(l1l11_opy_ (u"ࠪ࡭ࡸࡍࡡ࡮ࡧ࡚ࠪ"),l1l11_opy_ (u"ࠫ࡫ࡧ࡬ࡴࡧ࡛ࠪ"))
                listitem.setProperty(l1l11_opy_ (u"ࠬ࡯ࡳࡃࡣࡦ࡯ࠬ࡜"), l1l11_opy_ (u"࠭ࡴࡳࡷࡨࠫ࡝"))
                listitem.setProperty(l1l11_opy_ (u"ࠧࡔࡪࡲࡻࡈ࡮࡮ࡏࡣࡰࡩࠬ࡞"),l1l11_opy_ (u"ࠨࡶࡵࡹࡪ࠭࡟"))
                self.l1l1ll1l_opy_.append(listitem)
            for category in helper.l1l1111l_opy_(l1llll1_opy_):
                listitem = xbmcgui.ListItem(category.name)
                listitem.setProperty(l1l11_opy_ (u"ࠩࡸࡶࡱ࠭ࡠ"), category.url)
                listitem.setProperty(l1l11_opy_ (u"ࠪࡰࡴ࡭࡯ࠨࡡ"), category.l11ll1ll_opy_)
                listitem.setProperty(l1l11_opy_ (u"ࠫࡳࡵࡷࡠࡲࡵࡳ࡬ࡺࡩࡵ࡮ࡨࠫࡢ"), l1l11_opy_ (u"ࠬ࠭ࡣ"))
                listitem.setProperty(l1l11_opy_ (u"࠭࡮ࡰࡹࡢࡴࡷࡵࡧࡵ࡫ࡷࡰࡪ࠭ࡤ"), l1l11_opy_ (u"ࠧࠨࡥ"))
                listitem.setProperty(l1l11_opy_ (u"ࠨࡰࡨࡼࡹࡥࡰࡳࡱࡪࡸ࡮ࡺ࡬ࡦࠩࡦ"), l1l11_opy_ (u"ࠩࠪࡧ"))
                listitem.setProperty(l1l11_opy_ (u"ࠪࡲࡴࡽ࡟ࡤࡪࡱࡴࡷࡵࡧࡥࡧࡶࡧࠬࡨ"), l1l11_opy_ (u"ࠫ࡫ࡧ࡬ࡴࡧࠪࡩ"))
                listitem.setProperty(l1l11_opy_ (u"ࠬࡴࡥࡹࡶࡢࡧ࡭ࡴࡰࡳࡱࡪࡨࡪࡹࡣࠨࡪ"), l1l11_opy_ (u"࠭ࡦࡢ࡮ࡶࡩࠬ࡫"))
                listitem.setProperty(l1l11_opy_ (u"ࠧࡪࡵࡓࡰࡦࡿࡡࡣ࡮ࡨࠫ࡬"), l1l11_opy_ (u"ࠨࡶࡵࡹࡪ࠭࡭"))
                listitem.setProperty(l1l11_opy_ (u"ࠩ࡫ࡥࡸࡔ࡯ࡸࠩ࡮"),l1l11_opy_ (u"ࠪࡪࡦࡲࡳࡦࠩ࡯"))
                listitem.setProperty(l1l11_opy_ (u"ࠫ࡭ࡧࡳࡏࡧࡻࡸࠬࡰ"),l1l11_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫࡱ"))
                listitem.setProperty(l1l11_opy_ (u"࠭ࡩࡴࡉࡤࡱࡪ࠭ࡲ"),l1l11_opy_ (u"ࠧࡧࡣ࡯ࡷࡪ࠭ࡳ"))
                listitem.setProperty(l1l11_opy_ (u"ࠨࡕ࡫ࡳࡼࡉࡨ࡯ࡐࡤࡱࡪ࠭ࡴ"),l1l11_opy_ (u"ࠩࡷࡶࡺ࡫ࠧࡵ"))
                self.l1l1ll1l_opy_.append(listitem)
        else:
            for category in helper.l1l1111l_opy_():
                listitem = xbmcgui.ListItem(category.name)
                listitem.setProperty(l1l11_opy_ (u"ࠪࡹࡷࡲࠧࡶ"), category.url)
                listitem.setProperty(l1l11_opy_ (u"ࠫࡱࡵࡧࡰࠩࡷ"), category.l11ll1ll_opy_)
                listitem.setProperty(l1l11_opy_ (u"ࠬࡴ࡯ࡸࡡࡳࡶࡴ࡭ࡴࡪࡶ࡯ࡩࠬࡸ"), l1l11_opy_ (u"࠭ࠧࡹ"))
                listitem.setProperty(l1l11_opy_ (u"ࠧ࡯ࡱࡺࡣࡵࡸ࡯ࡨࡶ࡬ࡸࡱ࡫ࠧࡺ"), l1l11_opy_ (u"ࠨࠩࡻ"))
                listitem.setProperty(l1l11_opy_ (u"ࠩࡱࡩࡽࡺ࡟ࡱࡴࡲ࡫ࡹ࡯ࡴ࡭ࡧࠪࡼ"), l1l11_opy_ (u"ࠪࠫࡽ"))
                listitem.setProperty(l1l11_opy_ (u"ࠫࡳࡵࡷࡠࡥ࡫ࡲࡵࡸ࡯ࡨࡦࡨࡷࡨ࠭ࡾ"), l1l11_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫࡿ"))
                listitem.setProperty(l1l11_opy_ (u"࠭࡮ࡦࡺࡷࡣࡨ࡮࡮ࡱࡴࡲ࡫ࡩ࡫ࡳࡤࠩࢀ"), l1l11_opy_ (u"ࠧࡧࡣ࡯ࡷࡪ࠭ࢁ"))
                listitem.setProperty(l1l11_opy_ (u"ࠨ࡫ࡶࡔࡱࡧࡹࡢࡤ࡯ࡩࠬࢂ"), l1l11_opy_ (u"ࠩࡷࡶࡺ࡫ࠧࢃ"))
                listitem.setProperty(l1l11_opy_ (u"ࠪ࡬ࡦࡹࡎࡰࡹࠪࢄ"),l1l11_opy_ (u"ࠫ࡫ࡧ࡬ࡴࡧࠪࢅ"))
                listitem.setProperty(l1l11_opy_ (u"ࠬ࡮ࡡࡴࡐࡨࡼࡹ࠭ࢆ"),l1l11_opy_ (u"࠭ࡦࡢ࡮ࡶࡩࠬࢇ"))
                listitem.setProperty(l1l11_opy_ (u"ࠧࡪࡵࡊࡥࡲ࡫ࠧ࢈"),l1l11_opy_ (u"ࠨࡨࡤࡰࡸ࡫ࠧࢉ"))
                listitem.setProperty(l1l11_opy_ (u"ࠩࡖ࡬ࡴࡽࡃࡩࡰࡑࡥࡲ࡫ࠧࢊ"),l1l11_opy_ (u"ࠪࡸࡷࡻࡥࠨࢋ"))
                self.l1l1ll1l_opy_.append(listitem)
        self.l1ll1_opy_.addItems(self.l1l1ll1l_opy_)
        xbmc.executebuiltin(l1l11_opy_ (u"ࠦࡉ࡯ࡡ࡭ࡱࡪ࠲ࡈࡲ࡯ࡴࡧࠫࡦࡺࡹࡹࡥ࡫ࡤࡰࡴ࡭ࠩࠣࢌ"))
    def l1l1ll_opy_(self, url):
        xbmc.executebuiltin(l1l11_opy_ (u"ࠧࡇࡣࡵ࡫ࡹࡥࡹ࡫ࡗࡪࡰࡧࡳࡼ࠮ࡢࡶࡵࡼࡨ࡮ࡧ࡬ࡰࡩࠬࠦࢍ"))
        self.l1l1ll1l_opy_ = []
        if not l1l11_opy_ (u"࠭ࡧࡦࡶࡢࡺࡴࡪ࡟ࡤࡣࡷࡩ࡬ࡵࡲࡪࡧࡶࠫࢎ") in url:
            listitem = xbmcgui.ListItem(l1l11_opy_ (u"ࠧ࠯࠰࠱ࠫ࢏"))
            listitem.setProperty(l1l11_opy_ (u"ࠨࡷࡵࡰࠬ࢐"), self.l11ll1l_opy_[-2])
            listitem.setProperty(l1l11_opy_ (u"ࠩ࡯ࡳ࡬ࡵࠧ࢑"), l1l11_opy_ (u"ࠪࠫ࢒"))
            listitem.setProperty(l1l11_opy_ (u"ࠫࡳࡵࡷࡠࡲࡵࡳ࡬ࡺࡩࡵ࡮ࡨࠫ࢓"), l1l11_opy_ (u"ࠬ࠭࢔"))
            listitem.setProperty(l1l11_opy_ (u"࠭࡮ࡰࡹࡢࡴࡷࡵࡧࡵ࡫ࡷࡰࡪ࠭࢕"), l1l11_opy_ (u"ࠧࠨ࢖"))
            listitem.setProperty(l1l11_opy_ (u"ࠨࡰࡨࡼࡹࡥࡰࡳࡱࡪࡸ࡮ࡺ࡬ࡦࠩࢗ"), l1l11_opy_ (u"ࠩࠪ࢘"))
            listitem.setProperty(l1l11_opy_ (u"ࠪࡲࡴࡽ࡟ࡤࡪࡱࡴࡷࡵࡧࡥࡧࡶࡧ࢙ࠬ"), l1l11_opy_ (u"ࠫ࡫ࡧ࡬ࡴࡧ࢚ࠪ"))
            listitem.setProperty(l1l11_opy_ (u"ࠬࡴࡥࡹࡶࡢࡧ࡭ࡴࡰࡳࡱࡪࡨࡪࡹࡣࠨ࢛"), l1l11_opy_ (u"࠭ࡦࡢ࡮ࡶࡩࠬ࢜"))
            listitem.setProperty(l1l11_opy_ (u"ࠧࡪࡵࡓࡰࡦࡿࡡࡣ࡮ࡨࠫ࢝"), l1l11_opy_ (u"ࠨࡶࡵࡹࡪ࠭࢞"))
            listitem.setProperty(l1l11_opy_ (u"ࠩ࡫ࡥࡸࡔ࡯ࡸࠩ࢟"),l1l11_opy_ (u"ࠪࡪࡦࡲࡳࡦࠩࢠ"))
            listitem.setProperty(l1l11_opy_ (u"ࠫ࡭ࡧࡳࡏࡧࡻࡸࠬࢡ"),l1l11_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫࢢ"))
            listitem.setProperty(l1l11_opy_ (u"࠭ࡩࡴࡉࡤࡱࡪ࠭ࢣ"),l1l11_opy_ (u"ࠧࡧࡣ࡯ࡷࡪ࠭ࢤ"))
            listitem.setProperty(l1l11_opy_ (u"ࠨ࡫ࡶࡆࡦࡩ࡫ࠨࢥ"), l1l11_opy_ (u"ࠩࡷࡶࡺ࡫ࠧࢦ"))
            listitem.setProperty(l1l11_opy_ (u"ࠪࡗ࡭ࡵࡷࡄࡪࡱࡒࡦࡳࡥࠨࢧ"),l1l11_opy_ (u"ࠫࡹࡸࡵࡦࠩࢨ"))
            self.l1l1ll1l_opy_.append(listitem)
        for channel in helper.l1llll1l_opy_(url):
            listitem = xbmcgui.ListItem(channel.title.replace(l1l11_opy_ (u"ࠬࠦࠨ࠲࠲࠻࠴࠮࠭ࢩ"),l1l11_opy_ (u"࠭ࠧࢪ")).replace(l1l11_opy_ (u"ࠧࠡࠪ࠺࠶࠵࠯ࠧࢫ"),l1l11_opy_ (u"ࠨࠩࢬ")).replace(l1l11_opy_ (u"ࠩ࡞ࡇࡔࡒࡏࡓࠢࡥࡰࡦࡩ࡫࡞ࠩࢭ"), l1l11_opy_ (u"ࠪ࡟ࡈࡕࡌࡐࡔࠣࠫࢮ")+self.l111l1_opy_+l1l11_opy_ (u"ࠫࡢ࠭ࢯ")))
            listitem.setProperty(l1l11_opy_ (u"ࠬࡻࡲ࡭ࠩࢰ"), channel.l1l1l1l_opy_)
            listitem.setProperty(l1l11_opy_ (u"࠭࡬ࡰࡩࡲࠫࢱ"), channel.logo)
            listitem.setProperty(l1l11_opy_ (u"ࠧ࡯ࡱࡺࡣࡵࡸ࡯ࡨࡶ࡬ࡸࡱ࡫ࠧࢲ"), l1l11_opy_ (u"ࠣࠧࡶࠦࢳ") % (channel.l11ll1_opy_))
            listitem.setProperty(l1l11_opy_ (u"ࠩࡱࡩࡽࡺ࡟ࡱࡴࡲ࡫ࡹ࡯ࡴ࡭ࡧࠪࢴ"), l1l11_opy_ (u"ࠥࠩࡸࠨࢵ") % (channel.l11llll1_opy_))
            listitem.setProperty(l1l11_opy_ (u"ࠫࡳࡵࡷࡠࡥ࡫ࡲࡵࡸ࡯ࡨࡦࡨࡷࡨ࠭ࢶ"), l1l11_opy_ (u"ࠧࡡࡃࡐࡎࡒࡖࠥࠫࡳ࡞࡝ࡅࡡࠪࡹ࡛࠰ࡄࡠ࡟࠴ࡉࡏࡍࡑࡕࡡࠧࢷ") % (self.l111l1_opy_,channel.l1lll11l_opy_))
            listitem.setProperty(l1l11_opy_ (u"࠭࡮ࡦࡺࡷࡣࡨ࡮࡮ࡱࡴࡲ࡫ࡩ࡫ࡳࡤࠩࢸ"), channel.l1ll11_opy_)
            listitem.setProperty(l1l11_opy_ (u"ࠧࡪࡵࡓࡰࡦࡿࡡࡣ࡮ࡨࠫࢹ"), l1l11_opy_ (u"ࠨࡶࡵࡹࡪ࠭ࢺ"))
            listitem.setProperty(l1l11_opy_ (u"ࠩ࡬ࡷࡌࡧ࡭ࡦࠩࢻ"),l1l11_opy_ (u"ࠪࡪࡦࡲࡳࡦࠩࢼ"))
            listitem.setProperty(l1l11_opy_ (u"ࠫ࡮ࡹࡖࡐࡆࠪࢽ"), l1l11_opy_ (u"ࠬࡺࡲࡶࡧࠪࢾ"))
            if channel.l11ll1_opy_ != l1l11_opy_ (u"ࠨࠢࢿ"):
                listitem.setProperty(l1l11_opy_ (u"ࠧࡩࡣࡶࡒࡴࡽࠧࣀ"),l1l11_opy_ (u"ࠨࡶࡵࡹࡪ࠭ࣁ"))
            else:
                listitem.setProperty(l1l11_opy_ (u"ࠩ࡫ࡥࡸࡔ࡯ࡸࠩࣂ"),l1l11_opy_ (u"ࠪࡪࡦࡲࡳࡦࠩࣃ"))
            if channel.l11llll1_opy_ != l1l11_opy_ (u"ࠦࠧࣄ"):
                listitem.setProperty(l1l11_opy_ (u"ࠬ࡮ࡡࡴࡐࡨࡼࡹ࠭ࣅ"),l1l11_opy_ (u"࠭ࡴࡳࡷࡨࠫࣆ"))
            else:
                listitem.setProperty(l1l11_opy_ (u"ࠧࡩࡣࡶࡒࡪࡾࡴࠨࣇ"),l1l11_opy_ (u"ࠨࡨࡤࡰࡸ࡫ࠧࣈ"))
            listitem.setProperty(l1l11_opy_ (u"ࠩࡖ࡬ࡴࡽࡃࡩࡰࡑࡥࡲ࡫ࠧࣉ"),l1l11_opy_ (u"ࠪࡸࡷࡻࡥࠨ࣊"))
            if l1l11_opy_ (u"ࠫࠥ࠮࠱࠱࠺࠳࠭ࠬ࣋") in channel.title:
                listitem.setProperty(l1l11_opy_ (u"ࠬ࡯ࡳ࠲࠲࠻࠴ࠬ࣌"),l1l11_opy_ (u"࠭ࡴࡳࡷࡨࠫ࣍"))
            else:
                listitem.setProperty(l1l11_opy_ (u"ࠧࡪࡵ࠴࠴࠽࠶ࠧ࣎"),l1l11_opy_ (u"ࠨࡨࡤࡰࡸ࡫࣏ࠧ"))
            if l1l11_opy_ (u"ࠩࠣࠬ࠼࠸࠰࣐ࠪࠩ") in channel.title:
                listitem.setProperty(l1l11_opy_ (u"ࠪ࡭ࡸ࠽࠲࠱࣑ࠩ"),l1l11_opy_ (u"ࠫࡹࡸࡵࡦ࣒ࠩ"))
            else:
                listitem.setProperty(l1l11_opy_ (u"ࠬ࡯ࡳ࠸࠴࠳࣓ࠫ"),l1l11_opy_ (u"࠭ࡦࡢ࡮ࡶࡩࠬࣔ"))
            self.l1l1ll1l_opy_.append(listitem)
        self.l1ll1_opy_.addItems(self.l1l1ll1l_opy_)
        if len(self.l1l1ll1l_opy_) == 1:
            l11llll_opy_.ok(helper.title,l1l11_opy_ (u"ࠧ࡜ࡅࡒࡐࡔࡘࠠࡳࡧࡧࡡࡠࡈ࡝ࡏࡱ࡚ࠣࡔࡊࠠࡧࡱࡸࡲࡩࠦࡦࡰࡴࠣࡸ࡭࡯ࡳࠡࡵࡨࡧࡹ࡯࡯࡯࠰࡞࠳ࡇࡣ࡛࠰ࡅࡒࡐࡔࡘ࡝ࠨࣕ"),l1l11_opy_ (u"ࠨࠩࣖ"),l1l11_opy_ (u"ࠩࡓࡰࡪࡧࡳࡦࠢࡦ࡬ࡪࡩ࡫ࠡࡤࡤࡧࡰࠦ࡬ࡢࡶࡨࡶࠦ࠭ࣗ"))
        xbmc.executebuiltin(l1l11_opy_ (u"ࠥࡈ࡮ࡧ࡬ࡰࡩ࠱ࡇࡱࡵࡳࡦࠪࡥࡹࡸࡿࡤࡪࡣ࡯ࡳ࡬࠯ࠢࣘ"))
    def l11lllll_opy_(self):
        l1l11_opy_ (u"ࠦࠧࠨ࡬ࡪࡵࡷࠤࡨ࡮ࡡ࡯ࡰࡨࡰࡸࠦࡦࡰࡴࠣࡥࠥ࡭ࡩࡷࡧࡱࠤࡨࡧࡴࡦࡩࡲࡶࡾࠨࠢࠣࣙ")
        xbmc.executebuiltin(l1l11_opy_ (u"ࠧࡇࡣࡵ࡫ࡹࡥࡹ࡫ࡗࡪࡰࡧࡳࡼ࠮ࡢࡶࡵࡼࡨ࡮ࡧ࡬ࡰࡩࠬࠦࣚ"))
        self.l1l1ll1l_opy_ = []
        if self.l1l1llll_opy_ == l1l11_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲࡥࡦࡢࡸࡲࡶ࡮ࡺࡥࡴࠩࣛ"):
            for channel in helper.l11l1l1_opy_():
                listitem = xbmcgui.ListItem(channel.title.replace(l1l11_opy_ (u"ࠧࠡࠪ࠴࠴࠽࠶ࠩࠨࣜ"),l1l11_opy_ (u"ࠨࠩࣝ")).replace(l1l11_opy_ (u"ࠩࠣࠬ࠼࠸࠰ࠪࠩࣞ"),l1l11_opy_ (u"ࠪࠫࣟ")).replace(l1l11_opy_ (u"ࠫࡠࡉࡏࡍࡑࡕࠤࡧࡲࡡࡤ࡭ࡠࠫ࣠"), l1l11_opy_ (u"ࠬࡡࡃࡐࡎࡒࡖࠥ࠭࣡")+self.l111l1_opy_+l1l11_opy_ (u"࠭࡝ࠨ࣢")))
                listitem.setProperty(l1l11_opy_ (u"ࠧࡶࡴ࡯ࣣࠫ"), channel.l1l1l1l_opy_)
                listitem.setProperty(l1l11_opy_ (u"ࠨ࡮ࡲ࡫ࡴ࠭ࣤ"), channel.logo)
                listitem.setProperty(l1l11_opy_ (u"ࠩࡱࡳࡼࡥࡰࡳࡱࡪࡸ࡮ࡺ࡬ࡦࠩࣥ"), l1l11_opy_ (u"ࠥ࡟ࡈࡕࡌࡐࡔࠣࡶࡪࡪ࡝࡜ࡄࡠࡒࡔ࡝࠺࡜࠱ࡅࡡࡠ࠵ࡃࡐࡎࡒࡖࡢ࡛ࠦࡄࡑࡏࡓࡗࠦࠥࡴ࡟࡞ࡆࡢࠫࡳ࡜࠱ࡅࡡࡠ࠵ࡃࡐࡎࡒࡖࡢࠨࣦ") % (self.l111l1_opy_, channel.l11ll1_opy_))
                listitem.setProperty(l1l11_opy_ (u"ࠫࡳ࡫ࡸࡵࡡࡳࡶࡴ࡭ࡴࡪࡶ࡯ࡩࠬࣧ"), l1l11_opy_ (u"ࠧࡡࡃࡐࡎࡒࡖࠥ࡭ࡲࡦࡧࡱࡡࡠࡈ࡝ࡏࡇ࡛ࡘࠥ࡯࡮ࠡ࡝࠲ࡇࡔࡒࡏࡓ࡟࡞ࡇࡔࡒࡏࡓࠢࡰࡩࡩ࡯ࡵ࡮ࡵ࡯ࡥࡹ࡫ࡢ࡭ࡷࡨࡡࠪࡹ࠺࡜࠱ࡅࡡࡠ࠵ࡃࡐࡎࡒࡖࡢ࡛ࠦࡄࡑࡏࡓࡗࠦࠥࡴ࡟࡞ࡆࡢࠫࡳ࡜࠱ࡅࡡࡠ࠵ࡃࡐࡎࡒࡖࡢࠨࣨ") % (channel.l1llllll_opy_, self.l111l1_opy_, channel.l11llll1_opy_))
                listitem.setProperty(l1l11_opy_ (u"࠭࡮ࡰࡹࡢࡧ࡭ࡴࡰࡳࡱࡪࡨࡪࡹࡣࠨࣩ"), l1l11_opy_ (u"ࠢ࡜ࡅࡒࡐࡔࡘࠠࠦࡵࡠ࡟ࡇࡣࠥࡴ࡝࠲ࡆࡢࡡ࠯ࡄࡑࡏࡓࡗࡣࠢ࣪") % (self.l111l1_opy_,channel.l1lll11l_opy_))
                listitem.setProperty(l1l11_opy_ (u"ࠨࡰࡨࡼࡹࡥࡣࡩࡰࡳࡶࡴ࡭ࡤࡦࡵࡦࠫ࣫"), channel.l1ll11_opy_)
                listitem.setProperty(l1l11_opy_ (u"ࠩ࡬ࡷࡕࡲࡡࡺࡣࡥࡰࡪ࠭࣬"), l1l11_opy_ (u"ࠪࡸࡷࡻࡥࠨ࣭"))
                if l1l11_opy_ (u"ࠫ࠳ࡳࡰ࠵࣮ࠩ") in channel.l1l1l1l_opy_:
                    listitem.setProperty(l1l11_opy_ (u"ࠬ࡯ࡳࡗࡑࡇ࣯ࠫ"), l1l11_opy_ (u"࠭ࡴࡳࡷࡨࣰࠫ"))
                else:
                    listitem.setProperty(l1l11_opy_ (u"ࠧࡪࡵ࡙ࡓࡉ࠲ࣱࠧ"), l1l11_opy_ (u"ࠨࡨࡤࡰࡸ࡫ࣲࠧ"))
                if channel.l11ll1_opy_ != l1l11_opy_ (u"ࠤࠥࣳ"):
                    listitem.setProperty(l1l11_opy_ (u"ࠪ࡬ࡦࡹࡎࡰࡹࠪࣴ"),l1l11_opy_ (u"ࠫࡹࡸࡵࡦࠩࣵ"))
                else:
                    listitem.setProperty(l1l11_opy_ (u"ࠬ࡮ࡡࡴࡐࡲࡻࣶࠬ"),l1l11_opy_ (u"࠭ࡦࡢ࡮ࡶࡩࠬࣷ"))
                if channel.l11llll1_opy_ != l1l11_opy_ (u"ࠢࠣࣸ"):
                    listitem.setProperty(l1l11_opy_ (u"ࠨࡪࡤࡷࡓ࡫ࡸࡵࣹࠩ"),l1l11_opy_ (u"ࠩࡷࡶࡺ࡫ࣺࠧ"))
                else:
                    listitem.setProperty(l1l11_opy_ (u"ࠪ࡬ࡦࡹࡎࡦࡺࡷࠫࣻ"),l1l11_opy_ (u"ࠫ࡫ࡧ࡬ࡴࡧࠪࣼ"))
                if self.l11lll11_opy_:
                    listitem.setProperty(l1l11_opy_ (u"࡙ࠬࡨࡰࡹࡆ࡬ࡳࡔࡡ࡮ࡧࠪࣽ"),l1l11_opy_ (u"࠭ࡴࡳࡷࡨࠫࣾ"))
                else:
                    listitem.setProperty(l1l11_opy_ (u"ࠧࡔࡪࡲࡻࡈ࡮࡮ࡏࡣࡰࡩࠬࣿ"),l1l11_opy_ (u"ࠨࡨࡤࡰࡸ࡫ࠧऀ"))
                if l1l11_opy_ (u"ࠩࠣࠬ࠶࠶࠸࠱ࠫࠪँ") in channel.title:
                    listitem.setProperty(l1l11_opy_ (u"ࠪ࡭ࡸ࠷࠰࠹࠲ࠪं"),l1l11_opy_ (u"ࠫࡹࡸࡵࡦࠩः"))
                else:
                    listitem.setProperty(l1l11_opy_ (u"ࠬ࡯ࡳ࠲࠲࠻࠴ࠬऄ"),l1l11_opy_ (u"࠭ࡦࡢ࡮ࡶࡩࠬअ"))
                if l1l11_opy_ (u"ࠧࠡࠪ࠺࠶࠵࠯ࠧआ") in channel.title:
                    listitem.setProperty(l1l11_opy_ (u"ࠨ࡫ࡶ࠻࠷࠶ࠧइ"),l1l11_opy_ (u"ࠩࡷࡶࡺ࡫ࠧई"))
                else:
                    listitem.setProperty(l1l11_opy_ (u"ࠪ࡭ࡸ࠽࠲࠱ࠩउ"),l1l11_opy_ (u"ࠫ࡫ࡧ࡬ࡴࡧࠪऊ"))
                if self.l11lll_opy_:
                    if l1l11_opy_ (u"ࠬࠦࡀࠡࠩऋ") in channel.title:
                        listitem.setProperty(l1l11_opy_ (u"࠭ࡩࡴࡉࡤࡱࡪ࠭ऌ"),l1l11_opy_ (u"ࠧࡵࡴࡸࡩࠬऍ"))
                        l11ll11l_opy_ = channel.title.partition(l1l11_opy_ (u"ࠣࠪࠥऎ"))
                        l11ll11l_opy_ = l11ll11l_opy_[2].partition(l1l11_opy_ (u"ࠤࠣࡄࠥࠨए"))
                        l11111l_opy_ = l11ll11l_opy_[2].partition(l1l11_opy_ (u"ࠥ࠭ࠥࠨऐ"))
                        l11l1_opy_ = l11111l_opy_[2].partition(l1l11_opy_ (u"ࠦࡢࠨऑ"))
                        l11l1_opy_ = l11l1_opy_[0].partition(l1l11_opy_ (u"ࠧࡡࠢऒ"))
                        l11ll11l_opy_ = l11ll11l_opy_[0]
                        l11111l_opy_ = l11111l_opy_[0]
                        l11l1_opy_ = l1l11_opy_ (u"ࠨ࡛ࡄࡑࡏࡓࡗࠦࡧࡳࡧࡨࡲࡢࡡࡂ࡞ࢽࠣࡗ࡙ࡇࡒࡕࡕࠣࡅ࡙ࡀࠠࠣओ")+l11l1_opy_[0]+l1l11_opy_ (u"ࠢࠡࢭ࡞࠳ࡇࡣ࡛࠰ࡅࡒࡐࡔࡘ࡝ࠣऔ")
                        home_logo = l1l11_opy_ (u"ࠨࡶࡨࡥࡲࡹ࠯ࠨक")+self.l11lll_opy_+l1l11_opy_ (u"ࠩ࠲ࠫख")+l11ll11l_opy_+l1l11_opy_ (u"ࠪ࠲ࡵࡴࡧࠨग")
                        away_logo = l1l11_opy_ (u"ࠫࡹ࡫ࡡ࡮ࡵ࠲ࠫघ")+self.l11lll_opy_+l1l11_opy_ (u"ࠬ࠵ࠧङ")+l11111l_opy_+l1l11_opy_ (u"࠭࠮ࡱࡰࡪࠫच")
                        listitem.setProperty(l1l11_opy_ (u"ࠧࡩࡱࡰࡩࡤࡲ࡯ࡨࡱࠪछ"),home_logo)
                        listitem.setProperty(l1l11_opy_ (u"ࠨࡣࡺࡥࡾࡥ࡬ࡰࡩࡲࠫज"),away_logo)
                        listitem.setProperty(l1l11_opy_ (u"ࠩࡪࡥࡲ࡫࡟ࡵ࡫ࡰࡩࠬझ"),l11l1_opy_)
                        channel.title = channel.title.partition(l1l11_opy_ (u"ࠥࠬࠧञ"))
                        l11ll11_opy_ = channel.title[0]
                        channel.title = channel.title[2].partition(l1l11_opy_ (u"ࠦ࠮ࠨट"))
                        l11l1ll_opy_ = channel.title[0]
                        channel.title = channel.title[2].partition(l1l11_opy_ (u"ࠧࡡࠢठ"))
                        l1_opy_ = channel.title[1]+channel.title[2]
                        channel.title = l11ll11_opy_+l11l1ll_opy_+l1_opy_
                        listitem.setLabel(l1l11_opy_ (u"ࠨ࡛ࡄࡑࡏࡓࡗࠦࠥࡴ࡟ࠨࡷࡠ࠵ࡃࡐࡎࡒࡖࡢࠨड") % (self.l111l1_opy_, channel.title))
                    else:
                        listitem.setProperty(l1l11_opy_ (u"ࠧࡪࡵࡊࡥࡲ࡫ࠧढ"),l1l11_opy_ (u"ࠨࡨࡤࡰࡸ࡫ࠧण"))
                else:
                    listitem.setProperty(l1l11_opy_ (u"ࠩ࡬ࡷࡌࡧ࡭ࡦࠩत"),l1l11_opy_ (u"ࠪࡪࡦࡲࡳࡦࠩथ"))
                self.l1l1ll1l_opy_.append(listitem)
            self.l1ll1_opy_.addItems(self.l1l1ll1l_opy_)
            if not self.l1l1ll1l_opy_:
                l11llll_opy_.ok(helper.title,l1l11_opy_ (u"ࠫࡠࡉࡏࡍࡑࡕࠤࡷ࡫ࡤ࡞࡝ࡅࡡࡓࡵࠠࡦࡸࡨࡲࡹࡹࠠࡴࡥ࡫ࡩࡩࡻ࡬ࡦࡦ࠱࡟࠴ࡈ࡝࡜࠱ࡆࡓࡑࡕࡒ࡞ࠩद"),l1l11_opy_ (u"ࠬ࠭ध"),l1l11_opy_ (u"࠭ࡐ࡭ࡧࡤࡷࡪࠦࡣࡩࡧࡦ࡯ࠥࡨࡡࡤ࡭ࠣࡰࡦࡺࡥࡳࠣࠪन"))
            xbmc.executebuiltin(l1l11_opy_ (u"ࠢࡅ࡫ࡤࡰࡴ࡭࠮ࡄ࡮ࡲࡷࡪ࠮ࡢࡶࡵࡼࡨ࡮ࡧ࡬ࡰࡩࠬࠦऩ"))
        else:
            for channel in helper.l1llll1l_opy_(self.l1l1llll_opy_):
                listitem = xbmcgui.ListItem(channel.title.replace(l1l11_opy_ (u"ࠨࠢࠫ࠵࠵࠾࠰ࠪࠩप"),l1l11_opy_ (u"ࠩࠪफ")).replace(l1l11_opy_ (u"ࠪࠤ࠭࠽࠲࠱ࠫࠪब"),l1l11_opy_ (u"ࠫࠬभ")).replace(l1l11_opy_ (u"ࠬࡡࡃࡐࡎࡒࡖࠥࡨ࡬ࡢࡥ࡮ࡡࠬम"), l1l11_opy_ (u"࡛࠭ࡄࡑࡏࡓࡗࠦࠧय")+self.l111l1_opy_+l1l11_opy_ (u"ࠧ࡞ࠩर")))
                listitem.setProperty(l1l11_opy_ (u"ࠨࡷࡵࡰࠬऱ"), channel.l1l1l1l_opy_)
                listitem.setProperty(l1l11_opy_ (u"ࠩ࡯ࡳ࡬ࡵࠧल"), channel.logo)
                if not channel.l11ll1_opy_ and not self.l11lll_opy_ and not l1l11_opy_ (u"ࠪࠤࡅࠦࠧळ") in channel.title and not l1l11_opy_ (u"ࠫࡕࡖࡖࠨऴ") in self.l1ll1l11_opy_ and not l1l11_opy_ (u"࡚ࠬࡗࡊࡖࡆࡌ࡚ࠥࡖࠨव") in self.l1ll1l11_opy_ and not l1l11_opy_ (u"࠭ࡘ࡙࡚ࠪश") in self.l1ll1l11_opy_:
                    channel.l11ll1_opy_ = l1l11_opy_ (u"ࠧ࡜ࡅࡒࡐࡔࡘࠠࡳࡧࡧࡡࡠࡈ࡝ࡑࡴࡲ࡫ࡷࡧ࡭ࠡ࡫ࡱࡪࡴࡸ࡭ࡢࡶ࡬ࡳࡳࠦࡣࡰ࡯࡬ࡲ࡬ࠦࡳࡰࡱࡱ࠲࠳࠴࡛࠰ࡄࡠ࡟࠴ࡉࡏࡍࡑࡕࡡࠬष")
                    listitem.setProperty(l1l11_opy_ (u"ࠨࡰࡲࡻࡤࡶࡲࡰࡩࡷ࡭ࡹࡲࡥࠨस"), l1l11_opy_ (u"ࠤ࡞ࡇࡔࡒࡏࡓࠢࡵࡩࡩࡣ࡛ࡃ࡟ࡓࡶࡴ࡭ࡲࡢ࡯ࠣ࡭ࡳ࡬࡯ࡳ࡯ࡤࡸ࡮ࡵ࡮ࠡࡥࡲࡱ࡮ࡴࡧࠡࡵࡲࡳࡳ࠴࠮࠯࡝࠲ࡆࡢࡡ࠯ࡄࡑࡏࡓࡗࡣࠢह"))
                else:
                    listitem.setProperty(l1l11_opy_ (u"ࠪࡲࡴࡽ࡟ࡱࡴࡲ࡫ࡹ࡯ࡴ࡭ࡧࠪऺ"), l1l11_opy_ (u"ࠦࡠࡉࡏࡍࡑࡕࠤࡷ࡫ࡤ࡞࡝ࡅࡡࡓࡕࡗ࠻࡝࠲ࡆࡢࡡ࠯ࡄࡑࡏࡓࡗࡣࠠ࡜ࡅࡒࡐࡔࡘࠠࠦࡵࡠ࡟ࡇࡣࠥࡴ࡝࠲ࡆࡢࡡ࠯ࡄࡑࡏࡓࡗࡣࠢऻ") % (self.l111l1_opy_, channel.l11ll1_opy_))
                listitem.setProperty(l1l11_opy_ (u"ࠬࡴࡥࡹࡶࡢࡴࡷࡵࡧࡵ࡫ࡷࡰࡪ़࠭"), l1l11_opy_ (u"ࠨ࡛ࡄࡑࡏࡓࡗࠦࡧࡳࡧࡨࡲࡢࡡࡂ࡞ࡐࡈ࡜࡙ࠦࡩ࡯ࠢ࡞࠳ࡈࡕࡌࡐࡔࡠ࡟ࡈࡕࡌࡐࡔࠣࡱࡪࡪࡩࡶ࡯ࡶࡰࡦࡺࡥࡣ࡮ࡸࡩࡢࠫࡳ࠻࡝࠲ࡆࡢࡡ࠯ࡄࡑࡏࡓࡗࡣࠠ࡜ࡅࡒࡐࡔࡘࠠࠦࡵࡠ࡟ࡇࡣࠥࡴ࡝࠲ࡆࡢࡡ࠯ࡄࡑࡏࡓࡗࡣࠢऽ") % (channel.l1llllll_opy_, self.l111l1_opy_, channel.l11llll1_opy_))
                listitem.setProperty(l1l11_opy_ (u"ࠧ࡯ࡱࡺࡣࡨ࡮࡮ࡱࡴࡲ࡫ࡩ࡫ࡳࡤࠩा"), l1l11_opy_ (u"ࠣ࡝ࡆࡓࡑࡕࡒࠡࠧࡶࡡࡠࡈ࡝ࠦࡵ࡞࠳ࡇࡣ࡛࠰ࡅࡒࡐࡔࡘ࡝ࠣि") % (self.l111l1_opy_,channel.l1lll11l_opy_))
                listitem.setProperty(l1l11_opy_ (u"ࠩࡱࡩࡽࡺ࡟ࡤࡪࡱࡴࡷࡵࡧࡥࡧࡶࡧࠬी"), channel.l1ll11_opy_)
                listitem.setProperty(l1l11_opy_ (u"ࠪ࡭ࡸࡖ࡬ࡢࡻࡤࡦࡱ࡫ࠧु"), l1l11_opy_ (u"ࠫࡹࡸࡵࡦࠩू"))
                listitem.setProperty(l1l11_opy_ (u"ࠬ࡯ࡳࡗࡑࡇ࠰ࠬृ"), l1l11_opy_ (u"࠭ࡦࡢ࡮ࡶࡩࠬॄ"))
                if channel.l11ll1_opy_ != l1l11_opy_ (u"ࠢࠣॅ"):
                    listitem.setProperty(l1l11_opy_ (u"ࠨࡪࡤࡷࡓࡵࡷࠨॆ"),l1l11_opy_ (u"ࠩࡷࡶࡺ࡫ࠧे"))
                else:
                    listitem.setProperty(l1l11_opy_ (u"ࠪ࡬ࡦࡹࡎࡰࡹࠪै"),l1l11_opy_ (u"ࠫ࡫ࡧ࡬ࡴࡧࠪॉ"))
                if channel.l11llll1_opy_ != l1l11_opy_ (u"ࠧࠨॊ"):
                    listitem.setProperty(l1l11_opy_ (u"࠭ࡨࡢࡵࡑࡩࡽࡺࠧो"),l1l11_opy_ (u"ࠧࡵࡴࡸࡩࠬौ"))
                else:
                    listitem.setProperty(l1l11_opy_ (u"ࠨࡪࡤࡷࡓ࡫ࡸࡵ्ࠩ"),l1l11_opy_ (u"ࠩࡩࡥࡱࡹࡥࠨॎ"))
                if self.l11lll11_opy_:
                    listitem.setProperty(l1l11_opy_ (u"ࠪࡗ࡭ࡵࡷࡄࡪࡱࡒࡦࡳࡥࠨॏ"),l1l11_opy_ (u"ࠫࡹࡸࡵࡦࠩॐ"))
                else:
                    listitem.setProperty(l1l11_opy_ (u"࡙ࠬࡨࡰࡹࡆ࡬ࡳࡔࡡ࡮ࡧࠪ॑"),l1l11_opy_ (u"࠭ࡦࡢ࡮ࡶࡩ॒ࠬ"))
                if l1l11_opy_ (u"ࠧࠡࠪ࠴࠴࠽࠶ࠩࠨ॓") in channel.title:
                    listitem.setProperty(l1l11_opy_ (u"ࠨ࡫ࡶ࠵࠵࠾࠰ࠨ॔"),l1l11_opy_ (u"ࠩࡷࡶࡺ࡫ࠧॕ"))
                else:
                    listitem.setProperty(l1l11_opy_ (u"ࠪ࡭ࡸ࠷࠰࠹࠲ࠪॖ"),l1l11_opy_ (u"ࠫ࡫ࡧ࡬ࡴࡧࠪॗ"))
                if l1l11_opy_ (u"ࠬࠦࠨ࠸࠴࠳࠭ࠬक़") in channel.title:
                    listitem.setProperty(l1l11_opy_ (u"࠭ࡩࡴ࠹࠵࠴ࠬख़"),l1l11_opy_ (u"ࠧࡵࡴࡸࡩࠬग़"))
                else:
                    listitem.setProperty(l1l11_opy_ (u"ࠨ࡫ࡶ࠻࠷࠶ࠧज़"),l1l11_opy_ (u"ࠩࡩࡥࡱࡹࡥࠨड़"))
                if self.l11lll_opy_:
                    if l1l11_opy_ (u"ࠪࠤࡅࠦࠧढ़") in channel.title:
                        listitem.setProperty(l1l11_opy_ (u"ࠫ࡮ࡹࡇࡢ࡯ࡨࠫफ़"),l1l11_opy_ (u"ࠬࡺࡲࡶࡧࠪय़"))
                        l11ll11l_opy_ = channel.title.partition(l1l11_opy_ (u"ࠨࠨࠣॠ"))
                        l11ll11l_opy_ = l11ll11l_opy_[2].partition(l1l11_opy_ (u"ࠢࠡࡂࠣࠦॡ"))
                        l11111l_opy_ = l11ll11l_opy_[2].partition(l1l11_opy_ (u"ࠣࠫࠣࠦॢ"))
                        l11l1_opy_ = l11111l_opy_[2].partition(l1l11_opy_ (u"ࠤࡠࠦॣ"))
                        l11l1_opy_ = l11l1_opy_[0].partition(l1l11_opy_ (u"ࠥ࡟ࠧ।"))
                        l11ll11l_opy_ = l11ll11l_opy_[0]
                        l11111l_opy_ = l11111l_opy_[0]
                        try:
                            home_score,away_score,l11l111_opy_ = helper.l111l11_opy_(self.l11lll_opy_.lower(), l11ll11l_opy_+l1l11_opy_ (u"ࠦࠥࡆࠠࠣ॥")+l11111l_opy_)
                        except:
                            home_score = None
                            away_score = None
                            l11l111_opy_ = None
                        l1l11_opy_ (u"ࠬ࠭ࠧࡰࡦࡧࡷࠏࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡶࡵࡽ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡨࡰ࡯ࡨࡣࡵࡵࡩ࡯ࡶࡶࡴࡷ࡫ࡡࡥ࠮ࡤࡻࡦࡿ࡟ࡱࡱ࡬ࡲࡹࡹࡰࡳࡧࡤࡨ࠱ࡵࡶࡦࡴ࡯࡭ࡳ࡫ࠬࡶࡰࡧࡩࡷࡲࡩ࡯ࡧࠣࡁࠥ࡮ࡥ࡭ࡲࡨࡶ࠳࡭ࡥࡵࡡࡲࡨࡩࡹࠨࡴࡧ࡯ࡪ࠳ࡹࡥ࡭ࡧࡦࡸࡪࡪ࡟ࡤࡣࡷࡩ࡬ࡵࡲࡺࡡ࡬ࡷࡘࡶ࡯ࡳࡶ࠱ࡰࡴࡽࡥࡳࠪࠬ࠰ࠥ࡮࡯࡮ࡧࡢࡸࡪࡧ࡭ࠬࠤࠣࡄࠥࠨࠫࡢࡹࡤࡽࡤࡺࡥࡢ࡯ࠬࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࡦࡺࡦࡩࡵࡺ࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࡲࡤࡷࡸࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠪࠫࠬ०")
                        if l11l111_opy_:
                            l11l1_opy_ = l1l11_opy_ (u"ࠨ࡛ࡄࡑࡏࡓࡗࠦࡧࡳࡧࡨࡲࡢࡡࡂ࡞ࢽࠣࠦ१")+l11l111_opy_.replace(l1l11_opy_ (u"ࠧࠩࠩ२"),l1l11_opy_ (u"ࠨࠩ३")).replace(l1l11_opy_ (u"ࠩࠬࠫ४"),l1l11_opy_ (u"ࠪࠫ५"))+l1l11_opy_ (u"ࠦࠥࢱ࡛࠰ࡄࡠ࡟࠴ࡉࡏࡍࡑࡕࡡࠧ६")
                        else:
                            l11l1_opy_ = l1l11_opy_ (u"ࠧࡡࡃࡐࡎࡒࡖࠥ࡭ࡲࡦࡧࡱࡡࡠࡈ࡝ࢼࠢࡖࡘࡆࡘࡔࡔࠢࡄࡘ࠿ࠦࠢ७")+l11l1_opy_[0]+l1l11_opy_ (u"ࠨࠠࢬ࡝࠲ࡆࡢࡡ࠯ࡄࡑࡏࡓࡗࡣࠢ८")
                        home_logo = l1l11_opy_ (u"ࠧࡵࡧࡤࡱࡸ࠵ࠧ९")+self.l11lll_opy_+l1l11_opy_ (u"ࠨ࠱ࠪ॰")+l11ll11l_opy_+l1l11_opy_ (u"ࠩ࠱ࡴࡳ࡭ࠧॱ")
                        away_logo = l1l11_opy_ (u"ࠪࡸࡪࡧ࡭ࡴ࠱ࠪॲ")+self.l11lll_opy_+l1l11_opy_ (u"ࠫ࠴࠭ॳ")+l11111l_opy_+l1l11_opy_ (u"ࠬ࠴ࡰ࡯ࡩࠪॴ")
                        listitem.setProperty(l1l11_opy_ (u"࠭ࡨࡰ࡯ࡨࡣࡱࡵࡧࡰࠩॵ"),home_logo)
                        listitem.setProperty(l1l11_opy_ (u"ࠧࡢࡹࡤࡽࡤࡲ࡯ࡨࡱࠪॶ"),away_logo)
                        listitem.setProperty(l1l11_opy_ (u"ࠨࡩࡤࡱࡪࡥࡴࡪ࡯ࡨࠫॷ"),l11l1_opy_)
                        if home_score and away_score:
                            if home_score > away_score:
                                l11ll1l1_opy_ = home_score
                                l1llll11_opy_ = l1l11_opy_ (u"ࠩ࡞ࡇࡔࡒࡏࡓࠢࡧࡥࡷࡱࡧࡳࡧࡼࡡࠬॸ")+away_score+l1l11_opy_ (u"ࠪ࡟࠴ࡉࡏࡍࡑࡕࡡࠬॹ")
                            else:
                                l11ll1l1_opy_ = l1l11_opy_ (u"ࠫࡠࡉࡏࡍࡑࡕࠤࡩࡧࡲ࡬ࡩࡵࡩࡾࡣࠧॺ")+home_score+l1l11_opy_ (u"ࠬࡡ࠯ࡄࡑࡏࡓࡗࡣࠧॻ")
                                l1llll11_opy_ = away_score
                            listitem.setProperty(l1l11_opy_ (u"࠭ࡨࡰ࡯ࡨࡣࡸࡩ࡯ࡳࡧࠪॼ"),l1l11_opy_ (u"ࠢ࡜ࡄࡠࠦॽ")+l11ll1l1_opy_+l1l11_opy_ (u"ࠣ࡝࠲ࡆࡢࠨॾ"))
                            listitem.setProperty(l1l11_opy_ (u"ࠩࡤࡻࡦࡿ࡟ࡴࡥࡲࡶࡪ࠭ॿ"),l1l11_opy_ (u"ࠥ࡟ࡇࡣࠢঀ")+l1llll11_opy_+l1l11_opy_ (u"ࠦࡠ࠵ࡂ࡞ࠤঁ"))
                        channel.title = channel.title.partition(l1l11_opy_ (u"ࠧ࠮ࠢং"))
                        l11ll11_opy_ = channel.title[0]
                        channel.title = channel.title[2].partition(l1l11_opy_ (u"ࠨࠩࠣঃ"))
                        l11l1ll_opy_ = channel.title[0]
                        channel.title = channel.title[2].partition(l1l11_opy_ (u"ࠢ࡜ࠤ঄"))
                        l1_opy_ = channel.title[1]+channel.title[2]
                        channel.title = l11ll11_opy_+l11l1ll_opy_+l1_opy_
                        listitem.setLabel(l1l11_opy_ (u"ࠣ࡝ࡆࡓࡑࡕࡒࠡࠧࡶࡡࠪࡹ࡛࠰ࡅࡒࡐࡔࡘ࡝ࠣঅ") % (self.l111l1_opy_, channel.title))
                    else:
                        listitem.setProperty(l1l11_opy_ (u"ࠩ࡬ࡷࡌࡧ࡭ࡦࠩআ"),l1l11_opy_ (u"ࠪࡪࡦࡲࡳࡦࠩই"))
                else:
                    listitem.setProperty(l1l11_opy_ (u"ࠫ࡮ࡹࡇࡢ࡯ࡨࠫঈ"),l1l11_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫউ"))
                self.l1l1ll1l_opy_.append(listitem)
            self.l1ll1_opy_.addItems(self.l1l1ll1l_opy_)
            if not self.l1l1ll1l_opy_:
                l11llll_opy_.ok(helper.title,l1l11_opy_ (u"࡛࠭ࡄࡑࡏࡓࡗࠦࡲࡦࡦࡠ࡟ࡇࡣࡎࡰࠢࡨࡺࡪࡴࡴࡴࠢࡶࡧ࡭࡫ࡤࡶ࡮ࡨࡨ࠳ࡡ࠯ࡃ࡟࡞࠳ࡈࡕࡌࡐࡔࡠࠫঊ"),l1l11_opy_ (u"ࠧࠨঋ"),l1l11_opy_ (u"ࠨࡒ࡯ࡩࡦࡹࡥࠡࡥ࡫ࡩࡨࡱࠠࡣࡣࡦ࡯ࠥࡲࡡࡵࡧࡵࠥࠬঌ"))
            xbmc.executebuiltin(l1l11_opy_ (u"ࠤࡇ࡭ࡦࡲ࡯ࡨ࠰ࡆࡰࡴࡹࡥࠩࡤࡸࡷࡾࡪࡩࡢ࡮ࡲ࡫࠮ࠨ঍"))
    def l1l11l1l_opy_(self, url, l1l1l1_opy_=l1l11_opy_ (u"ࠪࠫ঎"), l1l111ll_opy_=l1l11_opy_ (u"ࠫࠬএ"), l1l1111_opy_=l1l11_opy_ (u"ࠬ࠭ঐ")):
        xbmc.executebuiltin(l1l11_opy_ (u"ࠨࡄࡪࡣ࡯ࡳ࡬࠴ࡃ࡭ࡱࡶࡩ࠭ࡨࡵࡴࡻࡧ࡭ࡦࡲ࡯ࡨࠫࠥ঑"))
        self.l1ll1ll_opy_ = True
        l1l11l_opy_ = l1l11_opy_ (u"࡙࡚࡛ࠧࠫ঒"), l1l11_opy_ (u"ࠨࡃࡧࡹࡱࡺࠧও"), l1l11_opy_ (u"ࠩࡄࡨࡺࡲࡴࡴࠩঔ"),l1l11_opy_ (u"ࠪࡅࡉ࡛ࡌࡕࠩক"),l1l11_opy_ (u"ࠫࡆࡊࡕࡍࡖࡖࠫখ"),l1l11_opy_ (u"ࠬࡧࡤࡶ࡮ࡷࠫগ"),l1l11_opy_ (u"࠭ࡡࡥࡷ࡯ࡸࡸ࠭ঘ"),l1l11_opy_ (u"ࠧࡑࡱࡵࡲࠬঙ"),l1l11_opy_ (u"ࠨࡒࡒࡖࡓ࠭চ"),l1l11_opy_ (u"ࠩࡳࡳࡷࡴࠧছ"),l1l11_opy_ (u"ࠪࡔࡴࡸ࡮ࠨজ"),l1l11_opy_ (u"ࠫࡽࡾࡸࠨঝ"), l1l11_opy_ (u"ࠬ࠷࠸ࠬࠩঞ")
        if l1l1l1_opy_ == l1l11_opy_ (u"࠭ࠧট"):
            l1lllll1_opy_ = self.l1ll1_opy_.getSelectedItem()
            l11_opy_ = l1lllll1_opy_.getProperty(l1l11_opy_ (u"ࠧ࡭ࡱࡪࡳࠬঠ"))
            l1llll_opy_ = l1lllll1_opy_.getLabel().replace(l1l11_opy_ (u"ࠨ࡝ࡆࡓࡑࡕࡒࠡࡤ࡯ࡥࡨࡱ࡝ࠨড"),l1l11_opy_ (u"ࠩ࡞ࡇࡔࡒࡏࡓࠢࡺ࡬࡮ࡺࡥ࡞ࠩঢ"))
            l1111ll_opy_ = l1lllll1_opy_.getProperty(l1l11_opy_ (u"ࠪࡲࡴࡽ࡟ࡤࡪࡱࡴࡷࡵࡧࡥࡧࡶࡧࠬণ")).replace(l1l11_opy_ (u"ࠫࡠࡉࡏࡍࡑࡕࠤࡧࡲࡡࡤ࡭ࡠࠫত"),l1l11_opy_ (u"ࠬࡡࡃࡐࡎࡒࡖࠥࡽࡨࡪࡶࡨࡡࠬথ"))
        else:
            l1llll_opy_ = l1l1l1_opy_
            l11_opy_ = l1l1111_opy_
            l1111ll_opy_ = l1l111ll_opy_
        if self.l1l11ll_opy_:
            if any(s in l1llll_opy_ for s in l1l11l_opy_) or any(s in self.l1ll1l11_opy_ for s in l1l11l_opy_):
                xbmc.executebuiltin((l1l11_opy_ (u"ࡻ࡙ࠧࡄࡐࡇ࠳ࡔ࡯ࡵ࡫ࡩ࡭ࡨࡧࡴࡪࡱࡱࠬࠧࡖࡡࡳࡧࡱࡸࡦࡲ࠭ࡍࡱࡦ࡯ࠥࡋ࡮ࡢࡤ࡯ࡩࡩࠧࠢ࠭ࠢࠥࡇ࡭ࡧ࡮࡯ࡧ࡯ࡷࠥࡳࡡࡺࠢࡦࡳࡳࡺࡡࡪࡰࠣࡥࡩࡻ࡬ࡵࠢࡦࡳࡳࡺࡥ࡯ࡶࠥ࠰ࠥ࠸࠰࠱࠲ࠬࠫদ")))
                text = l11llll_opy_.input(l1l11_opy_ (u"ࠢࡑࡣࡵࡩࡳࡺࡡ࡭࠯ࡏࡳࡨࡱ࠺ࠡࡒ࡯ࡩࡦࡹࡥࠡࡧࡱࡸࡪࡸࠠࡺࡱࡸࡶࠥࡖࡡࡳࡧࡱࡸࡦࡲࠠࡄࡱࡧࡩࠧধ"), type=xbmcgui.INPUT_NUMERIC, option=xbmcgui.ALPHANUM_HIDE_INPUT)
                if text!=self.l1lll_opy_:
                    xbmc.executebuiltin((l1l11_opy_ (u"ࡶ࡛ࠩࡆࡒࡉ࠮ࡏࡱࡷ࡭࡫࡯ࡣࡢࡶ࡬ࡳࡳ࠮ࠢࡑࡣࡵࡩࡳࡺࡡ࡭࠯ࡏࡳࡨࡱࠠࡆࡴࡵࡳࡷࠧࠢ࠭ࠢࠥࡍࡳࡩ࡯ࡳࡴࡨࡧࡹࠦࡣࡰࡦࡨࠥࠧ࠲ࠠ࠴࠲࠳࠴࠮࠭ন")))
                    return
        try:
            listitem = xbmcgui.ListItem(l1l11_opy_ (u"ࠩࡗ࡭ࡹࡲࡥࠨ঩"), thumbnailImage=l11_opy_)
            listitem.setInfo(l1l11_opy_ (u"ࠪࡺ࡮ࡪࡥࡰࠩপ"), {l1l11_opy_ (u"࡙ࠫ࡯ࡴ࡭ࡧࠪফ"): l1llll_opy_, l1l11_opy_ (u"ࠬࡖ࡬ࡰࡶࠪব"): l1111ll_opy_})
        except:
            pass
        url = url+l1l11_opy_ (u"࠭ࡼࡽࡗࡶࡩࡷ࠳ࡁࡨࡧࡱࡸࡂ࠭ভ")+helper.l11l11_opy_+l1l11_opy_ (u"ࠧ࠰ࠩম")+helper.l11l_opy_
        if l1l11_opy_ (u"ࠨ࠱ࡰࡳࡻ࡯ࡥ࠰ࠩয") in url:
            xbmc.executebuiltin(l1l11_opy_ (u"ࠩࡻࡦࡲࡩ࠮ࡱ࡮ࡤࡽࡲ࡫ࡤࡪࡣࠫࠫর") + url + l1l11_opy_ (u"ࠪ࠭ࠬ঱"))
        else:
            xbmc.Player().play(item=url, listitem=listitem)
    def init(self, level, pos=-1):
        if level == l1l11_opy_ (u"ࠫࡨࡧࡴࡦࡩࡲࡶࡾ࠭ল"):
            self.l1l1ll1l_opy_ = []
            self.l1ll1_opy_.reset()
            self.l11ll1l_opy_ = [helper.l1l111l_opy_]
            self.l1ll11l1_opy_ = -1
            if self.l11l1lll_opy_ > -1:
                self.l11l11l_opy_.getListItem(self.l11l1lll_opy_).setProperty(l1l11_opy_ (u"ࠬࡩ࡬ࡪࡥ࡮ࡩࡩ࠭঳"), l1l11_opy_ (u"࠭ࡦࡢ࡮ࡶࡩࠬ঴"))
            self.l11l11l_opy_.getSelectedItem().setProperty(l1l11_opy_ (u"ࠧࡤ࡮࡬ࡧࡰ࡫ࡤࠨ঵"), l1l11_opy_ (u"ࠨࡶࡵࡹࡪ࠭শ"))
            self.l11l1lll_opy_ = self.l11l11l_opy_.getSelectedPosition()
            self.l1l1llll_opy_ = self.l11l11l_opy_.getListItem(self.l11l1lll_opy_).getProperty(l1l11_opy_ (u"ࠩࡸࡶࡱ࠭ষ"))
            self.l1ll1l11_opy_ = self.l11l11l_opy_.getListItem(self.l11l1lll_opy_).getLabel()
        elif level == l1l11_opy_ (u"ࠪࡧࡦࡺࡥࡨࡱࡵࡽࡤࡼ࡯ࡥࠩস"):
            if self.l1ll11l1_opy_ > -1:
                self.l1ll1_opy_.getListItem(self.l1ll11l1_opy_).setProperty(l1l11_opy_ (u"ࠫࡨࡲࡩࡤ࡭ࡨࡨࠬহ"), l1l11_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫ঺"))
            self.l1ll1_opy_.getSelectedItem().setProperty(l1l11_opy_ (u"࠭ࡣ࡭࡫ࡦ࡯ࡪࡪࠧ঻"), l1l11_opy_ (u"ࠧࡵࡴࡸࡩ়ࠬ"))
            if pos == 0:
                self.l1ll11l1_opy_ = 0
            else:
                self.l1ll11l1_opy_ = self.l1ll1_opy_.getSelectedPosition()
            if self.l1ll11l1_opy_ > -1:
                if self.l1ll1_opy_.getListItem(self.l1ll11l1_opy_).getProperty(l1l11_opy_ (u"ࠨ࡫ࡶࡆࡦࡩ࡫ࠨঽ")) == l1l11_opy_ (u"ࠩࡷࡶࡺ࡫ࠧা"):
                    self.l11ll1l_opy_.remove(self.l1l1llll_opy_)
            self.l1l1llll_opy_ = self.l1ll1_opy_.getListItem(self.l1ll11l1_opy_).getProperty(l1l11_opy_ (u"ࠪࡹࡷࡲࠧি"))
            if not self.l1l1llll_opy_ in self.l11ll1l_opy_:
                self.l11ll1l_opy_.append(self.l1l1llll_opy_)
            self.l1ll11l1_opy_ = -1
        elif level == l1l11_opy_ (u"ࠫࡨ࡮ࡡ࡯ࡰࡨࡰࠬী"):
            if self.l1ll11l1_opy_ > -1:
                self.l1ll1_opy_.getListItem(self.l1ll11l1_opy_).setProperty(l1l11_opy_ (u"ࠬࡩ࡬ࡪࡥ࡮ࡩࡩ࠭ু"), l1l11_opy_ (u"࠭ࡦࡢ࡮ࡶࡩࠬূ"))
            self.l1ll1_opy_.getSelectedItem().setProperty(l1l11_opy_ (u"ࠧࡤ࡮࡬ࡧࡰ࡫ࡤࠨৃ"), l1l11_opy_ (u"ࠨࡶࡵࡹࡪ࠭ৄ"))
            self.l1ll11l1_opy_ = self.l1ll1_opy_.getSelectedPosition()
    def l1l1ll11_opy_(self):
        l1lllll1_opy_ = self.l1ll1_opy_.getSelectedItem()
        l1l1l11_opy_ = l1lllll1_opy_.getLabel()
        l1lll111_opy_ = l1lllll1_opy_.getProperty(l1l11_opy_ (u"ࠩࡸࡶࡱ࠭৅"))
        l1lllll_opy_ = l1lllll1_opy_.getProperty(l1l11_opy_ (u"ࠪࡰࡴ࡭࡯ࠨ৆"))
        l1l1lll_opy_ = l1lllll1_opy_.getProperty(l1l11_opy_ (u"ࠫ࡮ࡹ࠱࠱࠺࠳ࠫে"))
        l1ll1ll1_opy_ = l1lllll1_opy_.getProperty(l1l11_opy_ (u"ࠬ࡯ࡳ࠸࠴࠳ࠫৈ"))
        l11l1ll1_opy_ = l1lllll1_opy_.getProperty(l1l11_opy_ (u"࠭ࡩࡴࡉࡤࡱࡪ࠭৉"))
        if l11l1ll1_opy_ == l1l11_opy_ (u"ࠧࡵࡴࡸࡩࠬ৊"):
            if l1l11_opy_ (u"ࠨࠢࡃࠤࠬো") in l1l1l11_opy_:
                l1l1l11_opy_ = l1l1l11_opy_.partition(l1l11_opy_ (u"ࠤࡠࠦৌ"))
                l1l1l11_opy_ = l1l1l11_opy_[2]
                l1l1l11_opy_ = l1l1l11_opy_.partition(l1l11_opy_ (u"ࠥࠤࡠࠨ্"))
                l1l1l11_opy_ = l1l11_opy_ (u"ࠦࡠࡈ࡝ࠣৎ")+l1l1l11_opy_[0]+l1l11_opy_ (u"ࠧࡡ࠯ࡃ࡟ࠥ৏")
        if l1l1lll_opy_ == l1l11_opy_ (u"࠭ࡴࡳࡷࡨࠫ৐"):
            l1l1l11_opy_ = l1l1l11_opy_+l1l11_opy_ (u"ࠢࠡࠪ࠴࠴࠽࠶ࠩࠣ৑")
        if l1ll1ll1_opy_ == l1l11_opy_ (u"ࠨࡶࡵࡹࡪ࠭৒"):
            l1l1l11_opy_ = l1l1l11_opy_+l1l11_opy_ (u"ࠤࠣࠬ࠼࠸࠰ࠪࠤ৓")
        if l1l11_opy_ (u"ࠪࡼࡽࡾࠧ৔") in self.l1ll1l11_opy_.lower():
            return
        if l1l11_opy_ (u"ࠫ࠳ࡺࡳࠨ৕") in l1lll111_opy_ or l1l11_opy_ (u"ࠬ࠴࡭ࡱ࠶ࠪ৖") in l1lll111_opy_:
            l1l11l1_opy_ = helper.l1l1ll11_opy_(l1l1l11_opy_,l1lll111_opy_,l1lllll_opy_,self)
        if helper.l1l11111_opy_ and not self.l1l1ll1_opy_:
            self.l1l11ll1_opy_()
            self.l11l11l_opy_.reset()
            self.l11l11l_opy_.addItems(self.l1ll111l_opy_)
            self.l11l1lll_opy_ = self.l11l1lll_opy_ + 1
            self.l11l11l_opy_.getListItem(self.l11l1lll_opy_).setProperty(l1l11_opy_ (u"࠭ࡣ࡭࡫ࡦ࡯ࡪࡪࠧৗ"), l1l11_opy_ (u"ࠧࡵࡴࡸࡩࠬ৘"))
            self.l11l11l_opy_.selectItem(self.l11l1lll_opy_)
        if l1l11l1_opy_ and self.l1l1llll_opy_ == l1l11_opy_ (u"ࠨࡥࡸࡷࡹࡵ࡭ࡠࡨࡤࡺࡴࡸࡩࡵࡧࡶࠫ৙"):
            if self.l1l1ll1_opy_ and not helper.l1l11111_opy_:
                self.l1l11ll1_opy_()
                self.l11l11l_opy_.reset()
                self.l11l11l_opy_.addItems(self.l1ll111l_opy_)
                self.l11l1lll_opy_ = 0
                self.l11l11l_opy_.selectItem(self.l11l1lll_opy_)
                self.l1l1ll1_opy_ = False
            if helper.l1l11111_opy_:
                self.l11lllll_opy_()
            else:
                self.l1l1ll1l_opy_ = []
            self.l1ll1_opy_.reset()
            self.l1ll1_opy_.addItems(self.l1l1ll1l_opy_)
            if not self.l1l1ll1l_opy_:
                self.setFocus(self.window.getControl(210))
    def onAction(self, action):
        try:
            if self.l1ll1l1l_opy_ == 230:
                if action.getId() == l1l1lll1_opy_:
                    self.l1l1ll11_opy_()
                    return
                if action.getId() in [l1lll1l1_opy_, l1lll1_opy_, l111111_opy_] and self.l1ll1_opy_.getListItem(0).getLabel() == l1l11_opy_ (u"ࠩ࠱࠲࠳࠭৚"):
                    l1lllll1_opy_ = self.l1ll1_opy_.getListItem(0)
                    l1111l_opy_ = l1lllll1_opy_.getProperty(l1l11_opy_ (u"ࠪࡹࡷࡲࠧ৛"))
                    if l1l11_opy_ (u"ࠫ࡬࡫ࡴࡠࡸࡲࡨࡤࡹࡣࡢࡶࡨ࡫ࡴࡸࡩࡦࡵࠪড়") in l1111l_opy_ or l1l11_opy_ (u"ࠬ࡭ࡥࡵࡡࡹࡳࡩࡥࡣࡢࡶࡨ࡫ࡴࡸࡩࡦࡵࠪঢ়") in l1111l_opy_:
                        self.init(l1l11_opy_ (u"࠭ࡣࡢࡶࡨ࡫ࡴࡸࡹࡠࡸࡲࡨࠬ৞"), 0)
                        self.l1ll1111_opy_(l1111l_opy_)
                        self.l1ll1_opy_.reset()
                        self.l1ll1_opy_.addItems(self.l1l1ll1l_opy_)
                        if self.l1l1ll1l_opy_:
                            self.setFocus(self.window.getControl(230))
                    elif l1l11_opy_ (u"ࠧࡨࡧࡷࡣࡻࡵࡤࡠࡵࡷࡶࡪࡧ࡭ࡴࠩয়") in l1111l_opy_:
                        self.init(l1l11_opy_ (u"ࠨࡥࡤࡸࡪ࡭࡯ࡳࡻࡢࡺࡴࡪࠧৠ"), 0)
                        self.l1l1ll_opy_(l1111l_opy_)
                        self.l1ll1_opy_.reset()
                        self.l1ll1_opy_.addItems(self.l1l1ll1l_opy_)
                        if self.l1l1ll1l_opy_:
                            self.setFocus(self.window.getControl(230))
                    return
            xbmcgui.WindowXMLDialog.onAction(self, action)
        except:
            pass
    def onFocus(self, controlId):
        if controlId in [210, 230]:
            self.l1ll1l1l_opy_ = controlId
        if controlId == 69:
            xbmc.executebuiltin(l1l11_opy_ (u"ࠤࡄࡧࡹ࡯ࡶࡢࡶࡨ࡛࡮ࡴࡤࡰࡹࠫࡪࡺࡲ࡬ࡴࡥࡵࡩࡪࡴࡶࡪࡦࡨࡳ࠮ࠨৡ"))
    def onClick(self, controlId):
        try:
            xbmc.executebuiltin(l1l11_opy_ (u"ࠥࡅࡨࡺࡩࡷࡣࡷࡩ࡜࡯࡮ࡥࡱࡺࠬࡧࡻࡳࡺࡦ࡬ࡥࡱࡵࡧࠪࠤৢ"))
            if controlId in [90, 130]:
                if controlId == 90:
                    addon.openSettings()
                    self.l11lll11_opy_ = addon.getSetting(l1l11_opy_ (u"ࠫࡸ࡮࡯ࡸࡥ࡫ࡥࡳࡴࡥ࡭ࡰࡤࡱࡪ࠭ৣ")) == l1l11_opy_ (u"ࠬࡺࡲࡶࡧࠪ৤")
                    self.l1l11ll_opy_ = addon.getSetting(l1l11_opy_ (u"࠭ࡰࡢࡴࡨࡲࡹࡧ࡬ࡰࡥ࡮ࠫ৥")) == l1l11_opy_ (u"ࠧࡵࡴࡸࡩࠬ০")
                    self.l1lll_opy_ = addon.getSetting(l1l11_opy_ (u"ࠨࡲࡤࡶࡪࡴࡴࡢ࡮ࡦࡳࡩ࡫ࠧ১"))
                    if l1l11_opy_ (u"ࠩࡪࡩࡹࡥࡶࡰࡦࡢࡧࡦࡺࡥࡨࡱࡵ࡭ࡪࡹࠧ২") in self.l1l1llll_opy_:
                        self.l1ll1111_opy_()
                    elif l1l11_opy_ (u"ࠪ࡫ࡪࡺ࡟ࡷࡱࡧࡣࡸࡺࡲࡦࡣࡰࡷࠬ৩") in self.l1l1llll_opy_:
                        self.l1l1ll_opy_(self.l1l1llll_opy_)
                    else:
                        self.l11lllll_opy_()
                    self.l1ll1_opy_.reset()
                    self.l1ll1_opy_.addItems(self.l1l1ll1l_opy_)
                    self.l1ll1_opy_.selectItem(self.l1ll11l1_opy_)
                elif controlId == 130:
                    l1111_opy_ = xbmcaddon.Addon(id=l1l11_opy_ (u"ࠫࡵࡲࡵࡨ࡫ࡱ࠲ࡵࡸ࡯ࡨࡴࡤࡱ࠳ࡸࡥ࡭ࡱࡤࡨࡪࡪࡴࡷࠩ৪"))
                    l1111_opy_.setSetting(l1l11_opy_ (u"ࠬࡸࡥ࡭ࡱࡤࡨࡪࡪ࠮ࡶࡵࡨࡶࠬ৫"), username)
                    l1111_opy_.setSetting(l1l11_opy_ (u"࠭ࡲࡦ࡮ࡲࡥࡩ࡫ࡤ࠯ࡲࡤࡷࡸ࠭৬"), password)
                    xbmc.executebuiltin(l1l11_opy_ (u"ࠢࡓࡷࡱࡅࡩࡪ࡯࡯ࠪࡳࡰࡺ࡭ࡩ࡯࠰ࡳࡶࡴ࡭ࡲࡢ࡯࠱ࡶࡪࡲ࡯ࡢࡦࡨࡨࡹࡼࠩࠣ৭"))
                xbmc.executebuiltin(l1l11_opy_ (u"ࠣࡆ࡬ࡥࡱࡵࡧ࠯ࡅ࡯ࡳࡸ࡫ࠨࡣࡷࡶࡽࡩ࡯ࡡ࡭ࡱࡪ࠭ࠧ৮"))
                return
            if controlId == 210:
                self.init(l1l11_opy_ (u"ࠩࡦࡥࡹ࡫ࡧࡰࡴࡼࠫ৯"))
                l1l1l1ll_opy_ = self.l11l11l_opy_.getSelectedItem()
                l1111l_opy_ = l1l1l1ll_opy_.getProperty(l1l11_opy_ (u"ࠪࡹࡷࡲࠧৰ"))
                l111_opy_ = l1l1l1ll_opy_.getLabel()
                if l1l11_opy_ (u"ࠫ࡬࡫ࡴࡠࡸࡲࡨࡤࡩࡡࡵࡧࡪࡳࡷ࡯ࡥࡴࠩৱ") in l1111l_opy_:
                    self.l1ll1111_opy_()
                else:
                    if l1l11_opy_ (u"ࠬࡓࡌࡃࠩ৲") in l111_opy_:
                        self.l11lll_opy_ = l1l11_opy_ (u"࠭ࡍࡍࡄࠪ৳")
                    elif l1l11_opy_ (u"ࠧࡏࡊࡏࠫ৴") in l111_opy_:
                        self.l11lll_opy_ = l1l11_opy_ (u"ࠨࡐࡋࡐࠬ৵")
                    elif l1l11_opy_ (u"ࠩࡑࡊࡑ࠭৶") in l111_opy_:
                        self.l11lll_opy_ = l1l11_opy_ (u"ࠪࡒࡋࡒࠧ৷")
                    elif l1l11_opy_ (u"ࠫࡓࡈࡁࠨ৸") in l111_opy_:
                        self.l11lll_opy_ = l1l11_opy_ (u"ࠬࡔࡂࡂࠩ৹")
                    else:
                        self.l11lll_opy_ = False
                    self.l11lllll_opy_()
                if self.l1l1ll1l_opy_:
                    self.setFocus(self.window.getControl(230))
            elif controlId == 230:
                l1lllll1_opy_ = self.l1ll1_opy_.getSelectedItem()
                l1111l_opy_ = l1lllll1_opy_.getProperty(l1l11_opy_ (u"࠭ࡵࡳ࡮ࠪ৺"))
                if l1l11_opy_ (u"ࠧࡨࡧࡷࡣࡻࡵࡤࡠࡵࡦࡥࡹ࡫ࡧࡰࡴ࡬ࡩࡸ࠭৻") in l1111l_opy_ or l1l11_opy_ (u"ࠨࡩࡨࡸࡤࡼ࡯ࡥࡡࡦࡥࡹ࡫ࡧࡰࡴ࡬ࡩࡸ࠭ৼ") in l1111l_opy_:
                    self.init(l1l11_opy_ (u"ࠩࡦࡥࡹ࡫ࡧࡰࡴࡼࡣࡻࡵࡤࠨ৽"))
                    self.l1ll1111_opy_(l1111l_opy_)
                    self.l1ll1_opy_.reset()
                    self.l1ll1_opy_.addItems(self.l1l1ll1l_opy_)
                    if self.l1l1ll1l_opy_:
                        self.setFocus(self.window.getControl(230))
                elif l1l11_opy_ (u"ࠪ࡫ࡪࡺ࡟ࡷࡱࡧࡣࡸࡺࡲࡦࡣࡰࡷࠬ৾") in l1111l_opy_:
                    self.init(l1l11_opy_ (u"ࠫࡨࡧࡴࡦࡩࡲࡶࡾࡥࡶࡰࡦࠪ৿"))
                    self.l1l1ll_opy_(l1111l_opy_)
                    self.l1ll1_opy_.reset()
                    self.l1ll1_opy_.addItems(self.l1l1ll1l_opy_)
                    if self.l1l1ll1l_opy_:
                        self.setFocus(self.window.getControl(230))
                else:
                    self.init(l1l11_opy_ (u"ࠬࡩࡨࡢࡰࡱࡩࡱ࠭਀"))
                    if l1lllll1_opy_.getProperty(l1l11_opy_ (u"࠭ࡩࡴࡒ࡯ࡥࡾࡧࡢ࡭ࡧࠪਁ")) == l1l11_opy_ (u"ࠧࡵࡴࡸࡩࠬਂ"):
                        if self.l111ll1_opy_ == l1l11_opy_ (u"ࠨࡶࡵࡹࡪ࠭ਃ"):
                            l111l1l_opy_ = re.compile(l1l11_opy_ (u"ࠩ࠱࠮࠴࠮࠮ࠫࡁࠬ࠲ࡹࡹࠧ਄")).findall(l1111l_opy_.replace(l1l11_opy_ (u"ࠪ࠲ࡲ࠹ࡵ࠹ࠩਅ"),l1l11_opy_ (u"ࠫ࠳ࡺࡳࠨਆ")))
                            for i in l111l1l_opy_:
                                l111l1l_opy_ = i
                            if helper.l1l1l1l1_opy_(l111l1l_opy_):
                                name = l1lllll1_opy_.getLabel().replace(l1l11_opy_ (u"ࠬࡡࡃࡐࡎࡒࡖࠥࡨ࡬ࡢࡥ࡮ࡡࠬਇ"),l1l11_opy_ (u"࡛࠭ࡄࡑࡏࡓࡗࠦࡷࡩ࡫ࡷࡩࡢ࠭ਈ")).replace(l1l11_opy_ (u"ࠧࠡࠪ࠴࠴࠽࠶ࠩࠨਉ"),l1l11_opy_ (u"ࠨࠩਊ")).replace(l1l11_opy_ (u"ࠩࠣࠬ࠼࠸࠰ࠪࠩ਋"),l1l11_opy_ (u"ࠪࠫ਌"))
                                ll_opy_ = l11llll_opy_.select(helper.title,[l1l11_opy_ (u"ࠦ࡜ࡧࡴࡤࡪࠣࠦ਍")+name+l1l11_opy_ (u"ࠧࠦࡌࡪࡸࡨࠥࠧ਎"), l1l11_opy_ (u"ࠨࡔࡗࡅࡤࡸࡨ࡮ࡵࡱࠢࡩࡳࡷࠦࠢਏ")+name])
                                if ll_opy_ == 0:
                                    self.l1l11l1l_opy_(l1111l_opy_)
                                    return
                                elif ll_opy_ == 1:
                                    helper.l1ll1l_opy_(l111l1l_opy_, name, self)
                                    return
                            else:
                                self.l1l11l1l_opy_(l1111l_opy_)
                                return
                        else:
                            self.l1l11l1l_opy_(l1111l_opy_)
                            return
            xbmc.executebuiltin(l1l11_opy_ (u"ࠢࡅ࡫ࡤࡰࡴ࡭࠮ࡄ࡮ࡲࡷࡪ࠮ࡢࡶࡵࡼࡨ࡮ࡧ࡬ࡰࡩࠬࠦਐ"))
        except Exception:
            xbmc.executebuiltin(l1l11_opy_ (u"ࠣࡆ࡬ࡥࡱࡵࡧ࠯ࡅ࡯ࡳࡸ࡫ࠨࡣࡷࡶࡽࡩ࡯ࡡ࡭ࡱࡪ࠭ࠧ਑"))
            pass
if __name__ == l1l11_opy_ (u"ࠤࡢࡣࡲࡧࡩ࡯ࡡࡢࠦ਒"):
    xbmc.executebuiltin(l1l11_opy_ (u"ࠥࡈ࡮ࡧ࡬ࡰࡩ࠱ࡇࡱࡵࡳࡦࠪࡥࡹࡸࡿࡤࡪࡣ࡯ࡳ࡬࠯ࠢਓ"))
    xbmc.executebuiltin(l1l11_opy_ (u"ࠦࡆࡩࡴࡪࡸࡤࡸࡪ࡝ࡩ࡯ࡦࡲࡻ࠭ࡨࡵࡴࡻࡧ࡭ࡦࡲ࡯ࡨࠫࠥਔ"))
    l11lll1_opy_ = helper.l11ll_opy_()
    if l11lll1_opy_ != 1:
        xbmc.executebuiltin(l1l11_opy_ (u"ࠧࡊࡩࡢ࡮ࡲ࡫࠳ࡉ࡬ࡰࡵࡨࠬࡧࡻࡳࡺࡦ࡬ࡥࡱࡵࡧࠪࠤਕ"))
        addon.openSettings()
        sys.exit(0)
    gui = l111ll_opy_(l1l11_opy_ (u"࠭ࡳࡤࡴ࡬ࡴࡹ࠳ࡲࡦ࡮ࡲࡥࡩ࡫ࡤࡵࡸ࠱ࡼࡲࡲࠧਖ"), l11ll111_opy_, SKIN)
    gui.doModal()
    del gui
    xbmc.executebuiltin(l1l11_opy_ (u"ࠢࡅ࡫ࡤࡰࡴ࡭࠮ࡄ࡮ࡲࡷࡪ࠮ࡢࡶࡵࡼࡨ࡮ࡧ࡬ࡰࡩࠬࠦਗ"))