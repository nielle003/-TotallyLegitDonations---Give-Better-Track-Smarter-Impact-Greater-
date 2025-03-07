from database import Database
from user import User
from campaign import Campaign
from donation import Donation
from event import Event

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
            name = input("Enter your name: ")
            email = input("Enter your email: ")
            password = input("Enter your password: ")
            role = input("Enter your role (donor/organization): ")
            user.register(name, email, password, role)
            logged_in_user = user.login(email, password)
        elif choice == "2":
            email = input("Enter your email: ")
            password = input("Enter your password: ")
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
                    donation.make_donation(logged_in_user[0], 1, 200)
                event.create_event("Tree Planting", "2025-03-15", "City Park")
                event.register_volunteer(1, logged_in_user[0])
            else:
                print("Invalid option. Please try again.")
    
    db.close()

if __name__ == "__main__":
    main()