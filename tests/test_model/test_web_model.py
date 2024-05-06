import unittest
from unittest.mock import patch, MagicMock

from src.model.web_model import WebModel


class TestWebModel(unittest.TestCase):
    def setUp(self):
        self.web_model = WebModel()

    @patch('src.model.web_model.Process')
    def test_start_web_server_existing_alive_process(self, mock_process):
        # Simulate an existing alive server process
        self.web_model.server_process = MagicMock()
        self.web_model.server_process.is_alive.return_value = True

        ip = "127.0.0.1"
        port = 5000
        self.web_model.start_web_server(ip, port)

        self.web_model.server_process.start.assert_not_called()

    def test_stop_web_server_alive_process(self):
        # Simulate an existing alive server process
        self.web_model.server_process = MagicMock()
        self.web_model.server_process.is_alive.return_value = True

        self.web_model.stop()

        self.web_model.server_process.terminate.assert_called_once()
        self.web_model.server_process.join.assert_called_once()
        print("Web server process has been stopped.")

    def test_stop_web_server_no_process(self):
        # No process to stop
        self.web_model.stop()

        # Ensure nothing has been called since there was no process
        assert self.web_model.server_process is None

    def test_stop_web_server_dead_process(self):
        # Simulate an existing dead server process
        self.web_model.server_process = MagicMock()
        self.web_model.server_process.is_alive.return_value = False

        self.web_model.stop()

        self.web_model.server_process.terminate.assert_not_called()
        self.web_model.server_process.join.assert_not_called()
