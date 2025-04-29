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
            return True
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
            print("\nActive Campaigns:\n")
            for campaign in campaigns:
                print(f"Campaign ID: {campaign[0]} \nTitle: {campaign[1]}, \nDescription: {campaign[2]}, \nGoal: {campaign[3]}, Raised: {campaign[4]}\n\n")
        else:
            print("\nNo active campaigns available.")

    def view_my_campaigns(self, user_id):
        """Fetch and display only the campaigns created by this user."""
        query = "SELECT title, description, goal_amount, funds_raised, deadline FROM campaigns WHERE user_id = %s"
        campaigns = self.__db.fetch(query, (user_id,))
        
        if campaigns:
            print("\n📢 Your Campaigns:")
            for campaign in campaigns:
                print(f"Title: {campaign[0]}, \nDescription: {campaign[1]}, \nGoal: ${campaign[2]}, Raised: ${campaign[3]}, Deadline: {campaign[4]}\n")
        else:
            print("\nYou have not created any campaigns.")

    def view_my_campaign_donations(self, user_id):
        """Fetch and display total donations from the funds_raised column for campaigns created by a specific user."""
        query = """
        SELECT campaign_id, title, funds_raised, 
            (SELECT MAX(donation_date) FROM donations WHERE campaign_id = c.campaign_id) AS last_donation_date
        FROM campaigns c
        WHERE user_id = %s;
        """
        result = self.__db.fetch(query, (user_id,))
        
        if result:
            print("\n💰 Your Campaign Donations:")
            for row in result:
                last_donation_date = row[3] if row[3] else "No donations yet"
                print(f"Campaign ID: {row[0]}, Title: {row[1]}, Total Donations: ${row[2]:.2f}, Last Donation Date: {last_donation_date}\n")
        else:
            print("\nNo donations found for your campaigns.")

