import numpy as np
import pandas as pd


class Indicators:
    """
    A class designed to compute various financial trading indicators from a given DataFrame containing
    historical stock or cryptocurrency price data.

    Attributes:
        data_frame (DataFrame): A pandas DataFrame containing columns like 'open', 'high', 'low', 'close', and 'volume'
                                which are necessary for calculating trading indicators.
    """

    def __init__(self, data_frame):
        """
        Initializes the Indicators class with a pandas DataFrame.

        Parameters:
            data_frame (DataFrame): The data frame containing trading data.
        """
        self.data_frame = data_frame

    def exponential_moving_average(self, window=14):
        """
        Calculates the Exponential Moving Average (EMA) of the 'close' price over a specified number of periods.

        Parameters:
            window (int): The span of the window for the EMA calculation, default is 14 periods.

        Returns:
            Series: A pandas Series containing the EMA values.
        """
        try:
            return self.data_frame['close'].ewm(span=window, adjust=False).mean()
        except Exception as e:
            print(f"Error calculating EMA: {e}")
            return pd.Series()

    def moving_average_convergence_divergence(self, slow=26, fast=12, signal=9):
        """
        Calculates the Moving Average Convergence Divergence (MACD) values.

        Parameters:
            slow (int): The number of periods for the slow EMA, default is 26.
            fast (int): The number of periods for the fast EMA, default is 12.
            signal (int): The number of periods for the signal line EMA, default is 9.

        Returns:
            tuple: A tuple containing three pandas Series (MACD line, signal line, and histogram).
        """
        try:
            ema_fast = self.exponential_moving_average(window=fast)
            ema_slow = self.exponential_moving_average(window=slow)
            macd = ema_fast - ema_slow
            macd_signal = macd.ewm(span=signal, adjust=False).mean()
            macd_histogram = macd - macd_signal
            return macd, macd_signal, macd_histogram
        except Exception as e:
            print(f"Error calculating MACD: {e}")
            return pd.Series(), pd.Series(), pd.Series()

    def relative_strength_index(self, window=14):
        """
        Calculates the Relative Strength Index (RSI) over a specified window.

        Parameters:
            window (int): The number of periods to calculate RSI, default is 14.

        Returns:
            Series: A pandas Series containing the RSI values.
        """
        try:
            delta = self.data_frame['close'].diff()
            gain = (delta.where(delta > 0, 0)).ewm(alpha=1 / window, adjust=False).mean()
            loss = (-delta.where(delta < 0, 0)).ewm(alpha=1 / window, adjust=False).mean()
            rs = gain / loss
            return 100 - (100 / (1 + rs))
        except Exception as e:
            print(f"Error calculating RSI: {e}")
            return pd.Series()

    def bollinger_bands(self, window=20, num_of_std=2):
        """
        Calculates the Bollinger Bands for the 'close' price.

        Parameters:
            window (int): The number of periods for the moving average.
            num_of_std (int): The number of standard deviations for the upper and lower bands.

        Returns:
            tuple: A tuple containing three pandas Series (upper band, moving average, lower band).
        """
        try:
            ma = self.data_frame['close'].rolling(window=window).mean()
            std = self.data_frame['close'].rolling(window=window).std()
            upper_band = ma + (std * num_of_std)
            lower_band = ma - (std * num_of_std)
            return upper_band, ma, lower_band
        except Exception as e:
            print(f"Error calculating Bollinger Bands: {e}")
            return pd.Series(), pd.Series(), pd.Series()

    def average_true_range(self, window=14):
        """
        Calculates the Average True Range (ATR) which measures market volatility.

        Parameters:
            window (int): The number of periods to calculate ATR, default is 14.

        Returns:
            Series: A pandas Series containing the ATR values.
        """
        try:
            high_low = self.data_frame['high'] - self.data_frame['low']
            high_close = np.abs(self.data_frame['high'] - self.data_frame['close'].shift())
            low_close = np.abs(self.data_frame['low'] - self.data_frame['close'].shift())
            tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
            return tr.rolling(window=window).mean()
        except Exception as e:
            print(f"Error calculating ATR: {e}")
            return pd.Series()

    def commodity_channel_index(self, window=20):
        """
        Calculates the Commodity Channel Index (CCI) which identifies cyclical trends.

        Parameters:
            window (int): The number of periods for the CCI calculation, default is 20.

        Returns:
            Series: A pandas Series containing the CCI values.
        """
        try:
            tp = (self.data_frame['high'] + self.data_frame['low'] + self.data_frame['close']) / 3
            ma = tp.rolling(window=window).mean()
            md = (tp - ma).abs().rolling(window=window).mean()
            cci = (tp - ma) / (0.015 * md)
            return cci
        except Exception as e:
            print(f"Error calculating CCI: {e}")
            return pd.Series()

    def stochastics_oscillator(self, k_window=14, d_window=3):
        """
        Calculates the Stochastic Oscillator, a momentum indicator comparing a particular closing price
        of a security to a range of its prices over a certain period of time.

        Parameters:
            k_window (int): The number of periods for the %K line calculation, default is 14.
            d_window (int): The number of periods for the %D line (moving average of %K), default is 3.

        Returns:
            tuple: A tuple containing two pandas Series (%K line, %D line).
        """
        try:
            low_min = self.data_frame['low'].rolling(window=k_window).min()
            high_max = self.data_frame['high'].rolling(window=k_window).max()
            k_percent = 100 * ((self.data_frame['close'] - low_min) / (high_max - low_min))
            d_percent = k_percent.rolling(window=d_window).mean()
            return k_percent, d_percent
        except Exception as e:
            print(f"Error calculating Stochastics Oscillator: {e}")
            return pd.Series(), pd.Series()

    def momentum(self, window=10):
        """
        Calculates the Momentum, which is the difference in the 'close' price over a specified number of periods.

        Parameters:
            window (int): The number of periods over which to calculate momentum, default is 10.

        Returns:
            Series: A pandas Series containing the momentum values.
        """
        try:
            return self.data_frame['close'].diff(periods=window)
        except Exception as e:
            print(f"Error calculating Momentum: {e}")
            return pd.Series()

    def rate_of_change(self, periods=14):
        """
        Calculates the Rate of Change (ROC), which measures the percentage change in price between the current price
        and the price a certain number of periods ago.

        Parameters:
            periods (int): The number of periods to calculate the rate of change, default is 14.

        Returns:
            Series: A pandas Series containing the ROC values.
        """
        try:
            return self.data_frame['close'].pct_change(periods=periods) * 100
        except Exception as e:
            print(f"Error calculating Rate of Change: {e}")
            return pd.Series()

    def on_balance_volume(self):
        """
        Calculates the On Balance Volume (OBV), an indicator that uses volume flow to predict changes in stock price.

        Returns:
            array: An array representing the cumulative total of volume adjusted based on whether the closing price
                   was up or down compared to the previous period.
        """
        try:
            # Calculate the On Balance Volume
            obv = np.where(self.data_frame['close'] > self.data_frame['close'].shift(1),
                           self.data_frame['volume'],  # Condition if True: use volume
                           -self.data_frame['volume']  # Condition if False: use negative volume
                           ).cumsum()  # Cumulatively sum up the true/false assigned volumes

            return obv
        except Exception as e:
            print(f"Error calculating OBV: {e}")
            return pd.Series()

