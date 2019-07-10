# -*- coding: utf-8 -*-
import xbmc, xbmcplugin, xbmcgui
import sys
import urllib
import json
from urlparse import parse_qsl
from resources.lib.modules.indicators_bookmarks import detect_bookmark, erase_bookmark
from resources.lib.modules.nav_utils import hide_busy_dialog, close_all_dialog
from resources.lib.modules.utils import sec2time
import settings
# from resources.lib.modules.utils import logger

__handle__ = int(sys.argv[1])
window = xbmcgui.Window(10000)

class FenPlayer(xbmc.Player):
    def __init__ (self):
        xbmc.Player.__init__(self)
        self.set_resume = settings.set_resume()
        self.set_watched = settings.set_watched()
        self.autoplay_nextep = settings.autoplay_next_episode()
        self.nextep_threshold = settings.nextep_threshold()
        self.nextep_info = None
        self.delete_nextep_playcount = True

    def run(self, url=None):
        params = dict(parse_qsl(sys.argv[2].replace('?','')))
        rootname = params.get('rootname', '')
        try:
            if rootname == 'nill':
                url = urllib.unquote(params.get("url"))
                self.play(url)
                return
            url = url if url else params.get("url") if 'url' in params else None
            url = urllib.unquote(url)
            if not url: return
            self.meta = json.loads(window.getProperty('fen_media_meta'))
            rootname = self.meta['rootname'] if 'rootname' in self.meta else ''
            bookmark = self.bookmarkChoice()
            if bookmark == -1: return
            self.meta.update({'url': url, 'bookmark': bookmark})
            listitem = xbmcgui.ListItem(path=url)
            try:
                listitem.setProperty('StartPercent', str(self.meta.get('bookmark')))
                listitem.setArt({'poster': self.meta.get('poster'), 'fanart': self.meta.get('fanart'),
                                'banner': self.meta.get('banner'), 'clearlogo': self.meta.get('clearlogo'),
                                'landscape': self.meta.get('landscape')})
                if self.meta['vid_type'] == 'movie':
                    listitem.setInfo(
                        'video', {'mediatype': 'movie', 'trailer': str(self.meta['trailer']),
                        'title': self.meta['title'], 'size': '0', 'duration': self.meta['duration'],
                        'plot': self.meta['plot'], 'rating': self.meta['rating'], 'premiered': self.meta['premiered'],
                        'studio': self.meta['studio'],'year': self.meta['year'], 'genre': self.meta['genre'],
                        'tagline': self.meta['tagline'], 'code': self.meta['imdb_id'], 'imdbnumber': self.meta['imdb_id'],
                        'director': self.meta['director'], 'writer': self.meta['writer'], 'votes': self.meta['votes']})
                elif self.meta['vid_type'] == 'episode':
                    listitem.setInfo(
                        'video', {'mediatype': 'episode', 'trailer': str(self.meta['trailer']), 'title': self.meta['ep_name'],
                        'tvshowtitle': self.meta['title'], 'size': '0', 'plot': self.meta['plot'], 'year': self.meta['year'],
                        'premiered': self.meta['premiered'], 'genre': self.meta['genre'], 'season': int(self.meta['season']),
                        'episode': int(self.meta['episode']), 'duration': str(self.meta['duration']), 'rating': self.meta['rating']})
            except: pass
            try:
                self.play(url, listitem)
            except:
                xbmcplugin.setResolvedUrl(__handle__, True, listitem)
            self.monitor()
        except: return

    def bookmarkChoice(self):
        season = self.meta.get('season', '')
        episode = self.meta.get('episode', '')
        if season == 0: season = ''
        if episode == 0: episode = ''
        bookmark = 0
        try: resume_point, curr_time = detect_bookmark(self.meta['vid_type'], self.meta['media_id'], season, episode)
        except: resume_point = 0
        if resume_point > 0:
            percent = resume_point
            raw_time = float(curr_time)
            time = sec2time(raw_time, n_msec=0)
            bookmark = self.getResumeStatus(time, percent, bookmark, self.meta.get('from_library', None))
            if bookmark == 0: erase_bookmark(self.meta['vid_type'], self.meta['media_id'], season, episode)
        return bookmark

    def getResumeStatus(self, time, percent, bookmark, from_library):
        if settings.auto_resume(): return percent
        dialog = xbmcgui.Dialog()
        xbmc.sleep(600)
        choice = dialog.contextmenu(['Resume from [B]%s[/B]' % time, 'Start from Beginning'])
        return percent if choice == 0 else bookmark if choice == 1 else -1

    def monitor(self):
        self.library_setting = 'library' if 'from_library' in self.meta else None
        self.autoplay_next_episode = True if self.meta['vid_type'] == 'episode' and self.autoplay_nextep else False
        while not self.isPlayingVideo():
            xbmc.sleep(100)
        close_all_dialog()
        while self.isPlayingVideo():
            try:
                self.total_time = self.getTotalTime()
                self.curr_time = self.getTime()
                xbmc.sleep(100)
                if self.autoplay_next_episode:
                    current_point = round(float(self.curr_time/self.total_time*100),1)
                    if current_point >= self.nextep_threshold:
                        if not self.nextep_info:
                            self.nextEpPrep()
                        else: pass
            except: pass
        self.mediaWatchedMarker()

    def mediaWatchedMarker(self):
        try:
            if self.delete_nextep_playcount: window.clearProperty('current_autoplay_next_number')
            resume_point = round(float(self.curr_time/self.total_time*100),1)
            from_search = 'true'
            xbmc.sleep(3000)
            if self.set_resume < resume_point < self.set_watched:
                from resources.lib.modules.indicators_bookmarks import set_bookmark
                set_bookmark(self.meta['vid_type'], self.meta['media_id'], self.curr_time, self.total_time, self.meta.get('season', ''), self.meta.get('episode', ''), from_search)
            elif resume_point > self.set_watched:
                if self.meta['vid_type'] == 'movie':
                    from resources.lib.modules.indicators_bookmarks import mark_movie_as_watched_unwatched
                    watched_function = mark_movie_as_watched_unwatched
                    watched_params = {"mode": "mark_movie_as_watched_unwatched", "action": 'mark_as_watched',
                    "media_id": self.meta['media_id'], "title": self.meta['title'], "year": self.meta['year'],
                    "from_search": from_search}
                else:
                    from resources.lib.modules.indicators_bookmarks import mark_episode_as_watched_unwatched
                    watched_function = mark_episode_as_watched_unwatched
                    watched_params = {"mode": "mark_episode_as_watched_unwatched", "action": "mark_as_watched",
                    "season": self.meta['season'], "episode": self.meta['episode'], "media_id": self.meta['media_id'],
                    "title": self.meta['title'], "year": self.meta['year'], "imdb_id": self.meta['imdb_id'],
                    "tvdb_id": self.meta["tvdb_id"], "from_search": from_search}
                watched_function(watched_params)
            else: pass
        except: pass
        return

    def nextEpPrep(self):
        auto_nextep_limit_reached = False
        autoplay_next_check_threshold = settings.autoplay_next_check_threshold()
        try: current_number = int(window.getProperty('current_autoplay_next_number'))
        except: current_number = 1
        if autoplay_next_check_threshold != 0:
            if current_number == autoplay_next_check_threshold:
                auto_nextep_limit_reached = True
                continue_playing = xbmcgui.Dialog().yesno('Fen Next Episode', '[B]Are you still watching %s?[/B]' % self.meta['title'], '', '', 'Not Watching', 'Still Watching', 10000)
                if not continue_playing == 1:
                    from resources.lib.modules.nav_utils import notification
                    notification('Fen Next Episode Cancelled', 6000)
                    self.nextep_info = {'pass': True}
        if not self.nextep_info:
            from resources.lib.modules.next_episode import nextep_playback_info, nextep_play
            self.nextep_info = nextep_playback_info(self.meta['tmdb_id'], int(self.meta['season']), int(self.meta['episode']), self.library_setting)
            if not self.nextep_info.get('pass', False):
                if not auto_nextep_limit_reached: self.delete_nextep_playcount = False
                window.setProperty('current_autoplay_next_number', str(current_number+1))
                nextep_play(self.nextep_info)

    # def onAVStarted(self):
    #     close_all_dialog()

    # def onPlayBackStarted(self):
    #     close_all_dialog()

    def playAudioAlbum(self, t_files=None, name=None, from_seperate=False):
        import os
        import xbmcaddon
        from resources.lib.modules.utils import clean_file_name, batch_replace, to_utf8
        from resources.lib.modules.nav_utils import setView
        __addon_id__ = 'plugin.video.fen'
        __addon__ = xbmcaddon.Addon(id=__addon_id__)
        __handle__ = int(sys.argv[1])
        addon_dir = xbmc.translatePath(__addon__.getAddonInfo('path'))
        icon_directory = settings.get_theme()
        default_furk_icon = os.path.join(icon_directory, 'furk.png')
        formats = ('.3gp', ''), ('.aac', ''), ('.flac', ''), ('.m4a', ''), ('.mp3', ''), \
        ('.ogg', ''), ('.raw', ''), ('.wav', ''), ('.wma', ''), ('.webm', ''), ('.ra', ''), ('.rm', '')
        params = dict(parse_qsl(sys.argv[2].replace('?','')))
        furk_files_list = []
        playlist = xbmc.PlayList(xbmc.PLAYLIST_MUSIC)
        playlist.clear()
        if from_seperate: t_files = [i for i in t_files if clean_file_name(i['path']) == params.get('item_path')]
        for item in t_files:
            try:
                name = item['path'] if not name else name
                if not 'audio' in item['ct']: continue
                url = item['url_dl']
                track_name = clean_file_name(batch_replace(to_utf8(item['name']), formats))
                listitem = xbmcgui.ListItem(track_name)
                listitem.setThumbnailImage(default_furk_icon)
                listitem.setInfo(type='music',infoLabels={'title': track_name, 'size': int(item['size']), 'album': clean_file_name(batch_replace(to_utf8(name), formats)),'duration': item['length']})
                listitem.setProperty('mimetype', 'audio/mpeg')
                playlist.add(url, listitem)
                if from_seperate: furk_files_list.append((url, listitem, False))
            except: pass
        self.play(playlist)
        if from_seperate:
            xbmcplugin.addDirectoryItems(__handle__, furk_files_list, len(furk_files_list))
            setView('view.furk_files')
            xbmcplugin.endOfDirectory(__handle__)





