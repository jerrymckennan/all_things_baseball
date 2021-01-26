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
# It will check to make sure the MySQL server is up. Since mine is local on my laptop, I don't always have 
# it running. It will also check on the password letting your re-enter without needing to re-run the script.
while True:
    try:
        # Creates the connection to the MySQL database
        connection = pymysql.connect(host='',
                             user='',
                             password=mysql_pass,
                             db='hit_probability',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
        break

    except pymysql.err.OperationalError as e:
        err_no = e.args[0]
        print(err_no)
        # This is for if MySQL server is shutdown
        if err_no == 2003:
            print("MySQL Server is currently shutdown. Let me start that for you.")
            os.system('mysql.server start')
            print("MySQL Server should be up and running.")
        # This is for the wrong password
        if err_no == 1045:
            print("Error with password, re-enter:")
            mysql_pass = getpass.getpass()
    finally:
        connection = pymysql.connect(host='localhost',
                         user='root',
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
        player_query = "SELECT ev, launch_angle, hit, event FROM player WHERE at_bat > 0 AND player_name LIKE '"+name+"%' AND YEAR(game_date) = "+year+" AND ball_in_play > 0 AND ev > 0;"
        player_data = pd.read_sql(player_query, connection)
        player_data.loc[player_data['hit'] == 0, 'hit'] = 'out'
        player_data.loc[player_data['hit'] == 1, 'hit'] = 'hit'
        player_data.loc[player_data['event'] == "field_out", 'event'] = "out"
        player_data.loc[player_data['event'] == "force_out", 'event'] = "out"
        player_data.loc[player_data['event'] == "field_error", 'event'] = "error"
        player_data.loc[player_data['event'] == "sac_fly", 'event'] = "out"
        player_data.loc[player_data['event'] == "fielders_choice", 'event'] = "out"
        player_data.loc[player_data['event'] == "grounded_into_double_play", 'event'] = "out"
        player_data.loc[player_data['event'] == "double_play", 'event'] = "out"
        player_data.loc[player_data['event'] == "sac_bunt", 'event'] = "out"
        player_data.loc[player_data['event'] == "fielders_choice_out", 'event'] = "out"
        player_data.loc[player_data['event'] == "sac_fly_double_play", 'event'] = "out"
        player_data.loc[player_data['event'] == "home_run", 'event'] = "home run"
        # The next 6 is to also increase the size of the dot based on type of hit. It's not used right now, but it is set up to play with.
        player_data.loc[player_data['event'] == "single", 'size'] = (1*.25)
        player_data.loc[player_data['event'] == "double", 'size'] = (2*.25)
        player_data.loc[player_data['event'] == "triple", 'size'] = (3*.25)
        player_data.loc[player_data['event'] == "home run", 'size'] = (4*.25)
        player_data.loc[player_data['event'] == "out", 'size'] = (1*.25)
        player_data.loc[player_data['event'] == "error", 'size'] = (1*.25)
        
finally:
    connection.close()
    
# Using this to make sure the correct number of bins are displayed each time
ev_int = int(ev_data.iloc[0])
la_int = int(la_data.iloc[0])

# This creates a proper legend that includes colors for out, error, and each type of hit
sns.histplot(data, x="ev", y="launch_angle", hue="woba", bins=(ev_int,la_int), weights="woba", palette="Reds", legend='brief')
sns.scatterplot(data=player_data, x="ev", y="launch_angle", hue="event", hue_order=['out', 'error', 'single', 'double', 'triple', 'home run'], palette="flare", legend='full')
plt.legend(bbox_to_anchor=(1.01, 1), borderaxespad=0, loc='upper left')
plt.xlabel('EV')
plt.ylabel('Launch Angle')
plt.title("EV and LA histogram with "+name+" ball in play overlay for "+year)
plt.show()
