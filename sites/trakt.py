from utils import common
from sites import traktlib, furklib
import datetime,sys,time
import xbmcgui,xbmc,xbmcplugin
import sys
from utils import settings
from utils import searcher


def addToXbmcLib(fg = None):
	totalAdded=0
	if fg == 'True':
		common.Notification('Getting:','Trending')	
	movies = traktlib.getTrendingMoviesFromTrakt()
	if movies:
		for movie in movies:
			if not movie['watched'] and movie['watchers']>1:
				totalAdded = totalAdded + common.createMovieStrm(movie['title'],movie['year'],movie['imdb_id'])
			        common.createMovieNfo(movie['title'],movie['year'],movie['imdb_id'])

	if fg == 'True':
		common.Notification('Getting:','Recommended')	
	movies = traktlib.getRecommendedMoviesFromTrakt()
	if movies:
	    for movie in movies:
		totalAdded = totalAdded + common.createMovieStrm(movie['title'],movie['year'],movie['imdb_id'])
	        common.createMovieNfo(movie['title'],movie['year'],movie['imdb_id'])
	if fg == 'True':
		common.Notification('Getting:','Watchlist Movies')	
	movies = traktlib.getWatchlistMoviesFromTrakt()
	for movie in movies:
		totalAdded = totalAdded + common.createMovieStrm(movie['title'],movie['year'],movie['imdb_id'])
	        common.createMovieNfo(movie['title'],movie['year'],movie['imdb_id'])


	if fg == 'True':
		common.Notification('Getting:','Calendar Shows')	
	d = datetime.date.today() + datetime.timedelta(days=-8)
	currentdate = d.strftime('%Y%m%d')
	series = traktlib.getShowsCalendarFromTrakt(currentdate)
	for show in series:
	    episodes = show['episodes']
    
	    for episode in episodes:
		myepisode = episode['episode']
	        myshow = episode['show']
		totalAdded = totalAdded + common.createShowStrm(myshow['title'],myepisode['season'],myepisode['number'],myshow['tvdb_id'])

	if fg == 'True':		
		common.Notification('Getting:','Watchlist Shows')	
	totalAdded = totalAdded + getWatchlistShows()
	if fg == 'True':
		common.Notification('Total:', str(totalAdded))
	return totalAdded



def displaySeasons(tvdb_id):
	xbmcplugin.setContent(int(sys.argv[1]), 'tvshows')
	seasons = traktlib.getSeasons(tvdb_id)
	show = traktlib.getShow(tvdb_id)
	for season in seasons:
		common.createShowSeasonListItemTrakt(show, season, tvdb_id)
	common.endofDir()
	
def displayEpisodes(season, tvdb_id):
	xbmcplugin.setContent(int(sys.argv[1]), 'tvshows')
	show = traktlib.getShow(tvdb_id)
	episodes = traktlib.getEpisodes(tvdb_id, season)
	for episode in episodes:
		common.createEpisodeListItemTrakt(show, episode, tvdb_id)
	common.endofDir()

def getWatchlistShows():
	tot = 0
	shows = traktlib.getWatchlistShowsfromTrakt()

	for myshow in shows:
		if common.checkEnded(myshow['title']) == False:
			fullshow = traktlib.getFullShow(myshow['tvdb_id'])
			seasons = fullshow['seasons']
			common.Notification('Getting:', myshow['title'])
			for season in seasons:
				if season['season']==0:
				    continue
				episodes = season['episodes']
				for myepisode in episodes:
					tot = tot + common.createShowStrm(myshow['title'],myepisode['season'],myepisode['number'],myshow['tvdb_id'])
			common.putShowStatus(fullshow['title'],fullshow['status'])
	return tot


def displayGenres(type):	
	if type == 'Movie':
		genres = traktlib.getMovieGenres()
		url = sys.argv[0]+'?action=trakt_RecommendedMovies&genre=' 
	elif type == 'Show' :
		genres = traktlib.getShowGenres()
		url = sys.argv[0]+'?action=trakt_RecommendedShows&genre=' 

	for genre in genres:
		common.createListItem(genre['name'], True, url+genre['slug'])
	common.endofDir()


def displayLists(type):
	genres = None
	
	if type == 'Movie':
		genres = ['Action','Adventure','Animation','Comedy','Crime',
			'Documentary','Drama','Family','Fantasy','Film Noir','History',
			'Horror','Indie','Music','Musical','Mystery','No Genre','Romance',
			'Science Fiction','Sport','Suspense','Thriller','War','Western']
		
		url = sys.argv[0]+'?action=trakt_getList&user=cloudberry&slug=movie-'

		#genres = traktlib.getMovieGenres()
		#genres = traktlib.getListsFromTrakt()
		#url = sys.argv[0]+'?action=trakt_RecommendedMovies&genre=' 
		#url = sys.argv[0]+'?action=trakt_getList&user=cloudberry&slug=' 
	elif type == 'Show' :
		genres = ['Action','Adventure','Animation','Children',
			'Comedy','Documentary','Drama','Fantasy',
			'Game Show','Home and Garden','Mini Series',
			'News','No Genre','Reality','Science Fiction',
			'Soap','Special Interest','Sport','Talk Show',
			'Western']

		#genres = traktlib.getShowGenres()
		#url = sys.argv[0]+'?action=trakt_RecommendedShows&genre=' 
		url = sys.argv[0]+'?action=trakt_getList&user=cloudberry&slug=show-' 

	for genre in genres:
		#traktlib.createListTrakt(genre, type)
		common.createListItem(genre, True, url + genre.lower().replace(' ', '-'))

	#for genre in genres:
	#	common.createListItem(genre['name'], True, url+genre['slug'])
	common.endofDir()
	
def displayAdultGenres():

	

	genres = [ "Amateur","Anal","Asian","Ass","BBW","Big Dicks","Big Tits","Blondes",
		"Blowjob","Bondage","Brunette","Cumshot","Deep Throat",
		"Fetish","Fisting","Gangbang","Gay","Handjob","Hardcore","Hentai",
		"Interracial","Lesbian","Masturbation","Mature","MILF","Pornstars",
		"Sex Toys","Shemale","Squirting","Striptease","Teens","Threesome","Tranny"]

	url = sys.argv[0]+'?action=trakt_SearchCache&query=' 
	for genre in genres:
		common.createListItem(genre, True, url+genre)
	common.endofDir()

def displayRecommendedShows(genre):
	xbmcplugin.setContent(int(sys.argv[1]), 'tvshows')
	shows = traktlib.getRecommendedShowsFromTrakt(genre)
	for show in shows:
		common.createShowListItemTrakt(show)
	common.endofDir()

def displayProgress():
	progress = traktlib.getProgress()
	for current in progress:
		lastseason = 100
		lastepisode = 100
		for season in current['seasons']:
			seasonnumber = int(season['season'])
			for episode in season ['episodes']:
				if not season ['episodes'][episode]:
					myseason,myepisode = seasonnumber,int(episode)
					if myseason<lastseason:
						lastseason = myseason
						lastepisode = 100
					if myseason==lastseason and myepisode<lastepisode:
						lastepisode = myepisode
					#print '{0} S{1} E{2} / S{3} E{4}'.format(current['show']['title'],myseason,myepisode,lastseason,lastepisode)

		#print '{0} S{1} E{2}'.format(current['show']['title'],lastseason,lastepisode)
		#break
		if lastseason <>100:
			common.createShowListItemTrakt(current['show'],len(progress),lastseason,lastepisode)
	common.endofDir()


def calculateProgress():
	progress = traktlib.getProgress()
	shows = {}
	

	progressByShow = {}
	for current in progress:
		lastseason = 100
		lastepisode = 100
		allwatched = False
		if current['progress']['left']<>0:
			for season in current['seasons']:
				seasonnumber = int(season['season'])
				for episode in season ['episodes']:
					if not season ['episodes'][episode]:
						myseason,myepisode = seasonnumber,int(episode)
						if myseason<lastseason:
							lastseason = myseason
							lastepisode = 100
						if myseason==lastseason and myepisode<lastepisode:
							lastepisode = myepisode
					#print '{0} S{1} E{2} / S{3} E{4}'.format(current['show']['title'],myseason,myepisode,lastseason,lastepisode)
		else:
			allwatched = True
		#print '{0} S{1} E{2}'.format(current['show']['title'],lastseason,lastepisode)
		#break
		show = {}
		if lastseason<>100:
			shows[current['show']['title']]= (lastseason,lastepisode)
		elif allwatched:
			shows[current['show']['title']]= (0,0)
		
	return shows

def displayList(user,slug):
	#xbmcplugin.setContent(int(sys.argv[1]), 'movies')
	myList = traktlib.getList(user,slug)
	movies = []
	shows = []
	for item in myList['items']:
		if item['type']=="movie":
			movies.append(item['movie'])
		elif item['type']=="show":
			shows.append(item['show'])			

	for movie in movies:
		try:
			common.createMovieListItemTrakt(movie,totalItems = len(movies))
		except:
			None
	for show in shows:
		try:
			common.createShowListItemTrakt(show,totalItems = len(shows))
		except:
			None
		
	common.endofDir()
	return

def displayRecommendedMovies(genre):
	xbmcplugin.setContent(int(sys.argv[1]), 'movies')
	movies = traktlib.getRecommendedMoviesFromTrakt(genre)
	for movie in movies:
		common.createMovieListItemTrakt(movie,totalItems = len(movies))
	common.endofDir()
	return

def traktSeenRate(imdbid):
	mymovie = traktlib.getMovieInfobyImdbid(imdbid)
	movie = {}
	movie['imdb_id'] = mymovie['imdb_id']
	movie['title']= mymovie['title']
	movie['year']= mymovie['year']
	ratings = []
	for i in range(1,11):
		ratings.append(str(i))
	dialog = xbmcgui.Dialog()
	myrating = dialog.select('Rating', ratings)
	if myrating==-1: return
	movie['rating'] = ratings[myrating]
	response = traktlib.setRating(movie,'movie')
	common.traktResponse(response)
	args = {}
	movie = {}
	args['movies'] = []
	movie['imdb_id'] = mymovie['imdb_id']
	movie['title']= mymovie['title']
	movie['year']= mymovie['year']
	movie['plays'] = 1
	movie['last_played'] = int(time.time())
	args['movies'].append(movie)
	traktlib.setSeen(args)
	return

def traktSeenShow(tvdbid,season,episode):
	show = {}
	show['tvdb_id'] = tvdbid
	if season==100:
		ratings = []
		for i in range(1,11):
			ratings.append(str(i))
		dialog = xbmcgui.Dialog()
		myrating = dialog.select('Rating', ratings)
		if myrating==-1: return
		show['rating'] = ratings[myrating]
		response = traktlib.setRating(show,'show')
		common.traktResponse(response)
	
	response = traktlib.setShowSeen(tvdbid,season,episode)
	common.traktResponse(response)


	return

def traktDismissMovie(imdbid):
	response = traktlib.dismissMovie(imdbid)
	common.Notification(response['status'],response['message'])

def addShowtoWatchlist(tvdbid):
	response = traktlib.addShowtoWatchList(tvdbid)
	common.traktResponse(response)
	getWatchlistShows()
	xbmc.executebuiltin('UpdateLibrary(video)')

def traktDismissShow(tvdbid):
	response = traktlib.dismissShow(tvdbid)
	common.Notification(response['status'],response['message'])

def addMovietoWatchlist(imdbid):
	response = traktlib.addMovietoWatchlist(imdbid)
	common.traktResponse(response)
	movies = traktlib.getWatchlistMoviesFromTrakt()
	for movie in movies:
		common.createMovieStrm(movie['title'],movie['year'],movie['imdb_id'])
	        common.createMovieNfo(movie['title'],movie['year'],movie['imdb_id'])
	xbmc.executebuiltin('UpdateLibrary(video)')



def traktAction(params):
	if(params['action'] == 'trakt_Menu'):
		displayTraktMenu()
	
	elif(params['action'] == 'trakt_SearchMovies'):
	        # Search
	        keyboard = xbmc.Keyboard(settings.getSetting('last_movie_search'), 'Search')
		keyboard.doModal()
	        if keyboard.isConfirmed():
		        query = keyboard.getText()
		        settings.setSetting('last_movie_search', query)
			movies = traktlib.getMovieInfobySearch(unicode(query))
			for movie in movies:
				common.createMovieListItemTrakt(movie,totalItems = len(movies))
			common.endofDir()
	
	elif(params['action'] == 'trakt_SearchShows'):
	        # Search
	        keyboard = xbmc.Keyboard(settings.getSetting('last_tv_show_search'), 'Search')
		keyboard.doModal()
	        if keyboard.isConfirmed():
		        query = keyboard.getText()
		        settings.setSetting('last_tv_show_search', query)
			shows = traktlib.getShowInfobySearch(unicode(query))
			for show in shows:
				common.createShowListItemTrakt(show,totalItems = len(shows))
			common.endofDir()
	
		
	elif(params['action'] == 'trakt_SeenRate'):
		imdbid = params['imdbid']
		traktSeenRate(imdbid)

	elif(params['action'] == 'trakt_DismissMovie'):
		imdbid = params['imdbid']
		traktDismissMovie(imdbid)

	elif(params['action'] == 'trakt_MovieGenres'):
		displayGenres(type='Movie')

	elif(params['action'] == 'trakt_ShowGenres'):
		displayGenres(type='Show')

	elif(params['action'] == 'trakt_ShowLists'):
		displayLists(type=params['type'])

	elif(params['action'] == 'trakt_ShowAdultLists'):
		displayAdultGenres()
		
	elif(params['action'] == 'trakt_SearchCache'):
		query = params['query']
		searcher.SearchFromMenu(query)

	elif(params['action'] == 'trakt_RecommendedShows'):
		try:
			genre = params['genre']
		except:
			genre = None
		if genre:
			displayRecommendedShows(genre)
		else :			
			url = sys.argv[0]+'?action=trakt_ShowGenres' 
			common.createListItem('Filter by Genre', True, url)
			displayRecommendedShows(genre)

	elif(params['action'] == 'trakt_listfeeds'):
			myfeeds = furklib.myFeeds()['feeds']
			myfeeds = sorted(myfeeds,key=lambda feed: feed['name'])
			url = sys.argv[0]+'?action=trakt_addfeeds' 
			common.createListItem('Add Feeds from trakt', True, url)
			for feed in myfeeds:
				url = sys.argv[0]+'?action=trakt_MovieGenres' 
				common.createListItem(feed['name'], True, url)
			common.endofDir()
	
	elif(params['action'] == 'trakt_addfeeds'):
			myfeeds = furklib.myFeeds()['feeds']
			shows = traktlib.getWatchlistShowsfromTrakt()
			progress = traktlib.getProgress()
			series = []
			for current in progress:
				series.append(current['show'])
			shows = shows + series
			for show in shows:
				check = [feed for feed in myfeeds if feed['name'] == show['title']]
				if len(check)==0:
					furklib.addFeed(show['title'])
					url = sys.argv[0]+'?action=trakt_MovieGenres' 
					common.createListItem(show['title'], False, '')
			common.endofDir()

	elif(params['action'] == 'trakt_RecommendedMovies'):
		try:
			genre = params['genre']
		except:
			genre = None
		if genre:
			displayRecommendedMovies(genre)
		else :			
			url = sys.argv[0]+'?action=trakt_MovieGenres' 
			common.createListItem('Filter by Genre', True, url)
			displayRecommendedMovies(genre)
			
	elif(params['action'] == 'trakt_Seasons'):
		tvdbid = params['tvdbid']
		displaySeasons(tvdbid)

	elif(params['action'] == 'trakt_Episodes'):
		tvdbid = params['tvdbid']
		season = params['season']
		displayEpisodes(season, tvdbid)

	elif(params['action'] == 'trakt_AddShowtoWatchlist'):
		tvdbid = params['tvdbid']
		addShowtoWatchlist(tvdbid)
	
	elif(params['action'] == 'trakt_AddMovietoWatchlist'):
		imdbid = params['imdbid']
		addMovietoWatchlist(imdbid)

	elif(params['action'] == 'trakt_RemoveMoviefromWatchlist'):
		imdbid = params['imdbid']
		response = traktlib.removeMoviefromWatchlist(imdbid)
		common.traktResponse(response)

	elif(params['action'] == 'trakt_DismissShow'):
		tvdbid = params['tvdbid']
		traktDismissShow(tvdbid)
	
	elif(params['action'] == 'trakt_SetShowSeen'):
		tvdbid = params['tvdbid']
		try:
			season = params['season']
			episode = params['episode']
		except:
			season = 100
			episode = 100
		response = traktSeenShow(tvdbid,season,episode)

	elif(params['action'] == 'trakt_TrendingMovies'):
		xbmcplugin.setContent(int(sys.argv[1]), 'movies')
		movies = traktlib.getTrendingMoviesFromTrakt()
		for movie in movies:
			common.createMovieListItemTrakt(movie,totalItems = len(movies))
		common.endofDir()

	elif(params['action'] == 'trakt_TrendingShows'):
		xbmcplugin.setContent(int(sys.argv[1]), 'tvshows')
		shows = traktlib.getTrendingShowsFromTrakt()
		progressShows = calculateProgress()
		for show in shows:
			if show['title'] in progressShows:
				common.createShowListItemTrakt(show,len(shows))#,progressShows[show['title']][0],progressShows[show['title']][1])
			else:
				common.createShowListItemTrakt(show,totalItems = len(shows))
		common.endofDir()
	
	elif(params['action'] == 'trakt_Progress'):
		displayProgress()
	elif(params['action'] == 'trakt_getList'):
		user=params['user']
		slug=params['slug']
		displayList(user,slug)
	else:
		common.Notification('Action Not found:' , params['action'])

def displayTraktMenu():
	
	url = sys.argv[0]+'?action='
	common.createListItem('Search in Furk cache', True, url+'search')
	common.createListItem('My Furk files', True, url+'myFiles')
	common.createListItem('Search Movie', True, url+'trakt_SearchMovies')	
	common.createListItem('Search TV Show', True, url+'trakt_SearchShows')
	#common.createListItem('Recommended Movies', True, url+'trakt_MovieGenres')
	common.createListItem('Trending Movies', True, url +'trakt_TrendingMovies')
	#common.createListItem('Recommended TV Shows', True, url +'trakt_ShowGenres')
	common.createListItem('Trending TV Shows', True, url +'trakt_TrendingShows')
	common.createListItem('Movies', True, url +'trakt_ShowLists&user=cloudberry&type=Movie')
	common.createListItem('TV Shows', True, url +'trakt_ShowLists&user=cloudberry&type=Show')

	common.createListItem('Featured', True, url +'trakt_getList&user=cloudberry&slug=movie-featured')
	common.createListItem('Most Popular', True, url +'trakt_getList&user=cloudberry&slug=movie-most-popular')
	common.createListItem('Highly rated', True, url +'trakt_getList&user=cloudberry&slug=movie-highly-rated')
	
	common.createListItem('Featured', True, url +'trakt_getList&user=cloudberry&slug=show-featured')
	common.createListItem('Most Popular', True, url +'trakt_getList&user=cloudberry&slug=show-most-popular')
	common.createListItem('Highly rated', True, url +'trakt_getList&user=cloudberry&slug=show-highly-rated')

	if settings.getSetting('adult_menu') == 'true':
		common.createListItem('Adult', True, url +'trakt_ShowAdultLists')

	common.createListItem('IMDB Top 250', True, url +'trakt_getList&user=mmounirou&slug=imdb-best-250-movies')
	common.createListItem('Movies of 2013', True, url +'trakt_getList&user=BenFranklin&slug=movies-of-2013')
	common.endofDir()
