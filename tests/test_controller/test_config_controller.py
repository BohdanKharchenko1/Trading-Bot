import unittest
from unittest.mock import MagicMock, patch
from PyQt5 import QtWidgets
from src.controller.config_controller import ConfigController


class TestConfigController(unittest.TestCase):
    def setUp(self):
        # Mock the view and model
        self.mock_view = MagicMock()
        self.mock_model = MagicMock()
        self.mock_view.test_button = MagicMock()
        self.mock_view.save_button = MagicMock()
        self.mock_view.file_button = MagicMock()
        self.mock_view.api_key = MagicMock()
        self.mock_view.api_secret = MagicMock()

        # Instantiate the controller
        self.controller = ConfigController(self.mock_view, self.mock_model)

    def test_connect_signals(self):
        # Test that signals are connected correctly
        self.mock_view.test_button.clicked.connect.assert_called_with(self.controller._test_connection)
        self.mock_view.save_button.clicked.connect.assert_called_with(self.controller._save_configuration)
        self.mock_view.file_button.clicked.connect.assert_called_with(self.controller._load_credentials_from_file)

    @patch('PyQt5.QtWidgets.QMessageBox')
    def test_test_connection(self, mock_message_box):
        # Setup
        self.mock_model.test_connection.return_value = None  # Simulate successful connection

        # Action
        self.controller._test_connection()

        # Assert
        mock_message_box.information.assert_called_once()

    @patch('PyQt5.QtWidgets.QMessageBox')
    def test_test_connection_failure(self, mock_message_box):
        # Setup
        self.mock_model.test_connection.return_value = "Network Timeout"  # Simulate failed connection

        # Action
        self.controller._test_connection()

        # Assert
        mock_message_box.critical.assert_called_once_with(self.mock_view, "Error", "Connection failed: Network Timeout")

    @patch('PyQt5.QtWidgets.QMessageBox')
    def test_save_configuration(self, mock_message_box):
        # Setup
        self.mock_view.api_key.text.return_value = "new_api_key"
        self.mock_view.api_secret.text.return_value = "new_api_secret"
        self.mock_model.save_configuration.return_value = True

        # Action
        self.controller._save_configuration()

        # Assert
        self.assertEqual(self.mock_model.api_key, "new_api_key")
        self.assertEqual(self.mock_model.api_secret, "new_api_secret")
        mock_message_box.information.assert_called_once_with(self.mock_view, "Success", "Configuration saved successfully.")

