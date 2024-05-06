from functools import partial

from src.model.automated_trader import AutomatedTrader


class StartMenuController:
    """
    A controller class responsible for managing interactions between the user interface and the underlying
    business logic for starting and stopping automated trading, updating configurations, and handling trading strategies.

    Attributes:
        view (QtWidgets.QMainWindow): The main window or widget that contains the GUI elements.
        model (object): The start menu model which provides an interface to the trading functionality.
        trading_data_fetcher (object): An instance responsible for fetching trading data.
        account_interaction_model (object): An instance managing direct interactions with the trading account.
        config_model (object): A model for loading and saving configuration settings.
        automated_trader (AutomatedTrader or None): The automated trader instance, if one is running.
    """
    def __init__(self, view, start_menu_model, trading_data_fetcher, account_interaction_model, config_model):
        self.view = view
        self.view.update_button_text(None)  # None or an empty string to indicate no strategy is running
        self.model = start_menu_model
        self.trading_data_fetcher = trading_data_fetcher
        self.account_interaction_model = account_interaction_model
        self.config_model = config_model
        self.automated_trader = None
        try:
            self.strategies = self.load_strategies()
            self.setup_connections()
        except Exception as e:
            print(f"Error during controller initialization: {e}")

    def load_strategies(self):
        try:
            return self.config_model.load_trading_config()
        except Exception as e:
            print(f"Error loading strategies: {e}")
            return []

    def setup_connections(self):
        try:
            # Ensure each button is connected to toggle_automated_trading with the correct strategy
            for strategy in self.strategies:
                button = self.view.buttons[strategy['name']]
                # Use partial to correctly capture the current strategy in the lambda function
                button.clicked.connect(partial(self.toggle_automated_trading, strategy))

            # Connect the strategy_selected signal to update_button_text
            self.view.strategy_selected.connect(self.view.update_button_text)
            self.view.pnl_button.clicked.connect(self.handle_fetch_pnl)
            self.view.cancel_orders_requested.connect(self.handle_close_positions)
            self.view.fetch_positions_requested.connect(self.handle_open_positions)


        except Exception as e:
            print(f"Error setting up connections: {e}")

    def toggle_automated_trading(self, strategy):
        try:
            # Access the current_strategy directly, not as a callable
            current_strategy_name = self.view.current_strategy

            if self.automated_trader and self.automated_trader.is_alive():
                # If the strategy is running and the clicked strategy is the same as the running one, stop it.
                if current_strategy_name == strategy['name']:
                    print(f"Stopping {current_strategy_name}")
                    self.stop_automated_trading()
                    self.view.strategy_selected.emit(None)  # Signal that no strategy is running
                else:
                    print(
                        f"Strategy {current_strategy_name} is already running. To start a new strategy, stop the running one first.")
            else:
                # If no strategy is running, start the clicked strategy.
                if current_strategy_name != strategy['name']:
                    print(f"Starting {strategy['name']}")
                    self.start_automated_trading(strategy)
                # Else, it means we have successfully stopped a strategy, so we don't need to start another one.

        except Exception as e:
            print(f"Error toggling trading for {strategy['name']}: {e}")

    def start_automated_trading(self, strategy):
        try:
            print(f"Starting automated trading for {strategy['name']}")
            self.model.set_current_strategy(strategy)
            if self.automated_trader:
                print("Existing trader found. Stopping it before starting a new one.")
                self.automated_trader.stop_trading()
                self.automated_trader.join()

            self.automated_trader = AutomatedTrader(
                start_menu_model=self.model,
                trading_data_fetcher=self.trading_data_fetcher,
                account_interaction_model=self.account_interaction_model
            )
            self.automated_trader.start()
            self.view.update_button_text(strategy['name'])
        except Exception as e:
            print(f"Error starting automated trading for {strategy['name']}: {e}")

    def stop_automated_trading(self):
        try:
            if self.automated_trader:
                self.automated_trader.stop_trading()
                self.automated_trader.join()
                if not self.automated_trader.is_alive():
                    print("Trader thread has successfully stopped.")
                else:
                    print("Trader thread did not stop as expected.")
                self.automated_trader = None
                self.view.strategy_selected.emit(None)
                print("Automated trading has been successfully stopped.")
        except Exception as e:
            print(f"Error stopping automated trading: {e}")

    def handle_fetch_pnl(self):
        symbol = 'BTCUSDT'  # Assuming you want to fetch PnL for BTCUSDT
        try:
            closed_pnl_data = self.model.fetch_closed_pnl(symbol, self.account_interaction_model)
            if closed_pnl_data is not None and 'list' in closed_pnl_data:
                # Sum the 'closedPnl' field from each item in the 'list'
                total_closed_pnl = sum(float(item['closedPnl']) for item in closed_pnl_data['list'])
                self.view.display_pnl(total_closed_pnl)
            else:
                self.view.display_error("Failed to fetch closed PnL.")
        except Exception as e:
            print(f"Error fetching PnL: {e}")
            self.view.display_error("Error fetching closed PnL.")

    def handle_close_positions(self):
        # Replace with the actual symbol if needed
        try:
            # Attempt to close all positions for the symbol
            success = self.model.close_all_positions(self.account_interaction_model)
            if success:
                self.view.show_message("All positions have been closed.")
            else:
                self.view.show_message("Failed to close positions.")
        except Exception as e:
            self.view.show_message(f"Error occurred: {str(e)}")

    def handle_open_positions(self):
        try:
            # Define the symbol for which positions are to be fetched
            symbol = 'BTCUSDT'

            # Fetch open positions from the model
            positions = self.model.fetch_open_positions(symbol, self.account_interaction_model)

            # Check if positions are returned and display them, otherwise show a message
            if positions:
                self.view.display_positions(positions)
            else:
                self.view.show_message("No open positions available.")
        except Exception as e:
            # If an error occurs, log the error and display a message to the user
            print(f"Error occurred while handling open positions: {e}")
            self.view.show_message("Failed to retrieve open positions.")
