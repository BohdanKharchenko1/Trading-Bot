# config_model.py
import json
import os

from PyQt5 import QtWidgets
from pybit.unified_trading import HTTP


class ConfigModel:
    def __init__(self, api_key="", api_secret=""):
        self.api_key = api_key
        self.api_secret = api_secret
        self.session = None
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(current_dir))
        self.trading_config_path = os.path.join(project_root, 'config', 'trading_config.json')
        self.config_file_path = os.path.join(project_root, 'config', 'config.json')
        self.web_config_path = os.path.join(project_root, 'config', 'web_config.json')
        self.load_configuration()
        self.trading_config = self.load_trading_config()

    def update_session(self):
        try:
            self.session = HTTP(testnet=True, api_key=self.api_key, api_secret=self.api_secret)
        except Exception as e:
            print(f"Failed to update session: {e}")

    def test_connection(self):
        if not self.session:
            return "Session not established. Cannot test connection."
        try:
            info = self.session.get_account_info()
            print(info)
            return None if info else "No account information returned"


        except Exception as e:
            return f"Connection test failed: {e}"

    def save_configuration(self):
        try:
            config_data = {
                "api_key": self.api_key,
                "api_secret": self.api_secret
            }
            with open(self.config_file_path, 'w') as file:
                json.dump(config_data, file, indent=4)
            return True
        except (FileNotFoundError, IOError) as e:
            print(f"Failed to save configuration: {e}")
            return False

    def load_configuration(self):
        try:
            with open(self.config_file_path, 'r') as file:
                config_data = json.load(file)
                self.api_key = config_data.get('api_key', '')
                self.api_secret = config_data.get('api_secret', '')
                self.update_session()
        except FileNotFoundError:
            print("Configuration file not found. Using defaults.")
        except json.JSONDecodeError as e:
            print(f"Error reading configuration file: {e}. Using defaults.")

    def load_credentials_from_file(self, file_path):
        try:
            with open(file_path, 'r') as file:
                # Read the single line containing the credentials
                credentials = file.readline().strip()
                # Split the line into api_key and secret, assuming they are separated by a comma
                parts = credentials.split(',')
                if len(parts) == 2:
                    self.api_key = parts[0].strip()
                    self.api_secret = parts[1].strip()
                    self.update_session()
                    QtWidgets.QMessageBox.information(None, "Success", "Credentials loaded successfully.")
                else:
                    QtWidgets.QMessageBox.critical(None, "Format Error",
                                                   "The file format is incorrect. Expected 'api_key, secret'.")
        except FileNotFoundError:
            QtWidgets.QMessageBox.critical(None, "File Not Found", "The specified file was not found.")
        except Exception as e:
            QtWidgets.QMessageBox.critical(None, "Error", f"An unexpected error occurred: {e}")

    def load_trading_config(self):
        """
        Loads trading configuration from a JSON file.
        """
        try:
            with open(self.trading_config_path, 'r') as file:
                config = json.load(file)
            print("Trading configuration loaded successfully.")
            return config['trading_strategies']
        except FileNotFoundError:
            print("Trading configuration file not found.")
            return {}
        except json.JSONDecodeError:
            print("Error decoding the trading configuration.")
            return {}
        except Exception as e:
            print(f"An error occurred while loading trading configuration: {e}")
            return {}

    def save_web_configuration(self, ip_address, port):
        """
        Saves the web server configuration to a JSON file.

        Args:
        ip_address (str): The IP address for the web server.
        port (int): The port number for the web server.

        Returns:
        bool: True if the configuration was saved successfully, False otherwise.
        """
        try:
            web_config_data = {
                "ip_address": ip_address,
                "port": port
            }
            with open(self.web_config_path, 'w') as file:
                json.dump(web_config_data, file, indent=4)
            print("Web configuration saved successfully.")
            return True
        except (FileNotFoundError, IOError) as e:
            print(f"Failed to save web configuration: {e}")
            return False

    def load_web_configuration(self):
        """
        Loads the web server configuration from a JSON file.

        Returns:
        tuple: A tuple containing the IP address and port if loaded successfully, or None if an error occurs.
        """
        try:
            with open(self.web_config_path, 'r') as file:
                web_config_data = json.load(file)
            ip_address = web_config_data.get("ip_address", "127.0.0.1")  # Default to localhost if not set
            port = web_config_data.get("port", 8000)  # Default to port 8000 if not set
            print("Web configuration loaded successfully:", ip_address, port)
            return ip_address, int(port)
        except FileNotFoundError:
            print("Web configuration file not found. Using default settings.")
            return "127.0.0.1", 8000  # Return default values if the file doesn't exist
        except json.JSONDecodeError as e:
            print(f"Error decoding the web configuration: {e}")
            return None
        except Exception as e:
            print(f"An unexpected error occurred while loading web configuration: {e}")
            return None
