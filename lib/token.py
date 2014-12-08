from datetime import datetime

class Token:
	default_properties = ['TokenID', 'SessionUniqueID', 'TokenAccessToken', 'TokenRefreshToken', 'TokenCreatedTimestamp', 'TokenExpireTimestamp']

	def __init__ (self, params={}):
		# default links to other objects
		self.session = None

		for key, value in params.iteritems():
			setattr (self, key, value)

		for key in self.__class__.default_properties:
			if not hasattr (self, key):
				setattr (self, key, None)

	def to_dict (self):
		dict = {}
		dict['TokenID'] = self.TokenID
		dict['SessionUniqueID'] = self.SessionUniqueID
		dict['TokenAccessToken'] = self.TokenAccessToken
		dict['TokenRefreshToken'] = self.TokenRefreshToken
		dict['TokenCreatedTimestamp'] = self.TokenCreatedTimestamp
		dict['TokenExpireTimestamp'] = self.TokenExpireTimestamp

		return dict

	def update_with_new_token_info (self, params):
		self.TokenAccessToken = params['access_token']
		self.TokenRefreshToken = params['refresh_token']

		if self.TokenCreatedTimestamp is None:
			self.TokenCreatedTimestamp = datetime.fromtimestamp(params['token_created']).strftime("%Y-%m-%d %H:%M:%S")

		self.TokenExpireTimestamp = datetime.fromtimestamp(params['token_created'] + params['expires_in']).strftime("%Y-%m-%d %H:%M:%S")
