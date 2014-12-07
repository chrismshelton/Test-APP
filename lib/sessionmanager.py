class SessionManager:
	def __init__ (self, config):
		self.config = config

	def create (self, session):

	def delete (self, session):

	def getAll (self):

	def get (self, session_unique_id):

	def save (self, session):
		# Because we make up our own primary key, instead of getting it
		# from the db (like with an AUTOINCREMENT integer), we don't know
		# whether we're INSERTing or UPDATEing a row. That's okay, though,
		# since 99% of the time we're going to be updating, we'll just assume
		# its an update and the number of rows changed is 0 then we know
		# we need to insert instead.

		rows = self.update (session)

		if rows == 0:
			rows = self.create (session)

		if rows:
			return True
		else:
			return False

	def update (self, session):				
