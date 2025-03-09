import re
from database import Database
from user import User
from campaign import Campaign
from donation import Donation
from event import Event

def get_valid_email():
    while True:
        email = input("Enter your email: ")
        if re.match(r"^[\w.-]+@[a-zA-Z\d.-]+\.[a-zA-Z]{2,}$", email):
            return email
        print("Invalid email format. Please try again.")

def get_valid_password():
    while True:
        password = input("Enter your password (at least 6 characters): ")
        if len(password) >= 6:
            return password
        print("Password must be at least 6 characters long.")

def get_valid_role():
    while True:
        role = input("Enter your role (donor/organization): ").lower()
        if role in ["donor", "organization"]:
            return role
        print("Invalid role. Please enter 'donor' or 'organization'.")

def get_positive_integer(prompt):
    while True:
        try:
            value = int(input(prompt))
            if value > 0:
                return value
            print("Value must be a positive integer.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def main():
    db = Database()
    user = User(db)
    campaign = Campaign(db)
    donation = Donation(db)
    event = Event(db)

    while True:
        print("\nWelcome to the Nonprofit Donation System!")
        choice = input("Do you want to (1) Register, (2) Login, or (3) Exit? ")
        
        if choice == "1":
            name = input("Enter your name: ").strip()
            email = get_valid_email()
            password = get_valid_password()
            role = get_valid_role()
            user.register(name, email, password, role)
            logged_in_user = user.login(email, password)
        elif choice == "2":
            email = get_valid_email()
            password = get_valid_password()
            logged_in_user = user.login(email, password)
        elif choice == "3":
            print("Exiting system. Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")
            continue
        
        while logged_in_user:
            action = input("Do you want to (1) Log out or (2) Continue using the system? ")
            if action == "1":
                print("You have been logged out.")
                logged_in_user = None
                break
            elif action == "2":
                if logged_in_user[4] == "organization":
                    campaign.create_campaign(logged_in_user[0], "Food for All", "Helping communities fight hunger", 10000, "2025-12-31")
                campaign.list_campaigns()
                if logged_in_user[4] == "donor":
                    campaign_id = get_positive_integer("Enter campaign ID to donate to: ")
                    amount = get_positive_integer("Enter donation amount: ")
                    donation.make_donation(logged_in_user[0], campaign_id, amount)
                event_name = input("Enter event name: ")
                event_date = input("Enter event date (YYYY-MM-DD): ")
                event_location = input("Enter event location: ")
                event.create_event(event_name, event_date, event_location)
                event_id = get_positive_integer("Enter event ID to register for: ")
                event.register_volunteer(event_id, logged_in_user[0])
            else:
                print("Invalid option. Please try again.")
    
    db.close()

if __name__ == "__main__":
    main()
