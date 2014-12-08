from gi.repository import GLib
import os.path
import sqlite3

from lib.app_settings_manager import AppSettingsManager
from lib.api_manager import APIManager
from lib.token_manager import TokenManager
from lib.session_manager import SessionManager

# Ugh. Python doesn't have a __DIR__, only a __file__... BUT IT CHANGES. WTF.
# So we need to save it here or else we might lose it
_SOURCE_BASE_DIR = os.path.dirname (os.path.dirname (os.path.realpath(__file__)))

class Config():
	def __init__(self):
		self.config_db = None
		self.init_default()

	def init_default (self):
		self.apiManager = APIManager()
		self.appSettingsManager = AppSettingsManager (self)
		self.sessionManager = SessionManager (self)
		self.tokenManager = TokenManager (self)

	def get_app_config_directory (self):
		data_dir = GLib.get_user_config_dir()
		app_dir = data_dir+"/test-app"

		if not os.path.isdir(app_dir):
			os.mkdir (app_dir)

		return app_dir

	def get_app_database (self):
		if self.config_db is None:
			app_dir = self.get_app_config_directory()
			self.config_db = sqlite3.connect (app_dir+"/config.sqlite3")
			self.config_db.row_factory=sqlite3.Row

			with file(_SOURCE_BASE_DIR+"/db/schema.sql") as f:
				sql = f.read()

			self.config_db.executescript (sql)

		return self.config_db

	def get_server_base_url (self):
		return "https://cmshelton.com/jb/"
