# Happy (analytical) football ticket hunting in Happy Valley!!!
from pandas import Series, DataFrame
import pandas as pd
import numpy as np
import os
path = os.path.join(os.path.expanduser('~'), 'psu_tix_prices.txt')                   # read in data file (see example)
tix_data = pd.read_csv(open(path, 'r'), sep=" ", header = None, on_bad_lines='skip') # if line data is messed up, ignore it (probably doesn't matter too much)
tix_data_rev = tix_data.iloc[::-1].reset_index()                                     # Oldest entries are at the bottom of the list since newest listings are added to the top, so reverse index
emails_prices = tix_data_rev[[0,2]]
emails_prices.rename(columns={0:'email_addr',2:'asking_price'}, inplace=True)        # Get & rename only email address and asking price columns


def clean_currency(x):  # Credit: Function code taken from pbpython.com
    """ If the value is a string, then remove currency symbol and delimiters
    otherwise, the value is numeric and can be converted
    """
    if isinstance(x, str):
        return(x.replace('$', '').replace(',', ''))
    return(x)


emails_prices['asking_price']=emails_prices['asking_price'].apply(clean_currency).astype('float')  # convert $x to float
avg_price = round(emails_prices['asking_price'].mean(),2)
# Data visualization of prices
%matplotlib inline                                   
import matplotlib.pyplot as plt
# Histogram of prices (if you are a scalper and reading this, scalping is bad and you should feel bad)
plt.figure(figsize=(15, 10))
values, bins, bars = plt.hist(emails_prices['asking_price'], edgecolor='white', bins=[0, 20, 30, 40, 50, 60, 70, 80, 90, 100, 120, 140, 160, 180, 200, 300])
plt.xlabel("Asking Price")
plt.ylabel("Count")
plt.title(f'Histogram of Asking Prices: mean={avg_price}')
plt.bar_label(bars, fontsize=20, color='navy')
plt.margins(x=0.01, y=0.1)
plt.show()
# Boxplot of prices 
pd.plotting.boxplot(emails_prices, column = 'asking_price') 
plt.title(f'Boxplot of Asking Prices')
plt.ylabel("Price in $")
plt.show()
print(round(emails_prices['asking_price'].describe(),2))  # Basic summary statistics
# Lineplot (see how most list prices are currently trending, though no timestamp data is available)
t = np.arange(0, len(emails_prices), 1)
plt.plot(t, emails_prices['asking_price'])
plt.title('Ticket price from oldest to most recent')
plt.ylabel("Asking Price ($)")
plt.show()

# Top 10 list of people to inquire about prices (cheapest first)
emails_prices.sort_values(by = ['asking_price'], ascending=True,inplace=True)
print('TOP 10 CHEAPEST SELLERS')
print(emails_prices[0:10])
# Top 3 people that need to stop scalping
print('TOP 3 SCALPERS')
emails_prices.sort_values(by = ['asking_price'], ascending=False,inplace=True)
print(emails_prices[0:3])