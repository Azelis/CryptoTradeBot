from Trading_Save_Data import excel_store
from Poloniex import poloniex

# <API Key>, <Secret Key>``
source_API = poloniex("",
"")

# The key point to record data in excel file
# In order to record, excel="yes" should be called in the function
def Buy_Crypto(currency_pair, buy_price, record_amount, transaction_time=0, type_trade=0, record_price=0,row_y=0, excel="no"):
        source_API.buy(currency_pair, 
                       buy_price, 
                       record_amount)
        #Record in excel file
        if excel == "yes":
            excel_store(transaction_time, 
                        type_trade, 
                        record_price, 
                        record_amount, 
                        currency_pair,
                        row_y)
        
def Sell_Crypto(currency_pair, sell_price, record_amount, transaction_time=0, type_trade=0, record_price=0,row_y=0, excel="no"):
        source_API.sell(currency_pair, 
                        sell_price, 
                        record_amount)
        # Record in excel file
        if excel == "yes":
            excel_store(transaction_time, 
                        type_trade, 
                        record_price, 
                        record_amount, 
                        currency_pair,
                        row_y)

 