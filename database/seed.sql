USE predict_sports;

INSERT INTO Games (game_id, date, home_team_id, away_team_id, home_score, away_score)
VALUES
(1, '2025-01-15 18:00:00', 1, 2, 3, 2),
(2, '2025-01-16 19:00:00', 3, 4, 4, 5);

INSERT INTO Players (player_id, name, team_id, position, average_points)
VALUES
(1, 'Player A', 1, 'Forward', 22.5),
(2, 'Player B', 2, 'Guard', 18.4);
