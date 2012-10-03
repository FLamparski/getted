from gi.repository import Gtk
from getted.tedtalk import TEDTalkWidget
from getted.tedlister import TEDTalk

class CustomToolbar(Gtk.Toolbar):
    def __init__(self):
        super(CustomToolbar, self).__init__()
        self.get_style_context().add_class(Gtk.STYLE_CLASS_PRIMARY_TOOLBAR) #Style this as Primary Toolbar
    
    def insert(self, item, pos):
        ''' If widget item is not a ToolItem, make it one. '''
        if not isinstance(item, Gtk.ToolItem):
            widget = Gtk.ToolItem()
            widget.add(item)
            item = widget
        
        super(CustomToolbar, self).insert(item, pos)
        return item

class GetTEDWindow (Gtk.Window):
    def __init__ (self):
        # Also init: Window
        Gtk.Window.__init__(self)
        self.set_default_size(400, 500)
        
        container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.banner = CustomToolbar()
        
        # Generate the custom toolbar
        self.setup_toolbar()
        container.pack_start(self.banner, expand=False, fill=True, padding=2)
        
        # Main window setup
        scrolled_window = Gtk.ScrolledWindow()
        self.TEDviewport = Gtk.Viewport()
        scrolled_window.add(self.TEDviewport)
        container.pack_start(scrolled_window, True, True, 5)
        
        self.busy_spinner = Gtk.Spinner(active=True)
        self.TEDviewport.add(self.busy_spinner)
        
        self.statusbar = Gtk.Statusbar()
        
        container.pack_start(self.statusbar, expand=False, fill=True, padding=2)
        self.add(container)
    
    def setup_toolbar(self):
        titlelbl = Gtk.Label()
        titlelbl.set_markup("""<span size="x-large"><span color="white"><b>Get<span color="red">TED</span></b></span></span>""")
        self.banner.insert(titlelbl, 0).set_expand(True)
        
        separator0 = Gtk.SeparatorToolItem()
        self.banner.insert(separator0, 1)
        
        button_refresh = Gtk.ToolButton(label="Refresh feed")
        button_refresh.set_icon_widget(Gtk.Image.new_from_stock(Gtk.STOCK_REFRESH, 2))
        self.banner.insert(button_refresh, 2)
        
        button_options = Gtk.ToolButton(label="Options")
        button_options.set_icon_widget(Gtk.Image.new_from_stock(Gtk.STOCK_PREFERENCES, 2))
        self.banner.insert(button_options, 3)
