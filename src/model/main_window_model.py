import pandas as pd
from pybit.unified_trading import HTTP

class MainWindowModel:
    """
    A model class that manages data fetching and processing for a main window interface
    using trading data from an API.

    Attributes:
        config_model (object): Configuration model containing API credentials and other settings.
        session (HTTP): A session for making API requests initialized with user credentials.
    """

    def __init__(self, config_model):
        """
        Initializes the MainWindowModel with a configuration model and sets up the API session.

        Parameters:
            config_model (object): Configuration model with necessary API keys for initialization.
        """
        self.config_model = config_model
        self.update_session()

    def update_session(self):
        """
        Initializes or updates the HTTP session for making API requests based on the configuration model.

        Handles exceptions by printing error messages if the session cannot be initialized.
        """
        try:
            self.session = HTTP(
                testnet=True,
                api_key=self.config_model.api_key,
                api_secret=self.config_model.api_secret
            )
        except Exception as e:
            print(f"Error initializing HTTP session: {e}")

    def fetch_data(self):
        """
        Fetches trading data for 'BTCUSDT' over a specified interval using the HTTP session.

        Returns:
            DataFrame: A pandas DataFrame containing formatted trading data,
                       or an empty DataFrame if data fetching fails or if data is in an incorrect format.
        """
        try:
            response = self.session.get_kline(symbol='BTCUSDT', interval='60', limit=168)
            print("API Response:", response)
            if response and 'result' in response and 'list' in response['result']:
                df = self.format_data(response['result']['list'])
                print("Formatted DataFrame:\n", df.head())
                return df
            else:
                print("No data or incorrect data format received from API.")
                return pd.DataFrame()
        except Exception as e:
            print(f"Failed to fetch data due to: {e}")
            return pd.DataFrame()

    def format_data(self, data):
        """
        Converts raw data from the API into a formatted pandas DataFrame.

        Parameters:
            data (list): Raw data list containing dictionaries of trading information.

        Returns:
            DataFrame: A pandas DataFrame with formatted and indexed trading data,
                       or an empty DataFrame if there are errors in formatting.
        """
        try:
            if not data:
                print("No data received for formatting.")
                return pd.DataFrame()

            df = pd.DataFrame(data, columns=[
                'timestamp', 'open', 'high', 'low', 'close', 'volume', 'turnover'
            ])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            df.set_index('timestamp', inplace=True)
            return df.apply(pd.to_numeric, errors='ignore')
        except Exception as e:
            print(f"Error formatting data: {e}")
            return pd.DataFrame()
