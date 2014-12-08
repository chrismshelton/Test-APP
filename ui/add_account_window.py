from gi.repository import Gtk, GObject

# http://python-gtk-3-tutorial.readthedocs.org/en/latest/dialogs.html

class AddAccountWindow (Gtk.Dialog):
	__gsignals__ = {
		'sign-in': (GObject.SIGNAL_RUN_FIRST, None, ()),
		'token-entered': (GObject.SIGNAL_RUN_FIRST, None, (str,)),
	}

	def __init__ (self, controller, parent):
		Gtk.Dialog.__init__ (self, "Add Account", parent, 0)
		self.set_default_size (400, 300)

		label = Gtk.Label ("First, you have to login to the UP app and get an auth code. Once you have a code, enter it in the box below.")
		label.set_line_wrap (True)

		box = self.get_content_area()
		box.add (label)

		b1 = Gtk.Button ("Sign in to UP!")
		b1.connect ("clicked", self.on_sign_in)

		# if we don't make a "Box" to put the button in then it makes
		# the button HUGE and it looks dumb
		b1_box = Gtk.Box()
		b1_box.add (b1)

		self.code_entry = Gtk.TextView()
		# removed for easier debugging
		#self.code_entry.set_editable (False)
		self.code_entry.set_size_request (200, 200)
		self.code_entry.set_wrap_mode (Gtk.WrapMode.CHAR)

		self.code_entry.get_buffer().connect ("modified-changed", self.on_text_changed)

		# Gtk puts things one after the other in the order that you add them.
		# Each container has an "orientation", so adding 3 things to a
		# horizontal container will put them like this:
		#		a b c
		#
		# and adding 3 things to a vertical container will put them
		# like this:
		#		a
		#		b
		#		c
		#
		# The default container for a "Dialog" appears to be horizontal,
		# but we want our text input to be below the button, so we should
		# make a new vertical box to organize them
		button_box = Gtk.Box (orientation=Gtk.Orientation.VERTICAL)
		button_box.pack_start (b1_box, False, False, 2)
		button_box.add (self.code_entry)

		box.pack_start (button_box, True, True, 2)

		self.show_all()

	def on_response (self, arg1, response):
		self.destroy()

	def on_sign_in (self, button):
		self.code_entry.set_editable (True)
		self.emit ("sign-in")

	def on_text_changed (self, buffer):
		bounds = buffer.get_bounds()
		text = buffer.get_text (bounds[0], bounds[1], False)
		self.emit ("token-entered", text)

	def set_complete (self):
		self.destroy()
