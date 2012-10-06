from gi.repository import Gtk, GdkPixbuf, GObject
from urllib import request
from getted.tedlister import TEDTalk

class TEDTalkWidget (Gtk.Box):
	__gsignals__ = {
		'play-talk': (GObject.SIGNAL_RUN_LAST, None, (str,)),
		'save-talk': (GObject.SIGNAL_RUN_LAST, None, (str,))
       	}
	
	def __init__ (self, talk):
		Gtk.Box.__init__(self)
		#
		self.talk = talk
		#
		self.childbox_title = Gtk.Box(spacing=5, orientation=Gtk.Orientation.VERTICAL)
		titlelabel = Gtk.Label()
		titlelabel.set_markup("<b><span size=\"large\"><a href=\"talk:watch\">" + self.talk.title
		+ "</a></span></b>\n<i>By " + self.talk.speaker + "</i>")
		titlelabel.connect("activate-link", self.play_talk)
		self.childbox_title.pack_start(titlelabel, False, False, 2)
		datestr = self.talk.pub_date.strftime("%d %b %Y %H:%M")
		datelabel = Gtk.Label()
		datelabel.set_markup("<small>" + datestr + "</small>")
		self.childbox_title.pack_start(datelabel, False, False, 2)
		#
		self.talk_thumbnail = Gtk.Image(stock=Gtk.STOCK_REFRESH, icon_size=4) # Display a Gtk "Refresh" icon temporarily.
		self.__load_talk_thumbnail(self.talk.image) # Handle the image loading
		#
		self.childbox_buttons = Gtk.Box(spacing=10, orientation=Gtk.Orientation.HORIZONTAL)
		playbtn = Gtk.Button(Gtk.STOCK_MEDIA_PLAY)
		savebtn = Gtk.Button(Gtk.STOCK_SAVE)
		self.childbox_buttons.pack_start(playbtn, False, False, 2)
		self.childbox_buttons.pack_start(savebtn, False, False, 2)
		playbtn.connect("clicked", self.play_talk)
		savebtn.connect("clicked", self.save_talk)
		#
		self.pack_start(self.childbox_title, True, False, 1)
		self.pack_start(self.talk_thumbnail, True, False, 1)
		self.pack_start(self.childbox_buttons, True, False, 1)
		self.childbox_title.get_style_context().add_class("getted-talk-titlebox")
		self.childbox_buttons.get_style_context().add_class("getted-talk-buttonsbox")
		self.show_all()

	def __load_talk_thumbnail(self, imgurl):
		image = request.urlopen(imgurl)
		fname = imgurl.split('/')[-1]
		floc = '/tmp/getted/' + fname
		import os
		imgfile = open(floc, 'wb')
		imgfile.write(image.read())
		imgfile.close()
		
		pixbuf = GdkPixbuf.Pixbuf.new_from_file(floc)
		smallpixbuf = pixbuf.scale_simple(307, 230, GdkPixbuf.InterpType.BILINEAR)
		self.talk_thumbnail.set_from_pixbuf(smallpixbuf)
	
	def play_talk (self):
		self.emit("play-talk", self.talk.getHQVideolink())
	
	def save_talk (self):
		self.emit("save-talk", self.talk.getHQVideolink())
