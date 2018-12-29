# -*- coding: utf-8 -*-
#modes 500-600
import base64 
import byb_modules as BYB 
import byb_api as BYBAPI 
import _Edit
import koding
import re

from libs._addon import *
from libs._common import *

Dolog = koding.dolog
#string = '<externallink>tmdb=(movie|tv|company*|**list):list_id=(**list id|*company id):list_type=(latest|popular|nowplaying|toprated|upcoming|movies*|tv*):=list</externallink>'
def tmdb_list(url):
	imdb = ''
	debrid = False
	ApiKey = apikey()
	Page = '1'
	PageTotal = '0'
	if not 'page=' in url:
		ListAssign = url.replace('=:','=none:')
		ListAssignItems =re.compile( r'tmdb=(.+?):list_id=(.+?):list_type=(.+?):=list').findall(ListAssign)
		for ListHeader,ListId,ListType in ListAssignItems:
			if ListHeader.lower() == 'list':
				BYBAPI.tmdb_list_get_items(ApiKey,ListId)
			elif ListHeader.lower() == 'company':
				BYBAPI.tmdb_company_get_results(ApiKey,ListId,ListType)
				Page,PageTotal = BYBAPI.tmdb_company_get_results_page_counter(ApiKey,ListId,ListType)
			elif ListHeader == 'movie' or ListHeader == 'tv':
				BYBAPI.tmdb_movietv_get_lists(ApiKey,ListHeader,ListType)
				Page,PageTotal = BYBAPI.tmdb_movietv_get_lists_page_counter(ApiKey,ListHeader,ListType)
	elif 'page=' in url:
		ListAssign = url.replace('=:','=none:')
		ListAssignItems =re.compile( r'tmdb=(.+?):list_id=(.+?):list_type=(.+?):page=(.+?):=list').findall(ListAssign)
		for ListHeader,ListId,ListType,Page in ListAssignItems:
			if ListHeader.lower() == 'list':
				BYBAPI.tmdb_list_get_items(ApiKey,ListId)
			elif ListHeader.lower() == 'company':
				BYBAPI.tmdb_company_get_results(ApiKey,ListId,ListType,Page)
				Page,PageTotal = BYBAPI.tmdb_company_get_results_page_counter(ApiKey,ListId,ListType,Page)
			elif ListHeader == 'movie' or ListHeader == 'tv':
				BYBAPI.tmdb_movietv_get_lists(ApiKey,ListHeader,ListType,Page)
				Page,PageTotal = BYBAPI.tmdb_movietv_get_lists_page_counter(ApiKey,ListHeader,ListType,Page)
	for items in BYBAPI.Details_list:
		name = items.get('title','Title Missing')
		date = items.get('release_date','')
		Year = date.split('-')[0]
		MediaType = items.get('mediatype','').lower()
		Dolog(MediaType,line_info=True)
		TmdbDataString = ''
		if _Edit.TMDBMovieList == 'search_addon':
			mode = 404
			TmdbDataString = 'tmdb={}'.format(items.get('ID',''))
		elif _Edit.TMDBMovieList == 'search_internet':
			mode = 600
			if MediaType == 'movie' or ListHeader == 'movie' or ListType == 'movies': 
				TmdbDataString = '#search=movies:name={}:year={}:imdb={}:debrid={}'.format(name.encode('utf-8', 'ignore').strip(':'),Year,imdb,debrid)
			elif MediaType == 'tv' or ListHeader == 'tv':
				TmdbDataString = '#search' 
		Name = name if len(name) > 0 else 'Name Missing'
		Name = '{}'.format(Name.encode('utf-8', 'ignore').strip(':'))
		BYB.addDir(ChannelColor(Name),TmdbDataString,mode,items.get('poster_path',icon_tmdb),items.get('backdrop_path',fanart_tmdb),items.get('overview','').encode('utf-8', 'ignore'),items.get('Genres',''),date.encode('utf-8'),'')
	if int(Page)+1 <= int(PageTotal):
		NextPage =  str(int(Page) + 1)
		BYB.addDir(ChannelColor('Next Page {}'.format(NextPage)),'tmdb={}:list_id={}:list_type={}:page={}:=list'.format(ListHeader,ListId,ListType,NextPage),500,icon_nextpage,addon_fanart,'Next Page {} of {}'.format(NextPage,PageTotal),'','','')


def apikey():
	if _Edit.UseTMDB :
	    if _Edit.TMDB_api != '':
	        TMDB_api = base64.b64decode(_Edit.TMDB_api)
	    elif _Edit.TMDB_api == '':
	        TMDB_api = setting('tmdb_key')
	    if len(_Edit.TMDB_api) > 0 and len(setting('tmdb_key')) > 0:
	        TMDB_api = setting('tmdb_key')
	else:
		Dolog('Check _Edit.py settings of UseTMDB',line_info=True)
		TMDB_api = None 
	return TMDB_api
