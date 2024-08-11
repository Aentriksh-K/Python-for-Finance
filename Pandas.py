
import numpy as np
import pandas as pd

a = np.array(['Aent',6,'62'])  # instead of array, you can also create normal dictionary
print(a)
s = pd.Series(a)
# series is nothing but table which holds different values. *It is always 1 dimansional* 
# It can be of any type

print(s)
print(s[2])

