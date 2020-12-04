/*

These are just some fun queries that I've run. 
The first part creates a temporary with the data I want.
The second part is a query that gets the following data points:
    1. Average Distance, EV, and LA for all balls in play
    2. Gets the SUM for each type of actual base hit as well as total hits
    3. Gets the SUM for each chance of a hit as well as total chance of a hit
    4. Gets the difference between actual and chance as a percentage
    
If there is a specific player or year I want to focus on, add that to the WHERE clause in the second query

An example output of the second query:

+-------------+------+--------------+---------+---------+---------+--------+-----------+---------+--------+-----------+---------+--------+-----------+-----------+--------+-----------+------------+----------+-------------+
| player_name | year | avg_distance | avg_ev  | avg_la  | singles | exp_1b | 1b_%_diff | doubles | exp_2b | 2b_%_diff | triples | exp_3b | 3b_%_diff | home_runs | exp_hr | hr_%_diff | total_hits | exp_hits | hits_%_diff |
+-------------+------+--------------+---------+---------+---------+--------+-----------+---------+--------+-----------+---------+--------+-----------+-----------+--------+-----------+------------+----------+-------------+
| Trout       | 2019 |   212.461318 | 90.9198 | 22.2092 |      63 |  63.99 |   -1.5471 |      27 |  26.66 |    1.2753 |       2 |   2.38 |  -15.9664 |        45 |  48.60 |   -7.4074 |        137 |   141.63 |     -3.2691 |
| Goodrum     | 2019 |   167.807018 | 89.3018 | 13.1895 |      61 |  61.12 |   -0.1963 |      27 |  24.01 |   12.4531 |       5 |   2.19 |  128.3105 |        12 |  12.48 |   -3.8462 |        105 |    99.80 |      5.2104 |
| Candelario  | 2019 |   166.080508 | 88.2966 | 15.8051 |      41 |  50.56 |  -18.9082 |      17 |  17.06 |   -0.3517 |       2 |   1.32 |   51.5152 |         8 |   9.81 |  -18.4506 |         68 |    78.75 |    -13.6508 |
| Pederson    | 2020 |   170.247788 | 93.9115 | 13.5841 |      22 |  21.63 |    1.7106 |       4 |   6.14 |  -34.8534 |       0 |   0.30 | -100.0000 |         9 |   8.36 |    7.6555 |         35 |    36.43 |     -3.9253 |
| Candelario  | 2020 |   174.088889 | 89.8741 | 12.7481 |      34 |  34.01 |   -0.0294 |      10 |  10.34 |   -3.2882 |       3 |   0.87 |  244.8276 |         7 |   7.54 |   -7.1618 |         54 |    52.76 |      2.3503 |
| Correa      | 2020 |   151.223404 | 89.6968 | 10.9309 |      49 |  44.47 |   10.1866 |      10 |  11.54 |  -13.3449 |       0 |   1.07 | -100.0000 |        11 |  12.46 |  -11.7175 |         70 |    69.54 |      0.6615 |
| Lindor      | 2020 |   176.975000 | 89.9850 | 13.0800 |      40 |  40.97 |   -2.3676 |      14 |  13.54 |    3.3973 |       0 |   1.02 | -100.0000 |         8 |   7.61 |    5.1248 |         62 |    63.14 |     -1.8055 |
| Renfroe     | 2020 |   168.244681 | 88.5213 | 16.7660 |       7 |  13.93 |  -49.7487 |       6 |   4.27 |   40.5152 |       0 |   0.20 | -100.0000 |         9 |   7.98 |   12.7820 |         22 |    26.38 |    -16.6035 |
| Story       | 2020 |   207.597633 | 90.3964 | 21.1598 |      39 |  33.94 |   14.9087 |      13 |  13.88 |   -6.3401 |       4 |   1.11 |  260.3604 |        11 |  10.62 |    3.5782 |         67 |    59.55 |     12.5105 |
| Castro      | 2020 |   173.152174 | 85.6304 | 10.8804 |      33 |  25.32 |   30.3318 |       4 |   5.34 |  -25.0936 |       2 |   0.43 |  365.1163 |         6 |   6.86 |  -12.5364 |         45 |    37.95 |     18.5771 |
+-------------+------+--------------+---------+---------+---------+--------+-----------+---------+--------+-----------+---------+--------+-----------+-----------+--------+-----------+------------+----------+-------------+

*/

CREATE TEMPORARY TABLE test SELECT
py.player_name,
YEAR(py.game_date) as year,
py.distance,
pr.ev,
pr.launch_angle,
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
WHERE pr.ev = py.ev AND pr.launch_angle = py.launch_angle
GROUP BY YEAR(py.game_date), py.player_name, py.game_date, py.ab_num, event
ORDER BY py.game_date;

SELECT 
player_name,
year,
SUM(distance)/COUNT(distance) as avg_distance,
SUM(ev)/COUNT(ev) as avg_ev,
SUM(launch_angle)/COUNT(launch_angle) as avg_la,
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
FROM test
WHERE ev > 0
GROUP BY player_name, year;
