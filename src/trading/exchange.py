from binance.client import Client
from config.config import API_KEY, SECRET_KEY, TESTNET_URL

client = Client(API_KEY, SECRET_KEY, testnet=True)
client.API_URL = TESTNET_URL  


