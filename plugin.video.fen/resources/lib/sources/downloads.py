
import xbmcvfs, xbmcgui
import re
import json
import os
import urlparse
from resources.lib.modules.utils import clean_file_name, replace_html_codes
from resources.lib.modules import settings
# from resources.lib.modules.utils import logger

window = xbmcgui.Window(10000)

class DownloadsSource:
    def __init__(self):
        self.scrape_provider = 'downloads'
        self.sources = []
        self.provider_color = settings.provider_color(self.scrape_provider)
        self.show_filenames = settings.show_filenames()

    def results(self, info):
        self.info = info
        self.db_type = self.info.get("db_type")
        self.download_path = settings.download_directory(self.db_type)
        self.title = self.info.get("title")
        self.year = self.info.get("year")
        self.season = self.info.get("season")
        self.episode = self.info.get("episode")
        self.file_dl = self._get_video(self.db_type, self.title, self.year, self.season, self.episode)
        if not self.file_dl: return self.sources
        self.size = self._get_size(self.file_dl)
        self.details = self._get_release_details()
        self.video_quality = self._get_release_quality(self.file_dl)
        self.display_name = self._build_display_name()
        self.sources.append({'name': self.file_name,
                        'display_name': self.display_name,
                        'label': self.display_name,
                        'quality': self.video_quality,
                        'size': self.size,
                        'url_dl': self.file_dl,
                        'id': self.file_dl,
                        'downloads': True,
                        'direct': True,
                        'source': self.scrape_provider,
                        'scrape_provider': self.scrape_provider})

        window.setProperty('downloads_source_results', json.dumps(self.sources))
        
        return self.sources

    def _get_video(self, db_type, title, year, season=None, episode=None):
        try:
            file_fetcher = self._fetch_movie if self.db_type == 'movie' else self._fetch_episode
            match = None
            try:
                dirs, files = xbmcvfs.listdir(self.download_path)
                for item in dirs:
                    match = self._match_media(item)
                    if match:
                        break
            except: pass
            if not match: return None
            result = file_fetcher(match)
            return result
        except: pass

    def _match_media(self, item):
        if clean_file_name(self.title).lower() in clean_file_name(item).lower():
            if self.db_type == 'movie':
                if item.split('(')[1][:4] in self._year_query_list():
                    return item
            else:
                return item
        else:
            return None

    def _fetch_movie(self, item):
        match = None
        movie_path = os.path.join(self.download_path, item)
        dirs, files = xbmcvfs.listdir(movie_path)
        for item in files:
            ext = os.path.splitext(urlparse.urlparse(item).path)[1][1:]
            if ext in ['mp4', 'mkv', 'flv', 'avi', 'mpg']:
                match = item
                if match:
                    self.file_name = match
                    break
        if not match: return None
        url_path = os.path.join(movie_path, match)
        return url_path

    def _fetch_episode(self, item):
        match = None
        season_queries = self._season_query_list()
        season_path = os.path.join(self.download_path, item)
        dirs, files = xbmcvfs.listdir(season_path)
        for item in dirs:
            if item.lower() in season_queries:
                match = item
                if match:
                    break
        if not match: return None
        episode_path = os.path.join(season_path, match)
        queries = self._episode_query_list()
        match = None
        dirs, files = xbmcvfs.listdir(episode_path)
        for item in files:
            ext = os.path.splitext(urlparse.urlparse(item).path)[1][1:]
            if ext.lower() in ['mp4', 'mkv', 'flv', 'avi', 'mpg']:
                if any(i in item.lower() for i in queries):
                    match = item
                    if match:
                        self.file_name = match
                        break
        if not match: return None
        url_path = os.path.join(episode_path, match)
        return url_path

    def _get_size(self, file):
        f = xbmcvfs.File(file)
        size = f.size()
        return size

    def _year_query_list(self):
        return (str(self.year), str(int(self.year)+1), str(int(self.year)-1))

    def _season_query_list(self):
        return ['season %02d' % int(self.season), 'season %s' % self.season]

    def _episode_query_list(self):
        return ['s%02de%02d' % (int(self.season), int(self.episode)), '%dx%02d' % (int(self.season), int(self.episode)),
                '%02dx%02d' % (int(self.season), int(self.episode))]

    def _build_display_name(self):
        quality = '[I]{}[/I] '.format(self.video_quality) if self.video_quality in ('HQ', 'CAM', 'TELE', 'SCR') else '[B][I]{}[/I][/B] '.format(self.video_quality)
        details = self.details
        display = '[B]DOWNLOADS[/B]'
        display_name = '[COLOR={0}]{1} | {2} | {3}[/COLOR]'.format(self.provider_color, display.upper(), quality.upper(), details.upper())
        if self.show_filenames: display_name += '[COLOR={0}] | [I]{1}[/I][/COLOR]'.format(self.provider_color, clean_file_name(self.file_name).upper())
        return display_name

    def _get_release_quality(self, release_name):
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
                vid_quality = 'SD'
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
