from database import Database

class Donation:
    def __init__(self, db):
        self.__db = db

    def donate_to_campaign(self, user_id, campaign_id, amount):
        try:
            # Validate campaign existence
            check_query = "SELECT COUNT(*) FROM campaigns WHERE campaign_id = %s"
            campaign_exists = self.__db.fetch_one(check_query, (campaign_id,))
            if not campaign_exists or campaign_exists[0] == 0:
                print(f"❌ Campaign ID {campaign_id} does not exist.")
                return

            # Insert donation
            query = """
            INSERT INTO donations (user_id, campaign_id, amount, donation_date)
            VALUES (%s, %s, %s, NOW());
            """
            self.__db.execute(query, (user_id, campaign_id, amount))

            # Update funds_raised
            update_query = """
            UPDATE campaigns 
            SET funds_raised = funds_raised + %s 
            WHERE campaign_id = %s;
            """
            self.__db.execute(update_query, (amount, campaign_id))

            print(f"✅ Successfully donated ${amount:.2f} to campaign ID: {campaign_id}")
        except Exception as e:
            print(f"❌ Donation failed due to an error: {e}")

    def get_total_donations(self, campaign_id):
        """Retrieve the total amount of funds raised for a campaign."""
        try:
            query = "SELECT funds_raised FROM campaigns WHERE campaign_id = %s"
            result = self.__db.fetch_one(query, (campaign_id,))
            if result:
                return result[0]
            else:
                print("⚠️ Campaign not found.")
                return 0.00
        except Exception as e:
            print(f"❌ Could not retrieve total donations: {e}")
            return 0.00

    def view_donation_history(self, user_id):
        """Fetches and displays the donation history of a user."""
        try:
            query = """
            SELECT campaign_id, amount, donation_date 
            FROM donations 
            WHERE user_id = %s 
            ORDER BY donation_date DESC
            """
            donations = self.__db.fetch(query, (user_id,))
            
            if donations:
                print("\n📜 Your Donation History:")
                for donation in donations:
                    print(f"📌 Campaign {donation[0]}: Donated ${donation[1]:.2f} on {donation[2]}\n")
            else:
                print("ℹ️ No donations found.")
        except Exception as e:
            print(f"❌ Error fetching donation history: {e}")
