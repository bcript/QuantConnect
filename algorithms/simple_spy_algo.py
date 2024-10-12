# region imports
from AlgorithmImports import *
# endregion

class DeterminedBlueJellyfish(QCAlgorithm):

    def initialize(self):
        self.set_start_date(2023, 4, 11)
        self.set_end_date(2023, 5, 11)
        self.set_cash(100000)

        # ticker symbol
        spy = self.add_equity("SPY", Resolution.DAILY)

        spy.set_data_normalization_mode(DataNormalizationMode.RAW)

        self.spy = spy.symbol

        self.set_benchmark("SPY")
        # 2-4x leverage
        self.set_brokerage_model(BrokerageName.INTERACTIVE_BROKERS_BROKERAGE, AccountType.MARGIN)
        
        self.entryPrice = 0
        self.period = timedelta(31) # 31 days
        self.nextEntryTime = self.Time


    def on_data(self, data: Slice):
        if not self.spy in data:
            return 
        # current price of SPY (PD close price)
        price = data[self.spy].Close
        # price = data[self.spy] / price = self.Securities[self.spy].Close

        if not self.Portfolio.Invested:

            # 1 month holding time
            if self.nextEntryTime <= self.Time:
                # self.SetHoldings(self.spy, 1) # 1% of portfolio
                self.market_order(self.spy, int(self.Portfolio.Cash / price))
                self.Log("BUY SPY @" + str(price))
                self.entryPrice = price

        # check if 10% </> price
        elif self.entryPrice * 1.1 < price or self.entryPrice * 0.9 > price:
            self.liquidate()
            self.Log("SELL SPY @" + str(price))
            self.nextEntryTime = self.Time + self.period

