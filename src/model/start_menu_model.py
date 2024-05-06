import numpy as np
from keras.models import load_model
from pybit.unified_trading import HTTP
from sklearn.preprocessing import MinMaxScaler

from src.model.indicators import Indicators


class StartMenuModel:

    def __init__(self, config_model):
        """
        Parameters:
            config_model (object): Configuration model containing necessary API keys and other settings.

        Attributes:
            scaler (MinMaxScaler): Scaler for normalizing data.
            config_model (object): Stores the configuration model.
            model (keras model): Loaded machine learning model for price prediction.
            session (HTTP): Trading session for executing trades.
            current_strategy (dict): Currently active trading strategy.
        """
        try:
            self.scaler = MinMaxScaler(feature_range=(0, 1))
            self.config_model = config_model
            self.model = load_model('ml_model/my_model.h5')
            self.session = HTTP(testnet=True, api_key=self.config_model.api_key,
                                api_secret=self.config_model.api_secret)
            self.current_strategy = None
            print("Model and session initialized successfully.")
        except Exception as e:
            print(f"Error initializing StartMenuModel: {e}")

    def set_current_strategy(self, strategy):
        """
        Parameters:
            strategy (dict): A dictionary containing strategy settings.
        """
        self.current_strategy = strategy

    def predict_next_price(self, data):
        """
        Parameters:
            data (array): Input data for the model, usually the latest trading data.
        Returns:
            float: Predicted price or None if prediction fails.
        """
        try:
            prediction = self.model.predict(data)
            print(f"Prediction output: {prediction}")
            return prediction[0][0]
        except Exception as e:
            print(f"Error in prediction: {e}")
            return None

    def fetch_and_process_data(self, trading_data_fetcher):
        """
        Parameters:
            trading_data_fetcher (object): A data fetching object capable of retrieving trading data.

        Returns:
            array: Processed and scaled data ready for prediction or None if fetching fails or insufficient data.
        """
        try:
            df = trading_data_fetcher.fetch_data()
            if df.empty:
                print("Fetched data is empty.")
                return None

            if df.shape[0] < 40:
                print(f"Not enough data to form a sequence for prediction. Required: 40, Available: {df.shape[0]}")
                return None

            scaled_data = self.scaler.fit_transform(
                df.iloc[-40:][['open', 'high', 'low', 'close', 'volume', 'turnover', 'SMA_5', 'SMA_10']])
            scaled_data = scaled_data.reshape(1, 40, 8)
            return scaled_data
        except Exception as e:
            print(f"Error fetching or processing data: {e}")
            return None

    def predict_and_execute_trade(self, input_data, trading_data_fetcher, account_interaction_model):
        """
        Parameters:
            input_data (array): Scaled and processed input data for the prediction model.
            trading_data_fetcher (object): Data fetcher used for retrieving the last known BTC price.
            account_interaction_model (object): Model used for account interactions and trading execution.

        Returns:
            bool: True if the trade was successfully executed, False otherwise.
        """
        try:
            predicted_scaled_price = self.predict_next_price(input_data)
            if predicted_scaled_price is not None:
                last_price = trading_data_fetcher.fetch_last_btc_price()
                if last_price is not None:
                    dummy_array = np.zeros((1, 8))
                    dummy_array[0, 3] = predicted_scaled_price
                    predicted_price = self.scaler.inverse_transform(dummy_array)[0, 3]
                    return self.make_trade_decision(predicted_price, last_price, account_interaction_model,
                                                    trading_data_fetcher)
            return False
        except Exception as e:
            print(f"Error during prediction or trading execution: {e}")
            return False

    def make_trade_decision(self, predicted_price, last_price, account_interaction_model, trading_data_fetcher):
        """
        Parameters:
            predicted_price (float): The price predicted by the model.
            last_price (float): The last known trading price of BTC.
            account_interaction_model (object): Model used for account interactions such as balance checks and order placement.
            trading_data_fetcher (object): Data fetcher used for retrieving the latest data and trading indicators.

        Returns:
            bool: True if a trade decision is made and executed, False otherwise.
        """
        if not self.current_strategy:
            print("No trading strategy is set.")
            return False
        try:
            df = trading_data_fetcher.fetch_data()  # Assuming this returns the latest data
            if df is None:
                print("Failed to retrieve data for indicators.")
                return False

            # Check indicators
            indicator = Indicators(df)
            signals = self.check_trading_signals(df)

            # Example strategy: Increase take profit if any indicator signals a strong buy or sell
            strong_buy = any(signals[key] == 'Buy' for key in signals)
            strong_sell = any(signals[key] == 'Sell' for key in signals)

            # Print positive indicator signals
            if strong_buy or strong_sell:
                positive_signals = {key: signals[key] for key in signals if signals[key] in ['Buy', 'Sell']}
                print(f"Positive signals detected: {positive_signals}")

            balance = float(account_interaction_model.get_usdt_balance())
            leverage = float(self.current_strategy['leverage'])
            account_interaction_model.set_leverage('BTCUSDT', str(leverage))
            balance_percentage = float(self.current_strategy['balance_percentage'])

            qty = ((balance * balance_percentage) / last_price) * leverage
            qty = max(round(qty, 3), 0.001)

            print(f'Quantity: {qty}, Comparing predicted price {predicted_price} with last price {last_price}')

            side = 'Buy' if predicted_price > last_price else 'Sell'

            # Adjust take profit based on indicator signals
            take_profit_multiplier = 2 if strong_buy or strong_sell else 1

            self.place_order(side, qty, last_price, take_profit_multiplier)
            return True

        except Exception as e:
            print(f"Error making trade decision: {e}")
            return False

    def place_order(self, side, qty, last_price, take_profit_multiplier=1):
        if not self.current_strategy:
            print("No trading strategy is set for placing an order.")
            return
        try:
            stop_loss_percentage = self.current_strategy['risk_management']['stop_loss']
            take_profit_percentage = self.current_strategy['risk_management']['take_profit'] * take_profit_multiplier

            stop_loss_price = last_price * (1 - stop_loss_percentage) if side == 'Buy' else last_price * (
                    1 + stop_loss_percentage)
            take_profit_price = last_price * (1 + take_profit_percentage) if side == 'Buy' else last_price * (
                    1 - take_profit_percentage)

            response = self.session.place_order(
                category="linear",
                symbol="BTCUSDT",
                side=side,
                orderType="Market",
                qty=str(qty),
                timeInForce="GoodTillCancel",
                stop_loss=str(round(stop_loss_price, 2)),
                take_profit=str(round(take_profit_price, 2))
            )
            print(f"Order placed: {response}")
        except Exception as e:
            print(f"Error placing order: {e}")

    def fetch_closed_pnl(self, symbol, account_interaction_model):
        return account_interaction_model.get_closed_pnl(symbol)

    def fetch_open_positions(self, symbol, account_interaction_model):
        return account_interaction_model.get_positions(symbol)

    def close_all_positions(self, account_interaction_model):
        try:
            response = account_interaction_model.get_positions(symbol='BTCUSDT')
            if 'list' in response:
                open_positions = response['list']
                if not open_positions:
                    print("No open positions to close.")
                    return True

                for position in open_positions:
                    symbol = position['symbol']
                    qty = float(position['size'])
                    if qty <= 0:
                        print(f"Skipping position for {symbol} due to zero size.")
                        continue

                    side = 'Sell' if position['side'] == 'Buy' else 'Buy'
                    try:
                        close_response = account_interaction_model.place_reduce_only_order(
                            symbol=symbol, qty=qty, side=side)
                        if close_response and close_response.get('retCode', 1) != 0:
                            error_msg = close_response.get('retMsg', 'No error message available')
                            print(f"Failed to close position for {symbol}: {error_msg}")
                            return False
                    except Exception as e:
                        print(f"Exception when placing reduce-only order for {symbol}: {e}")
                        return False

                print("All positions closed successfully.")
                return True
            else:
                print("Failed to fetch open positions: No 'list' found in response")
                return False
        except Exception as e:
            print(f"Exception when trying to close all positions: {e}")
            return False

    def check_trading_signals(self, df):
        indicator = Indicators(df)
        signals = {}
        try:
            # MACD signal
            macd, signal, _ = indicator.moving_average_convergence_divergence()
            signals['MACD'] = 'Buy' if (macd.iloc[-1] > signal.iloc[-1]) and (
                    macd.iloc[-2] < signal.iloc[-2]) else 'Sell'
        except Exception as e:
            print(f"Error calculating MACD: {e}")

        try:
            # RSI signal
            rsi = indicator.relative_strength_index()
            signals['RSI'] = 'Buy' if rsi.iloc[-1] < 30 else 'Sell' if rsi.iloc[-1] > 70 else 'Hold'
        except Exception as e:
            print(f"Error calculating RSI: {e}")

        try:
            # CCI signal
            cci = indicator.commodity_channel_index()
            signals['CCI'] = 'Buy' if cci.iloc[-1] < -100 else 'Sell' if cci.iloc[-1] > 100 else 'Hold'
        except Exception as e:
            print(f"Error calculating CCI: {e}")

        try:
            # Stochastic Oscillator signal
            k, d = indicator.stochastics_oscillator()
            signals['Stochastic'] = 'Buy' if (k.iloc[-1] < 20) and (k.iloc[-1] > d.iloc[-1]) else 'Sell' if (k.iloc[
                                                                                                                 -1] > 80) and (
                                                                                                                    k.iloc[
                                                                                                                        -1] <
                                                                                                                    d.iloc[
                                                                                                                        -1]) else 'Hold'
        except Exception as e:
            print(f"Error calculating Stochastic Oscillator: {e}")

        try:
            # Bollinger Bands signal
            upper, middle, lower = indicator.bollinger_bands()
            signals['Bollinger'] = 'Sell' if df['close'].iloc[-1] > upper.iloc[-1] else 'Buy' if df['close'].iloc[-1] < \
                                                                                                 lower.iloc[
                                                                                                     -1] else 'Hold'
        except Exception as e:
            print(f"Error calculating Bollinger Bands: {e}")

        try:
            # Momentum signal
            momentum = indicator.momentum()
            signals['Momentum'] = 'Buy' if momentum.iloc[-1] > 0 else 'Sell'
        except Exception as e:
            print(f"Error calculating Momentum: {e}")

        try:
            # Rate of Change signal
            roc = indicator.rate_of_change()
            signals['ROC'] = 'Buy' if roc.iloc[-1] > 0 else 'Sell'
        except Exception as e:
            print(f"Error calculating ROC: {e}")

        try:
            # On-Balance Volume signal
            obv = indicator.on_balance_volume()
            signals['OBV'] = 'Buy' if obv[-1] > obv[-2] else 'Sell'
        except Exception as e:
            print(f"Error calculating OBV: {e}")

        return signals
