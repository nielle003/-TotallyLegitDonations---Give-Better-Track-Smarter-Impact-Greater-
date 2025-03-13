from database import Database

class Campaign:
    def __init__(self, db):
        self.__db = db

    def create_campaign(self, user_id, title, description, goal_amount, deadline):
        query = """
        INSERT INTO campaigns (user_id, title, description, goal_amount, deadline, status, funds_raised)
        VALUES (%s, %s, %s, %s, %s, 'active', 0)
        """
        try:
            self.__db.execute(query, (user_id, title, description, goal_amount, deadline))
            print("✅ Campaign created successfully!")
        except Exception as e:
            print(f"❌ ERROR: Campaign creation failed! {e}")

    def list_campaigns(self):
        query = "SELECT * FROM campaigns"
        campaigns = self.__db.fetch(query)
        for campaign in campaigns:
            print(f"{campaign[0]}: {campaign[2]} (Goal: ${campaign[4]})")

    def view_active_campaigns(self):
        query = "SELECT * FROM campaigns WHERE status = 'active'"
        campaigns = self.__db.fetch(query)
        if campaigns:
            print("\nActive Campaigns:")
            for campaign in campaigns:
                print(f"Title: {campaign[1]}, \nDescription: {campaign[2]}, \nGoal: {campaign[3]}, Raised: {campaign[4]}")
        else:
            print("\nNo active campaigns available.")

    def view_campaign_donations(self, user_id):
        """Fetch and display donations for campaigns created by a specific user."""
        query = """
        SELECT c.campaign_id, c.title, COALESCE(SUM(d.amount), 0) AS total_donations, MAX(d.donation_date) AS last_donation_date
        FROM campaigns c
        LEFT JOIN donations d ON c.campaign_id = d.campaign_id
        WHERE c.user_id = %s
        GROUP BY c.campaign_id, c.title;
        """
        result = self.__db.fetch(query, (user_id,))
        
        if result:
            print("\nYour Campaign Donations:")
            for row in result:
                last_donation_date = row[3] if row[3] else "No donations yet"
                print(f"Campaign ID: {row[0]}, Title: {row[1]}, Total Donations: ${row[2]:.2f}, Last Donation Date: {last_donation_date}")
        else:
            print("\nNo donations found for your campaigns.")
