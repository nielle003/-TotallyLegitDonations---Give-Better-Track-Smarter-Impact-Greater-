class User:
    def __init__(self, db):
        self.__db = db  # ✅ Correct attribute

    def register(self, name, email, password, role):
        query = "INSERT INTO users (name, email, password, role) VALUES (%s, %s, %s, %s)"
        self.__db.execute(query, (name, email, password, role))
        print("User registered successfully!")

    def login(self, email, password):
        query = "SELECT user_id, name, email, role FROM users WHERE email = %s AND password = %s"
        result = self.__db.fetch(query, (email, password))

        if result and len(result) > 0:
            return result[0], True  # User found, return user details
        else:
            return None


    def update_profile(self, user_id, new_name, new_email, new_password):
        query = "UPDATE users SET name=%s, email=%s, password=%s WHERE user_id=%s"
        self.__db.execute(query, (new_name, new_email, new_password, user_id))
        print("Profile updated successfully!")
