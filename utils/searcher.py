import xbmcgui,xbmc,xbmcplugin
import re
import sys,unicodedata
from sites import furklib
from utils import common,settings
from ext.titles.series import SeriesParser
from ext.titles.movie import MovieParser
from ext.titles.parser import TitleParser, ParseWarning
from ext.hurry.filesize import size

quality_options = []
quality_urls = []
quality_cleanname =[]
quality_ids =[]
unquality_options = []
unquality_urls = []
unquality_cleanname =[]
unquality_ids =[]
unique_qualities = []


def SearchFromMenu(query):
	#xbmcplugin.setContent(int(sys.argv[1]), 'movies')
	dirs = furklib.searchFurk(query)
	if dirs:
		for dir in dirs:
			#if dir['is_ready']=='0':
			#	continue
			id = dir['info_hash']
			dirname = dir['name']
			url = sys.argv[0]+'?action=listFiles&id='+id

			if dir['is_ready']=='0':
				dirname = '[COLOR red]' + dirname + '[/COLOR]'
			
			if (dir.has_key('type') and dir['type'] == 'video' and dir.has_key('ss_urls') and dir.has_key('video_info')):			
				common.createFurkSearchListItem(dirname, True, url, dir['ss_urls'][4], dir['video_info'], id)
		common.endofDir()
	return

def getMyFiles():
	dirs = furklib.myFiles()
	if dirs:
		for dir in dirs:
			if dir['is_ready']=='0':
				continue
			id = dir['info_hash']
			dirname = dir['name']
			url = sys.argv[0]+'?action=listFiles&id='+id
			#if dir['av_result'] == 'ok' and dir['is_ready'] == '1':
			#	common.createListItem('[COLOR green]' + dirname + '[/COLOR]', True, url)
			#elif dir['av_result'] == 'error':
			#	common.createListItem('[COLOR red]' + dirname + '[/COLOR]', True, url)
			#else:
			common.createListItem(common.CleanFileName(dirname), True, url)
			
		common.endofDir()
	return

def showAccountPicture():
	xbmc.executebuiltin("ShowPicture(http://streamcub.com/api/bwusage.php?username=" + 
		settings.getSetting('username') + "&password=" + settings.getSetting('password') + ")");
	return

def download(id):
	dialog = xbmcgui.Dialog()
	if dialog.yesno("Download", "This file is not cached", "Would you like us to download it for you?", 'We will send you an e-mail when it is done'):
		furklib.addDownload(id)
		dialog.ok('Download started' , 'You can view this file under', '[My files] when download is complete')
	return

def ListFiles(id):
	files = furklib.fileInfo(id)
	
	if not files:
		download(id)
		return
	
	for f in files:
		
		if not f.has_key('url_dl'):
			download(id)
			return
		
		myname = f['name']
		myurl = f['url_dl']
		common.createListItem(myname, False, myurl)
	common.endofDir()
	return

def SearchDialog(type,title,year,season,number,go=False):
	global quality_options
	global quality_urls
	global quality_cleanname 
	global quality_ids
	global unquality_options
	global unquality_urls
	global unquality_cleanname
	global unquality_ids
	global unique_qualities

	if go:
		updateDialog = xbmcgui.DialogProgress()
		updateDialog.create("Streamcub Library", "Searching")
		updateDialog.update(20, "searching", title)	
	

	title = common.CleanFileName(title)

	if type=='Movie':
		if year==0:
			query = '{0} -cam'.format(title)
			dirs = furklib.searchFurk(query)
		else:
			query = '{0} {1} -cam'.format(title,year)
			dirs = furklib.searchFurk(query)
	elif type=='Show':

		query = '''{0} S{1:0>2}E{2:0>2}'''.format(title, season, number)
		dirs = furklib.searchFurk(query)
		
	else:
		query = title
		dirs = furklib.searchFurk(title)
	if go:
		updateDialog.close()
	k = 0
	found720p = False
	foundDvd = False
	foundAtleastOneCached = False
	if go:
		pDialog = xbmcgui.DialogProgress()
		pDialog.create('Searching for files')
	count = 0
	
	if dirs:
		for file in dirs:
			count = count + 1
			percent = int(float(count * 100) / len(dirs))
			text = "%s files found ->" % len(quality_options) 
			for qual in unique_qualities:
				text = text + qual +','
			if go:
				pDialog.update(percent, text)
				if pDialog.iscanceled(): 
					pDialog.close()
					break

			if settings.getSetting('search_only_cached_files')=='true' and file['is_ready']=='0':
				continue
			id = file['info_hash']
			dirname = file['name']
			mysize = size(int(file['size']))
			valid = False

			#print ('Dirname ' + dirname)
			dirname =  common.CleanFileName(dirname)

			if type=='Show':

				myParser= guess_series(dirname)
				if myParser:
					myParser.parse()
					myName = myParser.name 
					mySeason = myParser.season
					myNumber = myParser.episode
					myYear = 0
					myNametoCheck = common.CleanFileName(myName).lower().replace(' ','')
					titletoCheck = common.CleanFileName(title).lower().replace(' ','')
					if myParser.quality: myquality = myParser.quality
					movie_name =  '''{0} {1} S{2:0>2}E{3:0>2}'''.format(myquality,myNametoCheck, mySeason, myNumber)					
					
					if int(mySeason) <> int(season):
						break
					elif titletoCheck == myNametoCheck and int(mySeason)==int(season) and int(myNumber)==int(number) and myquality.value>0:
						valid= True

					#Notification(mycheck.lower(),query.lower())
					if valid:
						if file['is_ready']=='0':
							movie_name =  '[COLOR red]' + dirname + '[/COLOR]'
						else:
							movie_name =  dirname
							foundAtleastOneCached = True

						#Notification('Quality:',str(myquality))
						quality_options.append('[' + mysize + '] '+str(myquality) + ' ' + movie_name)
						quality_ids.append(file['info_hash'])
						quality_cleanname.append(dirname)
						quality_urls.append(None)
						if not str(myquality) in unique_qualities:
							unique_qualities.append(str(myquality))
				else:
					# Notification ('cannot parse' , dirname)
					continue
	
			elif type=='Movie':
				valid = False
				parser = MovieParser()
				parser.data = dirname
				parser.parse()
				myName = parser.name 
				myYear = parser.year
				myquality = parser.quality
				movie_name = ''
				if file['is_ready']=='0':
					if file.has_key('type') and file['type'] == 'video':
						movie_name =  '[COLOR red]' + str(myquality) + ' ' + dirname + '[/COLOR]'
					else:
						continue
				else:
					movie_name = str(myquality) + ' ' + dirname
				movie_name2 = str(myquality) + ' ' + title.strip() + ' (' + str(year) + ')'
			

				if int(settings.getSetting('file_size_filter')) > 0 and int(file['size']) > (int(settings.getSetting('file_size_filter')) * 1024 * 1024 * 1024):
					continue

				if year==0 and title.lower() in myName.lower():
					valid = True
				if not myYear:
					myYear = 0
					valid = False
				title = unicodedata.normalize('NFKD',unicode(title,'utf-8')).encode('ASCII', 'ignore')
				#print 'T:' + title.lower()
				#print 'M:' + myName.lower() 
				if title.lower() in myName.lower() and myquality.value>250:
					valid = True

				if valid:
					quality_options.append('[' + mysize + '] '+ movie_name)
					quality_cleanname.append(dirname)
					quality_ids.append(file['info_hash'])
					if not str(myquality) in unique_qualities:
						unique_qualities.append(str(myquality))
					
				else:
					unquality_options.append(str(myquality) + ' ' + dirname)
					unquality_ids.append(file['info_hash'])
					unquality_cleanname.append(dirname)

			

	if not foundAtleastOneCached and type=='Show':
		season_episode = "s%.2de%.2d" % (int(season), int(number))
		season_episode2 = "%d%.2d" % (int(season), int(number))
	
		tv_show_season = "%s season %d" % (title, int(season))
		tv_show_episode = "%s %s" % (title, season_episode)

		dirs2 = []
		try:
			dirs2.extend(furklib.searchFurk(tv_show_episode))
		except:
			pass
		try:
			dirs2.extend(furklib.searchFurk(tv_show_season))
		except:
			pass

		# dirs2 = files
		titletoCheck = re.sub(r'\([^)]*\)', '', title)
		titletoCheck = common.CleanFileName(titletoCheck).lower()

		dir_names = []
		dir_ids = []
		
		count = 0

		for d in dirs2:
			
			count = count + 1
			percent = int(float(count * 100) / len(dirs2))
			text = "%s files found ->" % len(quality_options) 
			for qual in unique_qualities:
				text = text + qual +','
			if go:
				pDialog.update(percent, text)
			if pDialog.iscanceled(): 
				pDialog.close()
				break

			if settings.getSetting('search_only_cached_files')=='true' and d['is_ready']=='0':
				continue
			
			dirnametoCheck=common.CleanFileName(d['name']).lower()
			print 'title:'+titletoCheck
			print 'dirname:'+dirnametoCheck
			if dirnametoCheck.startswith(titletoCheck) and 'season' in dirnametoCheck and str(season) in dirnametoCheck:
				print 'filebyfile for:'+dirnametoCheck
				filebyfile(False,d['info_hash'],d['name'],title,year,season,number)
			
		
		for d in dirs2:
			if d['is_ready']=='0':
				continue
			if not (d['name'].lower().startswith(title.lower())):
				continue
			dir_names.append(d['name'])
			dir_ids.append(d['info_hash'])
					
		
		if len(dir_names)>0:
			idx = 0
			for dirname in dir_names:
				id = dir_ids[idx]
				idx = idx + 1 
				filebyfile(False,id,dirname,title,year,season,number)
				if pDialog.iscanceled(): 
					pDialog.close()
	        		break
		else:
			pass

	if go:	
		pDialog.close()
	
	if len(quality_options) >= 1:
		dialog = xbmcgui.Dialog()
		quality_select = dialog.select('Select quality', quality_options)
	else:
		quality_select = -1
	
	if len(quality_options) == 0:
		dialog = xbmcgui.Dialog()	
		dialog.ok("Error", "Nothing found", "" )	

	# common.Notification ('Selected' , str(quality_select))
	if quality_select == -1:
		return None,None
	else:
		if type=='Show':
			
			try:
				myurl = quality_urls[quality_select]
				if myurl:
					myname = quality_cleanname[quality_select]
				else:
					raise Exception("empty url")
			except: 
				myid = quality_ids[quality_select]
				files = furklib.fileInfo(myid)
				
				if not files:
					download(myid)
					return None,None
				
				k = k + 1
				for f in files:
					myname = f['name']
					#print myname
					if 'sample' in myname.lower():
						continue
					if myname.endswith('avi') or myname.endswith('mkv') or myname.endswith('mp4') or myname.endswith('wmv'):
						myurl = f['url_dl']
						break
					else:
						continue
								
		elif type=='Movie':
			myid = quality_ids[quality_select]
			files = furklib.fileInfo(myid)
			myurl = None
			if not files:
				download(myid)
				return None,None
			
			for f in files:
				myname = f['name'].lower()
				#print myname
				if 'sample' in myname:
					continue
				if myname.endswith('avi') or myname.endswith('mkv') or myname.endswith('mp4') or myname.endswith('iso') or myname.endswith('wmv'):
					myurl = f['url_dl']
					myname = f['name']
					break
				else:
					continue

		#common.Notification('Found',myname)
		if myurl:
			return myname,myurl
		else:
			common.Notification('Not Found' , 'Please try again')
			return None,None

def guess_series(title):
        """Returns a valid series parser if this :title: appears to be a series"""
        #print 'title=' + title.encode("utf-8")
        parser = SeriesParser(identified_by='ep', allow_seasonless=False)
        # We need to replace certain characters with spaces to make sure episode parsing works right
        # We don't remove anything, as the match positions should line up with the original title
        clean_title = re.sub('[_.,\[\]\(\):]', ' ', title)
        match = parser.parse_episode(clean_title)
        if match:
            if parser.parse_unwanted(clean_title):
                return
            elif match['match'].start() > 1:
                # We start using the original title here, so we can properly ignore unwanted prefixes.
                # Look for unwanted prefixes to find out where the series title starts
                start = 0
                prefix = re.match('|'.join(parser.ignore_prefixes), title)
                if prefix:
                    start = prefix.end()
                # If an episode id is found, assume everything before it is series name
                name = title[start:match['match'].start()]
                # Remove possible episode title from series name (anything after a ' - ')
                name = name.split(' - ')[0]
                # Replace some special characters with spaces
                name = re.sub('[\._\(\) ]+', ' ', name).strip(' -')
                # Normalize capitalization to title case
                name = name.title()
                # If we didn't get a series name, return
                if not name:
                    return
                parser.name = name
                parser.data = title
		
                try:
                    parser.parse(data=title)
                except ParseWarning, pw:
                    common.Notification('ParseWarning:' , pw.value)
                if parser.valid:
                    return parser

def filebyfile(append,id,dirname,title,year,season,number):
		global quality_options
		global quality_urls
		global quality_cleanname 
		global quality_ids
		global unquality_options
		global unquality_urls
		global unquality_cleanname
		global unquality_ids
		global unique_qualities

		valid = False
		title = re.sub(r'\([^)]*\)', '', title)
		titletoCheck = common.CleanFileName(title).lower().replace(' ','')

		#print 'Dir:{0}'.format(dirname)
		files = furklib.fileInfo(id)
		if not files:
			return

		for f in files:
			name = f['name']
			path = f['path'].replace('/',' ')
			mysize = size(int(f['size']))
			if 'sample' in name.lower() or 'subs' in name.lower():
				continue
			play_url = f['url_dl']
			valid = False
			myquality = 'unknown Akin'
			myParser= guess_series(name)
			if not myParser:
				myParser= guess_series(title + ' ' + name)
			if not myParser:
				myParser= guess_series(title + ' ' + path + name)
			movie_name = dirname + ' ' + path + name
			if myParser:
				try:
					myParser.parse()
				except:
					continue
				myName = myParser.name 
				mySeason = myParser.season
				myNumber = myParser.episode
				myYear = 0
				if myParser.quality: myquality = myParser.quality
				myNametoCheck = common.CleanFileName(myName).lower().replace(' ','')
				
				movie_name = '''{0} {1} S{2:0>2}E{3:0>2}'''.format(myquality,myName, mySeason, myNumber)
				movie_name2 = '''B:{0} {1} S{2}E{3}'''.format('unk',title, season, number)
				clean_name = '''{1} S{2:0>2}E{3:0>2}'''.format(myquality,myName, mySeason, myNumber)
				#print 'U: {0} S{1}E{2}'.format(myNametoCheck,mySeason,myNumber)
				#print 'Y: {0} S{1}E{2}'.format(titletoCheck,season,number)
				if not myNametoCheck.startswith(titletoCheck):
					#print 'break namecheck'
					break
				if int(mySeason)==int(season) and int(myNumber)==int(number):
					valid= True
	
			if valid:
				if append:
					quality_options.append('[' + mysize + '] '+str(myquality) + ' ' + name)
					quality_cleanname.append(clean_name)
					quality_urls.append(play_url)
					if not str(myquality) in unique_qualities:
						unique_qualities.append(str(myquality))
					break
				else:
					quality_options.insert(0, '[' + mysize + '] '+str(myquality) + ' ' + name)
					quality_cleanname.insert(0, clean_name)
					quality_urls.insert(0, play_url)
					if not str(myquality) in unique_qualities:
						unique_qualities.insert(0, str(myquality))
					break
			else:
				if append:
					unquality_options.append('[' + mysize + '] '+movie_name)
					unquality_cleanname.append(movie_name)
					unquality_urls.append(play_url)
				else:
					unquality_options.insert(0, '[' + mysize + '] '+movie_name)
					unquality_cleanname.insert(0, movie_name)
					unquality_urls.insert(0, play_url)
		return

def listfiles(id):
	files = furklib.fileInfo(id)
	if files:
		for f in files:
			myname = f['name']
			if 'sample' in myname.lower() or 'subs' in myname.lower():
				continue
			play_url = f['url_dl']
			if myname.endswith('avi') or myname.endswith('mkv') or myname.endswith('mp4') or myname.endswith('iso') or myname.endswith('mov') or myname.endswith('wmv'):
				quality_options.append(myname)
				quality_cleanname.append(myname)
				quality_urls.append(play_url)
				
	return
			