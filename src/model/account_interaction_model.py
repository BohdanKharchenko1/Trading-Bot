from pybit.unified_trading import HTTP


class AccountInteractionModel:
    """
    A model for interacting with a trading account through the Bybit API. It provides methods to manage trades,
    retrieve account details, and modify account settings.

    Attributes:
        config_model (object): A configuration object containing API keys and other necessary configurations.
        session (HTTP): An instance of HTTP from pybit used to make authenticated requests to the Bybit API.
    """
    def __init__(self, config_model):
        self.config_model = config_model
        try:
            self.session = HTTP(testnet=True, api_key=self.config_model.api_key,
                                api_secret=self.config_model.api_secret)
            print("HTTP session initialized successfully.")
        except Exception as e:
            print(f"Failed to initialize HTTP session: {e}")

    def get_usdt_balance(self):
        """
        Fetches the USDT balance from the Bybit account.
        """
        try:
            # Retrieve the wallet balance; assumes the method name and parameters align with the library's usage.
            response = self.session.get_wallet_balance(coin="USDT", accountType="UNIFIED")
            print(response)
            if response.get('retCode') == 0 and 'list' in response.get('result', {}):
                # Extracting the balance details from the response
                for coin_info in response['result']['list']:
                    if 'coin' in coin_info and isinstance(coin_info['coin'], list):
                        for coin in coin_info['coin']:
                            if coin['coin'] == 'USDT':
                                balance = coin['availableToWithdraw']
                                print(f"USDT Balance: {balance}")
                                return balance
            print(f"Failed to fetch USDT balance: {response.get('ret_msg', 'No error message received')}")
            return None
        except Exception as e:
            print(f"Exception when trying to fetch USDT balance: {e}")
            return None

    def set_leverage(self, symbol, leverage):
        """
        Sets the leverage for a specific symbol on the Bybit account.
        """
        try:
            # Assumes the method to set leverage is set_leverage in the API and accepts these parameters
            response = self.session.set_leverage(category='linear', symbol=symbol, buyLeverage=str(leverage),
                                                 sellLeverage=str(leverage))
            print(f'response {response}')
            if response.get('retCode') == 0:
                print(f"Leverage set successfully for {symbol} to {leverage}")
                return True
            else:
                print(f"Failed to set leverage: {response.get('ret_msg')}")
                return False
        except Exception as e:
            print(f"Exception when trying to set leverage: {e}")
            return False

    def get_open_orders(self, symbol):
        """
        Retrieves the open orders for the given symbol.
        """
        try:
            response = self.session.get_open_orders(symbol=symbol, category='linear')
            print(f"Open Orders: {response}")
            if response.get('retCode') == 0:
                return response['result']['list']  # Return the list of open orders
            else:
                return False  # Return an empty list if there are no open orders
        except Exception as e:
            print(f"Exception when trying to fetch open orders: {e}")
            return []  # Return an empty list in case of an exception

    def cancel_all_orders(self, symbol):
        """
        Cancels all open orders for a given symbol.
        """
        try:
            response = self.session.cancel_all_orders(symbol=symbol, category="linear")
            if response['retCode'] == 0:
                print(f"All orders cancelled for {symbol}.")
                return True
            else:
                print(f"Failed to cancel orders: {response['ret_msg']}")
                return False
        except Exception as e:
            print(f"Exception when trying to cancel all orders: {e}")
            return False

    def get_order_history(self, symbol):
        """
        Retrieves the order history for a given symbol.
        """
        try:
            response = self.session.get_order_history(symbol=symbol, category="linear")
            if response['retCode'] == 0:
                order_history = response['result']['data']
                print(f"Order History: {order_history}")
                return order_history
            else:
                print(f"Failed to get order history: {response['ret_msg']}")
                return None
        except Exception as e:
            print(f"Exception when trying to get order history: {e}")
            return None

    def get_closed_pnl(self, symbol):
        """
        Retrieves the closed profit and loss (PnL) for a given symbol.
        """
        try:
            # Replace 'get_closed_pnl' with the correct API endpoint method
            response = self.session.get_closed_pnl(symbol=symbol, category="linear")
            if response['retCode'] == 0:
                closed_pnl = response['result']
                print(f"Closed PnL: {closed_pnl}")
                return closed_pnl
            else:
                print(f"Failed to get closed PnL: {response['ret_msg']}")
                return None
        except Exception as e:
            print(f"Exception when trying to get closed PnL: {e}")
            return None

    def get_positions(self, symbol=None):
        """
        Retrieves the open positions for the given symbol or all symbols if none is specified.
        """
        try:
            # Replace 'get_positions' with the correct method name if it is different in the API
            if symbol:
                response = self.session.get_positions(symbol=symbol, category='linear')

            else:
                response = self.session.get_positions(
                    category="linear")  # This line is assuming that calling get_position without arguments returns all positions

            if response['retCode'] == 0:
                positions = response['result']
                print(f"Open Positions: {positions}")
                return positions
            else:
                print(f"Failed to get open positions: {response['retMsg']}")
                return None
        except Exception as e:
            print(f"Exception when trying to get open positions: {e}")
            return None

    def get_server_time(self):
        """
        Fetches the current server time from the Bybit API.
        """
        try:
            response = self.session.get_server_time()
            if response['retCode'] == 0:
                server_time = response['result']['timeSecond']  # The key for the server time in the response
                print(f"Server Time: {server_time}")
                return server_time
            else:
                print(f"Failed to fetch server time: {response.get('ret_msg')}")
                return None
        except Exception as e:
            print(f"Exception when trying to fetch server time: {e}")
            return None

    def place_reduce_only_order(self, symbol, qty, side):
        """
        Places a reduce-only order to close a position.
        """
        try:
            response = self.session.place_order(
                category='linear',
                symbol=symbol,
                side=side,
                order_type="Market",
                qty=qty,
                time_in_force="GoodTillCancel",
                reduce_only=True,
                close_on_trigger=True
            )
            if response.get('retCode') == 0:
                print(f"Order placed successfully for {symbol}")
            else:
                print(f"Failed to place order for {symbol}: {response.get('retMsg')}")
            return response
        except Exception as e:
            print(f"Exception when placing reduce-only order for {symbol}: {e}")
            return None
