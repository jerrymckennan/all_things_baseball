/*

This script can be run within MySQL for the first time setting up any or all databases. 
It will check to see if the database and table have been created or not, then do so if they haven't.
If this is not the first time using it or you want a clean set up, use the delete_data.sql script as well. That will delete all data located in all of these tables. If you want to add data, use the add_data.sql script. 

I personally like to use the command line, change directory to where this script is located and issuing the following command:

	mysql -u username -p < name_you_gave_this_file.sql

*/

CREATE DATABASE IF NOT EXISTS hit_probability;

USE hit_probability;

CREATE TABLE IF NOT EXISTS prob (
hits_1b_per_hip SMALLINT,
hits_2b_per_hip SMALLINT,
hits_3b_per_hip SMALLINT,
hits_hr_per_hip SMALLINT,
hits_per_hip SMALLINT,
n_hip SMALLINT,
n_hits SMALLINT,
n_hits_1b SMALLINT,
n_hits_2b SMALLINT,
n_hits_3b SMALLINT,
n_hits_hr SMALLINT,
launch_angle TINYINT,
woba DECIMAL(4,3),
year SMALLINT,
ev SMALLINT
);

CREATE TABLE IF NOT EXISTS fg_park_factor (
season SMALLINT,
team varchar(25),
basic_5yr SMALLINT,
3yr SMALLINT,
1yr SMALLINT,
1b SMALLINT,
2b SMALLINT,
3b SMALLINT,
hr SMALLINT,
so SMALLINT,
bb SMALLINT,
gb SMALLINT,
fb SMALLINT,
ld SMALLINT,
iffb SMALLINT,
fip SMALLINT
);

CREATE TABLE IF NOT EXISTS team_names (
city_state varchar(25),
nickname varchar(25),
3_letter_name varchar(3)
);

CREATE TABLE IF NOT EXISTS player (
player_name varchar(50),
at_bat TINYINT,
ab_num TINYINT,
bb_walk TINYINT,
ball_in_play TINYINT,
distance DECIMAL(5,2),
ev SMALLINT,
event varchar(25),
eventPretty varchar(25),
game_date DATE,
hit TINYINT,
is_1b TINYINT,
is_2b TINYINT,
is_3b TINYINT,
is_hr TINYINT,
launch_angle TINYINT
);
