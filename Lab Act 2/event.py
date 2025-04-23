from database import Database

class Event:
    def __init__(self, db):
        self.__db = db

    def create_event(self, organization_id, title, description, event_date, location):
        """Allows an organization to create an event."""
        try:
            query = """
            INSERT INTO events (user_id, name, description, date, location)
            VALUES (%s, %s, %s, %s, %s)
            """
            self.__db.execute(query, (organization_id, title, description, event_date, location))
            print("✅ Event created successfully!")
        except Exception as e:
            print(f"❌ ERROR: Event creation failed! {e}")

    def view_active_events(self):
        """Fetch and display all active events."""
        query = "SELECT event_id, name, description, date, location FROM events WHERE status = 'active'"
        events = self.__db.fetch(query)

        if events:
            print("\n📌 Active Events:")
            for event in events:
                print(f"📅 Event ID: {event[0]} \n{event[1]}  \n{event[2]} \non {event[3]} \nat {event[4]}\n")
        else:
            print("ℹ️ No active events found.")

    def volunteer_for_event(self, user_id, event_id):
        """Allows a user to volunteer for an event."""
        try:
            # Retrieve user's name from the users table
            user_query = "SELECT name FROM users WHERE user_id = %s"
            user_result = self.__db.fetch(user_query, (user_id,))
            
            if not user_result:
                print("❌ ERROR: User not found!")
                return
            
            user_name = user_result[0][0]

            # Check if the event exists
            event_query = "SELECT event_id FROM events WHERE event_id = %s"
            event_result = self.__db.fetch(event_query, (event_id,))
            
            if not event_result:
                print("❌ ERROR: Event does not exist!")
                return
            
            # Insert volunteer record
            query = "INSERT INTO event_volunteers (user_id, event_id, name, volunteer_date) VALUES (%s, %s, %s, NOW())"
            self.__db.execute(query, (user_id, event_id, user_name))
            
            print(f"✅ {user_name}, you have successfully volunteered for the event!")
        except Exception as e:
            print(f"❌ ERROR: Volunteering failed! {e}")

    def view_volunteer_history(self, user_id):
        """Fetches and displays the events a user has volunteered for."""
        query = """
        SELECT e.event_id, e.name, e.date, e.location, v.name FROM events e
        JOIN event_volunteers v ON e.event_id = v.event_id
        WHERE v.user_id = %s
        ORDER BY e.date DESC
        """
        events = self.__db.fetch(query, (user_id,))
        
        if events:
            print("\n📜 Your Volunteer History:")
            for event in events:
                print(f"📌 Event {event[0]}: {event[1]} on {event[2]} at {event[3]}\n")
        else:
            print("ℹ️ No volunteered events found.")

    def view_volunteers_for_event(self, event_id):
        """Fetches and displays all volunteers for a specific event."""
        query = """
        SELECT v.name, v.volunteer_date FROM event_volunteers v
        WHERE v.event_id = %s
        ORDER BY v.volunteer_date DESC
        """
        volunteers = self.__db.fetch(query, (event_id,))
        
        if volunteers:
            print(f"\n📋 Volunteers for Event {event_id}:")
            for volunteer in volunteers:
                print(f"👤 {volunteer[0]} - Joined on {volunteer[1]}\n")
        else:
            print("ℹ️ No volunteers for this event yet.")

    def opt_out_of_event(self, user_id, event_id):
        """Allows a user to opt out of an event they previously volunteered for."""
        try:
            # Check if the user has volunteered for the event
            check_query = "SELECT * FROM event_volunteers WHERE user_id = %s AND event_id = %s"
            volunteer_result = self.__db.fetch(check_query, (user_id, event_id))

            if not volunteer_result:
                print("❌ ERROR: You are not registered as a volunteer for this event!")
                return
            
            # Remove volunteer record
            delete_query = "DELETE FROM event_volunteers WHERE user_id = %s AND event_id = %s"
            self.__db.execute(delete_query, (user_id, event_id))
            
            print("✅ You have successfully opted out of the event.")
        except Exception as e:
            print(f"❌ ERROR: Opting out failed! {e}")

    
    def view_my_events(self, user_id):
        """Fetch and display events created by the logged-in organization along with their volunteers."""
        query = """
        SELECT e.event_id, e.name, e.description, e.date, e.location, 
            GROUP_CONCAT(u.name SEPARATOR ', ') AS volunteers
        FROM events e
        LEFT JOIN event_volunteers ev ON e.event_id = ev.event_id
        LEFT JOIN users u ON ev.user_id = u.user_id
        WHERE e.user_id = %s
        GROUP BY e.event_id, e.name, e.description, e.date, e.location
        """

        events = self.__db.fetch(query, (user_id,))

        if events:
            print("\n📅 Your Created Events with Volunteers:")
            for event in events:
                volunteers = event[5] if event[5] else "No volunteers yet"
                print(f"🔹 Event ID: {event[0]}\n   Title: {event[1]}\n   Description: {event[2]}\n   Date: {event[3]}\n   Location: {event[4]}\n   Volunteers: {volunteers}\n")
        else:
            print("\n⚠️ No events found for your organization.")


