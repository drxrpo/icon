import xbmc, xbmcgui, xbmcaddon
import sys, os
from urlparse import parse_qsl
from resources.lib.modules.nav_utils import notification
from resources.lib.modules.text import to_unicode, to_utf8
from resources.lib.modules import settings
try: from sqlite3 import dbapi2 as database
except ImportError: from pysqlite2 import dbapi2 as database
# from resources.lib.modules.utils import logger

__addon__ = xbmcaddon.Addon(id='plugin.video.fen')
__addon_profile__ = xbmc.translatePath(__addon__.getAddonInfo('profile'))


class Favourites:
    def __init__(self):
        self.dialog = xbmcgui.Dialog()
        self.fav_database = os.path.join(__addon_profile__, 'favourites.db')
        settings.check_database(self.fav_database)
        params = dict(parse_qsl(sys.argv[2].replace('?','')))
        self.db_type = params.get('db_type')
        self.tmdb_id = params.get('tmdb_id')
        self.title = params.get('title')
        self.name = params.get('name')
        self.id = params.get('_id')
        self.url_dl = params.get('url_dl')
        self.size = params.get('size')

    def add_to_favourites(self):
        try:
            dbcon = database.connect(self.fav_database)
            dbcon.execute("INSERT INTO favourites VALUES (?, ?, ?)", (self.db_type, str(self.tmdb_id), to_unicode(self.title)))
            dbcon.commit()
            dbcon.close()
            notification('[B]%s[/B] added to Favourites' % self.title.upper(), 3500)
        except: notification('[B]%s[/B] already in Favourites' % self.title.upper(), 3500)

    def remove_from_favourites(self):
        if self.db_type == 'audio': self.title = self.tmdb_id.split('<>')[0] 
        dbcon = database.connect(self.fav_database)
        dbcon.execute("DELETE FROM favourites where db_type=? and tmdb_id=?", (self.db_type, str(self.tmdb_id)))
        dbcon.commit()
        dbcon.close()
        xbmc.executebuiltin("Container.Refresh")
        notification('[B]%s[/B] removed from Favourites' % self.title.upper(), 3500)

    def get_favourites(self, db_type):
        dbcon = database.connect(self.fav_database)
        dbcur = dbcon.cursor()
        dbcur.execute('''SELECT tmdb_id, title FROM favourites WHERE db_type=?''', (db_type,))
        result = dbcur.fetchall()
        dbcon.close()
        if db_type == 'audio': result = list(set([i[0] for i in result]))
        else: result = [{'tmdb_id': str(i[0]), 'title': str(to_utf8(i[1]))} for i in result]
        return result

    def clear_favourites(self):
        fl = [('Movie Favourites', 'movie'), ('TV Show Favourites', 'tvshow'), ('Music Favourites', 'audio')]
        fl_choose = self.dialog.select("Choose Favourites to Erase", [i[0] for i in fl])
        if fl_choose < 0: return
        selection = fl[fl_choose]
        self.db_type = selection[1]
        confirm = self.dialog.yesno('Are you sure?', 'Continuing will erase all your [B]%s[/B]' % selection[0])
        if not confirm: return
        dbcon = database.connect(self.fav_database)
        dbcon.execute("DELETE FROM favourites WHERE db_type=?", (self.db_type,))
        dbcon.execute("VACUUM")
        dbcon.commit()
        dbcon.close()
        notification('[B]%s[/B] Erased' % selection[0], 3000)

    def add_to_favourites_audio(self):
        try:
            self.db_type = 'audio'
            self.title = self.dialog.input('Choose Name for New Fen Music Favourite', type=xbmcgui.INPUT_ALPHANUM, defaultt=self.name)
            self.tmdb_id = '%s<>%s<>%s<>%s' % (to_unicode(self.title), self.id, self.url_dl, self.size)
            self.add_to_favourites()
        except: notification('Error Adding Item to Favourites', 3500)

def retrieve_favourites(db_type, page_no, letter, passed_list=[]):
    import ast
    from resources.lib.modules.nav_utils import paginate_list
    from resources.lib.modules.utils import title_key
    limit = 40
    if db_type == 'audio': return Favourites().get_favourites(db_type)
    if not passed_list:
        data = Favourites().get_favourites(db_type)
        data = sorted(data, key=lambda k: title_key(k['title']))
        original_list = [{'media_id': i['tmdb_id'], 'title': i['title']} for i in data]
    else: original_list = ast.literal_eval(passed_list)
    paginated_list, total_pages = paginate_list(original_list, page_no, letter, limit)
    return paginated_list, original_list, total_pages, limit


