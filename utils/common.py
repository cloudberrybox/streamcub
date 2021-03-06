import os,sys,urlparse,re,time
import xbmcgui,xbmc,xbmcplugin,xbmcaddon
from sites import traktlib
import json
import traceback
#import SimpleDownloader as downloader

# downloader = downloader.SimpleDownloader()
CACHE_PATH= sys.modules[ "__main__" ].CACHE_PATH
MOVIES_PATH = sys.modules[ "__main__" ].MOVIES_PATH
TV_SHOWS_PATH = sys.modules[ "__main__" ].TV_SHOWS_PATH


def RemoveDirectory(dir):
	dialog = xbmcgui.Dialog()
	if dialog.yesno("Remove directory", "Do you want to remove directory?", dir):
		if os.path.exists(dir):
			pDialog = xbmcgui.DialogProgress()
			pDialog.create(' Removing directory...')
			pDialog.update(0, dir)	
			shutil.rmtree(dir)
			pDialog.close()
			Notification("Directory removed", dir)
		else:
			Notification("Directory not found", "Can't delete what does not exist.")	

def Notification(title, message):
        try:
                xbmc.executebuiltin("XBMC.Notification("+title+","+message+")")
                print message.encode("utf-8")
        except: pass
        return

def createMovieStrm(movietitle,movieyear,imdbid = 0):
	ret = 0
	CreateDirectory(MOVIES_PATH)		
	filename = '/{0} ({1})'.format(movietitle.encode('ascii', 'ignore'),movieyear)
	filename = CleanFileName(filename)
	filename = os.path.join(MOVIES_PATH, filename+'.strm' )
	if not os.path.isfile(filename):
		with open(filename, 'w') as f:
			f.write(
			'''plugin://plugin.video.streamcub/default.py?action=SearchMe&type=Movie&title={0}&year={1}&imdbid={2}'''.format(CleanFileName(movietitle), movieyear,imdbid))
		ret = 1
		Notification('Scraped:',movietitle)
	return ret 

def createShowStrm(show_name,season,number,tvdbid):
    ret = 0
    show_path = os.path.join(TV_SHOWS_PATH, CleanFileName(show_name))
    CreateDirectory(show_path)		
    season_path = os.path.join(show_path, str(season))
    showfull = '''{0} S{1:0>2}E{2:0>2}'''.format(show_name, season,number)
    showfull = CleanFileName(showfull)
    CreateDirectory(season_path)
    filename = season_path + '/{0}.strm'.format(showfull)
    if not os.path.isfile(filename):
	    with open(filename, 'w') as f:
		f.write(
	'''plugin://plugin.video.streamcub/default.py?action=SearchMe&type=Show&title={0}&season={1}&episode={2}&tvdbid={3}'''.format(show_name,season,number,tvdbid))
	    ret = 1
	    Notification('Scraped:',showfull)
    return ret

def createMovieNfo(movietitle,movieyear,imdbid):
# write nfo file
	filename = CleanFileName('/{0} ({1})'.format(movietitle.encode('ascii', 'ignore'),movieyear))
	filename = filename + '.nfo'
	filename = os.path.join(MOVIES_PATH, filename)

	if not os.path.isfile(filename):
		with open(filename, 'w') as f:
			f.write(
				'''http://akas.imdb.com/title/{0}/'''.format(imdbid))
	return




def CleanFileName(s):
	s = s.encode('ascii', 'ignore')
	s = s.replace(' (Eng subs)', '')
	s = s.replace(' (eng subs)', '')
	s = s.replace(' (English subs)', '')
	s = s.replace(' (english subs)', '')
	s = s.replace(' (Eng Subs)', '')
	s = s.replace(' (English Subs)', '')
	s = s.replace('&#x26;', '&')
	s = s.replace('&#x27;', '\'')
	s = s.replace('&#xC6;', 'AE')
	s = s.replace('&#xC7;', 'C')
	s = s.replace('&#xF4;', 'o')
	s = s.replace('&#xE9;', 'e')
	s = s.replace('&#xEB;', 'e')
	s = s.replace('&#xED;', 'i')
	s = s.replace('&#xEE;', 'i')
	s = s.replace('&frac12;', ' ')
	s = s.replace('&#xBD;', ' ') #half character
	s = s.replace('&#xB3;', ' ')
	s = s.replace('&#xB0;', ' ') #degree character
	s = s.replace('&#xA2;', 'c')
	s = s.replace('&#xE2;', 'a')
	s = s.replace('&#xEF;', 'i')
	s = s.replace('&#xE1;', 'a')
	s = s.replace('&#xE8;', 'e')
	s = s.replace('%2E', '.')
	s = s.replace('"', ' ')
	s = s.replace('*', ' ')
	s = s.replace('/', ' ')
	s = s.replace(':', ' ')
	s = s.replace('<', ' ')
	s = s.replace('>', ' ')
	s = s.replace('?', ' ')
	s = s.replace('\\', ' ')
	s = s.replace('|', ' ')
	s = s.replace('.', ' ')
	s = s.replace('!', ' ')
	s = s.replace("'", ' ')
	s = s.replace("-", ' ')
	s = s.replace("&",' ')
	try:
		s = re.sub(' +',' ',s)
	except:
		pass
	s = s.strip()
	return s

def CreateDirectory(dir_path):
	dir_path = dir_path.strip()
	if not os.path.exists(dir_path):
		os.makedirs(dir_path)
	return

def createCachePath():
	CreateDirectory (CACHE_PATH)
	return

def getMovieInfobySearch(movietitle,movieyear):
	filename = '/{0} ({1})'.format(movietitle,movieyear)
	filename = CleanFileName(filename)
	filename = os.path.join(CACHE_PATH, filename+'.txt' )
	movie = readMovie(filename,type='search')
	if movie: 
		return getMovieInfobyImdbid(movie['imdb_id'])

	movies = traktlib.getMovieInfobySearch(movietitle)
	mymovie = None
	if not movies:
		return None
	for movie in movies:
		try:
			if int(movie['year']) == int(movieyear) or len(movies)==1:
				mymovie = getMovieInfobyImdbid(movie['imdb_id'])
				writeMovieInfobySearch(movietitle,movieyear,movie)
				break
			else:
				continue
		except:
			continue
	if mymovie:
		return movie
	else:
		return None

def writeMovieInfobySearch(movietitle,movieyear,movie):
	filename = '/{0} ({1})'.format(movietitle,movieyear)
	filename = CleanFileName(filename)
	filename = os.path.join(CACHE_PATH, filename+'.txt' )
	return writeMovie(filename,movie)

def getMovieFromCache(imdbid):
	filename = '/{0}'.format(imdbid)
	filename = CleanFileName(filename)
	filename = os.path.join(CACHE_PATH, filename+'.txt' )
	movie = readMovie(filename)
	#if movie: print 'Movie is in cache'
	return movie
		
def readMovie(filename,type='normal'):
	if not os.path.isfile(filename):
		return None
	else:
		f = open(filename, 'r')
		raw = f.read()
		movie = json.loads(raw)
		if type=='search': return movie
		try:
			if movie['watched'] == False: movie = checkWatched(movie)
		except:
			movie = checkWatched(movie)
		return movie

def checkWatched(movie):
	#print 'checking:' + movie['title']
	filename = os.path.join(CACHE_PATH, 'watched.txt' )
	if not os.path.isfile(filename):
		refreshWatched=True
	else:
		f = os.path.getmtime(filename)
		if time.time() - f > 30000:
			refreshWatched=True
		else:
			refreshWatched=False
	if refreshWatched == True:
		watchedMovies = traktlib.getWatchedMovies()
		if not watchedMovies:
			return movie
		writeMovie(filename,watchedMovies)
	else:
		f = open(filename, 'r')
		raw = f.read()
		watchedMovies = json.loads(raw)
	

	for watchedMovie in watchedMovies:
		if movie['imdb_id'] == watchedMovie['imdb_id']:
			#print movie['title'] + ' is watched'
			movie['watched'] = True
			#writeMovietoCache(movie['imdb_id'].lstrip('t'),movie)
			return movie
			

	return movie



def writeMovie(filename,data):
	with open(filename, 'w') as f:
		f.write(json.dumps(data))
	ret = 1
	return ret 

def writeMovietoCache(imdbid,data):
	ret = 0
	CreateDirectory (CACHE_PATH)
	filename = '/{0}'.format(imdbid)
	filename = CleanFileName(filename)
	filename = os.path.join(CACHE_PATH, filename+'.txt' )
	writeMovie(filename,data)
	return

def getMovieInfobyImdbid (imdbid):
	imdbid = imdbid.lstrip('t')
	if imdbid == '': return None
	movie = getMovieFromCache(imdbid)
	if movie:
		return movie
	if not movie:
		movie = traktlib.getMovieInfobyImdbid(imdbid)
		if movie:
			writeMovietoCache(imdbid,movie)
	if movie: return movie
	return None

	

def createMovieListItemfromimdbid(imdbid,totalItems = 10 , extrainfo = None):
	movie = getMovieInfobyImdbid(imdbid)
	if not movie:
		return
	movie['extrainfo'] = extrainfo
	createMovieListItemTrakt(movie,totalItems = totalItems)
	return


def createMovieListItemTrakt(movie, movietitle = None,movieyear = None, totalItems = 10 , extrainfo = None):
	if movie:
		movietitle = movie['title']
		movieyear = movie['year']
		imdbid = movie['imdb_id']
	else:
		imdbid = None
	try:
		s =  movie['extrainfo'].format(movietitle.encode("utf-8"),movieyear)
	except:
		if extrainfo:
			s= extrainfo.format(movietitle.encode("utf-8"),movieyear)
		else:
			#s= movietitle.encode("utf-8")
			s= '{0} ({1})'.format(movietitle.encode("utf-8"),movieyear)
	
	li = xbmcgui.ListItem(s)

	if movie:
		addMovieInfotoListitem(li,movie)
	url = sys.argv[0]+'?action=SearchMe&go=now&type=Movie&title='+CleanFileName(movietitle)+'&year='+str(movieyear)+'&imdbid='+str(imdbid)
	return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=url, listitem=li, isFolder=False, totalItems = totalItems)


def createShowSeasonListItemTrakt(show, season, tvdbid, totalItems = 10):
	if season['season'] == 0:
		text = 'Specials'
	else:
		text = 'Season ' + str(season['season'])
	li = xbmcgui.ListItem(text)
	
	try:
		li.setThumbnailImage (season['images']['poster'])
	except:
		pass
		
	try:
		li.setProperty( "Fanart_Image", (show['images']['fanart']))
	except:
		pass
		
	url = sys.argv[0]+'?action=trakt_Episodes&go=now&type=Show&title='+show['title']+'&season=' + str(season['season']) +'&tvdbid='+str(tvdbid)
	return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=url, listitem=li, isFolder=True, totalItems = totalItems)

def createShowListItemTrakt(show, totalItems = 10,season =1,episode=1):
	if show:
		showtitle = show['title']
		tvdbid = show['tvdb_id']
	else:
		tvdbid = None

	season_episode = "s%.2de%.2d" % (int(season), int(episode))
	text= showtitle  # + " (" + str(show['year']) + ")"
	li = xbmcgui.ListItem(text)

	if show:
		addShowInfotoListitem(li,show)
		
	url = sys.argv[0]+'?action=trakt_Seasons&go=now&type=Show&title='+CleanFileName(show['title'])+'&season=' + str(season) + '&episode='+ str(episode) +'&tvdbid='+str(tvdbid)
	return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=url, listitem=li, isFolder=True, totalItems = totalItems)

def createEpisodeListItemTrakt(show, episode, tvdbid, totalItems = 10):
	season_episode = "s%.2de%.2d" % (int(episode['season']), int(episode['episode']))
	li = xbmcgui.ListItem(str(episode['episode']) + ' ' + episode['title'])

	if episode:
		episodedata={'episode':None, 'show':None}
		episodedata['episode'] = episode
		episodedata['show'] = show
		addEpisodeInfotoListitem(li, episodedata)
		
	url = sys.argv[0]+'?action=SearchMe&go=now&type=Show&title='+show['title']+'&season=' + str(episode['season']) + '&episode='+ str(episode['episode']) +'&tvdbid='+str(tvdbid)
	return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=url, listitem=li, isFolder=False, totalItems = 10)


def createMovieListItem(text, movietitle, movieyear, totalItems = 10 , imdbid=None):
	mymovie = None
	if imdbid:
		try:
			mymovie = getMovieInfobyImdbid(imdbid)
		except:
			pass
	else:
			mymovie = getMovieInfobySearch(movietitle,movieyear)

	if mymovie:
		createMovieListItemTrakt(mymovie, totalItems = totalItems)
	else:
		createMovieListItemTrakt(None,movietitle,movieyear,totalItems = totalItems)
		
	return

def createFurkSearchListItem(text, isFolder, url, img, plot, id, totalItems = 10):
	li = xbmcgui.ListItem(text)
	if img:
		li.setIconImage (img)
		li.setThumbnailImage (img)
		cm = [( "Add to My Files", "XBMC.RunPlugin(%s?action=download&id=%s)" % ( sys.argv[ 0 ], id), ) , ]
		li.addContextMenuItems( cm, replaceItems=False )
		
	return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=url, listitem=li, isFolder=isFolder,totalItems = totalItems)

def createListItem(text, isFolder, url, name='',totalItems = 10):
	li = xbmcgui.ListItem(text)
	return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=url, listitem=li, isFolder=isFolder,totalItems = totalItems)

def createStreamListItem(title, iconImage, url, totalItems = 10):
	li = xbmcgui.ListItem(label=title, iconImage=iconImage, thumbnailImage=iconImage, path=url)
	return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=url, listitem=li, isFolder=False,totalItems = totalItems)

def endofDir():
	pluginhandle=int(sys.argv[1])
	xbmcplugin.endOfDirectory(pluginhandle)
        xbmcplugin.addSortMethod(pluginhandle, xbmcplugin.SORT_METHOD_VIDEO_RATING)
	return

def checkEnded(show_name):
	show_path = os.path.join(TV_SHOWS_PATH, CleanFileName(show_name))
	show_path = os.path.join(show_path, 'Done.txt')
	return os.path.isfile(show_path)

def putShowStatus(show_name,status):
	show_path = os.path.join(TV_SHOWS_PATH, CleanFileName(show_name))
	show_path = os.path.join(show_path, 'Done.txt')
	open(show_path,'w')
	return

def addMovieInfotoListitem(li,movie):
	li.setThumbnailImage (movie['images']['poster'])
	try:
		li.setProperty( "Fanart_Image", (movie['images']['fanart']))
	except:
		pass
	li.setInfo('video', { 'Plot': movie['overview'] })
	li.setInfo('video', { 'Year': movie['year'] })
	li.setInfo('video', { 'Tagline': movie['tagline'] })
	#li.setInfo('video', { 'Cast': movie['runtime'] })
	try:
		rating = movie['rating_advanced']
	except:
		rating = int(movie['ratings']['percentage']) / 10.0
	if rating == 0 :
		rating = int(movie['ratings']['percentage']) / 10.0
	li.setInfo('video', { 'Rating': rating })
	
	mygenre = ''
	try:
		for genre in movie['genres']:
			mygenre = mygenre + genre + ' / '
	
		if len(mygenre)>0:
			mygenre = mygenre[:-2] 
		li.setInfo('video', { 'Genre': mygenre})
	except:
		pass

	try:
		if not movie['trailer']=='':
			path = movie['trailer']
			url_data = urlparse.urlparse(path)
			query = urlparse.parse_qs(url_data.query)
			video_id = query["v"][0]
			url = "plugin://plugin.video.youtube/?action=play_video&videoid=%s" %video_id
			li.setInfo('video', { 'Trailer': url })
	except:
		pass
	
	try:
		if movie['watched']==True:
			li.setInfo( "video", { "playcount": 1 } )
			watched = True
			overlay = ( xbmcgui.ICON_OVERLAY_NONE, )
	                overlay = ( overlay, xbmcgui.ICON_OVERLAY_WATCHED, )[ watched ]
			li.setInfo ( "video", {'Overlay' : overlay })
	except:
		pass
	try:
		cast = []
		for actor in movie['people']['actors']:
			cast += [ (actor['name'] , actor ['character'] )]
		li.setInfo('video', { 'CastAndRole' : cast } )
	except:
		pass
	try:
		directors = ''
		for director in movie['people']['directors']:
			directors += director['name'] + ' / '
		if len(directors)>0:
			directors = directors[:-2] 
			li.setInfo('video', { 'Director' : directors } )
	except:
		pass
	try:
		li.setInfo('video', { 'Duration' : str(movie['runtime']) } )
	except:
		pass
	try:
		directors = ''
		for director in movie['people']['writers']:
			directors += director['name'] + ' / '
		if len(directors)>0:
			directors = directors[:-2] 
			li.setInfo('video', { 'Writer' : directors } )
	except:
		pass

def addShowInfotoListitem(li,show):
	try:
		li.setThumbnailImage (show['images']['poster'])
	except:
		pass
	try:
		li.setProperty( "Fanart_Image", (show['images']['fanart']))
	except:
		pass
	try:
		li.setInfo('video', { 'Plot': show['overview'] })
		li.setInfo('video', { 'Year': show['year'] })
	except:
		pass
	#li.setInfo('video', { 'Tagline': show['tagline'] })
	rating = 0

	try:
		rating = show['rating_advanced']
	except:
		try:
			rating = int(show['ratings']['percentage']) / 10.0
		except:
			pass
	if rating == 0 :
		try:
			rating = int(show['ratings']['percentage']) / 10.0
		except:
			pass
	li.setInfo('video', { 'Rating': rating })
	try:
		mygenre = ''
		for genre in show['genres']:
			mygenre = mygenre + genre + ' / '
	
		if len(mygenre)>0:
			mygenre = mygenre[:-2] 
		li.setInfo('video', { 'Genre': mygenre})
	except:
		pass

	try:
		li.setInfo('video', { 'Duration' : str(show['runtime']) } )
	except:
		pass
	try:
		if show['watched']==True:
			li.setInfo( "video", { "playcount": 1 } )
			watched = True
			overlay = ( xbmcgui.ICON_OVERLAY_NONE, )
	                overlay = ( overlay, xbmcgui.ICON_OVERLAY_WATCHED, )[ watched ]
			li.setInfo ( "video", {'Overlay' : overlay })
	except:
		pass


def addEpisodeInfotoListitem(li,episodedata):
	episode = episodedata['episode']
	show = episodedata['show']
	li.setProperty( "Fanart_Image", (show['images']['fanart']))
	li.setProperty ("TVShowThumb",(show['images']['poster']))
	li.setProperty ("SeasonThumb",(show['images']['poster']))
	li.setInfo('video', { 'TVShowTitle' : show['title'] })
	li.setInfo('video', { 'Season' : episode['season'] })
	li.setInfo('video', { 'Episode' : episode['number'] })
	li.setInfo('video', { 'Plot': episode['overview'] })
	li.setInfo('video', { 'Year': show['year'] })
	li.setThumbnailImage (episode['images']['screen'])
	first_aired = time.localtime(episode['first_aired'])
	myTime = time.strftime("%d %b %Y",first_aired)
	li.setInfo('video', { 'Premiered': myTime })
	#li.setInfo('video', { 'Tagline': show['tagline'] })

	try:
		rating = episode['rating_advanced']
	except:
		rating = int(episode['ratings']['percentage']) / 10.0
	if rating == 0 :
		rating = int(episode['ratings']['percentage']) / 10.0
	li.setInfo('video', { 'Rating': rating })
	try:
		mygenre = ''
		for genre in show['genres']:
			mygenre = mygenre + genre + ' / '
	
		if len(mygenre)>0:
			mygenre = mygenre[:-2] 
		li.setInfo('video', { 'Genre': mygenre})
	except:
		pass

	try:
		li.setInfo('video', { 'Duration' : str(show['runtime']) } )
	except:
		pass
	try:
		if show['watched']==True:
			li.setInfo( "video", { "playcount": 1 } )
			watched = True
			overlay = ( xbmcgui.ICON_OVERLAY_NONE, )
	                overlay = ( overlay, xbmcgui.ICON_OVERLAY_WATCHED, )[ watched ]
			li.setInfo ( "video", {'Overlay' : overlay })
	except:
		pass


def addMovieInfotoPlayListitem(li,movie):
	li.setInfo('video', { 'Plot': movie['overview'] })
	li.setInfo('video', { 'Year': movie['year'] })
	li.setInfo('video', { 'Tagline': movie['tagline'] })
	li.setInfo('video', { 'Title': movie['title'] })
	li.setThumbnailImage (movie['images']['poster'])
	try:
		rating = movie['rating_advanced']
	except:
		rating = int(movie['ratings']['percentage']) / 10.0
	if rating == 0 :
		rating = int(movie['ratings']['percentage']) / 10.0
	li.setInfo('video', { 'Rating': rating })
	
	mygenre = ''
	for genre in movie['genres']:
		mygenre = mygenre + genre + ' / '
	
	if len(mygenre)>0:
		mygenre = mygenre[:-2] 
	li.setInfo('video', { 'Genre': mygenre})

#	try:
#		if not movie['trailer']=='':
#			path = movie['trailer']
#			url_data = urlparse.urlparse(path)
#			query = urlparse.parse_qs(url_data.query)
#			video_id = query["v"][0]
#			url = "plugin://plugin.video.youtube/?action=play_video&videoid=%s" %video_id
#			li.setInfo('video', { 'Trailer': url })
#	except:
#		pass
#	
	try:
		cast = []
		for actor in movie['people']['actors']:
			cast += [ (actor['name'] , actor ['character'] )]
		li.setInfo('video', { 'CastAndRole' : cast } )
	except:
		pass
	try:
		directors = ''
		for director in movie['people']['directors']:
			directors += director['name'] + ' / '
		if len(directors)>0:
			directors = directors[:-2] 
			li.setInfo('video', { 'Director' : directors } )
	except:
		pass
#	try:
#		li.setInfo('video', { 'Duration' : str(movie['runtime']) } )
#	except:
#		pass
	try:
		directors = ''
		for director in movie['people']['writers']:
			directors += director['name'] + ' / '
		if len(directors)>0:
			directors = directors[:-2] 
			li.setInfo('video', { 'Writer' : directors } )
	except:
		pass
	return

def download(id):
	Notification('Not implemented')
	return

def traktResponse(response):
	try:
		Notification(response['status'],response['message'])
	except:
		try:
			Notification(response['status'],response['error'])
		except:
			result = ''
			for key, value in response.iteritems():
				if str(value) <> '0':
					result = result + key +':' + str(value) +' '
			Notification(response['status'],result)
