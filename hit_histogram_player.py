# This Python script uses data queried from the database to create a histogram chart for either hits or wOBA based on LA and EV
# Then it allows you to also gather the same data for a specific player that you can then use in a scatter chart over top of the
# histogram

import numpy as np
import pandas as pd
import pymysql.cursors
import getpass
import matplotlib
import matplotlib.pyplot as plt

answer = input("Select wOBA or hits: ")

mysql_pass = getpass.getpass()

# Make sure to update this information for your personal set up. Specifically host, user, and db sections
connection = pymysql.connect(host='localhost',
                             user='username',
                             password=mysql_pass,
                             db='hit_probability',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

# These are the queries. You'll want to update the year for each one and update the player_name variable to ensure you get the data you want.
# I might play with making these variables that you can fill in at the beginning.
try:
    with connection.cursor() as cursor:
        sql_mode = "SET SESSION sql_mode=''"
        cursor.execute(sql_mode)
        ev_table = "CREATE TEMPORARY TABLE ev SELECT ev FROM prob WHERE year = 2019;"
        cursor.execute(ev_table)
        la_table = "CREATE TEMPORARY TABLE launch_angle SELECT launch_angle FROM prob WHERE year = 2019;"
        cursor.execute(la_table)
        ev_query = "SELECT DISTINCT ev FROM ev;"
        la_query = "SELECT DISTINCT launch_angle FROM launch_angle;"
        data_query = "SELECT ev, launch_angle, n_hip, n_hits, woba FROM prob WHERE year = 2019 AND ev > 0 ORDER BY year, ev, launch_angle;"
        ev_data = pd.read_sql(ev_query, connection)
        la_data = pd.read_sql(la_query, connection)
        data = pd.read_sql(data_query, connection)
        player_query = "SELECT ev, launch_angle, hit FROM player WHERE at_bat > 0 AND player_name LIKE 'schwarber%' AND YEAR(game_date) = 2019 AND ball_in_play > 0;"
        player_data = pd.read_sql(player_query, connection)
finally:
    connection.close()

# Converts the data from above to NumPy for graphing purposes
ev_data_label = ev_data.to_numpy()
la_data_label = la_data.to_numpy()
ev_data_use = data["ev"].to_numpy()
la_data_use = data["launch_angle"].to_numpy()
player_ev_data = player_data["ev"].to_numpy()
player_la_data = player_data["launch_angle"].to_numpy()
    
if answer == "wOBA":
    weighted_data = data["woba"].to_numpy()
if answer == "hits":
    weighted_data = data["n_hip"].to_numpy()

plt.hist2d(ev_data_use, la_data_use, bins=(50, 50), cmap=plt.cm.Reds, weights=weighted_data)
plt.plot(player_ev_data, player_la_data, linestyle='none', marker='.', c='darkorange', markersize=3)
plt.xlabel('EV')
plt.ylabel('Launch Angle')
 
# Adds a basic title, would need to be updated. Perhap use an Input variable here to get the name correct each time
plt.title("EV and LA histogram with Schwarber BIP overlay for 2019")
plt.show()
