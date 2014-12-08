from gi.repository import Gtk

from controllers.main_controller import MainController
from lib.config import Config

from ui.app_main_window import AppMainWindow

class AppMain (Gtk.Application):
	def __init__ (self):
		Gtk.Application.__init__ (self)

		self.config = Config()

	def do_activate (self):
		self.window = AppMainWindow (self)
		self.window.show_all()

		self.controller = MainController(self)
		self.controller.start()
		#self.window.show_add_account_popup (self.config)

	def do_startup (self):
		Gtk.Application.do_startup (self)
