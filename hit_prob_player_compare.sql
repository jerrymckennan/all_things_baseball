/*

I was wanting to compare to specific players over the course of a large sample size. To do so, I needed to create a temporary table that I could then
import my data for each one over their last 1,500 PA each. This is what I used to create the temporary table, insert the data from the second player,
and a couple of queries I used to actually compare them.

*/

CREATE TEMPORARY TABLE compare SELECT
py.player_name,
YEAR(py.game_date) as year,
py.bb_walk,
py.is_1b,
py.is_2b,
py.is_3b,
py.is_hr
FROM player AS py
WHERE py.player_name LIKE 'Schwa%' 
GROUP BY py.player_name, py.game_date, py.ab_num, event
ORDER BY py.game_date DESC
LIMIT 1500;

INSERT INTO compare (player_name,year,bb_walk,is_1b,is_2b,is_3b,is_hr)
SELECT
py.player_name,
YEAR(py.game_date) as year,
py.bb_walk,
py.is_1b,
py.is_2b,
py.is_3b,
py.is_hr
FROM player AS py
WHERE py.player_name LIKE 'Rosar%' 
GROUP BY py.player_name, py.game_date, py.ab_num, event
ORDER BY py.game_date DESC
LIMIT 1500;

SELECT
player_name,
SUM(bb_walk),
SUM(is_1b),
SUM(is_2b),
SUM(is_3b),
SUM(is_hr)
FROM compare
GROUP BY player_name;

SELECT
player_name,
(SUM(bb_walk)+SUM(is_1b)) as bbs_and_singles,
SUM(is_hr),
(SUM(is_2b)+SUM(is_3b)+SUM(is_hr)) AS xbh,
(SUM(bb_walk)+SUM(is_1b)+SUM(is_2b)+SUM(is_3b)+SUM(is_hr)) AS times_onbase
FROM compare
GROUP BY player_name;
