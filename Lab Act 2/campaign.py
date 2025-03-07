from database import Database

class Campaign:
    def __init__(self, db):
        self.__db = db

    def create_campaign(self, org_id, title, description, goal_amount, deadline):
        query = """
        INSERT INTO campaigns (org_id, title, description, goal_amount, deadline)
        VALUES (%s, %s, %s, %s, %s)
        """
        self.__db.execute(query, (org_id, title, description, goal_amount, deadline))
        print("Campaign created successfully!")

    def list_campaigns(self):
        query = "SELECT * FROM campaigns"
        campaigns = self.__db.fetch(query)
        for campaign in campaigns:
            print(f"{campaign[0]}: {campaign[2]} (Goal: ${campaign[4]})")