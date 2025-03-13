import mysql.connector

class Database:
    def __init__(self):
        try:
            self.connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="4122133pogi",
                database="nonprofit_donation_db"
            )
            if self.connection.is_connected():
                self.cursor = self.connection.cursor()  # ✅ Ensure cursor is created
            else:
                print("❌ Failed to connect to the database!")
                self.cursor = None
        except mysql.connector.Error as e:
            print(f"❌ Database connection failed! Error: {e}")
            self.connection = None
            self.cursor = None

    def execute(self, query, values=None):
        try:
            if not self.cursor:
                raise Exception("❌ ERROR: Cursor not initialized!")
            self.cursor.execute(query, values or ())
            self.connection.commit()
        except Exception as e:
            print(f"❌ ERROR: Database execution failed! {e}")

    def fetch(self, query, values=None):
        try:
            if not self.cursor:
                raise Exception("❌ ERROR: Cursor not initialized!")
            self.cursor.execute(query, values or ())
            return self.cursor.fetchall()
        except Exception as e:
            print(f"❌ ERROR: Database fetch failed! {e}")
            return None

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
