import FinanceDataReader as fdr
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import warnings
plt.rcParams["figure.figsize"] = (14,8)
plt.rcParams['font.size'] = 16
plt.rcParams['lines.linewidth'] = 2
plt.rcParams["axes.grid"] = True
plt.rcParams['axes.axisbelow'] = True
warnings.filterwarnings('ignore')
from matplotlib.figure import Figure

# #fetch the price data
data = fdr.DataReader('S&P500')

# select only Colse column
close = data['Close']

# set a period for comparing
start_date = '2023-04-01'
end_date = '2023-04-20'

# Time series chart of a selected period
# close[start_date:end_date].plot();
base = close[start_date:end_date]
base_norm = (base - base.min()) / (base.max() - base.min())

# window size : number of past days to see the pattern
window_size = len(base)

# how many days you wanna predict
next_date = 5  #5means one week, 10 means two weeks ...and so on

# number of search
moving_cnt = len(close) - window_size - next_date - 1

def cosine_similarity(x, y):
    return np.dot(x, y) / (np.sqrt(np.dot(x, x)) * np.sqrt(np.dot(y, y)))

# a dictionary for similarity
sim_list = []

for i in range(moving_cnt):
    target = close[i:i+window_size]
    
    # Normalize
    target_norm = (target - target.min()) / (target.max() - target.min())
    
    # save the cosine similarity 
    cos_similarity = cosine_similarity(base_norm, target_norm)
    
    # append it to the list
    sim_list.append(cos_similarity)

print(pd.Series(sim_list).sort_values(ascending = False).head(20))

idx = 10801

top_ = close[idx:idx+window_size+next_date]
top_norm = (top_ - top_.min()) / (top_.max() - top_.min())

plt.plot(base_norm.values, label='base')
plt.plot(top_norm.values, label='target')
plt.axvline(x=len(base_norm)-1, c='r', linestyle='--')
plt.axvspan(len(base_norm.values)-1, len(top_norm.values)-1, facecolor='yellow', alpha=0.3)
plt.legend()
plt.show()
