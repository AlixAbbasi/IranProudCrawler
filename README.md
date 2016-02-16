# IranProudCrawler
IranProudCrawler is a python script to detect live tv urls from IranProud servers and put it into an M3U compatible file. You can use this file in your TVBox using the IPTV Simple PVR.

### Whats new in version 1.2
- Compatible with OpenElec 6.x
- No longer using urllib, we are now using the requests to make the performance better
- Support icon! now you can add icons to the channel. Please look at the `How to add icons' section.
- Fixed a bug in the v1.0 which was not working with IPTV Simple PVR

###Requirements
- Its better you run this code in Linux, e.g. the OpenElec itself
- You need to install the `requests` module. To install the module please type `sudo pip install requests` and you are ready!. 
- Please make sure that you have a "icons" folder in the same folder as crawler.py. 

### Install on OpenElec
- Once you installed the OpenElec please install the IPTV Simple PVR.
- Then either copy the `tvlist.m3u` file (as a result of executing the `crawler.py`) and the icons dir to the OpenElec `/storage` dir or directly run this code in the `/storage`. 

### How to add icons
- Copy the icons folder created and filled by the script to your KODI/OpenElec machine
- Start KODI, go to Settings->AddOns->My Addons -> PVR Clients -> PRV IPTV Simple Client -> Configure-> Channel Logos and set the XML logos choice thing to Ignore
- Go to Settings->TV->OSD/Menu-> Menu/OSD and set "Folder with channel icons" to point at our icons folder located at `/storage/icons.
- Click "scan for missing icons"
- Enjoy!
