from database import Database

class User:
    def __init__(self, db):
        self.__db = db

    def register(self, name, email, password, role):
        query = "INSERT INTO users (name, email, password, role) VALUES (%s, %s, %s, %s)"
        self.__db.execute(query, (name, email, password, role))
        print("User registered successfully!")

    def login(self, email, password):
        query = "SELECT * FROM users WHERE email=%s AND password=%s"
        user = self.__db.fetch(query, (email, password))
        if user:
            print(f"Welcome, {user[0][1]}! You are logged in as {user[0][4]}.")
            return user[0]
        else:
            print("Invalid email or password.")
            return None