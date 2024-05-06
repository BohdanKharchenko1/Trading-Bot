import unittest
from unittest.mock import MagicMock, patch
from src.controller.start_menu_controller import StartMenuController


class TestStartMenuController(unittest.TestCase):
    def setUp(self):
        # Mock the required components
        self.mock_view = MagicMock()
        self.mock_start_menu_model = MagicMock()
        self.mock_trading_data_fetcher = MagicMock()
        self.mock_account_interaction_model = MagicMock()
        self.mock_config_model = MagicMock()

        # Instantiate the controller with mocked components
        self.controller = StartMenuController(
            view=self.mock_view,
            start_menu_model=self.mock_start_menu_model,
            trading_data_fetcher=self.mock_trading_data_fetcher,
            account_interaction_model=self.mock_account_interaction_model,
            config_model=self.mock_config_model
        )


    @patch('src.model.automated_trader.AutomatedTrader')
    def test_toggle_automated_trading(self, mock_automated_trader):
        # Setup strategy data and simulate button click
        strategy = {'name': 'strategy1'}
        self.controller.toggle_automated_trading(strategy)

        # Check if a new trader is created and started
        mock_automated_trader.assert_called_once()
        mock_automated_trader.return_value.start.assert_called_once()

    def test_handle_fetch_pnl(self):
        # Setup to return some PnL data
        self.mock_start_menu_model.fetch_closed_pnl.return_value = {
            'list': [{'closedPnl': '1000'}, {'closedPnl': '500'}]}
        self.controller.handle_fetch_pnl()

        # Check if the PnL data is correctly processed and displayed
        self.mock_view.display_pnl.assert_called_with(1500.0)

    def test_handle_close_positions(self):
        # Setup to simulate successful position closure
        self.mock_start_menu_model.close_all_positions.return_value = True
        self.controller.handle_close_positions()

        # Check message display on success
        self.mock_view.show_message.assert_called_with("All positions have been closed.")

    def test_handle_open_positions(self):
        # Setup to simulate fetching positions
        self.mock_start_menu_model.fetch_open_positions.return_value = [{'position': 'data'}]
        self.controller.handle_open_positions()

        # Check if positions are displayed correctly
        self.mock_view.display_positions.assert_called_with([{'position': 'data'}])
