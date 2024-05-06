import unittest
from unittest.mock import MagicMock, patch
from src.model.account_interaction_model import AccountInteractionModel


class TestAccountInteractionModel(unittest.TestCase):
    def setUp(self):
        self.mock_config_model = MagicMock(api_key="test_key", api_secret="test_secret")
        self.account_model = AccountInteractionModel(self.mock_config_model)



    @patch('pybit.unified_trading.HTTP.set_leverage')
    def test_set_leverage(self, mock_set_leverage):
        # Setup mock response
        mock_set_leverage.return_value = {'retCode': 0}
        result = self.account_model.set_leverage('BTCUSDT', 10)
        self.assertTrue(result)

    @patch('pybit.unified_trading.HTTP.get_open_orders')
    def test_get_open_orders(self, mock_get_open_orders):
        # Setup mock response
        mock_get_open_orders.return_value = {
            'retCode': 0,
            'result': {
                'list': [{'order_id': '123', 'status': 'open'}]
            }
        }
        orders = self.account_model.get_open_orders('BTCUSDT')
        self.assertEqual(len(orders), 1)
        self.assertEqual(orders[0]['order_id'], '123')

    @patch('pybit.unified_trading.HTTP.cancel_all_orders')
    def test_cancel_all_orders(self, mock_cancel_all_orders):
        # Setup mock response
        mock_cancel_all_orders.return_value = {'retCode': 0}
        result = self.account_model.cancel_all_orders('BTCUSDT')
        self.assertTrue(result)

    @patch('pybit.unified_trading.HTTP.get_order_history')
    def test_get_order_history(self, mock_get_order_history):
        # Setup mock response
        mock_get_order_history.return_value = {
            'retCode': 0,
            'result': {
                'data': [{'order_id': '123', 'status': 'filled'}]
            }
        }
        history = self.account_model.get_order_history('BTCUSDT')
        self.assertIsInstance(history, list)
        self.assertEqual(history[0]['order_id'], '123')

    @patch('pybit.unified_trading.HTTP.get_closed_pnl')
    def test_get_closed_pnl(self, mock_get_closed_pnl):
        # Setup mock response
        mock_get_closed_pnl.return_value = {
            'retCode': 0,
            'result': {'total_pnl': '1000'}
        }
        pnl = self.account_model.get_closed_pnl('BTCUSDT')
        self.assertEqual(pnl['total_pnl'], '1000')

    @patch('pybit.unified_trading.HTTP.get_server_time')
    def test_get_server_time(self, mock_get_server_time):
        # Setup mock response
        mock_get_server_time.return_value = {
            'retCode': 0,
            'result': {'timeSecond': 1620000000}
        }
        server_time = self.account_model.get_server_time()
        self.assertEqual(server_time, 1620000000)

    @patch('pybit.unified_trading.HTTP.place_order')
    def test_place_reduce_only_order(self, mock_place_order):
        # Setup mock response
        mock_place_order.return_value = {'retCode': 0}
        response = self.account_model.place_reduce_only_order('BTCUSDT', '1', 'Sell')
        self.assertEqual(response['retCode'], 0)
