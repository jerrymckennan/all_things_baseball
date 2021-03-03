# This plots the same data as starter_vs_reliever_no_outliers.py, but allows for the outliers to appear. So starters with > 6 fWAR are included here.

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import os.path
from os import path

# 2010:
# 1585 qualified relievers w/ average FB velocity (20-43)
# 1320 starters w/ IP >= 100 (20-47)

# 2000:
# 2968 qualified relievers w/ average FB velocity (20-43)
# 2615 starters w/ IP >= 100 (20-47)

st_data = pd.read_csv('/path/file.csv')
re_data = pd.read_csv('/path/file.csv')
re_data = re_data[re_data['Season'] < 2020]
st_data['WAR_over_IP'] = st_data['WAR']/st_data['IP']
re_data['WAR_over_IP'] = re_data['WAR']/re_data['IP']

st_data_velo = st_data[st_data['FBv'] > 0]
re_data_velo = re_data[re_data['FBv'] > 0]

st_counter = 19
re_counter = 19

st_age_mean = pd.DataFrame(columns=['ERA','FIP','xFIP','WAR','IP','Age','FBv', 'WAR_over_IP'])
re_age_mean = pd.DataFrame(columns=['ERA','FIP','xFIP','WAR','IP','Age','FBv', 'WAR_over_IP'])
st_age_mean_velo = pd.DataFrame(columns=['ERA','FIP','xFIP','WAR','IP','Age','FBv', 'WAR_over_IP'])
re_age_mean_velo = pd.DataFrame(columns=['ERA','FIP','xFIP','WAR','IP','Age','FBv', 'WAR_over_IP'])
war_diff = pd.DataFrame(columns=['WAR', 'Age'])
velo_diff = pd.DataFrame(columns=['FBv', 'Age'])
IP_diff = pd.DataFrame(columns=['IP', 'Age'])

while st_counter <= max(st_data['Age']):
    st_age = st_data[st_data['Age'] == st_counter].mean()
    st_age_mean = st_age_mean.append(st_age, ignore_index=True)
    st_counter += 1
while re_counter <= max(re_data['Age']):
    re_age = re_data[re_data['Age'] == re_counter].mean()
    re_age_mean = re_age_mean.append(re_age, ignore_index=True)
    re_counter += 1
    
st_counter = 19
re_counter = 19
    
while st_counter <= max(st_data_velo['Age']):
    st_age_velo = st_data_velo[st_data_velo['Age'] == st_counter].mean()
    st_age_mean_velo = st_age_mean_velo.append(st_age_velo, ignore_index=True)
    st_counter += 1
while re_counter <= max(re_data_velo['Age']):
    re_age_velo = re_data_velo[re_data_velo['Age'] == re_counter].mean()
    re_age_mean_velo = re_age_mean_velo.append(re_age_velo, ignore_index=True)
    re_counter += 1
    
war_diff['WAR'] = st_age_mean['WAR'] - re_age_mean['WAR']
war_diff['Age'] = st_age_mean['Age']
velo_diff['FBv'] = st_age_mean['FBv'] - re_age_mean['FBv']
velo_diff['Age'] = st_age_mean['Age']
IP_diff['IP'] = st_age_mean['IP'] - re_age_mean['IP']
IP_diff['Age'] = st_age_mean['Age']
    
st_age_mean.drop(columns=['Name','Season','Team'], inplace=True)
re_age_mean.drop(columns=['Name','Season','Team'], inplace=True)

fig, axes = plt.subplots(1, 3, sharey=True, figsize=((30,7)), constrained_layout=True)
sns.stripplot(ax=axes[0], data=st_data_velo, x="Age", y="FBv", size=4, color="blue", linewidth=0).set_title("FB velocity range by age for starters");
axes[0].set_ylabel("FB velocity");
sns.stripplot(ax=axes[1], data=re_data_velo, x="Age", y="FBv", size=4, color="purple", linewidth=0).set_title("FB velocity range by age for relievers");
axes[1].set_ylabel("");
sns.regplot(ax=axes[2], data=st_age_mean, x="Age", y="FBv", color="blue").set_title("Starter vs Reliever average FB velocity by age");
sns.regplot(ax=axes[2], data=re_age_mean, x="Age", y="FBv", color="purple");
axes[2].set_ylabel("");
axes[2].set_xticks(np.arange(19,49,1));
axes[0].axhline(y=st_data['FBv'].mean(), color="blue", linestyle='dashed');
axes[1].axhline(y=re_data['FBv'].mean(), color="purple", linestyle='dashed');
axes[2].axhline(y=st_data['FBv'].mean(), color="blue", linestyle='dashed');
axes[2].axhline(y=re_data['FBv'].mean(), color="purple", linestyle='dashed');
axes[2].legend(['Starter', 'Reliever', str(round(st_data['FBv'].mean(),1)), str(round(re_data['FBv'].mean(),1))]);

fig2, axes2 = plt.subplots(1, 3, sharey=True, figsize=((30,7)), constrained_layout=True)
sns.stripplot(ax=axes2[0], data=st_data, x="Age", y="WAR", size=4, color="blue", linewidth=0).set_title("fWAR by age for starters");
axes2[0].set_ylabel("fWAR");
sns.stripplot(ax=axes2[1], data=re_data, x="Age", y="WAR", size=4, color="purple", linewidth=0).set_title("fWAR by age for relievers");
axes2[1].set_ylabel("");
sns.regplot(ax=axes2[2], data=st_age_mean, x="Age", y="WAR", color="blue").set_title("Starter vs Reliever average fWAR by age");
sns.regplot(ax=axes2[2], data=re_age_mean, x="Age", y="WAR", color="purple");
axes2[2].set_ylabel("");
axes2[2].set_xticks(np.arange(19,49,1));
axes2[0].axhline(y=st_data['WAR'].mean(), color="blue", linestyle='dashed');
axes2[1].axhline(y=re_data['WAR'].mean(), color="purple", linestyle='dashed');
axes2[2].axhline(y=st_data['WAR'].mean(), color="blue", linestyle='dashed');
axes2[2].axhline(y=re_data['WAR'].mean(), color="purple", linestyle='dashed');
axes2[2].legend(['Starter', 'Reliever', str(round(st_data['WAR'].mean(),1)), str(round(re_data['WAR'].mean(),1))]);

fig3, axes3 = plt.subplots(1, 3, sharey=True, figsize=((30,7)), constrained_layout=True)
sns.stripplot(ax=axes3[0], data=st_data, x="Age", y="WAR_over_IP", size=4, color="blue", linewidth=0).set_title("fWAR/IP by age for starters");
axes3[0].set_ylabel("fWAR");
sns.stripplot(ax=axes3[1], data=re_data, x="Age", y="WAR_over_IP", size=4, color="purple", linewidth=0).set_title("fWAR/IP by age for relievers");
axes3[1].set_ylabel("");
sns.regplot(ax=axes3[2], data=st_age_mean, x="Age", y="WAR_over_IP", color="blue").set_title("Starter vs Reliever average fWAR/IP by age ");
sns.regplot(ax=axes3[2], data=re_age_mean, x="Age", y="WAR_over_IP", color="purple");
axes3[2].set_ylabel("");
axes3[2].set_xticks(np.arange(19,49,1));
axes3[0].axhline(y=st_data['WAR_over_IP'].mean(), color="blue", linestyle='dashed');
axes3[1].axhline(y=re_data['WAR_over_IP'].mean(), color="purple", linestyle='dashed');
axes3[2].axhline(y=st_data['WAR_over_IP'].mean(), color="blue", linestyle='dashed');
axes3[2].axhline(y=re_data['WAR_over_IP'].mean(), color="purple", linestyle='dashed');
axes3[2].legend(['Starter', 'Reliever', str(round(st_data['WAR_over_IP'].mean(),4)), str(round(re_data['WAR_over_IP'].mean(),4))]);

fig4, axes4 = plt.subplots(1, 3, sharey=True, figsize=((30,7)), constrained_layout=True)
sns.stripplot(ax=axes4[0], data=st_data, x="Age", y="IP", size=4, color="blue", linewidth=0).set_title("IP by age for starters");
axes4[0].set_ylabel("fIP");
sns.stripplot(ax=axes4[1], data=re_data, x="Age", y="IP", size=4, color="purple", linewidth=0).set_title("IP by age for relievers");
axes4[1].set_ylabel("");
sns.regplot(ax=axes4[2], data=st_age_mean, x="Age", y="IP", color="blue").set_title("Starter vs Reliever average IP by age");
sns.regplot(ax=axes4[2], data=re_age_mean, x="Age", y="IP", color="purple");
axes4[2].set_ylabel("");
axes4[2].set_xticks(np.arange(19,49,1));
axes4[0].axhline(y=st_data['IP'].mean(), color="blue", linestyle='dashed');
axes4[1].axhline(y=re_data['IP'].mean(), color="purple", linestyle='dashed');
axes4[2].axhline(y=st_data['IP'].mean(), color="blue", linestyle='dashed');
axes4[2].axhline(y=re_data['IP'].mean(), color="purple", linestyle='dashed');
axes4[2].legend(['Starter', 'Reliever', str(round(st_data['IP'].mean(),1)), str(round(re_data['IP'].mean(),1))]);

fig5, axes5 = plt.subplots(1, 3, figsize=((30,7)), constrained_layout=True)
sns.regplot(ax=axes5[0], data=war_diff, x="Age", y="WAR", color="orange").set_title("Average WAR difference between relievers and starters by age (starters - relievers)");
sns.regplot(ax=axes5[1], data=velo_diff, x="Age", y="FBv", color="orange").set_title("Average Fastball Velocity difference between relievers and starters by age (starters - relievers)");
sns.regplot(ax=axes5[2], data=IP_diff, x="Age", y="IP", color="orange").set_title("Average IP difference between relievers and starters by age (starters - relievers)");
axes5[0].set_ylabel("WAR");
axes5[1].set_ylabel("Fastball Velocity");
axes5[2].set_ylabel("Innings Pitched");
axes5[0].set_xticks(np.arange(19,45,1));
axes5[1].set_xticks(np.arange(19,45,1));
axes5[2].set_xticks(np.arange(19,45,1));

plt.show()
