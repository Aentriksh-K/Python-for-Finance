
# Problem Statement : if i invest $100 in each stock 5 year ago, what will be their price today? Plot their graph.

import matplotlib.pyplot as plt, pandas as pd, numpy as np, yfinance as yf

ticker = ["AAPL","MSFT","F","MS", "NVDA", "TSLA", "META","XOM","GOOGL", "CVX"]
raw_data = yf.download(ticker,period = '5y')
df = pd.DataFrame(raw_data)
adj_cl = df["Adj Close"]

for i in ticker:
    adj_cl[ i + " Return"] =  adj_cl[i]/adj_cl[i].shift(1) - 1 
adj_cl.dropna(inplace = True)

ret_adj_cl = adj_cl.iloc[:,10:] # choose all column of last 10 position 

rebase_df = pd.DataFrame() # to store new dataframe which shows journey of $100 invested 5years ago
for j in ret_adj_cl.columns :  # j holds column name 
    temp = 100 # $100 invested
    temp2 = [] 
    for i in ret_adj_cl[j]: # i holds % return value
        temp = ( 1 + i) * temp # initially temp is 100, multiplied by 1 + % return, and appends to empty list. This new value is again multiplied with next % return ( This shows how my $100 is changing every day ) 
        temp2.append(temp)
    rebase_df[j] = temp2 # store all values of each j in rebase dataframe

print(rebase_df) # shows value of $100  invested per trading day, till today


plt.plot(rebase_df)
plt.legend(list(rebase_df))
plt.show()
