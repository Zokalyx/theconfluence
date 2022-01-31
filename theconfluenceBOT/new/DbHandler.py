# Modification of Thejusko's original file
# Adjusted for single db connection (not pooled)
# This is just to test the functionality of redditorqueue.py

import mysql.connector
from mysql.connector import errorcode


class DbHandler:

    _connection: mysql.connector.connection
    

    def __init__(self):
        """
            Create a DB connection

            If a Database Connection Pool already exists,
            don't create a new connection
            Instead get a connection from the pool
        """
        try:
            DbHandler._connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="redditbot",
                autocommit=True,
            )
        except (mysql.connector.Error) as e:
            if e.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Access to database denied. Please check credentials.")
            elif e.errno == errorcode.ER_BAD_DB_ERROR:
                print("Chosen database does not exist.")
            else:
                print(e)

        except Exception as e:
            print(e)


    def fetchAll(self, query, data):
        cursor = None
        try:
            self._connection.reconnect()
            cursor = self._connection.cursor()
        except (ValueError):
           print("Cursor is unavailable")

        result = []
        if cursor is not None:
            try:
                cursor.execute(query, data)
            except Exception as e:
                print("Failed Query: " + cursor.statement + "\n" + str(e))
            warnings = cursor.fetchwarnings()
            if warnings:
                print(f"Insert containes following warnings:\n {warnings}")
            result = cursor.fetchall()
            cursor.close()
        return result

    def execute(self, query, data):
        cursor = None
        try:
            self._connection.reconnect()
            cursor = self._connection.cursor()
        except (ValueError):
            print("Cursor is unavailable")

        if cursor is not None:
            try:
                cursor.execute(query, data)
            except Exception as e:
                print("Failed Query: " + cursor.statement + "\n" + str(e))
            warnings = cursor.fetchwarnings()
            if warnings:
                print(f"Insert containes following warnings:\n {warnings}")
            cursor.close()
