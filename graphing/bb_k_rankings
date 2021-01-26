# This graph shows where a team's players rank amongst the rest of the league in BB%/K%.
#
# I exported a CSV sheet from FanGraphs and used that for the data.
#
# This particular sheet took any player who had 100 PA in a given season then the graphs
# separated them out by each year. Otherwise it was very, very crowded and hard to read.

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

team = input("Type in your team's nickname please (e.g. Nationals, Blue Jays, etc): ")

data = pd.read_csv('/location/of/csv_file.csv')
data.sort_values(by=['BB%'], inplace=True)
data['BB%'] = data['BB%'].map(lambda x: x.rstrip('%'))
data['K%'] = data['K%'].map(lambda x: x.rstrip('%'))

data['BB%'] = data['BB%'].astype(float)
data['K%'] = data['K%'].astype(float)

data.drop(columns=['Name', 'playerid'], inplace=True)
player_team = data[data['Team'] == team]

columns = ('BB%', 'K%')

league_2015 = data[data['Season'] == 2015]
player_team_2015 = player_team[player_team['Season'] == 2015]
league_2016 = data[data['Season'] == 2016]
player_team_2016 = player_team[player_team['Season'] == 2016]
league_2017 = data[data['Season'] == 2017]
player_team_2017 = player_team[player_team['Season'] == 2017]
league_2018 = data[data['Season'] == 2018]
player_team_2018 = player_team[player_team['Season'] == 2018]
league_2019 = data[data['Season'] == 2019]
player_team_2019 = player_team[player_team['Season'] == 2019]
league_2020 = data[data['Season'] == 2020]
player_team_2020 = player_team[player_team['Season'] == 2020]

x_label = ('0%','3%','6%','9%','12%','15%','18%','21%')
y_label = ('0%','5%','10%','15%','20%','25%','30%','35%','40%','45%','50%')

fig, axes = plt.subplots(2, 3, figsize=((15,10)))

sns.scatterplot(ax=axes[0,0], data=league_2015, x="BB%", y="K%").set_title("2015 BB%/K% rates")
sns.scatterplot(ax=axes[0,0], data=player_team_2015, x="BB%", y="K%")
sns.scatterplot(ax=axes[0,1], data=league_2016, x="BB%", y="K%").set_title("2016 BB%/K% rates")
sns.scatterplot(ax=axes[0,1], data=player_team_2016, x="BB%", y="K%")
sns.scatterplot(ax=axes[0,2], data=league_2017, x="BB%", y="K%").set_title("2017 BB%/K% rates")
sns.scatterplot(ax=axes[0,2], data=player_team_2017, x="BB%", y="K%")
sns.scatterplot(ax=axes[1,0], data=league_2018, x="BB%", y="K%").set_title("2018 BB%/K% rates")
sns.scatterplot(ax=axes[1,0], data=player_team_2018, x="BB%", y="K%")
sns.scatterplot(ax=axes[1,1], data=league_2019, x="BB%", y="K%").set_title("2019 BB%/K% rates")
sns.scatterplot(ax=axes[1,1], data=player_team_2019, x="BB%", y="K%")
sns.scatterplot(ax=axes[1,2], data=league_2020, x="BB%", y="K%").set_title("2020 BB%/K% rates")
sns.scatterplot(ax=axes[1,2], data=player_team_2020, x="BB%", y="K%")

fig.tight_layout(pad=3.0)

axes[0,0].set_xticks(np.arange(0,(max(data['BB%'])+3),3))
axes[0,1].set_xticks(np.arange(0,(max(data['BB%'])+3),3))
axes[0,2].set_xticks(np.arange(0,(max(data['BB%'])+3),3))
axes[1,0].set_xticks(np.arange(0,(max(data['BB%'])+3),3))
axes[1,1].set_xticks(np.arange(0,(max(data['BB%'])+3),3))
axes[1,2].set_xticks(np.arange(0,(max(data['BB%'])+3),3))

axes[0,0].set_yticks(np.arange(0,(max(data['K%'])+5),5))
axes[0,1].set_yticks(np.arange(0,(max(data['K%'])+5),5))
axes[0,2].set_yticks(np.arange(0,(max(data['K%'])+5),5))
axes[1,0].set_yticks(np.arange(0,(max(data['K%'])+5),5))
axes[1,1].set_yticks(np.arange(0,(max(data['K%'])+5),5))
axes[1,2].set_yticks(np.arange(0,(max(data['K%'])+5),5))

axes[0,0].set_xticklabels(rotation=45, labels=x_label)
axes[0,1].set_xticklabels(rotation=45, labels=x_label)
axes[0,2].set_xticklabels(rotation=45, labels=x_label)
axes[1,0].set_xticklabels(rotation=45, labels=x_label)
axes[1,1].set_xticklabels(rotation=45, labels=x_label)
axes[1,2].set_xticklabels(rotation=45, labels=x_label)

axes[0,0].set_yticklabels(rotation=45, labels=y_label)
axes[0,1].set_yticklabels(rotation=45, labels=y_label)
axes[0,2].set_yticklabels(rotation=45, labels=y_label)
axes[1,0].set_yticklabels(rotation=45, labels=y_label)
axes[1,1].set_yticklabels(rotation=45, labels=y_label)
axes[1,2].set_yticklabels(rotation=45, labels=y_label)

plt.show()
