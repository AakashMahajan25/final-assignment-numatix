import pandas as pd
from binance.client import Client
from config.config import API_KEY, SECRET_KEY, COLUMNS

client = Client(API_KEY, SECRET_KEY, testnet=True)

def fetch_binance_data_15m(symbol):
    data_live = client.get_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_15MINUTE)
    df_live = pd.DataFrame(data_live, columns=COLUMNS)
    df_live['timestamp'] = pd.to_datetime(df_live['timestamp'], unit='ms')
    df_live.set_index('timestamp', inplace=True)
    df_live = df_live.astype(float)
    return df_live[['open', 'high', 'low', 'close', 'volume']]

def fetch_binance_data_1h(symbol):
    data_live = client.get_klines(symbol=symbol, interval=Client.KLINE_INTERVAL_1HOUR)
    df_live = pd.DataFrame(data_live, columns=COLUMNS)
    df_live['timestamp'] = pd.to_datetime(df_live['timestamp'], unit='ms')
    df_live.set_index('timestamp', inplace=True)
    df_live = df_live.astype(float)
    return df_live[['open', 'high', 'low', 'close', 'volume']]