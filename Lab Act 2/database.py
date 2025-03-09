import mysql.connector

class Database:
    def __init__(self):
        self.__conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="admin",
            database="nonprofit_donation_db"
        )
        self.__cursor = self.__conn.cursor()

    def execute(self, query, params=None):
        self.__cursor.execute(query, params or ())
        self.__conn.commit()

    def fetch(self, query, params=None):
        self.__cursor.execute(query, params or ())
        return self.__cursor.fetchall()

    def close(self):
        self.__cursor.close()
        self.__conn.close()