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
save = input("Save plot as picture, yes or no?: ")

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
        ev_table = "CREATE TEMPORARY TABLE ev SELECT ev FROM prob WHERE year = "+year+";"
        cursor.execute(ev_table)
        la_table = "CREATE TEMPORARY TABLE launch_angle SELECT launch_angle FROM prob WHERE year = "+year+";"
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
    
# This is based on the variable answered in the beginning. 
if answer == "wOBA":
    weighted_data = data["woba"].to_numpy()
if answer == "hits":
    weighted_data = data["n_hip"].to_numpy()

# This is the graphing section
# The bins need to change occassionally otherwise the data doesn't look as sharp. I'm still working on making that as a variable
plt.hist2d(ev_data_use, la_data_use, bins=(109,176), cmap=plt.cm.Reds, weights=weighted_data)
plt.plot(player_ev_data, player_la_data, linestyle='none', marker='.', c="darkorange", markersize=3, label=player_name_data)
plt.xlabel('EV')
plt.ylabel('Launch Angle')

# This will save the graph as if you answered yes at the beginning. Otherwise it just displays it.
if save == "yes":
    location = input("Enter location and file name to save graph: ")
    # Add a basic title
    plt.title("EV and LA histogram with "+name1+" BIP overlay for "+year)
    plt.savefig(location, facecolor='white')
    plt.show()
else:
    # Add a basic title
    plt.title("EV and LA histogram with "+name1+" BIP overlay for "+year)
    plt.show()
