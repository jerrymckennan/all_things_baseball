# This will plot the number of balls in play, hits, and probable hits based on the EV and LA of each BIP for two players in a year

import pandas as pd
import numpy as np
import seaborn as sns
import pymysql.cursors
import getpass
import os.path
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.patches as mpatches
from matplotlib.dates import date2num, num2date
from datetime import datetime

# A few variables needed to continue on
print("Enter your MySQL password: "), 
mysql_pass = getpass.getpass()
year = input("Enter year: ")
player_name = input("Enter player: ")
player_name2 = input("Enter player: ")

while True:
    try:
        # Creates the connection to the MySQL database
        connection = pymysql.connect(host=hostname,
                             user=username,
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
            
    connection = pymysql.connect(host='localhost',
                     user='root',
                     password=mysql_pass,
                     db='hit_probability',
                     charset='utf8mb4',
                     cursorclass=pymysql.cursors.DictCursor)
try:
    with connection.cursor() as cursor:
        sql_mode = "SET SQL_MODE = ''"
        cursor.execute(sql_mode)
        temp_table = "CREATE TEMPORARY TABLE test SELECT py.player_name, py.game_date, py.distance, py.ball_in_play AS bip, pr.ev, pr.launch_angle, pr.hits_1b_per_hip, py.is_1b, pr.hits_2b_per_hip, py.is_2b, pr.hits_3b_per_hip, py.is_3b, pr.hits_hr_per_hip, py.is_hr FROM player AS py JOIN prob AS pr ON pr.year = YEAR(py.game_date) WHERE pr.ev = py.ev AND pr.launch_angle = py.launch_angle GROUP BY py.game_date, py.player_name, py.game_date, py.ab_num, event ORDER BY py.game_date;"
        cursor.execute(temp_table)
        data = "SELECT p1.game_date, p1.player_name, (SELECT SUM(p3.ball_in_play) FROM player AS p3 WHERE p3.player_name = p1.player_name AND p3.game_date <= p1.game_date AND p3.game_date >= '"+year+"-03-01') AS counting_bip, (SELECT SUM(p2.hit) FROM player AS p2 WHERE p2.player_name = p1.player_name AND p2.game_date >= '"+year+"-03-01' AND p2.game_date <= p1.game_date) AS counting_hits, (SELECT ROUND((SUM(hits_1b_per_hip)/100)+(SUM(hits_2b_per_hip)/100)+(SUM(hits_3b_per_hip)/100)+(SUM(hits_hr_per_hip)/100),0) FROM test AS t WHERE t.player_name = p1.player_name AND t.game_date <= p1.game_date AND t.game_date >= '"+year+"-03-01') as prob_hits FROM player AS p1 WHERE p1.player_name LIKE '"+player_name+"' AND p1.game_date > '"+year+"-03-01' AND p1.game_date < '"+year+"-09-30' GROUP BY p1.game_date, p1.player_name;"
        data2 = "SELECT p1.game_date, p1.player_name, (SELECT SUM(p3.ball_in_play) FROM player AS p3 WHERE p3.player_name = p1.player_name AND p3.game_date <= p1.game_date AND p3.game_date >= '"+year+"-03-01') AS counting_bip, (SELECT SUM(p2.hit) FROM player AS p2 WHERE p2.player_name = p1.player_name AND p2.game_date >= '"+year+"-03-01' AND p2.game_date <= p1.game_date) AS counting_hits, (SELECT ROUND((SUM(hits_1b_per_hip)/100)+(SUM(hits_2b_per_hip)/100)+(SUM(hits_3b_per_hip)/100)+(SUM(hits_hr_per_hip)/100),0) FROM test AS t WHERE t.player_name = p1.player_name AND t.game_date <= p1.game_date AND t.game_date >= '"+year+"-03-01') as prob_hits FROM player AS p1 WHERE p1.player_name LIKE '"+player_name2+"' AND p1.game_date > '"+year+"-03-01' AND p1.game_date < '"+year+"-9-30' GROUP BY p1.game_date, p1.player_name;"
        player_data = pd.read_sql(data, connection)
        player2_data = pd.read_sql(data2, connection)
except pymysql.err.OperationalError:
    # This is if the MySQL Server is not yet started
    print("MySQL Server is currently shutdown. Let me start that for you.")
    os.system('mysql.server start')
    print("MySQL Server should be up and running.")
finally:
    connection.close()

player_data = player_data.append(player2_data)
fig, axes = plt.subplots(1, 3, figsize=((50,12)))

sns.lineplot(ax=axes[0], data=player_data, x="game_date", y="counting_bip", hue="player_name", legend="full").set_title(player_name+" vs "+player_name2+" balls in play by date for year "+year)
sns.lineplot(ax=axes[1], data=player_data, x="game_date", y="counting_hits", hue="player_name", legend="full").set_title(player_name+" vs "+player_name2+" hits by date for year "+year)
sns.lineplot(ax=axes[2], data=player_data, x="game_date", y="prob_hits", hue="player_name", legend="full").set_title(player_name+" vs "+player_name2+" probable hits by date for year "+year)

axes[0].get_yaxis().set_visible(True)
axes[0].set_yticks(np.arange(0,600,25))
sns.despine(ax=axes[0], top=True, right=True)
axes[1].get_yaxis().set_visible(True)
axes[1].set_yticks(np.arange(0,600,25))
sns.despine(ax=axes[1], top=True, right=True)
axes[2].get_yaxis().set_visible(True)
axes[2].set_yticks(np.arange(0,600,25))
sns.despine(ax=axes[2], top=True, right=True)
