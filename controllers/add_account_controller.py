import base64
from gi.repository import Gio, Gtk
import json

from lib.session import Session
from lib.token import Token
from ui.add_account_window import AddAccountWindow

#
# This class contains all the logic for signing up someone with our app.
# 
class AddAccountController:
	def __init__ (self, config, app):
		self.app = app
		self.config = config
		self.session = Session.create()
		self.session_created = False

	# This is the main method for this controller. It creates a new
	# pop up window, and asks the user to sign up. If the sign up
	# completes successfully, it returns them a new session/token.
	# If it doesn't (for example, if the user closes the pop up without
	# entering in a code), None is returned.
	def add_user_account (self):
		dialog = AddAccountWindow (self, self.app.get_active_window())

		dialog.connect ("sign-in", self.on_sign_in)
		dialog.connect ("token-entered", self.on_token_entered)

		response = dialog.run()

		if response == Gtk.ResponseType.OK:
			controller.create_session()

		dialog.destroy()

		if self.session.token is not None:
			return self.session
		else:
			return None

	# Returns true if a Token string is able to be unserialized correctly;
	# False if it is not.
	def is_token_string_valid (self, token_string):
		return (self.unserialize_user_token (token_string) is not None)

	# When the user clicks the button to sign in, launch the appropriate url
	# in their default browser.
	def on_sign_in (self, dialog):
		url = self.session.get_auth_url (self.config)
		Gio.AppInfo.launch_default_for_uri (url)

	# Whenever the user changes the contents of the "paste your code in here" box,
	# check to see if its a valid token. If it is, we did it! Yaay!
	def on_token_entered (self, dialog, token_string):
		if self.is_token_string_valid (token_string):
			self.update_session_with_token (token_string)
			dialog.set_complete()

	# Create a token object from the string the user pasted in,
	# and add it to our app database
	def token_object_from_string (self, token_string):
		object = self.unserialize_user_token (token_string)

		params = {'SessionUniqueID' : self.session.SessionUniqueID}
		print self.session.to_dict()
		print params
		token = Token (params)
		token.session = self.session
		token.update_with_new_token_info (object)

		return token

	# Try to unserialize the user-given string. Returns
	# either a dictionary, or None.
	def unserialize_user_token (self, base64_text):
		text = base64.b64decode (base64_text)

		if text == "":
			# invalid code
			return None

		try:
			token = json.loads (text)
			return token
		except ValueError:
			# invalid code
			return None

	# Take the array of values we got from the server and
	# update the appropriate token properties with them.
	# Save the new token.
	def update_session_with_token (self, token_string):
		token = self.token_object_from_string (token_string)
		self.config.sessionManager.save (self.session)
		self.session.token = token
		self.config.tokenManager.save (token)

		

		#if token is not None:
		#	self.session.token = token
		#	self.response (Gtk.ResponseType.OK)
