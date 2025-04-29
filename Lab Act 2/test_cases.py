# functional_test_cases.py

from user import User
from campaign import Campaign
from donation import Donation
from database import Database

class TestCase:
    def __init__(self, id, title, description, test_data, preconditions, steps, expected, actual, status, remarks, tested_by, date_tested):
        self.id = id
        self.title = title
        self.description = description
        self.test_data = test_data
        self.preconditions = preconditions
        self.steps = steps
        self.expected = expected
        self.actual = actual
        self.status = status
        self.remarks = remarks
        self.tested_by = tested_by
        self.date_tested = date_tested

    def display(self):
        print(f"\nTest Case ID: {self.id}")
        print(f"Title: {self.title}")
        print(f"Description: {self.description}")
        print(f"Test Data: {self.test_data}")
        print(f"Preconditions: {self.preconditions}")
        print(f"Steps: {self.steps}")
        print(f"Expected Result: {self.expected}")
        print(f"Actual Result: {self.actual}")
        print(f"Status: {self.status}")
        print(f"Remarks: {self.remarks}")
        print(f"Tested by: {self.tested_by}")
        print(f"Date Tested: {self.date_tested}")


def test_user_login():
    db = Database()
    user = User(db)
    result = user.login("johndoe@example.com", "Test@123")
    assert result != 1, "Login should succeed with correct credentials"

def test_campaign_creation():
    db = Database()
    campaign = Campaign(db)
    result = campaign.create("Save the Rainforest", 5000, "Help us preserve our rainforests.", "org_id")
    assert result is True, "Campaign creation should succeed"

def test_make_donation():
    db = Database()
    donation = Donation(db)
    result = donation.make_donation("user_id", "campaign_id", 100)
    assert result is True, "Donation should be processed successfully"

test_cases = [
    TestCase(
        "TC001",
        "Campaign Creation by Organization",
        "Check if organizations can create fundraising campaigns.",
        {"Title": "Save the Rainforest", "Target Amount": 5000, "Description": "Help us preserve our rainforests."},
        "Organization must be logged in.",
        ["Login as organization.", "Go to Create Campaign.", "Fill form and submit."],
        "New campaign is listed under active campaigns. Confirmation message is shown.",
        "Campaign displayed and confirmation shown.",
        "Passed",
        "Campaign creation works as intended.",
        "Nielle Barcelona",
        "2025-APR-23"
    ),
    TestCase(
        "TC002",
        "Making a Donation to a Campaign",
        "Validate that users can donate to active campaigns.",
        {"Donation Amount": 100},
        "User must be logged in; Campaign must exist.",
        ["Login as user.", "Select a campaign.", "Click Donate and confirm."],
        "Donation is processed and recorded.",
        "Donation recorded successfully.",
        "Passed",
        "Donation flow behaves correctly.",
        "Nielle Barcelona",
        "2025-APR-23"
    ),
    TestCase(
        "TC003",
        "Viewing Donation History",
        "Ensure users can view their past donations.",
        {"Existing Record": True},
        "User must have made at least one donation.",
        ["Login as user.", "Go to Donation History."],
        "List of previous donations is displayed correctly.",
        "Donation history shown correctly.",
        "Passed",
        "Displays accurate user donation records.",
        "Aldrich Ryan Antony",
        "2025-APR-23"
    ),
    TestCase(
        "TC004",
        "Display Total Donations for a Campaign",
        "Verify that total donations are calculated and shown.",
        {"Campaign with donations": True},
        "Campaign must have at least one donation.",
        ["Open campaign page.", "Check total amount."],
        "The total reflects correct donation sum.",
        "Total updated and displayed correctly.",
        "Passed",
        "Correctly aggregates and shows donations.",
        "Aldrich Ryan Antony",
        "2025-APR-23"
    ),
    TestCase(
        "TC005",
        "User Registration Functionality",
        "Validate new user registration.",
        {"Name": "John Doe", "Email": "johndoe@example.com", "Password": "Test@123"},
        "User must have valid email and connection.",
        ["Navigate to registration.", "Enter info.", "Click Register."],
        "Success message and DB insert.",
        "Registration successful, user added.",
        "Passed",
        "Registration checks and stores new user.",
        "Mark Kevin Ramos",
        "2025-APR-23"
    ),
    TestCase(
        "TC006",
        "User Login Functionality",
        "Ensure registered users can login.",
        {"Email": "johndoe@example.com", "Password": "Test@123"},
        "User must be registered.",
        ["Go to login.", "Enter credentials.", "Click Login."],
        "User redirected to dashboard.",
        "User logged in and redirected correctly.",
        "Passed",
        "Login confirms account and redirects.",
        "Mark Kevin Ramos",
        "2025-APR-23"
    ),
]


def run_all_tests():
    print("\n===== DISPLAYING TEST CASES =====")
    for case in test_cases:
        case.display()

    print("\n===== RUNNING FUNCTIONAL TESTS =====")
    test_user_login()
    test_campaign_creation()
    test_make_donation()
    print("\n✅ All functional tests executed successfully.")


if __name__ == "__main__":
    run_all_tests()
