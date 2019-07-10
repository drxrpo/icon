import xbmcaddon, xbmcgui
import re
import json
from resources.lib.modules.easynews_api import EasyNewsAPI
from resources.lib.modules.utils import clean_file_name, replace_html_codes
from resources.lib.modules import settings
# from resources.lib.modules.utils import logger

__addon_id__ = 'plugin.video.fen'
__addon__ = xbmcaddon.Addon(id=__addon_id__)
window = xbmcgui.Window(10000)
EasyNews = EasyNewsAPI()

class EasyNewsSource:
    def __init__(self):
        self.scrape_provider = 'easynews'
        self.sources = []
        self.provider_color = settings.provider_color(self.scrape_provider)
        self.show_filenames = settings.show_filenames()
        self.max_results = int(__addon__.getSetting('easynews_limit'))
        self.max_gb = __addon__.getSetting('easynews_maxgb')
        self.max_bytes = int(self.max_gb) * 1024 * 1024 * 1024

    def results(self, info):
        self.info = info
        search_name = self._search_name()
        files = EasyNews.search(search_name)
        files = files[0:self.max_results]
        for item in files:
            try:
                if self.max_bytes:
                    match = re.search('([\d.]+)\s+(.*)', item['size'])
                    if match:
                        size_bytes = self.to_bytes(*match.groups())
                        if size_bytes > self.max_bytes:
                            continue
                self.file_name = item['name']
                self.file_dl = item['url_dl']
                self.size = item['rawSize']
                self.video_info = ''
                self.details = self._get_release_details()
                self.video_quality = self._get_release_quality(self.file_name)
                self.display_name = self._build_display_name()
                self.sources.append({'name': self.file_name,
                                'display_name': self.display_name,
                                'label': self.display_name,
                                'quality': self.video_quality,
                                'size': self.size,
                                'url_dl': self.file_dl,
                                'id': self.file_dl,
                                'local': False,
                                'direct': True,
                                'source': self.scrape_provider,
                                'scrape_provider': self.scrape_provider})
            except: pass

        window.setProperty('easynews_source_results', json.dumps(self.sources))

        return self.sources

    def _build_display_name(self):
        display = '[B]EASYNEWS[/B]'
        quality = '[I]{}[/I] '.format(self.video_quality) if self.video_quality in ('SD', 'CAM', 'TELE', 'SCR') else '[I][B]{}[/B][/I] '.format(self.video_quality)
        display_name = '[COLOR={0}]{1} | {2} | {3}[/COLOR]'.format(self.provider_color, display.upper(), quality.upper(), self.details.upper())
        if self.show_filenames: display_name += '[COLOR={0}] | [I]{1}[/I][/COLOR]'.format(self.provider_color, clean_file_name(self.file_name).upper())
        return display_name

    def _search_name(self):
        search_title = clean_file_name(self.info.get("title"))
        db_type = self.info.get("db_type")
        year = self.info.get("year")
        years = '%s,%s,%s' % (str(int(year - 1)), year, str(int(year + 1)))
        season = self.info.get("season")
        episode = self.info.get("episode")
        if db_type == 'movie': search_name = '"%s" %s' % (search_title, years)
        else: search_name = '%s S%02dE%02d' % (search_title,  int(season), int(episode))
        return search_name

    def _get_release_quality(self, release_name):
        vid_quality = 'SD'
        try:
            release_name = release_name.upper()
            fmt = re.sub('(.+)(\.|\(|\[|\s)(\d{4}|S\d*E\d*|S\d*)(\.|\)|\]|\s)', '', release_name)
            fmt = re.split('\.|\(|\)|\[|\]|\s|-', fmt)
            fmt = [i.lower() for i in fmt]
            if any(i in ['dvdscr', 'r5', 'r6'] for i in fmt): vid_quality = 'SCR'
            elif any(i in ['camrip', 'tsrip', 'hdcam', 'hd-cam', 'hdts', 'dvdcam', 'dvdts', 'cam', 'telesync', 'ts'] for i in fmt): vid_quality = 'CAM'
            elif any(i in ['tc', 'hdtc', 'telecine', 'tc720p', 'tc720', 'hdtc'] for i in fmt): vid_quality = 'TELE'
            elif '2160p' in fmt: vid_quality = '4K'
            elif '1080p' in fmt: vid_quality = '1080p'
            elif '720p' in fmt: vid_quality = '720p'
        except: pass
        return vid_quality

    def _get_release_details(self):
        name = replace_html_codes(self.file_name)
        size = float(self.size)/1073741824
        fmt = re.sub('(.+)(\.|\(|\[|\s)(\d{4}|S\d*E\d*)(\.|\)|\]|\s)', '', name)
        fmt = re.split('\.|\(|\)|\[|\]|\s|\-', fmt)
        fmt = [x.lower() for x in fmt]
        if '3d' in fmt: q = ' | 3D'
        else: q = ''
        try:
            info = self.video_info.replace('\n','')
            v = re.compile('Video: (.+?),').findall(info)[0]
            a = re.compile('Audio: (.+?), .+?, (.+?),').findall(info)[0]
            info = '%.2f GB%s | %s | %s | %s' % (size, q, v, a[0], a[1])
            info = re.sub('\(.+?\)', '', info)
            info = info.replace('stereo', '2.0')
            info = info.replace('eac3', 'dd+')
            info = info.replace('ac3', 'dd')
            info = info.replace('channels', 'ch')
            info = ' '.join(info.split())
            return info
        except: pass
        try:
            v = a = ''
            if any(i in ['hevc', 'h265', 'x265'] for i in fmt): v = ' | [B]HEVC[/B]'
            if '10bit' in fmt: v += ' | 10BIT'
            if 'imax' in fmt: v += ' | IMAX'
            if 'bluray' in fmt: v += ' | BLURAY'
            if 'web-dl' in fmt: v += ' | WEB-DL'
            if 'web' in fmt: v += ' | WEB-DL'
            if 'hdrip' in fmt: v += ' | HDRip'
            if 'bd-r' in fmt: v += ' | BD-R'
            if 'bd-rip' in fmt: v += ' | BD-RIP'
            if 'bd.r' in fmt: v += ' | BD-R'
            if 'bdr' in fmt: v += ' | BD-R'
            if 'bdrip' in fmt: v += ' | BD-RIP'
            if 'brrip' in fmt: v += ' | BR-RIP'
            if 'xvid' in fmt: v += ' | XVID'
            if 'mp4' in fmt: v += ' | MP4'
            if 'mkv' in fmt: v += ' | MKV'
            if 'avi' in fmt: v += ' | AVI'
            if 'dts' in fmt: a += ' | DTS'
            if 'atmos' in fmt: a += ' | ATMOS'
            if 'truehd' in fmt: a += ' | TRUEHD'
            if 'mp3' in fmt: a += ' | MP3'
            if 'aac' in fmt: a += ' | AAC'
            info = '%.2f GB%s%s%s' % (size, q, v, a)
            return info
        except: pass
        try:
            if any(i in ['hevc', 'h265', 'x265'] for i in fmt): v = 'HEVC'
            else: v = 'h264'
            info = '%.2f GB%s | %s' % (size, q, v)
            return info
        except: pass
        try:
            info = '%.2f GB%s | [I]%s[/I]' % (size, q, name.replace('.', ' '))
            return info
        except: pass

    def to_bytes(self, num, unit):
        unit = unit.upper()
        if unit.endswith('B'): unit = unit[:-1]
        units = ['', 'K', 'M', 'G', 'T', 'P', 'E', 'Z']
        try: mult = pow(1024, units.index(unit))
        except: mult = sys.maxint
        return int(float(num) * mult)

