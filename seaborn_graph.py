# In an effort to familiarize myself with multiple graphing modules, I did the sort of graph as I did in matplotlib.py
# but with seaborn. I found seaborn to be a bit more simple from a coding perspective; but a lot more resource intensive.

import pandas as pd
import pymysql.cursors
import getpass
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt

# A few variables needed to continue on
print("Enter your MySQL password: "), 
mysql_pass = getpass.getpass()
name = input("Specify the last name of the player: ")
year = input("Select a year: ")

# This is to connect to a local MySQL connection. Will need to fill in host and user here between the ''
connection = pymysql.connect(host='',
                             user='',
                             password=mysql_pass,
                             db='hit_probability',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

# This is the section where the queries are ran to get the needed data. It runs the queries and then keeps the data in a Pandas DataFrame
try:
    with connection.cursor() as cursor:
        sql_mode = "SET SESSION sql_mode=''"
        cursor.execute(sql_mode)
        ev_table = "CREATE TEMPORARY TABLE ev SELECT DISTINCT ev FROM prob WHERE year = "+year+";"
        cursor.execute(ev_table)
        la_table = "CREATE TEMPORARY TABLE launch_angle SELECT DISTINCT launch_angle FROM prob WHERE year = "+year+";"
        cursor.execute(la_table)
        data_query = "SELECT ev, launch_angle, n_hip, n_hits, woba FROM prob WHERE year = "+year+" AND ev > 0 ORDER BY year, ev, launch_angle;"
        ev_query = "SELECT DISTINCT COUNT(ev) FROM ev;"
        la_query = "SELECT DISTINCT COUNT(launch_angle) FROM launch_angle;"
        data = pd.read_sql(data_query, connection)
        ev_data = pd.read_sql(ev_query, connection)
        la_data = pd.read_sql(la_query, connection)
        player_query = "SELECT ev, launch_angle, hit FROM player WHERE at_bat > 0 AND player_name LIKE '"+name+"%' AND YEAR(game_date) = "+year+" AND ball_in_play > 0 AND ev > 0;"
        player_data = pd.read_sql(player_query, connection)
        player_data.loc[player_data['hit'] == 0, 'hit'] = 'out'
        player_data.loc[player_data['hit'] == 1, 'hit'] = 'hit'
finally:
    connection.close()
    
# Using this to make sure the correct number of bins are displayed each time
ev_int = int(ev_data.iloc[0])
la_int = int(la_data.iloc[0])

# I realized you have the option to save the graph without needing to do so via the script. So I left that out here.
# This graph also shows the difference between hits and outs for the balls in play.
# I also need to work on the legend. For some reason there is an extra label in there...
sns.displot(data, x="ev", y="launch_angle", hue="woba", bins=(109,176), weights="woba", palette="Reds", height=6, aspect=1.5, legend=False)
sns.scatterplot(data=player_data, x="ev", y="launch_angle", hue="hit", size=1, palette="Purples", legend='full')
plt.legend(bbox_to_anchor=(1.01, 1), borderaxespad=0)
plt.xlabel('EV')
plt.ylabel('Launch Angle')
plt.title("EV and LA histogram with "+name+" BIP overlay for "+year)
plt.savefig('/Users/jerrymckennan/Desktop/seaborn_graph.png', facecolor='white')
plt.show()
