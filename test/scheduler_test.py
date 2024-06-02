import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Ensure the Project directory is in the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scheduler import book_timeslot

class TestSchedulerFunctions(unittest.TestCase):
    @patch('scheduler.build')
    @patch('scheduler.InstalledAppFlow')
    @patch('scheduler.pickle.load')
    @patch('scheduler.os.path.exists')
    @patch('scheduler.open', create=True)
    def test_book_timeslot(self, mock_open, mock_exists, mock_pickle_load, mock_InstalledAppFlow, mock_build):
        # Mock the credential flow
        mock_exists.return_value = True
        mock_creds = MagicMock()
        mock_creds.valid = True
        mock_pickle_load.return_value = mock_creds

        # Mock Google Calendar API
        mock_service = MagicMock()
        mock_build.return_value = mock_service

        # Mock events list
        mock_events = {
            'items': []
        }
        mock_service.events().list().execute.return_value = mock_events

        event_description = "Meeting"
        booking_time = "10:00"
        input_email = "test@example.com"
        booking_date = "2024-05-20"

        result = book_timeslot(event_description, booking_time, input_email, booking_date)
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
