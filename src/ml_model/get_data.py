import datetime as dt
import time

import pandas as pd
from pybit.unified_trading import HTTP

# Session initialization
session = HTTP(api_key="ussjsEk1NyHm57ambu", api_secret="1Rqw5ZV6rqUudgvL2bkwf0tQhUE7ToUZvQ6q", testnet=True)


def format_data(response):
    '''
    Formats raw kline data from response to a pandas DataFrame.
    '''
    data = response.get('list', None)
    if not data:
        return

    try:
        data = pd.DataFrame(data,
                            columns=[
                                'timestamp',
                                'open',
                                'high',
                                'low',
                                'close',
                                'volume',
                                'turnover'
                            ])
        data['timestamp'] = pd.to_datetime(data['timestamp'], unit='ms', utc=True)
        data.set_index('timestamp', inplace=True)
        data = data[::-1].apply(pd.to_numeric)
        return data
    except Exception as e:
        print(f"Error formatting data: {e}")
        return pd.DataFrame()


def get_last_timestamp(df):
    try:
        return int(df.index[-1].timestamp() * 1000)
    except Exception as e:
        print(f"Error getting last timestamp: {e}")
        return None


start = int(dt.datetime(2017, 1, 1).timestamp() * 1000)
interval = 60
symbol = 'BTCUSDT'
df = pd.DataFrame()

while True:
    try:
        response = session.get_kline(category='linear', symbol=symbol, start=start, interval=interval).get('result')
        latest = format_data(response)

        if not isinstance(latest, pd.DataFrame) or latest.empty:
            print("No new data or failed to fetch data.")
            break

        start = get_last_timestamp(latest)
        if start is None:
            break

        time.sleep(0.1)  # Delay to prevent API rate limit issues

        df = pd.concat([df, latest])
        print(f'Collecting data starting {dt.datetime.fromtimestamp(start / 1000)}')

        if len(latest) == 1:
            break
    except Exception as e:
        print(f"Error during data collection loop: {e}")
        break

if not df.empty:
    df['SMA_5'] = df['close'].rolling(window=5).mean()
    df['SMA_10'] = df['close'].rolling(window=10).mean()
    df.dropna(inplace=True)
    df.drop_duplicates(subset=['timestamp'], keep='last', inplace=True)
    df.to_csv('new_BTCSDT_1h_data_since_2020.csv', index=True)
    print("Data collection complete and saved to CSV.")
else:
    print("No data collected.")
