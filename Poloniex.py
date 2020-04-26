import requests
from requests import Session
import time
import hmac,hashlib
from urllib.parse import urlencode


def createTimeStamp(datestr, format="%Y-%m-%d %H:%M:%S"):
    return time.mktime(time.strptime(datestr, format))

class poloniex:
    def __init__(self, APIKey, Secret):
        self.APIKey = APIKey
        self.Secret = Secret
        
    def post_process(self, before):
        after = before

        # Add timestamps if there isnt one but is a datetime
        if('return' in after):
            if(isinstance(after['return'], list)):
                for x in range(0, len(after['return'])):
                    if(isinstance(after['return'][x], dict)):
                        if('datetime' in after['return'][x] and 'timestamp' not in after['return'][x]):
                            after['return'][x]['timestamp'] = float(createTimeStamp(after['return'][x]['datetime']))
                            
        return after

    def api_query(self, command, req={}, start_pos={}, period_pos={}):

        if(command == "returnTicker" or command == "return24hVolume"):
            ret = requests.get('https://poloniex.com/public?command=' + command)
            return ret.json()
        elif(command == "returnOrderBook"):
            ret = requests.get('https://poloniex.com/public?command=' + command + '&currencyPair=' + str(req['currencyPair']) + 
                               '&depth=' + str(100))
            return ret.json()
        elif(command == "returnMarketTradeHistory"):
            ret = requests.get('https://poloniex.com/public?command=' + "returnTradeHistory" + '&currencyPair=' + str(req['currencyPair']) + '&start=' + 
            str(start_pos['start']) + '&end=' + str(period_pos['end']))
            return ret.json()
        elif(command == "returnChartData"):
            ret = requests.get('https://poloniex.com/public?command=' + "returnChartData" + '&currencyPair=' + str(req['currencyPair']) + '&start=' + 
            str(start_pos['start']) + '&period=' + str(period_pos['period']))
            return ret.json()

        else:
            req['command'] = command
            req['nonce'] = int(time.time()*1000)

            sign = hmac.new(self.Secret.encode('utf-8'), urlencode(req).encode('utf-8'), hashlib.sha512).hexdigest()
            headers = {
                'Key': self.APIKey,
                'Sign': sign
            }
            ret = Session().post('https://poloniex.com/tradingApi', headers=headers, data=req)
            jsonRet = ret.json()
            return self.post_process(jsonRet)


    def returnTicker(self):
        return self.api_query("returnTicker")

    def return24hVolume(self):
        return self.api_query("return24hVolume") #Doesn't work

    def returnOrderBook (self, currencyPair): #Add time depth
        return self.api_query("returnOrderBook", {'currencyPair': currencyPair})

    def returnMarketTradeHistory (self, currencyPair, start, end):
        return self.api_query("returnMarketTradeHistory", {'currencyPair': currencyPair}, {'start': start}, {'end': end})

    def returnChartData (self, currencyPair, start, period): #periods in seconds (valid values are 300, 900, 1800, 7200, 14400 and 86400 ?); dont need to use end till it is default as current date
        return self.api_query("returnChartData", {'currencyPair': currencyPair}, {'start': start}, {'period': period})

    # Returns all of your balances.
    # Outputs: 
    # {"BTC":"0.59098578","LTC":"3.31117268", ... }
    def returnBalances(self):
        return self.api_query('returnBalances')
    
    # Returns your open orders for a given market, specified by the "currencyPair" POST parameter, e.g. "BTC_XCP"
    # Inputs:
    # currencyPair  The currency pair e.g. "BTC_XCP"
    # Outputs: 
    # orderNumber   The order number
    # type          sell or buy
    # rate          Price the order is selling or buying at
    # Amount        Quantity of order
    # total         Total value of order (price * quantity)
    def returnOpenOrders(self,currencyPair):
        return self.api_query('returnOpenOrders',{"currencyPair":currencyPair})


    # Returns your trade history for a given market, specified by the "currencyPair" POST parameter
    # Inputs:
    # currencyPair  The currency pair e.g. "BTC_XCP"
    # Outputs: 
    # date          Date in the form: "2014-02-19 03:44:59"
    # rate          Price the order is selling or buying at
    # amount        Quantity of order
    # total         Total value of order (price * quantity)
    # type          sell or buy
    def returnTradeHistory(self,currencyPair,start):
        return self.api_query('returnTradeHistory',{"currencyPair":currencyPair,"start":start})

    # Places a buy order in a given market. Required POST parameters are "currencyPair", "rate", and "amount". If successful, the method will return the order number.
    # Inputs:
    # currencyPair  The curreny pair
    # rate          price the order is buying at
    # amount        Amount of coins to buy
    # Outputs: 
    # orderNumber   The order number
    def buy(self,currencyPair,rate,amount):
        return self.api_query('buy',{"currencyPair":currencyPair,"rate":rate,"amount":amount})

    # Places a sell order in a given market. Required POST parameters are "currencyPair", "rate", and "amount". If successful, the method will return the order number.
    # Inputs:
    # currencyPair  The curreny pair
    # rate          price the order is selling at
    # amount        Amount of coins to sell
    # Outputs: 
    # orderNumber   The order number
    def sell(self,currencyPair,rate,amount):
        return self.api_query('sell',{"currencyPair":currencyPair,"rate":rate,"amount":amount})

    # Cancels an order you have placed in a given market. Required POST parameters are "currencyPair" and "orderNumber".
    # Inputs:
    # currencyPair  The curreny pair
    # orderNumber   The order number to cancel
    # Outputs: 
    # success        1 or 0
    def cancel(self,currencyPair,orderNumber):
        return self.api_query('cancelOrder',{"currencyPair":currencyPair,"orderNumber":orderNumber})

    # Immediately places a withdrawal for a given currency, with no email confirmation. In order to use this method, the withdrawal privilege must be enabled for your API key. Required POST parameters are "currency", "amount", and "address". Sample output: {"response":"Withdrew 2398 NXT."} 
    # Inputs:
    # currency      The currency to withdraw
    # amount        The amount of this coin to withdraw
    # address       The withdrawal address
    # Outputs: 
    # response      Text containing message about the withdrawal
    def withdraw(self, currency, amount, address):
        return self.api_query('withdraw',{"currency":currency, "amount":amount, "address":address})
    #Returns your balances sorted by account. You may optionally specify the "account" POST parameter if you wish to fetch only the balances of one account. Please note that balances in your margin account may not be accessible if you have any open margin positions or orders. Sample output:
    
    def returnAvailableAccountBalances(self):
        return self.api_query("returnAvailableAccountBalances")