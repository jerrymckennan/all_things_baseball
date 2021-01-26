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
game_date DATE,
hit TINYINT,
is_1b TINYINT,
is_2b TINYINT,
is_3b TINYINT,
is_hr TINYINT,
launch_angle TINYINT
);

CREATE TABLE IF NOT EXISTS fg_guts (
year SMALLINT,
woba DECIMAL(5,3),
wobascale DECIMAL(5,3),
wbb DECIMAL(5,3),
whbp DECIMAL(5,3),
w1b DECIMAL(5,3),
w2b DECIMAL(5,3),
w3b DECIMAL(5,3),
whr DECIMAL(5,3),
runsb DECIMAL(5,3),
runcs DECIMAL(5,3),
rpa DECIMAL(5,3),
rw DECIMAL(5,3),
cfip DECIMAL(5,3)
);

CREATE TABLE IF NOT EXISTS barrels AS
SELECT year, ev, launch_angle
FROM prob
WHERE (n_hits/n_hip) >= .500 AND ((n_hits_1b+(n_hits_2b*2)+(n_hits_3b*3)+(n_hits_hr*4))/n_hip) >= 1.500 AND ev = 98 AND launch_angle >= 26 AND launch_angle <=30
OR (n_hits/n_hip) >= .500 AND ((n_hits_1b+(n_hits_2b*2)+(n_hits_3b*3)+(n_hits_hr*4))/n_hip) >= 1.500 AND ev = 99 AND launch_angle >= 25 AND launch_angle <=31
OR (n_hits/n_hip) >= .500 AND ((n_hits_1b+(n_hits_2b*2)+(n_hits_3b*3)+(n_hits_hr*4))/n_hip) >= 1.500 AND ev = 100 AND launch_angle >= 24 AND launch_angle <=33
OR (n_hits/n_hip) >= .500 AND ((n_hits_1b+(n_hits_2b*2)+(n_hits_3b*3)+(n_hits_hr*4))/n_hip) >= 1.500 AND ev = 101 AND launch_angle >= 23 AND launch_angle <=34
OR (n_hits/n_hip) >= .500 AND ((n_hits_1b+(n_hits_2b*2)+(n_hits_3b*3)+(n_hits_hr*4))/n_hip) >= 1.500 AND ev = 102 AND launch_angle >= 22 AND launch_angle <=35
OR (n_hits/n_hip) >= .500 AND ((n_hits_1b+(n_hits_2b*2)+(n_hits_3b*3)+(n_hits_hr*4))/n_hip) >= 1.500 AND ev = 103 AND launch_angle >= 21 AND launch_angle <=36
OR (n_hits/n_hip) >= .500 AND ((n_hits_1b+(n_hits_2b*2)+(n_hits_3b*3)+(n_hits_hr*4))/n_hip) >= 1.500 AND ev = 104 AND launch_angle >= 20 AND launch_angle <=37
OR (n_hits/n_hip) >= .500 AND ((n_hits_1b+(n_hits_2b*2)+(n_hits_3b*3)+(n_hits_hr*4))/n_hip) >= 1.500 AND ev = 105 AND launch_angle >= 19 AND launch_angle <=38
OR (n_hits/n_hip) >= .500 AND ((n_hits_1b+(n_hits_2b*2)+(n_hits_3b*3)+(n_hits_hr*4))/n_hip) >= 1.500 AND ev = 106 AND launch_angle >= 18 AND launch_angle <=39
OR (n_hits/n_hip) >= .500 AND ((n_hits_1b+(n_hits_2b*2)+(n_hits_3b*3)+(n_hits_hr*4))/n_hip) >= 1.500 AND ev = 107 AND launch_angle >= 17 AND launch_angle <=40
OR (n_hits/n_hip) >= .500 AND ((n_hits_1b+(n_hits_2b*2)+(n_hits_3b*3)+(n_hits_hr*4))/n_hip) >= 1.500 AND ev = 108 AND launch_angle >= 16 AND launch_angle <=41
OR (n_hits/n_hip) >= .500 AND ((n_hits_1b+(n_hits_2b*2)+(n_hits_3b*3)+(n_hits_hr*4))/n_hip) >= 1.500 AND ev = 109 AND launch_angle >= 15 AND launch_angle <=42
OR (n_hits/n_hip) >= .500 AND ((n_hits_1b+(n_hits_2b*2)+(n_hits_3b*3)+(n_hits_hr*4))/n_hip) >= 1.500 AND ev = 110 AND launch_angle >= 14 AND launch_angle <=43
OR (n_hits/n_hip) >= .500 AND ((n_hits_1b+(n_hits_2b*2)+(n_hits_3b*3)+(n_hits_hr*4))/n_hip) >= 1.500 AND ev = 111 AND launch_angle >= 13 AND launch_angle <=44
OR (n_hits/n_hip) >= .500 AND ((n_hits_1b+(n_hits_2b*2)+(n_hits_3b*3)+(n_hits_hr*4))/n_hip) >= 1.500 AND ev = 112 AND launch_angle >= 12 AND launch_angle <=45
OR (n_hits/n_hip) >= .500 AND ((n_hits_1b+(n_hits_2b*2)+(n_hits_3b*3)+(n_hits_hr*4))/n_hip) >= 1.500 AND ev = 113 AND launch_angle >= 11 AND launch_angle <=46
OR (n_hits/n_hip) >= .500 AND ((n_hits_1b+(n_hits_2b*2)+(n_hits_3b*3)+(n_hits_hr*4))/n_hip) >= 1.500 AND ev = 114 AND launch_angle >= 10 AND launch_angle <=47
OR (n_hits/n_hip) >= .500 AND ((n_hits_1b+(n_hits_2b*2)+(n_hits_3b*3)+(n_hits_hr*4))/n_hip) >= 1.500 AND ev = 115 AND launch_angle >= 9 AND launch_angle <=48
OR (n_hits/n_hip) >= .500 AND ((n_hits_1b+(n_hits_2b*2)+(n_hits_3b*3)+(n_hits_hr*4))/n_hip) >= 1.500 AND ev >= 116 AND launch_angle >= 8 AND launch_angle <=50
;
