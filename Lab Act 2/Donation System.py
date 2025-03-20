import mysql.connector

# Database Connection
class Database:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="admin",
            database="nonprofit_donation_db"
        )
        self.cursor = self.conn.cursor()

    def execute(self, query, params=None):
        self.cursor.execute(query, params or ())
        self.conn.commit()

    def fetch(self, query, params=None):
        self.cursor.execute(query, params or ())
        return self.cursor.fetchall()

    def close(self):
        self.cursor.close()
        self.conn.close()

# User Management
class User:
    def __init__(self, db):
        self.db = db

    def register(self, name, email, password, role):
        query = "INSERT INTO users (name, email, password, role) VALUES (%s, %s, %s, %s)"
        self.db.execute(query, (name, email, password, role))
        print("User registered successfully!")

    def login(self, email, password):
        query = "SELECT * FROM users WHERE email=%s AND password=%s"
        user = self.db.fetch(query, (email, password))
        if user:
            print(f"Welcome, {user[0][1]}! You are logged in as {user[0][4]}.")
            return user[0]
        else:
            print("Invalid email or password.")
            return None

# Campaign Management
class Campaign:
    def __init__(self, db):
        self.db = db

    def create_campaign(self, org_id, title, description, goal_amount, deadline):
        query = """
        INSERT INTO campaigns (org_id, title, description, goal_amount, deadline)
        VALUES (%s, %s, %s, %s, %s)
        """
        self.db.execute(query, (org_id, title, description, goal_amount, deadline))
        print("Campaign created successfully!")

    def list_campaigns(self):
        query = "SELECT * FROM campaigns"
        campaigns = self.db.fetch(query)
        for campaign in campaigns:
            print(f"{campaign[0]}: {campaign[2]} (Goal: ${campaign[4]})")

# Donation Management
class Donation:
    def __init__(self, db):
        self.db = db

    def make_donation(self, donor_id, campaign_id, amount):
        query = "INSERT INTO donations (donor_id, campaign_id, amount) VALUES (%s, %s, %s)"
        self.db.execute(query, (donor_id, campaign_id, amount))
        print("Thank you for your donation!")

# Event Management
class Event:
    def __init__(self, db):
        self.db = db

    def create_event(self, name, date, location):
        query = "INSERT INTO events (name, date, location) VALUES (%s, %s, %s)"
        self.db.execute(query, (name, date, location))
        print("Event created successfully!")

    def register_volunteer(self, event_id, volunteer_id):
        query = "INSERT INTO event_volunteers (event_id, volunteer_id) VALUES (%s, %s)"
        self.db.execute(query, (event_id, volunteer_id))
        print("Volunteer registered for the event!")

# Main Program
if __name__ == "__main__":
    db = Database()
    user = User(db)
    campaign = Campaign(db)
    donation = Donation(db)
    event = Event(db)

    # Example Workflow
    user.register("Alice", "alice@example.com", "securepass123", "donor")
    logged_in_user = user.login("alice@example.com", "securepass123")

    if logged_in_user and logged_in_user[4] == "organization":
        campaign.create_campaign(logged_in_user[0], "Food for All", "Helping communities fight hunger", 10000, "2025-12-31")

    campaign.list_campaigns()

    if logged_in_user and logged_in_user[4] == "donor":
        donation.make_donation(logged_in_user[0], 1, 200)

    event.create_event("Tree Planting", "2025-03-15", "City Park")
    event.register_volunteer(1, logged_in_user[0])

    db.close()