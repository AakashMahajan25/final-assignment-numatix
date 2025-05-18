from backtesting import Backtest
from .LiveStrategy import LiveStrategy
from backtesting.lib import crossover
import pandas as pd
import os
from src.trading.exchange import client

class LatestStrategy(LiveStrategy):
    data_1hr = None  

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client = client
        self.symbol = "BTCUSDT"  

    @staticmethod
    def EMA(series, window):
        return pd.Series(series).ewm(span=window, adjust=False).mean()

    def init(self):
        self.ema_15m_1 = self.I(self.EMA, self.data.Close, 9)
        self.ema_15m_2 = self.I(self.EMA, self.data.Close, 21)

        if self.data_1hr is not None:
            aligned_1h = self.data_1hr.reindex(self.data.index, method='ffill')
            self.ema_1h = self.I(self.EMA, aligned_1h.Close, 50)
        else:
            self.ema_1h = None

    def next(self):
        if crossover(self.ema_15m_1,self.ema_15m_2) and self.data_1hr.Close[-1] > self.ema_1h[-1]:
            self.position.close()
            self.buy()
        elif crossover(self.ema_15m_2,self.ema_15m_1) and self.data_1hr.Close[-1] < self.ema_1h[-1]:
            self.position.close()
            self.sell()


def to_ohlcv(series):
        df = pd.DataFrame({
            'Open': series,
            'High': series,
            'Low': series,
            'Close': series,
        }, index=series.index)
        return df


def run_live_strategy(data_15m, data_1h, strategy_class=LatestStrategy): 
    strategy_class.data_1hr = data_1h
    bt = Backtest(data_15m, strategy_class, cash=1_000_000, commission=0.001)
    stats = bt.run()

    trades = pd.DataFrame(stats['_trades'])
    bt.plot()
    if not os.path.exists('data'):
        os.makedirs('data')
    trades.to_csv('data/backtest_trades.csv', index=False)

    return stats