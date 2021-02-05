# This will create two separate CSV files, one with starter data and one with reliever data.
# I used this to compare Fastball Velocity, fWAR, IP, and fWAR/IP between starters and relievers
# with the script called starters_vs_relievers.py in the graphing folder.

import pandas as pd
import numpy as np
import os.path
from os import path
import time

rel_counter = 1
st_counter = 1
rel_file = '/location/filename.csv'
st_file = '/location/filename.csv'

while rel_counter <= 99:
    counter = str(rel_counter)
    url = "https://www.fangraphs.com/leaders.aspx?pos=all&stats=rel&lg=all&qual=y&type=c,13,6,45,62,59,3,76&season=2020&month=0&season1=2000&ind=1&team=0&rost=0&age=0&filter=&players=0&startdate=&enddate=&page="+counter+"_30"
    data = pd.read_html(url)
    data = data[16]
    data.drop(data.tail(1).index,inplace=True)
    data.rename(columns={"#":" num"}, inplace=True)
    data.fillna(0, inplace=True)
    if path.exists(rel_file):
        data.to_csv(rel_file, mode='a', header=False)
    else:
        data.to_csv(rel_file)
    time.sleep(np.random.randint(2,10))
    rel_counter = int(counter)
    rel_counter += 1
    
while st_counter <= 88:
    counter = str(st_counter)
    url = "https://www.fangraphs.com/leaders.aspx?pos=all&stats=sta&lg=all&qual=100&type=c,13,6,45,62,59,3,76&season=2020&month=0&season1=2000&ind=1&team=0&rost=0&age=0&filter=&players=0&startdate=2000-01-01&enddate=2020-12-31&page="+counter+"_30"
    data = pd.read_html(url)
    data = data[16]
    data.drop(data.tail(1).index,inplace=True)
    data.rename(columns={"#":" num"}, inplace=True)
    data.fillna(0, inplace=True)
    if path.exists(st_file):
        data.to_csv(st_file, mode='a', header=False)
    else:
        data.to_csv(st_file)
    time.sleep(np.random.randint(2,10))
    st_counter = int(counter)
    st_counter += 1
