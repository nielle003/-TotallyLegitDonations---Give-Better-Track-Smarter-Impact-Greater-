import mysql.connector

class Database:
    def __init__(self):
        try:
            self.connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="admin",
                database="nonprofit_donation_db"
            )
            if self.connection.is_connected():
                self.cursor = self.connection.cursor()
                print("✅ Connected to the database.")
            else:
                raise Exception("Connection established, but not marked as connected.")
        except mysql.connector.Error as e:
            print(f"❌ Database connection failed! Error: {e}")
            self.connection = None
            self.cursor = None

    def execute(self, query, values=None):
        try:
            if not self.cursor:
                raise Exception("Cursor is not initialized.")
            self.cursor.execute(query, values or ())
            self.connection.commit()
        except mysql.connector.Error as e:
            print(f"❌ ERROR: MySQL execution failed: {e}")
        except Exception as e:
            print(f"❌ ERROR: Execution failed: {e}")

    def fetch(self, query, values=None):
        try:
            if not self.cursor:
                raise Exception("Cursor is not initialized.")
            self.cursor.execute(query, values or ())
            return self.cursor.fetchall()
        except mysql.connector.Error as e:
            print(f"❌ ERROR: MySQL fetch failed: {e}")
        except Exception as e:
            print(f"❌ ERROR: Fetch failed: {e}")
        return []

    def fetch_one(self, query, values=None):
        try:
            if not self.cursor:
                raise Exception("Cursor is not initialized.")
            self.cursor.execute(query, values or ())
            return self.cursor.fetchone()
        except mysql.connector.Error as e:
            print(f"❌ ERROR: MySQL fetch_one failed: {e}")
        except Exception as e:
            print(f"❌ ERROR: Fetch_one failed: {e}")
        return None

    def close(self):
        try:
            if self.cursor:
                self.cursor.close()
            if self.connection:
                self.connection.close()
            print("🔒 Database connection closed.")
        except mysql.connector.Error as e:
            print(f"❌ ERROR: Failed to close database properly: {e}")
        except Exception as e:
            print(f"❌ ERROR: General close error: {e}")
