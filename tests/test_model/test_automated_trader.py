import unittest
from unittest.mock import MagicMock, patch

from src.model.automated_trader import AutomatedTrader


class TestAutomatedTrader(unittest.TestCase):
    def setUp(self):
        self.mock_start_menu_model = MagicMock()
        self.mock_trading_data_fetcher = MagicMock()
        self.mock_account_interaction_model = MagicMock()
        self.trader = AutomatedTrader(self.mock_start_menu_model, self.mock_trading_data_fetcher,
                                      self.mock_account_interaction_model, interval=3600)
        self.trader.daemon = True  # Ensure the thread does not block the test exit

    @patch("time.sleep", side_effect=InterruptedError("Interrupt for quick test"))
    def test_run(self, mock_sleep):
        with self.assertRaises(InterruptedError):
            self.trader.run()
        self.assertTrue(self.trader.running)

    def test_perform_trade_check_no_orders(self):
        self.mock_account_interaction_model.get_open_orders.return_value = False
        self.mock_start_menu_model.fetch_and_process_data.return_value = 'input_data'
        self.mock_start_menu_model.predict_and_execute_trade.return_value = True
        self.trader.interruptible_sleep = MagicMock()

        self.trader.perform_trade_check()

        self.mock_start_menu_model.predict_and_execute_trade.assert_called_with('input_data',
                                                                                self.mock_trading_data_fetcher,
                                                                                self.mock_account_interaction_model)
        self.trader.interruptible_sleep.assert_called_with(900)  # Check if the wait after trade is 15 minutes

    def test_get_server_time_with_retry_success(self):
        self.mock_account_interaction_model.get_server_time.return_value = 3600
        result = self.trader.get_server_time_with_retry()
        self.assertEqual(result, 3600)

    def test_get_server_time_with_retry_failure(self):
        self.mock_account_interaction_model.get_server_time.side_effect = Exception("Network Error")
        result = self.trader.get_server_time_with_retry()
        self.assertIsNone(result)

    def test_stop_trading(self):
        self.trader.running = True
        self.trader.stop_trading()
        self.assertFalse(self.trader.running)
