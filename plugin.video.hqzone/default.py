import urllib,urllib2,re,cookielib,string,os
import xbmc, xbmcgui, xbmcaddon, xbmcplugin
from t0mm0.common.net import Net as net

addon_id = 'plugin.video.hqzone'
selfAddon = xbmcaddon.Addon(id=addon_id)
prettyName='HQZone'
art = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.hqzone/resources/art', ''))
datapath = xbmc.translatePath(selfAddon.getAddonInfo('profile'))
UpdatePath=os.path.join(datapath,'Update')
try: os.makedirs(UpdatePath)
except: pass

def OPENURL(url):
        print "openurl = " + url
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        link=pars.unescape(link)
        link=urllib.unquote(link)
        link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','')
        return link


user = selfAddon.getSetting('hqusername')
passw = selfAddon.getSetting('hqpassword')
cookie_file = os.path.join(os.path.join(datapath,'Cookies'), 'hqzone.cookies')
if user == '' or passw == '':
    if os.path.exists(cookie_file):
        try: os.remove(cookie_file)
        except: pass
    dialog = xbmcgui.Dialog()
    ret = dialog.yesno('[COLOR=FF67cc33]MashUp[/COLOR]', 'Please set your HQZone credentials','or register if you dont have an account','at www.HQZone.Tv','Cancel','Login')
    if ret == 1:
        keyb = xbmc.Keyboard('', 'Enter Username or Email')
        keyb.doModal()
        if (keyb.isConfirmed()):
            search = keyb.getText()
            username=search
            keyb = xbmc.Keyboard('', 'Enter Password:')
            keyb.doModal()
            if (keyb.isConfirmed()):
                search = keyb.getText()
                password=search
                selfAddon.setSetting('hqusername',username)
                selfAddon.setSetting('hqpassword',password)
                
user = selfAddon.getSetting('hqusername')
passw = selfAddon.getSetting('hqpassword')

def setCookie(srDomain):
    import hashlib
    m = hashlib.md5()
    m.update(passw)
    net().http_GET('http://www.hqzone.tv/forums/view.php?pg=live')
    net().http_POST('http://www.hqzone.tv/forums/login.php?do=login',{'vb_login_username':user,'vb_login_password':passw,'vb_login_md5password':m.hexdigest(),'vb_login_md5password_utf':m.hexdigest(),'do':'login','securitytoken':'guest','url':'http://www.hqzone.tv/forums/view.php?pg=live','s':''})


def cleanHex(text):
    def fixup(m):
        text = m.group(0)
        if text[:3] == "&#x": return unichr(int(text[3:-1], 16)).encode('utf-8')
        else: return unichr(int(text[2:-1])).encode('utf-8')
    return re.sub("(?i)&#\w+;", fixup, text.decode('ISO-8859-1').encode('utf-8'))

def MAINHQ():
    setCookie('http://www.hqzone.tv/forums/view.php?pg=live')
    response = net().http_GET('http://www.hqzone.tv/forums/view.php?pg=live')
    link = response.content
    link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('  ','')
    addDir('[COLOR blue]Schedule[/COLOR]','http://www.hqzone.tv/forums/calendar.php?c=1&do=displayweek',475,art+'/hqzone.png')
    match=re.findall('(?sim)<h4 class="panel_headin.+?">([^<]+?)</h4><ul>(.+?)</ul>',link)
    for name,links in match[0:3]:
        if 'Channels' == name:
            name='VIP Streams'
        addDir(name,links,471,art+'/hqzone.png')
    addLink('[COLOR red]VOD[/COLOR]','','')
    match=re.findall('(?sim)<h4 class="panel_headin.+?">([^<]+?)</h4><ul>(.+?)</ul>',link)
    for name,links in match[3:]:
        if 'Channels' == name:
            name='VIP Streams'
        addDir(name,links,473,art+'/hqzone.png')
    if len(match) < 2:
        xbmc.executebuiltin("XBMC.Container.Refresh")
    
    
def Calendar(murl):
    setCookie(murl)
    response = net().http_GET(murl)
    link = response.content
    link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('  ','')
    month=re.findall('(?sim)<h2 class="blockhead">([^<]+?)</h2>',link)
    match=re.findall('(?sim)<h3><span class=".+?">([^<]+?)</span><span class="daynum" style=".+?" onclick=".+?">(\d+)</span></h3><ul class="blockrow eventlist">(.+?)</ul>',link)
    for day,num,data in match:
       addLink('[COLOR blue]'+day+' '+num+' '+month[0]+'[/COLOR]','','')
       match2=re.findall('(?sim)<span class="eventtime">([^<]+?)</span><a href=".+?" title=".+?">([^<]+?)</a>',data)
       for time,title in match2:
           addLink('[COLOR yellow]'+time+'[/COLOR] '+title,'','')
    
def LISTMENU(murl):
    match=re.findall('(?sim)<li><a href="([^"]+?)" target="I1">([^<]+?)</a></li>',murl)
    if not match:
        match=re.findall('(?sim)<a href="([^"]+?)" target="I1"><img src="([^"]+?)"',murl)
    for url,name in match:
        url = 'http://www.hqzone.tv/forums/'+url
        addPlay(name,url,474,'')

def LISTMENU2(murl):
    match=re.findall('(?sim)<li><a href="([^"]+?)" target="I1">([^<]+?)</a></li>',murl)
    for url,name in match:
        url = 'http://www.hqzone.tv/forums/'+url
        addDir(name,url,472,art+'/hqzone.png')

def LISTCONTENT(murl,thumb):
    setCookie(murl)
    response = net().http_GET(murl)
    link = response.content
    link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('  ','')
    match=re.findall('(?sim)sources: \[\{ file: "([^"]+?)" \}\],title: "([^"]+?)"',link)
    for url,name in match:
        addPlay(name,url,474,'')


def get_link(murl):
    if 'mp4' in murl:
        swf='http://www.hqzone.tv/forums/jwplayer/jwplayer.flash.swf'
        streamer=re.search('(?sim)(rtmp://.+?/vod/)(.+?.mp4)',murl)
        return streamer.group(1)+'mp4:'+streamer.group(2)+' swfUrl='+swf+' pageUrl=http://www.hqzone.tv/forums/view.php?pg=live# token=WY846p1E1g15W7s'
    setCookie(murl)
    response = net().http_GET(murl)
    link = response.content
    link = cleanHex(link)
    link=link.replace('\r','').replace('\n','').replace('\t','').replace('&nbsp;','').replace('  ','')
    m3u8=re.findall('<a href="([^"]+?.m3u8)">',link)
    flash=re.search('file=(.+?)&streamer=(.+?)&dock',link)
    if m3u8:
        return m3u8[0]
    elif flash:
        swf='http://www.hqzone.tv/forums/jwplayer/player.swf'
        return flash.group(2)+' playpath='+flash.group(1)+' swfUrl='+swf+' pageUrl='+murl+' live=true timeout=20 token=WY846p1E1g15W7s'

    else:
        swf='http://www.hqzone.tv/forums/jwplayer/jwplayer.flash.swf'
        streamer=re.findall("file: '([^']+)',",link)[0]
        return streamer.replace('redirect','live')+' swfUrl='+swf+' pageUrl='+murl+' live=true timeout=20 token=WY846p1E1g15W7s'
    
def PLAYLINK(mname,murl,thumb):
        ok=True
        stream_url = get_link(murl)     
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.clear()
        listitem = xbmcgui.ListItem(thumbnailImage=thumb)
        liz=xbmcgui.ListItem(mname, iconImage=thumb, thumbnailImage=thumb)
        playlist.add(stream_url,listitem)
        xbmcPlayer = xbmc.Player()
        xbmcPlayer.play(playlist)
        return ok
                                             
def CheckForAutoUpdate(force = False):
    GitHubRepo    = 'hqzone'
    GitHubUser    = 'haze108'
    GitHubBranch  = 'master'
    UpdateVerFile = 'update'
    RunningFile   = 'running'
    verCheck=True #main.CheckVersion()#Checks If Plugin Version is up to date
    if verCheck == True:
        from resources.libs import autoupdate
        try:
            print "Mashup auto update - started"
            html=main.OPENURL('https://offshoregit.com/'+GitHubUser+'/'+GitHubRepo+'?files=1', mobile=True, verbose=False)
        except: 
        m = re.search("commits/master">(\d+) commit</a>",html,re.I)
        if m: gitver = int(m.group(1))
        else: gitver = 0
        UpdateVerPath = os.path.join(UpdatePath,UpdateVerFile)
        try: locver = int(autoupdate.getUpdateFile(UpdateVerPath))
        except: locver = 0
        RunningFilePath = os.path.join(UpdatePath, RunningFile)
        if locver < gitver and (not os.path.exists(RunningFilePath) or os.stat(RunningFilePath).st_mtime + 120 < time.time()) or force:
            UpdateUrl = 'https://offshoregit.com/'+GitHubUser+'/'+GitHubRepo+'/repository/archive.zip'
            UpdateLocalName = GitHubRepo+'.zip'
            UpdateDirName   = GitHubRepo+'-'+GitHubBranch
            UpdateLocalFile = xbmc.translatePath(os.path.join(UpdatePath, UpdateLocalName))
            main.setFile(RunningFilePath,'')
            print "auto update - new update available ("+str(gitver)+")"
            xbmc.executebuiltin("XBMC.Notification(MashUp Update,New Update detected,3000,"+''+")")
            xbmc.executebuiltin("XBMC.Notification(MashUp Update,Updating...,3000,"+''+")")
            try:os.remove(UpdateLocalFile)
            except:pass
            try: urllib.urlretrieve(UpdateUrl,UpdateLocalFile)
            except:pass
            if os.path.isfile(UpdateLocalFile):
                extractFolder = xbmc.translatePath('special://home/addons')
                pluginsrc =  xbmc.translatePath(os.path.join(extractFolder,UpdateDirName))
                if autoupdate.unzipAndMove(UpdateLocalFile,extractFolder,pluginsrc):
                    autoupdate.saveUpdateFile(UpdateVerPath,str(gitver))
                    main.GA("Autoupdate",str(gitver)+" Successful")
                    print "Mashup auto update - update install successful ("+str(gitver)+")"
                    xbmc.executebuiltin("XBMC.Notification(MashUp Update,Successful,5000,"+main.slogo+")")
                    xbmc.executebuiltin("XBMC.Container.Refresh")
                    if selfAddon.getSetting('autochan')=='true':
                        xbmc.executebuiltin('XBMC.RunScript('+xbmc.translatePath(main.mashpath + '/resources/libs/changelog.py')+',Env)')
                else:
                    print "Mashup auto update - update install failed ("+str(gitver)+")"
                    xbmc.executebuiltin("XBMC.Notification(MashUp Update,Failed,3000,"+main.elogo+")")
                    main.GA("Autoupdate",str(gitver)+" Failed")
            else:
                print "Mashup auto update - cannot find downloaded update ("+str(gitver)+")"
                xbmc.executebuiltin("XBMC.Notification(MashUp Update,Failed,3000,"+main.elogo+")")
                main.GA("Autoupdate",str(gitver)+" Repo problem")
            try:os.remove(RunningFilePath)
            except:pass
        else:
            if force: xbmc.executebuiltin("XBMC.Notification(MashUp Update,MashUp is up-to-date,3000,"+main.slogo+")")
            print "Mashup auto update - Mashup is up-to-date ("+str(locver)+")"
        return        
        

def addPlay(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage='', thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setProperty('fanart_image',art+"fanart.jpg")
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz, isFolder = False)
        return ok


def addLink(name,url,iconimage):
    liz=xbmcgui.ListItem(name, iconImage=art+'/link.png', thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels={ "Title": name } )
    liz.setProperty('fanart_image',art+"fanart.jpg")
    return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)

def addDir(name, url, mode, thumbImage):

        u  = sys.argv[0]

        u += "?url="  + urllib.quote_plus(url)
        u += "&mode=" + str(mode)
        u += "&name=" + urllib.quote_plus(name)

        liz = xbmcgui.ListItem(name, iconImage='', thumbnailImage=thumbImage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setProperty('fanart_image','')

        xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz,isFolder=True)



def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param
              
params=get_params()
url=None
name=None
mode=None
iconimage=None

try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass
try:
    iconimage=urllib.unquote_plus(params["iconimage"])
    iconimage = iconimage.replace(' ','%20')
except:
        pass

print "Mode: "+str(mode)
print "Name: "+str(name)


if mode==None or url==None or len(url)<1:
        MAINHQ()
       
    
elif mode==471:
    LISTMENU(url)
        
elif mode==472:
    LISTCONTENT(url,iconimage)
        
elif mode==473:
    LISTMENU2(url)
            
elif mode==474:
    PLAYLINK(name,url,iconimage)

elif mode==475:
    Calendar(url)
        
xbmcplugin.endOfDirectory(int(sys.argv[1]))

