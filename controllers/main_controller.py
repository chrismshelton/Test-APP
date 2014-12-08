import json

from controllers.add_account_controller import AddAccountController

from lib.config import Config

# This class manages the main application flow
class MainController:
	def __init__ (self, app):
		self.app = app
		self.config = Config()

		self.currentSession = None

	def find_default_session (self):
		default_session_id = self.config.appSettingsManager.getValueForKey ("DefaultSession")

		if default_session_id is None:
			return None

		default_session = self.config.sessionManager.get (default_session_id)

		#if default_session is None:
		# do some error thing here	

		return default_session

	# Loads the default session/token if there is one,
	# otherwise asks the user to sign up
	def find_or_create_default_session (self):
		session = self.find_default_session()

		if session is None:
			add_account = AddAccountController (self.config, self.app)
			session = add_account.add_user_account()

			if session is not None:
				self.set_as_default_session (session)

		return session

	# Set a session as the app default. It will be loaded
	# automatically on start-up next time.
	def set_as_default_session (self, session):
		print session.SessionUniqueID
		self.config.appSettingsManager.setKey ("DefaultSession", session.SessionUniqueID)

	# This is where the app "starts"
	# It doesn't do anything yet, except do some test api calls and print the results
	def start (self):
		self.currentSession = self.find_or_create_default_session()

		if self.currentSession.token is None:
			self.currentSession.token = self.config.tokenManager.get_by_session_id (self.currentSession.SessionUniqueID)

		if self.currentSession.token is not None:
			moves = self.config.apiManager.get_moves (self.currentSession.token, {'date' : '20141205'})
			print json.dumps (moves, indent=4)

			sleeps = self.config.apiManager.get_sleeps (self.currentSession.token, {'date' : '20141205'})
			print json.dumps (sleeps, indent=4)

			for sleep in sleeps['data']['items']:
				phases = self.config.apiManager.get_sleep_phases (self.currentSession.token, sleep['xid'])
				print json.dumps (phases, indent=4)
