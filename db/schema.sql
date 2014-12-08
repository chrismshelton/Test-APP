/*
 * We need to keep track of the users oauth token, but i'm sure we'll eventually want
 * to keep track of some other data too. So lets just plan on using a database right
 * from the start. SQLite is perfect for this; it doesn't need its own process like
 * mysql and other "big" dbs, it uses a (small) single file for storage, but it still
 * gives us all the flexibility and reliability of sql.
 */

CREATE TABLE IF NOT EXISTS Session (
	/* SessionUniqueID because SessionUUID looks AWFUL */
	SessionUniqueID text NOT NULL PRIMARY KEY,

	SessionCreatedTimestamp text NULL DEFAULT NULL
);


/*
 * I'm pretty sure UP said you can only have one token per app per user,
 * but anyways, it's clunky trying to put it in the Session table, because
 * the names end up way too long... SessionTokenAccessToken...
 * SessionTokenCreatedTimestamp... yuck
 */
CREATE TABLE IF NOT EXISTS Token (
	TokenID integer AUTO_INCREMENT PRIMARY KEY,

	/* This token belogs to someone.. who? */
	SessionUniqueID text NOT NULL,

	TokenAccessToken text NOT NULL,

	TokenRefreshToken text NOT NULL,

	TokenCreatedTimestamp datetime NOT NULL,

	TokenExpireTimestamp datetime NOT NULL,

	/*
	 * This makes sure every token belongs to an existing session!
	 */
	FOREIGN KEY (SessionUniqueID) REFERENCES Session (SessionUniqueID)
);


/*
 * I've never done this before, but I've always wondered if it would work well;
 * sometimes you want to have some global application settings where each setting
 * is just a single value; normally i guess I'd use like a json file or something,
 * but lets see how this works
 */
CREATE TABLE IF NOT EXISTS AppSettings (
	AppSettingsKey text NOT NULL PRIMARY KEY,
	AppSettingsValue text NOT NULL
);
