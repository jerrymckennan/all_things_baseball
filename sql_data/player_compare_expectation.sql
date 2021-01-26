/*

This is just like the player_compare.sql but it also includes expected hits based on EV and LA over the course of the same amount of PA.

*/

CREATE TEMPORARY TABLE compare SELECT
py.player_name,
YEAR(py.game_date) as year,
py.distance,
pr.ev,
pr.launch_angle,
py.bb_walk,
pr.hits_1b_per_hip,
py.is_1b,
pr.hits_2b_per_hip,
py.is_2b,
pr.hits_3b_per_hip,
py.is_3b,
pr.hits_hr_per_hip,
py.is_hr
FROM player AS py
JOIN prob AS pr
ON pr.year = YEAR(py.game_date)
WHERE pr.ev = py.ev AND pr.launch_angle = py.launch_angle AND py.player_name LIKE 'Schwa%'
GROUP BY YEAR(py.game_date), py.player_name, py.game_date, py.ab_num, event
ORDER BY py.game_date DESC
LIMIT 1500;

INSERT INTO compare (player_name,year,distance,ev,launch_angle,bb_walk,hits_1b_per_hip,is_1b,hits_2b_per_hip,is_2b,hits_3b_per_hip,is_3b,hits_hr_per_hip,is_hr)
SELECT
py.player_name,
YEAR(py.game_date) as year,
py.distance,
pr.ev,
pr.launch_angle,
py.bb_walk,
pr.hits_1b_per_hip,
py.is_1b,
pr.hits_2b_per_hip,
py.is_2b,
pr.hits_3b_per_hip,
py.is_3b,
pr.hits_hr_per_hip,
py.is_hr
FROM player AS py
JOIN prob AS pr
ON pr.year = YEAR(py.game_date)
WHERE pr.ev = py.ev AND pr.launch_angle = py.launch_angle AND py.player_name LIKE 'Rosar%'
GROUP BY YEAR(py.game_date), py.player_name, py.game_date, py.ab_num, event
ORDER BY py.game_date DESC
LIMIT 1500;

/*

Queries used

*/

SELECT
player_name,
(SUM(bb_walk)+SUM(is_1b)) as bbs_and_singles,
(SUM(bb_walk)+(ROUND(SUM(hits_1b_per_hip)/100,2))) as exp_bbs_and_singles,
SUM(is_hr),
ROUND(SUM(hits_hr_per_hip)/100,2) as exp_hr,
(SUM(is_2b)+SUM(is_3b)+SUM(is_hr)) AS xbh,
ROUND((SUM(hits_2b_per_hip)/100)+(SUM(hits_3b_per_hip)/100)+(SUM(hits_hr_per_hip)/100),2) AS exp_xbh,
(SUM(bb_walk)+SUM(is_1b)+SUM(is_2b)+SUM(is_3b)+SUM(is_hr)) AS times_onbase,
(SUM(bb_walk)+ROUND((SUM(hits_1b_per_hip)/100)+(SUM(hits_2b_per_hip)/100)+(SUM(hits_3b_per_hip)/100)+(SUM(hits_hr_per_hip)/100),2)) as exp_times_onbase
FROM compare
GROUP BY player_name;

SELECT 
player_name,
year,
SUM(distance)/COUNT(distance) as avg_distance,
SUM(ev)/COUNT(ev) as avg_ev,
SUM(launch_angle)/COUNT(launch_angle) as avg_la,
SUM(bb_walk) as walks,
SUM(is_1b) as singles,
ROUND(SUM(hits_1b_per_hip)/100,2) as exp_1b,
(1-(SUM(is_1b)/(SUM(hits_1b_per_hip)/100)))*100*(-1) as '1b_%_diff',
SUM(is_2b) as doubles,
ROUND(SUM(hits_2b_per_hip)/100,2) as exp_2b,
(1-(SUM(is_2b)/(SUM(hits_2b_per_hip)/100)))*100*(-1) as '2b_%_diff',
SUM(is_3b) as triples,
ROUND(SUM(hits_3b_per_hip)/100,2) as exp_3b,
(1-(SUM(is_3b)/(SUM(hits_3b_per_hip)/100)))*100*(-1) as '3b_%_diff',
SUM(is_hr) as home_runs,
ROUND(SUM(hits_hr_per_hip)/100,2) as exp_hr,
(1-(SUM(is_hr)/(SUM(hits_hr_per_hip)/100)))*100*(-1) as 'hr_%_diff',
SUM(is_1b)+SUM(is_2b)+SUM(is_3b)+SUM(is_hr) as total_hits,
ROUND((SUM(hits_1b_per_hip)/100)+(SUM(hits_2b_per_hip)/100)+(SUM(hits_3b_per_hip)/100)+(SUM(hits_hr_per_hip)/100),2) as exp_hits,
(1-((SUM(is_1b)+SUM(is_2b)+SUM(is_3b)+SUM(is_hr))/((SUM(hits_1b_per_hip)/100)+(SUM(hits_2b_per_hip)/100)+(SUM(hits_3b_per_hip)/100)+(SUM(hits_hr_per_hip)/100))))*100*(-1) as 'hits_%_diff'
FROM compare
GROUP BY player_name;
