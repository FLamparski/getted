# (c) 2012 by Filip Wieland <matka.poohatka@gmail.com>
# GPL 3
# Enjoy ;)

"""
This module includes the core elements of GetTED: The function to load TED RSS
file, and a class representing a TED Talk, which in GetTED underlays the
TEDTalkWidget.
"""

from urllib.request import urlopen
from xml.dom import minidom
import datetime

class TEDTalk (object):
	def __init__ (self, item_dom):
		self.title = item_dom.getElementsByTagName("title")[0].childNodes[0].toxml()
		self.speaker = item_dom.getElementsByTagName("itunes:author")[0].childNodes[0].toxml()
		self.description = item_dom.getElementsByTagName("description")[0].childNodes[0].toxml()
		pub_date_str = item_dom.getElementsByTagName("pubDate")[0].childNodes[0].toxml()
		self.pub_date = datetime.datetime.strptime(pub_date_str, "%a, %d %b %Y %H:%M:%S +0000")
		self.image = item_dom.getElementsByTagName("itunes:image")[0].attributes['url'].value
		self.duration = item_dom.getElementsByTagName("itunes:duration")[0].childNodes[0].toxml()
		self.videolink = item_dom.getElementsByTagName("feedburner:origEnclosureLink")[0].childNodes[0].toxml()
	
	def getHQVideolink(self):
		link = self.videolink.split('?')[0]
		return link[:-4] + "-480p" + link[-4:]

def GetTEDTalks ():
	ted_talks = [] # TEDTalk collection
	feedfile = urlopen("http://feeds.feedburner.com/tedtalks_video")
	feed = minidom.parse(feedfile)
	feeditems = feed.getElementsByTagName("item")
	for item in feeditems:
		talk = TEDTalk(item)
		ted_talks.append(talk)
	return ted_talks

