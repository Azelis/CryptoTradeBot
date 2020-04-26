######### Functions from other python files #########
from Poloniex import poloniex, createTimeStamp
from Technical import TechnicalIndicators
from Trading_Operations import Buy_Crypto, Sell_Crypto

###########################
from time import gmtime, strftime
import pandas as pd

#<API Key>, <Secret Key>``
source_API = poloniex("", "")

def MACD_RSI_STRATEGY(trade_currency, market_currency, data_range_time = 604800, periodic = 1800, do_trade = "no", excel="no"):
    ################## parameters for strategies ##################

    strategy = TechnicalIndicators()
    macd_fast = 12
    macd_slow = 26
    rsi_period = 14
    rsi_upper = 70
    rsi_down = 30
    nNine = 9 
    #default row_y for excel to record
    row_y = 1
    ################################################################
    #simulation = for simulation purpose, if 0, the function will stop, to run simulatino once
    while True:
        try:
            # Get currency pair
            currency_pair = market_currency + "_" + trade_currency
            # Current time
            end_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
            # Get a range till when gather a data
            start_time_days = int(createTimeStamp(end_time)) - data_range_time
            # Current portfolio info      
            portfelis = pd.DataFrame(source_API.returnBalances().items())
             #Current data for given market and trade currency       
            if source_API.returnChartData(currency_pair,start_time_days,periodic) =={'error': 'Invalid currency pair.'}:
                print("Invalid currency pair")                
            chart_data = pd.DataFrame(source_API.returnChartData(currency_pair,start_time_days,periodic))
            ########## MACD
            macd = strategy.MACD(chart_data['close'],macd_slow,macd_fast,nNine)
            macdSignal = macd["signal"].iloc[-1]
            macdSignal_position = macd["macd"].iloc[-1]
            ########## RSI
            rsi = strategy.RSI(chart_data['close'],rsi_period).iloc[-1]
            #####General information
            # Current amount of trade currency
            amount_trade = float(portfelis[portfelis[0] == trade_currency][1].values) #Amount of trade currency in portfolio
            # Current amount of Market currency      
            amount_market = float(portfelis[portfelis[0] == market_currency][1].values) #Amount of market currency in portfolio
            # Time for taken data_range_time, made transactions based on currency pair    
            trade_period = start_time_days-data_range_time*10000
            # if sign is given for transaction: 
            # yes(action) | no(nothing) | not sufficient fund(not possible to do a trade)
            action = "Nothing"
            
            last_strategy = "None"
            # Checking last trade, if there was not, as default - sell, to make first
            # transaction as buy
            if source_API.returnTradeHistory(currency_pair,trade_period) != []:
                last_types_trade = pd.DataFrame(source_API.returnTradeHistory(currency_pair,trade_period))["type"][0] 
            else:
                last_types_trade = "sell"
            
            #################### Applying prepared data ####################
            if last_types_trade == "sell": 
                # Safe to stop algo, since having market currency
                type_trade = "Want: buy (safe to stop), -RSI, -MACD"
                if  rsi < rsi_down: # Buy
                    # Giving access for macd
                    last_strategy = "rsi"
                    
            if last_types_trade == "buy":
                # Important to end up with market currency to avoid volatility
                type_trade = "Want: sell (Do not stop), -RSI, -MACD"
                if rsi > rsi_upper: # Sell
                    # Giving access for macd
                    last_strategy = "rsi"     
                    
            # First RSI have to be satisfied  in order to move on MACD       
            if last_strategy == "rsi":
                type_trade = "Want: sell, +RSI, -MACD"
                if  macdSignal > 0 and macdSignal_position < 0 and last_types_trade == "sell":
                    # Getting current lowest SELL ORDERS price
                    buy_price_real = float(pd.DataFrame(source_API.returnOrderBook(currency_pair))['asks'][1][0])
                    # For recording
                    record_price = buy_price_real
                    #for record, amount changes to convert to trade amount
                    record_amount = amount_market / buy_price_real
                    # To make sure once will put a price, it will be very high to buy instantly
                    # Because automatically it will buy from the lowest price offers
                    buy_price = buy_price_real*2
                    # Give access to buy
                    type_trade = "buy"
                    action = "yes"
                    # Recording last strategy
                    last_strategy = "macd"
                    
                if macdSignal < 0 and macdSignal_position > 0 and last_types_trade == "buy":
                    # Getting current highest buy ORDERS price
                    sell_price_real = float(pd.DataFrame(source_API.returnOrderBook(currency_pair))['bids'][1][0])
                    # To record info
                    record_price = sell_price_real 
                    #Amount does not change
                    record_amount = amount_trade
                    # To sell instantly               
                    sell_price = sell_price_real/2
                    # Recording last strategy
                    last_strategy = "rsi"
                    # Give access to sell              
                    type_trade = "sell"
                    action = "yes"
                    # Recording last strategy
                    last_strategy = "macd"  
            print (type_trade, "  RSI:", str(round(rsi, 2)),
                   "  MACD Signal:",str(round(macdSignal, 4)))
            
            if action == "yes":
                print ("Completed:", type_trade, 
                       "   price:",record_price,"   amount: ",record_amount)
                if do_trade == "yes":
                    row_y = row_y + 1
                    if type_trade == "sell":
                        Sell_Crypto(currency_pair,
                                    sell_price,
                                    record_amount,
                                    end_time,
                                    type_trade,
                                    record_price, 
                                    row_y,
                                    excel)
                        # Because Market currencies have low volatility
                        print("Sold, Safe to stop")
                    if type_trade == "buy":
                        Buy_Crypto(currency_pair,
                                   buy_price,
                                   record_amount,
                                   end_time,
                                   type_trade,
                                   record_price, 
                                   row_y,
                                   excel)         
                        print("Bought")
        except Exception:
            print ("Error - RSI_MACD")
            continue
    
        
