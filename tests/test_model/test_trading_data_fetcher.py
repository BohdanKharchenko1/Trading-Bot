import unittest
from unittest.mock import MagicMock, patch

from src.model.trading_data_fetcher import TradingDataFetcher


class TestTradingDataFetcher(unittest.TestCase):
    def setUp(self):
        self.mock_config_model = MagicMock()
        self.data_fetcher = TradingDataFetcher(self.mock_config_model)

    def test_fetch_data_no_session(self):
        # Simulate a scenario where the session is not initialized
        self.data_fetcher.session = None
        result = self.data_fetcher.fetch_data()
        self.assertTrue(result.empty)

    @patch('pybit.unified_trading.HTTP.get_kline')
    def test_fetch_data_api_failure(self, mock_get_kline):
        # Simulate API failure
        mock_get_kline.side_effect = Exception("API Error")
        result = self.data_fetcher.fetch_data()
        self.assertTrue(result.empty)

    @patch('pybit.unified_trading.HTTP.get_kline')
    def test_format_data_empty_list(self, mock_get_kline):
        # Test formatting when there's no valid data in the list
        mock_get_kline.return_value = {'result': {'list': []}}
        result = self.data_fetcher.fetch_data()
        self.assertTrue(result.empty)

    @patch('pybit.unified_trading.HTTP.get_kline')
    def test_fetch_last_btc_price_failure(self, mock_get_kline):
        # Test handling failures during price fetch
        mock_get_kline.side_effect = Exception("Failed to fetch price")
        price = self.data_fetcher.fetch_last_btc_price()
        self.assertIsNone(price)
