import re
from datetime import datetime
from database import Database
from user import User
from campaign import Campaign
from donation import Donation
from event import Event

def safe_input(prompt, type_=str, condition=lambda x: True, error_msg="Invalid input. Try again."):
    while True:
        try:
            value = type_(input(prompt))
            if not condition(value):
                raise ValueError()
            return value
        except ValueError:
            print(error_msg)

def validate_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def validate_date(date_str):
    try:
        date = datetime.strptime(date_str, "%Y-%m-%d").date()
        return date >= datetime.today().date()
    except ValueError:
        return False


def add_funds(user_id, db):
    amount = safe_input("\nEnter the amount to add: $", float, lambda x: x > 0,
                        "Please enter a positive number.")
    update_query = "UPDATE users SET balance = balance + %s WHERE user_id = %s"
    db.execute(update_query, (amount, user_id))
    print(f"Successfully added ${amount:.2f} to your balance!")

def get_user_balance(user_id, db):
    query = "SELECT balance FROM users WHERE user_id = %s"
    result = db.fetch(query, (user_id,))
    return result[0][0] if result else 0

def process_payment(user_id, amount, db):
    current_balance = get_user_balance(user_id, db)
    if current_balance >= amount:
        update_query = "UPDATE users SET balance = balance - %s WHERE user_id = %s"
        db.execute(update_query, (amount, user_id))
        return True
    else:
        print("Insufficient balance! Please add funds.")
        return False

def donor_dashboard(donation, campaign, event, user_id, db):
    while True:
        current_balance = get_user_balance(user_id, db)
        print(f"\n📊 Donor Dashboard \n💰 Your current balance: ${current_balance:.2f}")
        print("\n(1) Browse Campaigns \n(2) Donate to Campaign \n(3) View Donation History")
        print("(4) View Events \n(5) Volunteer for an Event \n(6) View Volunteered Events \n(7) Opt Out of Event")
        print("(8) Add Funds \n(9) Log out")

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            campaign.view_active_campaigns()

        elif choice == "2":
            campaign_id = input("Enter campaign ID to donate: ").strip()
            amount = safe_input("Enter donation amount: ", float, lambda x: x > 0,
                                "Please enter a valid positive number.")
            if process_payment(user_id, amount, db):
                donation.donate_to_campaign(user_id, campaign_id, amount)
            else:
                print("❌ Donation failed due to insufficient balance.")

        elif choice == "3":
            donation.view_donation_history(user_id)

        elif choice == "4":
            event.view_active_events(user_id)

        elif choice == "5":
            event_id = input("Enter event ID to volunteer: ").strip()
            event.volunteer_for_event(user_id, event_id)

        elif choice == "6":
            event.view_volunteer_history(user_id)

        elif choice == "7":
            event_id = input("Enter event ID to opt out: ").strip()
            event.opt_out_of_event(user_id, event_id)

        elif choice == "8":
            add_funds(user_id, db)

        elif choice == "9":
            print("🔒 Logging out...")
            break

        else:
            print("❌ Invalid choice. Try again.")     

def organization_dashboard(campaign, event, user_id):
    while True:
        print("\n🏢 Organization Dashboard")
        print("(1) Create Campaign \n(2) View My Campaigns \n(3) View Donations to My Campaigns")
        print("(4) Create Event \n(5) View My Events \n(6) Log out")

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            title = input("Enter campaign title: ").strip()
            description = input("Enter campaign description: ").strip()
            goal_amount = safe_input("Enter goal amount: ", float, lambda x: x > 0,
                                     "Goal amount must be a positive number.")
            deadline = safe_input("Enter deadline (YYYY-MM-DD): ", str, validate_date,
                                  "Please enter a valid date (YYYY-MM-DD) that is today or in the future.")
            campaign.create_campaign(user_id, title, description, goal_amount, deadline)

        elif choice == "2":
            campaign.view_my_campaigns(user_id)

        elif choice == "3":
            campaign.view_my_campaign_donations(user_id)

        elif choice == "4":
            title = input("Enter event title: ").strip()
            description = input("Enter event description: ").strip()
            event_date = safe_input("Enter event date (YYYY-MM-DD): ", str, validate_date,
                                    "Please enter a valid date in YYYY-MM-DD format.")
            location = input("Enter event location: ").strip()
            event.create_event(user_id, title, description, event_date, location)

        elif choice == "5":
            event.view_my_events(user_id)

        elif choice == "6":
            print("🔒 Logging out...")
            break

        else:
            print("❌ Invalid choice. Try again.")

def main():
    db = Database()
    user = User(db)
    campaign = Campaign(db)
    donation = Donation(db)
    event = Event(db)

    while True:
        print("\nWelcome to the Nonprofit Donation System!")
        choice = input("Do you want to (1) Register, (2) Login, or (3) Exit?: ").strip()

        if choice == "1":
            name = input("Enter your name: ").strip()
            email = safe_input("Enter your email: ", str, validate_email, "Please enter a valid email address.")
            password = input("Enter your password: ").strip()

            while True:
                role = input("Enter your role (donor or organization): ").strip().lower()
                if role in ["donor", "organization"]:
                    break
                else:
                    print("❌ Invalid role. Please enter either 'donor' or 'organization'.")

            user.register(name, email, password, role)
            logged_in_user = user.login(email, password)

        elif choice == "2":
            email = safe_input("Enter your email: ", str, validate_email,
                               "Please enter a valid email address.")
            password = input("Enter your password: ").strip()
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
                organization_dashboard(campaign, event, user_id)
            else:
                print("Login failed. Please try again.")
        else:
            print("❌ Login failed. Please check your credentials.")

    db.close()

if __name__ == "__main__":
    main()
