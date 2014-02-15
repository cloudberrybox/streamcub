import sys, urllib, time, re, os
import xbmc, xbmcaddon, xbmcgui, xbmcplugin
import context
from utils import settings


# Plugin constants
__plugin__ = 'Streamcub Library'
__author__ = 'Streamcub Team'
__url__ = 'http://www.streamcub.com'
__version__ = '1.1.9'

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
	elif cat == 'french':
		common.createStreamListItem('1 - BoardRiders', 'http://static.playtv.fr/img/tv_channels/142_medium.png', 'http://live240.impek.com/brtv')
		common.createStreamListItem('2 - Calaisis TV', 'http://static.playtv.fr/img/tv_channels/143_medium.png', 'rtsp://91.121.2.60/calaistv')
		common.createStreamListItem('3 - Canal Savoir', 'http://upload.wikimedia.org/wikipedia/fr/thumb/d/d1/Logo_Canal_Savoir.svg/257px-Logo_Canal_Savoir.svg.png', 'mms://stream2.canal.qc.ca/enOndes_haut_debit')
		common.createStreamListItem('4 - Tele Antilles', 'http://static.playtv.fr/img/tv_channels/182_medium.png', 'http://live240.impek.com/soleiltv')
		common.createStreamListItem('5 - TVM Est Parisien', 'http://static.playtv.fr/img/tv_channels/199_medium.png', 'rtmp://rtmp.infomaniak.ch/livecast playpath=cineplume swfUrl=http://static.infomaniak.ch/livetv/player-v3.swf?cfg=http://static.infomaniak.ch/configvideo/cineplume/tvm/359_config.xml pageUrl=http://www.playtv.fr/television/#tvm-est-parisien swfVfy=true live=true')
	else:
		common.createListItem('French', True, url+'LiveTVMenu&category=french')
		common.createListItem('German', True, url+'LiveTVMenu&category=german')
		common.createListItem('Turkish', True, url+'LiveTVMenu&category=turkish')

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




