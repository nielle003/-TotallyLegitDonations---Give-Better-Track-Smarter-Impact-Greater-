from database import Database

class Event:
    def __init__(self, db):
        self.__db = db

    def create_event(self, name, date, location):
        query = "INSERT INTO events (name, date, location) VALUES (%s, %s, %s)"
        self.__db.execute(query, (name, date, location))
        print("Event created successfully!")

    def register_volunteer(self, event_id, volunteer_id):
        query = "INSERT INTO event_volunteers (event_id, volunteer_id) VALUES (%s, %s)"
        self.__db.execute(query, (event_id, volunteer_id))
        print("Volunteer registered for the event!")