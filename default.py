import sys, urllib, time, re, os
import xbmc, xbmcaddon, xbmcgui, xbmcplugin
import context
from utils import settings


# Plugin constants
__plugin__ = 'Streamcub Library'
__author__ = 'Streamcub Team'
__url__ = 'http://www.streamcub.com'
__version__ = '1.2.1'

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
	common.createListItem('Live TV',True,url + 'LiveTVMenu')
	common.createListItem('Search all torrents', True, url+'search')
	common.createListItem('Setup',False,url +'setup')
	xbmcplugin.endOfDirectory(int(sys.argv[1]))

def ShowMenu():  #homescreen
	print 'Streamcub TV show menu'
	url = sys.argv[0]+'?action='
	common.createListItem('Search TV Show', True, url+'trakt_SearchShows')
	common.createListItem('Genres', True, url +'trakt_ShowLists&type=Show')
	common.createListItem('Featured', True, url +'trakt_getList&user=cloudberry&slug=show-featured')
	common.createListItem('Most Popular', True, url +'trakt_TrendingShows')
	common.createListItem('Highly rated', True, url +'trakt_getList&user=cloudberry&slug=show-highly-rated')
	xbmcplugin.endOfDirectory(int(sys.argv[1]))
	
def MovieMenu():  #homescreen
	print 'Streamcub Movie menu'
	url = sys.argv[0]+'?action='
	common.createListItem('Search Movie', True, url+'trakt_SearchMovies')
	common.createListItem('Genres', True, url +'trakt_ShowLists&type=Movie')
	common.createListItem('Featured', True, url +'trakt_getList&user=cloudberry&slug=movie-featured')
	common.createListItem('Most Popular', True, url +'trakt_TrendingMovies')
	common.createListItem('Highly rated', True, url +'trakt_getList&user=mmounirou&slug=imdb-best-250-movies')	
	xbmcplugin.endOfDirectory(int(sys.argv[1]))

def LiveTVMenu(cat):  #homescreen
	print 'Streamcub Live TV menu'
	url = sys.argv[0]+'?action='
	if cat == 'turkish':
		common.createStreamListItem('1 - A Haber', 'http://www.blogsitesi.net/wp-content/uploads/2012/12/a-haber.jpg', 'rtmp://5.63.151.6:443/ahaber playpath=ahaber3 swfUrl=http://i.tmgrup.com.tr/p/flowplayer-3.2.9.swf?i=2 pageUrl=http://www.ahaber.com.tr/webtv/videoizle/ahaber/canli_yayin')
		common.createStreamListItem('2 - XN HD', 'http://us.123rf.com/400wm/400/400/6kor3dos/6kor3dos1207/6kor3dos120700011/14519487-3d-person-with-red-question-mark.jpg', 'rtmp://win5.yayinda.org/telecine/telecine')
		common.createStreamListItem('3 - Star TV', 'http://www.tvnetonline.com/logolar/tr/star_tv_tr.jpg', 'http://85.132.71.4:1935/turktv/startv.sdp/playlist.m3u8')
		common.createStreamListItem('4 - Kanal D', 'http://www.canlitv4.com/images/kanallar/kanald.jpg', 'rtmp://85.132.71.4:1935/turktv/kanald.sdp swfUrl=http://www.livetv.az/static/player/player.swf pageUrl=http://www.livetv.az/kanald swfVfy=1 live=1 timeout=15 ')
		common.createStreamListItem('5 - Kanal D (alternativ)', 'http://www.canlitv4.com/images/kanallar/kanald.jpg', 'rtmp://85.132.44.99:1935/turktv playpath=kanald.sdp swfUrl=http://www.livetv.az/static/player/player.swf pageUrl=http://www.livetv.az/kanald live=1')
		common.createStreamListItem('6 - Show TV', 'http://www.tvnetonline.com/logolar/showtv.jpg', 'rtmp://mn-l.mncdn.com/showtv/ playpath=showtv2 swfUrl=http://static.oroll.com/p.swf?v=21.79&amp;ts=15-12-2013 pageUrl=http://www.showtv.com.tr/canli-yayin live=1 timeout=15')
		common.createStreamListItem('7 - ATV (alternativ)', 'http://www.cetsohbet.com/canli-tv-izle/resimler/atv.jpg', 'rtmp://159.253.145.140/atv playpath=atv3 swfUrl=http://i.tmgrup.com.tr/p/flowplayer-3.2.10.swf?i=2 pageUrl=http://www.atv.com.tr/webtv/canli-yayin')
		common.createStreamListItem('8 - ATV Avrupa', 'http://www.cetsohbet.com/canli-tv-izle/resimler/atv.jpg', 'rtmp://159.253.131.115:443/atveu playpath=atveu3 swfUrl=http://i.tmgrup.com.tr/p/flowplayer-3.2.9.swf?i=2 pageUrl=http://www.atvavrupa.tv/webtv/videoizle/atv_avrupa/canli_yayin')
		common.createStreamListItem('9 - FOX TV', 'http://i.imgur.com/wp3R9.jpg', 'rtmp://edge03-01.az.myvideo.az/dvrh264/foxturk app=dvrh264/foxturk playpath=mp4:foxturk swfUrl=http://www.myvideo.az/dvr/dvrSkip.swf pageUrl=http://www.myvideo.az live=1 timeout=15')
		common.createStreamListItem('10 - TRT 1', 'http://img.webme.com/pic/n/netcanlitvizle/trt11.png', 'http://85.132.44.99:1935/turktv/trt1.sdp/playlist.m3u8')
		common.createStreamListItem('11 - TRT Haber', 'http://www.lyngsat-logo.com/logo/tv/tt/trt_haber.jpg', 'rtmp://mn-l.mncdn.com/trthaber/ playpath=trthaber3 swfUrl=http://mnhst.mncdn.net/players/player/flowplayer.unlimited-3.2.16.swf pageUrl=http://www.trt.net.tr/anasayfa/canli.aspx?y=tv&amp;k=trthaber')
		common.createStreamListItem('12 - TRT Spor', 'http://www.lyngsat-logo.com/logo/tv/tt/trt3_spor.jpg', 'rtmp://edge03-08.az.myvideo.az/dvrh264/trt3 app=dvrh264/trt3 playpath=mp4:trt3 swfUrl=http://www.myvideo.az/dvr/dvrSkip7.swf?v=1.91 pageUrl=http://www.myvideo.az live=1 timeout=15')
		common.createStreamListItem('13 - TRT Turk', 'http://gurbetim.free.fr/3/canli_canli_tv/logo/trt_turk.jpg', 'rtmp://mn-l.mncdn.com/trtturk/ playpath=trtturk3 swfUrl=http://trt.net.tr/js/jwplayer.flash.swf pageUrl=http://trt.net.tr/Anasayfa/canli.aspx?y=tv&amp;k=trtturk live=1 timeout=15')
		common.createStreamListItem('14 - TRT Muzik', 'http://www.turkishdelight.de/tv/trtmuzik.jpg', 'mms://95.0.159.131/TRTMUZIK')
		common.createStreamListItem('15 - TRT6', 'http://kurdistancommentary.files.wordpress.com/2010/12/trt6.png', 'rtmp://mn-l.mncdn.com/trt6/trt61 swfUrl=http://www.trt.net.tr/js/jwplayer.flash.swf pageUrl=http://www.trt.net.tr/anasayfa/canli.aspx?y=tv&amp;k=trt6')
		common.createStreamListItem('16 - TV8', 'http://gurbetim.free.fr/3/canli_canli_tv/tv_izle/Haber_kanallar/logo/tv8_tr.jpg', 'rtmp://strm-3.tr.medianova.tv/tv8/tv8_live3 pageUrl=http://www.tv8.com.tr swfUrl=http://static.oroll.com live=1')
		common.createStreamListItem('17 - TV8 (alternativ)', 'http://gurbetim.free.fr/3/canli_canli_tv/tv_izle/Haber_kanallar/logo/tv8_tr.jpg', 'rtmp://strm-3.tr.medianova.tv/tv8/ playpath=tv8_live3 swfUrl=http://static.oroll.com/p.swf?v=18.75 pageUrl=http://www.tv8.com.tr/iyitelevizyon-webtv swfVfy=1 live=true')
		common.createStreamListItem('18 - KANAL 7', 'http://www.lyngsat-logo.com/logo/tv/kk/kanal7_tr.jpg', 'http://iphone.gostream.nl/kanal7iphone/smil:kanal7.smil/playlist.m3u8')
		common.createStreamListItem('19 - CNN Turk', 'http://gurbetim.free.fr/3/canli_canli_tv/tv_izle/Haber_kanallar/logo/cnn_turk.jpg', 'rtmp://dcdn.motiwe.com:1935/dogantv/_definst_/arizatv/ playpath=cnnturk.stream swfUrl=http://www.ecanlihdtvizle.com/wp-content/plugins/proplayer/players/player.swf pageUrl=http://www.ecanlihdtvizle.com/cnn-turk/')
		common.createStreamListItem('20 - Haberturk', 'http://www.tubeturk.net/tv/resimler/haberturk.jpg', 'rtmp://live-ciner.mncdn.net/haberturk/ playpath=haberturk2 swfUrl=http://www.haberturk.com/images/flash/flowplayer.commercial-3.1.5.swf pageUrl=http://www.haberturk.com/canliyayin live=true swfVfy=true timeout=10')
		common.createStreamListItem('21 - SamanyoluTV', 'http://www.dizi.info.tr/wp-content/uploads/2009/09/samanyolu1.jpg', 'rtmp://fml.ams.1B3E.edgecastcdn.net/201B3E playpath=STVEU1 swfUrl=http://www.hdtvizle.com/proplayer/players/player.swf live=1 pageUrl=http://www.hdtvizle.com/166-samanyolu-avrupa-hd-izle.html')
		common.createStreamListItem('22 - Samanyolu Haber', 'http://www.canli-radyo-dinle.org/images/logo/tv/stv_haber.jpg', 'mms://yayin.canlitv.com/shaber')
		common.createStreamListItem('23 - Kanal24', 'http://www.anten.de/images/kanal24.jpg', 'rtmp://strm-3.tr.medianova.tv/kanal24/kanal243 swfUrl=http://releases.flowplayer.org/swf/flowplayer-3.2.15.swf pageUrl=http://www.canlitvizled.org/wp-content/list/kanal24.html live=true swfVfy=true timeout=10')
		common.createStreamListItem('24 - Kanal A', 'http://www.lyngsat-logo.com/logo/tv/kk/kanal_a_tr.jpg', 'rtmp://yayin.yayin.tv.tr:1935/kanala/ playpath=kanala1 swfUrl=http://www.hdtvizle.com/proplayer/players/player.swf pageUrl=http://www.hdtvizle.com/33-kanal-a-hd-izle.html live=true swfVfy=true timeout=10')
		common.createStreamListItem('25 - Kanal A (alternativ)', 'http://www.lyngsat-logo.com/logo/tv/kk/kanal_a_tr.jpg', 'rtmp://yayin.yayin.tv.tr:1935/kanala/kanala2')
		common.createStreamListItem('26 - World Travel Channel', 'http://www.lyngsat-logo.com/logo/tv/ww/world_travel_channel.jpg', 'rtsp://stream.taksimbilisim.com:1935/wtc/bant1')
		common.createStreamListItem('27 - Kanal T', 'http://www.lyngsat-logo.com/logo/tv/kk/kanal_t.jpg', 'rtmp://213.128.67.74/live/kanalt1')
		common.createStreamListItem('28 - NTV', 'http://img.webme.com/pic/n/netcanlitvizle/ntv1.png', 'rtmp://85.132.44.99:1935/turktv/ntv.sdp swfUrl=http://www.livetv.az/static/player/player.swf pageUrl=http://www.livetv.az/ntv swfVfy=true timeout=10')
		common.createStreamListItem('29 - NTV SPOR', 'http://www.mobilcanlitv.com/KanalResim/ntvspor.jpg', 'mmsh://85.111.3.55:80/ntvspor')
		common.createStreamListItem('30 - Tv2', 'http://4.bp.blogspot.com/-jkheVbM35UI/UGXU1ZwP4cI/AAAAAAAAHes/UZm8T6djpao/s1600/tv2.jpg', 'rtmp://85.132.44.99:1935/turktv/tv2.sdp swfUrl=http://www.livetv.az/static/player/player.swf pageUrl=http://www.livetv.az/tv2 swfVfy=true timeout=10')
		common.createStreamListItem('31 - SportsTV', 'http://4.bp.blogspot.com/-IE6g3oCm2b4/UG8orflc6LI/AAAAAAAAJRA/UoLG36SkibM/s1600/sports-tv.png', 'rtmp://stream.sportstv.com.tr/sportstv/SportsTV3')
		common.createStreamListItem('32 - GS TV', 'http://cdn.galatasaray.org/images/HEADER-TR.jpg', 'rtmp://cdn21.motiwe.com/live/gstv370 app=live pageURL=http://gsstore.org/dosyalar/facebook/gstvvv/ swfUrl=http://cdn3.motiwe.com/player/player.swf live=true')
		common.createStreamListItem('33 - BJK TV', 'http://www.bjktv.org/files/logo/70be4667a0.png', 'rtmp://extondemand.livestream.com/ondemand playpath=mp4:trans/dv15/mogulus-user-files/ch27182818314/2013/06/11/af5d3b3b-3237-4d60-968a-275300410d8c.mp4 swfUrl=http://cdn.livestream.com/chromelessPlayer/v21/playerapi.swf?allowchat=false&amp;autoPlay=true&amp;mode=false&amp;color=0x000000&amp;hideInfo=true&amp;hideChannelBranding=false&amp;showMoreVideos=false&amp;textLines=2&amp;iconColorOver=0xe7e7e7&amp;t=343909&amp;time=&amp;lschannel=true&amp;browseMode=false&amp;jsEnabled=false pageUrl=http://www.livestream.com/embed/27182818314?&amp;color=0x000000&amp;iconColorOver=0xe7e7e7&amp;showMoreVideos=false&amp;hideInfo=true&amp;autoPlay=true&amp;lschannel=true&amp;browseMode=false&amp;textLines=2&amp;hideChannelBranding=false&amp;mode=false&amp;allowchat=false&amp;layout=4&amp;t=343909')
		common.createStreamListItem('34 - Cagri Tv', 'http://www.teknikportal.com/image-uploads/cagri-tv-frekansi-0.jpg', 'rtmp://yayin5.canliyayin.org/live/cagritv pageURL=http://hd-canlitv-izle.blogspot.dk/2012/06/cagr-tv-canl-izle-cagr-tv-izle.html swfUrl=http://www.hdtvizle.com/proplayer/players/player.swf live=true&lt;/link&gt;')
		common.createStreamListItem('35 - SkyTurk', 'http://www.haberahval.com/wp-content/uploads/2013/01/sky-turk3.jpg', 'rtmp://stream.pivol.com:1935/livestream/ playpath=skyturk360 swfUrl=http://www.creare-design.co.uk/jwplayer/jwplayer.flash.swf pageUrl=http://www.webtentvizle.com/2013/08/skyturk-360-canl-izle.html swfVfy=true timeout=10')
		common.createStreamListItem('36 - FOX Belgesel', 'http://www.canliizleyin.com/content/icons/fox-belgesel-icon-1.png', 'http://yayin.networkbil.com/foxbelgesel')
		common.createStreamListItem('37 - A HABER ', 'http://www.lyngsat-logo.com/logo/tv/aa/a_haber.jpg', 'rtmp://185.2.138.220:443/ahaber playpath=ahaber3 swfUrl=http://i.tmgrup.com.tr/p/flowplayer-3.2.9.swf?i=2 pageUrl=http://www.ahaber.com.tr/webtv/videoizle/ahaber/canli_yayin live=1')
		common.createStreamListItem('38 - MINIKA COCUK', 'http://www.benimtv.com/admin/userimages/tu-minika-go.gif', 'rtmp://159.253.131.115/minika playpath=minika3 swfUrl=http://i.tmgrup.com.tr/mnka/player/TMDMedia/TMDPlayer327.swf pageUrl=http://www.minika.com.tr/minika_tv/minikago live=1')
		common.createStreamListItem('39 - Karamel TV', 'http://www.lyngsat-logo.com/logo/tv/kk/karamel_tv.jpg', 'rtmp://strm-3.tr.medianova.tv/karamel/karamel')
		common.createStreamListItem('40 - PLANET COCUK', 'http://www.lyngsat-logo.com/logo/tv/pp/planet_cocuk.jpg', 'rtmp://planetler.ercdn.net:1935/live/planet2 swfUrl&gt;http://fpdownload.adobe.com pageUrl&gt;http://www.planetler.com')
		common.createStreamListItem('41 - Sinema Turk', 'http://netyayini.com/picture/logo/2204.jpg', 'http://yayin7.canliyayin.org/sinematurk')
		common.createStreamListItem('42 - Sinema Yabanci', 'http://netyayini.com/picture/logo/2220.jpg', 'http://yayin7.canliyayin.org/sinema')
		common.createStreamListItem('43 - Sinema 1', 'http://netyayini.com/picture/logo/2221.jpg', 'http://yayin7.canliyayin.org/sinema1')
		common.createStreamListItem('44 - Sinema 2', 'http://netyayini.com/picture/logo/2222.jpg', 'http://yayin7.canliyayin.org/sinema2')
		common.createStreamListItem('45 - Sinema 3', 'http://netyayini.com/picture/logo/2223.jpg', 'http://yayin7.canliyayin.org/sinema3')
		common.createStreamListItem('46 - Sinema 4', 'http://netyayini.com/picture/logo/2224.jpg', 'http://yayin7.canliyayin.org/sinema4')
		common.createStreamListItem('47 - Kanalsport(danish)', 'http://i8.c.dk/pics/8/9/3/74398/596x341.jpg', 'http://lswb-de-08.servers.octoshape.net:1935/live/kanalsport_2000k/playlist.m3u8')
		common.createStreamListItem('48 - TV5', 'http://4.bp.blogspot.com/-oyNJuvzpBNE/UO3LYWw15PI/AAAAAAAAOpA/eXkTj2_zh6o/s1600/tv5.jpg', 'mmsh://yayin3.canliyayin.org/tv5')
		common.createStreamListItem('49 - Semerkand HD', 'https://encrypted-tbn1.gstatic.com/images?q=tbn:ANd9GcQ0kxm3kTZOZMvVulI876yOJq7u9UOBPfNYOdVLhA161TOi66Nf', 'rtmp://91.194.90.61:1935/Semerkand playpath=Live swfUrl=http://fpdownload.adobe.com/strobe/FlashMediaPlayback.swf/[[DYNAMIC]]/1 pageUrl=http://www.webtentvizle.com/2013/09/semerkand-tv-canl-izle.html')
		common.createStreamListItem('50 - Cine5', 'http://www.derszamani.net/wp-content/uploads/2013/09/cine51.jpg', 'rtmp://cine5.stream.cubecdn.net:1935/cine5 playpath=stream1 swfUrl=http://player.cubecdn.net/swf/smb.swf live=1 pageUrl=http://www.cine5.com.tr/canli-izle.html')
		common.createStreamListItem('51 - SuperSport 3', 'http://www.lyngsat-logo.com/hires/dd/digit_alb_supersport3.png', 'rtmp://81.17.23.118:1935/stream/ playpath=IpUgHhCEPs.stream swfUrl=http://thecdn.04stream.com/p/ooolo1.swf pageUrl=http://www.04stream.com/ebb.php?adsp=&amp;width=600&amp;height=460&amp;st=q4h475o5t4q5b3c325x5n2b4u214y2v27424v203s2t2x264f4&amp;adx=&amp;stream=i554n5e4a474w2u2l5h5q264v2b443n2s4w5v3b4c3f4f3r42516t294y2q274z2w2p2s2d4u2z3x2x2a4m2v4x565p5g3b4p4n4m3v383v5o4e4k5o3t3546484q4r5z334v4y3s2p224c464x244i5s254432384y2n574n5l5t2w2o5h534a4r27413q2l56423z2r233z2343434t2y3s2p224r294r4&amp;sooor=OA==&amp;str=is&amp;idom=firstrownow.eu')
		common.createStreamListItem('52 - SterkTV', 'http://www.sterktv.net/assets/images/logo.png', 'rtmp://178.33.61.33:1936/72/stream live=1 timeout=15')
	elif cat == 'arabic':
		common.createStreamListItem('Al jadeed', '', 'http://origin.etacdn.com/jadeedlive/smil:live.smil/playlist.m3u8')
		common.createStreamListItem('Mtv', '', 'rtmp://livestreaming1.itworkscdn.net/mtvlive playpath=murrtelevision_360p swfUrl=http://mtv.com.lb/Player/485/jwplayer.flash.swf pageUrl=http://mtv.com.lb/Player/704/485 live=1')
		common.createStreamListItem('Lbc Europe', '', 'rtmp://livestreaming.itworkscdn.net/lbclive/lbc_1 playpath=lbc_1 swfUrl=http://www.lbcgroup.tv/livemedia4/jwplayer.flash.swf live=1 pageUrl=http://www.lbcgroup.tv/watch-lbci-live')
		common.createStreamListItem('Al Mayadeen', '', 'rtmp://livestreaming3.itworkscdn.net/mayadeenlive/ playpath=mayadsat swfUrl=http://www.almayadeen.net/content/jwplayer/jwplayer.flash.swf pageUrl=http://www.almayadeen.net/ar/Live swfVfy=true live=true timeout=live')
		common.createStreamListItem('Nbn', '', 'http://www.nbn.com.lb/live/iphone_pl.php')
		common.createStreamListItem('Al Manar', '', 'rtsp://live.almanar.com.lb/live')
		common.createStreamListItem('Futur tv', '', 'rtmp://livestreaming2.itworkscdn.net/ftvlive/ playpath=ftvlive swfUrl=http://itworks-me.net/ftvent/jwplayer.flash.swf live=1 pageUrl=http://itworks-me.net/ftvent/index.html')
		common.createStreamListItem('Skynews Arabia', '', 'rtmp://hd7.lsops.net/live//skynewsi_ar_372')
		common.createStreamListItem('Aljazeera', '', 'rtmp://aljazeeraflashlivefs.fplive.net/aljazeeraflashlive-live/aljazeera_ara_high')
		common.createStreamListItem('Al Jazeera Moubashar', '', 'rtmp://aljazeeraflashlivefs.fplive.net/aljazeeraflashlive-live/aljazeera_mubasher2_high')
		common.createStreamListItem('Al Jazeera Masr', '', 'rtmp://aljazeeraflashlivefs.fplive.net/aljazeeraflashlive-live/aljazeera_misr_high')
		common.createStreamListItem('BBC Arabia', '', 'http://www.bbc.co.uk/arabic/meta/tx/live/atv_live_bb.asx')
		common.createStreamListItem('AL Jazeerah English', '', 'rtmp://aljazeeraflashlivefs.fplive.net/aljazeeraflashlive-live/aljazeera_eng_high')
		common.createStreamListItem('Al Arabia', '', 'http://livestream5.alarabiya.tv/i/live_1@141854/index_1_av-p.m3u8')
		common.createStreamListItem('Melody Aflam', '', 'rtmp://38.96.148.24/MelodyAflam playpath=MAflam_576p swfUrl=http://www.melody.net/flowplayer/flowplayer.commercial-3.2.16.swf pageUrl=http://www.melody.net/pages/view/id/1 live=1 timeout=15')
		common.createStreamListItem('Melody Classic', '', 'rtmp://38.96.148.24/MelodyClassic playpath=MClassic_576p swfUrl=http://www.melody.net/flowplayer/flowplayer.commercial-3.2.16.swf live=1 pageUrl=http://www.melody.net/halilou.com live=1 timeout=15')
		common.createStreamListItem('Melody Hits', '', 'rtmp://38.96.148.24/MelodyHits/MHits_576p')
		common.createStreamListItem('Melody Arabia', '', 'rtmp://38.96.148.24/MelodyArabia playpath=MArabia_576p swfUrl=http://www.melody.net/flowplayer/flowplayer.commercial-3.2.16.swf pageUrl=http://www.melody.net/pages/view/id/24 live=1 timeout=15')
		common.createStreamListItem('Bein+5', '', 'http://hls01-06.az.myvideo.az/hls-live/livepkgr/sport5/sport5/sport5.m3u8')
		common.createStreamListItem('Mbc', '', 'http://mbc-live.hds.adaptive.level3.net/hls-live/mbc-channel02/_definst_/live.m3u8')
		common.createStreamListItem('MBC 2', '', 'http://212.179.77.42/live/livestream2/gmswf.m3u8')
		common.createStreamListItem('Mbc 2', '', 'http://212.179.77.42/live/livestream2/gmswf.m3u8')
		common.createStreamListItem('MBC3', '', 'rtmp://5.63.146.236/live/azsq1299?id=149841 swfUrl=http://mips.tv/content/scripts/eplayer.swf live=1 pageUrl=http://mips.tv/embedplayer/activacion1/1/650/400 conn=S:OK ?live')
		common.createStreamListItem('MBC 3', '', 'rtmp://5.63.146.236/live/azsq1299?id=149841 swfUrl=http://mips.tv/content/scripts/eplayer.swf live=1 pageUrl=http://mips.tv/embedplayer/activacion1/1/650/400 conn=S:OK ?live')
		common.createStreamListItem('MBC 4', '', 'rtmp://206.190.138.68/live playpath=trhtgfjhgjhg?id=147478 swfUrl=http://mips.tv/content/scripts/eplayer.swf live=1 pageUrl=http://mips.tv/embedplayer/activacion1/1/650/400 conn=S:OK ?live')
		common.createStreamListItem('MBC 4', '', 'rtmp://173.193.46.104/live playpath=trhtgfjhgjhg?id=147478 swfUrl=http://mips.tv/content/scripts/eplayer.swf live=1 pageUrl=http://mips.tv/embedplayer/trhtgfjhgjhg/1/600/380 conn=S:OK --live')
		common.createStreamListItem('MBC Action', '', 'rtmp://5.63.146.236/live/ playpath=EFEDFzddac?id=149861 swfUrl=http://mips.tv/content/scripts/eplayer.swf live=1 pageUrl=http://mips.tv/embedplayer/activacion1/1/650/400 conn=S:OK ?live')
		common.createStreamListItem('CBC', '', 'http://iphone-streaming.ustream.tv/ustreamVideo/8707800/streams/live/hasbahca.m3u8')
		common.createStreamListItem('CBC 2', '', 'http://iphone-streaming.ustream.tv/ustreamVideo/12794820/streams/live/hasbahca.m3u8')
		common.createStreamListItem('Dubai one .', '', 'http://cdnedvrdubaione.endavomedia.com/smil:dmilivedubaione.smil/playlist.m3u8')
		common.createStreamListItem('al horriya', '', 'rtmp://fms.pwmcdn.com/alhorreya/alhorreya2')
		common.createStreamListItem('Noorsat', '', 'rtmp://fl1.viastreaming.net/noursat/livestream')
		common.createStreamListItem('Fatafeet', '', 'http://212.179.77.42/live/livestream3/gmswf.m3u8')
		common.createStreamListItem('Al Nabaa Tv', '', 'http://alnabaa.lsops.net/live/alnabaa_ar_hls.smil/playlist.m3u8')
		common.createStreamListItem('Bahrain Sport', '', 'rtmp://alayam.netromedia.net/btv3/btv3')
		common.createStreamListItem('Suryoyo sat', '', 'mms://130.89.163.47:34555')
		common.createStreamListItem('Al kaas hd', '', 'rtmp://fml.44C9.edgecastcdn.net/2044C9/ pageUrl=http://shoof.alkass.net/shoof/?live=1 swfUrl=http://shoof.alkass.net/shoof/jwplayer/player.swf live=1 playpath=hd1?e32719fb7f5675b7285acc2c3c4aaaab2613f2ea2c86da1894bb6c6f1f693d03436df4649356b724cdcbde')
		common.createStreamListItem('Al arabiya al hadath', '', 'http://livestream2.alarabiya.tv/files/hadath.m3u8')
		common.createStreamListItem('Al jazeera Documentary', '', 'rtmp://aljazeeraflashlivefs.fplive.net/aljazeeraflashlive-live/aljazeera_doc_med')
		common.createStreamListItem('Sama Dubai', '', 'rtmp://dmiLiveSamaDubai.flash.internapcdn.net/ app=dmiLiveSamaDubai/live_1 playpath=dmilivesamadubai_3 swfUrl=http://vod.dmi.ae/bundles/endavoenhance/js/lib/jwplayer/jwplayer.flash.swf live=true timeout=15 pageUrl=http://vod.dmi.ae/jwplayer/player16.php?width=630&height=461&channel=samadubai')
		common.createStreamListItem('Dubai Tv', '', 'rtsp://wms03.endavomedia.com:1935/dmi/_definst_/dmilivedubaitv_bb.stream')
		common.createStreamListItem('France 24', '', 'mms://stream1.france24.yacast.net/f24_livefrda')
		common.createStreamListItem('Ksa2', '', 'rtsp://38.96.148.74/CH2TV')
		common.createStreamListItem('AL Hiwar', '', 'rtmp://185.2.136.148/livepkgr/livestream')
		common.createStreamListItem('Al Iraqia', '', 'http://212.7.196.74/iraqia')
		common.createStreamListItem('Nile Family', '', 'rtmp://livestreaming4.onlinehorizons.net/NTNNileFamily playpath=livestream swfUrl=http://niletc.tv/player/player.swf live=1 pageUrl=http://niletc.tv/stream.php?ch=family')
		common.createStreamListItem('Nile Drama- low quality', '', 'rtmp://livestreaming4.onlinehorizons.net/NTNNileDrama playpath=livestream?ch=drama swfUrl=http://ntn.onlinehorizons.net/player/player.swf pageUrl=http://www.ntnegypt.net/stream.php live=1 \par')
		common.createStreamListItem('Nile Comedy - low quality', '', 'rtmp://livestreaming4.onlinehorizons.net/NTNNileComedy/ playpath=livestream swfUrl=http://niletc.tv/player/player.swf pageUrl=http://niletc.tv/stream.php?ch=comedy swfVfy=true live=true timeout=60')
		common.createStreamListItem('Nile Cinema - low quality', '', 'rtmp://livestreaming4.onlinehorizons.net/NTNNileCinema playpath=livestream swfUrl=http://niletc.tv/player/player.swf live=1 pageUrl=http://niletc.tv/stream.php?ch=cinema player=default')
		common.createStreamListItem('BBC', '', 'http://www.bbc.co.uk/arabic/meta/tx/live/atv_live_bb.asx')
		common.createStreamListItem('Orient News', '', 'rtmp://67.228.219.186/live/ playpath=live1 swfUrl=http://www.watcharab.com/tv/swf/orienttv.swf pageUrl=http://www.elahmad.com/tv/orienttv.php swfVfy=true live=true timeout=60')
		common.createStreamListItem('Al Aan', '', 'http://alaan_hls-lh.akamaihd.net/i/alaan_ar@103399/master.m3u8')
		common.createStreamListItem('Sama Syria', '', 'rtmp://sama-tv.net/live playpath=samatv swfUrl=http://www.addounia.tv/live/player.swf live=true timeout=15 pageUrl=http://www.addounia.tv/index.php?page=live')
		common.createStreamListItem('Oman Tv', '', 'rtmp://38.96.148.30/live/omantv1')
		common.createStreamListItem('Oman TV Sport', '', 'rtmp://38.96.148.30/live/omantv2')
		common.createStreamListItem('Bahrain SPort', '', 'rtmp://alayam.netromedia.net/btv3/btv3')
		common.createStreamListItem('KTV Sport', '', 'rtmp://62.215.183.1/rtmplive/rtpencoder/ch3.sdp')
		common.createStreamListItem('Al maghribiya', '', 'http://rm-edge-4.cdn2.streamago.tv/streamagoedge/1922/815/playlist.m3u8')
		common.createStreamListItem('al nahar', '', 'rtmp://50.7.180.18/nahar1 playpath=nahar1.stream_480p swfUrl=http://demos.streamtrix.com/swf/flowplayer.commercial-3.2.15.swf pageUrl=http://demos.streamtrix.com/Alnahar/')
		common.createStreamListItem('Al nahar +2', '', 'rtmp://50.7.180.18/nahar1/alnahar2.stream_480p swfUrl=http://demos.streamtrix.com/swf/flowplayer.commercial-3.2.15.swf pageUrl=http://demos.streamtrix.com/Alnahar/')
		common.createStreamListItem('al nahar drama', '', 'rtmp://50.7.180.18/nahar1 playpath=alnahardrama.stream_480p swfUrl=http://demos.streamtrix.com/swf/flowplayer.commercial-3.2.15.swf pageUrl=http://demos.streamtrix.com/alnahardrama/')
		common.createStreamListItem('aghani', '', 'rtmp://mobilestreaming.itworkscdn.com/aghanitv/ playpath=aghanitv swfUrl=http://tv.webactu-webtv.com/jwplayer1/jwplayer.flash.swf pageUrl=http://tv.webactu-webtv.com/egypte/aghani.html')
		common.createStreamListItem('al mehwar', '', 'rtmp://livestreaming4.onlinehorizons.net/MehwarTV playpath=livestream swfUrl=http://onlinehorizons.net/livestreaming/MehwarTV/player.swf pageUrl=http://www.elmehwartv.com/1/ rating=-1.00')
		common.createStreamListItem('al mehwar drama', '', 'rtmp://livestreaming4.onlinehorizons.net/MehwarTVDRAMA playpath=livestream swfUrl=http://onlinehorizons.net/livestreaming/MehwarTV/player.swf pageUrl=http://www.elmehwartv.com/1/ rating=-1.00')
		common.createStreamListItem('OnTv', '', 'http://xontvegx.api.channel.livestream.com/3.0/playlist.m3u8')
		common.createStreamListItem('OnTv Live', '', 'http://xontveglivex.api.channel.livestream.com/3.0/playlist.m3u8')
		common.createStreamListItem('al ayam', '', 'rtmp://alayam.netromedia.net/btv2/btv2')
		common.createStreamListItem('el chourouk tv', '', 'rtmp://live.echoroukonline.com/live/EchoroukTV')
		common.createStreamListItem('libya tv', '', 'rtmp://hd2.lsops.net/live//libyatv_ar_372')
		common.createStreamListItem('al fayhaa', '', 'mmsh://77.67.107.89/al-fayhaa')
		common.createStreamListItem('al sharqiya', '', 'rtmp://ns8.indexforce.com/alsharqiyalive/mystream')
		common.createStreamListItem('kuwait tv', '', 'rtmp://62.215.183.1/rtmplive/rtpencoder/ch6.sdp')
		common.createStreamListItem('kuwait 1', '', 'rtmp://62.215.183.1/rtmplive/rtpencoder/ch4.sdp')
		common.createStreamListItem('kuwait sport', '', 'rtmp://62.215.183.1/rtmplive/rtpencoder/ch3.sdp')
		common.createStreamListItem('kuwait 2', '', 'rtmp://62.215.183.1/rtmplive/rtpencoder/ch2.sdp')
		common.createStreamListItem('ANN Syria', '', 'rtmp://ns8.indexforce.com/ann/ann')
		common.createStreamListItem('Jordan Tv', '', 'rtmp://64.251.14.168/jorlive/?hghpl]=a2V5bGl2ZTgzLTI1NS02Ny0yNTIyMDE0LTAzLTA5LTEyLTQyLTAy/jrtv')
		common.createStreamListItem('al alam', '', 'http://hd6.lsops.net/live/alalam_ar_hls.smil/playlist.m3u8')
		common.createStreamListItem('al baghdadiya', '', 'rtmp://cp44832.live.edgefcs.net/live//albag1_500@90981')
		common.createStreamListItem('africa tv', '', 'rtmp://africatv.live.net.sa/live/africatv3')
		common.createStreamListItem('Miracle tv', '', 'rtmp://flash0.80205-live0.dna.qbrick.com/80205-live0/troens2')
		common.createStreamListItem('al alamia', '', 'rtmp://ns8.indexforce.com/alalamia/alalamia')
		common.createStreamListItem('al hayat', '', 'rtmp://media.islamexplained.com:1935/live/_definst_mp4:ahme.stream_360p')
		common.createStreamListItem('al hurra', '', 'rtmp://cp51007.live.edgefcs.net/live/Alhurra_Flash@15')
		common.createStreamListItem('al kaas', '', 'rtsp://78.100.44.238/live-kass/kass')
		common.createStreamListItem('Tunisia Al Wataniya', '', 'rtmp://ca-edge-6.cdn2.streamago.tv:1935/streamagoedge/1052?/ playpath=224 swfUrl=http://www.streamago.tv/app/StreamVideo.swf pageUrl=http://www.streamago.tv/spirituality/1052/ live=true swfVfy=true timeout=30')
		common.createStreamListItem('Saudi Al thakafiya', '', 'http://38.96.148.75/culture')
		common.createStreamListItem('Saudi Sport 1', '', 'http://38.96.148.75/Alriyadiah')
		common.createStreamListItem('Saudi Al Ekhbariya', '', 'mms://38.96.148.75/Ekhbariya?MSWMExt=.asf')
	elif cat == 'german':
		common.createStreamListItem('1 - Baden TV', 'http://www.lyngsat-logo.com/hires/bb/baden_tv.png', 'rtmp://badentv-stream2.siebnich.info/rtplive playpath=vlc.sdp')
		common.createStreamListItem('2 - ZDF', 'http://www.ab-ovo.nl/sites/default/files/corporate/zdf.jpg', 'rtmp://109.236.89.165/live/zdf')
		common.createStreamListItem('3 - Super RTL', 'http://www.rsasr.krefeld.schulen.net/homepages_if/homepages2010/HomepageZorbeyOezcan/Bilder/superrtl.jpg', 'rtmp://109.236.89.165/live/superrtl')
		common.createStreamListItem('4 - Juwelo TV', 'http://www.lyngsat-logo.com/hires/jj/juwelo_tv_it.png', 'rtmp://85.214.107.68/juwelo_hd playpath=live_DE1')
		common.createStreamListItem('5 - NRW TV', 'http://kress.de/uploads/rte_migration_tt_news/Logo_nrw_tv.jpg', 'http://streaming001.broadcast.tneg.de/nrwtv/nrwtv/nrwlive.stream/hasbahca.m3u8')
		common.createStreamListItem('6 - TRP1', 'http://www.blm.de/files/gif1/Tele_Regional_Passau1.gif', 'http://stream2.telvi.de/trp1live/livestream1/playlist.m3u8')
		common.createStreamListItem('7 - ORF Sport', 'http://www.peakbreak.at/wp-content/uploads/2013/08/orf_sport_plus_logo.jpg', 'http://194.232.200.128:1935/orfs_q6a/orf.sdp/playlist.m3u8')
		common.createStreamListItem('8 - ORF 3', 'http://images2.wikia.nocookie.net/__cb20120220211505/logopedia/images/7/73/ORF_III_logo.svg', 'rtsp://apasfwl.apa.at:80/orf3_q4a/orf.sdp')
		common.createStreamListItem('9 - ORF 1', 'http://www.mastersoundentertainment.de/wp-content/uploads/2013/03/ORF_1.png', 'rtmp://109.236.89.165/live/orf1')
		common.createStreamListItem('10 - TvAktuell', 'http://regiowiki.pnp.de/images/thumb/Senderlogo-TVAktuell.jpg/300px-Senderlogo-TVAktuell.jpg', 'http://tvaktuellr.iptv-playoutcenter.de:1935/tvaktuellr/tvaktuellr.stream_3/playlist.m3u8')
		common.createStreamListItem('11 - Alex tv', 'http://b.vimeocdn.com/ts/303/642/303642979_640.jpg', 'http://alex-stream.rosebud-media.de:1935/live/alexlivetv.smil/playlist.m3u8')
		common.createStreamListItem('12 - Barntele', 'http://cf.juggle-images.com/matte/white/280x280/telebarn-logo-primary.jpg', 'rtsp://rtmp.infomaniak.ch/livecast/barntele')
		common.createStreamListItem('13 - RTL', 'http://www.worldtv.dk/files/billeder/Kanaler/Tysk/rtl.png', 'rtmp://109.236.89.165/live/rtl')
		common.createStreamListItem('14 - RBB Berlin', 'http://image1.hoerzu.de/files/station_logos/52.png', 'http://88.212.11.206:5000/live/13/13.m3u8')
		common.createStreamListItem('15 - VRF', 'http://www.247webtv.com/wp-content/uploads/2012/06/VRF-Vogtland.gif', 'mms://87.106.241.76/VRF')
		common.createStreamListItem('16 - OjrfEins HD', 'http://upload.wikimedia.org/wikipedia/commons/thumb/4/4f/ORF_Eins_HD_logo.svg/798px-ORF_Eins_HD_logo.svg.png', 'http://195.250.60.51:8844/udp/239.100.202.1:3001')
		common.createStreamListItem('17 - RTL 2', 'http://www.lyngsat-logo.com/logo/tv/rr/rtl2_de.jpg', 'rtmp://109.236.89.165/live/rtl2')
		common.createStreamListItem('18 - 3sat', 'http://ivi.ucoz.net/_pu/1/98509058.jpg', 'rtmp://109.236.89.165/live/3sat')
		common.createStreamListItem('19 - VOX', 'http://www.reckmann.org/wp-content/vox.jpg', 'rtmp://109.236.89.165/live/vox')
		common.createStreamListItem('20 - ORF 1', 'http://images.wikia.com/how-i-met-your-mother/de/images/a/a3/Logo_tv_orf_1.jpg', 'http://194.232.200.128:1935/orf1_q6a/orf.sdp/hasbahca.m3u8')
		common.createStreamListItem('21 - KIKA', 'http://www.fchellaskagran.at/wb/media/Unlimitid/tmp_hellas2009_logo_kika.jpg', 'rtmp://109.236.89.165/live/kika')
		common.createStreamListItem('22 - ARD', 'http://nepidd.files.wordpress.com/2010/09/ard_logo.png', 'rtmp://109.236.89.165/live/ard')
	elif cat == 'scandinavian':
		common.createStreamListItem('Svt1', '', 'http://ys-live.ds.cdn.yousee.tv/iPhone/rtpencoder/e28_wcif.sdp/e28_wcif.sdp-mr2548k.m3u8')
		common.createStreamListItem('Svt2', '', 'http://ys-live.ds.cdn.yousee.tv/iPhone/rtpencoder/e42_wcif.sdp/e42_wcif.sdp-mr2548k.m3u8')
		common.createStreamListItem('TV3 HD', '', 'http://viasatlive5-i.akamaihd.net/hls/live/202794/tv3se/1aik.m3u8')
		common.createStreamListItem('TV12 Sverige', '', 'http://tvhdslive-f.akamaihd.net/i/EDCSPORTHDS_1@108870/index_4_av-b.m3u8')
		common.createStreamListItem('Tv4 Sport X', '', 'http://tvhdslive-f.akamaihd.net/i/EDCXTRAHDS_1@108871/index_4_av-b.m3u8')
		common.createStreamListItem('viasat hockey', '', 'http://viasatlive4-i.akamaihd.net/hls/live/202772/viasathockey/1aik.m3u8')
		common.createStreamListItem('Viasat Golf', '', 'http://viasatlive5-i.akamaihd.net/hls/live/207033/golfHDno/2hbk.m3u8')
		common.createStreamListItem('C More Live HD', '', 'http://cmorehlsedc-i.akamaihd.net/hls/live/208150/cmlivehd/cmlivehd.m3u8')
		common.createStreamListItem('C More Tennis', '', 'http://cmorehlsedc-i.akamaihd.net/hls/live/208147/cmtennis/cmtennis.m3u8')
		common.createStreamListItem('C More Extreme', '', 'http://cmorehlsedc-i.akamaihd.net/hls/live/208148/cmextreme/cmextreme.m3u8')
		common.createStreamListItem('C More Hockey', '', 'http://cmorehlsedc-i.akamaihd.net/hls/live/208149/cmhockey/cmhockey.m3u8')
		common.createStreamListItem('C More Footbol', '', 'http://cmorehlsedc-i.akamaihd.net/hls/live/208154/cmfotboll/cmfotboll.m3u8')
		common.createStreamListItem('C More Sport HD', '', 'http://cmorehlsedc-i.akamaihd.net/hls/live/208145/cmsporthd/cmsporthd.m3u8')
		common.createStreamListItem('Karlskrona', '', 'rtmp://80.78.208.198/live/flv:live.stream live=true')
		common.createStreamListItem('Sport hd', '', 'http://ys-live.ds.cdn.yousee.tv/iPhone/rtpencoder/e731_wcif.sdp/e731_wcif.sdp-mr2548k.m3u8')
		common.createStreamListItem('kanal 9', '', 'http://ys-live.ds.cdn.yousee.tv/iPhone/rtpencoder/e54_wcif.sdp/e54_wcif.sdp-mr2548k.m3u8')
		common.createStreamListItem('TCM', '', 'http://ys-live.ds.cdn.yousee.tv/iPhone/rtpencoder/e41_wcif.sdp/e41_wcif.sdp-mr2548k.m3u8')
		common.createStreamListItem('TLC', '', 'http://ys-live.ds.cdn.yousee.tv/iPhone/rtpencoder/e772_wcif.sdp/e772_wcif.sdp-mr2548k.m3u8')
		common.createStreamListItem('Kanal 7', '', 'http://ys-live.ds.cdn.yousee.tv/iPhone/rtpencoder/e802_wcif.sdp/e802_wcif.sdp-mr2548k.m3u8')
		common.createStreamListItem('TV 7 Plus', '', 'rtmp://vod.tv7.fi/tv7plus-web/_definst_/mp4:tv7plus.stream_360p')
		common.createStreamListItem('CNN', '', 'http://ys-live.ds.cdn.yousee.tv/iPhone/rtpencoder/e46_wcif.sdp/e46_wcif.sdp-mr2548k.m3u8')
		common.createStreamListItem('BBC Life Style', '', 'http://ys-live.ds.cdn.yousee.tv/iPhone/rtpencoder/e722_wcif.sdp/e722_wcif.sdp-mr2548k.m3u8')
		common.createStreamListItem('BBC world News', '', 'http://ys-live.ds.cdn.yousee.tv/iPhone/rtpencoder/e751_wcif.sdp/e751_wcif.sdp-mr2548k.m3u8')
		common.createStreamListItem('BBC Knowledge', '', 'http://ys-live.ds.cdn.yousee.tv/iPhone/rtpencoder/e26_wcif.sdp/e26_wcif.sdp-mr2548k.m3u8')
		common.createStreamListItem('BBC Entertainment', '', 'http://ys-live.ds.cdn.yousee.tv/iPhone/rtpencoder/e48_wcif.sdp/e48_wcif.sdp-mr2548k.m3u8')
		common.createStreamListItem('Dina Tv', '', 'rtmp://curofix.arcada.fi/live/live.sdp')
		common.createStreamListItem('C More Live 4', '', 'http://cmorehlsedc-i.akamaihd.net/hls/live/208153/cmlive4/cmlive4.m3u8')
		common.createStreamListItem('C More Live 3', '', 'http://cmorehlsedc-i.akamaihd.net/hls/live/208152/cmlive3/cmlive3.m3u8')
		common.createStreamListItem('C More Live 2', '', 'http://cmorehlsedc-i.akamaihd.net/hls/live/208151/cmlive2/cmlive2.m3u8')
		common.createStreamListItem('Dr1', '', 'http://ys-live.ds.cdn.yousee.tv/iPhone/rtpencoder/e20_wcif.sdp/e20_wcif.sdp-mr2548k.m3u8')
		common.createStreamListItem('Dr2', '', 'http://ys-live.ds.cdn.yousee.tv/iPhone/rtpencoder/e21_wcif.sdp/e21_wcif.sdp-mr2548k.m3u8')
		common.createStreamListItem('Tv2', '', 'http://ys-live.ds.cdn.yousee.tv/iPhone/rtpencoder/e22_wcif.sdp/e22_wcif.sdp-mr2548k.m3u8')
		common.createStreamListItem('Tv2 zulu', '', 'http://ys-live.ds.cdn.yousee.tv/iPhone/rtpencoder/e24_wcif.sdp/e24_wcif.sdp-mr2548k.m3u8')
		common.createStreamListItem('Tv2 charlie,', '', 'http://ys-live.ds.cdn.yousee.tv/iPhone/rtpencoder/e25_wcif.sdp/e25_wcif.sdp-mr2548k.m3u8')
		common.createStreamListItem('Bbc knowledge', '', 'http://ys-live.ds.cdn.yousee.tv/iPhone/rtpencoder/e26_wcif.sdp/e26_wcif.sdp-mr2548k.m3u8')
		common.createStreamListItem('Mtv', '', 'http://ys-live.ds.cdn.yousee.tv/iPhone/rtpencoder/e27_wcif.sdp/e27_wcif.sdp-mr2548k.m3u8')
		common.createStreamListItem('Nrk1', '', 'http://ys-live.ds.cdn.yousee.tv/iPhone/rtpencoder/e30_wcif.sdp/e30_wcif.sdp-mr2548k.m3u8')
		common.createStreamListItem('Nickelodeon', '', 'http://ys-live.ds.cdn.yousee.tv/iPhone/rtpencoder/e32_wcif.sdp/e32_wcif.sdp-mr2548k.m3u8')
		common.createStreamListItem('Vh1', '', 'http://ys-live.ds.cdn.yousee.tv/iPhone/rtpencoder/e33_wcif.sdp/e33_wcif.sdp-mr2548k.m3u8')
		common.createStreamListItem('Nat geo', '', 'http://ys-live.ds.cdn.yousee.tv/iPhone/rtpencoder/e34_wcif.sdp/e34_wcif.sdp-mr2548k.m3u8')
		common.createStreamListItem('Dk 4', '', 'http://ys-live.ds.cdn.yousee.tv/iPhone/rtpencoder/e35_wcif.sdp/e35_wcif.sdp-mr2548k.m3u8')
		common.createStreamListItem('Eurosport', '', 'http://ys-live.ds.cdn.yousee.tv/iPhone/rtpencoder/e36_wcif.sdp/e36_wcif.sdp-mr2548k.m3u8')
		common.createStreamListItem('Disney xd', '', 'http://ys-live.ds.cdn.yousee.tv/iPhone/rtpencoder/e37_wcif.sdp/e37_wcif.sdp-mr2548k.m3u8')
		common.createStreamListItem('Viasat 3', '', 'http://ys-live.ds.cdn.yousee.tv/iPhone/rtpencoder/e39_wcif.sdp/e39_wcif.sdp-mr2548k.m3u8')
		common.createStreamListItem('Disney channel', '', 'http://ys-live.ds.cdn.yousee.tv/iPhone/rtpencoder/e40_wcif.sdp/e40_wcif.sdp-mr2548k.m3u8')
		common.createStreamListItem('Tcm', '', 'http://ys-live.ds.cdn.yousee.tv/iPhone/rtpencoder/e41_wcif.sdp/e41_wcif.sdp-mr2548k.m3u8')
		common.createStreamListItem('Discovery channel', '', 'http://ys-live.ds.cdn.yousee.tv/iPhone/rtpencoder/e44_wcif.sdp/e44_wcif.sdp-mr2548k.m3u8')
		common.createStreamListItem('Animal planet', '', 'http://ys-live.ds.cdn.yousee.tv/iPhone/rtpencoder/e45_wcif.sdp/e45_wcif.sdp-mr2548k.m3u8')
		common.createStreamListItem('Cnn', '', 'http://ys-live.ds.cdn.yousee.tv/iPhone/rtpencoder/e46_wcif.sdp/e46_wcif.sdp-mr2548k.m3u8')
		common.createStreamListItem('Bbc entertainment', '', 'http://ys-live.ds.cdn.yousee.tv/iPhone/rtpencoder/e48_wcif.sdp/e48_wcif.sdp-mr2548k.m3u8')
		common.createStreamListItem('Dr ramasjang', '', 'http://ys-live.ds.cdn.yousee.tv/iPhone/rtpencoder/e50_wcif.sdp/e50_wcif.sdp-mr2548k.m3u8')
		common.createStreamListItem('Kanal 4', '', 'http://ys-live.ds.cdn.yousee.tv/iPhone/rtpencoder/e51_wcif.sdp/e51_wcif.sdp-mr2548k.m3u8')
		common.createStreamListItem('Tv9', '', 'http://ys-live.ds.cdn.yousee.tv/iPhone/rtpencoder/e54_wcif.sdp/e54_wcif.sdp-mr2548k.m3u8')
		common.createStreamListItem('Tv5', '', 'http://ys-live.ds.cdn.yousee.tv/iPhone/rtpencoder/e56_wcif.sdp/e56_wcif.sdp-mr2548k.m3u8')
		common.createStreamListItem('Tv6', '', 'http://ys-live.ds.cdn.yousee.tv/iPhone/rtpencoder/e57_wcif.sdp/e57_wcif.sdp-mr2548k.m3u8')
		common.createStreamListItem('Tv4', '', 'http://ys-live.ds.cdn.yousee.tv/iPhone/rtpencoder/e58_wcif.sdp/e58_wcif.sdp-mr2548k.m3u8')
		common.createStreamListItem('Folgetinget', '', 'http://ys-live.ds.cdn.yousee.tv/iPhone/rtpencoder/e63_wcif.sdp/e63_wcif.sdp-mr2548k.m3u8')
		common.createStreamListItem('Dr3', '', 'http://ys-live.ds.cdn.yousee.tv/iPhone/rtpencoder/e701_wcif.sdp/e701_wcif.sdp-mr2548k.m3u8')
		common.createStreamListItem('Viasat sport1', '', 'http://ys-live.ds.cdn.yousee.tv/iPhone/rtpencoder/e711_wcif.sdp/e711_wcif.sdp-mr2548k.m3u8')
		common.createStreamListItem('Tnt', '', 'http://ys-live.ds.cdn.yousee.tv/iPhone/rtpencoder/e721_wcif.sdp/e721_wcif.sdp-mr2548k.m3u8')
		common.createStreamListItem('Bbc lifestyle', '', 'http://ys-live.ds.cdn.yousee.tv/iPhone/rtpencoder/e722_wcif.sdp/e722_wcif.sdp-mr2548k.m3u8')
		common.createStreamListItem('3 Sport2', '', 'http://viasatlive5-i.akamaihd.net/hls/live/207018/tv3sport2HD/2liu.m3u8')
		common.createStreamListItem('Kanal8', '', 'http://ys-live.ds.cdn.yousee.tv/iPhone/rtpencoder/e732_wcif.sdp/e732_wcif.sdp-mr2548k.m3u8')
		common.createStreamListItem('Rtl', '', 'http://ys-live.ds.cdn.yousee.tv/iPhone/rtpencoder/e741_wcif.sdp/e741_wcif.sdp-mr2548k.m3u8')
		common.createStreamListItem('Ndr', '', 'http://ys-live.ds.cdn.yousee.tv/iPhone/rtpencoder/e742_wcif.sdp/e742_wcif.sdp-mr2548k.m3u8')
		common.createStreamListItem('Bbc world news', '', 'http://ys-live.ds.cdn.yousee.tv/iPhone/rtpencoder/e751_wcif.sdp/e751_wcif.sdp-mr2548k.m3u8')
		common.createStreamListItem('Eurosport 2', '', 'http://ys-live.ds.cdn.yousee.tv/iPhone/rtpencoder/e752_wcif.sdp/e752_wcif.sdp-mr2548k.m3u8')
		common.createStreamListItem('Plus 3', '', 'http://ys-live.ds.cdn.yousee.tv/iPhone/rtpencoder/e761_wcif.sdp/e761_wcif.sdp-mr2548k.m3u8')
		common.createStreamListItem('tv 3 Puls', '', 'http://viasatlive1-i.akamaihd.net/hls/live/202795/tv3puls/wifi2000.m3u8')
		common.createStreamListItem('3 puls', '', 'http://ys-live.ds.cdn.yousee.tv/iPhone/rtpencoder/e762_wcif.sdp/e762_wcif.sdp-mr2548k.m3u8')
		common.createStreamListItem('Disney junior', '', 'http://ys-live.ds.cdn.yousee.tv/iPhone/rtpencoder/e771_wcif.sdp/e771_wcif.sdp-mr2548k.m3u8')
		common.createStreamListItem('Tlc', '', 'http://ys-live.ds.cdn.yousee.tv/iPhone/rtpencoder/e772_wcif.sdp/e772_wcif.sdp-mr2548k.m3u8')
		common.createStreamListItem('Tv2 fri', '', 'http://ys-live.ds.cdn.yousee.tv/iPhone/rtpencoder/e782_wcif.sdp/e782_wcif.sdp-mr2548k.m3u8')
		common.createStreamListItem('Disney Junio', '', 'http://ys-live.ds.cdn.yousee.tv/iPhone/rtpencoder/e771_wcif.sdp/e771_wcif.sdp-mr2548k.m3u8')
		common.createStreamListItem('TNT', '', 'http://ys-live.ds.cdn.yousee.tv/iPhone/rtpencoder/e721_wcif.sdp/e721_wcif.sdp-mr2548k.m3u8')
		common.createStreamListItem('Folketings Kanalen', '', 'http://ys-live.ds.cdn.yousee.tv/iPhone/rtpencoder/e63_wcif.sdp/e63_wcif.sdp-mr2548k.m3u8')
		common.createStreamListItem('Disney Channel', '', 'http://ode-cds-se1.se.ys-live.ds.cdn.yousee.tv/iPhone/rtpencoder/e40_wcif.sdp/e40_wcif.sdp-mr2548k.m3u8')
		common.createStreamListItem('Tv3', '', 'http://ys-live.ds.cdn.yousee.tv/iPhone/rtpencoder/e39_wcif.sdp/e39_wcif.sdp-mr2548k.m3u8')
		common.createStreamListItem('DR Ramasjang', '', 'http://ys-live.ds.cdn.yousee.tv/iPhone/rtpencoder/e50_wcif.sdp/e50_wcif.sdp-mr2548k.m3u8')
		common.createStreamListItem('Dina', '', 'rtmp://curofix.arcada.fi/live/live.sdp')
		common.createStreamListItem('Life Style', '', 'rtmp://stream1.lifestyletv.se/live/livestream2')
		common.createStreamListItem('Atv5', '', 'rtmp://82.94.228.203/live/live1.stream')
		common.createStreamListItem('L1', '', 'rtsp://wm-live.media.dutchview.nl/L1vestream')
		common.createStreamListItem('ZDF', '', 'http://ys-live.ds.cdn.yousee.tv:80/iPhone/rtpencoder/e29_wcif.sdp/e29_wcif.sdp-mr2524k.m3u8')
		common.createStreamListItem('deutch welle', '', 'rtsp://46.249.213.87/broadcast/deutschewelle-tablet.3gp')
	elif cat == 'sport2':
		common.createStreamListItem('TraceSport', '', 'rtsp://46.249.213.87/broadcast/tracetvsports-tablet.3gp')
		common.createStreamListItem('Sky Poker', '', 'rtmp://cp67698.live.edgefcs.net/live/SkyPoker_500k@9124')
		common.createStreamListItem('Sevilla Fc', '', 'rtmp://flash0.80137-live0.dna.qbrick.com/80137-live0/sevillafc')
		common.createStreamListItem('Viasat Sport', '', 'http://hls.novotelecom.ru/streaming/viasat_sport/tvrec/playlist.m3u8')
		common.createStreamListItem('Fight Club', '', 'http://hls.novotelecom.ru/streaming/fight_club/tvrec/playlist.m3u8?')
		common.createStreamListItem('extreme sport', '', 'http://hls.novotelecom.ru/streaming/khl/tvrec/playlist.m3u8?')
		common.createStreamListItem('CHL', '', 'http://hls.novotelecom.ru/streaming/khl/tvrec/playlist.m3u8?')
		common.createStreamListItem('Grandprix', '', 'rtmp://27.131.141.254/grandprix/live')
		common.createStreamListItem('Ghetto', '', 'rtsp://46.249.213.93/broadcast/ghettokid-tablet.3gp')
		common.createStreamListItem('Drift 4 ever', '', 'rtsp://46.249.213.93/broadcast/drift4ever-tablet.3gp')
		common.createStreamListItem('Climb On', '', 'rtsp://46.249.213.93/broadcast/climbon-tablet.3gp')
		common.createStreamListItem('Sport 2 HD', '', 'http://viasatlive5-i.akamaihd.net/hls/live/207018/tv3sport2HD/2liu.m3u8')
		common.createStreamListItem('sport channel', '', 'http://iphone-streaming.ustream.tv/uhls/12762028/streams/live/iphone/hasbahca.m3u8')
		common.createStreamListItem('live sport', '', 'mms://83.222.161.217/100livesport')
		common.createStreamListItem('Stadium 1', '', 'rtmp://111.223.33.105:39245/3SDdeeDweSwOdIdw2rcHDwwcDiI/PremieRLeague_01')
		common.createStreamListItem('Stadium 2', '', 'rtmp://111.223.33.105:39245/3SDdeeDweSwOdIdw2rcHDwwcDiI/PremieRLeague_02')
		common.createStreamListItem('Stadium 3', '', 'rtmp://202.170.127.28:51593/1jnfivkderngoessd-hd/PremieRaGuel_3')
		common.createStreamListItem('Stadium 4', '', 'rtmp://202.170.127.28:51593/1jnfivkderngoessd-hd/PremieRaGuel_4')
		common.createStreamListItem('Eurosport 2', '', 'http://ys-live.ds.cdn.yousee.tv/iPhone/rtpencoder/e752_wcif.sdp/e752_wcif.sdp-mr2548k.m3u8')
		common.createStreamListItem('Eurosport', '', 'http://ys-live.ds.cdn.yousee.tv/iPhone/rtpencoder/e36_wcif.sdp/e36_wcif.sdp-mr2548k.m3u8')
		common.createStreamListItem('Viasat Sport', '', 'http://178.49.132.73/streaming/viasat_sport/tvrec/playlist.m3u8')
		common.createStreamListItem('C more tennis', '', 'http://cmorehlsedc-i.akamaihd.net/hls/live/208147/cmtennis/cmtennis.m3u8')
		common.createStreamListItem('C more sweden Sport', '', 'http://cmorehlsedc-i.akamaihd.net/hls/live/208145/cmsporthd/cmsporthd.m3u8')
		common.createStreamListItem('C more live HD', '', 'http://cmorehlsedc-i.akamaihd.net/hls/live/208150/cmlivehd/cmlivehd.m3u8')
		common.createStreamListItem('C more hockey', '', 'http://cmorehlsedc-i.akamaihd.net/hls/live/208149/cmhockey/cmhockey.m3u8')
		common.createStreamListItem('C more football', '', 'http://cmorehlsedc-i.akamaihd.net/hls/live/208154/cmfotboll/cmfotboll.m3u8')
		common.createStreamListItem('C more extreme', '', 'http://cmorehlsedc-i.akamaihd.net/hls/live/208148/cmextreme/cmextreme.m3u8')
		common.createStreamListItem('Sport tv 2', '', 'http://www.skype.tvzune.org/hls/sporttv2.m3u8')
		common.createStreamListItem('Sport tv 1', '', 'http://www.skype.tvzune.org/hls/sporttv1.m3u8')
		common.createStreamListItem('pac 12 national', '', 'http://xrxs.net/video/live-p12netw-4728.m3u8')
		common.createStreamListItem('Sky Sport F1', '', 'rtmp://94.242.228.178:80/liverepeater playpath=141891 swfUrl=http://cdn.goodcast.pw/players.swf live=1 pageUrl=http://goodcast.pw/ token=Fo5_n0w?U.rA6l3-70w47ch')
		common.createStreamListItem('Skysport1', '', 'rtmp://37.220.32.43:443/liverepeater/23697 live=1 pageUrl=http://1cdn.filotv.pw/ token=#atd%#$ZH live=N.SAT')
		common.createStreamListItem('Skysport 2', '', 'rtmp://37.220.32.55:443/liverepeater playpath=33698 swfUrl=http://www.longtailvideo.com/content/ova/jwplayer/player.swf live=1 pageUrl=http://1cdn.filotv.pw/ token=#atd%#$ZH')
		common.createStreamListItem('SkySport 3', '', 'rtmp://37.220.36.71:443/liverepeater playpath=23699 swfUrl=http://static.surk.tv/atdedead.swf live=1 pageUrl=http://1cdn.filotv.pw/ token=#atd%#$ZH')
		common.createStreamListItem('SkySport 4', '', 'rtmp://37.220.34.18:443/liverepeater playpath=23700 swfUrl=http://97ff0e7e610f20512dbe-483e6ce63d68aeb3d05af6c054efb801.r29.cf1.rackcdn.com/atdedead.swf live=1 pageUrl=http://1cdn.filotv.pw/ token=#atd%#$ZH live=N.SAT')
		common.createStreamListItem('True Sport', '', 'rtmp://m22.megafun.vn/hctv/vstv018')
		common.createStreamListItem('Fox Sport', '', 'http://m24.megafun.vn/live.vs?c=vstv042&q=high')
		common.createStreamListItem('Star Sport', '', 'http://m24.megafun.vn/live.vs?c=vstv033&q=high')
		common.createStreamListItem('arena sport 5', '', 'mms://212.200.188.70/5')
		common.createStreamListItem('arena sport 3', '', 'mms://212.200.188.70/3')
		common.createStreamListItem('Sport Time 1', '', 'rtmp://streamer.a1.net:1935/rtmplive/redundant/channels/Sporttime/SporttimeTV/mp4:channel1_1200')
		common.createStreamListItem('SPORT Time 2', '', 'rtmp://streamer.a1.net:1935/rtmplive/redundant/channels/Sporttime/SporttimeTV/mp4:channel2_1200')
		common.createStreamListItem('Sport time 3', '', 'rtmp://streamer.a1.net:1935/rtmplive/redundant/channels/Sporttime/SporttimeTV/mp4:channel3_1200')
		common.createStreamListItem('Sport time 4', '', 'rtmp://streamer.a1.net:1935/rtmplive/redundant/channels/Sporttime/SporttimeTV/mp4:channel4_1200')
		common.createStreamListItem('Sport time 5', '', 'rtmp://streamer.a1.net:1935/rtmplive/redundant/channels/Sporttime/SporttimeTV/mp4:channel5_1200')
		common.createStreamListItem('Sport Time 6', '', 'rtmp://streamer.a1.net:1935/rtmplive/redundant/channels/Sporttime/SporttimeTV/mp4:channel6_1200')
		common.createStreamListItem('Football', '', 'http://178.49.132.73/streaming/futbol/tvrec/playlist.m3u8')
		common.createStreamListItem('Fight Club', '', 'http://178.49.132.73/streaming/fight_club/tvrec/playlist.m3u8')
		common.createStreamListItem('Auto Plus', '', 'http://178.49.132.73/streaming/auto_plus/tvrec/playlist.m3u8')
		common.createStreamListItem('1 channel', '', 'http://178.49.132.73/streaming/1kanal/tvrec/playlist.m3u8')
		common.createStreamListItem('Automotive Italia', '', 'rtsp://46.249.213.87/broadcast/automotivetv-tablet.3gp')
		common.createStreamListItem('Cnop1', '', 'http://hls01-06.az.myvideo.az/hls-live/livepkgr/sport01/sport01/sport01.m3u8')
		common.createStreamListItem('Bein 5', '', 'http://hls01-06.az.myvideo.az/hls-live/livepkgr/sport5/sport5/sport5.m3u8')
		common.createStreamListItem('NTV Online', '', 'http://hls01-09.az.myvideo.az/hls-live/livepkgr/ntvonline/ntvonline/ntvonline.m3u8')
		common.createStreamListItem('NTV Football', '', 'http://hls01-07.az.myvideo.az/hls-live/livepkgr/ntvfootball/ntvfootball/ntvfootball.m3u8')
		common.createStreamListItem('RedBull Sport', '', 'http://live.iphone.redbull.de.edgesuite.net/iphone.m3u8')
		common.createStreamListItem('Chelsea Tv', '', 'rtmp://cp96798.live.edgefcs.net/live/ChelTV_Ch01_1000k@26291')
		common.createStreamListItem('Fox Sport', '', 'http://m24.megafun.vn/live.vs?c=vstv042&q=high')
		common.createStreamListItem('Fox Sport Brazil', '', 'rtmp://31.204.153.72/live/ playpath=fsb swfUrl=http://www.cdn-br.com/swf/player.swf live=1 pageUrl=http://www.cdn-br.com/mastertv/FSB.htm --live')
		common.createStreamListItem('Redbull Tv HD', '', 'http://live.iphone.redbull.de.edgesuite.net/webtvHD.m3u8')
		common.createStreamListItem('Espn', '', 'rtmp://31.7.58.250:1935/stream/5654ygt.stream swfUrl=http://thecdn.04stream.com/p/bbp.swf live=1 pageUrl=http://thecdn.04stream.com/live=1')
		common.createStreamListItem('NBA TV', '', 'rtmp://31.7.58.122:1935/stream/I8s9S4H7.stream playpath=N1V3R0h8.stream swfUrl=http://thecdn.04stream.com/p/bbp.swf live=true  pageUrl=http://www.04stream.com/NBA TV')
		common.createStreamListItem('GMM Sport', '', 'rtmp://58.97.57.152/live playpath=ch78 swfUrl=http://www.one2hd.com/swfs/mediaPlayer/mediaPlayer.swf pageUrl=http://www.one2hd.com/')
		common.createStreamListItem('Kuwait Sport', '', 'rtmp://62.215.183.1/rtmplive/rtpencoder/ch3.sdp')
		common.createStreamListItem('WWE', '', 'rtmp://www.planeta-online.tv:1936/live/ playpath=wrestling.stream swfUrl=http://pro-wrestling.tv/uppod.swf live=1 pageUrl=http://www.watchtv.co/wwe-hd-tv-live/')
		common.createStreamListItem('arena sport1', '', 'mms://212.200.188.70/1')
		common.createStreamListItem('arena sport 4', '', 'mms://212.200.188.70/4')
		common.createStreamListItem('arena sport 2', '', 'mms://212.200.188.70/2')
		common.createStreamListItem('outdoor Channel', '', 'rtmp://lm02.everyon.tv:1935/ptv2/pld613')
		common.createStreamListItem('Xsport', '', 'http://tv.goweb.com/share/channels/channel/id/458/sign/18dc548a05abb23b014800dac36ac4a16a63fbb7/base/41398')
		common.createStreamListItem('Bura Sport', '', 'http://stream.yayindayiz.biz/Bursaspor/bursaspor/playlist.m3u8')
		common.createStreamListItem('auto moto', '', 'mms://83.222.161.217/bgtv1')
		common.createStreamListItem('gaz', '', 'mms://83.222.161.217/100gaz')
		common.createStreamListItem('live sport Bg', '', 'mms://83.222.161.217/100livesport')
		common.createStreamListItem('bmw bg', '', 'mms://83.222.161.217/bmw')
		common.createStreamListItem('mercedes bg', '', 'mms://83.222.161.217/channel_mercedes')
		common.createStreamListItem('porche bg', '', 'mms://83.222.161.217/channel_porsche')
		common.createStreamListItem('Xtreme impact', '', 'rtsp://46.249.213.93/broadcast/xtremeimpacts-tablet.3gp')
		common.createStreamListItem('trace sport', '', 'rtsp://46.249.213.87/broadcast/tracetvsports-tablet.3gp')
		common.createStreamListItem('Rai Sport', '', 'rtsp://streaming.rai.it/Newsvod/x/vod/sport/ultimi/20080607124947mpo40jfnotiziario_sportivo_-rainet.wmv')
	elif cat == 'spanish':
		common.createStreamListItem('lasexta', '', 'rtmp://antena3fms35livefs.fplive.net:1935/antena3fms35live-live/stream-lasexta_1')
		common.createStreamListItem('Antenna3', '', 'rtmp://antena3fms35livefs.fplive.net:1935/antena3fms35live-live/stream-antena3_1')
		common.createStreamListItem('Eventos 6', '', 'http://antena3-aos1-apple-live.adaptive.level3.net/apple/antena3/channel11/eventos_6_700K_640x368_baseline.m3u8')
		common.createStreamListItem('Sevilla', '', 'rtmp://flash0.80137-live0.dna.qbrick.com/80137-live0/sevillafc')
		common.createStreamListItem('Kiss Tv', '', 'rtmp://tst.es.flash.glb.ipercast.net/tst.es-live/live')
		common.createStreamListItem('Ibiza', '', 'rtsp://46.249.213.87/broadcast/ibizaontv-tablet.3gp?trackingid=3041310000')
		common.createStreamListItem('Hogarutil', '', 'http://brightcove03-f.akamaihd.net/HOGARUTIL_1_1100@117573?videoId=2518851062001&lineUpId=&pubId=2385340627001&playerId=2418571368001&affiliateId=&v=3.1.0&fp=WIN%2011,9,900,117&r=YCNRA&g=NMDHLHVDQHIT')
		common.createStreamListItem('First Music HD', '', 'rtmp://109.239.142.62/live/livestream3')
		common.createStreamListItem('tele madrid', '', 'http://iphone.telemadrid.es.edgesuite.net/telemadridsat_iphone.m3u8')
		common.createStreamListItem('Andalucia', '', 'http://iphone-andaluciatelevision.rtva.stream.flumotion.com/rtva/andaluciatelevision-iphone-multi/main.m3u8')
		common.createStreamListItem('Tele madrid', '', 'http://iphone.telemadrid.es.edgesuite.net/telemadridsat_iphone.m3u8')
		common.createStreamListItem('Sevilla', '', 'rtmp://flash0.80137-live0.dna.qbrick.com/80137-live0/sevillafc')
		common.createStreamListItem('Club Directo Tv', '', 'rtmp://87.106.183.39/live/myStream_2')
		common.createStreamListItem('RT', '', 'rtmp://rt.fms.visionip.tv/live?autostart=true/RT_Spanish_3')
		common.createStreamListItem('Tv Galicia', '', 'http://iphone.telemadrid.es.edgesuite.net/telemadridsat_iphone.m3u8')
		common.createStreamListItem('Tv Vida', '', 'rtmp://flash3.todostreaming.es:1935/radiovida/livestream')
		common.createStreamListItem('Etv2.', '', 'rtmp://193.40.133.138/live/etv2')
		common.createStreamListItem('canal 53', '', 'mms://streaming.uanl.mx/canal53bandaancha/')
	else:
		common.createListItem('News', True, 'plugin://plugin.video.filmontv/?description&group=NEWS TV&iconimage=http://static.filmon.com/couch/groups/1/big_logo.png&mode=3&name=NEWS TV&programme_id&startdate_time&url=1')
		common.createListItem('Sport', True, 'plugin://plugin.video.filmontv/?description&group=SPORTS&iconimage=http://static.filmon.com/couch/groups/2/big_logo.png&mode=3&name=SPORTS&programme_id&startdate_time&url=2')
		common.createListItem('More Sport', True, url+'LiveTVMenu&category=sport2')
		common.createListItem('Arabic', True, url+'LiveTVMenu&category=arabic')
		common.createListItem('Australian', True, 'plugin://plugin.video.filmontv/?description&group=AUSTRALIAN TV&iconimage=http://static.filmon.com/couch/groups/4/big_logo.png&mode=3&name=AUSTRALIAN TV&programme_id&startdate_time&url=4')
		common.createListItem('Scandinavian', True, url+'LiveTVMenu&category=scandinavian')
		common.createListItem('Spanish', True, url+'LiveTVMenu&category=spanish')
		common.createListItem('French', True, 'plugin://plugin.video.filmontv/?description&group=FRENCH TV&iconimage=http://static.filmon.com/couch/groups/27/big_logo.png&mode=3&name=FRENCH TV&programme_id&startdate_time&url=27')
		common.createListItem('German', True, url+'LiveTVMenu&category=german')
		common.createListItem('Italian', True, 'plugin://plugin.video.filmontv/?description&group=ITALIAN TV&iconimage=http://static.filmon.com/couch/groups/30/big_logo.png&mode=3&name=ITALIAN TV&programme_id&startdate_time&url=30')
		common.createListItem('Middle Eastern', True, 'plugin://plugin.video.filmontv/?description&group=MIDDLE EASTERN TV&iconimage=http://static.filmon.com/couch/groups/28/big_logo.png&mode=3&name=MIDDLE EASTERN TV&programme_id&startdate_time&url=28')
		common.createListItem('Russian', True, 'plugin://plugin.video.filmontv/?description&group=RUSSIAN TV&iconimage=http://static.filmon.com/couch/groups/130/big_logo.png&mode=3&name=RUSSIAN TV&programme_id&startdate_time&url=130')
		common.createListItem('Turkish', True, url+'LiveTVMenu&category=turkish')
		common.createListItem('UK', True, 'plugin://plugin.video.filmontv/?description&group=UK LIVE TV&iconimage=http://static.filmon.com/couch/groups/5/big_logo.png&mode=3&name=UK LIVE TV&programme_id&startdate_time&url=5')

	xbmcplugin.endOfDirectory(int(sys.argv[1]))


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





