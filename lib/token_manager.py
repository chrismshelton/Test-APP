from lib.token import Token

class TokenManager:
	def __init__ (self, config):
		self.config = config

	# Create a new token.
	# Sets the TokenID property of the token object
	# if the token was inserted succesfully.
	# Returns the number of rows added (0 or 1)
	def create (self, token):
		params = token.to_dict()

		insert_columns = []
		param_columns = []

		for key in params:
			# don't insert an id, so we get an AUTO_INCREMENT value
			if key != 'TokenID':
				insert_columns.append (key)
				param_columns.append (":"+key)

		insert_list = ",".join (insert_columns)
		param_list = ",".join (param_columns)

		query = """
			INSERT
			INTO
				"Token"
				({insert_list})
					VALUES
				({param_list});
		"""

		full_query = query.format (insert_list = insert_list, param_list = param_list)

		print full_query
		print params

		db = self.config.get_app_database()
		cursor = db.cursor()
		cursor.execute (full_query, params)
		db.commit()

		if cursor.rowcount >= 0:
			token.TokenID = cursor.lastrowid

		return cursor.rowcount

	def delete (self, token):
		return

	def getAll (self):
		return

	# Returns the token for the given session id, or None.
	def get_by_session_id (self, session_unique_id):
		query = """
			SELECT
				*
			FROM
				"Token"
			WHERE
				SessionUniqueID = :SessionUniqueID;
		"""

		db = self.config.get_app_database()
		cursor = db.cursor()
		cursor.execute (query, {'SessionUniqueID' : session_unique_id})
		row = cursor.fetchone()

		if row is None:
			return None

		params = {}

		for key in row.keys():
			params[key] = row[key]

		return Token (params)

	# Writes the token into the database. If it is already in the database,
	# the existing rows properties are updated.
	def save (self, token):
		rows = self.update (token)

		# -1 on error
		if rows <= 0:
			rows = self.create (token)

		if rows:
			return True
		else:
			return False

	def update (self, token):
		if token.TokenID is None:
			return False

		params = token.to_dict()

		update_columns = []

		for key in params:
			if key != 'TokenID':
				update_columns.append (key+" = :"+key)

		#                    wtf backwards
		update_column_list = ",".join (update_columns)

		query = """
			UPDATE
				"Token"
			SET
				{update_cols}
			WHERE
				TokenID = :TokenID;
		"""

		full_query = query.format(update_cols = ",".join(update_columns))
		db = self.config.get_app_database()
		cursor = db.cursor()
		cursor.execute (full_query, params)
		db.commit()
		return cursor.rowcount
