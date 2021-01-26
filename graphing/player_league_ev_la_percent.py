# This graph will get a percentage for each EV and LA on balls in play for a player,
# then it will do the same for league wide and put all four in their own scatterplots.

import pandas as pd
import seaborn as sns
import pymysql.cursors
import getpass
import os.path
import matplotlib.pyplot as plt

# A few variables needed to continue on
print("Enter your MySQL password: "), 
mysql_pass = getpass.getpass()
year = input("Please enter a year: ")
player_name = input("Please enter a player name: ")

# This is to connect to a local MySQL connection. Will need to fill in host and user here between the ''
connection = pymysql.connect(host='localhost',
                             user='root',
                             password=mysql_pass,
                             db='hit_probability',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

try:
    with connection.cursor() as cursor:
        player_ev_data = "SELECT DISTINCT p1.ev, (SELECT DISTINCT SUM(ball_in_play) AS bip FROM player AS p2 WHERE p1.ev = p2.ev AND YEAR(p1.game_date) = YEAR(p2.game_date) AND p1.player_name = p2.player_name) AS bip, (SELECT SUM(ball_in_play) AS total_bip FROM player AS p3 WHERE p1.player_name = p3.player_name AND YEAR(p1.game_date) = YEAR(p3.game_date)) AS total_bip, ((SELECT DISTINCT SUM(ball_in_play) AS bip FROM player AS p2 WHERE p1.ev = p2.ev AND YEAR(p1.game_date) = YEAR(p2.game_date) AND p1.player_name = p2.player_name)/(SELECT SUM(ball_in_play) AS total_bip FROM player AS p3 WHERE p1.player_name = p3.player_name AND YEAR(p1.game_date) = YEAR(p3.game_date))*100) AS perc FROM player AS p1 WHERE ev > 0 AND p1.player_name LIKE '"+player_name+"%' AND YEAR(p1.game_date) = "+year+" ORDER BY p1.ev;"
        league_ev_data = "SELECT DISTINCT ev, SUM(n_hip) as bip, (SELECT DISTINCT SUM(n_hip) FROM prob as p2 WHERE ev > 0 AND p2.year = p1.year) AS total_bip, (SUM(n_hip)/(SELECT DISTINCT SUM(n_hip) FROM prob as p2 WHERE ev > 0 AND p2.year = p1.year)*100) AS perc FROM prob AS p1 WHERE ev > 0 AND year = "+year+" GROUP BY year, ev ORDER BY ev;"
        player_la_data = "SELECT DISTINCT p1.launch_angle, (SELECT DISTINCT SUM(ball_in_play) AS bip FROM player AS p2 WHERE p1.launch_angle = p2.launch_angle AND YEAR(p1.game_date) = YEAR(p2.game_date) AND p1.player_name = p2.player_name) AS bip, (SELECT SUM(ball_in_play) AS total_bip FROM player AS p3 WHERE p1.player_name = p3.player_name AND YEAR(p1.game_date) = YEAR(p3.game_date)) AS total_bip, ((SELECT DISTINCT SUM(ball_in_play) AS bip FROM player AS p2 WHERE p1.launch_angle = p2.launch_angle AND YEAR(p1.game_date) = YEAR(p2.game_date) AND p1.player_name = p2.player_name)/(SELECT SUM(ball_in_play) AS total_bip FROM player AS p3 WHERE p1.player_name = p3.player_name AND YEAR(p1.game_date) = YEAR(p3.game_date))*100) AS perc FROM player AS p1 WHERE ev > 0 AND p1.player_name LIKE '"+player_name+"%' AND YEAR(p1.game_date) = "+year+" ORDER BY p1.launch_angle;"
        league_la_data = "SELECT DISTINCT launch_angle, SUM(n_hip) as bip, (SELECT DISTINCT SUM(n_hip) FROM prob as p2 WHERE ev > 0 AND p2.year = p1.year) AS total_bip, (SUM(n_hip)/(SELECT DISTINCT SUM(n_hip) FROM prob as p2 WHERE ev > 0 AND p2.year = p1.year)*100) AS perc FROM prob AS p1 WHERE ev > 0 AND year = "+year+" GROUP BY year, launch_angle ORDER BY launch_angle;"
        player_ev_data = pd.read_sql(player_ev_data, connection)
        league_ev_data = pd.read_sql(league_ev_data, connection)
        player_la_data = pd.read_sql(player_la_data, connection)
        league_la_data = pd.read_sql(league_la_data, connection)
        player_ev_data["who"] = player_name
        league_ev_data["who"] = "league"
        player_la_data["who"] = player_name
        league_la_data["who"] = "league"
except pymysql.err.OperationalError:
    # This is if the MySQL Server is not yet started
    print("MySQL Server is currently shutdown. Let me start that for you.")
    os.system('mysql.server start')
    print("MySQL Server should be up and running.")
finally:
    connection.close()

# Creates the subplots and individual plots. Included in the individual plots is the location on the larger plot specified with the fig, axes variable
fig, axes = plt.subplots(2, 2, sharey='col', sharex='col', figsize=((20,9)))
                
sns.scatterplot(ax=axes[0,0], data=player_ev_data, x="ev", y="perc", hue="perc", hue_norm=(0,4), palette="seismic", legend='brief').set_title(player_name+" EV data for "+year, fontsize=9)
sns.scatterplot(ax=axes[1,0], data=league_ev_data, x="ev", y="perc", hue="perc", hue_norm=(0,4), palette="seismic", legend='brief').set_title("League EV data for "+year, fontsize=9)
sns.scatterplot(ax=axes[0,1], data=player_la_data, x="launch_angle", y="perc", hue="perc", hue_norm=(0,4), palette="seismic", legend='brief').set_title(player_name+" LA data for "+year, fontsize=9)
sns.scatterplot(ax=axes[1,1], data=league_la_data, x="launch_angle", y="perc", hue="perc", hue_norm=(0,4), palette="seismic", legend='brief').set_title("League LA data for "+year, fontsize=9)

fig.suptitle("Percentage of BIP that match Exit Velocity and Launch Angle for "+player_name+" vs league average", fontsize=15)

plt.show()
