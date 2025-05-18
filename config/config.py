import os 
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")

TESTNET_URL = 'https://testnet.binance.vision/api'
SYMBOL = "BTCUSDT"

COLUMNS = ['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'number_of_trades', 
'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore']

