import xbmcaddon, xbmcgui
import re
import json
from datetime import timedelta
from resources.lib.modules.furk_api import FurkAPI
from resources.lib.modules import fen_cache
from resources.lib.modules.utils import clean_file_name, replace_html_codes
from resources.lib.modules import settings
# from resources.lib.modules.utils import logger

Furk = FurkAPI()
__addon__ = xbmcaddon.Addon(id='plugin.video.fen')
window = xbmcgui.Window(10000)

class FurkSource:
    def __init__(self):
        self.scrape_provider = 'furk'
        self.sources = []
        self.provider_color = settings.provider_color(self.scrape_provider)
        self.show_filenames = settings.show_filenames()
        self.furk_limit = int(__addon__.getSetting('furk.limit'))
        self.max_gb = int(__addon__.getSetting('furk_maxgb'))

    def results(self, info):
        self.info = info
        self.search_name = self._search_name()
        files = Furk.search(self.search_name)
        if not files: return self.sources
        self.active_downloads = self.get_active_downloads()
        cached_files = [i for i in files if i.get('type') == 'video' and i.get('is_ready') == '1'][0:self.furk_limit]
        uncached_files = [i for i in files if i not in cached_files]
        for i in cached_files:
            try:
                self.file_name = i['name']
                self.file_id = i['id']
                self.files_num_video = i['files_num_video']
                self.size = int(i['size'])
                if not int(self.files_num_video) > 3:
                    if float(self.size)/1073741824 > self.max_gb:
                        continue
                self.file_dl = i['url_dl']
                self.video_info = i['video_info']
                self.details = self._get_release_details()
                self.video_quality = self._get_release_quality(self.file_name, self.file_dl)
                self.display_name = self._build_display_name()
                self.sources.append({'name': self.file_name,
                                'display_name': self.display_name,
                                'label': self.display_name,
                                'quality': self.video_quality,
                                'size': self.size,
                                'url_dl': self.file_dl,
                                'id': self.file_id,
                                'local': False,
                                'direct': True,
                                'source': self.scrape_provider,
                                'scrape_provider': self.scrape_provider})
            except: pass
        for i in uncached_files:
            try:
                self.file_name = i['name']
                self.info_hash = i['info_hash']
                self.file_id = self.info_hash
                try: self.size = int(i['size'])
                except: self.size = 0
                self.file_dl = self.info_hash
                self.active_download = True if self.info_hash in self.active_downloads else False
                self.details = '%.2f GB' % (float(self.size)/1073741824)
                self.video_quality = self._get_release_quality(self.file_name, self.file_dl)
                self.display_name = self._build_display_name(uncached=True)
                self.sources.append({'name': self.file_name,
                                'display_name': self.display_name,
                                'label': self.display_name,
                                'quality': self.video_quality,
                                'size': self.size,
                                'url_dl': self.file_dl,
                                'id': self.file_id,
                                'local': False,
                                'direct': True,
                                'uncached': True,
                                'source': self.scrape_provider,
                                'scrape_provider': self.scrape_provider})
            except: pass

        window.setProperty('furk_source_results', json.dumps([i for i in self.sources if not 'uncached' in i]))

        return self.sources

    def get_active_downloads(self):
        _cache = fen_cache.FenCache()
        cache = _cache.get('furk_active_downloads')
        if cache != None: result = cache
        else:
            active_downloads = Furk.file_get_active()
            result = [i['info_hash'] for i in active_downloads]
            _cache.set('furk_active_downloads', result, expiration=timedelta(hours=1))
        return result

    def _search_name(self):
        search_title = clean_file_name(self.info.get("title"))
        search_title = search_title.replace(' ', '+')
        db_type = self.info.get("db_type")
        year = self.info.get("year")
        years = '%s+|+%s+|+%s' % (str(int(year - 1)), year, str(int(year + 1)))
        season = self.info.get("season")
        episode = self.info.get("episode")
        if db_type == 'movie': search_name = '@name+%s+%s' % (search_title, years)
        else:
            queries = self._seas_ep_query_list(season, episode)
            search_name = '@name+%s+@files+%s+|+%s+|+%s' % (search_title, queries[0], queries[1], queries[2])
        return search_name

    def _build_display_name(self, uncached=False):
        if uncached:
            color = 'green' if self.active_download else 'red'
            display = '[B]FURK[/B] | %s' % ('[COLOR=green][B]ACTIVE[/B][/COLOR]' if self.active_download else '[COLOR=red][B]UNCACHED[/B][/COLOR]')
        else: display = '[B]FURK[/B] | PACK [B](x%02d)[/B]' % int(self.files_num_video) if int(self.files_num_video) > 3 else '[B]FURK[/B] | SINGLE'
        quality = '[I]{}[/I] '.format(self.video_quality) if self.video_quality in ('SD', 'CAM', 'TELE', 'SCR') else '[I][B]{}[/B][/I] '.format(self.video_quality)
        if uncached: return '[COLOR={0}]{1} | {2} | {3} | [COLOR={4}][I]{5}[/I][/COLOR][/COLOR]'.format(self.provider_color, display.upper().replace('RED', 'red').replace('GREEN', 'green'), quality.upper(), self.details.upper(), color, clean_file_name(self.file_name).upper().replace('RED', 'red').replace('GREEN', 'green')).replace(self.provider_color.upper(), self.provider_color)
        display_name = '[COLOR={0}]{1} | {2} | {3}[/COLOR]'.format(self.provider_color, display.upper().replace('RED', 'red').replace('GREEN', 'green'), quality.upper(), self.details.upper()).replace(self.provider_color.upper(), self.provider_color)
        if self.show_filenames: display_name += '[COLOR={0}] | [I]{1}[/I][/COLOR]'.format(self.provider_color, clean_file_name(self.file_name).upper())
        return display_name

    def _seas_ep_query_list(self, season, episode):
        return ['s%02de%02d' % (int(season), int(episode)), '%dx%02d' % (int(season), int(episode)),
                '%02dx%02d' % (int(season), int(episode))]

    def _get_release_quality(self, release_name, release_link=None):
        if release_name is None: return
        try: release_name = release_name
        except: pass
        try:
            vid_quality = None
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
            elif 'brrip' in fmt: vid_quality = '720p'
            if not vid_quality:
                if release_link:
                    release_link = release_link.lower()
                    try: release_link = release_link
                    except: pass
                    if any(i in ['dvdscr', 'r5', 'r6'] for i in release_link): vid_quality = 'SCR'
                    elif any(i in ['camrip', 'tsrip', 'hdcam', 'hdts', 'dvdcam', 'dvdts', 'cam', 'telesync', 'ts'] for i in release_link): vid_quality = 'CAM'
                    elif any(i in ['tc', 'hdtc', 'telecine', 'tc720p', 'tc720', 'hdtc'] for i in release_link): vid_quality = 'TELE'
                    elif '2160' in release_link: vid_quality = '4K'
                    elif '1080' in release_link: vid_quality = '1080p'
                    elif '720' in release_link: vid_quality = '720p'
                    elif '.hd' in release_link: vid_quality = 'SD'
                    else: vid_quality = 'SD'
                else: vid_quality = 'SD'
            return vid_quality
        except:
            return 'SD'

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
            if any(i in ['hevc', 'h265', 'x265'] for i in fmt): v = '[B]HEVC[/B]'
            else: v = 'h264'
            info = '%.2f GB%s | %s' % (size, q, v)
            return info
        except: pass
        try:
            info = '%.2f GB%s | [I]%s[/I]' % (size, q, name.replace('.', ' '))
            return info
        except: pass




