# coding: UTF-8
import sys
l1111ll1_opy_ = sys.version_info [0] == 2
l1l11ll1_opy_ = 2048
l111llll_opy_ = 7
def l1lll1_opy_ (l1ll111_opy_):
	global l1l1l111_opy_
	l11ll11l_opy_ = ord (l1ll111_opy_ [-1])
	l1l1ll_opy_ = l1ll111_opy_ [:-1]
	l1lll11l_opy_ = l11ll11l_opy_ % len (l1l1ll_opy_)
	l1l11l1_opy_ = l1l1ll_opy_ [:l1lll11l_opy_] + l1l1ll_opy_ [l1lll11l_opy_:]
	if l1111ll1_opy_:
		l1l11l_opy_ = unicode () .join ([unichr (ord (char) - l1l11ll1_opy_ - (l1111_opy_ + l11ll11l_opy_) % l111llll_opy_) for l1111_opy_, char in enumerate (l1l11l1_opy_)])
	else:
		l1l11l_opy_ = str () .join ([chr (ord (char) - l1l11ll1_opy_ - (l1111_opy_ + l11ll11l_opy_) % l111llll_opy_) for l1111_opy_, char in enumerate (l1l11l1_opy_)])
	return eval (l1l11l_opy_)
import tools
import base64
import xbmcgui
def l1ll1lll1_opy_():
	xbmc.executebuiltin(l1lll1_opy_ (u"ࠬࡊࡩࡢ࡮ࡲ࡫࠳ࡉ࡬ࡰࡵࡨࠬ࠶࠶࠱࠵࠲ࠬࠫ०"))
	l111111_opy_ = xbmcgui.Dialog()
	l1ll1llll_opy_ = tools.get_setting(l1ll1ll1l_opy_(l1lll1_opy_ (u"ࠨࡤ࡮ࡈࡸ࡞࡜࠷ࡨࡢ࠴࠼ࡺ࡟ࡇ࠽࠾ࠤ१")))
	l1lll1111_opy_ = l111111_opy_.input(l1ll1ll1l_opy_(l1lll1_opy_ (u"ࠧࡖࡉࡻࡰ࡞࡞ࡎ࡭ࡋࡊ࡚ࡺࡪࡇࡗࡻࡌࡌࡱࡼࡤ࡙ࡋࡪ࡝࠸࡜ࡹࡤ࡯࡙ࡹࡩࡉࡂࡒ࡛࡛ࡎࡱࡨ࡮ࡓࡪࡥࡇࡇࡊࡢ࠳ࡔ࡯ࠫ२")), type=xbmcgui.INPUT_NUMERIC, option=xbmcgui.ALPHANUM_HIDE_INPUT)
	if l1lll1111_opy_ == l1ll1llll_opy_ or l1ll1llll_opy_ == l1lll1_opy_ (u"ࠨࠩ३"):
		l1ll1ll11_opy_ = l111111_opy_.input(l1ll1ll1l_opy_(l1lll1_opy_ (u"ࠩࡘࡋࡽࡲ࡙࡙ࡐ࡯ࡍࡍࡔ࡬ࡥࡅࡅ࠹ࡧ࠹ࡖࡺࡋࡊ࠹ࡱࡪࡹࡃࡓ࡜࡜ࡏࡲࡢ࡯ࡔ࡫ࡦࡈࡈࡄࡣ࠴ࡕࡰࠬ४")), type=xbmcgui.INPUT_NUMERIC, option=xbmcgui.ALPHANUM_HIDE_INPUT)
		tools.set_setting(l1ll1ll1l_opy_(l1lll1_opy_ (u"ࠥࡨࡲࡌࡵ࡛࡙࠴࡬ࡦ࠸࠹ࡷ࡜ࡄࡁࡂࠨ५")), l1ll1ll11_opy_)
		tools.set_setting(l1ll1ll1l_opy_(l1lll1_opy_ (u"ࠦࡩࡳࡆࡶ࡜࡚࠵࡭ࡨࡈࡗࡴࡤࡻࡂࡃࠢ६")), l1lll1_opy_ (u"ࠬࡺࡲࡶࡧࠪ७"))
		tools.open_settings_dialog()
	else:
		xbmc.executebuiltin((l1lll1_opy_ (u"ࡻ࡙ࠧࡄࡐࡇ࠳ࡔ࡯ࡵ࡫ࡩ࡭ࡨࡧࡴࡪࡱࡱࠬࠧࡖࡡࡳࡧࡱࡸࡦࡲ࠭ࡍࡱࡦ࡯ࠥࡋࡲࡳࡱࡵࠥࠧ࠲ࠠࠣࡋࡱࡧࡴࡸࡲࡦࡥࡷࠤࡨࡵࡤࡦࠣࠥ࠰ࠥ࠹࠰࠱࠲ࠬࠫ८")))
		tools.open_settings_dialog()
		return
def l1ll1ll1l_opy_(data):
	video = base64.b64decode(data)
	return video
l1ll1lll1_opy_()