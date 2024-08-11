import matplotlib.pyplot, pandas as pd, yfinance as yf, numpy as np
ticker = ["AAPL","MSFT","F","MS", "NVDA", "TSLA", "META","XOM","GOOGL", "CVX"]
raw_data = yf.download(ticker, period = "5y")
df = pd.DataFrame(raw_data)
adj_cl = df["Adj Close"]

for i in ticker:
    adj_cl[ i + " Returns"] = (adj_cl[i]/adj_cl[i].shift(1) - 1) # calculating returns based on previous day

adj_cl.dropna(inplace= True) # to remove first row as first row in NaN

col =  list(adj_cl.columns)[-10:] # gives name of last 10 columns

return1 = []
risk1 = []
for i in col:
    CAGR_Mean = adj_cl[i].mean()  # calculatin CAGR
    CAGR = ((CAGR_Mean + 1)**250 - 1) * 100   # number of trading days is 250 
    return1.append(CAGR)
    # calculating risk (Standard deviation) 
    risk = (adj_cl[i].std() * np.sqrt(250)) * 100   # number of trading days is 250 
    risk1.append(risk)

return_risk = pd.DataFrame(index = ticker)
return_risk["Return"] = return1
return_risk["Risk"] = risk1
return_risk["Risk adj Return"] = return_risk["Return"] / return_risk["Risk"] # adding new field and calculating Risk adjusted return

Risk_adj_ret_list = list(return_risk["Risk adj Return"]) # it shows in simple list format
sum_risk_adj_ret = np.sum(Risk_adj_ret_list) # sum of all risk adj. return

weght_risk_adj_ret = Risk_adj_ret_list/sum_risk_adj_ret # assigning weight to each index
return_risk["Weight"] = weght_risk_adj_ret
return_risk