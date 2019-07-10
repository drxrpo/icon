
class DefaultMenus:
    
    def RootList(self):
        return [
            {
                "iconImage": "movies.png", 
                "mode": "navigator.main",
                "action": "MovieList",
                "name": "Movies", 
                "foldername": "Movies",
                "info": "Access Fen Movie Menus."
            }, 
            {
                "iconImage": "tv.png", 
                "mode": "navigator.main",
                "action": "TVShowList",
                "name": "TV Shows", 
                "foldername": "TV Shows",
                "info": "Access Fen TV Show Menus."
            }, 
            {
                "iconImage": "genre_music.png", 
                "mode": "navigator.main",
                "action": "AudioList",
                "name": "Music", 
                "foldername": "Music",
                "info": "Access Fen Music Menus."
            }, 
            {
                "iconImage": "search.png", 
                "mode": "navigator.search", 
                "name": "Search", 
                "foldername": "Search",
                "info": "Access Search Menus for Movies - TV Shows - Music - Furk - Easynews."
            }, 
            {
                "iconImage": "furk.png", 
                "mode": "navigator.furk", 
                "name": "Furk", 
                "foldername": "Furk",
                "info": "Access Your Furk files and other information relating to your Furk account."
            }, 
            {
                "iconImage": "easynews.png", 
                "mode": "navigator.easynews", 
                "name": "Easynews", 
                "foldername": "Easynews",
                "info": "Search Easynews and get information relating to your Easynews account."
            }, 
            {
                "iconImage": "trakt.png", 
                "mode": "navigator.my_trakt_content", 
                "name": "My Trakt Lists", 
                "foldername": "My Trakt Lists",
                "info": "Access your Trakt Lists and Watchlists. You must be logged into Trakt to view your Lists."
            }, 
            {
                "iconImage": "favourites.png", 
                "mode": "navigator.favourites", 
                "name": "Favourites", 
                "foldername": "Favourites",
                "info": "Access Fen Movie - TV Show - Audio Favourites."
            }, 
            {
                "iconImage": "library.png", 
                "mode": "navigator.subscriptions", 
                "name": "Subscriptions", 
                "foldername": "Subscriptions Root",
                "info": "Access Fen Movie and TV Show Subscriptions Items."
            }, 
            {
                "iconImage": "watched_1.png", 
                "mode": "navigator.watched", 
                "name": "Watched", 
                "foldername": "Watched",
                "info": "Access Fen Watched Items for Movies and TV Shows that have been fully watched in Fen."
            }, 
            {
                "iconImage": "player.png", 
                "mode": "navigator.in_progress", 
                "name": "In Progress", 
                "foldername": "In Progress",
                "info": "Access Fen In Progress Menus for Movies and TV Show Episodes currently In Progress."
            }, 
            {
                "iconImage": "downloads.png", 
                "mode": "navigator.downloads", 
                "name": "Downloads", 
                "foldername": "Fen Downloads",
                "info": "Access your Fen Downloads folder."
            }, 
            {
                "iconImage": "library_kodi.png", 
                "mode": "navigator.kodi_library", 
                "name": "Kodi Library", 
                "foldername": "Kodi Library Root",
                "info": "Access your Kodi Library for Movies and TV Shows."
            }, 
            {
                "iconImage": "settings2.png", 
                "mode": "navigator.tools", 
                "name": "Tools", 
                "foldername": "Tools",
                "info": "Access Fen Tools to change some settings and set some account details such as Trakt and TMDb. Also set view modes and clear some Fen settings such as Favourites and Subscriptions Items."
            }, 
            {
                "iconImage": "settings.png", 
                "mode": "navigator.settings", 
                "name": "Settings", 
                "foldername": "Settings",
                "info": "Access Fen Settings from within the add-on."
            }
        ]

    def MovieList(self):
        return [
            {
                "name": "Trending", 
                "iconImage": "trending.png", 
                "foldername": "Trending", 
                "mode": "build_movie_list", 
                "action": "trakt_movies_trending",
                "info": "Browse Trending Movies."
            }, 
            {
                "name": "Popular", 
                "iconImage": "popular.png", 
                "foldername": "Popular", 
                "mode": "build_movie_list", 
                "action": "tmdb_movies_popular",
                "info": "Browse Popular Movies."
            }, 
            {
                "action": "tmdb_movies_premieres", 
                "iconImage": "fresh.png", 
                "mode": "build_movie_list", 
                "name": "Premieres", 
                "foldername": "Movies Premiering",
                "info": "Browse Movies that have Premiered in the Last Month."
            }, 
            {
                "name": "Latest Releases", 
                "iconImage": "dvd.png", 
                "foldername": "Latest Releases", 
                "mode": "build_movie_list", 
                "action": "tmdb_movies_latest_releases",
                "info": "Browse Movies Released Within the Last Month."
            }, 
            {
                "action": "trakt_movies_top10_boxoffice", 
                "iconImage": "box_office.png", 
                "mode": "build_movie_list", 
                "name": "Top 10 Box Office", 
                "foldername": "Movies Box Office",
                "info": "Browse Top 10 Movies from this Weeks Box Office."
            }, 
            {
                "name": "Blockbusters", 
                "iconImage": "most_voted.png", 
                "foldername": "Blockbusters", 
                "mode": "build_movie_list", 
                "action": "tmdb_movies_blockbusters",
                "info": "Browse Blockbuster Movies."
            }, 
            {
                "name": "In Theaters", 
                "iconImage": "intheatres.png", 
                "foldername": "In Theaters", 
                "mode": "build_movie_list", 
                "action": "tmdb_movies_in_theaters",
                "info": "Browse In Theater Movies."
            }, 
            {
                "name": "Top Rated", 
                "iconImage": "top_rated.png", 
                "foldername": "Top Rated", 
                "mode": "build_movie_list", 
                "action": "tmdb_movies_top_rated",
                "info": "Browse Top Rated Movies."
            }, 
            {
                "name": "Up Coming", 
                "iconImage": "lists.png", 
                "foldername": "Up Coming", 
                "mode": "build_movie_list", 
                "action": "tmdb_movies_upcoming",
                "info": "Browse Up Coming Movies."
            }, 
            {
                "name": "Anticipated", 
                "iconImage": "most_anticipated.png", 
                "foldername": "Anticipated", 
                "mode": "build_movie_list", 
                "action": "trakt_movies_anticipated",
                "info": "Browse Anticipated Movies."
            }, 
            {
                "name": "Oscar Winners", 
                "iconImage": "oscar-winners.png", 
                "foldername": "Oscar Winners", 
                "mode": "build_movie_list", 
                "action": "imdb_movies_oscar_winners",
                "info": "Browse Oscar Winning Movies."
            }, 
            {
                "name": "Mosts", 
                "menu_type": "movie", 
                "iconImage": "trakt.png", 
                "foldername": "Mosts", 
                "mode": "navigator.trakt_mosts",
                "info": "Access Trakt Mosts Movie Menus. Menus are Most Played, Most Collected and Most Watched. These can be filtered by This Week, This Month, This Year or All Time."
            }, 
            {
                "name": "Genres", 
                "menu_type": "movie", 
                "iconImage": "genres.png", 
                "foldername": "Genres", 
                "mode": "navigator.genres",
                "info": "Access Movies by Genres."
            }, 
            {
                "name": "Languages", 
                "menu_type": "movie", 
                "iconImage": "languages.png", 
                "foldername": "Movie Languages", 
                "mode": "navigator.languages", 
                "info": "Browse Movies by Language."
            }, 
            {
                "name": "Years", 
                "menu_type": "movie", 
                "iconImage": "calender.png", 
                "foldername": "Movie Years", 
                "mode": "navigator.years", 
                "info": "Browse Movies by Year."
            }, 
            {
                "name": "Certifications", 
                "menu_type": "movie", 
                "iconImage": "certifications.png", 
                "foldername": "Certifications", 
                "mode": "navigator.certifications",
                "info": "Access Movies by US Certifications."
            }, 
            {
                "name": "Popular People", 
                "iconImage": "genre_comedy.png", 
                "foldername": "Popular People", 
                "mode": "build_movie_list", 
                "action": "tmdb_popular_people",
                "info": "Browse Most Popular People in Movies."
            }, 
            {
                "name": "Trakt Collection", 
                "iconImage": "traktcollection.png", 
                "foldername": "Trakt Collection", 
                "mode": "build_movie_list", 
                "action": "trakt_collection",
                "info": "Browse your Trakt Movie Collection. You must be logged into Trakt to view your Collection."
            }, 
            {
                "name": "Trakt Watchlist", 
                "iconImage": "traktwatchlist.png", 
                "foldername": "Trakt Watchlist", 
                "mode": "build_movie_list", 
                "action": "trakt_watchlist",
                "info": "Browse your Trakt Movie Watchlist. You must be logged into Trakt to view your Watchlist."
            }, 
            {
                "name": "Trakt Recommendations", 
                "iconImage": "traktrecommendations.png", 
                "foldername": "Trakt Recommendations", 
                "mode": "build_movie_list", 
                "action": "trakt_recommendations",
                "info": "Browse your Trakt Recommendations. You must be logged into Trakt to view your Recommendations."
            }, 
            {
                "foldername": "Watched", 
                "iconImage": "watched_1.png", 
                "mode": "build_movie_list",  
                "action": "watched_movies", 
                "name": "Watched",
                "info": "Browse Movies that you have Watched in Fen."
            }, 
            {
                "foldername": "In Progress", 
                "iconImage": "player.png", 
                "mode": "build_movie_list",  
                "action": "in_progress_movies", 
                "name": "In Progress",
                "info": "Browse Movies that you have begun to watch in Fen, but haven't finished."
            }, 
            {
                "name": "Favourites", 
                "iconImage": "favourites.png", 
                "foldername": "Movie Favourites", 
                "mode": "build_movie_list", 
                "action": "favourites_movies",
                "info": "Browse Movies you have added to Fen Favourites."
            }, 
            {
                "name": "Subscriptions", 
                "iconImage": "library.png", 
                "foldername": "Subscriptions", 
                "mode": "build_movie_list", 
                "action": "subscriptions_movies",
                "info": "Browse Movies you have added to Fen Subscriptions."
            }, 
            {
                "name": "Kodi Library", 
                "iconImage": "library_kodi.png", 
                "foldername": "Kodi Library", 
                "mode": "build_movie_list", 
                "action": "kodi_library_movies",
                "info": "Browse Movies that are in your personal Kodi Library."
            }, 
            {
                "name": "Kodi Library - Recently Added", 
                "iconImage": "library_kodi_recently_added.png", 
                "foldername": "Recently Added to Kodi Library", 
                "mode": "build_kodi_library_recently_added", 
                "db_type": "movies",
                "info": "Browse Recently Added Movies from your Local Kodi Library."
            }, 
            {
                "name": "Search", 
                "iconImage": "search.png", 
                "foldername": "Movie Search", 
                "mode": "build_movie_list", 
                "action": "tmdb_movies_search", 
                "query": "NA",
                "info": "Search for Movies by name."
            }, 
            {
                "name": "People Search", 
                "iconImage": "search_people.png", 
                "foldername": "People Movie Search", 
                "mode": "build_movie_list", 
                "action": "tmdb_movies_people_search", 
                "query": "NA",
                "info": "Search for Movies starring an Actor or Actress."
            }, 
            {
                "foldername": "Movie Search History", 
                "iconImage": "search.png", 
                "mode": "search_history", 
                "action": "movie",
                "name": "Search History",
                "info": "Access a History of Movie Searches. The last 10 searches are stored."
            }
        ]
    
    def TVShowList(self):
        return [
            {
                "action": "trakt_tv_trending", 
                "iconImage": "trending.png", 
                "mode": "build_tvshow_list", 
                "name": "Trending", 
                "foldername": "TV Trending",
                "info": "Browse Trending TV Shows."
            }, 
            {
                "action": "tmdb_tv_popular", 
                "iconImage": "popular.png", 
                "mode": "build_tvshow_list", 
                "name": "Popular", 
                "foldername": "TV Popular",
                "info": "Browse Popular TV Shows."
            }, 
            {
                "action": "tmdb_tv_premieres", 
                "iconImage": "fresh.png", 
                "mode": "build_tvshow_list", 
                "name": "Premieres", 
                "foldername": "TV Premiering",
                "info": "Browse TV Shows that have Premiered in the Last Month."
            }, 
            {
                "action": "tmdb_tv_top_rated", 
                "iconImage": "top_rated.png", 
                "mode": "build_tvshow_list", 
                "name": "Top Rated", 
                "foldername": "TV Top Rated",
                "info": "Browse Top Rated TV Shows."
            }, 
            {
                "action": "tmdb_tv_airing_today", 
                "iconImage": "live.png", 
                "mode": "build_tvshow_list", 
                "name": "Airing Today",
                "info": "Browse TVShows Airing Today."
            }, 
            {
                "action": "tmdb_tv_on_the_air", 
                "iconImage": "ontheair.png", 
                "mode": "build_tvshow_list", 
                "name": "On the Air", 
                "foldername": "TV On the Air",
                "info": "Browse TVShows On the Air."
            }, 
            {
                "name": "Up Coming", 
                "iconImage": "lists.png", 
                "foldername": "Up Coming", 
                "mode": "build_tvshow_list", 
                "action": "tmdb_tv_upcoming",
                "info": "Browse Up Coming TV Shows."
            }, 
            {
                "action": "trakt_tv_anticipated", 
                "iconImage": "most_anticipated.png", 
                "mode": "build_tvshow_list", 
                "name": "Anticipated",
                "info": "Browse Anticipated TVShows."
            }, 
            {
                "menu_type": "tvshow", 
                "iconImage": "trakt.png", 
                "mode": "navigator.trakt_mosts", 
                "name": "Mosts", 
                "foldername": "TV Trakt Mosts",
                "info": "Access Trakt Mosts TV Show Menus. Menus are Most Played, Most Collected and Most Watched. These can be filtered by This Week, This Month, This Year or All Time."
            }, 
            {
                "menu_type": "tvshow", 
                "iconImage": "genres.png", 
                "mode": "navigator.genres", 
                "name": "Genres", 
                "foldername": "TV Genres",
                "info": "Access TV Shows by Genres."
            }, 
            {
                "menu_type": "tvshow", 
                "iconImage": "networks.png", 
                "mode": "navigator.networks", 
                "name": "Networks", 
                "foldername": "TV Networks",
                "info": "Access TV Networks."
            }, 
            {
                "menu_type": "tvshow", 
                "iconImage": "languages.png", 
                "mode": "navigator.languages", 
                "name": "Languages", 
                "foldername": "TV Show Languages",
                "info": "Browse TV Shows by Language."
            }, 
            {
                "name": "Years", 
                "menu_type": "tvshow", 
                "iconImage": "calender.png", 
                "foldername": "TV Show Years", 
                "mode": "navigator.years", 
                "info": "Browse TV Shows by Year."
            }, 
            {
                "menu_type": "tvshow", 
                "iconImage": "certifications.png", 
                "mode": "navigator.certifications", 
                "name": "Certifications", 
                "foldername": "TV Show Certifications",
                "info": "Access TV Shows by US Certifications."
            }, 
            {
                "name": "Popular People", 
                "iconImage": "genre_comedy.png", 
                "foldername": "Popular People", 
                "mode": "build_tvshow_list", 
                "action": "tmdb_popular_people",
                "info": "Browse Most Popular People in TV Shows."
            }, 
            {
                "action": "trakt_collection", 
                "iconImage": "traktcollection.png", 
                "mode": "build_tvshow_list", 
                "name": "Trakt Collection", 
                "foldername": "Trakt TV Collection",
                "info": "Browse your Trakt TV Show Collection. You must be logged into Trakt to view your Collection."
            }, 
            {
                "action": "trakt_watchlist", 
                "iconImage": "traktwatchlist.png", 
                "mode": "build_tvshow_list", 
                "name": "Trakt Watchlist", 
                "foldername": "Trakt TV Watchlist",
                "info": "Browse your Trakt TV Show Watchlist. You must be logged into Trakt to view your Watchlist."
            }, 
            {
                "name": "Trakt Recommendations", 
                "iconImage": "traktrecommendations.png", 
                "foldername": "Trakt Recommendations", 
                "mode": "build_tvshow_list", 
                "action": "trakt_recommendations",
                "info": "Browse your Trakt Recommendations. You must be logged into Trakt to view your Recommendations."
            }, 
            {
                "foldername": "Watched", 
                "iconImage": "watched_1.png", 
                "mode": "build_tvshow_list",  
                "action": "watched_tvshows", 
                "name": "Watched",
                "info": "Browse TV Shows that you have Watched in Fen."
            }, 
            {
                "action": "in_progress_tvshows", 
                "iconImage": "in_progress_tvshow.png", 
                "mode": "build_tvshow_list", 
                "name": "In Progress TV Shows", 
                "foldername": "In Progress TV Shows",
                "info": "Browse TV Shows that you have begun to watch in Fen, but haven't finished."
            }, 
            {
                "iconImage": "player.png", 
                "mode": "build_in_progress_episode", 
                "name": "In Progress Episodes", 
                "foldername": "In Progress Episodes",
                "info": "Browse Episodes that you have begun to watch in Fen, but haven't finished."
            }, 
            {
                "iconImage": "next_episodes.png", 
                "mode": "build_next_episode", 
                "name": "Next Episodes", 
                "foldername": "It Next Episodes",
                "info": "Next available to watch episodes based on either Trakt or Fen watched history."
            }, 
            {
                "action": "favourites_tvshows", 
                "iconImage": "favourites.png", 
                "mode": "build_tvshow_list", 
                "name": "Favourites", 
                "foldername": "TV Show It Favourites",
                "info": "Browse TV Shows you have added to Fen Favourites."
            }, 
            {
                "action": "subscriptions_tvshows", 
                "iconImage": "library.png", 
                "mode": "build_tvshow_list", 
                "name": "Subscriptions", 
                "foldername": "Subscriptions",
                "info": "Browse TV Shows you have added to Fen Subscriptions."
            }, 
            {
                "action": "kodi_library_tvshows", 
                "iconImage": "library_kodi.png", 
                "mode": "build_tvshow_list", 
                "name": "Kodi Library", 
                "foldername": "Kodi Library",
                "info": "Browse TV Shows that are in your personal Kodi Library."
            }, 
            {
                "name": "Kodi Library - Recently Added", 
                "iconImage": "library_kodi_recently_added.png", 
                "foldername": "Recently Added to Kodi Library", 
                "mode": "build_kodi_library_recently_added", 
                "db_type": "episodes",
                "info": "Browse Recently Added Episodes from your Local Kodi Library."
            }, 
            {
                "name": "Search", 
                "iconImage": "search.png", 
                "foldername": "TV Show Search", 
                "mode": "build_tvshow_list", 
                "action": "tmdb_tv_search", 
                "query": "NA",
                "info": "Search for TV Shows by name."
            }, 
            {
                "name": "People Search", 
                "iconImage": "search_people.png", 
                "foldername": "People TV Show Search", 
                "mode": "build_tvshow_list", 
                "action": "tmdb_tv_people_search", 
                "query": "NA",
                "info": "Search for TV Shows starring an Actor or Actress."
            }, 
            {
                "iconImage": "search.png", 
                "mode": "search_history", 
                "action": "tvshow",
                "name": "Search History", 
                "foldername": "TV Show Search History",
                "info": "Browse a History of TV Show Searches. The last 10 searches are stored."
            }
        ]

    def AudioList(self):
        return [
            { 
                "name": "My Furk Music Files", 
                "iconImage": "lists.png", 
                "foldername": "My Furk Audio Files", 
                "mode": "furk.my_furk_files", 
                "db_type": "audio",
                "info": "Browse Music Files and Folders saved in your Furk My Files section."
            }, 
            {
                "name": "Music Favourites", 
                "iconImage": "genre_music.png", 
                "foldername": "Audio Favourites", 
                "mode": "my_furk_audio_favourites",
                "info": "Browse Music Folders saved as Favourites in Fen."
            }, 
            {
                "name": "Search Furk For Music", 
                "iconImage": "search.png", 
                "foldername": "Search Furk (Audio)", 
                "mode": "furk.search_furk", 
                "db_type": "audio",
                "info": "Search Furk For Music."
            }, 
            {
                "name": "Music Search History", 
                "iconImage": "search.png", 
                "foldername": "Audio Search History", 
                "mode": "search_history", 
                "action": "furk_audio",
                "info": "Browse a History of Music Searches. The last 10 searches are stored."
            }
        ]

    def DefaultMenuItems(self):
        return ['RootList', 'MovieList', 'TVShowList', 'AudioList']






