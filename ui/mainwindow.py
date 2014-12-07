from gi.repository import Gtk, Gdk

from lib.config import Config
from lib.session import Session
from ui.addaccountwindow import AddAccountWindow

# copied most of this out of https://developer.gnome.org/gnome-devel-demos/stable/GtkApplicationWindow.py.html

class AppMainWindow (Gtk.ApplicationWindow):
	def __init__ (self, application):
		Gtk.Window.__init__ (self, title="Jawbone UP", application=application)

		# we don't want our app to start up with a dinky little 100x100px window
		# so get the screen size and set the width and height to half the max
		# this makes a reasonable sized window
		screen = Gdk.Screen.get_default()
		self.set_size_request (screen.get_width() / 2, screen.get_height() / 2)

	def show_add_account_popup (self, config):
		new_session = None
		dialog = AddAccountWindow (self, config)
		response = dialog.run()

		if response == Gtk.ResponseType.OK:
			new_session = dialog.get_session()

		dialog.destroy()
		print ("Response: "+str(new_session))

class AppMain (Gtk.Application):
	def __init__ (self):
		Gtk.Application.__init__ (self)
		self.config = Config()

	def do_activate (self):
		self.window = AppMainWindow (self)
		self.window.show_all()
		self.window.show_add_account_popup (self.config)

	def do_startup (self):
		Gtk.Application.do_startup (self)
