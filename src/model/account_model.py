import json
import os
import bcrypt

class AccountModel:
    """
    A class that manages user account operations including creation, verification, and deletion,
    as well as saving and loading account details to and from a JSON file.

    Attributes:
        account_config_path (str): Path to the JSON file where account information is stored.
        accounts (dict): A dictionary storing user account details, typically username and hashed password.
    """

    def __init__(self):
        """
        Initializes the AccountModel, setting the file path for the account configurations and loading existing
        accounts from file or creating a new empty account dictionary if the file does not exist.
        """
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(current_dir))
        self.account_config_path = os.path.join(project_root, 'config', 'account.json')

        if not os.path.exists(self.account_config_path):
            self.accounts = {}
            self._save_accounts_to_file()
        else:
            try:
                self._load_accounts_from_file()
            except Exception as e:
                print(f"Failed to load accounts: {e}")
                self.accounts = {}

    def _load_accounts_from_file(self):
        """
        Private method to load account information from the JSON configuration file.
        Handles JSON decoding errors and general file reading exceptions.
        """
        try:
            with open(self.account_config_path, 'r') as file:
                self.accounts = json.load(file)
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
            self.accounts = {}  # Reset if the content is corrupted
        except Exception as e:
            print(f"Failed to read file: {e}")
            self.accounts = {}

    def _save_accounts_to_file(self):
        """
        Private method to save the current accounts dictionary to the JSON configuration file.
        Handles general file writing exceptions.
        """
        try:
            with open(self.account_config_path, 'w') as file:
                json.dump(self.accounts, file, indent=4)
        except Exception as e:
            print(f"Failed to save accounts: {e}")

    def create_user(self, username, password):
        """
        Creates a new user account with a username and password. Passwords are hashed before storage.
        Raises a ValueError if an account already exists with the given username or if the account limit is reached.

        Parameters:
            username (str): The username for the new account.
            password (str): The password for the new account.
        """
        if len(self.accounts) >= 1:
            raise ValueError("Only one account is allowed.")

        if username in self.accounts:
            raise ValueError("Username already exists.")

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        self.accounts[username] = hashed_password.decode('utf-8')  # Store the hashed password as a string
        try:
            self._save_accounts_to_file()
        except Exception as e:
            print(f"Failed to create user: {e}")

    def verify_user(self, username, password):
        """
        Verifies a user's password against the stored hashed password.

        Parameters:
            username (str): The username to verify.
            password (str): The password to verify.

        Returns:
            bool: True if the password matches the stored hash, False otherwise.
        """
        try:
            stored_password = self.accounts.get(username)
            if stored_password is not None:
                return bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8'))
            return False
        except Exception as e:
            print(f"Error verifying user: {e}")
            return False

    def delete_user(self, username):
        """
        Deletes a user account by username.

        Parameters:
            username (str): The username of the account to delete.

        Raises:
            ValueError: If the username does not exist.
        """
        try:
            if username in self.accounts:
                del self.accounts[username]
                self._save_accounts_to_file()
                print(f"User '{username}' deleted successfully.")
            else:
                raise ValueError("Username does not exist.")
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Error deleting user: {e}")

    def user_exists(self, username):
        """
        Checks if a user exists in the account dictionary.

        Parameters:
            username (str): The username to check.

        Returns:
            bool: True if the username exists, False otherwise.
        """
        try:
            return username in self.accounts
        except Exception as e:
            print(f"Error checking user existence: {e}")
            return False

    def get_password_hash(self, username):
        """
        Retrieves the stored password hash for a given username.

        Parameters:
            username (str): The username for which to retrieve the password hash.

        Returns:
            str or None: The password hash if the user exists, None otherwise.
        """
        try:
            return self.accounts.get(username)
        except Exception as e:
            print(f"Error getting password hash for user '{username}': {e}")
            return None
