# This script grabs the data saved in a CSV file that was retrieved from FanGraphs for relievers and starters.
# Got some really cool data and graphs out of this. Also wanted to try to normalize the data for the first time,
# so I was able to use IQR to take out some of the really, really good and really, really bad seasons. Not that
# I didn't want them included, I wanted to make sure they didn't skew my data any.

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import os.path
from os import path

# 2010-2019:
# 1585 qualified relievers w/ average FB velocity (20-43)
# 1320 starters w/ IP >= 100 (20-47)

# 2002-2019:
# 2968 qualified relievers w/ average FB velocity (20-43)
# 2615 starters w/ IP >= 100 (20-47)

st_data = pd.read_csv('/Users/jerrymckennan/Documents/JSON/starters_totals.csv')
re_data = pd.read_csv('/Users/jerrymckennan/Documents/JSON/relievers_totals.csv')
st_data = st_data[st_data['IP'] >= 150]
re_data = re_data[re_data['Season'] < 2020]
st_data['WAR_over_IP'] = st_data['WAR']/st_data['IP']
re_data['WAR_over_IP'] = re_data['WAR']/re_data['IP']

st_data_war = st_data

st_data.loc[st_data.WAR > 4.99, 'pitcher_num'] = "Ace"
st_data.loc[st_data.WAR.between(4.25,4.99), 'pitcher_num'] = "1"
st_data.loc[st_data.WAR.between(3.5,4.25), 'pitcher_num'] = "2"
st_data.loc[st_data.WAR.between(2.75,3.5), 'pitcher_num'] = "3"
st_data.loc[st_data.WAR.between(2,2.75), 'pitcher_num'] = "4"
st_data.loc[st_data.WAR.between(1.25,2), 'pitcher_num'] = "5"
st_data.loc[st_data.WAR < 1.25, 'pitcher_num'] = "AAA"

st_data_war.loc[st_data_war.WAR > 4.99, 'pitcher_num'] = "Ace"
st_data_war.loc[st_data_war.WAR.between(4.25,4.99), 'pitcher_num'] = "1"
st_data_war.loc[st_data_war.WAR.between(3.5,4.25), 'pitcher_num'] = "2"
st_data_war.loc[st_data_war.WAR.between(2.75,3.5), 'pitcher_num'] = "3"
st_data_war.loc[st_data_war.WAR.between(2,2.75), 'pitcher_num'] = "4"
st_data_war.loc[st_data_war.WAR.between(1.25,2), 'pitcher_num'] = "5"
st_data_war.loc[st_data_war.WAR < 1.25, 'pitcher_num'] = "AAA"

st_data_q1_war = st_data['WAR'].quantile(.25)
st_data_q3_war = st_data['WAR'].quantile(.75)

st_data_IQR = st_data_q3_war - st_data_q1_war

st_low_outlier = st_data_q1_war - (1.5 * st_data_IQR)
st_high_outlier = st_data_q3_war + (1.5 * st_data_IQR)

st_data = st_data[st_data['WAR'] < st_high_outlier]
st_data = st_data[st_data['WAR'] > st_low_outlier]

re_data_q1_war = re_data['WAR'].quantile(.25)
re_data_q3_war = re_data['WAR'].quantile(.75)

re_data_IQR = re_data_q3_war - re_data_q1_war

re_low_outlier = re_data_q1_war - (1.5 * re_data_IQR)
re_high_outlier = re_data_q3_war + (1.5 * re_data_IQR)

re_data = re_data[re_data['WAR'] < re_high_outlier]
re_data = re_data[re_data['WAR'] > re_low_outlier]

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
war_IP_diff = pd.DataFrame(columns=['IP', 'Age'])

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
war_IP_diff['WAR'] = st_age_mean['WAR'] - re_age_mean['WAR']
war_IP_diff['IP'] = st_age_mean['IP'] - re_age_mean['IP']
war_IP_diff['WAR/IP'] = war_IP_diff['WAR']/war_IP_diff['IP']
war_IP_diff['Age'] = st_age_mean['Age']
    
st_age_mean.drop(columns=['Name','Season','Team'], inplace=True)
re_age_mean.drop(columns=['Name','Season','Team'], inplace=True)

fig, axes = plt.subplots(1, 3, sharey=True, figsize=((30,7)), constrained_layout=True)
sns.stripplot(ax=axes[0], data=st_data_velo, x="Age", y="FBv", size=4, hue="pitcher_num", hue_order=['Ace','1','2','3','4','5','AAA'], palette="coolwarm_r", linewidth=0).set_title("FB velocity range by age for starters");
axes[0].set_ylabel("FB velocity");
axes[0].legend(title="Rotation spot");
sns.stripplot(ax=axes[1], data=re_data_velo, x="Age", y="FBv", size=4, color="purple", linewidth=0).set_title("FB velocity range by age for relievers");
axes[1].set_ylabel(": ");
sns.regplot(ax=axes[2], data=st_age_mean_velo, x="Age", y="FBv", color="blue").set_title("Starter vs Reliever average FB velocity by age");
sns.regplot(ax=axes[2], data=re_age_mean_velo, x="Age", y="FBv", color="purple");
axes[2].set_ylabel(": ");
axes[2].set_xticks(np.arange(19,49,1));
axes[0].axhline(y=st_data_velo['FBv'].mean(), color="blue", linestyle='dashed');
axes[1].axhline(y=re_data_velo['FBv'].mean(), color="purple", linestyle='dashed');
axes[2].axhline(y=st_data_velo['FBv'].mean(), color="blue", linestyle='dashed');
axes[2].axhline(y=re_data_velo['FBv'].mean(), color="purple", linestyle='dashed');
axes[2].legend(['Starter', 'Reliever', str(round(st_data_velo['FBv'].mean(),1)), str(round(re_data_velo['FBv'].mean(),1))]);

fig2, axes2 = plt.subplots(1, 3, sharey=True, figsize=((30,7)), constrained_layout=True)
sns.stripplot(ax=axes2[0], data=st_data, x="Age", y="WAR", size=4, hue="pitcher_num", hue_order=['Ace','1','2','3','4','5','AAA'], palette="coolwarm_r", linewidth=0).set_title("fWAR by age for starters");
axes2[0].set_ylabel("fWAR");
axes2[0].legend(title="Rotation spot");
sns.stripplot(ax=axes2[1], data=re_data, x="Age", y="WAR", size=4, color="purple", linewidth=0).set_title("fWAR by age for relievers");
axes2[1].set_ylabel(": ");
sns.regplot(ax=axes2[2], data=st_age_mean, x="Age", y="WAR", color="blue").set_title("Starter vs Reliever average fWAR by age");
sns.regplot(ax=axes2[2], data=re_age_mean, x="Age", y="WAR", color="purple");
axes2[2].set_ylabel(": ");
axes2[2].set_xticks(np.arange(19,49,1));
axes2[0].axhline(y=st_data['WAR'].mean(), color="blue", linestyle='dashed');
axes2[1].axhline(y=re_data['WAR'].mean(), color="purple", linestyle='dashed');
axes2[2].axhline(y=st_data['WAR'].mean(), color="blue", linestyle='dashed');
axes2[2].axhline(y=re_data['WAR'].mean(), color="purple", linestyle='dashed');
axes2[2].legend(['Starter', 'Reliever', str(round(st_data['WAR'].mean(),1)), str(round(re_data['WAR'].mean(),1))]);

fig3, axes3 = plt.subplots(1, 3, sharey=True, figsize=((30,7)), constrained_layout=True)
sns.stripplot(ax=axes3[0], data=st_data, x="Age", y="WAR_over_IP", size=4, hue="pitcher_num", hue_order=['Ace','1','2','3','4','5','AAA'], palette="coolwarm_r", linewidth=0).set_title("fWAR/IP by age for starters");
axes3[0].set_ylabel("fWAR");
axes3[0].legend(title="Rotation spot");
sns.stripplot(ax=axes3[1], data=re_data, x="Age", y="WAR_over_IP", size=4, color="purple", linewidth=0).set_title("fWAR/IP by age for relievers");
axes3[1].set_ylabel(": ");
sns.regplot(ax=axes3[2], data=st_age_mean, x="Age", y="WAR_over_IP", color="blue").set_title("Starter vs Reliever average fWAR/IP by age ");
sns.regplot(ax=axes3[2], data=re_age_mean, x="Age", y="WAR_over_IP", color="purple");
axes3[2].set_ylabel(": ");
axes3[2].set_xticks(np.arange(19,49,1));
axes3[0].axhline(y=st_data['WAR_over_IP'].mean(), color="blue", linestyle='dashed');
axes3[1].axhline(y=re_data['WAR_over_IP'].mean(), color="purple", linestyle='dashed');
axes3[2].axhline(y=st_data['WAR_over_IP'].mean(), color="blue", linestyle='dashed');
axes3[2].axhline(y=re_data['WAR_over_IP'].mean(), color="purple", linestyle='dashed');
axes3[2].legend(['Starter', 'Reliever', str(round(st_data['WAR_over_IP'].mean(),4)), str(round(re_data['WAR_over_IP'].mean(),4))]);

fig4, axes4 = plt.subplots(1, 3, sharey=True, figsize=((30,7)), constrained_layout=True)
sns.stripplot(ax=axes4[0], data=st_data, x="Age", y="IP", size=4, hue="pitcher_num", hue_order=['Ace','1','2','3','4','5','AAA'], palette="coolwarm_r", linewidth=0).set_title("IP by age for starters");
axes4[0].set_ylabel("IP");
axes4[0].legend(title="Rotation spot");
sns.stripplot(ax=axes4[1], data=re_data, x="Age", y="IP", size=4, color="purple", linewidth=0).set_title("IP by age for relievers");
axes4[1].set_ylabel(": ");
sns.regplot(ax=axes4[2], data=st_age_mean, x="Age", y="IP", color="blue").set_title("Starter vs Reliever average IP by age");
sns.regplot(ax=axes4[2], data=re_age_mean, x="Age", y="IP", color="purple");
axes4[2].set_ylabel(": ");
axes4[2].set_xticks(np.arange(19,49,1));
axes4[0].axhline(y=st_data['IP'].mean(), color="blue", linestyle='dashed');
axes4[1].axhline(y=re_data['IP'].mean(), color="purple", linestyle='dashed');
axes4[2].axhline(y=st_data['IP'].mean(), color="blue", linestyle='dashed');
axes4[2].axhline(y=re_data['IP'].mean(), color="purple", linestyle='dashed');
axes4[2].legend(['Starter', 'Reliever', str(round(st_data['IP'].mean(),1)), str(round(re_data['IP'].mean(),1))]);

fig5, axes5 = plt.subplots(1, 3, figsize=((30,7)), constrained_layout=True)
sns.regplot(ax=axes5[0], data=war_diff, x="Age", y="WAR", color="orange").set_title("Average starter WAR minus Average reliever WAR by age");
sns.regplot(ax=axes5[1], data=velo_diff, x="Age", y="FBv", color="orange").set_title("Average starter FB velocity minus Average reliever FB velocity by age");
sns.regplot(ax=axes5[2], data=war_IP_diff, x="Age", y="WAR/IP", color="orange").set_title("Average starter WAR/IP minus Average reliever WAR/IP by age");
axes5[0].set_ylabel("WAR");
axes5[1].set_ylabel("Fastball Velocity");
axes5[2].set_ylabel("Innings Pitched");
axes5[0].set_xticks(np.arange(19,45,1));
axes5[1].set_xticks(np.arange(19,45,1));
axes5[2].set_xticks(np.arange(19,45,1));

fig6, axes6 = plt.subplots(1, 1, figsize=((30,7)), constrained_layout=True)
sns.swarmplot(ax=axes6, data=st_data_war, x="Age", y="WAR", size=3, hue="pitcher_num", hue_order=['Ace','1','2','3','4','5','AAA'], palette="coolwarm_r", linewidth=0).set_title("fWAR by age for starters");
axes6.legend(title="Rotation spot")
axes6.axhline(y=5, color="#dc5e4b", linestyle='dashed');
axes6.axhline(y=4.26, color="#f39879", linestyle='dashed');
axes6.axhline(y=3.51, color="#f4c3ab", linestyle='dashed');
axes6.axhline(y=2.76, color="#dddcdb", linestyle='dashed');
axes6.axhline(y=2.01, color="#b8cff8", linestyle='dashed');
axes6.axhline(y=1.26, color="#8daffd", linestyle='dashed');

plt.show()
