import binascii
import os

# We need to keep track of some user info so we can connect
# to the jawbone api. Once we create a token, its good for a year,
# so we keep track of it so the user doesn't have to log in every time

class Session:
	# list of all the "base" properties that sessions always have
	default_properties = ['SessionUniqueId', 'SessionCreatedTimestamp']

	def __init__ (self, params):
		# default links to other objects
		self.Token = None

		# wtf is this
		for key, value in params.iteritems():
			setattr (self, key, value)

		# i like to make sure all my class properties exist, even if
		# they are empty (in php at least, i don't know if you would do
		# this in python)
		for key in self.__class__.default_properties:
			if not hasattr (self, key):
				setattr (self, key, None)

	def get_auth_url (self, config):
		return config.get_server_base_url() + "register/" + self.SessionUniqueId + "/"

	# This is sort of an uncommon way of doing things, but I think its best.
	# Our object doesn't know anything about a database, and our database doesn't
	# care about the internals of the object, and as long as they both agree on a
	# generic dumb intermediate format it doesn't matter. Also being able to easily
	# get an array (err... dictionary, right python?) version of an objects important
	# fields is very useful; then we can go wild adding properties and junk to our object
	# as we need to and we don't have to keep going to the db file like "ohhh make sure you
	# don't try to insert object.stupidCacheThing into the database!"
	#
	# A lot of frameworks seem to pull the columns straight from the DB - I don't know
	# if I like this way, I think it makes it easier to add fields and stuff if the object
	# itself is used as the canonical definition of the class. Blah blah blah
	def to_dict (self):
		dict = {}
		dict['SessionUniqueId'] = self.SessionUniqueId
		dict['SessionCreatedTimestamp'] = self.SessionCreatedTimestamp

		return dict

	@staticmethod
	def create():
		# we need a unique id to be able to identify ourselves on the server
		# we'll use a uuid so we don't have to consult the server an extra
		# time 
		# python has a uuid library but requiring a library to be installed to
		# replace 2 lines of code is insane
		new_id = binascii.b2a_hex (os.urandom (16))

		# a real uuid needs to have '4' as the 12th digit and '8', '9', 'a', or 'b'
		# as the 16th digit

		# to keep it random we take the 16th digit as an int and divide it by 4 (making it
		# equally likely to be 0, 1, 2, or 3 - and then we add 8 to it make it between 8, 9,
		# 10, and 11 (or '8', '9', 'a', and 'b' in hex)
		new_uuid = new_id[0:12]+'4'+new_id[13:16]+('%x' % ((int(new_id[16], 16) / 4) + 8))+new_id[17:32]

		session_params = {'SessionUniqueId' : new_uuid}

		return Session (session_params)
