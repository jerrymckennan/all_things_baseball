/*

This is a fun query to find out how many miles of balls were put in play. I like to use a specific player because that's fun. Example using the query below:

+---------------+------+------+------+------+------+----------------+-----------------+
| balls_in_play | hits | 1b   | 2b   | 3b   | hr   | distance_miles | avg_distance_ft |
+---------------+------+------+------+------+------+----------------+-----------------+
|           354 |  137 |   63 |   27 |    2 |   45 |      14.043371 |      209.460452 |
+---------------+------+------+------+------+------+----------------+-----------------+

*/

SELECT
SUM(ball_in_play) as balls_in_play,
SUM(hit) as hits,
SUM(is_1b) as 1b,
SUM(is_2b) as 2b,
SUM(is_3b) as 3b,
SUM(is_hr) as hr,
SUM(distance)/5280 as distance_miles,
SUM(distance)/SUM(ball_in_play) as avg_distance_ft
FROM player
WHERE player_name LIKE 'Trou%';
