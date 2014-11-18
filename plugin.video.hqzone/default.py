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

def OPENURL(url, mobile = False, q = False, verbose = True, timeout = 10, cookie = None, data = None, cookiejar = False, log = True, headers = [], type = '',ua = False,setCookie = []):
    import urllib2 
    UserAgent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'
    if ua: UserAgent = ua
    try:
        if log:
            print "Openurl = " + url
        if cookie and not cookiejar:
            import cookielib
            cookie_file = os.path.join(os.path.join(datapath,'Cookies'), cookie+'.cookies')
            cj = cookielib.LWPCookieJar()
            if os.path.exists(cookie_file):
                try:
                    cj.load(cookie_file,True)
                    for c in setCookie:
                        cj.set_cookie(c)
                except: cj.save(cookie_file,True)
            else: cj.save(cookie_file,True)
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        elif cookiejar:
            import cookielib
            cj = cookielib.LWPCookieJar()
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        else:
            opener = urllib2.build_opener()
        if mobile:
            opener.addheaders = [('User-Agent', 'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_0 like Mac OS X; en-us) AppleWebKit/532.9 (KHTML, like Gecko) Version/4.0.5 Mobile/8A293 Safari/6531.22.7')]
        else:
            opener.addheaders = [('User-Agent', UserAgent)]
        for header in headers:
            opener.addheaders.append(header)
        if data:
            if type == 'json': 
                import json
                data = json.dumps(data)
                opener.addheaders.append(('Content-Type', 'application/json'))
            else: data = urllib.urlencode(data)
            response = opener.open(url, data, timeout)
        else:
            response = opener.open(url, timeout=timeout)
        if cookie and not cookiejar:
            cj.save(cookie_file,True)
        link=response.read()
        response.close()
        opener.close()
        #link = net(UserAgent).http_GET(url).content
        link=link.replace('&#39;',"'").replace('&quot;','"').replace('&amp;',"&").replace("&#39;","'").replace('&lt;i&gt;','').replace("#8211;","-").replace('&lt;/i&gt;','').replace("&#8217;","'").replace('&amp;quot;','"').replace('&#215;','x').replace('&#038;','&').replace('&#8216;','').replace('&#8211;','').replace('&#8220;','').replace('&#8221;','').replace('&#8212;','')
        link=link.replace('%3A',':').replace('%2F','/')
        if q: q.put(link)
        return link
    except Exception as e:
        if verbose:
            xbmc.executebuiltin("XBMC.Notification(Sorry!,Source Website is Down,3000,"+elogo+")")
        xbmc.log('***********Website Error: '+str(e)+'**************', xbmc.LOGERROR)
        xbmc.log('***********Url: '+url+' **************', xbmc.LOGERROR)
        import traceback
        traceback.print_exc()
        link ='website down'
        if q: q.put(link)
        return link

def setFile(path,content,force=False):
    if os.path.exists(path) and not force:
        return False
    else:
        try:
            open(path,'w+').write(content)
            return True
        except: pass
    return False


user = selfAddon.getSetting('hqusername')
passw = selfAddon.getSetting('hqpassword')
cookie_file = os.path.join(os.path.join(datapath,'Cookies'), 'hqzone.cookies')
if user == '' or passw == '':
    if os.path.exists(cookie_file):
        try: os.remove(cookie_file)
        except: pass
    dialog = xbmcgui.Dialog()
    ret = dialog.yesno('[COLOR Blue]HQZone[/COLOR]', 'Please set your HQZone credentials','or register if you dont have an account','at www.HQZone.Tv','Cancel','Login')
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
        print link
        streamer=re.findall("file: '([^']+)',",link)[0]
        return streamer.replace('redirect','live')+' swfUrl='+swf+' pageUrl='+murl+' live=true timeout=20 token=WY846p1E1g15W7s'
    
def PLAYLINK(mname,murl,thumb):
        ok=True
        stream_url = get_link(murl)     
        playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
        playlist.clear()
        infoL={'Title': mname, 'Genre': 'Live'} 
        listitem = xbmcgui.ListItem(mname, thumbnailImage=thumb)
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
    verCheck=True 
    if verCheck == True:
        import autoupdate
        import time
        try:
            print "HQZone auto update - started"
            html=OPENURL('https://github.com/'+GitHubUser+'/'+GitHubRepo+'?files=1', mobile=True, verbose=False)
        except:
            html=''
        m = re.search("View (\d+) commit",html,re.I)
        if m: gitver = int(m.group(1))
        else: gitver = 0
        UpdateVerPath = os.path.join(UpdatePath,UpdateVerFile)
        try: locver = int(autoupdate.getUpdateFile(UpdateVerPath))
        except: locver = 0
        RunningFilePath = os.path.join(UpdatePath, RunningFile)
        if locver < gitver and (not os.path.exists(RunningFilePath) or os.stat(RunningFilePath).st_mtime + 120 < time.time()) or force:
            UpdateUrl = 'https://github.com/'+GitHubUser+'/'+GitHubRepo+'/archive/'+GitHubBranch+'.zip'
            UpdateLocalName = GitHubRepo+'.zip'
            UpdateDirName   = GitHubRepo+'-'+GitHubBranch
            UpdateLocalFile = xbmc.translatePath(os.path.join(UpdatePath, UpdateLocalName))
            setFile(RunningFilePath,'')
            print "auto update - new update available ("+str(gitver)+")"
            xbmc.executebuiltin("XBMC.Notification(HQZone Update,New Update detected,3000,"")")
            xbmc.executebuiltin("XBMC.Notification(HQZone Update,Updating...,3000,"")")
            try:os.remove(UpdateLocalFile)
            except:pass
            try: urllib.urlretrieve(UpdateUrl,UpdateLocalFile)
            except:pass
            if os.path.isfile(UpdateLocalFile):
                extractFolder = xbmc.translatePath('special://home/addons')
                pluginsrc =  xbmc.translatePath(os.path.join(extractFolder,UpdateDirName))
                if autoupdate.unzipAndMove(UpdateLocalFile,extractFolder,pluginsrc):
                    autoupdate.saveUpdateFile(UpdateVerPath,str(gitver))
                    print "HQZone auto update - update install successful ("+str(gitver)+")"
                    xbmc.executebuiltin("XBMC.Notification(HQZone Update,Successful,5000,"")")
                    xbmc.executebuiltin("XBMC.Container.Refresh")

                else:
                    print "HQZone auto update - update install failed ("+str(gitver)+")"
                    xbmc.executebuiltin("XBMC.Notification(HQZone Update,Failed,3000,"")")

            else:
                print "HQZone auto update - cannot find downloaded update ("+str(gitver)+")"
                xbmc.executebuiltin("XBMC.Notification(HQZone Update,Failed,3000,"")")
            try:os.remove(RunningFilePath)
            except:pass
        else:
            if force: xbmc.executebuiltin("XBMC.Notification(HQZone Update,HQZone is up-to-date,3000,"")")
            print "HQZone auto update - HQZone is up-to-date ("+str(locver)+")"
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
        liz.setProperty('fanart_image',art+"fanart.jpg")

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
        import threading
        threading.Thread(target=CheckForAutoUpdate).start()
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

