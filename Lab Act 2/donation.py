from database import Database

class Donation:
    def __init__(self, db):
        self.__db = db

    def donate_to_campaign(self, user_id, campaign_id, amount):
        """Allows a user to donate, ensuring the campaign exists."""
        try:
            # Check if the campaign exists
            campaign_query = "SELECT campaign_id FROM campaigns WHERE campaign_id = %s"
            campaign_result = self.__db.fetch(campaign_query, (campaign_id,))
            
            if not campaign_result:
                print("❌ ERROR: Campaign does not exist!")
                return
            
            # Insert the donation using user_id
            query = "INSERT INTO donations (user_id, campaign_id, amount, donation_date) VALUES (%s, %s, %s, NOW())"
            self.__db.execute(query, (user_id, campaign_id, amount))
            print("✅ Thank you for your donation!")
        
        except Exception as e:
            print(f"❌ ERROR: Donation failed! {e}")

    def view_donation_history(self, user_id):
        """Fetches and displays the donation history of a user."""
        query = "SELECT campaign_id, amount, donation_date FROM donations WHERE user_id = %s ORDER BY donation_date DESC"
        donations = self.__db.fetch(query, (user_id,))
        
        if donations:
            print("\n📜 Your Donation History:")
            for donation in donations:
                print(f"📌 Campaign {donation[0]}: Donated ${donation[1]:.2f} on {donation[2]}")
        else:
            print("ℹ️ No donations found.")
