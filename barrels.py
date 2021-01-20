import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import getpass
import pymysql.cursors

print("Enter your MySQL password: "), 
mysql_pass = getpass.getpass()

# This is to connect to a local MySQL connection. Will need to fill in host and user here between the ''
connection = pymysql.connect(host='localhost',
                             user='root',
                             password=mysql_pass,
                             db='hit_probability',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

try:
    with connection.cursor() as cursor:
        barrel_data_2015 = "SELECT * FROM barrels WHERE year = 2015 ORDER BY launch_angle;"
        barrel_data_2015 = pd.read_sql(barrel_data_2015, connection)
        non_barrel_data_2015 = "SELECT p1.ev, p1.launch_angle, p1.n_hip FROM prob AS p1 LEFT JOIN barrels AS b1 ON p1.ev = b1.ev AND p1.launch_angle = b1.launch_angle WHERE b1.ev IS NULL and b1.launch_angle IS NULL AND p1.ev > 0 AND p1.year = 2015;"
        non_barrel_data_2015 = pd.read_sql(non_barrel_data_2015, connection)
        barrel_data_2016 = "SELECT * FROM barrels WHERE year = 2016 ORDER BY launch_angle;"
        barrel_data_2016 = pd.read_sql(barrel_data_2016, connection)
        non_barrel_data_2016 = "SELECT p1.ev, p1.launch_angle, p1.n_hip FROM prob AS p1 LEFT JOIN barrels AS b1 ON p1.ev = b1.ev AND p1.launch_angle = b1.launch_angle WHERE b1.ev IS NULL and b1.launch_angle IS NULL AND p1.ev > 0 AND p1.year = 2016;"
        non_barrel_data_2016 = pd.read_sql(non_barrel_data_2016, connection)
        barrel_data_2017 = "SELECT * FROM barrels WHERE year = 2017 ORDER BY launch_angle;"
        barrel_data_2017 = pd.read_sql(barrel_data_2017, connection)
        non_barrel_data_2017 = "SELECT p1.ev, p1.launch_angle, p1.n_hip FROM prob AS p1 LEFT JOIN barrels AS b1 ON p1.ev = b1.ev AND p1.launch_angle = b1.launch_angle WHERE b1.ev IS NULL and b1.launch_angle IS NULL AND p1.ev > 0 AND p1.year = 2017;"
        non_barrel_data_2017 = pd.read_sql(non_barrel_data_2017, connection)
        barrel_data_2018 = "SELECT * FROM barrels WHERE year = 2018 ORDER BY launch_angle;"
        barrel_data_2018 = pd.read_sql(barrel_data_2018, connection)
        non_barrel_data_2018 = "SELECT p1.ev, p1.launch_angle, p1.n_hip FROM prob AS p1 LEFT JOIN barrels AS b1 ON p1.ev = b1.ev AND p1.launch_angle = b1.launch_angle WHERE b1.ev IS NULL and b1.launch_angle IS NULL AND p1.ev > 0 AND p1.year = 2018;"
        non_barrel_data_2018 = pd.read_sql(non_barrel_data_2018, connection)
        barrel_data_2019 = "SELECT * FROM barrels WHERE year = 2019 ORDER BY launch_angle;"
        barrel_data_2019 = pd.read_sql(barrel_data_2019, connection)
        non_barrel_data_2019 = "SELECT p1.ev, p1.launch_angle, p1.n_hip FROM prob AS p1 LEFT JOIN barrels AS b1 ON p1.ev = b1.ev AND p1.launch_angle = b1.launch_angle WHERE b1.ev IS NULL and b1.launch_angle IS NULL AND p1.ev > 0 AND p1.year = 2019;"
        non_barrel_data_2019 = pd.read_sql(non_barrel_data_2019, connection)
        barrel_data_2020 = "SELECT * FROM barrels WHERE year = 2020 ORDER BY launch_angle;"
        barrel_data_2020 = pd.read_sql(barrel_data_2020, connection)
        non_barrel_data_2020 = "SELECT p1.ev, p1.launch_angle, p1.n_hip FROM prob AS p1 LEFT JOIN barrels AS b1 ON p1.ev = b1.ev AND p1.launch_angle = b1.launch_angle WHERE b1.ev IS NULL and b1.launch_angle IS NULL AND p1.ev > 0 AND p1.year = 2020;"
        non_barrel_data_2020 = pd.read_sql(non_barrel_data_2020, connection)
except pymysql.err.OperationalError:
    # This is if the MySQL Server is not yet started
    print("MySQL Server is currently shutdown. Let me start that for you.")
    os.system('mysql.server start')
    print("MySQL Server should be up and running.")
finally:
    connection.close()

# These plots are for barrels compared to the rest of the balls in play
fig, axes = plt.subplots(2, 3, sharey='all', sharex='all', figsize=((40,18)))
sns.scatterplot(ax=axes[0,0], data=barrel_data_2015, x="launch_angle", y="ev", hue="ev", hue_norm=(50,110), palette="seismic", legend=False).set_title("2015 barrel data vs all BIP", fontsize=15)
sns.scatterplot(ax=axes[0,0], data=non_barrel_data_2015, x="launch_angle", y="ev", hue="ev", size=1.5, hue_norm=(70,110), palette="coolwarm", legend=False)
sns.scatterplot(ax=axes[0,1], data=barrel_data_2016, x="launch_angle", y="ev", hue="ev", hue_norm=(50,110), palette="seismic", legend=False).set_title("2016 barrel data vs all BIP", fontsize=15)
sns.scatterplot(ax=axes[0,1], data=non_barrel_data_2016, x="launch_angle", y="ev", hue="ev", size=1.5, hue_norm=(70,110), palette="coolwarm", legend=False)
sns.scatterplot(ax=axes[0,2], data=barrel_data_2017, x="launch_angle", y="ev", hue="ev", hue_norm=(50,110), palette="seismic", legend=False).set_title("2017 barrel data vs all BIP", fontsize=15)
sns.scatterplot(ax=axes[0,2], data=non_barrel_data_2017, x="launch_angle", y="ev", hue="ev", size=1.5, hue_norm=(70,110), palette="coolwarm", legend=False)
sns.scatterplot(ax=axes[1,0], data=barrel_data_2018, x="launch_angle", y="ev", hue="ev", hue_norm=(50,110), palette="seismic", legend=False).set_title("2018 barrel data vs all BIP", fontsize=15)
sns.scatterplot(ax=axes[1,0], data=non_barrel_data_2018, x="launch_angle", y="ev", hue="ev", size=1.5, hue_norm=(70,110), palette="coolwarm", legend=False)
sns.scatterplot(ax=axes[1,1], data=barrel_data_2019, x="launch_angle", y="ev", hue="ev", hue_norm=(50,110), palette="seismic", legend=False).set_title("2019 barrel data vs all BIP", fontsize=15)
sns.scatterplot(ax=axes[1,1], data=non_barrel_data_2019, x="launch_angle", y="ev", hue="ev", size=1.5, hue_norm=(70,110), palette="coolwarm", legend=False)
sns.scatterplot(ax=axes[1,2], data=barrel_data_2020, x="launch_angle", y="ev", hue="ev", hue_norm=(50,110), palette="seismic", legend=False).set_title("2020 barrel data vs all BIP", fontsize=15)
sns.scatterplot(ax=axes[1,2], data=non_barrel_data_2020, x="launch_angle", y="ev", hue="ev", size=1.5, hue_norm=(70,110), palette="coolwarm", legend=False)
fig.suptitle("Barrel data with BIP", fontsize=30)

# These plots are only barrels, can make it easy to compare to all years
fig, axes = plt.subplots(2, 3, sharey='all', sharex='all', figsize=((40,18)))
sns.scatterplot(ax=axes[0,0], data=barrel_data_2015, x="launch_angle", y="ev", hue="ev", hue_norm=(60,110), palette="Reds", legend=False).set_title("2015 barrels", fontsize=15)
sns.scatterplot(ax=axes[0,1], data=barrel_data_2016, x="launch_angle", y="ev", hue="ev", hue_norm=(60,110), palette="Reds", legend=False).set_title("2016 barrels", fontsize=15)
sns.scatterplot(ax=axes[0,2], data=barrel_data_2017, x="launch_angle", y="ev", hue="ev", hue_norm=(60,110), palette="Reds", legend=False).set_title("2017 barrels", fontsize=15)
sns.scatterplot(ax=axes[1,0], data=barrel_data_2018, x="launch_angle", y="ev", hue="ev", hue_norm=(60,110), palette="Reds", legend=False).set_title("2018 barrels", fontsize=15)
sns.scatterplot(ax=axes[1,1], data=barrel_data_2019, x="launch_angle", y="ev", hue="ev", hue_norm=(60,110), palette="Reds", legend=False).set_title("2019 barrels", fontsize=15)
sns.scatterplot(ax=axes[1,2], data=barrel_data_2020, x="launch_angle", y="ev", hue="ev", hue_norm=(60,110), palette="Reds", legend=False).set_title("2020 barrels", fontsize=15)
fig.suptitle("Barrel data", fontsize=30)
