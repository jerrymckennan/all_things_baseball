/*

This script can be run within MySQL for the first time setting up or for reloading all data.
It will check to see if the database and table have been created or not, then do so if they
haven't. Then it will delete any data that might be in there just to ensure there is no
duplicated data. From there it will take each of the CSV files that was created with the
Python script. Each section can be removed to accommodate the number of CSV files you want
to use. You can also copy and paste to add more, if you want.

I enjoy using the SQL script to handle this, seems faster. Though I will try to also make a
script for Python for those who want to use that as well.

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

DELETE FROM prob;

LOAD DATA INFILE '/directory/file.csv' INTO TABLE prob
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 LINES
( 
hits_1b_per_hip,
hits_2b_per_hip,
hits_3b_per_hip,
hits_hr_per_hip,
hits_per_hip,
n_hip,
n_hits,
n_hits_1b,
n_hits_2b,
n_hits_3b,
n_hits_hr,
launch_angle,
woba,
year,
ev
);


LOAD DATA INFILE '/directory/file.csv' INTO TABLE prob
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 LINES
( 
hits_1b_per_hip,
hits_2b_per_hip,
hits_3b_per_hip,
hits_hr_per_hip,
hits_per_hip,
n_hip,
n_hits,
n_hits_1b,
n_hits_2b,
n_hits_3b,
n_hits_hr,
launch_angle,
woba,
year,
ev
);


LOAD DATA INFILE '/directory/file.csv' INTO TABLE prob
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 LINES
( 
hits_1b_per_hip,
hits_2b_per_hip,
hits_3b_per_hip,
hits_hr_per_hip,
hits_per_hip,
n_hip,
n_hits,
n_hits_1b,
n_hits_2b,
n_hits_3b,
n_hits_hr,
launch_angle,
woba,
year,
ev
);


LOAD DATA INFILE '/directory/file.csv' INTO TABLE prob
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 LINES
( 
hits_1b_per_hip,
hits_2b_per_hip,
hits_3b_per_hip,
hits_hr_per_hip,
hits_per_hip,
n_hip,
n_hits,
n_hits_1b,
n_hits_2b,
n_hits_3b,
n_hits_hr,
launch_angle,
woba,
year,
ev
);


LOAD DATA INFILE '/directory/file.csv' INTO TABLE prob
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 LINES
( 
hits_1b_per_hip,
hits_2b_per_hip,
hits_3b_per_hip,
hits_hr_per_hip,
hits_per_hip,
n_hip,
n_hits,
n_hits_1b,
n_hits_2b,
n_hits_3b,
n_hits_hr,
launch_angle,
woba,
year,
ev
);


LOAD DATA INFILE '/directory/file.csv' INTO TABLE prob
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 LINES
( 
hits_1b_per_hip,
hits_2b_per_hip,
hits_3b_per_hip,
hits_hr_per_hip,
hits_per_hip,
n_hip,
n_hits,
n_hits_1b,
n_hits_2b,
n_hits_3b,
n_hits_hr,
launch_angle,
woba,
year,
ev
);
