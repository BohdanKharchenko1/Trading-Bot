import unittest
from unittest.mock import MagicMock, mock_open, patch
import bcrypt
from src.model.account_model import AccountModel


class TestAccountModel(unittest.TestCase):
    def setUp(self):
        self.account_model = AccountModel()

    @patch('os.path.exists', return_value=False)
    @patch('builtins.open', new_callable=mock_open)
    def test_init_no_existing_file(self, mock_file, mock_exists):
        # Test initialization when no account file exists
        AccountModel()
        mock_file.assert_called_once()  # Check that it attempted to open a file to write the default empty accounts

    @patch('os.path.exists', return_value=True)
    @patch('builtins.open', mock_open(read_data='{"user1": "hashed_password"}'))
    @patch('json.load', return_value={'user1': 'hashed_password'})
    def test_init_existing_file(self, mock_load, mock_file, mock_exists):
        # Test loading existing accounts from file
        model = AccountModel()
        self.assertEqual(model.accounts, {'user1': 'hashed_password'})

    @patch('builtins.open', new_callable=mock_open)
    def test_create_user(self, mock_file):
        # Setup
        self.account_model.accounts = {}
        username = "testuser"
        password = "password123"

        # Action
        self.account_model.create_user(username, password)

        # Assert
        self.assertIn(username, self.account_model.accounts)
        hashed_password = self.account_model.accounts[username]
        self.assertTrue(bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')))

    @patch('builtins.open', new_callable=mock_open)
    def test_verify_user(self, mock_file):
        # Setup user creation
        username = "testuser"
        password = "password123"
        self.account_model.create_user(username, password)

        # Action and Assert
        self.assertTrue(self.account_model.verify_user(username, password))
        self.assertFalse(self.account_model.verify_user(username, "wrongpassword"))

    @patch('builtins.open', new_callable=mock_open)
    def test_delete_user(self, mock_file):
        # Setup
        username = "testuser"
        password = "password123"
        self.account_model.create_user(username, password)

        # Action
        self.account_model.delete_user(username)

        # Assert
        self.assertNotIn(username, self.account_model.accounts)

    @patch('builtins.open', new_callable=mock_open)
    def test_user_exists(self, mock_file):
        # Setup
        username = "testuser"
        password = "password123"
        self.account_model.create_user(username, password)

        # Action and Assert
        self.assertTrue(self.account_model.user_exists(username))
        self.assertFalse(self.account_model.user_exists("nonexistentuser"))

