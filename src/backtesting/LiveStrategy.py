from backtesting import Strategy
from src.trading.exchange import client
from src.utils.logger import log_trade_to_csv, setup_logger
from config.config import SYMBOL

logger = setup_logger()

class LiveStrategy(Strategy):
    def close_existing_positions(self):
        try:
            account_info = client.get_account()
            balances = account_info['balances']

            base_asset = SYMBOL.replace("USDT", "")  # e.g., BTC in BTCUSDT
            asset_balance = next((b for b in balances if b['asset'] == base_asset), None)

            if asset_balance:
                free_amount = float(asset_balance['free'])

                if free_amount > 0:
                    logger.info(f"Closing open BUY position of {free_amount} {base_asset}")
                    client.create_order(
                        symbol=self.symbol,
                        side="SELL",
                        type="MARKET",
                        quantity=free_amount
                    )
        except Exception as e:
            logger.error(f"Error closing existing positions: {e}")

    def buy(self, *, size=Strategy._FULL_EQUITY, **kwargs):
        self.close_existing_positions()
        order = super().buy(size=size, **kwargs)

        try:
            binance_order = client.create_order(
                symbol=self.symbol,
                side="BUY",
                type="MARKET",
                quantity=0.001
            )
            fill_price = float(binance_order['fills'][0]['price'])
            log_trade_to_csv(SYMBOL, "BUY", size, fill_price)

        except Exception as e:
            logger.error(f"Error placing BUY order on Binance: {e}")

        return order

    def sell(self, *, size=Strategy._FULL_EQUITY, **kwargs):
        self.close_existing_positions()
        order = super().sell(size=size, **kwargs)

        try:
            binance_order = client.create_order(
                symbol=self.symbol,
                side="SELL",
                type="MARKET",
                quantity=0.001
            )
            fill_price = float(binance_order['fills'][0]['price'])
            log_trade_to_csv(SYMBOL, "SELL", size, fill_price)

        except Exception as e:
            logger.error(f"Error placing SELL order on Binance: {e}")

        return order
