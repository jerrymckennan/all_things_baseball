/*

This script can be run within MySQL to populate tables created in the hit_prob_db.sql and was
gathered from the different parts of the Python script. For the CSV file imports, make sure to use a valid path and file name that you have used to begin with. Also beware that this will import the data into each table regardless of whether it is there already or not.

There is a query that should run through and delete any duplicates of the data. 

*/

USE hit_probability;

LOAD DATA INFILE '/path/hit_data.csv' INTO TABLE prob
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

/* 

I did find that my data was slightly skewed because there was no data for zero LA and zero EV, obviously. Since BBs and Ks would have zeros for both, and I wanted
to see that data, I had to add the following for each year. This could be optional.

*/

INSERT INTO prob () VALUES(0,0,0,0,0,0,0,0,0,0,0,0,0.000,2015,0);
INSERT INTO prob () VALUES(0,0,0,0,0,0,0,0,0,0,0,0,0.000,2016,0);
INSERT INTO prob () VALUES(0,0,0,0,0,0,0,0,0,0,0,0,0.000,2017,0);
INSERT INTO prob () VALUES(0,0,0,0,0,0,0,0,0,0,0,0,0.000,2018,0);
INSERT INTO prob () VALUES(0,0,0,0,0,0,0,0,0,0,0,0,0.000,2019,0);
INSERT INTO prob () VALUES(0,0,0,0,0,0,0,0,0,0,0,0,0.000,2020,0);

LOAD DATA INFILE '/path/for_park_factor_data.csv' INTO TABLE fg_park_factor
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 LINES
( 
season,
team,
basic_5yr,
3yr,
1yr,
1b,
2b,
3b,
hr,
so,
bb,
gb,
fb,
ld,
iffb,
fip
);

INSERT INTO team_names (city_state, nickname, 3_letter_name) VALUES
('Los Angeles', 'Dodgers', 'LAD'),
('San Diego', 'Padres', 'SDP'),
('San Francisco', 'Giants', 'SFG'),
('Colorado', 'Rockies', 'COL'),
('St Louis', 'Cardinals', 'STL'),
('Chicago', 'Cubs', 'CHC'),
('Pittsburgh', 'Pirates', 'PIT'),
('Arizona', 'Diamondbacks', 'ARI'),
('Cincinnati', 'Reds', 'CIN'),
('Milwaukee', 'Brewers', 'MIL'),
('Washington', 'Nationals', 'WAS'),
('New York', 'Mets', 'NYM'),
('Philadelphia', 'Phillies', 'PHI'),
('Miami', 'Marlins', 'MIA'),
('Atlanta', 'Braves', 'ATL'),
('Texas', 'Rangers', 'TEX'),
('Los Angeles', 'Angels', 'LAA'),
('Seattle', 'Mariners', 'SEA'),
('Houston', 'Astros', 'HOU'),
('Oakland', 'Athletics', 'OAK'),
('Detroit', 'Tigers', 'DET'),
('Kansas City', 'Royals', 'KCR'),
('Chicago', 'White Sox', 'CWS'),
('Cleveland', 'Indians', 'CLE'),
('Minnesota', 'Twins', 'MIN'),
('Boston', 'Red Sox', 'BOS'),
('Baltimore', 'Orioles', 'BAL'),
('Toronto', 'Blue Jays', 'TOR'),
('New York', 'Yankees', 'NYY'),
('Tampa Bay', 'Rays', 'TBR');

LOAD DATA INFILE '/path/for_player.csv' INTO TABLE player
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 LINES
( 
at_bat,
ab_num,
bb_walk,
ball_in_play,
distance,
ev,
event,
eventPretty,
game_date,
hit,
is_1b,
is_2b,
is_3b,
is_hr,
launch_angle,
player_name
);

