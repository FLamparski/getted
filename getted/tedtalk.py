from gi.repository import Gtk, GdkPixbuf
from urllib import request
from GetTED.tedlister import TEDTalk

class TEDTalkWidget (Gtk.Box):
	def __init__ (self, talk):
		Gtk.Box.__init__(self)
		#
		self.talk = talk
		#
		self.childbox_title = Gtk.Box(spacing=5, orientation=Gtk.Orientation.VERTICAL)
		titlelabel = Gtk.Label()
		titlelabel.set_markup("<b><span style=\"font-size:large\"><a href=\"talk:watch\">" + self.talk.title
		+ "</a></span></b><br/><i>By " + self.talk.speaker + "</i>")
		titlelabel.connect("activate-link", self.play_talk)
		self.childbox_title.pack_start(titlelabel)
		datestr = self.talk.pub_date.strftime("%d %b %Y %H:%M")
		datelabel = Gtk.Label()
		datelabel.set_markup("<small>" + datestr + "</small>")
		self.childbox_title.pack_start(datelabel)
		#
		self.talk_thumbnail = Gtk.Image(stock=Gtk.STOCK_REFRESH, icon-size=4) # Display a Gtk "Refresh" icon temporarily.
		self.__load_talk_thumbnail(self.talk.image) # Handle the image loading
		#
		self.childbox_buttons = Gtk.Box(spacing=10, orientation=Gtk.Orientation.HORIZONTAL)
		playbtn = Gtk.Button(Gtk.STOCK_MEDIA_PLAY)
		savebtn = Gtk.Button(Gtk.STOCK_SAVE)
		self.childbox_buttons.pack_start(playbtn)
		self.childbox_buttons.pack_start(savebtn)
		playbtn.connect("clicked", self.play_talk)
		savebtn.connect("clicked", self.save_talk)
		#
		self.pack_start(self.childbox_title)
		self.pack_start(self.talk_thumbnail)
		self.pack_start(self.childbox_buttons)
		self.childbox_title.get_style_context().add_class("getted-talk-titlebox")
		self.childbox_buttons.get_style_context().add_class("getted-talk-buttonsbox")

	def __load_talk_thumbnail(self, imgurl):
		image = request.urlopen(imgurl)
		pixbuf = GdkPixbuf.Pixbuf.new_from_stream(image)
		smallpixbuf = pixbuf.scale_simple(307, 230, GdkPixbuf.InterpType.BILINEAR)
		self.talk_thumbnail.set_from_pixbuf(smallpixbuf)
