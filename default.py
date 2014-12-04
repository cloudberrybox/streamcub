import sys, urllib, time, re, os
import xbmc, xbmcaddon, xbmcgui, xbmcplugin
import context
from utils import settings


# Plugin constants
__plugin__ = 'Streamcub Library'
__author__ = 'Streamcub Team'
__url__ = 'http://www.streamcub.com'
__version__ = '1.3.1'

print "[PLUGIN] '%s: version %s' initialized!" % (__plugin__, __version__)

if settings.getSetting('tv_show_custom_directory') == "true":
	TV_SHOWS_PATH = settings.getSetting('tv_show_directory')
else:
	TV_SHOWS_PATH = os.path.join(xbmc.translatePath('special://profile/addon_data/plugin.video.streamcub/tvshows'), '')

if settings.getSetting('movie_custom_directory') == "true":
	MOVIES_PATH = settings.getSetting('movie_directory')
else:
	MOVIES_PATH = os.path.join(xbmc.translatePath('special://profile/addon_data/plugin.video.streamcub/movies'), '')

CACHE_PATH= os.path.join(xbmc.translatePath('special://profile/addon_data/plugin.video.streamcub/traktcache'), '')
try:
	MYCONTEXT = context.context().getContext()
except:
	MYCONTEXT = 'video'


from utils import searcher
from utils import common
from sites import trakt,traktlib
from sites import furklib

print sys.modules[ "__main__" ]

def parse_qs(u):
	params = '?' in u and dict(p.split('=') for p in u[u.index('?') + 1:].split('&')) or {}
	
	return params;

def AddonMenu():  #homescreen
	print 'Streamcub menu'
	url = sys.argv[0]+'?action=' 
	#common.createListItem(params['content_type'],True,url + 'myFiles')
	#params['action'] = 'trakt_Menu'
	#trakt.traktAction(params)

	common.createListItem('Movies', True, url +'MovieMenu')
	common.createListItem('TV Shows', True, url +'ShowMenu')
	if settings.getSetting('adult_menu') == 'true':
		common.createListItem('Adult', True, url +'trakt_ShowAdultLists')
	common.createListItem('My Files',True,url + 'myFiles')
	#common.createListItem('Live TV',True,url + 'LiveTVMenu')
	common.createListItem('Search all torrents', True, url+'search')
	common.createListItem('Setup',False,url +'setup')
	xbmcplugin.endOfDirectory(int(sys.argv[1]))

def ShowMenu():  #homescreen
	print 'Streamcub TV show menu'
	url = sys.argv[0]+'?action='
	common.createListItem('Search TV Show', True, url+'trakt_SearchShows')
	common.createListItem('[COLOR green]Genres[/COLOR]', True, url +'trakt_ShowGenres')
	common.createListItem('[COLOR green]Featured[/COLOR]', True, url +'trakt_Shows&name=featured')
	common.createListItem('Most Popular', True, url +'trakt_Shows&name=trending')
	common.createListItem('Highly Rated', True, url +'trakt_Shows&name=top_rated')
	common.createListItem('Airing This Week', True, url +'trakt_Shows&name=on_the_air')
	common.createListItem('Airing Today', True, url +'trakt_Shows&name=airing_today')
	xbmcplugin.endOfDirectory(int(sys.argv[1]))
	
def MovieMenu():  #homescreen
	print 'Streamcub Movie menu'
	url = sys.argv[0]+'?action='
	common.createListItem('Search Movie', True, url+'trakt_SearchMovies')
	common.createListItem('[COLOR green]Genres[/COLOR]', True, url +'trakt_MovieGenres')
	common.createListItem('Most Popular', True, url +'trakt_Movies&name=trending')
	#common.createListItem('Playing in theaters', True, url +'trakt_Movies&name=now_playing')
	common.createListItem('[COLOR green]Highly rated[/COLOR]', True, url +'trakt_Movies&name=top_rated')
	common.createListItem('[COLOR green]Featured[/COLOR]', True, url +'trakt_Movies&name=featured')
	common.createListItem('[COLOR green]Revenue[/COLOR]', True, url +'trakt_Movies&name=revenue')
	#common.createListItem('Upcoming', True, url +'trakt_Movies&name=upcoming')
	xbmcplugin.endOfDirectory(int(sys.argv[1]))

def LiveTVMenu(cat):  #homescreen
	print 'Streamcub Live TV menu'
	dialog = xbmcgui.Dialog()
	dialog.ok("Upgrade", "Your Cloudberry software is out of date",
		"Visit www.cloudberrybox.com/upgrade to upgrade your box.",
		"The update includes over 1000 new Live TV channels.")

def check_sources_xml(path):
    try:
        source_path = os.path.join(xbmc.translatePath('special://profile/'), 'sources.xml')
        f = open(source_path, 'a+')
	f.seek(0)
        content = f.read()
        f.close()
        path = str(path).replace('\\', '\\\\')
        if re.search(path, content):
            return True
    except:
        xbmc.log("Could not find sources.xml!")   
    return False

def startup():
	if len(settings.getSetting('username')) < 1:
		dialog = xbmcgui.Dialog()
		dialog.ok("Login", "Please login to your Streamcub account.",
			"Get a free account at www.streamcub.com")
		settings.openSettings()

	if len(settings.getSetting('username')) > 0:
		dialog = xbmcgui.Dialog()
		login_ok = furklib.login(settings.getSetting('username'),settings.getSetting('password'));
		if not login_ok and dialog.yesno("Login failed", "Do you want to view your settings?"):
			settings.openSettings()
		return login_ok
	else:
		return False

xbmc.log('params_str=%s' % sys.argv[2])       
params = parse_qs(sys.argv[2])
if not params:
        params['action'] = 'dirs'
try:
	action = params['action']
except:
	params['action'] = 'dirs'
xbmc.log('_params=%s' % params) 


if(params['action'] == 'search'):
        # Search
        keyboard = xbmc.Keyboard(settings.getSetting('last_cache_search'), 'Search')
        keyboard.doModal()

        if keyboard.isConfirmed():
                query = keyboard.getText()
                settings.setSetting('last_cache_search', query)
                searcher.SearchFromMenu(query)

elif(params['action'] == 'myFiles'):
         searcher.getMyFiles()


elif(params['action'] == 'listFiles'):
	id = params['id']
	searcher.ListFiles(id)

elif(params['action'] == 'scrapeMovie'):
	title = params['title']
	year = params['year']
	common.createMovieStrm(title,year,MOVIES_PATH)
	common.Notification ('Added to library:',title)
	xbmc.executebuiltin('UpdateLibrary(video)')

elif(params['action'] == 'ShowMenu'):
	ShowMenu()

elif(params['action'] == 'MovieMenu'):
	MovieMenu()

elif(params['action'] == 'LiveTVMenu'):
	try:
		LiveTVMenu(params['category'])
	except:
		LiveTVMenu(None)

elif(params['action'] == 'Trailers'):
	xbmc.executebuiltin("XBMC.RunScript(special://home/addons/plugin.video.streamcub/trailers.py)")

elif(params['action'] == 'SearchMe'):
    # Search
    type = params['type']
    year= 0
    season = 0
    episode = 0
    movie = None
    episodedata = None
    if type=='Show':
        type = params['type']
        season = params['season']
        episode = params['episode']
        title = params['title']
        try:
            tvdbid = params['tvdbid']
        except:
		    tvdbid = None
        if tvdbid:
            episodedata = traktlib.getEpisodeInfo(tvdbid,season,episode)
        else:
            episodedata = None
            
    elif type=='Movie':
        imdbid = params['imdbid']
        movie = common.getMovieInfobyImdbid(imdbid)
        if movie:
			title = movie['title']
			year = movie['year']
        else:
			title = params['title']
			year = params['year']
    else:
		type = 'Movie'
		title = params['query']
        
    go = False
    try:
        go = params['go']
        if go:
            go=True
    except:
		go = False

	

    print go
    myname,myurl = searcher.SearchDialog(type,title,year,season,episode,go)



    if myurl:
		#common.Notification("Found"," and playing!")
        time.sleep(1)
        listitem = xbmcgui.ListItem(myname, path=myurl)
        listitem.setLabel(myname)
        listitem.setProperty("IsPlayable", "true")
        if movie:
		          common.addMovieInfotoPlayListitem(listitem,movie)
			#common.Notification("Found"," Movie!")
			
        elif episodedata:	
			common.addEpisodeInfotoListitem(listitem,episodedata)

        xbmcplugin.setResolvedUrl(int(sys.argv[ 1 ]),True,listitem)
        if go:
			xbmc.Player().play(myurl, listitem)
        else:
            xbmcplugin.setResolvedUrl(int(sys.argv[ 1 ]),False,xbmcgui.ListItem())

elif(params['action'].startswith('imdb_')):
	imdb.imdbAction(params)

elif(params['action'].startswith('trakt_')):
	trakt.traktAction(params)

elif(params['action'] == 'traktlib'):
	try:
		fg = params['fg']
	except:
		fg = 'True'
	totalAdded = trakt.addToXbmcLib(fg)

	if totalAdded>0:
		common.Notification('Trakt', '{0} were added'.format(totalAdded))
	xbmc.executebuiltin('UpdateLibrary(video)')
#	if fg=='False':
#		settings.startTimer()


elif(params['action'] == 'download'):
	id = params['id']
	furklib.addDownload(id)
	Notification('File added')

elif(params['action'] == 'delete'):
	id = params['id']
	furklib.deleteDownload(id)

elif(params['action'] == 'setup'):
	settings.openSettings()

	if len(settings.getSetting('username')) > 0:
		furklib.login(settings.getSetting('username'),settings.getSetting('password'))
else:
	xbmc.log('argv=%s' % sys.argv)
	if (MYCONTEXT == 'video'):
		common.createCachePath()
		if startup() :
			AddonMenu()
                
print 'Closing Streamcub'
#sys.modules.clear()





