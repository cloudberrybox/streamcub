import xbmcaddon,xbmc

ADDON = xbmcaddon.Addon(id='plugin.video.streamcub')

def getSetting(myKey):
	return ADDON.getSetting(myKey)
def setSetting(myKey,myValue):
	ADDON.setSetting(id=myKey,value=myValue)
def openSettings():
	ADDON.openSettings()
