######### Functions from other python files #########
from Poloniex import poloniex,createTimeStamp
from Technical import TechnicalIndicators
#########

from time import gmtime, strftime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# <API Key>, <Secret Key>, to connect with Poloniex API
source_API = poloniex("API Key","Secret Key")

###### Simulation ######

def MACD_RSI_SIMULATION(market_currency,trade_currency, data_range_time, periodic):
    # Parameters 
    strategy = TechnicalIndicators()
    macd_fast = 12
    macd_slow = 26
    rsi_period = 14
    rsi_upper = 70
    rsi_down = 30
    nNine = 9 
    
    # As starting position for market transactions #
    willing_position = "buy"

    # To prepare data for simulation #
    currency_pair = market_currency + "_" + trade_currency
    end_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    start_time_days = int(createTimeStamp(end_time)) - data_range_time
    
    if source_API.returnChartData(currency_pair,start_time_days,periodic) =={'error': 'Invalid currency pair.'}:
        print("Invalid currency pair")      
        
    chart_data = pd.DataFrame(source_API.returnChartData(currency_pair,start_time_days,periodic))
    price = chart_data['close'].rename(market_currency + "-" + trade_currency)
    
    macd = strategy.MACD(price,macd_slow,macd_fast,nNine)
    macdSignal = macd["signal"]
    macdSignal_position = macd["macd"]
    
    rsi = strategy.RSI(price,rsi_period)
    rsi.iloc[0]

    trade_position = np.array(["none"]*len(price))
    
    # Create historical steps when strategy was willing to buy either sell position #
    for i in range(len(trade_position)):
        if willing_position == "buy":
            # Condition to satisfy buy signal
            if (rsi[i]<rsi_down) & (macdSignal[i] > 0) & (macdSignal_position[i] < 0):
                trade_position[i] = "buy"
                willing_position = "sell"
        elif willing_position == "sell":
            # Condition to satisfy sell signal
            if (rsi[i]>rsi_upper) & (macdSignal[i] < 0) & (macdSignal_position[i] > 0):
                trade_position[i] = "sell"
                willing_position = "buy"    
                
    # Parameters for simulation index part #
    bought_affecting = False
    index = np.array([100]*len(price))
    
    # Prepare Simulation data #
    for j in range(len(price)):
        
        index[j] = index[j-1]
        
        if trade_position[j] == 'buy':
            trade_price = price[j]
            trade_index = index[j]
            bought_affecting = True
            
        elif trade_position[j] == 'sell':
            bought_affecting = False
        if(bought_affecting  == True):
            # Calculating index 
            new_index = (price[j]/trade_price)*trade_index
            index[j] = new_index
    
    # Plot results #
    plt.title(price.name + " Simulation for the past " + 
              str(int(data_range_time/60/60/24)) + 
              " days, " + 
              str(int(periodic/60)) + 
              " m period")
    plt.plot(index)
    return plt.show()

