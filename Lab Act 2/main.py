from database import Database
from user import User
from campaign import Campaign
from donation import Donation
from event import Event


def add_funds(user_id, db):
    """Allows the user to add money to their balance."""
    amount = float(input("\nEnter the amount to add: $"))
    
    if amount <= 0:
        print("Invalid amount. Please enter a positive value.")
        return
    
    # Update user's balance
    update_query = "UPDATE users SET balance = balance + %s WHERE user_id = %s"
    db.execute(update_query, (amount, user_id))

    print(f"Successfully added ${amount:.2f} to your balance!")

def get_user_balance(user_id, db):
    """Fetches the user's current balance."""
    query = "SELECT balance FROM users WHERE user_id = %s"
    result = db.fetch(query, (user_id,))
    return result[0][0] if result else 0

def process_payment(user_id, amount, db):
    """Checks if the user has enough balance and deducts the amount if valid."""
    current_balance = get_user_balance(user_id, db)
    
    if current_balance >= amount:
        # Deduct amount from balance
        update_query = "UPDATE users SET balance = balance - %s WHERE user_id = %s"
        db.execute(update_query, (amount, user_id))
        return True
    else:
        print("Insufficient balance! Please add funds.")
        return False

def donor_dashboard(donation, campaign, event, user_id, db):
    while True:
        # Fetch and display current balance
        current_balance = get_user_balance(user_id, db)
        print(f"\nDonor Dashboard \n Your current balance: ${current_balance:.2f}")

        choice = input("(1) Browse Campaigns, \n(2) Donate to Campaign, \n(3) Donate to Event, \n(4) View Donation History, \n(5) View Events, \n(6) Add Funds, \n(7) Log out: ")
        
        if choice == "1":
            campaign.view_active_campaigns()
        elif choice == "2":
            campaign_id = input("Enter campaign ID to donate: ")
            amount = float(input("Enter donation amount: "))

            if process_payment(user_id, amount, db):
                donation.donate_to_campaign(user_id, campaign_id, amount)
            else:
                print("Donation failed due to insufficient balance.")
        
        elif choice == "3":
            event_id = input("Enter event ID to donate: ")
            amount = float(input("Enter donation amount: "))

            if process_payment(user_id, amount, db):
                donation.donate_to_event(user_id, event_id, amount)
            else:
                print("Donation failed due to insufficient balance.")

        elif choice == "4":
            donation.view_donation_history(user_id)
        elif choice == "5":
            event.view_active_events()
        elif choice == "6":
            add_funds(user_id, db)
        elif choice == "7":
            print("Logging out...")
            break
        else:
            print("Invalid choice. Try again.")


def organization_dashboard(campaign, user_id):
    while True:
        print("\nOrganization Dashboard")
        choice = input("(1) Create Campaign, (2) View Active Campaigns, (3) View Donations, (4) Log out: ")
        
        if choice == "1":
            title = input("Enter campaign title: ")
            description = input("Enter campaign description: ")
            goal_amount = float(input("Enter goal amount: "))
            deadline = input("Enter deadline (YYYY-MM-DD): ")
            campaign.create_campaign(user_id, title, description, goal_amount, deadline)
        elif choice == "2":
            campaign.view_active_campaigns()
        elif choice == "3":
            campaign.view_campaign_donations(user_id)
        elif choice == "4":
            print("Logging out...")
            break
        else:
            print("Invalid choice. Try again.")

def main():
    db = Database()
    user = User(db)
    campaign = Campaign(db)
    donation = Donation(db)
    event = Event(db)

    while True:
        print("\nWelcome to the Nonprofit Donation System!")
        choice = input("Do you want to (1) Register, (2) Login, or (3) Exit?:  ")
        
        if choice == "1":
            name = input("Enter your name: ")
            email = input("Enter your email: ")
            password = input("Enter your password: ")
            role = input("Enter your role (donor or organization): ")
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
        
        if logged_in_user:
            user_id, *_, role = logged_in_user
            if role == "donor":
                donor_dashboard(donation, campaign, event, user_id, db)
            elif role == "organization":
                organization_dashboard(campaign, user_id)
            else:
                print("Login failed. Please try again.")
                continue
    
    db.close()

if __name__ == "__main__":
    main()
