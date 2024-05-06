import unittest
from unittest.mock import MagicMock, patch, mock_open

from PyQt5 import QtWidgets

from src.model.config_model import ConfigModel


class TestConfigModel(unittest.TestCase):

    def setUp(self):
        QtWidgets.QMessageBox = MagicMock()  # Mock the QMessageBox before instances are created
        self.config_model = ConfigModel()

    @patch("builtins.open", new_callable=mock_open, read_data='{"api_key": "key123", "api_secret": "secret123"}')
    @patch("os.path.exists", return_value=True)
    def test_load_configuration_success(self, mock_exists, mock_file):
        self.config_model.load_configuration()
        self.assertEqual(self.config_model.api_key, "key123")
        self.assertEqual(self.config_model.api_secret, "secret123")
        mock_file.assert_called_once_with(self.config_model.config_file_path, 'r')

    @patch("json.dump")
    @patch("builtins.open", new_callable=mock_open)
    def test_save_configuration(self, mock_file, mock_json_dump):
        result = self.config_model.save_configuration()
        self.assertTrue(result)
        mock_file.assert_called_once_with(self.config_model.config_file_path, 'w')
        mock_json_dump.assert_called_once()

    @patch("builtins.open", new_callable=mock_open, read_data='{"trading_strategies": {"strategy1": "details"}}')
    def test_load_trading_config(self, mock_file):
        result = self.config_model.load_trading_config()
        self.assertEqual(result, {"strategy1": "details"})

    @patch("json.dump")
    @patch("builtins.open", new_callable=mock_open)
    def test_save_web_configuration(self, mock_file, mock_json_dump):
        result = self.config_model.save_web_configuration("192.168.1.1", 8080)
        self.assertTrue(result)
        mock_file.assert_called_once()
        mock_json_dump.assert_called_once()

    @patch("builtins.open", new_callable=mock_open, read_data='{"ip_address": "192.168.1.1", "port": 8080}')
    def test_load_web_configuration(self, mock_file):
        ip_address, port = self.config_model.load_web_configuration()
        self.assertEqual(ip_address, "192.168.1.1")
        self.assertEqual(port, 8080)

    @patch("pybit.unified_trading.HTTP")
    def test_test_connection_no_session(self, mock_http):
        self.config_model.session = None
        result = self.config_model.test_connection()
        self.assertEqual(result, "Session not established. Cannot test connection.")

    @patch("pybit.unified_trading.HTTP.get_account_info", return_value={"info": "some_account_info"})
    def test_test_connection_success(self, mock_get_account_info):
        self.config_model.session = MagicMock()
        self.config_model.session.get_account_info = mock_get_account_info
        result = self.config_model.test_connection()
        self.assertIsNone(result)
        mock_get_account_info.assert_called_once()
