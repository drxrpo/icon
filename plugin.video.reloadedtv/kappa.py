# coding: UTF-8
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
import xbmcgui
import xbmcaddon
addon = xbmcaddon.Addon(l1l11_opy_ (u"ࠨࡲ࡯ࡹ࡬࡯࡮࠯ࡸ࡬ࡨࡪࡵ࠮ࡳࡧ࡯ࡳࡦࡪࡥࡥࡶࡹࠫਘ"))
def l11l11ll_opy_():
	l11llll_opy_ = xbmcgui.Dialog()
	l11l1l11_opy_ = addon.getSetting(l1l11_opy_ (u"ࠩࡳࡥࡷ࡫࡮ࡵࡣ࡯ࡧࡴࡪࡥࠨਙ"))
	l11l1l1l_opy_ = l11llll_opy_.input(l1l11_opy_ (u"ࠪࡔࡦࡸࡥ࡯ࡶࡤࡰ࠲ࡒ࡯ࡤ࡭࠽ࠤࡕࡲࡥࡢࡵࡨࠤࡪࡴࡴࡦࡴࠣࡽࡴࡻࡲࠡࡥࡸࡶࡷ࡫࡮ࡵࠢࡓࡥࡷ࡫࡮ࡵࡣ࡯ࠤࡈࡵࡤࡦࠩਚ"), type=xbmcgui.INPUT_NUMERIC, option=xbmcgui.ALPHANUM_HIDE_INPUT)
	if l11l1l1l_opy_ == l11l1l11_opy_ or l11l1l11_opy_ == l1l11_opy_ (u"ࠫࠬਛ"):
		l11l11l1_opy_ = l11llll_opy_.input(l1l11_opy_ (u"ࠬࡖ࡬ࡦࡣࡶࡩࠥࡹࡥࡵࠢࡼࡳࡺࡸࠠ࡯ࡧࡺࠤࡕࡧࡲࡦࡰࡷࡥࡱࠦࡃࡰࡦࡨࠫਜ"), type=xbmcgui.INPUT_NUMERIC, option=xbmcgui.ALPHANUM_HIDE_INPUT)
		addon.setSetting(l1l11_opy_ (u"࠭ࡰࡢࡴࡨࡲࡹࡧ࡬ࡤࡱࡧࡩࠬਝ"), l11l11l1_opy_)
	else:
		xbmc.executebuiltin((l1l11_opy_ (u"ࡵࠨ࡚ࡅࡑࡈ࠴ࡎࡰࡶ࡬ࡪ࡮ࡩࡡࡵ࡫ࡲࡲ࠭ࠨࡐࡢࡴࡨࡲࡹࡧ࡬࠮ࡎࡲࡧࡰࠦࡅࡳࡴࡲࡶࠦࠨࠬࠡࠤࡌࡲࡨࡵࡲࡳࡧࡦࡸࠥࡩ࡯ࡥࡧࠤࠦ࠱ࠦ࠳࠱࠲࠳࠭ࠬਞ")))
		return
l11l11ll_opy_()