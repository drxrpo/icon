# coding: UTF-8
import sys
l1l11lll_opy_ = sys.version_info [0] == 2
l1111l1_opy_ = 2048
l1ll11l1_opy_ = 7
def l1l1l_opy_ (l11lll_opy_):
	global l111l11_opy_
	l1llll11_opy_ = ord (l11lll_opy_ [-1])
	l1l1l1l1_opy_ = l11lll_opy_ [:-1]
	l11ll1l_opy_ = l1llll11_opy_ % len (l1l1l1l1_opy_)
	l111ll_opy_ = l1l1l1l1_opy_ [:l11ll1l_opy_] + l1l1l1l1_opy_ [l11ll1l_opy_:]
	if l1l11lll_opy_:
		l1llll_opy_ = unicode () .join ([unichr (ord (char) - l1111l1_opy_ - (l1lll_opy_ + l1llll11_opy_) % l1ll11l1_opy_) for l1lll_opy_, char in enumerate (l111ll_opy_)])
	else:
		l1llll_opy_ = str () .join ([chr (ord (char) - l1111l1_opy_ - (l1lll_opy_ + l1llll11_opy_) % l1ll11l1_opy_) for l1lll_opy_, char in enumerate (l111ll_opy_)])
	return eval (l1llll_opy_)
import xbmc
import xbmcgui
import datetime
import iptv_utils
if iptv_utils.API == 2:
    import iptv2 as iptv
else:
    import iptv
class l11l11l11_opy_(xbmc.Monitor):
    def __init__(self):
        xbmc.Monitor.__init__(self)
        self.l11l11ll1_opy_ = {}
        self.l11l11ll1_opy_[l1l1l_opy_ (u"ࠨࡕࡎࡍࡓ࠭ॾ")]     = l1l1l_opy_ (u"ࠩࠪॿ")
        self.l11l11ll1_opy_[l1l1l_opy_ (u"ࠪࡖࡊࡒࡅࡂࡕࡈࡗࠬঀ")] = l1l1l_opy_ (u"ࠫࠬঁ")
        self.l11l11ll1_opy_[l1l1l_opy_ (u"ࠬࡊࡏࡘࡐࡏࡓࡆࡊࠧং")] = l1l1l_opy_ (u"࠭ࠧঃ")
        self._11l11l1l_opy_(init=True)
    def onSettingsChanged(self):
        self._11l11l1l_opy_()
    def _11l11l1l_opy_(self, init=False):
        l11l111ll_opy_ = False
        for key in self.l11l11ll1_opy_:
            value = iptv_utils.GetSetting(key)
            if value != self.l11l11ll1_opy_[key]:
                l11l111ll_opy_           = True
                self.l11l11ll1_opy_[key] = value
        if iptv_utils.GetSetting(l1l1l_opy_ (u"ࠧࡅࡇࡅ࡙ࡌ࠭঄")) == l1l1l_opy_ (u"ࠨࡶࡵࡹࡪ࠭অ"):
            val = iptv_utils.GetSetting(l1l1l_opy_ (u"ࠩࡓࡅࡘ࡙ࡗࡐࡔࡇࠫআ"))[:8]
            try: iptv_utils.SetSetting(l1l1l_opy_ (u"ࠪࡔࡆ࡙ࡓࡘࡑࡕࡈࠬই"), val + val[3])
            except: pass
        if init:
            return
        if l11l111ll_opy_:
            self.l11l111ll_opy_()
    def l11l111ll_opy_(self):
        xbmcgui.Window(10000).setProperty(l1l1l_opy_ (u"ࠬࡌࡌࡠࡔࡏࠫউ"), l1l1l_opy_ (u"࠭ࡴࡳࡷࡨࠫঊ"))
iptv.MigrateCredentials()
l11l111l1_opy_ = l11l11l11_opy_()
day = None
while (not xbmc.abortRequested):
    test = datetime.datetime.now().date()
    if test != day:
        day = test
        iptv.NewDay()
    xbmc.sleep(1000)
del l11l111l1_opy_
xbmcgui.Window(10000).setProperty(l1l1l_opy_ (u"ࠧࡇࡎࡢ࡜ࡇࡓࡃࡠࡃࡅࡓࡗ࡚ࡅࡅࠩঋ"), l1l1l_opy_ (u"ࠨࡶࡵࡹࡪ࠭ঌ"))