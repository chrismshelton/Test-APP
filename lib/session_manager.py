from lib.session import Session

class SessionManager:
	def __init__ (self, config):
		self.config = config

	def create (self, session):
		params = session.to_dict()

		insert_columns = []
		param_columns = []

		for key in params:
			insert_columns.append (key)
			param_columns.append (":"+key)

		insert_list = ",".join (insert_columns)
		param_list = ",".join (param_columns)

		query = """
			INSERT
			INTO
				"Session"
				({insert_list})
					VALUES
				({param_list});
		"""

		full_query = query.format (insert_list = insert_list, param_list = param_list)

		db = self.config.get_app_database()
		cursor = db.cursor()
		cursor.execute (full_query, params)
		db.commit()
		return cursor.rowcount

	# Doesnt do anything yet (obviously)
	def delete (self, session):
		return

	# Doesnt do anything yet (obviously)
	def getAll (self):
		return

	# Returns a session (or None), given a session ID.
	def get (self, session_unique_id):
		query = "SELECT * FROM \"Session\" WHERE SessionUniqueID = :SessionUniqueID;"
		db = self.config.get_app_database()
		cursor = db.cursor()
		cursor.execute (query, {'SessionUniqueID' : session_unique_id})

		row = cursor.fetchone()
		params = {}

		for key in row.keys():
			params[key] = row[key]

		return Session (params)

	def save (self, session):
		# Because we make up our own primary key, instead of getting it
		# from the db (like with an AUTOINCREMENT integer), we don't know
		# whether we're INSERTing or UPDATEing a row. That's okay, though,
		# since 99% of the time we're going to be updating, we'll just assume
		# its an update and the number of rows changed is 0 then we know
		# we need to insert instead.

		rows = self.update (session)

		# -1 on error
		if rows <= 0:
			rows = self.create (session)

		if rows:
			return True
		else:
			return False

	def update (self, session):
		params = session.to_dict()

		update_columns = []

		for key in params:
			if key != 'SessionUniqueID':
				update_columns.append (key+" = :"+key)

		#                    wtf backwards
		update_column_list = ",".join (update_columns)

		query = """
			UPDATE
				"Session"
			SET
				{update_cols}
			WHERE
				SessionUniqueID = :SessionUniqueID;
		"""

		full_query = query.format(update_cols = ",".join(update_columns))
		db = self.config.get_app_database()
		cursor = db.cursor()
		cursor.execute (full_query, params)
		db.commit()
		return cursor.rowcount
