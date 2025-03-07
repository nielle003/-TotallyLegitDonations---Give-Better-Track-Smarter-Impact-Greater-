from database import Database

class Donation:
    def __init__(self, db):
        self.__db = db

    def make_donation(self, donor_id, campaign_id, amount):
        query = "INSERT INTO donations (donor_id, campaign_id, amount) VALUES (%s, %s, %s)"
        self.__db.execute(query, (donor_id, campaign_id, amount))
        print("Thank you for your donation!")