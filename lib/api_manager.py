from jawbone import Jawbone
import utilities

#
# A helper class around the helper class for working with the API
#
# This class basically just gives us a function for each of
# jawbones "endpoint" urls. That way it looks cleaner when we
# call them from elsewhere in the code, and it will be easier to
# update them in the case that the api changes (for example, if
# Jawbone releases a v1.2 api)
#
class APIManager:
	def __init__ (self):
		self.api = Jawbone ('', '', '', '')

	def add_param_if_not_none (self, params, key, value):
		if value is not None:
			params[key] = value

	#
	# https://jawbone.com/up/developer/endpoints/moves
	#
	def get_moves (self, token, params):
		valid_params = ['date', 'page_token', 'start_time', 'end_time', 'updated_after']

		for key in params.keys():
			if key not in valid_params:
				raise ValueError ("Invalid key '%s' in function '%s'" % (key, utilities.current_function_name()))

		return self.api.api_call (token.TokenAccessToken, "nudge/api/v.1.1/users/@me/moves", **params)

	def get_sleeps (self, token, params):
		valid_params = ['date', 'page_token', 'start_time', 'end_time', 'updated_after']

		for key in params.keys():
			if key not in valid_params:
				raise ValueError ("Invalid key '%s' in function '%s'" % (key, utilities.current_function_name()))

		return self.api.api_call (token.TokenAccessToken, "nudge/api/v.1.1/users/@me/sleeps", **params)

	def get_sleep_phases (self, token, xid):
		url = "nudge/api/v.1.1/sleeps/{0}/ticks".format (xid)

		return self.api.api_call (token.TokenAccessToken, url)
