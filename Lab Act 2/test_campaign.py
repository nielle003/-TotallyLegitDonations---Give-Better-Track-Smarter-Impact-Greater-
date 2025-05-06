import unittest
from unittest.mock import MagicMock
import io
import sys
from contextlib import redirect_stdout

# Import the Campaign class
from campaign import Campaign

class MockDatabase:
    """Mock Database class to simulate database interactions without actual DB connections"""
    
    def __init__(self, mock_data=None):
        self.executed_queries = []
        self.executed_params = []
        self.mock_data = mock_data or []
        self.last_insert_id = 0
    
    def execute(self, query, params=None):
        self.executed_queries.append(query)
        self.executed_params.append(params)
        self.last_insert_id += 1
        return self.last_insert_id
    
    def fetch(self, query, params=None):
        self.executed_queries.append(query)
        self.executed_params.append(params)
        return self.mock_data

class TestCampaign(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method"""
        self.mock_db = MockDatabase()
        self.campaign = Campaign(self.mock_db)
        # Capture stdout for testing print statements
        self.captured_output = io.StringIO()
        
    def capture_output(self, func, *args, **kwargs):
        """Helper method to capture and return stdout from a function call"""
        with redirect_stdout(self.captured_output):
            result = func(*args, **kwargs)
        output = self.captured_output.getvalue()
        self.captured_output = io.StringIO()  # Reset for next capture
        return output, result
    
    def test_create_campaign_success(self):
        """Test successful campaign creation"""
        print("\n🧪 TEST: Create Campaign - Success Case")
        
        # Test data
        user_id = 1
        title = "Test Campaign"
        description = "This is a test campaign"
        goal_amount = 1000
        deadline = "2023-12-31"
        
        # Expected values
        expected_result = True
        expected_output = "✅ Campaign created successfully!"
        
        # Execute the method and capture output
        output, result = self.capture_output(
            self.campaign.create_campaign, 
            user_id, title, description, goal_amount, deadline
        )
        
        # Assertions
        is_success = result == expected_result and expected_output in output
        
        # Display results
        print(f"Expected result: {expected_result}")
        print(f"Actual result: {result}")
        print(f"Expected output: '{expected_output}'")
        print(f"Actual output: '{output.strip()}'")
        print(f"Test result: {'✅ PASS' if is_success else '❌ FAIL'}")
        
        # Unittest assertion
        self.assertTrue(is_success)
        
    def test_create_campaign_failure(self):
        """Test campaign creation failure"""
        print("\n🧪 TEST: Create Campaign - Failure Case")
        
        # Create a mock DB that raises an exception
        mock_db_fail = MockDatabase()
        mock_db_fail.execute = MagicMock(side_effect=Exception("Database error"))
        campaign = Campaign(mock_db_fail)
        
        # Test data
        user_id = 1
        title = "Test Campaign"
        description = "This is a test campaign"
        goal_amount = 1000
        deadline = "2023-12-31"
        
        # Expected values
        expected_result = None
        expected_output_part = "❌ ERROR: Campaign creation failed!"
        
        # Execute the method and capture output
        output, result = self.capture_output(
            campaign.create_campaign, 
            user_id, title, description, goal_amount, deadline
        )
        
        # Assertions
        is_success = result == expected_result and expected_output_part in output
        
        # Display results
        print(f"Expected result: {expected_result}")
        print(f"Actual result: {result}")
        print(f"Expected output contains: '{expected_output_part}'")
        print(f"Actual output: '{output.strip()}'")
        print(f"Test result: {'✅ PASS' if is_success else '❌ FAIL'}")
        
        # Unittest assertion
        self.assertTrue(expected_output_part in output)
        
    def test_list_campaigns(self):
        """Test listing all campaigns"""
        print("\n🧪 TEST: List All Campaigns")
        
        # Mock data for campaigns
        mock_campaigns = [
            (1, 1, "Campaign 1", "Description 1", 1000, 0, "2023-12-31", "active"),
            (2, 2, "Campaign 2", "Description 2", 2000, 500, "2023-12-31", "active")
        ]
        
        # Set up mock database with test data
        mock_db = MockDatabase(mock_campaigns)
        campaign = Campaign(mock_db)
        
        # Expected output
        expected_output_parts = ["1: Campaign 1 (Goal: $1000)", "2: Campaign 2 (Goal: $2000)"]
        
        # Execute the method and capture output
        output, _ = self.capture_output(campaign.list_campaigns)
        
        # Check if all expected parts are in the output
        all_parts_present = all(part in output for part in expected_output_parts)
        
        # Display results
        print(f"Expected output to contain: {expected_output_parts}")
        print(f"Actual output: '{output.strip()}'")
        print(f"Test result: {'✅ PASS' if all_parts_present else '❌ FAIL'}")
        
        # Unittest assertion
        self.assertTrue(all_parts_present)
        
    def test_view_active_campaigns_with_data(self):
        """Test viewing active campaigns when data exists"""
        print("\n🧪 TEST: View Active Campaigns - With Data")
        
        # Mock data for active campaigns
        mock_campaigns = [
            (1, "Campaign 1", "Description 1", 1000, 200, "2023-12-31", "active"),
            (2, "Campaign 2", "Description 2", 2000, 500, "2023-12-31", "active")
        ]
        
        # Set up mock database with test data
        mock_db = MockDatabase(mock_campaigns)
        campaign = Campaign(mock_db)
        
        # Expected output parts
        expected_output_parts = [
            "Active Campaigns:",
            "Campaign ID: 1",
            "Title: Campaign 1",
            "Campaign ID: 2",
            "Title: Campaign 2"
        ]
        
        # Execute the method and capture output
        output, _ = self.capture_output(campaign.view_active_campaigns)
        
        # Check if all expected parts are in the output
        all_parts_present = all(part in output for part in expected_output_parts)
        
        # Display results
        print(f"Expected output to contain: {expected_output_parts}")
        print(f"Actual output: '{output.strip()}'")
        print(f"Test result: {'✅ PASS' if all_parts_present else '❌ FAIL'}")
        
        # Unittest assertion
        self.assertTrue(all_parts_present)
        
    def test_view_active_campaigns_no_data(self):
        """Test viewing active campaigns when no data exists"""
        print("\n🧪 TEST: View Active Campaigns - No Data")
        
        # Set up mock database with no data
        mock_db = MockDatabase([])
        campaign = Campaign(mock_db)
        
        # Expected output
        expected_output = "No active campaigns available."
        
        # Execute the method and capture output
        output, _ = self.capture_output(campaign.view_active_campaigns)
        
        # Check if expected output is in the actual output
        is_success = expected_output in output
        
        # Display results
        print(f"Expected output: '{expected_output}'")
        print(f"Actual output: '{output.strip()}'")
        print(f"Test result: {'✅ PASS' if is_success else '❌ FAIL'}")
        
        # Unittest assertion
        self.assertTrue(is_success)

def run_tests():
    """Run all tests with custom output formatting"""
    print("\n" + "="*80)
    print("🧪 CAMPAIGN CLASS TEST SUITE 🧪".center(80))
    print("="*80)
    
    # Create a test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCampaign)
    
    # Run the tests
    result = unittest.TextTestRunner(verbosity=0).run(suite)
    
    # Print summary
    print("\n" + "="*80)
    print("📊 TEST SUMMARY 📊".center(80))
    print("="*80)
    print(f"Total tests: {result.testsRun}")
    print(f"Passed: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failed: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.wasSuccessful():
        print("\n✅ ALL TESTS PASSED ✅")
    else:
        print("\n❌ SOME TESTS FAILED ❌")
    
    print("="*80)

if __name__ == "__main__":
    run_tests()