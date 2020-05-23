import numpy as np
import pandas as pd

class TechnicalIndicators:
    def __init__(self,access_open="open"):
        self.access_open = access_open
	#Exponential Moving Average / Period=12 annd Period=26, defined on MACD
    def EMA(self,prices, period=12):
        x = np.asarray(prices) #Make a vector, o prices ("close")
        weights = None
        weights = np.exp(np.linspace(-1., 0., period))
        weights /= weights.sum()

        a = np.convolve(x, weights, mode='full')[:len(x)]
        a[:period] = a[period]
        return a
    
    # Moving Average Convergence Divergence (MACD) #
    def MACD(self, price, nslow=26, nfast=12, nNine=9):
        emaslow = self.EMA(price, nslow)
        emafast = self.EMA(price, nfast)
        macd = emafast - emaslow
        macd_signal = self.EMA(macd, nNine)
        signal = macd - macd_signal
        #macd, macd_signal, signal,emaslow,emafast
        macd_df = pd.DataFrame({"macd":macd, "macd_signal":macd_signal, 
                                "signal":signal, "emaslow":emaslow,
                                "emafast":emafast})
        return macd_df

    # Relative strength index (RSI) #
    # From Tradingview : https://www.tradingview.com/wiki/Talk:Relative_Strength_Index_(RSI) #
    def RSI(self,price, period=14):
       delta = price.diff()
       delta.iloc[0]
       up, down = delta.copy(), delta.copy()
       up[up < 0.0] = 0.0
       down[down > 0.0] = 0.0

       roll_up1 = up.ewm(com=(period-1), min_periods=period).mean()
       roll_down1 = down.abs().ewm(com=(period-1), min_periods=period).mean()
       RS1 = roll_up1 / roll_down1
       RSI1 = 100.0 - (100.0 / (1.0 + RS1))
       return RSI1
