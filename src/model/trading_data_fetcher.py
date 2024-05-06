import pandas as pd
from pybit.unified_trading import HTTP


class TradingDataFetcher:
    """
    A class responsible for fetching trading data from an API using a given configuration model.
    """

    def __init__(self, config_model):
        """
        Initializes the TradingDataFetcher instance with configuration settings.

        Parameters:
            config_model (ConfigModel): Configuration model containing API key and secret.

        Attributes:
            session (HTTP): An HTTP session for API requests. Initialized based on provided API key and secret.
        """
        self.config_model = config_model
        try:
            self.session = HTTP(testnet=True, api_key=self.config_model.api_key,
                                api_secret=self.config_model.api_secret)
        except Exception as e:
            print(f"Failed to initialize HTTP session: {e}")
            self.session = None

    def fetch_data(self, symbol='BTCUSDT', interval='60', limit=60):
        """
        Fetches trading data for a specified symbol and interval.

        Parameters:
            symbol (str): Trading symbol to fetch data for. Defaults to 'BTCUSDT'.
            interval (str): Time interval in minutes for the klines. Defaults to '60'.
            limit (int): Number of data points to return. Defaults to 60.

        Returns:
            DataFrame: A DataFrame containing the trading data, or an empty DataFrame if an error occurs.
        """
        if not self.session:
            print("HTTP session not initialized.")
            return pd.DataFrame()
        try:
            response = self.session.get_kline(category='linear', symbol=symbol, limit=limit, interval=interval).get(
                'result')
            if response:
                return self.format_data(response)
            else:
                print("Empty response from API.")
                return pd.DataFrame()
        except Exception as e:
            print(f"Failed to fetch data: {e}")
            return pd.DataFrame()

    def format_data(self, response):
        """
        Converts API response into a formatted DataFrame.

        Parameters:
            response (dict): The raw response from the API containing trading data.

        Returns:
            DataFrame: A DataFrame formatted from the API response, or an empty DataFrame if an error occurs.
        """
        if 'list' not in response or not response['list']:
            print("No 'list' in response or 'list' is empty.")
            return pd.DataFrame()

        try:
            df = pd.DataFrame(response['list'],
                              columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'turnover'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            df.set_index('timestamp', inplace=True)
            df = df.apply(pd.to_numeric, errors='coerce')
            df['SMA_5'] = df['close'].rolling(window=5).mean()
            df['SMA_10'] = df['close'].rolling(window=10).mean()
            df.dropna(inplace=True)
            return df.iloc[10:]  # Skip the oldest 10 intervals
        except Exception as e:
            print(f"Failed to format data: {e}")
            return pd.DataFrame()

    def fetch_last_btc_price(self, symbol='BTCUSDT', interval='1'):
        """
        Fetches the most recent closing price of Bitcoin.

        Parameters:
            symbol (str): Trading symbol, default is 'BTCUSDT'.
            interval (str): Time interval for the kline, default is '1' minute.

        Returns:
            float or None: The most recent closing price of Bitcoin, or None if an error occurs.
        """
        if not self.session:
            print("HTTP session not initialized.")
            return None
        try:
            response = self.session.get_kline(category='linear', symbol=symbol, limit=1, interval=interval).get(
                'result')
            if response and 'list' in response and response['list']:
                last_data_point = response['list'][0]
                last_price = float(last_data_point[4])
                return last_price
            else:
                print("No data received or incorrect data format.")
                return None
        except Exception as e:
            print(f"Failed to fetch last BTC price: {e}")
            return None
