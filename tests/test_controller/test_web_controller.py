import unittest
from unittest.mock import MagicMock, patch
from PyQt5 import QtWidgets
from src.controller.web_controller import WebController


class TestWebController(unittest.TestCase):
    def setUp(self):
        # Mock the view, model, and config_model
        self.mock_view = MagicMock()
        self.mock_model = MagicMock()
        self.mock_config_model = MagicMock()

        # Set up inputs in the view
        self.mock_view.ip_input = MagicMock()
        self.mock_view.port_input = MagicMock()

        # Instantiate the controller with mocked components
        self.controller = WebController(self.mock_view, self.mock_model, self.mock_config_model)

    def test_connect_signals(self):
        # Test that signals are connected correctly
        self.mock_view.start_web_button.clicked.connect.assert_called_with(self.controller.start_web_server)
        self.mock_view.save_button.clicked.connect.assert_called_with(self.controller.save_configuration)

    def test_load_and_display_web_configuration(self):
        # Configure the mock to simulate loaded configuration
        self.mock_config_model.load_web_configuration.return_value = ("192.168.1.1", 8080)
        self.controller.load_and_display_web_configuration()
        self.mock_view.ip_input.setText.assert_called_once_with("192.168.1.1")
        self.mock_view.port_input.setText.assert_called_once_with("8080")

    @patch('PyQt5.QtWidgets.QMessageBox')
    def test_start_web_server(self, mock_message_box):
        # Set up input text returns
        self.mock_view.ip_input.text.return_value = "192.168.1.1"
        self.mock_view.port_input.text.return_value = "8080"
        self.controller.validate_ip_port = MagicMock(return_value=True)

        # Execute the method
        self.controller.start_web_server()

        # Assertions
        self.mock_model.start_web_server.assert_called_with("192.168.1.1", 8080)
        mock_message_box.information.assert_called_once()

    @patch('PyQt5.QtWidgets.QMessageBox')
    def test_save_configuration(self, mock_message_box):
        # Set up input text returns
        self.mock_view.ip_input.text.return_value = "192.168.1.1"
        self.mock_view.port_input.text.return_value = "8080"
        self.controller.validate_ip_port = MagicMock(return_value=True)
        self.mock_config_model.save_web_configuration.return_value = True

        # Execute the method
        self.controller.save_configuration()

        # Assertions
        mock_message_box.information.assert_called_once_with(self.mock_view, "Success",
                                                             "Configuration saved successfully.")

    def test_validate_ip_port(self):
        # Set up input text returns
        self.mock_view.ip_input.text.return_value = "192.168.1.1"
        self.mock_view.port_input.text.return_value = "8080"

        # Execute the method
        result = self.controller.validate_ip_port("192.168.1.1", "8080")

        # Assertions
        self.assertTrue(result)

    @patch('PyQt5.QtWidgets.QMessageBox')
    def test_validate_ip_port_failure(self, mock_message_box):
        # Set up input text returns
        self.mock_view.ip_input.text.return_value = ""
        self.mock_view.port_input.text.return_value = "65536"  # Invalid port number

        # Execute the method
        result = self.controller.validate_ip_port("", "65536")

        # Assertions
        self.assertFalse(result)
        mock_message_box.warning.assert_called()
