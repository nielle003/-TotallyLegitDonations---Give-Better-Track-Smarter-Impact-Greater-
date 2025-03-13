from database import Database

class Event:
    def __init__(self, db):
        self.__db = db

    def create_event(self, name, date, location, description, status="active"):
        """Creates a new event and stores it in the database."""
        query = "INSERT INTO events (name, date, location, description, status) VALUES (%s, %s, %s, %s, %s)"
        self.__db.execute(query, (name, date, location, description, status))
        print("Event created successfully!")

    def view_active_events(self):
        """Fetch and display all active events."""
        query = "SELECT event_id, name, description, date FROM events WHERE status = 'active'"
        events = self.__db.fetch(query)

        if events:
            print("\nActive Events:")
            for event in events:
                print(f"ID: {event[0]}, Name: {event[1]}, Description: {event[2]}, Date: {event[3]}")
        else:
            print("\nNo active events found.")
