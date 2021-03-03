# This uses the same CSV file from previously created that would then let you compare two pitchers. 
# These particular graphs show cumulative fWAR by year in season, cumulative fWAR by age, fWAR by age.

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import os.path
from os import path
import warnings

warnings.filterwarnings("ignore")

pitcher_1 = input("Who is the first pitchers full name: ")
pitcher_2 = input("Who is the second pitchers full name: ")

st_data = pd.read_csv('/path/file.csv')
st_data['WAR_over_IP'] = st_data['WAR']/st_data['IP']

st_data_war = st_data

st_data_war.loc[st_data_war.WAR > 4.99, 'pitcher_num'] = "Ace"
st_data_war.loc[st_data_war.WAR.between(4.25,4.99), 'pitcher_num'] = "1"
st_data_war.loc[st_data_war.WAR.between(3.5,4.25), 'pitcher_num'] = "2"
st_data_war.loc[st_data_war.WAR.between(2.75,3.5), 'pitcher_num'] = "3"
st_data_war.loc[st_data_war.WAR.between(2,2.75), 'pitcher_num'] = "4"
st_data_war.loc[st_data_war.WAR.between(1.25,2), 'pitcher_num'] = "5"
st_data_war.loc[st_data_war.WAR < 1.25, 'pitcher_num'] = "AAA"

st_p1_data = st_data_war[st_data_war['Name'] == pitcher_1]
st_p2_data = st_data_war[st_data_war['Name'] == pitcher_2]

st_p1_data.sort_values(by=['Age'], inplace=True)
st_p1_data['Age_WAR'] = st_p1_data['WAR'].cumsum()

st_p2_data.sort_values(by=['Age'], inplace=True)
st_p2_data['Age_WAR'] = st_p2_data['WAR'].cumsum()

st_p1_data.reset_index(inplace=True)
st_p2_data.reset_index(inplace=True)

st_p1_data.drop(columns=['index'], inplace=True)
st_p2_data.drop(columns=['index'], inplace=True)

st_p1_data['year_num'] = st_p1_data.index + 1
st_p2_data['year_num'] = st_p2_data.index + 1

fig7, axes7 = plt.subplots(1, 1, figsize=((30,7)), constrained_layout=True)
sns.lineplot(ax=axes7, data=st_p1_data, x="Age", y="WAR")
sns.scatterplot(ax=axes7, data=st_p1_data, x="Age", y="WAR")
sns.lineplot(ax=axes7, data=st_p2_data, x="Age", y="WAR")
sns.scatterplot(ax=axes7, data=st_p2_data, x="Age", y="WAR")
axes7.axhline(y=5, color="#dc5e4b", linestyle='dashed');
axes7.legend([pitcher_1, pitcher_2], title="Pitcher");

for x,y in zip(st_p1_data['Age'],st_p1_data['WAR']):
    label = round(y, 2)
    plt.annotate(label,
                 (x,y),
                 textcoords="offset points",
                 xytext=(0,10),
                 ha='center')
    
for x,y in zip(st_p2_data['Age'],st_p2_data['WAR']):
    label = round(y, 2)
    plt.annotate(label,
                 (x,y),
                 textcoords="offset points",
                 xytext=(0,10),
                 ha='center')

fig8, axes8 = plt.subplots(1, 1, figsize=((30,7)), constrained_layout=True)
sns.lineplot(ax=axes8, data=st_p1_data, x="Age", y="Age_WAR");
sns.scatterplot(ax=axes8, data=st_p1_data, x="Age", y="Age_WAR");
sns.lineplot(ax=axes8, data=st_p2_data, x="Age", y="Age_WAR");
sns.scatterplot(ax=axes8, data=st_p2_data, x="Age", y="Age_WAR");
axes8.legend([pitcher_1, pitcher_2], title="Pitcher");

for x,y in zip(st_p1_data['Age'],st_p1_data['Age_WAR']):
    label = round(y, 2)
    plt.annotate(label,
                 (x,y),
                 textcoords="offset points",
                 xytext=(0,10),
                 ha='center')
    
for x,y in zip(st_p2_data['Age'],st_p2_data['Age_WAR']):
    label = round(y, 2)
    plt.annotate(label,
                 (x,y),
                 textcoords="offset points",
                 xytext=(0,10),
                 ha='center')

fig9, axes9 = plt.subplots(1, 1, figsize=((30,7)), constrained_layout=True)
sns.lineplot(ax=axes9, data=st_p1_data, x="year_num", y="Age_WAR");
sns.scatterplot(ax=axes9, data=st_p1_data, x="year_num", y="Age_WAR");
sns.lineplot(ax=axes9, data=st_p2_data, x="year_num", y="Age_WAR");
sns.scatterplot(ax=axes9, data=st_p2_data, x="year_num", y="Age_WAR");
axes9.legend([pitcher_1, pitcher_2], title="Pitcher");

for x,y in zip(st_p1_data['year_num'],st_p1_data['Age_WAR']):
    label = round(y, 2)
    plt.annotate(label,
                 (x,y),
                 textcoords="offset points",
                 xytext=(0,10),
                 ha='center')
    
for x,y in zip(st_p2_data['year_num'],st_p2_data['Age_WAR']):
    label = round(y, 2)
    plt.annotate(label,
                 (x,y),
                 textcoords="offset points",
                 xytext=(0,10),
                 ha='center')


plt.show()
