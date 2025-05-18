import logging
import csv
import os
from datetime import datetime, UTC

# Configure logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def setup_logger():
    return logger

def log_trade_to_csv(symbol, side, quantity, price, filename="data/live_trades.csv"):
    if not os.path.exists("data"):
        os.makedirs("data")

    file_exists = os.path.isfile(filename)

    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['timestamp', 'symbol', 'side', 'quantity', 'price'])
        writer.writerow([datetime.now(UTC), symbol, side, quantity, price])
        logger.info(f"Trade logged: {symbol}, {side}, Qty: {quantity}, Price: {price}")
