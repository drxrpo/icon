# coding: UTF-8
import sys
l1_opy_ = sys.version_info [0] == 2
l11_opy_ = 2048
l1l11_opy_ = 7
def l1lll_opy_ (ll_opy_):
    global l1l_opy_
    l1l1l_opy_ = ord (ll_opy_ [-1])
    l1ll1_opy_ = ll_opy_ [:-1]
    l1l1_opy_ = l1l1l_opy_ % len (l1ll1_opy_)
    l11l_opy_ = l1ll1_opy_ [:l1l1_opy_] + l1ll1_opy_ [l1l1_opy_:]
    if l1_opy_:
        l1ll_opy_ = unicode () .join ([unichr (ord (char) - l11_opy_ - (l111_opy_ + l1l1l_opy_) % l1l11_opy_) for l111_opy_, char in enumerate (l11l_opy_)])
    else:
        l1ll_opy_ = str () .join ([chr (ord (char) - l11_opy_ - (l111_opy_ + l1l1l_opy_) % l1l11_opy_) for l111_opy_, char in enumerate (l11l_opy_)])
    return eval (l1ll_opy_)
