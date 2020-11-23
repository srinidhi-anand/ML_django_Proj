import sqlite3
import traceback
import sys
from datetime import date

def convertToBinaryData(filename):
    #Convert digital data to binary format
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData

def db_sqlite_qry(obj_class, imagebytes):
	try:
		sqliteConnection = sqlite3.connect('SQLite_Python.db')
		cursor = sqliteConnection.cursor()
		create_sql = """ CREATE TABLE if not exists mld_app (id INTEGER PRIMARY KEY AUTOINCREMENT,user_name TEXT NOT NULL,password TEXT NOT NULL,object_class TEXT NOT NULL,images   BLOB, current_date DATE );"""
		
		query = cursor.execute(create_sql)
		#print("table created SqliteDb_developers table ", cursor.rowcount)
		sqlite_insert_query = """INSERT into mld_app( user_name, password, object_class, images,current_date)  VALUES(?, ?, ?, ?, ?);"""
		today = date.today()
		data_tuple = ('admin', 'password123', obj_class,imagebytes, today)
		cursor.execute(sqlite_insert_query,data_tuple) 
		
		sqliteConnection.commit()
		#print("Record inserted successfully into SqliteDb_developers table ", cursor.rowcount)
		cursor.close()

	except sqlite3.Error as error:
		print("Exception is", error.args)
		exc_type, exc_value, exc_tb = sys.exc_info()
	finally:
		if (sqliteConnection):
			sqliteConnection.close()
			
	return True

