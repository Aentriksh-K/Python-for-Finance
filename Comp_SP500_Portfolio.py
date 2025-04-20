
# Problem Statement : if i invest $100 in each stock 5 year ago, what will be their price today? Plot their graph.

import matplotlib.pyplot as plt, pandas as pd, numpy as np, yfinance as yf

ticker = ["AAPL","MSFT","F","MS", "NVDA", "TSLA", "META","XOM","GOOGL", "CVX"]
raw_data = yf.download(ticker,period = '5y')
df = pd.DataFrame(raw_data)
adj_cl = df["Adj Close"]

for i in ticker:
    adj_cl[ i + " Return"] =  (adj_cl[i]/adj_cl[i].shift(1) - 1 )
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

ret =[] # stock CAGR  
risk = [] # stock standard deviation

for i in ret_adj_cl.columns:
    CAGR_mean2 =  ret_adj_cl[i].mean()
    CAGR = ((CAGR_mean2 + 1)**250 - 1)*100 # Stock trades for 250 days
    ret.append(CAGR)

    std = ret_adj_cl[i].std() * np.sqrt(250) * 100
    risk.append(std)

risk_ret = pd.DataFrame(index = ticker)
risk_ret["Return2"] = ret
risk_ret["risk"] = risk
risk_ret["Risk_Adjusted_Ret"] = risk_ret["Return2"] / risk_ret["risk"] # Risk adjusted return calculation

risk_ret["Weight"] = risk_ret["Risk_Adjusted_Ret"]/(risk_ret["Risk_Adjusted_Ret"].sum()) # applying weights based on risk adjusted returns
final_df = pd.DataFrame()
final_df["Portfiolio NAV"] = rebase_df.dot(list(risk_ret["Weight"])) # if we have $100, invest them in 10 stocks portfolio based on the "weights" (Portfolio NAV is $100),  then what will be portfolio value? 

# compare Portfolio NAV with S&P 500 (what if we invest $100 in S&P 500 5Y ago)

ticker2 = "SPY" # S&P500
spy_data = yf.download(ticker2, period='5y')
df_spy_data = pd.DataFrame(spy_data)
df_spy_data["SPY_Returns"] = df_spy_data["Adj Close"]/(df_spy_data["Adj Close"].shift(1)) - 1

df_spy_data.dropna(inplace=True) # remove 1st row as it NaN 

temp2 = []
temp = 100
for i in df_spy_data["SPY_Returns"]:
    temp =  (i + 1)*temp
    temp2.append(temp)

final_df["S&P 500"] = temp2
final_df # shows value of $100 in Portfolio and S&P500 in last 5 years 


plt.plot(final_df)
plt.legend(final_df.columns)
plt.show()