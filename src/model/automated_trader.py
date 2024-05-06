import time
from threading import Thread


class AutomatedTrader(Thread):
    """
    A threaded trader class designed to automate trading operations at a specified interval, integrating trading
    data fetching, trade execution, and account interaction into its lifecycle.

    Attributes:
        start_menu_model (object): An instance of StartMenuModel used for executing trading strategies.
        trading_data_fetcher (object): An instance responsible for fetching trading data.
        account_interaction_model (object): An instance handling direct interaction with the trading account.
        interval (int): The time interval in seconds between trade checks. Default is 3600 seconds (1 hour).
        running (bool): Flag to control the running of the thread. Set to False to stop the thread.
        wait_after_trade (bool): A flag to indicate if a waiting period is activated after a trade.
    """
    def __init__(self, start_menu_model, trading_data_fetcher, account_interaction_model, interval=3600):
        super(AutomatedTrader, self).__init__()
        self.start_menu_model = start_menu_model
        self.trading_data_fetcher = trading_data_fetcher
        self.account_interaction_model = account_interaction_model
        self.interval = interval
        self.running = True
        self.wait_after_trade = False

    def run(self):
        print("Trader thread started running.")
        while self.running:
            try:
                self.handle_trading_cycle()
            except Exception as e:
                print(f"An error occurred in run method: {e}")
                self.interruptible_sleep(300)  # Sleep for 5 minutes before retrying

    def handle_trading_cycle(self):
        print("Attempting to fetch server time...")
        server_time = self.get_server_time_with_retry()

        if server_time:
            sleep_time = self.calculate_sleep_time(server_time)
            if sleep_time < 600:
                print(f"New hour starts in less than 10 minutes. Sleeping for {sleep_time} seconds...")
                self.interruptible_sleep(sleep_time)
            else:
                print("More than 10 minutes to the new hour, performing trade check now.")
                self.perform_trade_check()

            if self.wait_after_trade and self.running:
                print("Waiting period active after trade. Skipping trade check this cycle.")
            elif self.running:
                self.perform_trade_check()
                self.interruptible_sleep(60)
        else:
            print("Server time could not be fetched, sleeping for default interval.")
            self.interruptible_sleep(self.interval)

    def get_server_time_with_retry(self):
        try:
            server_time = self.account_interaction_model.get_server_time()
            if server_time:
                print(f"Server time fetched: {server_time}")
                return int(server_time)
        except Exception as e:
            print(f"Failed to fetch server time: {e}")
        return None

    def calculate_sleep_time(self, server_time):
        current_time = server_time
        next_hour = (current_time // 3600 + 1) * 3600
        return next_hour - current_time

    def perform_trade_check(self):
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print(f"Performing trade check at {current_time}")

        if not self.account_interaction_model.get_open_orders('BTCUSDT'):
            input_data = self.start_menu_model.fetch_and_process_data(self.trading_data_fetcher)
            if input_data is not None:
                trade_executed = self.start_menu_model.predict_and_execute_trade(
                    input_data, self.trading_data_fetcher, self.account_interaction_model)
                if trade_executed:
                    print("Trade executed successfully. Activating 15 minutes wait.")
                    self.wait_after_trade = True
                    self.interruptible_sleep(900)  # Wait for 15 minutes
                    self.wait_after_trade = False
                else:
                    print("No trade executed. Checking again in next cycle.")
                    self.interruptible_sleep(60)  # Wait for 1 minute before the next cycle
            else:
                print("No input data available for trading.")
                self.interruptible_sleep(60)  # Wait for 1 minute before the next cycle

    def interruptible_sleep(self, duration):
        start_time = time.time()
        while self.running and time.time() - start_time < duration:
            time.sleep(0.5)  # Ensure quick wake-up to check `self.running`

    def stop_trading(self):
        if self.running:
            self.running = False
            print("Stopping trading...")
