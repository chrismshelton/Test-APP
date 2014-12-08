class AppSettingsManager:
	def __init__ (self, config):
		self.config = config

	# Inserts the given key/value pair into the database
	def createKey (self, key, value):
		db = self.config.get_app_database()
		query = "INSERT INTO AppSettings (AppSettingsKey, AppSettingsValue) VALUES (:AppSettingsKey, :AppSettingsValue);"
		cursor = db.cursor()
		cursor.execute (query, {"AppSettingsKey" : key, "AppSettingsValue" : value})
		db.commit()
		return cursor.rowcount

	# Looks up a key in the database. Returns a string, or None.
	def getValueForKey (self, key):
		db = self.config.get_app_database()
		query = "SELECT AppSettingsValue FROM AppSettings WHERE AppSettingsKey = :AppSettingsKey;"
		cursor = db.cursor()
		cursor.execute (query, {"AppSettingsKey" : key})
		value = cursor.fetchone()

		if value is not None:
			return value[0]
		else:
			return None

	# Inserts the key/value pair into the database if the key does not
	# already exist. Updates the existing value if the key does exist.
	def setKey (self, key, value):
		rows = self.updateKey (key, value)

		if rows <= 0:
			rows = self.createKey (key, value)

		if rows > 0:
			return True
		else:
			return False

	def updateKey (self, key, value):
		db = self.config.get_app_database()
		query = "UPDATE AppSettings SET AppSettingsValue = :AppSettingsValue WHERE AppSettingsKey = :AppSettingsKey;"
		cursor = db.cursor()
		cursor.execute (query, {"AppSettingsKey" : key, "AppSettingsValue" : value})
		db.commit()
		return cursor.rowcount
