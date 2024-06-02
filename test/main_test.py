import unittest
from unittest.mock import patch, MagicMock
import sys
import os


# Ensure the Project directory is in the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import check_email, getLastMessage, sendMessage, sendInlineMessageForService

class TestMainFunctions(unittest.TestCase):

    @patch('main.os.getenv')
    def setUp(self, mock_getenv):
        mock_getenv.return_value = "fake_api_key"

    def test_check_email_valid(self):
        valid_email = "test@example.com"
        self.assertTrue(check_email(valid_email))

    def test_check_email_invalid(self):
        invalid_email = "invalid-email"
        self.assertFalse(check_email(invalid_email))

    @patch('main.requests.get')
    def test_getLastMessage_success(self, mock_get):
        mock_response = MagicMock()
        expected_json = {
            "result": [
                {"update_id": 1, "message": {"text": "Hello", "chat": {"id": 123}}}
            ]
        }
        mock_response.json.return_value = expected_json
        mock_get.return_value = mock_response

        last_msg, chat_id, update_id = getLastMessage()
        self.assertEqual(last_msg, "Hello")
        self.assertEqual(chat_id, 123)
        self.assertEqual(update_id, 1)

    @patch('main.requests.get')
    def test_getLastMessage_no_message(self, mock_get):
        mock_response = MagicMock()
        expected_json = {"result": []}
        mock_response.json.return_value = expected_json
        mock_get.return_value = mock_response

        last_msg, chat_id, update_id = getLastMessage()
        self.assertIsNone(last_msg)
        self.assertIsNone(chat_id)
        self.assertIsNone(update_id)

    @patch('main.requests.get')
    def test_sendMessage(self, mock_get):
        mock_response = MagicMock()
        mock_get.return_value = mock_response

        chat_id = 123
        text_message = "Hello, World!"
        response = sendMessage(chat_id, text_message)
        self.assertEqual(response, mock_response)

    @patch('main.requests.get')
    def test_sendInlineMessageForService(self, mock_get):
        mock_response = MagicMock()
        mock_get.return_value = mock_response

        chat_id = 123
        response = sendInlineMessageForService(chat_id)
        self.assertEqual(response, mock_response)

if __name__ == '__main__':
    unittest.main()
