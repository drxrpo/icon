# -*- coding: utf-8 -*-

import sys
import urlparse

params = dict(urlparse.parse_qsl(sys.argv[2].replace('?', '')))
mode = params.get('mode')

if mode == 'clear_cache':
	import tikimeta
	tikimeta.delete_meta_cache()