#Written by Ali Abbasi 
# Why I made this script?
# Because I could not sleep at night and I wanted to mess up with IranProud...
# 
import urllib2,urllib,re
class bcolors:
   HEADER = '\033[95m'
   OKBLUE = '\033[94m'
   OKGREEN = '\033[92m'
   WARNING = '\033[93m'
   FAIL = '\033[91m'
   ENDC = '\033[0m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
m3utext="#EXTINF:-1,"
logohandler=" #IMG:"
print bcolors.BOLD + "System Initialization to capture live tv channels from IranProud server" + bcolors.BOLD
url='http://www.iranproud.com/livetv'
BaseURL="http://www.iranproud.com"
req = urllib2.Request(url)
print "Connecting to IranProud server"
req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2015092817 Firefox/3.0.3')
response = urllib2.urlopen(req)
link=response.read()
response.close()
print "Received data, Now analysing..."
match=re.compile('<li><a href="(.+?)" target="_parent".+?src="(.+?)" .+?').findall(link)
i=len(match)-1
x=0
print ("Detected %i Live TV channel in IranProud server..." % (i)) 
while i>=x:
    for subdir,logo in match:
        mainurl=BaseURL+subdir
        req2 = urllib2.Request(mainurl)
        req2.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response2 = urllib2.urlopen(req2)
        link2=response2.read()
        response2.close()
        match2=re.compile('.+? videosrc="(.+?)".+?').findall(link2)
        for ChannelURL in match2:
             print bcolors.FAIL + ChannelURL + bcolors.FAIL
             ChannelNameFinal = (ChannelURL.split("/")[-1].split(".")[0])
             print bcolors.OKBLUE + ChannelNameFinal + bcolors.OKBLUE
             print logo
             with open("tvlist.m3u", "ab") as myfile:
                 myfile.write(m3utext+ChannelNameFinal)
                 myfile.write("\n")
                 myfile.write(ChannelURL)
                 myfile.write("\n")
                 myfile.write("\n")
                 myfile.close
        match2 = None
        link2 = None
        response2 = None
        req2 = None
        mainurl = None
        print x
        x = x+1

