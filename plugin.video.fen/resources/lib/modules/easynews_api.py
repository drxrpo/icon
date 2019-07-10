import xbmcaddon
import re
import random
import urllib
import urllib2
import urlparse
import json
import time, datetime
import base64
from resources.lib.modules import fen_cache
from resources.lib.modules.utils import to_utf8
# from resources.lib.modules.utils import logger

__addon_id__ = 'plugin.video.fen'
__addon__ = xbmcaddon.Addon(id=__addon_id__)
_cache = fen_cache.FenCache()

SORT = {'s1': 'relevance', 's1d': '-', 's2': 'dsize', 's2d': '-', 's3': 'dtime', 's3d': '-'}
SEARCH_PARAMS = {'st': 'adv', 'safeO': 0, 'sb': 1, 'fex': 'mkv, mp4, avi', 'fty[]': 'VIDEO', 'spamf': 1, 'u': '1', 'gx': 1, 'pno': 1, 'sS': 3}
SEARCH_PARAMS.update(SORT)
BR_VERS = [
    ['%s.0' % i for i in xrange(18, 53)],
    ['37.0.2062.103', '37.0.2062.120', '37.0.2062.124', '38.0.2125.101', '38.0.2125.104', '38.0.2125.111', '39.0.2171.71', '39.0.2171.95', '39.0.2171.99', '40.0.2214.93', '40.0.2214.111',
     '40.0.2214.115', '42.0.2311.90', '42.0.2311.135', '42.0.2311.152', '43.0.2357.81', '43.0.2357.124', '44.0.2403.155', '44.0.2403.157', '45.0.2454.101', '45.0.2454.85', '46.0.2490.71',
     '46.0.2490.80', '46.0.2490.86', '47.0.2526.73', '47.0.2526.80', '48.0.2564.116', '49.0.2623.112', '50.0.2661.86', '51.0.2704.103', '52.0.2743.116', '53.0.2785.143', '54.0.2840.71',
     '56.0.2924.87', '57.0.2987.133'],
    ['11.0'],
    ['8.0', '9.0', '10.0', '10.6']]

RAND_UAS = ['Mozilla/5.0 ({win_ver}{feature}; rv:{br_ver}) Gecko/20100101 Firefox/{br_ver}',
            'Mozilla/5.0 ({win_ver}{feature}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{br_ver} Safari/537.36',
            'Mozilla/5.0 ({win_ver}{feature}; Trident/7.0; rv:{br_ver}) like Gecko',
            'Mozilla/5.0 (compatible; MSIE {br_ver}; {win_ver}{feature}; Trident/6.0)']
FEATURES = ['; WOW64', '; Win64; IA64', '; Win64; x64', '']
WIN_VERS = ['Windows NT 10.0', 'Windows NT 7.0', 'Windows NT 6.3', 'Windows NT 6.2', 'Windows NT 6.1', 'Windows NT 6.0', 'Windows NT 5.1', 'Windows NT 5.0']

class EasyNewsAPI:
    def __init__(self):
        self.base_url = 'https://members.easynews.com'
        self.search_link = '/2.0/search/solr-search/advanced'
        self.username = __addon__.getSetting('easynews_user')
        self.password = __addon__.getSetting('easynews_password')
        self.auth = 'Basic ' + base64.b64encode('%s:%s' % (self.username, self.password))
        self.account_link = 'https://account.easynews.com/editinfo.php'
        self.usage_link = 'https://account.easynews.com/usageview.php'

    def search(self, query):
        cache = _cache.get("fen_%s_%s" % ('EASYNEWS_SEARCH', query))
        if cache:
            files = cache
        else:
            query_url = '/search?query=%s' % (urllib.quote_plus(query))
            results = self._get_links(query_url)
            files = to_utf8(self._process_files(results))
            _cache.set("fen_%s_%s" % ('EASYNEWS_SEARCH', query), files,
                expiration=datetime.timedelta(hours=2))
        return files

    def account(self):
        from bs4 import BeautifulSoup
        account_html = self._http_get(self.account_link)
        if account_html == None or account_html == '': raise Exception()
        account_html = BeautifulSoup(account_html, "html.parser")
        account_html = account_html.find_all('form', id = 'accountForm')[0]
        account_html = account_html.find_all('table', recursive = False)[0]
        account_html = account_html.find_all('tr', recursive = False)
        usage_html = self._http_get(self.usage_link)
        if usage_html == None or usage_html == '': raise Exception()
        usage_html = BeautifulSoup(usage_html, "html.parser")
        usage_html = usage_html.find_all('div', class_ = 'table-responsive')[0]
        usage_html = usage_html.find_all('table', recursive = False)[0]
        usage_html = usage_html.find_all('tr', recursive = False)
        account_info = {
                    'account_username': to_utf8(account_html[0].find_all('td', recursive = False)[1].getText()),
                    'account_type': to_utf8(account_html[1].find_all('td', recursive = False)[2].getText()),
                    'account_status': to_utf8(account_html[3].find_all('td', recursive = False)[2].getText()),
                    'account_expiration': to_utf8(account_html[2].find_all('td', recursive = False)[2].getText()),
                    'usage_total': to_utf8(usage_html[0].find_all('td', recursive = False)[1].getText()),
                    'usage_web': to_utf8(usage_html[1].find_all('td', recursive = False)[2].getText()),
                    'usage_NNTP': to_utf8(usage_html[2].find_all('td', recursive = False)[2].getText()),
                    'usage_remaining': to_utf8(usage_html[4].find_all('td', recursive = False)[2].getText()),
                    'usage_loyalty': to_utf8(usage_html[5].find_all('td', recursive = False)[2].getText())
                        }
        return account_info

    def _get_links(self, url):
        search_url, params = self._translate_search(url)
        html = self._http_get(search_url, params=params)
        result = self._parse_json(html)
        return result

    def _process_files(self, files):
        results = []
        down_url = files.get('downURL')
        dl_farm = files.get('dlFarm')
        dl_port = files.get('dlPort')
        files = files.get('data', [])
        for item in files:
            try:
                post_hash, size, post_title, ext, duration = item['0'], item['4'], item['10'], item['11'], item['14']
                checks = [False] * 5
                if 'alangs' in item and item['alangs'] and 'eng' not in item['alangs']: checks[1] = True
                if re.match('^\d+s', duration) or re.match('^[0-5]m', duration): checks[2] = True
                if 'passwd' in item and item['passwd']: checks[3] = True
                if 'virus' in item and item['virus']: checks[4] = True
                if 'type' in item and item['type'].upper() != 'VIDEO': checks[5] = True
                if any(checks):
                    continue
                stream_url = down_url + urllib.quote('/%s/%s/%s%s/%s%s' % (dl_farm, dl_port, post_hash, ext, post_title, ext))
                file_name = post_title
                file_dl = stream_url + '|Authorization=%s' % (urllib.quote(self.auth))
                results.append({'name': file_name,
                                'size': size,
                                'rawSize': item['rawSize'],
                                'url_dl': file_dl,
                                'full_item': item})
            except: pass
        return results

    def _http_get(self, url, params=None):
        MAX_RESPONSE = 1024 * 1024 * 5
        if not self.username or not self.password:
            return ''
        headers = {'Authorization': self.auth}
        if params:
            parts = urlparse.urlparse(url)
            if parts.query:
                params.update(self._parse_query(url))
                url = urlparse.urlunparse((parts.scheme, parts.netloc, parts.path, parts.params, '', parts.fragment))
            url += '?' + urllib.urlencode(params)
        if isinstance(url, unicode): url = url.encode('utf-8')
        request = urllib2.Request(url)
        headers = headers.copy()
        request.add_header('User-Agent', self._get_ua())
        request.add_header('Accept', '*/*')
        request.add_header('Accept-Encoding', 'gzip')
        request.add_unredirected_header('Host', request.get_host())
        for key, value in headers.iteritems(): request.add_header(key, value)
        response = urllib2.urlopen(request)
        if (response.getcode() in [301, 302, 303, 307] or response.info().getheader('Refresh')):
            if response.info().getheader('Refresh') is not None:
                refresh = response.info().getheader('Refresh')
                return refresh.split(';')[-1].split('url=')[-1]
            else:
                redir_url = response.info().getheader('Location')
                if redir_url.startswith('='):
                    redir_url = redir_url[1:]
                return redir_url
        content_length = response.info().getheader('Content-Length', 0)
        if int(content_length) > MAX_RESPONSE:
            return
        html = response.read(MAX_RESPONSE)
        return html

    def _translate_search(self, url):
        params = SEARCH_PARAMS
        params['pby'] = 100
        params['gps'] = params['sbj'] = self._parse_query(url)['query']
        url = self.base_url + self.search_link
        return url, params

    def _get_ua(self):
        try: last_gen = int(__addon__.getSetting('last_ua_create'))
        except: last_gen = 0
        if not __addon__.getSetting('current_ua') or last_gen < (time.time() - (7 * 24 * 60 * 60)):
            index = random.randrange(len(RAND_UAS))
            versions = {'win_ver': random.choice(WIN_VERS), 'feature': random.choice(FEATURES), 'br_ver': random.choice(BR_VERS[index])}
            user_agent = RAND_UAS[index].format(**versions)
            __addon__.setSetting('current_ua', user_agent)
            __addon__.setSetting('last_ua_create', str(int(time.time())))
        else:
            user_agent = __addon__.getSetting('current_ua')
        return user_agent

    def _parse_query(self, url):
        import urlparse
        q = {}
        queries = urlparse.parse_qs(urlparse.urlparse(url).query)
        if not queries: queries = urlparse.parse_qs(url)
        for key, value in queries.iteritems():
            if len(value) == 1:
                q[key] = value[0]
            else:
                q[key] = value
        return q

    def _parse_json(self, html):
        import json
        if html:
            try:
                if not isinstance(html, unicode):
                    if html.startswith('\xef\xbb\xbf'):
                        html = html[3:]
                    elif html.startswith('\xfe\xff'):
                        html = html[2:]
                    html = html.decode('utf-8')
                    
                js_data = json.loads(html)
                if js_data is None:
                    return {}
                else:
                    return js_data
            except (ValueError, TypeError):
                return {}
        else:
            return {}

    def to_bytes(self, num, unit):
        unit = unit.upper()
        if unit.endswith('B'): unit = unit[:-1]
        units = ['', 'K', 'M', 'G', 'T', 'P', 'E', 'Z']
        try: mult = pow(1024, units.index(unit))
        except: mult = sys.maxint
        return int(float(num) * mult)

