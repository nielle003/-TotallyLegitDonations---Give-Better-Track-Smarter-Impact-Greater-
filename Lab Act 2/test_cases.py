# functional_test_cases.py

from user import User
from campaign import Campaign
from donation import Donation
from database import Database



# def test_user_login():
#     db = Database()
#     user = User(db)
#     result = user.login("johndoe@example.com", "Test@123")
#     assert result != 1, "Login should succeed with correct credentials"

# def test_campaign_creation():
#     db = Database()
#     campaign = Campaign(db)
#     result = campaign.create_campaign("13", "Save the Rainforest", "Help us preserve our rainforests.", 5000, "2025-05-12")
#     assert result is True, "Campaign creation should succeed"

def test_make_donation():
    db = Database()
    donation = Donation(db)
    result = donation.donate_to_campaign("6", "5", 100)
    assert result is True, "Donation should be processed successfully"



def run_all_tests():
    print("\n===== RUNNING FUNCTIONAL TESTS =====")
    #test_user_login()
    #test_campaign_creation()
    test_make_donation()
    print("\n✅ All functional tests executed successfully.")


if __name__ == "__main__":
    run_all_tests()
