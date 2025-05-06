import unittest
from unittest.mock import MagicMock
import io
import sys
from contextlib import redirect_stdout

# Import the Event class
from event import Event

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

class TestEvent(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method"""
        self.mock_db = MockDatabase()
        self.event = Event(self.mock_db)
        # Capture stdout for testing print statements
        self.captured_output = io.StringIO()
        
    def capture_output(self, func, *args, **kwargs):
        """Helper method to capture and return stdout from a function call"""
        with redirect_stdout(self.captured_output):
            result = func(*args, **kwargs)
        output = self.captured_output.getvalue()
        self.captured_output = io.StringIO()  # Reset for next capture
        return output, result
    
    def test_create_event_success(self):
        """Test successful event creation"""
        print("\n🧪 TEST: Create Event - Success Case")
        
        # Test data
        organization_id = 1
        title = "Charity Run"
        description = "Annual charity run for cancer research"
        event_date = "2023-12-15"
        location = "Central Park"
        
        # Expected output
        expected_output = "✅ Event created successfully!"
        
        # Execute the method and capture output
        output, _ = self.capture_output(
            self.event.create_event, 
            organization_id, title, description, event_date, location
        )
        
        # Assertions
        is_success = expected_output in output
        
        # Display results
        print(f"Expected output: '{expected_output}'")
        print(f"Actual output: '{output.strip()}'")
        print(f"Test result: {'✅ PASS' if is_success else '❌ FAIL'}")
        
        # Unittest assertion
        self.assertTrue(is_success)
        
    def test_create_event_failure(self):
        """Test event creation failure"""
        print("\n🧪 TEST: Create Event - Failure Case")
        
        # Create a mock DB that raises an exception
        mock_db_fail = MockDatabase()
        mock_db_fail.execute = MagicMock(side_effect=Exception("Database error"))
        event = Event(mock_db_fail)
        
        # Test data
        organization_id = 1
        title = "Charity Run"
        description = "Annual charity run for cancer research"
        event_date = "2023-12-15"
        location = "Central Park"
        
        # Expected output part
        expected_output_part = "❌ ERROR: Event creation failed!"
        
        # Execute the method and capture output
        output, _ = self.capture_output(
            event.create_event, 
            organization_id, title, description, event_date, location
        )
        
        # Assertions
        is_success = expected_output_part in output
        
        # Display results
        print(f"Expected output contains: '{expected_output_part}'")
        print(f"Actual output: '{output.strip()}'")
        print(f"Test result: {'✅ PASS' if is_success else '❌ FAIL'}")
        
        # Unittest assertion
        self.assertTrue(is_success)
        
    def test_view_active_events_with_data(self):
        """Test viewing active events when data exists"""
        print("\n🧪 TEST: View Active Events - With Data")
        
        # Mock data for active events
        mock_events = [
            (1, "Beach Cleanup", "Help clean the local beach", "2023-11-20", "Sunny Beach"),
            (2, "Food Drive", "Collect food for the local food bank", "2023-11-25", "Community Center")
        ]
        
        # Set up mock database with test data
        mock_db = MockDatabase(mock_events)
        event = Event(mock_db)
        
        # Test data
        user_id = 1
        
        # Expected output parts
        expected_output_parts = [
            "📌 Active Events Available for You to Volunteer:",
            "Event ID: 1",
            "Beach Cleanup",
            "Event ID: 2",
            "Food Drive"
        ]
        
        # Execute the method and capture output
        output, _ = self.capture_output(event.view_active_events, user_id)
        
        # Check if all expected parts are in the output
        all_parts_present = all(part in output for part in expected_output_parts)
        
        # Display results
        print(f"Expected output to contain: {expected_output_parts}")
        print(f"Actual output: '{output.strip()}'")
        print(f"Test result: {'✅ PASS' if all_parts_present else '❌ FAIL'}")
        
        # Unittest assertion
        self.assertTrue(all_parts_present)
        
    def test_view_active_events_no_data(self):
        """Test viewing active events when no data exists"""
        print("\n🧪 TEST: View Active Events - No Data")
        
        # Set up mock database with no data
        mock_db = MockDatabase([])
        event = Event(mock_db)
        
        # Test data
        user_id = 1
        
        # Expected output
        expected_output = "ℹ️ You have volunteered for all available events!"
        
        # Execute the method and capture output
        output, _ = self.capture_output(event.view_active_events, user_id)
        
        # Check if expected output is in the actual output
        is_success = expected_output in output
        
        # Display results
        print(f"Expected output: '{expected_output}'")
        print(f"Actual output: '{output.strip()}'")
        print(f"Test result: {'✅ PASS' if is_success else '❌ FAIL'}")
        
        # Unittest assertion
        self.assertTrue(is_success)
        
    def test_volunteer_for_event_success(self):
        """Test successful volunteering for an event"""
        print("\n🧪 TEST: Volunteer For Event - Success Case")
        
        # Mock data for user and event
        mock_user = [("John Doe",)]
        mock_event = [(1,)]
        
        # Set up mock database with sequential responses
        mock_db = MockDatabase()
        mock_db.fetch = MagicMock(side_effect=[mock_user, mock_event])
        event = Event(mock_db)
        
        # Test data
        user_id = 1
        event_id = 1
        
        # Expected output
        expected_output = "✅ John Doe, you have successfully volunteered for the event!"
        
        # Execute the method and capture output
        output, _ = self.capture_output(event.volunteer_for_event, user_id, event_id)
        
        # Check if expected output is in the actual output
        is_success = expected_output in output
        
        # Display results
        print(f"Expected output: '{expected_output}'")
        print(f"Actual output: '{output.strip()}'")
        print(f"Test result: {'✅ PASS' if is_success else '❌ FAIL'}")
        
        # Unittest assertion
        self.assertTrue(is_success)
        
    def test_volunteer_for_event_user_not_found(self):
        """Test volunteering for an event when user is not found"""
        print("\n🧪 TEST: Volunteer For Event - User Not Found")
        
        # Set up mock database with empty response for user query
        mock_db = MockDatabase([])
        event = Event(mock_db)
        
        # Test data
        user_id = 999  # Non-existent user
        event_id = 1
        
        # Expected output
        expected_output = "❌ ERROR: User not found!"
        
        # Execute the method and capture output
        output, _ = self.capture_output(event.volunteer_for_event, user_id, event_id)
        
        # Check if expected output is in the actual output
        is_success = expected_output in output
        
        # Display results
        print(f"Expected output: '{expected_output}'")
        print(f"Actual output: '{output.strip()}'")
        print(f"Test result: {'✅ PASS' if is_success else '❌ FAIL'}")
        
        # Unittest assertion
        self.assertTrue(is_success)
        
    def test_volunteer_for_event_event_not_found(self):
        """Test volunteering for an event when event is not found"""
        print("\n🧪 TEST: Volunteer For Event - Event Not Found")
        
        # Mock data for user but empty for event
        mock_user = [("John Doe",)]
        
        # Set up mock database with sequential responses
        mock_db = MockDatabase()
        mock_db.fetch = MagicMock(side_effect=[mock_user, []])
        event = Event(mock_db)
        
        # Test data
        user_id = 1
        event_id = 999  # Non-existent event
        
        # Expected output
        expected_output = "❌ ERROR: Event does not exist!"
        
        # Execute the method and capture output
        output, _ = self.capture_output(event.volunteer_for_event, user_id, event_id)
        
        # Check if expected output is in the actual output
        is_success = expected_output in output
        
        # Display results
        print(f"Expected output: '{expected_output}'")
        print(f"Actual output: '{output.strip()}'")
        print(f"Test result: {'✅ PASS' if is_success else '❌ FAIL'}")
        
        # Unittest assertion
        self.assertTrue(is_success)
        
    def test_view_volunteer_history_with_data(self):
        """Test viewing volunteer history when data exists"""
        print("\n🧪 TEST: View Volunteer History - With Data")
        
        # Mock data for volunteer history
        mock_history = [
            (1, "Beach Cleanup", "2023-10-15", "Sunny Beach", "John Doe"),
            (2, "Food Drive", "2023-10-20", "Community Center", "John Doe")
        ]
        
        # Set up mock database with test data
        mock_db = MockDatabase(mock_history)
        event = Event(mock_db)
        
        # Test data
        user_id = 1
        
        # Expected output parts
        expected_output_parts = [
            "📜 Your Volunteer History:",
            "📌 Event 1: Beach Cleanup on 2023-10-15 at Sunny Beach",
            "📌 Event 2: Food Drive on 2023-10-20 at Community Center"
        ]
        
        # Execute the method and capture output
        output, _ = self.capture_output(event.view_volunteer_history, user_id)
        
        # Check if all expected parts are in the output
        all_parts_present = all(part in output for part in expected_output_parts)
        
        # Display results
        print(f"Expected output to contain: {expected_output_parts}")
        print(f"Actual output: '{output.strip()}'")
        print(f"Test result: {'✅ PASS' if all_parts_present else '❌ FAIL'}")
        
        # Unittest assertion
        self.assertTrue(all_parts_present)

def run_tests():
    """Run all tests with custom output formatting"""
    print("\n" + "="*80)
    print("🧪 EVENT CLASS TEST SUITE 🧪".center(80))
    print("="*80)
    
    # Create a test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestEvent)
    
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