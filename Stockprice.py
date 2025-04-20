import matplotlib.pyplot as plt, pandas as pd, yfinance as yf

ticker = ["AAPL","MSFT","F","NVDA", "TSLA", "META","GOOGL"]

raw_data = yf.download(ticker, period = "5y")
raw_data_df = pd.DataFrame(raw_data)
Adj_cl = raw_data_df ["Adj Close"]

plt.figure( figsize = (9,9) )

for i in ticker: # to compare multiple firms
    plt.plot(Adj_cl.index,Adj_cl[i])

plt.legend(ticker)
plt.title(" Stock Performance for last 5 years ")
plt.xlabel("Year")
plt.ylabel("Price in $")
plt.show()