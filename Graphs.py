import matplotlib.pyplot as plt

class chart_general:
    def time_series(x):
        plt.title(x.name)
        plt.plot(x)
        return plt.show()
    def daily_distribution(x):
        x.pct_change().plot.hist(bins=50)
        plt.xlabel('adjusted close 1-day percent change')
        return plt.show()

class chart_technical:
    def time_series_MACD(macd_full, original_data):
        plt.title(original_data.name + " MACD")
        plt.plot(macd_full["emaslow"])
        plt.plot(macd_full["emafast"]) 
        plt.plot(original_data)         
    def time_series_MACD_signals(macd_full):
        plt.title(" MACD Signals")
        plt.plot(macd_full["macd_signal"]) 
        plt.plot(macd_full["macd"]) 
        plt.axhline(y=0, color="black")
        return plt.show()
    def time_series_RSI(x):
        plt.title("RSI")
        plt.plot(x, color="black")
        plt.axhline(y=30, color="red")
        plt.axhline(y=70, color="red")
        return plt.show()
        
