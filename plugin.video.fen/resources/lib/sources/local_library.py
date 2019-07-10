
import xbmc, xbmcvfs, xbmcgui
import json
from resources.lib.modules.utils import clean_file_name, to_utf8
from resources.lib.modules import settings
# from resources.lib.modules.utils import logger

window = xbmcgui.Window(10000)

class LocalLibrarySource:
    def __init__(self):
        self.scrape_provider = 'local'
        self.sources = []
        self.provider_color = settings.provider_color(self.scrape_provider)
        self.show_filenames = settings.show_filenames()

    def results(self, info):
        self.info = info
        self.db_type = self.info.get("db_type")
        self.title = self.info.get("title")
        self.year = self.info.get("year")
        self.season = self.info.get("season")
        self.episode = self.info.get("episode")
        self.db_info = self._get_library_video(self.db_type, self.title, self.year, self.season, self.episode)
        if not self.db_info: return self.sources
        self.file_name = self.db_info.get("name")
        self.file_id = self.db_info.get("file_id")
        self.size = ''
        self.file_dl = self.db_info.get("file_id")
        self.video_quality = self.db_info.get("quality")
        self.details = self.db_info.get("details")
        self.display_name = self._build_display_name()
        self.sources.append({'name': self.file_name,
                        'display_name': self.display_name,
                        'label': self.display_name,
                        'quality': self.video_quality,
                        'size': self.size,
                        'url_dl': self.file_dl,
                        'url': self.file_dl,
                        'id': self.file_id,
                        'local': True,
                        'direct': True,
                        'source': self.scrape_provider,
                        'scrape_provider': self.scrape_provider})

        window.setProperty('local_source_results', json.dumps(self.sources))
        
        return self.sources

    def _get_library_video(self, db_type, title, year, season=None, episode=None):
        try:
            name = None
            years = (str(year), str(int(year)+1), str(int(year)-1))
            if db_type == 'movie':
                r = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.GetMovies", "params": {"filter":{"or": [{"field": "year", "operator": "is", "value": "%s"}, {"field": "year", "operator": "is", "value": "%s"}, {"field": "year", "operator": "is", "value": "%s"}]}, "properties": ["imdbnumber", "title", "originaltitle", "file"]}, "id": 1}' % years)
                r = to_utf8(r)
                r = json.loads(r)['result']['movies']
                try:
                    r = [i for i in r if clean_file_name(title).lower() in clean_file_name(to_utf8(i['title'])).lower()]
                    r = [i for i in r if not to_utf8(i['file']).endswith('.strm')][0]
                except: return None
                r = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.GetMovieDetails", "params": {"properties": ["streamdetails", "file"], "movieid": %s }, "id": 1}' % str(r['movieid']))
                r = to_utf8(r)
                r = json.loads(r)['result']['moviedetails']
            else:
                r = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.GetTVShows", "params": {"filter":{"or": [{"field": "year", "operator": "is", "value": "%s"}, {"field": "year", "operator": "is", "value": "%s"}, {"field": "year", "operator": "is", "value": "%s"}]}, "properties": ["title"]}, "id": 1}' % years)
                r = to_utf8(r)
                r = json.loads(r)['result']['tvshows']
                try:
                    r = [i for i in r if clean_file_name(title).lower() in (clean_file_name(to_utf8(i['title'])).lower() if not ' (' in to_utf8(i['title']) else clean_file_name(to_utf8(i['title'])).lower().split(' (')[0])][0]
                except: return None

                r = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.GetEpisodes", "params": {"filter":{"and": [{"field": "season", "operator": "is", "value": "%s"}, {"field": "episode", "operator": "is", "value": "%s"}]}, "properties": ["file"], "tvshowid": %s }, "id": 1}' % (str(season), str(episode), str(r['tvshowid'])))
                r = to_utf8(r)
                r = json.loads(r)['result']['episodes']
                try:
                    r = [i for i in r if not to_utf8(i['file']).endswith('.strm')][0]
                except:
                    return None
                r = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "VideoLibrary.GetEpisodeDetails", "params": {"properties": ["streamdetails", "file"], "episodeid": %s }, "id": 1}' % str(r['episodeid']))
                r = to_utf8(r)
                r = json.loads(r)['result']['episodedetails']
            url = r['file'].encode('utf-8')
            try: name = url.split('/')[-1:][0]
            except: name = None
            if not name:
                try: name = url.split('\\')[-1:][0]
                except: name = None
            if not name:
                name = title
            try: quality = int(r['streamdetails']['video'][0]['width'])
            except: quality = -1
            if quality > 1920: quality = '4K'
            if quality >= 1920: quality = '1080p'
            if 1280 <= quality < 1900: quality = '720p'
            if quality < 1280: quality = 'SD'
            release_details = []
            try:
                f = xbmcvfs.File(url) ; s = f.size() ; f.close()
                s = '%.2f GB' % (float(s)/1024/1024/1024)
                release_details.append(s)
            except: pass
            try:
                c = r['streamdetails']['video'][0]['codec']
                if c == 'avc1': c = 'h264'
                release_details.append(c)
            except: pass
            try:
                ac = r['streamdetails']['audio'][0]['codec']
                if ac == 'dca': ac = 'dts'
                if ac == 'dtshd_ma': ac = 'dts-hd ma'
                release_details.append(ac)
            except: pass
            try:
                ach = r['streamdetails']['audio'][0]['channels']
                if ach == 1: ach = 'mono'
                if ach == 2: ach = '2.0'
                if ach == 6: ach = '5.1'
                if ach == 8: ach = '7.1'
                release_details.append(ach)
            except: pass
            release_details = ' | '.join(release_details)
            release_details = release_details.encode('utf-8')
            return {'name': name, 'file_id': url, 'quality': quality, 'details': release_details}
        except: pass

    def _build_display_name(self):
        quality = '[I]{}[/I] '.format(self.video_quality) if self.video_quality in ('HQ', 'CAM', 'TELE', 'SCR') else '[B][I]{}[/I][/B] '.format(self.video_quality)
        details = self.details
        display = '[B]LOCAL[/B]'
        display_name = '[COLOR={0}]{1} | {2} | {3}[/COLOR]'.format(self.provider_color, display.upper(), quality.upper(), details.upper())
        if self.show_filenames: display_name += '[COLOR={0}] | [I]{1}[/I][/COLOR]'.format(self.provider_color, clean_file_name(self.file_name).upper())
        return display_name
