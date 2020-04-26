######### Functions from other python files #########
from Poloniex import poloniex,createTimeStamp
from Graphs import chart_technical, chart_general
from Technical import TechnicalIndicators
from Trading_Strategies import MACD_RSI_STRATEGY
from Trading_Simulation import MACD_RSI_SIMULATION

######### Libraries #########
from time import gmtime, strftime
import matplotlib.pyplot as plt
import pandas as pd
##############################


############# MODIFY PARAMETERS #################

#<API Key>, <Secret Key>``
source_API = poloniex("",
"")

# As a DOLLAR for buying a stock
market_currency = "USDT"#BTC; ETH; XMR; USDT

# As a STOCK which will be traded
trade_currency = "XRP" #XRP at least 0.0001

periodic = 900 
#300(5min)
#900(15 min)
#1800(30 min)
#7200(2 h)
#14400(4 h)
#86400(24 h)
data_range_time = 2592000
#1 day (86400 s)
#3 day (259200 s)
#1 week (604800 s)
#2 weeks (1209600 s)
#30days (2592000 s) 
#50days (4320000 s)
#90days (7776000 s)

############################################################


############## CREATING DATAFRAME ################
currency_pair = market_currency + "_" + trade_currency
end_time = int(createTimeStamp(strftime("%Y-%m-%d %H:%M:%S", gmtime())))
start_time = end_time - data_range_time 

# Market data about stock
chart_data = pd.DataFrame(source_API.returnChartData(currency_pair,start_time,periodic))

# Maximum 1000 rows past publc trading data
#trading_public_data = pd.DataFrame(source_API.returnMarketTradeHistory(currency_pair,start_time,end_time))

# Past Order Book
#order_data = pd.DataFrame(source_API.returnOrderBook(currency_pair))

# Data (price) to use for technical model decision
price = chart_data["close"].rename(market_currency + "-" + trade_currency)
##################################################



########## PROCESSES ###############

# Current price plot
chart_general.time_series(price)

# RSI plot
RSI_price = TechnicalIndicators().RSI(price)
chart_technical.time_series_RSI(RSI_price)

# Run trading bot (uncomment)
# MACD_RSI_STRATEGY(market_currency = market_currency,
#                   trade_currency = trade_currency,
#                   data_range_time = data_range_time, 
#                   periodic = periodic, 
#                   do_trade = "no",
#                   excel = "no")

MACD_RSI_SIMULATION(market_currency = market_currency,
                  trade_currency = trade_currency,
                  data_range_time = data_range_time, 
                  periodic = periodic)
