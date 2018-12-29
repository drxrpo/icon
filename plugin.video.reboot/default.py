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
import urllib,urllib2,sys,re,xbmcgui,xbmcaddon,datetime,os,json,base64,requests,pyxbmct,tools,thread,threading,time
import xml.etree.ElementTree as ElementTree
reload(sys)
sys.setdefaultencoding(l1lll1_opy_ (u"ࠫࡺࡺࡦ࠹ࠩࠀ"))
l1l1ll1l_opy_=l1lll1_opy_ (u"ࠧ࠻࠱࠶ࠤࠁ")
l111l111_opy_ = tools.get_runtime_path()
global status
global ll_opy_
ADDON = xbmcaddon.Addon(id=l1lll1_opy_ (u"࠭ࡰ࡭ࡷࡪ࡭ࡳ࠴ࡶࡪࡦࡨࡳ࠳ࡸࡥࡣࡱࡲࡸࠬࠂ"))
l11l1111_opy_ = ADDON.getAddonInfo(l1lll1_opy_ (u"ࠧࡷࡧࡵࡷ࡮ࡵ࡮ࠨࠃ"))
l111l1l1_opy_ = ADDON.getAddonInfo(l1lll1_opy_ (u"ࠨ࡫ࡧࠫࠄ"))
l111lll1_opy_ = ADDON.getAddonInfo(l1lll1_opy_ (u"ࠩࡱࡥࡲ࡫ࠧࠅ"))
l1lll1l1_opy_ = ADDON.getSetting(l1lll1_opy_ (u"ࠪࡷࡰ࡯࡮ࠨࠆ"))
l1l11111_opy_ = ADDON.getAddonInfo(l1lll1_opy_ (u"ࠫࡵࡧࡴࡩࠩࠇ"))
l11l1l_opy_ = os.path.join(l1l11111_opy_, l1lll1_opy_ (u"ࠬࡸࡥࡴࡱࡸࡶࡨ࡫ࡳࠨࠈ"))
l11l111_opy_ = os.path.join(l11l1l_opy_, l1lll1_opy_ (u"࠭ࡳ࡬࡫ࡱࡷࠬࠉ"), l1lll1l1_opy_, l1lll1_opy_ (u"ࠧ࡮ࡧࡧ࡭ࡦ࠭ࠊ"), l1lll1_opy_ (u"ࠨࡤࡤࡧࡰ࡭ࡲࡰࡷࡱࡨ࠳ࡶ࡮ࡨࠩࠋ"))
l11_opy_ = os.path.join(l11l1l_opy_, l1lll1_opy_ (u"ࠩࡶ࡯࡮ࡴࡳࠨࠌ"), l1lll1l1_opy_, l1lll1_opy_ (u"ࠪࡱࡪࡪࡩࡢࠩࠍ"))
l1lll111l_opy_ = xbmc.translatePath(os.path.join(l1lll1_opy_ (u"ࠫࡸࡶࡥࡤ࡫ࡤࡰ࠿࠵࠯ࡩࡱࡰࡩ࠴ࡧࡤࡥࡱࡱࡷࠬࠎ"),l1lll1_opy_ (u"ࠬࡸࡥࡱࡱࡶ࡭ࡹࡵࡲࡺ࠰ࡐ࠱࡙࡜ࡇࡶ࡫ࡧࡩࠬࠏ")))
ll_opy_ = l1lll1_opy_ (u"ࠨࡨࡵࡶࡳ࠾࠴࠵ࡴࡢࡴࡪࡩࡹࡩࡲࡦࡣࡷࡩࡸ࠴ࡣࡰ࡯࠲ࡥࡩࡪ࡯࡯࠱࡬ࡱࡦ࡭ࡥࡴ࠰ࡷࡼࡹࠨࠐ")
def run():
    global l1ll1l_opy_
    global l11l1l11_opy_
    global l11lll_opy_
    global l1lll11_opy_
    global host
    global l1lll1l1l_opy_
    global l111ll1_opy_
    global version
    global l1l1l1l1_opy_
    global port
    global username
    global password
    global l1111l1l_opy_
    global l1l11ll_opy_
    version = int(l11l111l_opy_(l1lll1_opy_ (u"ࠢࡎࡓࡀࡁࠧࠑ")))
    username=tools.get_setting(l1lll1_opy_ (u"ࠣࡗࡶࡩࡷࡴࡡ࡮ࡧࠥࠒ"))
    password=tools.get_setting(l1lll1_opy_ (u"ࠤࡓࡥࡸࡹࡷࡰࡴࡧࠦࠓ"))
    l1111l1l_opy_=tools.get_setting(l1lll1_opy_ (u"ࠥࡷ࡭ࡵࡷ࡮ࡣࡼࡴࡷࡵࠢࠔ")) == l1lll1_opy_ (u"ࠫࡹࡸࡵࡦࠩࠕ")
    l1l11ll_opy_=tools.get_setting(l1lll1_opy_ (u"ࠧࡹࡨࡰࡹࡰࡥࡾ࡬ࡲࡦࡧࠥࠖ")) == l1lll1_opy_ (u"࠭ࡴࡳࡷࡨࠫࠗ")
    if not username:
        username = l1lll1_opy_ (u"ࠢࡏࡑࡑࡉࠧ࠘")
        password=l1lll1_opy_ (u"ࠣࡐࡒࡒࡊࠨ࠙")
    host=l11l_opy_()
    port=l1lll1_opy_ (u"ࠤ࠵࠴࠽࠼ࠢࠚ")
    if sys.argv[0] != l1lll1_opy_ (u"ࠪࡴࡱࡻࡧࡪࡰ࠽࠳࠴ࡶ࡬ࡶࡩ࡬ࡲ࠳ࡼࡩࡥࡧࡲ࠲ࡷ࡫ࡢࡰࡱࡷ࠳ࠬࠛ"):
        l111111_opy_ = xbmcgui.Dialog()
        l111111_opy_.ok(l1lll1_opy_ (u"ࠫࡠࡉࡏࡍࡑࡕࠤࡷ࡫ࡤ࡞ࡉࡈࡅࡗ࡙࡛࠰ࡅࡒࡐࡔࡘ࡝࡜ࡅࡒࡐࡔࡘࠠࡸࡪ࡬ࡸࡪࡣࠠࡕࡘ࡞࠳ࡈࡕࡌࡐࡔࡠࠫࠜ"),l1lll1_opy_ (u"ࠬࡋࡲࡳࡱࡵࠥࠥ࡟࡯ࡶࠢ࡫ࡥࡻ࡫ࠠࡣࡧࡨࡲࠥࡪࡥࡵࡧࡦࡸࡪࡪࠠࡵࡴࡼ࡭ࡳ࡭ࠠࡵࡱࠣࡷࡹ࡫ࡡ࡭ࠢࡲࡹࡷࠦࡡࡥࡦࡲࡲ࠳࠭ࠝ"),l1lll1_opy_ (u"࠭ࡎࡪࡥࡨࠤࡹࡸࡹ࠯࠰࠱ࠫࠞ"),l1lll1_opy_ (u"ࠧࡏࡱࡺࠤ࡬ࡵࠠࡧࡷࡦ࡯ࠥࡿ࡯ࡶࡴࡶࡩࡱ࡬࠮ࠨࠟ"))
        sys.exit()
    l111ll1_opy_=tools.get_setting(l1lll1_opy_ (u"ࠣࡲࡤࡶࡪࡴࡴࡢ࡮ࡲࡧࡰࠨࠠ"))
    l1l1l1l1_opy_=tools.get_setting(l1lll1_opy_ (u"ࠤࡶ࡬ࡴࡽࡸࡹࡺࠥࠡ"))
    l1ll1l_opy_ = l1lll1_opy_ (u"ࠥࡋࡪࡧࡲࡴࠢࡗ࡚ࠥࠨࠢ")
    l1lll1l1l_opy_ = os.path.join( tools.get_runtime_path() , l1lll1_opy_ (u"ࠦࡷ࡫ࡳࡰࡷࡵࡧࡪࡹࠢࠣ") , l1lll1_opy_ (u"ࠧࡧࡲࡵࠤࠤ") )
    tools.log(l1ll1l_opy_+l11l111l_opy_(l1lll1_opy_ (u"ࠨࡕ࠴ࡔ࡫ࡧࡳࡘࡰࡣ࡯ࡦ࡫ࡩ࡞ࡁ࠾ࠤࠥ")))
    l11l1l11_opy_ = l11l111l_opy_(l1lll1_opy_ (u"ࠢࡋ࡚ࡐ࠺ࡏ࡞ࡍࡷ࡜࡚࠹ࡵࡠ࠲࠲ࡪࡐ࡭࠺ࡽࡡࡉࡃ࠲ࡨ࡝ࡔ࡬ࡤ࡯࠸࡬ࡧ࡝ࡕ࠺ࡌ࡛ࡑࡲࡩࡇࡇࡼࡦ࠷ࡩࡼࡣ࡮ࡓ࠼ࡎ࡝ࡓ࡭ࡥࡊ࡯ࡻ࡟࡚࠱࡯࡜࡛ࡖ࡫ࡨࡇ࡭࠴࡝࡚࠾ࡰ࡙࡙ࡔ࡯࡞࠷࠿ࡹࡢ࡙࡙ࡾࠧࠦ"))%(host,port,username,password)
    l11lll_opy_ = l11l111l_opy_(l1lll1_opy_ (u"ࠣࡌ࡛ࡑ࠻ࡐࡘࡎࡸ࡝࡛࠺ࡶ࡚࠳࠳࡫ࡑ࡮࠻ࡷࡢࡊࡄ࠳ࡩ࡞ࡎ࡭ࡥࡰ࠹࡭ࡨࡗࡖ࠻ࡍ࡜ࡒࡳࡣࡈࡈࡽࡧ࠸ࡪࡶࡤ࡯ࡔ࠽ࡏ࡞ࡍ࡮ࡦࡋࡰࡼࡠࡔ࠲ࡰ࡝࡜ࡗ࡬ࡤ࡮࠻࡮࡜࠷ࡔࡨࡥࡉ࡙ࡲࡧ࠹ࡊࡱ࡜࡛ࡑࡂࠨࠧ"))%(host,port,username,password)
    l1lll11_opy_ = l11l111l_opy_(l1lll1_opy_ (u"ࠤࡍ࡜ࡒ࠼ࡊ࡙ࡏࡹࡧࡌࡌࡵ࡛࡙ࡻࡪ࡞࡞ࡂࡱࡎࡱࡆࡴࡩࡄ࠺࠳ࡦ࠶࡛ࡿࡢ࡮ࡈࡷ࡞࡙࠶࡬ࡤࡻ࡝ࡻ࡞࡞ࡎࡻࡦ࠵࠽ࡾࡠࡄ࠱࡮ࡦࡻࡂࡃࠢࠨ"))%(host,port,username,password)
    params = tools.get_params()
    if params.get(l1lll1_opy_ (u"ࠥࡥࡨࡺࡩࡰࡰࠥࠩ")) is None:
        l111l11l_opy_(params)
    else:
        action = params.get(l1lll1_opy_ (u"ࠦࡦࡩࡴࡪࡱࡱࠦࠪ"))
        exec action+l1lll1_opy_ (u"ࠧ࠮ࡰࡢࡴࡤࡱࡸ࠯ࠢࠫ")
    tools.close_item_list()
def l111l11l_opy_(params):
    tools.log(l1ll1l_opy_+l11l111l_opy_(l1lll1_opy_ (u"ࠨࡔࡘࡈࡳࡦ࡮ࡈࡎ࡛࡙࠸࠵ࠧࠬ"))+repr(params))
    status = l1l1lll_opy_()
    if sys.argv[0] != l1lll1_opy_ (u"ࠧࡱ࡮ࡸ࡫࡮ࡴ࠺࠰࠱ࡳࡰࡺ࡭ࡩ࡯࠰ࡹ࡭ࡩ࡫࡯࠯ࡴࡨࡦࡴࡵࡴ࠰ࠩ࠭"):
        l111111_opy_ = xbmcgui.Dialog()
        l111111_opy_.ok(l1lll1_opy_ (u"ࠨ࡝ࡆࡓࡑࡕࡒࠡࡴࡨࡨࡢࡍࡅࡂࡔࡖ࡟࠴ࡉࡏࡍࡑࡕࡡࡠࡉࡏࡍࡑࡕࠤࡼ࡮ࡩࡵࡧࡠࠤ࡙࡜࡛࠰ࡅࡒࡐࡔࡘ࡝ࠨ࠮"),l1lll1_opy_ (u"ࠩࡈࡶࡷࡵࡲࠢࠢ࡜ࡳࡺࠦࡨࡢࡸࡨࠤࡧ࡫ࡥ࡯ࠢࡧࡩࡹ࡫ࡣࡵࡧࡧࠤࡹࡸࡹࡪࡰࡪࠤࡹࡵࠠࡴࡶࡨࡥࡱࠦ࡯ࡶࡴࠣࡥࡩࡪ࡯࡯࠰ࠪ࠯"),l1lll1_opy_ (u"ࠪࡒ࡮ࡩࡥࠡࡶࡵࡽ࠳࠴࠮ࠨ࠰"),l1lll1_opy_ (u"ࠫࡓࡵࡷࠡࡩࡲࠤ࡫ࡻࡣ࡬ࠢࡼࡳࡺࡸࡳࡦ࡮ࡩ࠲ࠬ࠱"))
        sys.exit()
    l1l1111l_opy_ = l11l11_opy_(l1lll1_opy_ (u"ࠬࡳࡡࡪࡰ࡬ࡱࡦ࡭ࡥࠨ࠲"))
    if l1l1111l_opy_ == l1lll1_opy_ (u"࠭ࡆࡢ࡮ࡶࡩࠬ࠳"):
        l1l1111l_opy_ = os.path.join(l1lll1l1l_opy_,l11l111l_opy_(l1lll1_opy_ (u"ࠢࡣࡉ࠼ࡲࡧࡿ࠵ࡸࡤࡰࡧࡂࠨ࠴")))
    if status == 1:
       tools.log(l1ll1l_opy_+l11l111l_opy_(l1lll1_opy_ (u"ࠣࡖࡊ࠽ࡳࡧࡗ࠵ࡩࡘ࠷࡛ࡰ࡙࠳ࡘࡽࡧࡼࡃ࠽ࠣ࠵")))
       if l1l111l1_opy_():
        tools.add_item(action=l1lll1_opy_ (u"ࠤࠥ࠶"),  title=l1l111l1_opy_(), thumbnail=l1l1111l_opy_ , fanart=os.path.join(l1lll1l1l_opy_,l11l111l_opy_(l1lll1_opy_ (u"ࠥ࡞ࡲࡌࡵ࡚࡚ࡍ࠴ࡑࡴࡂࡶ࡜ࡺࡁࡂࠨ࠷"))) , folder=False)
       tools.add_item(action=l1lll1_opy_ (u"ࠦࡆࡩࡣࡰࡷࡱࡸࠧ࠸"),  title=l1lll1_opy_ (u"ࠧࡡࡃࡐࡎࡒࡖࠥ࡭࡯࡭ࡦࡠ࡟ࡇࡣࡍࡺࠢࡄࡧࡨࡵࡵ࡯ࡶࠣࡍࡳ࡬࡯࡜࠱ࡅࡡࡠ࠵ࡃࡐࡎࡒࡖࡢࠨ࠹") , thumbnail=l1l1111l_opy_ , fanart=os.path.join(l1lll1l1l_opy_,l11l111l_opy_(l1lll1_opy_ (u"ࠨ࡚࡮ࡈࡸ࡝࡝ࡐ࠰ࡍࡰࡅࡹ࡟ࡽ࠽࠾ࠤ࠺"))) , folder=False)
       tools.add_item(action=l1lll1_opy_ (u"ࠢࡎࡣࡼࡪࡦ࡯ࡲࠣ࠻"),  title=l1lll1_opy_ (u"ࠣ࡝ࡆࡓࡑࡕࡒࠡࡴࡨࡨࡢࡡࡂ࡞ࡎ࡬ࡺࡪࠦࡔࡗ࡝࠲ࡆࡢࡡ࠯ࡄࡑࡏࡓࡗࡣࠢ࠼") , thumbnail=l1l1111l_opy_ , fanart=os.path.join(l1lll1l1l_opy_,l11l111l_opy_(l1lll1_opy_ (u"ࠤ࡝ࡱࡋࡻ࡙࡙ࡌ࠳ࡐࡳࡈࡵ࡛ࡹࡀࡁࠧ࠽"))) , folder=True)
       if l1111l1l_opy_:
        tools.add_item(action=l1lll1_opy_ (u"ࠥࡱࡕࡘࡏࠣ࠾"),  title=l1lll1_opy_ (u"ࠦࡠࡉࡏࡍࡑࡕࠤ࡫࡬࠴࠷࠺࠵ࡦ࠹ࡣ࡛ࡃ࡟ࡐ࡟ࡈࡕࡌࡐࡔࠣࡪ࡫ࡉ࠰ࡄ࠲ࡆ࠴ࡢࡧࡹࡧࡣ࡬ࡶࠥࡡࡃࡐࡎࡒࡖࠥ࡬ࡦ࠵࠸࠻࠶ࡧ࠺࡝ࡈ࡝ࡆࡓࡑࡕࡒࠡࡨࡩࡇ࠵ࡉ࠰ࡄ࠲ࡠࡹ࡮ࡪࡥ࡜ࡅࡒࡐࡔࡘࠠࡨࡱ࡯ࡨࡢࠦࡐࡓࡑ࡞࠳ࡇࡣ࡛࠰ࡅࡒࡐࡔࡘ࡝ࠣ࠿") , thumbnail=os.path.join(l1lll1l1l_opy_,l11l111l_opy_(l1lll1_opy_ (u"ࠧࡨࡘࡃࡻࡥࡽ࠺ࡽࡢ࡮ࡥࡀࠦࡀ"))) , fanart=os.path.join(l1lll1l1l_opy_,l11l111l_opy_(l1lll1_opy_ (u"ࠨ࡚࡮ࡈࡸ࡝࡝ࡐ࠰ࡍࡰࡅࡹ࡟ࡽ࠽࠾ࠤࡁ"))) , folder=False)
       if l1l11ll_opy_:
        if not l1111l1_opy_:
            tools.add_item(action=l1lll1_opy_ (u"ࠢ࡮ࡈࡕࡉࡊࠨࡂ"),  title=l1lll1_opy_ (u"ࠣ࡝ࡆࡓࡑࡕࡒࠡࡨࡩ࠴࠵࠾࠴ࡧࡨࡠ࡟ࡇࡣࡍ࡜ࡅࡒࡐࡔࡘࠠࡨࡪࡲࡷࡹࡽࡨࡪࡶࡨࡡ࠲ࡡ࠯ࡄࡑࡏࡓࡗࡣ࡛ࡄࡑࡏࡓࡗࠦࡹࡦ࡮࡯ࡳࡼࡣࡔࡗࠢࡊࡹ࡮ࡪࡥࠡࡈࡵࡩࡪࡡ࠯ࡃ࡟࡞࠳ࡈࡕࡌࡐࡔࡠࠦࡃ") , thumbnail=os.path.join(l1lll1l1l_opy_,l11l111l_opy_(l1lll1_opy_ (u"ࠤࡥ࡛࡟ࡿ࡚ࡘࡗࡸࡧࡌ࠻࡮ࠣࡄ"))) , fanart=os.path.join(l1lll1l1l_opy_,l11l111l_opy_(l1lll1_opy_ (u"ࠥ࡞ࡲࡌࡵ࡚࡚ࡍ࠴ࡑࡴࡂࡶ࡜ࡺࡁࡂࠨࡅ"))) , folder=False)
       tools.add_item(action=l1lll1_opy_ (u"ࠦࡈࡲࡥࡢࡴࡢࡇࡦࡩࡨࡦࠤࡆ"),  title=l1lll1_opy_ (u"ࠧࡡࡃࡐࡎࡒࡖࠥࡲࡩ࡮ࡧࡠ࡟ࡇࡣࡃ࡭ࡧࡤࡶࠥࡉࡡࡤࡪࡨࠤࡦࡴࡤࠡࡒࡤࡧࡰࡧࡧࡦࡵ࡞࠳ࡇࡣ࡛࠰ࡅࡒࡐࡔࡘ࡝ࠣࡇ") , thumbnail=l1l1111l_opy_ , fanart=os.path.join(l1lll1l1l_opy_,l11l111l_opy_(l1lll1_opy_ (u"ࠨ࡚࡮ࡈࡸ࡝࡝ࡐ࠰ࡍࡰࡅࡹ࡟ࡽ࠽࠾ࠤࡈ"))) , folder=False)
       tools.add_item(action=l1lll1_opy_ (u"ࠢࡄࡪࡨࡧࡰࡌ࡯ࡳࡗࡳࡨࡦࡺࡥࡴࠤࡉ"), title=l1lll1_opy_ (u"ࠣ࡝ࡆࡓࡑࡕࡒࠡࡤ࡯ࡹࡪࡣ࡛ࡃ࡟ࡆ࡬ࡪࡩ࡫ࠡࡨࡲࡶ࡛ࠥࡰࡥࡣࡷࡩࡸࡡ࠯ࡃ࡟࡞࠳ࡈࡕࡌࡐࡔࡠࠦࡊ") , thumbnail=l1l1111l_opy_ , fanart=os.path.join(l1lll1l1l_opy_,l11l111l_opy_(l1lll1_opy_ (u"ࠤ࡝ࡱࡋࡻ࡙࡙ࡌ࠳ࡐࡳࡈࡵ࡛ࡹࡀࡁࠧࡋ"))), folder=False)
       tools.add_item(action=l1lll1_opy_ (u"ࠥࡈࡴࡽ࡮ࡄࡪࡤࡲࡳ࡫࡬ࡴࠤࡌ"), title=l1lll1_opy_ (u"ࠦࡠࡉࡏࡍࡑࡕࠤࡷ࡫ࡤ࡞࡝ࡅࡡࡗ࡫ࡰࡰࡴࡷࡩࡩࠦࡃࡩࡣࡱࡲࡪࡲࡳ࡜࠱ࡅࡡࡠ࠵ࡃࡐࡎࡒࡖࡢࠨࡍ") , thumbnail=l1l1111l_opy_ , fanart=os.path.join(l1lll1l1l_opy_,l11l111l_opy_(l1lll1_opy_ (u"ࠧࡠ࡭ࡇࡷ࡜࡜ࡏ࠶ࡌ࡯ࡄࡸ࡞ࡼࡃ࠽ࠣࡎ"))), folder=False)
       tools.add_item(action=l1lll1_opy_ (u"ࠨ࡯ࡱࡧࡱࡣࡸ࡫ࡴࡵ࡫ࡱ࡫ࡸࠨࡏ"), title=l1lll1_opy_ (u"ࠢ࡜ࡅࡒࡐࡔࡘࠠࡸࡪ࡬ࡸࡪࡣ࡛ࡃ࡟ࡖࡩࡹࡺࡩ࡯ࡩࡶ࡟࠴ࡈ࡝࡜࠱ࡆࡓࡑࡕࡒ࡞ࠤࡐ") , thumbnail=l1l1111l_opy_ , fanart=os.path.join(l1lll1l1l_opy_,l11l111l_opy_(l1lll1_opy_ (u"ࠣ࡜ࡰࡊࡺ࡟ࡘࡋ࠲ࡏࡲࡇࡻ࡚ࡸ࠿ࡀࠦࡑ"))), folder=False)
       tools.set_view(tools.LIST)
    else:
        window = pyxbmct.AddonDialogWindow(l1lll1_opy_ (u"ࠩ࡞ࡇࡔࡒࡏࡓࠢࡵࡩࡩࡣࡌࡰࡩ࡬ࡲࠥ࡫ࡲࡳࡱࡵࠥࡠ࠵ࡃࡐࡎࡒࡖࡢ࠭ࡒ"))
        window.setGeometry(800, 400, 3, 1)
        background=pyxbmct.Image(l11l111_opy_)
        window.placeControl(background, 0, 0, 3, 1)
        l11ll1l_opy_ = pyxbmct.Label(l1lll1_opy_ (u"ࠪ࡟ࡈࡕࡌࡐࡔࠣࡶࡪࡪ࡝࡜ࡄࡠࡉࡷࡸ࡯ࡳࠣࠣࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦ࡬ࡰࡩ࡬ࡲࠥࡺ࡯ࠡࡉࡨࡥࡷࡹࠠࡕࡘࠤ࡟࠴ࡈ࡝࡜࠱ࡆࡓࡑࡕࡒ࡞ࠩࡓ"), alignment=pyxbmct.ALIGN_CENTER)
        l1ll1_opy_ = pyxbmct.TextBox()
        window.placeControl(l11ll1l_opy_, 0, 0)
        window.placeControl(l1ll1_opy_ , 1, 0)
        l1ll1_opy_.setText(l1lll1_opy_ (u"ࠫࡌ࡫ࡡࡳࡵࠣࡘ࡛ࠦࡲࡦࡳࡸ࡭ࡷ࡫ࡳࠡࡣࡱࠤࡦࡩࡴࡪࡸࡨࠤࡦࡩࡣࡰࡷࡱࡸ࠱ࠦࡰ࡭ࡧࡤࡷࡪࠦࡥ࡯ࡶࡨࡶࠥࡿ࡯ࡶࡴࠣࡋࡪࡧࡲࡴࠢࡗ࡚ࠥࡇࡣࡤࡱࡸࡲࡹࠦࡤࡦࡶࡤ࡭ࡱࡹ࠮ࠡ࡞ࡱࡠࡳࡏࡦࠡࡻࡲࡹࠥࡪ࡯ࠡࡰࡲࡸࠥ࡮ࡡࡷࡧࠣࡥࠥࡍࡥࡢࡴࡶࠤ࡙࡜ࠠࡢࡥࡦࡳࡺࡴࡴ࠭ࠢࡳࡰࡪࡧࡳࡦࠢࡵࡩࡦࡪࠠࡵࡪࡨࠤࡵ࡯࡮࡯ࡧࡧࠤࡵࡵࡳࡵࠢࡲࡲࠥࡵࡵࡳࠢࡩࡥࡨ࡫ࡢࡰࡱ࡮ࠤࡵࡧࡧࡦ࠼ࠣ࡬ࡹࡺࡰ࠻࠱࠲ࡪࡦࡩࡥࡣࡱࡲ࡯࠳ࡩ࡯࡮࠱ࡪࡶࡴࡻࡰࡴ࠱ࡕࡩࡧࡵ࡯ࡵ࠴࠷࠻ࠥࡺ࡯ࠡࡲࡸࡶࡨ࡮ࡡࡴࡧࠣࡥࡳࠦࡡࡤࡥࡲࡹࡳࡺ࠮ࠨࡔ"))
        l1lllll_opy_ = pyxbmct.Button(l1lll1_opy_ (u"ࠬࡡࡃࡐࡎࡒࡖࠥࡸࡥࡥ࡟࡞ࡆࡢࡕࡋ࡜࠱ࡅࡡࡠ࠵ࡃࡐࡎࡒࡖࡢ࠭ࡕ"))
        window.placeControl(l1lllll_opy_, 2, 0)
        window.setFocus(l1lllll_opy_)
        window.connect(l1lllll_opy_, window.close)
        window.connect(pyxbmct.ACTION_NAV_BACK, window.close)
        window.doModal()
        del window
        l111111_opy_ = xbmcgui.Dialog()
        l1l1_opy_ = l111111_opy_.yesno(l1lll1_opy_ (u"࡛࠭ࡄࡑࡏࡓࡗࠦࡲࡦࡦࡠࡋࡊࡇࡒࡔ࡝࠲ࡇࡔࡒࡏࡓ࡟࡞ࡇࡔࡒࡏࡓࠢࡺ࡬࡮ࡺࡥ࡞ࠢࡗ࡚ࡠ࠵ࡃࡐࡎࡒࡖࡢ࠭ࡖ"),l1lll1_opy_ (u"ࠧࡘࡱࡸࡰࡩࠦࡹࡰࡷࠣࡰ࡮ࡱࡥࠡࡶࡲࠤࡪࡴࡴࡦࡴࠣࡽࡴࡻࡲࠡ࡝ࡆࡓࡑࡕࡒࠡࡴࡨࡨࡢࡍࡅࡂࡔࡖ࡟࠴ࡉࡏࡍࡑࡕࡡࡠࡉࡏࡍࡑࡕࠤࡼ࡮ࡩࡵࡧࡠࠤ࡙࡜࡛࠰ࡅࡒࡐࡔࡘ࡝ࠡࡣࡦࡧࡴࡻ࡮ࡵࠢࡧࡩࡹࡧࡩ࡭ࡵࠣࡲࡴࡽ࠿ࠨࡗ"),l1lll1_opy_ (u"ࠨࠩࡘ"),l1lll1_opy_ (u"࡙ࠩࠪ"),l1lll1_opy_ (u"ࠪࡒࡴ࡚࠭"),l1lll1_opy_ (u"ࠫ࡞࡫ࡳࠨ࡛"))
        if l1l1_opy_:
            l1ll11ll_opy_()
            run()
        if not l1l1_opy_:
            sys.exit()
        else:
            sys.exit()
def open_settings(params):
    tools.log(l1ll1l_opy_+l11l111l_opy_(l1lll1_opy_ (u"࡛ࠧ࠲ࡗ࠲ࡧࡋࡱࡻ࡚࠴ࡏࡪࡦ࡜࡜ࡵࡥࡓࡀࡁࠧ࡜"))+repr(params))
    tools.open_settings_dialog()
def l1ll11ll_opy_():
    l111111_opy_ = xbmcgui.Dialog()
    l1l1lll1_opy_ = l111111_opy_.input(l1lll1_opy_ (u"࠭ࡅ࡯ࡶࡨࡶࠥࡿ࡯ࡶࡴࠣ࡟ࡈࡕࡌࡐࡔࠣࡶࡪࡪ࡝ࡈࡇࡄࡖࡘࡡ࠯ࡄࡑࡏࡓࡗࡣ࡛ࡄࡑࡏࡓࡗࠦࡷࡩ࡫ࡷࡩࡢࠦࡔࡗ࡝࠲ࡇࡔࡒࡏࡓ࡟࡙ࠣࡸ࡫ࡲ࡯ࡣࡰࡩࠦ࠭࡝"), type=xbmcgui.INPUT_ALPHANUM)
    pw = l111111_opy_.input(l1lll1_opy_ (u"ࠧࡆࡰࡷࡩࡷࠦࡹࡰࡷࡵࠤࡠࡉࡏࡍࡑࡕࠤࡷ࡫ࡤ࡞ࡉࡈࡅࡗ࡙࡛࠰ࡅࡒࡐࡔࡘ࡝࡜ࡅࡒࡐࡔࡘࠠࡸࡪ࡬ࡸࡪࡣࠠࡕࡘ࡞࠳ࡈࡕࡌࡐࡔࡠࠤࡕࡧࡳࡴࡹࡲࡶࡩࠧࠧ࡞"), type=xbmcgui.INPUT_ALPHANUM, option=xbmcgui.ALPHANUM_HIDE_INPUT)
    tools.set_setting(l1lll1_opy_ (u"ࠨࡗࡶࡩࡷࡴࡡ࡮ࡧࠪ࡟"), l1l1lll1_opy_)
    tools.set_setting(l1lll1_opy_ (u"ࠩࡓࡥࡸࡹࡷࡰࡴࡧࠫࡠ"), pw)
def l11l111l_opy_(l1lllll11_opy_):
    l1ll_opy_ = base64.b64decode(l1lllll11_opy_)
    return l1ll_opy_
def l1ll1ll_opy_():
    try:
        req = urllib2.Request(l1lll11_opy_)
        req.add_header(l11l111l_opy_(l1lll1_opy_ (u"࡚ࠥ࡝ࡔ࡬ࡤ࡫࠴ࡆ࡟࠸ࡖࡶࡦࡄࡁࡂࠨࡡ")) , l111l1l1_opy_+l1lll1_opy_ (u"ࠦ࠴ࡼࠢࡢ")+l11l1111_opy_)
        response = urllib2.urlopen(req)
        link=response.read()
        l1ll111l_opy_ = json.loads(link.decode(l1lll1_opy_ (u"ࠬࡻࡴࡧ࠺ࠪࡣ")))
        response.close()
        if l1ll111l_opy_:
            tools.log(l1ll1l_opy_+l11l111l_opy_(l1lll1_opy_ (u"ࠨࡡ࡮ࡔ࡫ࡨࡌࡋࡧࡣࡉ࠼࡬࡟ࡍࡖ࡬ࡋࡄࡁࡂࠨࡤ")))
        return l1ll111l_opy_
    except:
        l111111_opy_ = xbmcgui.Dialog()
        l111111_opy_.ok(l111lll1_opy_, l1lll1_opy_ (u"ࠧ࡜ࡅࡒࡐࡔࡘࠠࡳࡧࡧࡡࡠࡈ࡝ࡆࡴࡵࡳࡷࠦࡣࡰࡰࡱࡩࡨࡺࡩ࡯ࡩࠣࡸࡴࠦࡳࡦࡴࡹࡩࡷ࡛ࠧ࠰ࡄࡠ࡟࠴ࡉࡏࡍࡑࡕࡡࠬࡥ"),l1lll1_opy_ (u"ࠨࠩࡦ"), l1lll1_opy_ (u"ࠩ࡞ࡇࡔࡒࡏࡓࠢ࡯࡭ࡲ࡫ࡧࡳࡧࡨࡲࡢࡡࡂ࡞ࡒ࡯ࡩࡦࡹࡥࠡࡶࡵࡽࠥࡧࡧࡢ࡫ࡱࠤࡴࡸࠠࡤࡪࡨࡧࡰࠦࡦࡰࡴࠣࡳࡺࡸࠠ࡭ࡣࡷࡩࡸࡺࠠࡪࡰࡩࡳࡷࡳࡡࡵ࡫ࡲࡲࠥࡧࡳࠡࡹࡨࠤࡲࡧࡹࠡࡤࡨࠤࡵ࡫ࡲࡧࡱࡵࡱࡦ࡯࡮ࡨࠢࡰࡥ࡮ࡴࡴࡦࡰࡤࡲࡨ࡫࠮࡜࠱ࡅࡡࡠ࠵ࡃࡐࡎࡒࡖࡢ࠭ࡧ"))
        sys.exit()
def l1l1lll_opy_():
        l1l111ll_opy_ = l1ll1ll_opy_()
        try:
            global l1111l1_opy_
            userinfo = l1l111ll_opy_[l11l111l_opy_(l1lll1_opy_ (u"ࠥࡨ࡝ࡔ࡬ࡤ࡮࠼ࡴࡧࡳ࡚ࡷࠤࡨ"))]
            status = userinfo[l11l111l_opy_(l1lll1_opy_ (u"ࠦ࡞࡞ࡖ࠱ࡣࡄࡁࡂࠨࡩ"))]
            l1111l1_opy_ = userinfo[l11l111l_opy_(l1lll1_opy_ (u"ࠧࡠࡘࡩࡹ࡛࠶ࡗ࡮ࡤࡈࡗࡀࠦࡪ"))]
            return status
        except:
            return 0
def Account(params):
    tools.log(l1ll1l_opy_+l11l111l_opy_(l1lll1_opy_ (u"ࠨࡔ࡙࡭ࡪ࡝࡜ࡔࡪࡣ࠵࡙ࡹࡩࡉࡂࡏ࡜࡚࠹࠶ࡏࡁ࠾࠿ࠥ࡫"))+repr(params))
    l1llll11l_opy_ = l1ll1ll_opy_()
    l111ll1l_opy_ = l1llll11l_opy_[l11l111l_opy_(l1lll1_opy_ (u"ࠢࡥ࡚ࡑࡰࡨࡲ࠹ࡱࡤࡰ࡞ࡻࠨ࡬"))]
    status = l111ll1l_opy_[l11l111l_opy_(l1lll1_opy_ (u"ࠣࡥ࠶ࡖ࡭ࡪࡈࡗࡼࠥ࡭"))]
    if status == l11l111l_opy_(l1lll1_opy_ (u"ࠤࡔ࡛ࡓ࠶ࡡ࡙࡜࡯ࠦ࡮")):
        status = l1lll1_opy_ (u"ࠥ࡟ࡈࡕࡌࡐࡔࠣࡁࠥࡲࡩ࡮ࡧࡠࠦ࡯")+status+l1lll1_opy_ (u"ࠦࡠ࠵ࡃࡐࡎࡒࡖࡢࠨࡰ")
    else:
        status = l1lll1_opy_ (u"ࠧࡡࡃࡐࡎࡒࡖࠥࡃࠠࡳࡧࡧࡡࠧࡱ")+status+l1lll1_opy_ (u"ࠨ࡛࠰ࡅࡒࡐࡔࡘ࡝ࠣࡲ")
    expires = l111ll1l_opy_[l11l111l_opy_(l1lll1_opy_ (u"࡛࡚ࠢ࡫ࡻ࡝࠸ࡒࡩࡦࡊ࡙ࡂࠨࡳ"))]
    if expires:
       expires = datetime.datetime.fromtimestamp(int(expires)).strftime(l1lll1_opy_ (u"ࠨࠧࡧ࠳ࠪࡳ࠯࡛ࠦࠣࠩࡍࡀࠥࡎࠩࡴ"))
       expires = l1lll1_opy_ (u"ࠤ࡞ࡇࡔࡒࡏࡓࠢࡀࠤࡷ࡫ࡤ࡞ࠤࡵ")+expires+l1lll1_opy_ (u"ࠥ࡟࠴ࡉࡏࡍࡑࡕࡡࠧࡶ")
    else:
       expires = l11l111l_opy_(l1lll1_opy_ (u"࡙ࠦࡳࡖ࠳࡜࡛ࡍࡂࠨࡷ"))
    l1l1ll11_opy_ = l111ll1l_opy_[l11l111l_opy_(l1lll1_opy_ (u"ࠧࡨࡗࡇ࠶࡛࠶ࡓࡼࡢ࡮࠷࡯࡝࠸ࡘࡰࡣ࠴࠸ࡾࠧࡸ"))]
    if l1l1ll11_opy_ == l1lll1_opy_ (u"ࠨ࠰ࠣࡹ"):
        l1l1ll11_opy_ = l11l111l_opy_(l1lll1_opy_ (u"ࠢࡗ࡙࠸ࡷࡦ࡝࠱ࡱࡦࡊ࡚ࡰࠨࡺ"))
    username = l111ll1l_opy_[l11l111l_opy_(l1lll1_opy_ (u"ࠣࡦ࡛ࡒࡱࡩ࡭࠶ࡪࡥ࡛࡚ࡃࠢࡻ"))]
    window = pyxbmct.AddonDialogWindow(l1lll1_opy_ (u"ࠩࡐࡽࠥࡇࡣࡤࡱࡸࡲࡹࠦࡉ࡯ࡨࡲࡶࡲࡧࡴࡪࡱࡱ࠲ࠬࡼ"))
    window.setGeometry(400, 220, 5, 1)
    l1lll11ll_opy_ = pyxbmct.Label(l1lll1_opy_ (u"ࠪ࡟ࡈࡕࡌࡐࡔࠣࡁࠥ࡭࡯࡭ࡦࡠ࡙ࡸ࡫ࡲ࠻ࠢ࡞࠳ࡈࡕࡌࡐࡔࡠࠫࡽ")+username, alignment=pyxbmct.ALIGN_LEFT )
    l111l1l_opy_ = pyxbmct.Label(l1lll1_opy_ (u"ࠫࡠࡉࡏࡍࡑࡕࠤࡂࠦࡧࡰ࡮ࡧࡡࡘࡺࡡࡵࡷࡶ࠾ࠥࡡ࠯ࡄࡑࡏࡓࡗࡣࠧࡾ")+status, alignment=pyxbmct.ALIGN_LEFT )
    l1l111l_opy_ = pyxbmct.Label(l1lll1_opy_ (u"ࠬࡡࡃࡐࡎࡒࡖࠥࡃࠠࡨࡱ࡯ࡨࡢࡋࡸࡱ࡫ࡵࡩࡸࡀࠠ࡜࠱ࡆࡓࡑࡕࡒ࡞ࠩࡿ")+expires, alignment=pyxbmct.ALIGN_LEFT )
    l111l1_opy_ = pyxbmct.Label(l1lll1_opy_ (u"࡛࠭ࡄࡑࡏࡓࡗࠦ࠽ࠡࡩࡲࡰࡩࡣࡍࡢࡺࠣࡧࡴࡴ࡮ࡦࡥࡷ࡭ࡴࡴࡳ࠻ࠢ࡞࠳ࡈࡕࡌࡐࡔࡠࠫࢀ")+l1l1ll11_opy_, alignment=pyxbmct.ALIGN_LEFT )
    window.placeControl(l1lll11ll_opy_, 0, 0)
    window.placeControl(l111l1l_opy_, 1, 0)
    window.placeControl(l1l111l_opy_, 2, 0)
    window.placeControl(l111l1_opy_, 3, 0)
    l1lllll_opy_ = pyxbmct.Button(l1lll1_opy_ (u"ࠧࡄ࡮ࡲࡷࡪ࠭ࢁ"))
    window.placeControl(l1lllll_opy_, 4, 0)
    window.setFocus(l1lllll_opy_)
    window.connect(l1lllll_opy_, window.close)
    window.connect(pyxbmct.ACTION_NAV_BACK, window.close)
    window.doModal()
    del window
def Mayfair(params):
  request = urllib2.Request(l11l1l11_opy_, headers={l1lll1_opy_ (u"ࠣࡃࡦࡧࡪࡶࡴࠣࢂ") : l1lll1_opy_ (u"ࠤࡤࡴࡵࡲࡩࡤࡣࡷ࡭ࡴࡴ࠯ࡹ࡯࡯ࠦࢃ")})
  u = urllib2.urlopen(request)
  l111lll_opy_ = ElementTree.parse(u)
  l11l11ll_opy_ = l111lll_opy_.getroot()
  l111l1ll_opy_ = l11l11_opy_(l1lll1_opy_ (u"ࠪࡧࡦࡺࡥࡨࡱࡵࡽ࡮ࡳࡡࡨࡧࠪࢄ"))
  l1ll11l1_opy_ = l11l11_opy_(l1lll1_opy_ (u"ࠫࡨࡧࡴࡦࡩࡲࡶࡾࡨࡧࠨࢅ"))
  if l111l1ll_opy_ == l1lll1_opy_ (u"ࠬࡌࡡ࡭ࡵࡨࠫࢆ"):
    l111l1ll_opy_ = os.path.join(l1lll1l1l_opy_,l11l111l_opy_(l1lll1_opy_ (u"ࠨࡢࡈ࠻ࡱࡦࡾ࠻ࡷࡣ࡯ࡦࡁࠧࢇ")))
  if l1ll11l1_opy_ == l1lll1_opy_ (u"ࠧࡇࡣ࡯ࡷࡪ࠭࢈"):
    l1ll11l1_opy_ = os.path.join(l1lll1l1l_opy_,l11l111l_opy_(l1lll1_opy_ (u"ࠣ࡜ࡰࡊࡺ࡟ࡘࡋ࠲ࡏࡲࡇࡻ࡚ࡸ࠿ࡀࠦࢉ")))
  for l1111lll_opy_ in l111lll_opy_.findall(l11l111l_opy_(l1lll1_opy_ (u"ࠤ࡜࠶࡭࡮ࡢ࡮࠷࡯ࡦࡆࡃ࠽ࠣࢊ"))):
      title = l1111lll_opy_.find(l11l111l_opy_(l1lll1_opy_ (u"ࠥࡨࡌࡲ࠰ࡣࡉࡘࡁࠧࢋ"))).text
      title = base64.b64decode(title)
      a = l1lll1_opy_ (u"ࠫ࡝࡞ࡘࠨࢌ"), l1lll1_opy_ (u"ࠬࡇࡤࡶ࡮ࡷࠫࢍ"), l1lll1_opy_ (u"࠭ࡁࡥࡷ࡯ࡸࡸ࠭ࢎ"),l1lll1_opy_ (u"ࠧࡂࡆࡘࡐ࡙࠭࢏"),l1lll1_opy_ (u"ࠨࡃࡇ࡙ࡑ࡚ࡓࠨ࢐"),l1lll1_opy_ (u"ࠩࡤࡨࡺࡲࡴࠨ࢑"),l1lll1_opy_ (u"ࠪࡥࡩࡻ࡬ࡵࡵࠪ࢒"),l1lll1_opy_ (u"ࠫࡕࡵࡲ࡯ࠩ࢓"),l1lll1_opy_ (u"ࠬࡖࡏࡓࡐࠪ࢔"),l1lll1_opy_ (u"࠭ࡰࡰࡴࡱࠫ࢕"),l1lll1_opy_ (u"ࠧࡑࡱࡵࡲࠬ࢖"),l1lll1_opy_ (u"ࠨࡺࡻࡼࠬࢗ"), l1lll1_opy_ (u"ࠩ࠴࠼࠰࠭࢘")
      if l1l1l1l1_opy_ == l1lll1_opy_ (u"ࠥࡪࡦࡲࡳࡦࠤ࢙"):
        if any(s in title for s in a):
          return
      l11l1l1l_opy_ = l1111lll_opy_.find(l11l111l_opy_(l1lll1_opy_ (u"ࠦࡨࡍࡸࡩࡧ࡚ࡼࡵࡩ࠳ࡓࡨࡧ࡜ࡏࡹ࢚ࠢ"))).text
      tools.add_item( action=l1lll1_opy_ (u"ࠬࡳࡡࡺࡨࡤ࡭ࡷ࡭ࡥࡵࡥ࡫ࡲࡸ࢛࠭"), title=title , url=l11l1l1l_opy_ , thumbnail=l111l1ll_opy_ , fanart=l1ll11l1_opy_ , folder=False )
def l11l1_opy_():
  categories = list()
  url = l1lll1_opy_ (u"࠭ࠥࡴ࠼ࠨࡷ࠴࡫࡮ࡪࡩࡰࡥ࠷࠴ࡰࡩࡲࡂࡹࡸ࡫ࡲ࡯ࡣࡰࡩࡂࠫࡳࠧࡲࡤࡷࡸࡽ࡯ࡳࡦࡀࠩࡸࠬࡴࡺࡲࡨࡁࡒࡧࡹࡧࡣ࡬ࡶࡱࡵ࡬ࡰ࡮ࡢࡧࡦࡺࡥࡨࡱࡵ࡭ࡪࡹࠧ࢜")%(host,port,username,password)
  r = requests.get(url)
  match = re.compile(l1lll1_opy_ (u"ࠧ࠽ࡶ࡬ࡸࡱ࡫࠾ࠩ࠰࠮ࡃ࠮ࡂ࠯ࡵ࡫ࡷࡰࡪࡄ࠮ࠬࡁ࠿ࠥࡡࡡࡃࡅࡃࡗࡅࡡࡡࠨ࠯࠭ࡂ࠭ࡢࡣ࠾ࠨ࢝")).findall(r.content)
  for l11ll11_opy_,l1l11l1l_opy_ in match:
    l11ll11_opy_ = base64.b64decode(l11ll11_opy_)
    l1l1l_opy_ = os.path.join(l11l1l_opy_, l1lll1_opy_ (u"ࠨࡣࡵࡸࠬ࢞"), l1lll1_opy_ (u"ࠩ࡬ࡧࡴࡴ࠮ࡱࡰࡪࠫ࢟"))
    cat = l1llll11_opy_(l11ll11_opy_, l1l11l1l_opy_, l1l1l_opy_)
    categories.append(cat)
  return categories
def mayfairgetchns(params):
    if sys.argv[0] != l1lll1_opy_ (u"ࠪࡴࡱࡻࡧࡪࡰ࠽࠳࠴ࡶ࡬ࡶࡩ࡬ࡲ࠳ࡼࡩࡥࡧࡲ࠲ࡷ࡫ࡢࡰࡱࡷ࠳ࠬࢠ"):
        l111111_opy_ = xbmcgui.Dialog()
        l111111_opy_.ok(l1lll1_opy_ (u"ࠫࡠࡉࡏࡍࡑࡕࠤࡷ࡫ࡤ࡞ࡉࡈࡅࡗ࡙࡛࠰ࡅࡒࡐࡔࡘ࡝࡜ࡅࡒࡐࡔࡘࠠࡸࡪ࡬ࡸࡪࡣࠠࡕࡘ࡞࠳ࡈࡕࡌࡐࡔࡠࠫࢡ"),l1lll1_opy_ (u"ࠬࡋࡲࡳࡱࡵࠥࠥ࡟࡯ࡶࠢ࡫ࡥࡻ࡫ࠠࡣࡧࡨࡲࠥࡪࡥࡵࡧࡦࡸࡪࡪࠠࡵࡴࡼ࡭ࡳ࡭ࠠࡵࡱࠣࡷࡹ࡫ࡡ࡭ࠢࡲࡹࡷࠦࡡࡥࡦࡲࡲ࠳࠭ࢢ"),l1lll1_opy_ (u"࠭ࡎࡪࡥࡨࠤࡹࡸࡹ࠯࠰࠱ࠫࢣ"),l1lll1_opy_ (u"ࠧࡏࡱࡺࠤ࡬ࡵࠠࡧࡷࡦ࡯ࠥࡿ࡯ࡶࡴࡶࡩࡱ࡬࠮ࠨࢤ"))
        sys.exit()
    l1llll1l_opy_ = False
    tools.log(l1ll1l_opy_+l11l111l_opy_(l1lll1_opy_ (u"ࠣࡖࡊࡰ࠷ࡠࡓࡃࡆࡤࡋࡋࡻࡢ࡮ࡘࡶࡧࡾࡈࡎ࡛࡙࠸࠵ࡎࡇ࠽࠾ࠤࢥ"))+repr(params))
    url = params.get(l11l111l_opy_(l1lll1_opy_ (u"ࠤࡧ࡜ࡏࡹࠢࢦ")))
    request = urllib2.Request(url, headers={l1lll1_opy_ (u"ࠥࡅࡨࡩࡥࡱࡶࠥࢧ") : l1lll1_opy_ (u"ࠦࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱ࡻࡱࡱࠨࢨ")})
    u = urllib2.urlopen(request)
    l111lll_opy_ = ElementTree.parse(u)
    l11l11ll_opy_ = l111lll_opy_.getroot()
    l111ll_opy_ = list()
    l1lll1lll_opy_ = 0
    for l1111lll_opy_ in l111lll_opy_.findall(l11l111l_opy_(l1lll1_opy_ (u"ࠧ࡟࠲ࡩࡪࡥࡱ࠺ࡲࡢࡂ࠿ࡀࠦࢩ"))):
        title = l1111lll_opy_.find(l11l111l_opy_(l1lll1_opy_ (u"ࠨࡤࡈ࡮࠳ࡦࡌ࡛࠽ࠣࢪ"))).text
        title = base64.b64decode(title)
        title = title.partition(l1lll1_opy_ (u"ࠢ࡜ࠤࢫ"))
        l1111l11_opy_ = l1111lll_opy_.find(l11l111l_opy_(l1lll1_opy_ (u"ࠣࡥ࠶ࡖࡾࡠࡗࡇࡶ࡛࠷࡛ࡿࡢࡂ࠿ࡀࠦࢬ"))).text
        l1llllll_opy_ = l1111lll_opy_.find(l11l111l_opy_(l1lll1_opy_ (u"ࠤ࡝ࡋ࡛ࢀ࡙࠲࠻ࡳࡦ࡜ࡌ࡮࡛ࡓࡀࡁࠧࢭ"))).text
        l11l1l1_opy_ = title[1]+title[2]
        l11l1l1_opy_ = l11l1l1_opy_.partition(l1lll1_opy_ (u"ࠥࡡࠧࢮ"))
        l11l1l1_opy_ = l11l1l1_opy_[2]
        l11l1l1_opy_ = l11l1l1_opy_.partition(l1lll1_opy_ (u"ࠦࠥࠦࠠࠣࢯ"))
        l11l1l1_opy_ = l11l1l1_opy_[2]
        l1_opy_ = l11l111l_opy_(l1lll1_opy_ (u"ࠧࡐࡘࡎ࠿ࠥࢰ"))%(title[0]+title[1]+title[2])
        l1_opy_ = l1_opy_.partition(l1lll1_opy_ (u"ࠨ࡛࠰ࡅࡒࡐࡔࡘ࡝ࠣࢱ"))
        l1l1l1ll_opy_ = l1_opy_[2].partition(l1lll1_opy_ (u"ࠢࠡ࠭ࠣࠦࢲ"))
        l1l1l1ll_opy_ = l1l1l1ll_opy_[2].partition(l1lll1_opy_ (u"ࠣࠢࠣࠤࠧࢳ"))
        l1l1l1ll_opy_ = l1l1l1ll_opy_[0]
        l1_opy_ = l1_opy_[0]+l1_opy_[1]
        desc = l1111lll_opy_.find(l11l111l_opy_(l1lll1_opy_ (u"ࠤ࡝ࡋ࡛ࢀ࡙࠴ࡌࡳࡧࡍࡘࡰࡣ࠴࠷ࡁࠧࢴ"))).text
        if desc:
           desc = base64.b64decode(desc)
           l11l11l1_opy_ = desc.partition(l1lll1_opy_ (u"ࠥࠬࠧࢵ"))
           l1lllll1_opy_ = l11l11l1_opy_[0]
           l11l11l1_opy_ = l11l11l1_opy_[2].partition(l1lll1_opy_ (u"ࠦ࠮ࡢ࡮ࠣࢶ"))
           l11llll_opy_ = desc.partition(l1lll1_opy_ (u"ࠧ࠯࡜࡯ࠤࢷ"))
           l11llll_opy_ = l11llll_opy_[2].partition(l1lll1_opy_ (u"ࠨࠨࠣࢸ"))
           l111l_opy_ = l11llll_opy_[0]
           l1l1l11_opy_ = l11l11l1_opy_[0]
        else:
           l1l1l11_opy_ = l1lll1_opy_ (u"ࠢࠣࢹ")
        a = l1lll1_opy_ (u"ࠨ࡚࡛࡜ࠬࢺ"), l1lll1_opy_ (u"ࠩࡄࡨࡺࡲࡴࠨࢻ"), l1lll1_opy_ (u"ࠪࡅࡩࡻ࡬ࡵࡵࠪࢼ"),l1lll1_opy_ (u"ࠫࡆࡊࡕࡍࡖࠪࢽ"),l1lll1_opy_ (u"ࠬࡇࡄࡖࡎࡗࡗࠬࢾ"),l1lll1_opy_ (u"࠭ࡡࡥࡷ࡯ࡸࠬࢿ"),l1lll1_opy_ (u"ࠧࡢࡦࡸࡰࡹࡹࠧࣀ"),l1lll1_opy_ (u"ࠨࡒࡲࡶࡳ࠭ࣁ"),l1lll1_opy_ (u"ࠩࡓࡓࡗࡔࠧࣂ"),l1lll1_opy_ (u"ࠪࡴࡴࡸ࡮ࠨࣃ"),l1lll1_opy_ (u"ࠫࡕࡵࡲ࡯ࠩࣄ"),l1lll1_opy_ (u"ࠬࡾࡸࡹࠩࣅ"), l1lll1_opy_ (u"࠭࠱࠹࠭ࠪࣆ")
        if l111ll1_opy_ == l1lll1_opy_ (u"ࠢࡵࡴࡸࡩࠧࣇ"):
          if l1llll1l_opy_ != True:
            if any(s in l1_opy_ for s in a):
                xbmc.executebuiltin((l1lll1_opy_ (u"ࡶ࡛ࠩࡆࡒࡉ࠮ࡏࡱࡷ࡭࡫࡯ࡣࡢࡶ࡬ࡳࡳ࠮ࠢࡑࡣࡵࡩࡳࡺࡡ࡭࠯ࡏࡳࡨࡱࠠࡆࡰࡤࡦࡱ࡫ࡤࠢࠤ࠯ࠤࠧࡉࡨࡢࡰࡱࡩࡱࡹࠠ࡮ࡣࡼࠤࡨࡵ࡮ࡵࡣ࡬ࡲࠥࡧࡤࡶ࡮ࡷࠤࡨࡵ࡮ࡵࡧࡱࡸࠧ࠲ࠠ࠳࠲࠳࠴࠮࠭ࣈ")))
                l111111_opy_ = xbmcgui.Dialog()
                text = l111111_opy_.input(l11l111l_opy_(l1lll1_opy_ (u"ࠩࡘࡋࡋࡿ࡚ࡘ࠷࠳࡝࡜ࡽࡴࡕࡉ࠼࡮ࡦࢀ࡯ࡨࡗࡊࡼࡱ࡟ࡘࡏ࡮ࡌࡋ࡛ࡻࡤࡈࡘࡼࡍࡍࡲࡶࡥ࡚ࡌ࡫࡚ࡍࡆࡺ࡜࡚࠹࠵࡟ࡗࡸࡩࡔ࠶࠾ࡱ࡚ࡒ࠿ࡀࠫࣉ")), type=xbmcgui.INPUT_NUMERIC, option=xbmcgui.ALPHANUM_HIDE_INPUT)
                if text!=tools.get_setting(l11l111l_opy_(l1lll1_opy_ (u"ࠥࡧࡌ࡜ࡹࡣࡰࡕ࡬ࡧࡍࡎࡷ࡜ࡊ࡙ࡂࠨ࣊"))):
                    xbmc.executebuiltin((l1lll1_opy_ (u"ࡹࠬ࡞ࡂࡎࡅ࠱ࡒࡴࡺࡩࡧ࡫ࡦࡥࡹ࡯࡯࡯ࠪࠥࡔࡦࡸࡥ࡯ࡶࡤࡰ࠲ࡒ࡯ࡤ࡭ࠣࡉࡷࡸ࡯ࡳࠣࠥ࠰ࠥࠨࡉ࡯ࡥࡲࡶࡷ࡫ࡣࡵࠢࡦࡳࡩ࡫ࠡࠣ࠮ࠣ࠷࠵࠶࠰ࠪࠩ࣋")))
                    return
                else:
                    l1llll1l_opy_ = True
        if not l1llllll_opy_:
            l1llllll_opy_ = os.path.join(l1lll1l1l_opy_,l11l111l_opy_(l1lll1_opy_ (u"ࠧࡨࡇ࠺ࡰࡥࡽ࠺ࡽࡢ࡮ࡥࡀࠦ࣌")))
        l1lll1lll_opy_ = l1lll1lll_opy_ + 1
        l1111lll_opy_ = Channel(l1lll1lll_opy_, l1_opy_, l1llllll_opy_, l1111l11_opy_, l11l1l1_opy_, l1l1l11_opy_, l1l1l1ll_opy_)
        l111ll_opy_.append(l1111lll_opy_)
    l1ll11l_opy_(l111ll_opy_)
def l1ll11l_opy_(l111ll_opy_):
        if sys.argv[0] != l1lll1_opy_ (u"࠭ࡰ࡭ࡷࡪ࡭ࡳࡀ࠯࠰ࡲ࡯ࡹ࡬࡯࡮࠯ࡸ࡬ࡨࡪࡵ࠮ࡳࡧࡥࡳࡴࡺ࠯ࠨ࣍"):
            l111111_opy_ = xbmcgui.Dialog()
            l111111_opy_.ok(l1lll1_opy_ (u"ࠧ࡜ࡅࡒࡐࡔࡘࠠࡳࡧࡧࡡࡌࡋࡁࡓࡕ࡞࠳ࡈࡕࡌࡐࡔࡠ࡟ࡈࡕࡌࡐࡔࠣࡻ࡭࡯ࡴࡦ࡟ࠣࡘ࡛ࡡ࠯ࡄࡑࡏࡓࡗࡣࠧ࣎"),l1lll1_opy_ (u"ࠨࡇࡵࡶࡴࡸ࡛ࠡࠡࡲࡹࠥ࡮ࡡࡷࡧࠣࡦࡪ࡫࡮ࠡࡦࡨࡸࡪࡩࡴࡦࡦࠣࡸࡷࡿࡩ࡯ࡩࠣࡸࡴࠦࡳࡵࡧࡤࡰࠥࡵࡵࡳࠢࡤࡨࡩࡵ࡮࠯࣏ࠩ"),l1lll1_opy_ (u"ࠩࡑ࡭ࡨ࡫ࠠࡵࡴࡼ࠲࠳࠴࣐ࠧ"),l1lll1_opy_ (u"ࠪࡒࡴࡽࠠࡨࡱࠣࡪࡺࡩ࡫ࠡࡻࡲࡹࡷࡹࡥ࡭ࡨ࠱࣑ࠫ"))
            sys.exit()
        if not l111ll_opy_:
            l111111_opy_ = xbmcgui.Dialog()
            l111111_opy_.ok(l1lll1_opy_ (u"ࠫࡠࡉࡏࡍࡑࡕࠤࡷ࡫ࡤ࡞ࡉࡈࡅࡗ࡙࡛࠰ࡅࡒࡐࡔࡘ࡝࡜ࡅࡒࡐࡔࡘࠠࡸࡪ࡬ࡸࡪࡣࠠࡕࡘ࡞࠳ࡈࡕࡌࡐࡔࡠ࣒ࠫ"),l1lll1_opy_ (u"ࠬࡡࡃࡐࡎࡒࡖࠥࡸࡥࡥ࡟࡞ࡆࡢࡔ࡯ࠡࡧࡹࡩࡳࡺࡳࠡࡵࡦ࡬ࡪࡪࡵ࡭ࡧࡧ࠲ࡠ࠵ࡂ࡞࡝࠲ࡇࡔࡒࡏࡓ࡟࣓ࠪ"),l1lll1_opy_ (u"࠭ࠧࣔ"),l1lll1_opy_ (u"ࠧࡑ࡮ࡨࡥࡸ࡫ࠠࡤࡪࡨࡧࡰࠦࡢࡢࡥ࡮ࠤࡱࡧࡴࡦࡴࠤࠫࣕ"))
            return
        title = l1lll1_opy_ (u"ࠣࠤࣖ")
        d = l1ll1ll1_opy_(title,l111ll_opy_)
        d.doModal()
def mPRO(params):
    try:
        l1l11_opy_ = False
        if l1111ll_opy_(l1lll1_opy_ (u"ࠩࡳࡰࡺ࡭ࡩ࡯࠰ࡳࡶࡴ࡭ࡲࡢ࡯࠱ࡱࡹࡼࡧࡶ࡫ࡧࡩࡵࡸ࡯ࠨࣗ")):
            l11lll11_opy_ = xbmcaddon.Addon(l1lll1_opy_ (u"ࠪࡴࡱࡻࡧࡪࡰ࠱ࡴࡷࡵࡧࡳࡣࡰ࠲ࡲࡺࡶࡨࡷ࡬ࡨࡪࡶࡲࡰࠩࣘ"))
            if (l11lll11_opy_.getSetting(l1lll1_opy_ (u"ࠫࡷ࡫ࡢࡰࡱࡷ࠲ࡪࡴࡡࡣ࡮ࡨࡨࠬࣙ")) != l1lll1_opy_ (u"ࠬࡺࡲࡶࡧࠪࣚ") or l11lll11_opy_.getSetting(l1lll1_opy_ (u"࠭ࡲࡦࡤࡲࡳࡹ࠴ࡵࡴࡧࡵࠫࣛ")) != username or l11lll11_opy_.getSetting(l1lll1_opy_ (u"ࠧࡳࡧࡥࡳࡴࡺ࠮ࡱࡣࡶࡷࠬࣜ")) != password):
                l11lll11_opy_.setSetting(l1lll1_opy_ (u"ࠨࡴࡨࡦࡴࡵࡴ࠯ࡧࡱࡥࡧࡲࡥࡥࠩࣝ"), l1lll1_opy_ (u"ࠩࡷࡶࡺ࡫ࠧࣞ"))
                l11lll11_opy_.setSetting(l1lll1_opy_ (u"ࠪࡶࡪࡨ࡯ࡰࡶ࠱ࡹࡸ࡫ࡲࠨࣟ"), username)
                l11lll11_opy_.setSetting(l1lll1_opy_ (u"ࠫࡷ࡫ࡢࡰࡱࡷ࠲ࡵࡧࡳࡴࠩ࣠"), password)
        else:
            xbmc.executebuiltin(l1lll1_opy_ (u"ࠧ࡞ࡂࡎࡅ࠱ࡖࡺࡴࡐ࡭ࡷࡪ࡭ࡳ࠮ࡰ࡭ࡷࡪ࡭ࡳࡀ࠯࠰ࡲ࡯ࡹ࡬࡯࡮࠯ࡲࡵࡳ࡬ࡸࡡ࡮࠰ࡰࡸࡻ࡭ࡵࡪࡦࡨࡴࡷࡵ࠯ࠪࠤ࣡"))
            l1l11_opy_ = True
        if l1l11_opy_ == False:
            xbmc.executebuiltin(l1lll1_opy_ (u"ࠨࡒࡶࡰࡄࡨࡩࡵ࡮ࠩࡲ࡯ࡹ࡬࡯࡮࠯ࡲࡵࡳ࡬ࡸࡡ࡮࠰ࡰࡸࡻ࡭ࡵࡪࡦࡨࡴࡷࡵࠩࠣ࣢"))
        if not os.path.exists(l1lll111l_opy_):
            l111111_opy_ = xbmcgui.Dialog()
            l111111_opy_.ok(l1lll1_opy_ (u"ࠢ࡜ࡅࡒࡐࡔࡘࠠࡳࡧࡧࡡࡌࡋࡁࡓࡕ࡞࠳ࡈࡕࡌࡐࡔࡠ࡟ࡈࡕࡌࡐࡔࠣࡻ࡭࡯ࡴࡦ࡟ࠣࡘ࡛ࡡ࠯ࡄࡑࡏࡓࡗࡣࣣࠢ"), l1lll1_opy_ (u"ࠣ࡝ࡅࡡࡠࡉࡏࡍࡑࡕࠤࡷ࡫ࡤ࡞࡛ࡲࡹࠥࡊࡏࠡࡐࡒࡘࠥ࡮ࡡࡷࡧࠣ࡟ࡈࡕࡌࡐࡔࠣࡽࡪࡲ࡬ࡰࡹࡠࡑࡠ࠵ࡃࡐࡎࡒࡖࡢࡡࡃࡐࡎࡒࡖࠥ࡭ࡨࡰࡵࡷࡻ࡭࡯ࡴࡦ࡟࠰࡟࠴ࡉࡏࡍࡑࡕࡡࡠࡉࡏࡍࡑࡕࠤࡾ࡫࡬࡭ࡱࡺࡡ࡙࡜ࠠࡈࡷ࡬ࡨࡪࡡ࠯ࡄࡑࡏࡓࡗࡣࠧࡴࠢࡕࡩࡵࡵࡳࡪࡶࡲࡶࡾࠦࡩ࡯ࡵࡷࡥࡱࡲࡥࡥࠣ࡞࠳ࡈࡕࡌࡐࡔࡠ࡟࠴ࡈ࡝ࠣࣤ"),l1lll1_opy_ (u"ࠤ࡞ࡇࡔࡒࡏࡓࠢࡩࡪ࠹࠼࠸࠳ࡤ࠷ࡡࡒࡡ࠯ࡄࡑࡏࡓࡗࡣ࡛ࡄࡑࡏࡓࡗࠦࡦࡧࡅ࠳ࡇ࠵ࡉ࠰࡞ࡣࡼࡪࡦ࡯ࡲࠡ࡝࠲ࡇࡔࡒࡏࡓ࡟࡞ࡇࡔࡒࡏࡓࠢࡩࡪ࠹࠼࠸࠳ࡤ࠷ࡡࡌࡡ࠯ࡄࡑࡏࡓࡗࡣ࡛ࡄࡑࡏࡓࡗࠦࡦࡧࡅ࠳ࡇ࠵ࡉ࠰࡞ࡷ࡬ࡨࡪࡡ࠯ࡄࡑࡏࡓࡗࡣ࡛ࡄࡑࡏࡓࡗࠦࡧࡰ࡮ࡧࡡࠥࡖࡒࡐ࡝࠲ࡇࡔࡒࡏࡓ࡟ࠣࡥࡩࡪ࡯࡯ࠢࡵࡩࡶࡻࡩࡳࡧࡧࠤ࡫ࡵࡲࠡࡶ࡫࡭ࡸࠦࡦࡦࡣࡷࡹࡷ࡫ࠡࠣࣥ"),l1lll1_opy_ (u"ࠥࡋࡪࡺࠠࡪࡶࠣࡥࡹࡀࠠ࡜ࡅࡒࡐࡔࡘࠠࡰࡴࡤࡲ࡬࡫ࡲࡦࡦࡠ࡬ࡹࡺࡰ࠻࠱࠲ࡱࡦࡿࡦࡢ࡫ࡵ࡫ࡺ࡯ࡤࡦࡵ࠱ࡲࡪࡺ࠯ࡳࡧࡳࡳ࠴ࡡ࠯ࡄࡑࡏࡓࡗࡣ࡜࡯ࡣࡱࡨࠥ࡯࡮ࡴࡶࡤࡰࡱࠦࡲࡦࡲࡲࡷ࡮ࡺ࡯ࡳࡻ࠱ࡑ࠲࡚ࡖࡈࡷ࡬ࡨࡪ࠳࠱࠯࠶࠱ࡾ࡮ࡶࠠࡢࡰࡧࠤࡹࡸࡹࠡࡣࡪࡥ࡮ࡴࣦࠡࠣ"))
    except:
        pass
def mFREE(params):
    try:
        l1lll1l_opy_ = False
        if l1111ll_opy_(l1lll1_opy_ (u"ࠫࡵࡲࡵࡨ࡫ࡱ࠲ࡵࡸ࡯ࡨࡴࡤࡱ࠳ࡳࡴࡷࡩࡸ࡭ࡩ࡫ࠧࣧ")):
            l11l1ll1_opy_ = xbmcaddon.Addon(l1lll1_opy_ (u"ࠬࡶ࡬ࡶࡩ࡬ࡲ࠳ࡶࡲࡰࡩࡵࡥࡲ࠴࡭ࡵࡸࡪࡹ࡮ࡪࡥࠨࣨ"))
            if (l11l1ll1_opy_.getSetting(l1lll1_opy_ (u"࠭ࡲࡦࡤࡲࡳࡹ࠴ࡥ࡯ࡣࡥࡰࡪࡪࣩࠧ")) != l1lll1_opy_ (u"ࠧࡵࡴࡸࡩࠬ࣪") or l11l1ll1_opy_.getSetting(l1lll1_opy_ (u"ࠨࡴࡨࡦࡴࡵࡴ࠯ࡷࡶࡩࡷ࠭࣫")) != username or l11l1ll1_opy_.getSetting(l1lll1_opy_ (u"ࠩࡵࡩࡧࡵ࡯ࡵ࠰ࡳࡥࡸࡹࠧ࣬")) != password):
                l11l1ll1_opy_.setSetting(l1lll1_opy_ (u"ࠪࡶࡪࡨ࡯ࡰࡶ࠱ࡩࡳࡧࡢ࡭ࡧࡧ࣭ࠫ"), l1lll1_opy_ (u"ࠫࡹࡸࡵࡦ࣮ࠩ"))
                l11l1ll1_opy_.setSetting(l1lll1_opy_ (u"ࠬࡸࡥࡣࡱࡲࡸ࠳ࡻࡳࡦࡴ࣯ࠪ"), username)
                l11l1ll1_opy_.setSetting(l1lll1_opy_ (u"࠭ࡲࡦࡤࡲࡳࡹ࠴ࡰࡢࡵࡶࣰࠫ"), password)
        else:
            xbmc.executebuiltin(l1lll1_opy_ (u"࡙ࠢࡄࡐࡇ࠳ࡘࡵ࡯ࡒ࡯ࡹ࡬࡯࡮ࠩࡲ࡯ࡹ࡬࡯࡮࠻࠱࠲ࡴࡱࡻࡧࡪࡰ࠱ࡴࡷࡵࡧࡳࡣࡰ࠲ࡲࡺࡶࡨࡷ࡬ࡨࡪ࠵ࣱࠩࠣ"))
            l1lll1l_opy_ = True
        if l1lll1l_opy_ == False:
            xbmc.executebuiltin(l1lll1_opy_ (u"ࠣࡔࡸࡲࡆࡪࡤࡰࡰࠫࡴࡱࡻࡧࡪࡰ࠱ࡴࡷࡵࡧࡳࡣࡰ࠲ࡲࡺࡶࡨࡷ࡬ࡨࡪ࠯ࣲࠢ"))
        if not os.path.exists(l1lll111l_opy_):
            l111111_opy_ = xbmcgui.Dialog()
            l111111_opy_.ok(l1lll1_opy_ (u"ࠤ࡞ࡇࡔࡒࡏࡓࠢࡵࡩࡩࡣࡇࡆࡃࡕࡗࡠ࠵ࡃࡐࡎࡒࡖࡢࡡࡃࡐࡎࡒࡖࠥࡽࡨࡪࡶࡨࡡ࡚ࠥࡖ࡜࠱ࡆࡓࡑࡕࡒ࡞ࠤࣳ"), l1lll1_opy_ (u"ࠥ࡟ࡇࡣ࡛ࡄࡑࡏࡓࡗࠦࡲࡦࡦࡠ࡝ࡴࡻࠠࡅࡑࠣࡒࡔ࡚ࠠࡩࡣࡹࡩࠥࡡࡃࡐࡎࡒࡖࠥࡿࡥ࡭࡮ࡲࡻࡢࡓ࡛࠰ࡅࡒࡐࡔࡘ࡝࡜ࡅࡒࡐࡔࡘࠠࡨࡪࡲࡷࡹࡽࡨࡪࡶࡨࡡ࠲ࡡ࠯ࡄࡑࡏࡓࡗࡣ࡛ࡄࡑࡏࡓࡗࠦࡹࡦ࡮࡯ࡳࡼࡣࡔࡗࠢࡊࡹ࡮ࡪࡥ࡜࠱ࡆࡓࡑࡕࡒ࡞ࠩࡶࠤࡗ࡫ࡰࡰࡵ࡬ࡸࡴࡸࡹࠡ࡫ࡱࡷࡹࡧ࡬࡭ࡧࡧࠥࡠ࠵ࡃࡐࡎࡒࡖࡢࡡ࠯ࡃ࡟ࠥࣴ"),l1lll1_opy_ (u"ࠦࡠࡉࡏࡍࡑࡕࠤ࡫࡬࠰࠱࠺࠷ࡪ࡫ࡣࡍ࡜࠱ࡆࡓࡑࡕࡒ࡞࡝ࡆࡓࡑࡕࡒࠡࡩ࡫ࡳࡸࡺࡷࡩ࡫ࡷࡩࡢ࠳࡛࠰ࡅࡒࡐࡔࡘ࡝࡜ࡅࡒࡐࡔࡘࠠࡺࡧ࡯ࡰࡴࡽ࡝ࡕࡘࠣࡋࡺ࡯ࡤࡦ࡝࠲ࡇࡔࡒࡏࡓ࡟ࠣࡥࡩࡪ࡯࡯ࠢࡵࡩࡶࡻࡩࡳࡧࡧࠤ࡫ࡵࡲࠡࡶ࡫࡭ࡸࠦࡦࡦࡣࡷࡹࡷ࡫ࠡࠣࣵ"),l1lll1_opy_ (u"ࠧࡍࡥࡵࠢ࡬ࡸࠥࡧࡴ࠻ࠢ࡞ࡇࡔࡒࡏࡓࠢࡲࡶࡦࡴࡧࡦࡴࡨࡨࡢ࡮ࡴࡵࡲ࠽࠳࠴ࡳࡡࡺࡨࡤ࡭ࡷ࡭ࡵࡪࡦࡨࡷ࠳ࡴࡥࡵ࠱ࡵࡩࡵࡵ࠯࡜࠱ࡆࡓࡑࡕࡒ࡞࡞ࡱࡥࡳࡪࠠࡪࡰࡶࡸࡦࡲ࡬ࠡࡴࡨࡴࡴࡹࡩࡵࡱࡵࡽ࠳ࡓ࠭ࡕࡘࡊࡹ࡮ࡪࡥ࠮࠳࠱࠸࠳ࢀࡩࡱࠢࡤࡲࡩࠦࡴࡳࡻࠣࡥ࡬ࡧࡩ࡯ࣶࠣࠥ"))
    except:
        pass
def CheckForUpdates(params):
    try:
        addon_id=tools.addon_id
        l1llllll1_opy_=ADDON.getAddonInfo(l1lll1_opy_ (u"࠭ࡶࡦࡴࡶ࡭ࡴࡴࠧࣷ"))
        url = l1lll1_opy_ (u"ࠧࡩࡶࡷࡴ࠿࠵࠯ࡵࡣࡵ࡫ࡪࡺࡣࡳࡧࡤࡸࡪࡹ࠮ࡤࡱࡰ࠳࡬࡯ࡴ࠰ࡼ࡬ࡴࡸ࠵ࡰ࡭ࡷࡪ࡭ࡳ࠴ࡶࡪࡦࡨࡳ࠳ࡸࡥࡣࡱࡲࡸ࠴ࡧࡤࡥࡱࡱ࠲ࡽࡳ࡬ࠨࣸ")
        request = urllib2.Request(url, headers={l1lll1_opy_ (u"ࠨࡗࡶࡩࡷ࠳ࡁࡨࡧࡱࡸࣹࠬ"): l1lll1_opy_ (u"ࠩࡐࡳࡿ࡯࡬࡭ࡣ࠲࠹࠳࠶ࣺࠧ"), l1lll1_opy_ (u"ࠥࡅࡨࡩࡥࡱࡶࠥࣻ") : l1lll1_opy_ (u"ࠦࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱ࡻࡱࡱࠨࣼ")})
        u = urllib2.urlopen(request)
        l111lll_opy_ = ElementTree.parse(u)
        l11l11ll_opy_ = l111lll_opy_.getroot()
        l1l11l11_opy_=l11l11ll_opy_.get(l1lll1_opy_ (u"ࠬࡼࡥࡳࡵ࡬ࡳࡳ࠭ࣽ"))
        if l1llllll1_opy_ != l1l11l11_opy_:
            l111111_opy_ = xbmcgui.Dialog()
            xbmc.executebuiltin(l1lll1_opy_ (u"࠭ࡕࡱࡦࡤࡸࡪࡒ࡯ࡤࡣ࡯ࡅࡩࡪ࡯࡯ࡵࠫ࠭ࠬࣾ"))
            xbmc.executebuiltin(l1lll1_opy_ (u"ࠧࡖࡲࡧࡥࡹ࡫ࡁࡥࡦࡲࡲࡗ࡫ࡰࡰࡵࠫ࠭ࠬࣿ"))
            l111111_opy_.ok(l1lll1_opy_ (u"ࠣ࡝ࡆࡓࡑࡕࡒࠡࡴࡨࡨࡢࡍࡅࡂࡔࡖ࡟࠴ࡉࡏࡍࡑࡕࡡࡠࡉࡏࡍࡑࡕࠤࡼ࡮ࡩࡵࡧࡠࠤ࡙࡜࡛࠰ࡅࡒࡐࡔࡘ࡝ࠣऀ"), l1lll1_opy_ (u"ࠤࡑࡩࡼࠦࡵࡱࡦࡤࡸࡪࠦࡦࡰࡷࡱࡨࠦࠨँ"),l1lll1_opy_ (u"࡛ࠥࡪࠦࡷࡪ࡮࡯ࠤࡳࡵࡷࠡࡤࡨ࡫࡮ࡴࠠࡶࡲࡧࡥࡹ࡯࡮ࡨ࠰࠱ࠦं"),l1lll1_opy_ (u"࡙ࠦ࡮ࡩࡴࠢࡰࡥࡾࠦࡴࡢ࡭ࡨࠤࡦࠦࡦࡦࡹࠣࡱ࡮ࡴࡵࡵࡧࡶ࠰ࠥࡪࡥࡱࡧࡱࡨ࡮ࡴࡧࠡࡱࡱࠤࡾࡵࡵࡳࠢࡧࡩࡻ࡯ࡣࡦࠣ࡟ࡲࡕࡲࡥࡢࡵࡨࠤࡷ࡫ࡳࡵࡣࡵࡸࠥࡡࡂ࡞࡝ࡆࡓࡑࡕࡒࠡࡴࡨࡨࡢࡍࡅࡂࡔࡖ࡟࠴ࡉࡏࡍࡑࡕࡡࡠࡉࡏࡍࡑࡕࠤࡼ࡮ࡩࡵࡧࡠࠤ࡙࡜࡛࠰ࡄࡠ࡟࠴ࡉࡏࡍࡑࡕࡡࠥࡵ࡮ࡤࡧࠣࡽࡴࡻࠠࡴࡧࡨࠤ࡮ࡺࠠࡩࡣࡶࠤࡧ࡫ࡥ࡯ࠢࡸࡴࡩࡧࡴࡦࡦࠤࠦः"))
            sys.exit()
        else:
            l111111_opy_ = xbmcgui.Dialog()
            l111111_opy_.ok(l1lll1_opy_ (u"ࠧࡡࡃࡐࡎࡒࡖࠥࡸࡥࡥ࡟ࡊࡉࡆࡘࡓ࡜࠱ࡆࡓࡑࡕࡒ࡞࡝ࡆࡓࡑࡕࡒࠡࡹ࡫࡭ࡹ࡫࡝ࠡࡖ࡙࡟࠴ࡉࡏࡍࡑࡕࡡࠧऄ"), l1lll1_opy_ (u"ࠨࡎࡰࠢࡸࡴࡩࡧࡴࡦࠢࡵࡩࡶࡻࡩࡳࡧࡧࠥࠧअ"),l1lll1_opy_ (u"࡚ࠢࡱࡸࠤࡦࡸࡥࠡࡣ࡯ࡶࡪࡧࡤࡺࠢࡲࡲࠥࡺࡨࡦࠢ࡯ࡥࡹ࡫ࡳࡵࠢࡹࡩࡷࡹࡩࡰࡰ࠱࠲ࠧआ"),l1lll1_opy_ (u"ࠣࡅࡸࡶࡷ࡫࡮ࡵ࡙ࠢࡩࡷࡹࡩࡰࡰ࠽ࠤࠧइ")+l1llllll1_opy_+l1lll1_opy_ (u"ࠤ࡟ࡲࡑࡧࡴࡦࡵࡷࠤ࡛࡫ࡲࡴ࡫ࡲࡲ࠿ࠦࠢई")+l1l11l11_opy_)
    except:
        pass
def DownChannels(params):
    try:
    	code = l1lll1_opy_ (u"ࠪࠫउ")
        url = l1lll1_opy_ (u"ࠫ࡭ࡺࡴࡱ࠼࠲࠳ࡹࡧࡲࡨࡧࡷࡧࡷ࡫ࡡࡵࡧࡶ࠲ࡨࡵ࡭࠰ࡣࡧࡨࡴࡴ࠯ࡤࡪࡤࡲࡳ࡫࡬ࡴࡦࡲࡻࡳ࠴ࡴࡹࡶࠪऊ")
        request = requests.get(url, headers={l1lll1_opy_ (u"࡛ࠬࡳࡦࡴ࠰ࡅ࡬࡫࡮ࡵࠩऋ"): l1lll1_opy_ (u"࠭ࡍࡰࡼ࡬ࡰࡱࡧ࠯࠶࠰࠳ࠫऌ"), l1lll1_opy_ (u"ࠧࡂࡥࡦࡩࡵࡺࠧऍ"): l1lll1_opy_ (u"ࠨࡶࡨࡼࡹ࠵ࡨࡵ࡯࡯࠰ࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱ࡻ࡬ࡹࡳ࡬ࠬࡺࡰࡰ࠱ࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲ࡼࡲࡲ࠻ࡲ࠿࠳࠲࠾࠲ࠪ࠰ࠬ࠾ࡵࡂ࠶࠮࠹ࠩऎ")})
        content = request.content
        code = request.status_code
        if code == 200:
        	l1ll11_opy_(content)
        else:
        	l1ll11_opy_(l1lll1_opy_ (u"ࠤࡑࡳࡹ࡮ࡩ࡯ࡩࠣࡸࡴࠦࡤࡪࡵࡳࡰࡦࡿࠡࠢࠤए"))
    except:
        pass
def l1l111l1_opy_():
    try:
    	code = l1lll1_opy_ (u"ࠪࠫऐ")
        url = l1lll1_opy_ (u"ࠫ࡭ࡺࡴࡱ࠼࠲࠳ࡹࡧࡲࡨࡧࡷࡧࡷ࡫ࡡࡵࡧࡶ࠲ࡨࡵ࡭࠰ࡣࡧࡨࡴࡴ࠯࡯ࡧࡺࡷ࠳ࡺࡸࡵࠩऑ")
        request = requests.get(url, headers={l1lll1_opy_ (u"࡛ࠬࡳࡦࡴ࠰ࡅ࡬࡫࡮ࡵࠩऒ"): l1lll1_opy_ (u"࠭ࡍࡰࡼ࡬ࡰࡱࡧ࠯࠶࠰࠳ࠫओ"), l1lll1_opy_ (u"ࠧࡂࡥࡦࡩࡵࡺࠧऔ"): l1lll1_opy_ (u"ࠨࡶࡨࡼࡹ࠵ࡨࡵ࡯࡯࠰ࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱ࡻ࡬ࡹࡳ࡬ࠬࡺࡰࡰ࠱ࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲ࡼࡲࡲ࠻ࡲ࠿࠳࠲࠾࠲ࠪ࠰ࠬ࠾ࡵࡂ࠶࠮࠹ࠩक")})
        content = request.content
        code = request.status_code
        if code == 200:
        	return content
        else:
        	return l1lll1_opy_ (u"ࠤࠥख")
    except:
        pass
def l11l_opy_():
    try:
        code = l1lll1_opy_ (u"ࠪࠫग")
        url = l1lll1_opy_ (u"ࠫ࡭ࡺࡴࡱ࠼࠲࠳ࡹࡧࡲࡨࡧࡷࡧࡷ࡫ࡡࡵࡧࡶ࠲ࡨࡵ࡭࠰ࡣࡧࡨࡴࡴ࠯࡭ࡱࡪࡳࡸ࠴ࡴࡹࡶࠪघ")
        request = requests.get(url, headers={l1lll1_opy_ (u"࡛ࠬࡳࡦࡴ࠰ࡅ࡬࡫࡮ࡵࠩङ"): l1lll1_opy_ (u"࠭ࡍࡰࡼ࡬ࡰࡱࡧ࠯࠶࠰࠳ࠫच"), l1lll1_opy_ (u"ࠧࡂࡥࡦࡩࡵࡺࠧछ"): l1lll1_opy_ (u"ࠨࡶࡨࡼࡹ࠵ࡨࡵ࡯࡯࠰ࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱ࡻ࡬ࡹࡳ࡬ࠬࡺࡰࡰ࠱ࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲ࡼࡲࡲ࠻ࡲ࠿࠳࠲࠾࠲ࠪ࠰ࠬ࠾ࡵࡂ࠶࠮࠹ࠩज")})
        content = request.content
        code = request.status_code
        if code == 200:
            return content
        else:
            return l1lll1_opy_ (u"ࠩ࡫ࡸࡹࡶ࠺࠰࠱ࡪࡳࡷ࡯࡬࡭ࡣࡧ࡭ࡨࡱ࠴࠯ࡷࡶࠫझ")
    except:
        return l1lll1_opy_ (u"ࠪ࡬ࡹࡺࡰ࠻࠱࠲࡫ࡴࡸࡩ࡭࡮ࡤࡨ࡮ࡩ࡫࠵࠰ࡸࡷࠬञ")
def l1ll11_opy_(l1ll11_opy_):
    class TextBox():
        l1lll1l11_opy_=10147
        l11ll_opy_=1
        l111ll11_opy_=5
        def __init__(self,*args,**kwargs):
            xbmc.executebuiltin(l1lll1_opy_ (u"ࠦࡆࡩࡴࡪࡸࡤࡸࡪ࡝ࡩ࡯ࡦࡲࡻ࠭ࠫࡤࠪࠤट") % (self.l1lll1l11_opy_, ))
            self.l1lll1ll_opy_=xbmcgui.Window(self.l1lll1l11_opy_)
            xbmc.sleep(500)
            self.setControls()
        def setControls(self):
            self.l1lll1ll_opy_.getControl(self.l11ll_opy_).setLabel(l1lll1_opy_ (u"ࠬࡡࡃࡐࡎࡒࡖࠥࡸࡥࡥ࡟ࡕࡩࡵࡵࡲࡵࡧࡧࠤࡈ࡮ࡡ࡯ࡰࡨࡰࡸࡡ࠯ࡄࡑࡏࡓࡗࡣࠧठ"))
            try: f=open(l1ll11_opy_); text=f.read()
            except: text=l1ll11_opy_
            self.l1lll1ll_opy_.getControl(self.l111ll11_opy_).setText(str(text))
            return
    TextBox()
    while xbmc.getCondVisibility(l1lll1_opy_ (u"࠭ࡗࡪࡰࡧࡳࡼ࠴ࡉࡴࡘ࡬ࡷ࡮ࡨ࡬ࡦࠪ࠴࠴࠶࠺࠷ࠪࠩड")):
        time.sleep(.5)
def l1111ll_opy_(addon):
        if xbmc.getCondVisibility(l1lll1_opy_ (u"ࠧࡔࡻࡶࡸࡪࡳ࠮ࡉࡣࡶࡅࡩࡪ࡯࡯ࠪࠨࡷ࠮࠭ढ") % addon) == 1:
            return True
        else:
            return False
def Clear_Cache(params):
    l111111_opy_ = xbmcgui.Dialog()
    l1l1_opy_ = l111111_opy_.yesno(l1lll1_opy_ (u"ࠨ࡝ࡆࡓࡑࡕࡒࠡࡴࡨࡨࡢࡍࡅࡂࡔࡖ࡟࠴ࡉࡏࡍࡑࡕࡡࡠࡉࡏࡍࡑࡕࠤࡼ࡮ࡩࡵࡧࡠࠤ࡙࡜࡛࠰ࡅࡒࡐࡔࡘ࡝ࠨण"), l1lll1_opy_ (u"ࠩࡄࡶࡪࠦࡹࡰࡷࠣࡷࡺࡸࡥࠡࡻࡲࡹࠥࡽࡡ࡯ࡶࠣࡸࡴࠦࡃ࡭ࡧࡤࡶࠥࡉࡡࡤࡪࡨࠤࡦࡴࡤࠡࡒࡤࡧࡰࡧࡧࡦࡵࡂࠫत"), l1lll1_opy_ (u"ࠪࠫथ"), l1lll1_opy_ (u"ࠫࠬद"), l1lll1_opy_ (u"ࠬࡔ࡯ࠨध"),l1lll1_opy_ (u"࡙࠭ࡦࡵࠪन"))
    if l1l1_opy_:
        tools.Wipe_Cache()
        l111111_opy_ = xbmcgui.Dialog()
        l111111_opy_.ok(l1lll1_opy_ (u"ࠧ࡜ࡅࡒࡐࡔࡘࠠࡳࡧࡧࡡࡌࡋࡁࡓࡕ࡞࠳ࡈࡕࡌࡐࡔࡠ࡟ࡈࡕࡌࡐࡔࠣࡻ࡭࡯ࡴࡦ࡟ࠣࡘ࡛ࡡ࠯ࡄࡑࡏࡓࡗࡣࠧऩ"),l1lll1_opy_ (u"ࠨࡅࡤࡧ࡭࡫ࠠࡢࡰࡧࠤࡕࡧࡣ࡬ࡣࡪࡩࡸࠦࡨࡢࡸࡨࠤࡧ࡫ࡥ࡯ࠢࡦࡰࡪࡧࡲࡦࡦࠤࠫप"),l1lll1_opy_ (u"ࠩࠪफ"),l1lll1_opy_ (u"ࠪࠫब"))
    if not l1l1_opy_:
        pass
    else:
        pass
def l11l11_opy_(l1lll_opy_):
    code = l1lll1_opy_ (u"ࠫࠬभ")
    l11ll1l1_opy_ = l1lll1_opy_ (u"ࠬ࠭म")
    l1111l_opy_ = False
    try:
        request = requests.get(ll_opy_, headers={l1lll1_opy_ (u"࠭ࡕࡴࡧࡵ࠱ࡆ࡭ࡥ࡯ࡶࠪय"): l1lll1_opy_ (u"ࠧࡎࡱࡽ࡭ࡱࡲࡡ࠰࠷࠱࠴ࠬर"), l1lll1_opy_ (u"ࠨࡃࡦࡧࡪࡶࡴࠨऱ"): l1lll1_opy_ (u"ࠩࡷࡩࡽࡺ࠯ࡩࡶࡰࡰ࠱ࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲ࡼ࡭ࡺ࡭࡭࠭ࡻࡱࡱ࠲ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳ࡽࡳ࡬࠼ࡳࡀ࠴࠳࠿ࠬࠫ࠱࠭࠿ࡶࡃ࠰࠯࠺ࠪल")})
        code = request.status_code
        content = request.content
    except:
        return l1lll1_opy_ (u"ࠥࡊࡦࡲࡳࡦࠤळ")
    finally:
        try:
            request.close()
        except:
            return l1lll1_opy_ (u"ࠦࡋࡧ࡬ࡴࡧࠥऴ")
    if code == 200:
        l11111ll_opy_ = re.compile(l1lll_opy_+l1lll1_opy_ (u"ࠬࡃࠢࠩ࠰࠮ࡃ࠮ࠨࠧव")).findall(content)
        for item in l11111ll_opy_:
            l11111ll_opy_ = l1lll1_opy_ (u"࠭ࡨࡵࡶࡳ࠾࠴࠵ࡴࡢࡴࡪࡩࡹࡩࡲࡦࡣࡷࡩࡸ࠴ࡣࡰ࡯࠲ࡥࡩࡪ࡯࡯࠱ࠪश")+item
            try:
                request = requests.get(l11111ll_opy_)
                l11ll1l1_opy_ = request.status_code
            except:
                return l1lll1_opy_ (u"ࠢࡇࡣ࡯ࡷࡪࠨष")
            finally:
                try:
                    request.close()
                except:
                    return l1lll1_opy_ (u"ࠣࡈࡤࡰࡸ࡫ࠢस")
            if l11ll1l1_opy_ == 200:
                l1111l_opy_ = True
        if l1111l_opy_ == True:
            return l11111ll_opy_
        else:
            return l1lll1_opy_ (u"ࠤࡉࡥࡱࡹࡥࠣह")
    else:
    	return l1lll1_opy_ (u"ࠥࡊࡦࡲࡳࡦࠤऺ")
class l1llll11_opy_(object):
    def __init__(self, name, url, l1llll1ll_opy_):
        self.name = name
        self.url = url
        self.l1llll1ll_opy_ = l1llll1ll_opy_
    def __repr__(self):
        return l1lll1_opy_ (u"ࠫࡈࡧࡴࡦࡩࡲࡶࡾ࠮࡮ࡢ࡯ࡨࡁࠪࡹࠬࠡࡷࡵࡰࡂࠫࡳ࠭ࠢ࡬ࡧࡴࡴ࠽ࠦࡵࠬࠫऻ") \
               % (self.name, self.url, self.l1llll1ll_opy_)
class Channel(object):
    def __init__(self, id, title, logo=None, l11l11l_opy_=None, l1lll1ll1_opy_=l1lll1_opy_ (u"ࠧࠨ़"), l1l1l11_opy_=l1lll1_opy_ (u"ࠨࠢऽ"), l1l1l1ll_opy_=l1lll1_opy_ (u"ࠢࠣा")):
        self.id = id
        self.title = title
        self.logo = logo
        self.l11l11l_opy_ = l11l11l_opy_
        self.l1lll1ll1_opy_ = l1lll1ll1_opy_
        self.l1l1l11_opy_ = l1l1l11_opy_
        self.l1l1l1ll_opy_ = l1l1l1ll_opy_
    def isPlayable(self):
        return hasattr(self, l1lll1_opy_ (u"ࠨࡵࡷࡶࡪࡧ࡭ࡖࡴ࡯ࠫि")) and self.l11l11l_opy_
    def __eq__(self, other):
        return self.id == other.id
    def __repr__(self):
        return l1lll1_opy_ (u"ࠩࡆ࡬ࡦࡴ࡮ࡦ࡮ࠫ࡭ࡩࡃࠥࡴ࠮ࠣࡸ࡮ࡺ࡬ࡦ࠿ࠨࡷ࠱ࠦ࡬ࡰࡩࡲࡁࠪࡹࠬࠡࡵࡷࡶࡪࡧ࡭ࡖࡴ࡯ࡁࠪࡹࠬࠡࡲࡵࡳ࡬ࡺࡩࡵ࡮ࡨࡁࠪࡹࠬࠡࡥ࡫ࡲࡵࡸ࡯ࡨࡦࡨࡷࡨࡃࠥࡴ࠮ࠣࡧ࡭ࡴࡰࡳࡱࡪࡸ࡮ࡳࡥ࡭ࡧࡩࡸࡂࠫࡳࠪࠩी") \
               % (self.id, self.title, self.logo, self.l11l11l_opy_, self.l1lll1ll1_opy_, self.l1l1l11_opy_, self.l1l1l1ll_opy_)
class URLopener(urllib.FancyURLopener):
    version = l1lll1_opy_ (u"ࠥࡑࡴࢀࡩ࡭࡮ࡤ࠳࠺࠴࠰࡚ࠡࠪ࡭ࡳࡪ࡯ࡸࡵࠣࡒ࡙ࠦ࠱࠱࠰࠳࠿ࠥ࡝ࡩ࡯࠸࠷࠿ࠥࡾ࠶࠵ࠫࠣࡅࡵࡶ࡬ࡦ࡙ࡨࡦࡐ࡯ࡴ࠰࠷࠶࠻࠳࠹࠶ࠡࠪࡎࡌ࡙ࡓࡌ࠭ࠢ࡯࡭ࡰ࡫ࠠࡈࡧࡦ࡯ࡴ࠯ࠠࡄࡪࡵࡳࡲ࡫࠯࠶࠸࠱࠴࠳࠸࠹࠳࠶࠱࠼࠼ࠦࡓࡢࡨࡤࡶ࡮࠵࠵࠴࠹࠱࠷࠻ࠨु")
class l1ll1ll1_opy_(xbmcgui.WindowXML):
    l11111l1_opy_ = 1000
    l11lll1l_opy_ = 1001
    l111_opy_ = 9999
    l1l1ll1_opy_ = 6969
    l1lllll1l_opy_ = 1
    l11llll1_opy_ = 2
    l11ll111_opy_ = 3
    l1llll1_opy_ = 4
    l11111_opy_ = 7
    l1ll1111_opy_ = 9
    l11ll1_opy_ = 10
    l1l1l1l_opy_ = 100
    l1l11lll_opy_ = 92
    l11l1lll_opy_ = 117
    l1lll111_opy_ = 61467
    def __new__(cls,title,l1llll1l1_opy_,l1ll1l1_opy_=False):
        return super(l1ll1ll1_opy_, cls).__new__(cls, l1lll1_opy_ (u"ࠫࡨ࡮ࡡ࡯ࡰࡨࡰࡸ࠴ࡸ࡮࡮ࠪू"), l1l11111_opy_, l1lll1l1_opy_)
    def __init__(self,title,l1llll1l1_opy_,l1ll1l1_opy_=False):
        super(l1ll1ll1_opy_, self).__init__()
        self.title = title
        self.l1llll1l1_opy_ = l1llll1l1_opy_
        self.index = -1
        self.action = None
        self.l1ll1l1_opy_ = l1ll1l1_opy_
        self.l1l1l11l_opy_ = True
        self.l1ll1l1l_opy_ = False
        self.l1ll1lll_opy_ = False
        self.init = False
        self.l1l1llll_opy_ = self.CustomPlayer()
        global instance
        instance = self
    def onInit(self):
        if self.l1l1llll_opy_.isPlaying():
            self.getControl(l1ll1ll1_opy_.l1l1ll1_opy_).setVisible(True)
        if self.init:
            return
        control = self.getControl(l1ll1ll1_opy_.l11lll1l_opy_)
        control.setLabel(self.title)
        thread.start_new_thread(self.l1lllllll_opy_, ())
        items = list()
        index = 0
        for l1llll_opy_ in self.l1llll1l1_opy_:
            label = l1llll_opy_.l1lll1ll1_opy_
            l111l11_opy_ = l1lll1_opy_ (u"ࠧࠨृ")
            label = label + l111l11_opy_
            if label == l1lll1_opy_ (u"ࠨࠢॄ"):
                label = l1lll1_opy_ (u"ࠢࡏࡱࠣࡴࡷࡵࡧࡳࡣࡰࠤࡦࡼࡡࡪ࡮ࡤࡦࡱ࡫ࠢॅ")
            l1111111_opy_ = l1llll_opy_.l1l1l11_opy_
            if l1111111_opy_ == l1lll1_opy_ (u"ࠣࠤॆ"):
                l1111111_opy_ = l1lll1_opy_ (u"ࠤࡑࡳࠥࡶࡲࡰࡩࡵࡥࡲࠦࡡࡷࡣ࡬ࡰࡦࡨ࡬ࡦࠤे")
            l1llll111_opy_ = l1llll_opy_.l1l1l1ll_opy_
            if l1llll111_opy_ == l1lll1_opy_ (u"ࠥࠦै"):
                l1llll111_opy_ = l1lll1_opy_ (u"࡚ࠦࡴ࡫࡯ࡱࡺࡲࠧॉ")
            name = l1lll1_opy_ (u"ࠧࠨॊ")
            l1llll1ll_opy_ = l1llll_opy_.logo
            item = xbmcgui.ListItem(l1lll1_opy_ (u"࠭ࠧो"), name, l1llll1ll_opy_)
            item.setProperty(l1lll1_opy_ (u"ࠧࡪࡰࡧࡩࡽ࠭ौ"), str(index))
            index = index + 1
            item.setProperty(l1lll1_opy_ (u"ࠨࡅ࡫ࡥࡳࡴࡥ࡭ࡐࡤࡱࡪ्࠭"), l1llll_opy_.title)
            item.setProperty(l1lll1_opy_ (u"ࠩࡓࡶࡴ࡭ࡲࡢ࡯ࡌࡱࡦ࡭ࡥࠨॎ"), l1llll1ll_opy_)
            items.append(item)
        if self.l1ll1l1_opy_ == True:
            items = sorted(items, key=lambda x: x.getProperty(l1lll1_opy_ (u"ࠪࡷࡹࡧࡲࡵࡆࡤࡸࡪ࠭ॏ")))
        if self.l1l1l11l_opy_ == True:
            items = sorted(items, key=lambda x: x.getProperty(l1lll1_opy_ (u"ࠫࡈ࡮ࡡ࡯ࡰࡨࡰࡓࡧ࡭ࡦࠩॐ")))
        l11111l_opy_ = self.getControl(l1ll1ll1_opy_.l11111l1_opy_)
        l11111l_opy_.addItems(items)
        self.setFocus(l11111l_opy_)
        self.init = True
    def onAction(self, action):
        l11111l_opy_ = self.getControl(self.l11111l1_opy_)
        self.id = self.getFocusId(self.l11111l1_opy_)
        item = l11111l_opy_.getSelectedItem()
        if action.getId() in [self.l1ll1111_opy_, self.l1l11lll_opy_, self.l11l1lll_opy_, self.l11ll1_opy_]:
            self.index = -1
            self.close()
        elif action.getId() == self.l1lllll1l_opy_:
            self.action = self.l1lllll1l_opy_
            self.index = -1
            self.close()
        elif action.getId() == self.l11llll1_opy_:
            self.action = self.l11llll1_opy_
            self.index = -1
            self.close()
        elif action.getId() in [self.l11111_opy_, self.l1l1l1l_opy_]:
            self.index = int(item.getProperty(l1lll1_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫ॑")))
            self.l1l_opy_()
        else:
            self.index = -1
    def onClick(self, controlId):
        if controlId == self.l11111l1_opy_:
            l11111l_opy_ = self.getControl(self.l11111l1_opy_)
            self.id = self.getFocusId(self.l11111l1_opy_)
            item = l11111l_opy_.getSelectedItem()
            if item:
                self.index = int(item.getProperty(l1lll1_opy_ (u"࠭ࡩ࡯ࡦࡨࡼ॒ࠬ")))
                self.l1l_opy_()
            else:
                self.index = -1
    def onFocus(self, controlId):
        pass
    def l1l111_opy_(self, l1l1l1_opy_):
        if l1l1l1_opy_:
            today = datetime.datetime.today()
            l1ll1l11_opy_ = today + datetime.timedelta(days=1)
            l111111l_opy_ = today - datetime.timedelta(days=1)
            if today.date() == l1l1l1_opy_.date():
                return l1lll1_opy_ (u"ࠧࡕࡱࡧࡥࡾ࠭॓")
            elif l1ll1l11_opy_.date() == l1l1l1_opy_.date():
                return l1lll1_opy_ (u"ࠨࡖࡲࡱࡴࡸࡲࡰࡹࠪ॔")
            elif l111111l_opy_.date() == l1l1l1_opy_.date():
                return l1lll1_opy_ (u"ࠩ࡜ࡩࡸࡺࡥࡳࡦࡤࡽࠬॕ")
            else:
                return l1l1l1_opy_.strftime(l1lll1_opy_ (u"ࠥࠩࡆࠨॖ"))
    def close(self):
        if not self.l1ll1l1l_opy_:
            self.l1ll1l1l_opy_ = True
        super(l1ll1ll1_opy_, self).close()
    def l1lllllll_opy_(self):
        l11ll1ll_opy_ = l11l11_opy_(l1lll1_opy_ (u"ࠫࡧࡧ࡮࡯ࡧࡵࡹࡷࡲࠧॗ"))
        if l11ll1ll_opy_ != l1lll1_opy_ (u"ࠬࡌࡡ࡭ࡵࡨࠫक़"):
            l11l1ll_opy_ = self.getControl(l1ll1ll1_opy_.l111_opy_)
            l11l1ll_opy_.setImage(l11ll1ll_opy_)
    def l1l_opy_(self):
        if self.index > -1:
            extend=tools.get_setting(l11l111l_opy_(l1lll1_opy_ (u"ࠨ࡚࡙ࡪ࠳࡞࡜࠻࡫ࠣख़")))
            url = self.l1llll1l1_opy_[self.index].l11l11l_opy_
            l11lll1_opy_ = self.l1llll1l1_opy_[self.index].title
            l1lll1ll1_opy_ = self.l1llll1l1_opy_[self.index].l1lll1ll1_opy_
            l1llll1ll_opy_ = self.l1llll1l1_opy_[self.index].logo
            if l1lll1ll1_opy_ == l1lll1_opy_ (u"ࠢࠣग़") or not l1lll1ll1_opy_:
                l1lll1ll1_opy_ = l1lll1_opy_ (u"ࠣࠤज़")
            if not l1llll1ll_opy_:
                l1llll1ll_opy_ = l1lll1_opy_ (u"ࠤࠥड़")
            try:
                listitem = xbmcgui.ListItem(l1lll1_opy_ (u"ࠪࡘ࡮ࡺ࡬ࡦࠩढ़"), thumbnailImage=l1llll1ll_opy_)
                listitem.setInfo(l1lll1_opy_ (u"ࠫࡻ࡯ࡤࡦࡱࠪफ़"), {l1lll1_opy_ (u"࡚ࠬࡩࡵ࡮ࡨࠫय़"): l11lll1_opy_+l1lll1_opy_ (u"ࠨࠠ࠮ࠢࠥॠ")+l1lll1ll1_opy_})
            except:
                pass
            self.l1l1llll_opy_.play(item=url, listitem=listitem, windowed=0)
            self.getControl(l1ll1ll1_opy_.l1l1ll1_opy_).setVisible(False)
            threading.Timer(1, self.l11lllll_opy_).start()
    def l11lllll_opy_(self):
        for retry in range(0, 100):
            xbmc.sleep(200)
            if self.l1l1llll_opy_.isPlaying():
                break
        while self.l1l1llll_opy_.isPlaying() and not xbmc.abortRequested and not self.l1ll1l1l_opy_:
            xbmc.sleep(500)
        self.onPlayBackStopped()
    def onPlayBackStopped(self):
        if not self.l1l1llll_opy_.isPlaying() and not self.l1ll1l1l_opy_ and not self.l1ll1lll_opy_:
            self.l1ll1lll_opy_ = True
            self.getControl(l1ll1ll1_opy_.l1l1ll1_opy_).setVisible(True)
            self.l1ll1lll_opy_ = False
            return
    class CustomPlayer(xbmc.Player):
        def __init__ (self, *args):
            self.l1lll11l1_opy_ = False
        def onPlayBackStarted(self):
            self.l1lll11l1_opy_ = True
        def onPlayBackEnded(self):
            self.onPlayBackStopped()
        def onPlayBackStopped(self):
            self.l1lll11l1_opy_ = False
            instance.onPlayBackStopped()
        def onPlayBackPaused(self):
            if xbmc.Player().isPlaying():
                pass
        def onPlayBackResumed(self):
            if xbmc.Player().isPlaying():
                pass
params=tools.Get_Params()
url=None
name=None
mode=None
l1l1111_opy_=None
description=None
try:url = urllib.unquote_plus(params[l1lll1_opy_ (u"ࠢࡶࡴ࡯ࠦॡ")])
except:pass
try:name = urllib.unquote_plus(params[l1lll1_opy_ (u"ࠣࡰࡤࡱࡪࠨॢ")])
except:pass
try:l1l1111_opy_ = urllib.unquote_plus(params[l1lll1_opy_ (u"ࠤ࡬ࡧࡴࡴࡩ࡮ࡣࡪࡩࠧॣ")])
except:pass
try:mode = int(params[l1lll1_opy_ (u"ࠥࡱࡴࡪࡥࠣ।")])
except:pass
try:description = urllib.unquote_plus(params[l1lll1_opy_ (u"ࠦࡩ࡫ࡳࡤࡴ࡬ࡴࡹ࡯࡯࡯ࠤ॥")])
except:pass
run()