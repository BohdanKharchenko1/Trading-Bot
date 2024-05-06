import unittest
from unittest.mock import MagicMock

from src.model.main_window_model import MainWindowModel


class TestMainWindowModel(unittest.TestCase):
    def setUp(self):
        self.mock_config_model = MagicMock()
        self.mock_http = MagicMock()
        self.main_window_model = MainWindowModel(self.mock_config_model)
        self.main_window_model.session = self.mock_http

    def test_fetch_data_failure(self):
        self.mock_http.get_kline.return_value = {}
        df = self.main_window_model.fetch_data()
        self.assertTrue(df.empty)

    def test_format_data_success(self):
        data = [
            {'timestamp': 1609459200000, 'open': '29000', 'high': '29500', 'low': '28700', 'close': '29400',
             'volume': '5000', 'turnover': '1000'}
        ]
        df = self.main_window_model.format_data(data)
        self.assertFalse(df.empty)
        self.assertEqual(df.iloc[0]['open'], 29000)

    def test_format_data_empty(self):
        df = self.main_window_model.format_data([])
        self.assertTrue(df.empty)
