import sqlite3
import traceback
import sys

def deleteHistory():
	try:
		sqliteConnection = sqlite3.connect('SQLite_Python.db')
		cursor = sqliteConnection.cursor()
		delete_sql = """DELETE FROM mld_app WHERE current_date  BETWEEN datetime('now', '-15 days') AND datetime('now');"""
		query = cursor.execute(delete_sql)
		sqliteConnection.commit()
		cursor.close()

	except sqlite3.Error as error:
		print("Exception is", error.args)
	finally:
		if (sqliteConnection):
			sqliteConnection.close()
			print("The SQLite connection is closed")
			
	return 'deleted!'
	


