import sqlite3

con = sqlite3.connect('db.sqlite', check_same_thread=False)


def db_init(path):
	global con
	
	with con:
		con.execute("""CREATE TABLE IF NOT EXISTS User (
			id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
			login TEXT
		)""")
