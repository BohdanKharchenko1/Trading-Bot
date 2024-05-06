import unittest
from unittest.mock import MagicMock, patch

import numpy as np

from src.model.start_menu_model import StartMenuModel


class TestStartMenuModel(unittest.TestCase):
    def setUp(self):
        self.mock_config_model = MagicMock()
        self.mock_trading_data_fetcher = MagicMock()
        self.mock_account_interaction_model = MagicMock()
        self.start_menu_model = StartMenuModel(self.mock_config_model)

    def test_set_current_strategy(self):
        strategy = {'strategy_name': 'Test Strategy'}
        self.start_menu_model.set_current_strategy(strategy)
        self.assertEqual(self.start_menu_model.current_strategy, strategy)

    def test_fetch_and_process_data_empty(self):
        self.mock_trading_data_fetcher.fetch_data.return_value = []
        result = self.start_menu_model.fetch_and_process_data(self.mock_trading_data_fetcher)
        self.assertIsNone(result)

    def test_fetch_and_process_data_insufficient(self):
        data = np.random.rand(30, 8)
        self.mock_trading_data_fetcher.fetch_data.return_value = data
        result = self.start_menu_model.fetch_and_process_data(self.mock_trading_data_fetcher)
        self.assertIsNone(result)

    def test_predict_and_execute_trade_no_prediction(self):
        self.mock_trading_data_fetcher.fetch_last_btc_price.return_value = 10000
        input_data = np.random.rand(1, 40, 8)
        predicted_price = None
        self.start_menu_model.predict_next_price = MagicMock(return_value=predicted_price)
        result = self.start_menu_model.predict_and_execute_trade(input_data, self.mock_trading_data_fetcher,
                                                                 self.mock_account_interaction_model)
        self.assertFalse(result)

    @patch('src.model.start_menu_model.StartMenuModel.place_order')
    def test_make_trade_decision(self, mock_place_order):
        self.start_menu_model.current_strategy = {'leverage': 10, 'balance_percentage': 0.1,
                                                  'risk_management': {'stop_loss': 0.01, 'take_profit': 0.03}}
        self.mock_trading_data_fetcher.fetch_data.return_value = np.random.rand(50, 8)
        self.mock_account_interaction_model.get_usdt_balance.return_value = '10000'
        predicted_price = 11000
        last_price = 10000
        result = self.start_menu_model.make_trade_decision(predicted_price, last_price,
                                                           self.mock_account_interaction_model,
                                                           self.mock_trading_data_fetcher)
        self.assertTrue(result)
        mock_place_order.assert_called_once()
