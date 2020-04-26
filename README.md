# CryptoTradeBot (Python)
Automated Cryptocurrency Trading Platform for Poloniex.com. Algorithms are based on Python 3.7. Currently, a platform is using traditional MACD and RSI analysis to detect signs when the best time to buy and sell cryptocurrencies. <br/>
**Algorithm description** is under **Trading_Strategies.py** file description.
# Instruction
*   **IMPORTANT** Open main.py, Trading_Simulation.py, Trading_Strategies.py, Trading_Operations.py files and put API (Poloniex) and secret keys (Poloniex) for *source_API* variable to connect with your account. API and secret keys are accessible through the personal Poloniex account with all the tutorials already in <br/>
*   **main.py is the main file to run operations under section *PROCESSES*** <br/>
*   In main.py only under section *MODIFY PARAMETERS*, write parameters you want to use: cryptocurrency pair, data range, periodic between data (given availabilities are given in comments) <br/>
* To run trading part, in main.py under section *PROCESSES* run **MACD_RSI_STRATEGY**. If you want to stop automated trading, you have to stop python file manually <br/>
* As pre analysis, simulation part can be run with **MACD_RSI_SIMULATION** function, graphs can be run as **chart_technical** and **chart_general** by given example in section *PROCESSES* <br/>

(Option) In order to fullfit (**enable**) trade deal once running *MACD_RSI_STRATEGY* variable *do_trade* should be called as **do_trade = "yes"** <br/>
(Option) Change in Trading_Save_Data.py variable *direction* excel file direction, to gather all completed trades. After every trade forward in the other location, because once you will start to trade again, data will be modified in the same excel cells. In order to **enable** to save in excel file, once running *MACD_RSI_STRATEGY* variable *excel* should be called as **excel = "yes"** <br/>

# Files (for editing)
* **Graphs.py** - graphs by function **chart_technical** for RSI and MACD values and **chart_general** for general price <br/>
* **Poloniex.py** - All poloniex platform available functions (https://docs.poloniex.com/#introduction) to gather data and execute operations <br/>
* **Technical.py** - RSI and MACD strategies written by given https://www.tradingview.com/ platform <br/>
* **Trading_Operations.py** - Executing operations to buy or sell cryptocurrencies and has ability (if enabled) to save operation in excel file <br/>
* **Trading_Save_Data.py** - Gives ability to save data in excel file <br/>
* **Trading_Simulation.py** - Simulating all taken data by taken crypto-pair while using RSI-MACD strategy. Starting index = 100 and given output is a plot which shows how index changed <br/>
* **Trading_Strategies.py** - algorithm which **1.** get current MACD, RSI prices with the last made trade type (to avoid doing the same trading type. **2.** By given defaults value by https://www.tradingview.com/, if RSI value more than 70, algorithm is willing to sell, if less than 30 - buy. **3.** Once Approved by RSI to make operation, MACD value is compared by given https://www.tradingview.com/ defaults value, whether signals gives a sign to buy or sell **4.** Once current RSI and MACD values are declaring to do the same operation, algorithm is executing. **IMPORTANT** Algorithm is trading by all amount of money in tradable pair. <br/>
* **main.py** - The main file do pre-analysis and run trading bot

# Upcoming plan
To use ML and Deep Learning tools to analyse price data with Tensorflow 2.0.

