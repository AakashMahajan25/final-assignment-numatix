from src.utils.data import fetch_binance_data_15m, fetch_binance_data_1h
from src.backtesting.backtest import run_live_strategy, LatestStrategy
import os, time
from src.utils.logger import setup_logger
from config.config import SYMBOL

logger = setup_logger()

if not os.path.exists('data'):
    os.makedirs('data')

SYMBOL = "BTCUSDT"

def start_live_trading():
    try:
        # Fetch data
        df_15m = fetch_binance_data_15m(SYMBOL)
        df_15m.columns = [col.capitalize() for col in df_15m.columns]
        df_1h = fetch_binance_data_1h(SYMBOL)
        df_1h.columns = [col.capitalize() for col in df_1h.columns]

        # Run strategy with SYMBOL
        bt_results = run_live_strategy(df_15m, df_1h, LatestStrategy)
        logger.info(f"Backtesting results: {bt_results}")
        
    except Exception as e:
        logger.error(f"Error in live trading: {str(e)}")
        raise

if __name__ == "__main__":
    start_live_trading()
    



