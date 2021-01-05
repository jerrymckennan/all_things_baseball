# This is my first plotting script using matplotlib. It's a histogram map for the hits of over the course of a season
# and the coloring is dependent on either the number of hits or the wOBA for each Launch Angle and Exit Velocity combo.
# Then it plots the points of a ball-in-play for a given player in the same year.

import numpy as np
import pandas as pd
import pymysql.cursors
import getpass
import matplotlib
import matplotlib.pyplot as plt

# A few variables needed to continue on
print("Enter your MySQL password: "), 
mysql_pass = getpass.getpass()
answer = input("Select wOBA or hits: ")
name1 = input("Specify the last name of the first player: ")
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
        ev_query = "SELECT DISTINCT ev FROM ev;"
        la_query = "SELECT DISTINCT launch_angle FROM launch_angle;"
        data_query = "SELECT ev, launch_angle, n_hip, n_hits, woba FROM prob WHERE year = "+year+" AND ev > 0 ORDER BY year, ev, launch_angle;"
        ev_data = pd.read_sql(ev_query, connection)
        la_data = pd.read_sql(la_query, connection)
        data = pd.read_sql(data_query, connection)
        player_query = "SELECT ev, launch_angle, player_name FROM player WHERE at_bat > 0 AND player_name LIKE '"+name1+"%' AND YEAR(game_date) = "+year+" AND ball_in_play > 0;"
        player_data = pd.read_sql(player_query, connection)
finally:
    connection.close()

# For graphing purposes, the data is then converted over to a NumPy array
ev_data_label = ev_data.to_numpy()
la_data_label = la_data.to_numpy()
ev_data_use = data["ev"].to_numpy()
la_data_use = data["launch_angle"].to_numpy()
player_ev_data = player_data["ev"].to_numpy()
player_la_data = player_data["launch_angle"].to_numpy()
player_name_data = player_data["player_name"]

# Using this to make sure the correct number of bins are displayed each time
ev_int = int(ev_data.iloc[0])
la_int = int(la_data.iloc[0])
    
# This is based on the variable answered in the beginning. 
if answer == "wOBA":
    weighted_data = data["woba"].to_numpy()
if answer == "hits":
    weighted_data = data["n_hip"].to_numpy()

# This is the graphing section
plt.hist2d(ev_data_use, la_data_use, bins=(ev_int,la_int), cmap=plt.cm.Reds, weights=weighted_data)
plt.plot(player_ev_data, player_la_data, linestyle='none', marker='.', c="darkorange", markersize=3, label=player_name_data)
plt.xlabel('EV')
plt.ylabel('Launch Angle')
plt.title("EV and LA histogram with "+name1+" BIP overlay for "+year)
plt.show()
