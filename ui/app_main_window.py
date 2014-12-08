from gi.repository import Gtk, Gdk

# copied most of this out of https://developer.gnome.org/gnome-devel-demos/stable/GtkApplicationWindow.py.html

class AppMainWindow (Gtk.ApplicationWindow):
	def __init__ (self, application):
		Gtk.Window.__init__ (self, title="Jawbone UP", application=application)

		# we don't want our app to start up with a dinky little 100x100px window
		# so get the screen size and set the width and height to half the max
		# this makes a reasonable sized window
		screen = Gdk.Screen.get_default()
		self.set_size_request (screen.get_width() / 2, screen.get_height() / 2)
