from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from rich.panel import Panel
from rich.text import Text
from rich.style import Style
from database import Database
from user import User
from campaign import Campaign
from donation import Donation
from event import Event

# Initialize Rich console
console = Console()

def add_funds(user_id, db):
    """Allows the user to add money to their balance."""
    amount = float(Prompt.ask("\nEnter the amount to add", default="0.0"))
    
    if amount <= 0:
        console.print("Invalid amount. Please enter a positive value.", style="bold red")
        return
    
    # Update user's balance
    update_query = "UPDATE users SET balance = balance + %s WHERE user_id = %s"
    db.execute(update_query, (amount, user_id))

    console.print(f"Successfully added [bold green]${amount:.2f}[/bold green] to your balance!")

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
        console.print("Insufficient balance! Please add funds.", style="bold red")
        return False

def donor_dashboard(donation, campaign, event, user_id, db):
    while True:
        # Fetch and display current balance
        current_balance = get_user_balance(user_id, db)
        console.print(Panel.fit(f"Donor Dashboard \nYour current balance: [bold green]${current_balance:.2f}[/bold green]", title="Dashboard", style="bold blue"))

        # Display options
        console.print("(1) Browse Campaigns\n(2) Donate to Campaign\n(3) Donate to Event\n(4) View Donation History\n(5) View Events\n(6) Add Funds\n(7) Log out", style="bold")
        choice = Prompt.ask("Choose an option", choices=["1", "2", "3", "4", "5", "6", "7"], show_choices=False)
        
        if choice == "1":
            campaign.view_active_campaigns()
        elif choice == "2":
            campaign_id = Prompt.ask("Enter campaign ID to donate")
            amount = float(Prompt.ask("Enter donation amount", default="0.0"))

            if process_payment(user_id, amount, db):
                donation.donate_to_campaign(user_id, campaign_id, amount)
            else:
                console.print("Donation failed due to insufficient balance.", style="bold red")
        
        elif choice == "3":
            event_id = Prompt.ask("Enter event ID to donate")
            amount = float(Prompt.ask("Enter donation amount", default="0.0"))

            if process_payment(user_id, amount, db):
                donation.donate_to_event(user_id, event_id, amount)
            else:
                console.print("Donation failed due to insufficient balance.", style="bold red")

        elif choice == "4":
            donation.view_donation_history(user_id)
        elif choice == "5":
            event.view_active_events()
        elif choice == "6":
            add_funds(user_id, db)
        elif choice == "7":
            console.print("Logging out...", style="bold yellow")
            break
        else:
            console.print("Invalid choice. Try again.", style="bold red")

def organization_dashboard(campaign, user_id):
    while True:
        console.print(Panel.fit("Organization Dashboard", title="Dashboard", style="bold blue"))
        # Display options
        console.print("(1) Create Campaign\n(2) View Active Campaigns\n(3) View Donations\n(4) Log out", style="bold")
        choice = Prompt.ask("Choose an option", choices=["1", "2", "3", "4"], show_choices=False)
        
        if choice == "1":
            title = Prompt.ask("Enter campaign title")
            description = Prompt.ask("Enter campaign description")
            goal_amount = float(Prompt.ask("Enter goal amount", default="0.0"))
            deadline = Prompt.ask("Enter deadline (YYYY-MM-DD)")
            campaign.create_campaign(user_id, title, description, goal_amount, deadline)
        elif choice == "2":
            campaign.view_active_campaigns()
        elif choice == "3":
            campaign.view_campaign_donations(user_id)
        elif choice == "4":
            console.print("Logging out...", style="bold yellow")
            break
        else:
            console.print("Invalid choice. Try again.", style="bold red")

def main():
    db = Database()
    user = User(db)
    campaign = Campaign(db)
    donation = Donation(db)
    event = Event(db)

    while True:
        console.print(Panel.fit("Welcome to the Nonprofit Donation System!", title="Main Menu", style="bold blue"))
        # Display options
        console.print("(1) Register\n(2) Login\n(3) Exit", style="bold")
        choice = Prompt.ask("Choose an option", choices=["1", "2", "3"], show_choices=False)
        
        if choice == "1":
            name = Prompt.ask("Enter your name")
            email = Prompt.ask("Enter your email")
            password = Prompt.ask("Enter your password", password=True)
            role = Prompt.ask("Enter your role", choices=["donor", "organization"])
            user.register(name, email, password, role)
            logged_in_user = user.login(email, password)
        elif choice == "2":
            email = Prompt.ask("Enter your email")
            password = Prompt.ask("Enter your password", password=True)
            logged_in_user = user.login(email, password)
        elif choice == "3":
            console.print("Exiting system. Goodbye!", style="bold yellow")
            break
        else:
            console.print("Invalid option. Please try again.", style="bold red")
            continue
        
        if logged_in_user:
            user_id, *_, role = logged_in_user
            if role == "donor":
                donor_dashboard(donation, campaign, event, user_id, db)
            elif role == "organization":
                organization_dashboard(campaign, user_id)
            else:
                console.print("Login failed. Please try again.", style="bold red")
                continue
    
    db.close()

if __name__ == "__main__":
    main()