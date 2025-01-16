USE predict_sports;

CREATE TABLE Games (
    game_id INT PRIMARY KEY,
    date DATETIME,
    home_team_id INT,
    away_team_id INT,
    home_score INT,
    away_score INT
);

CREATE TABLE Players (
    player_id INT PRIMARY KEY,
    name VARCHAR(100),
    team_id INT,
    position VARCHAR(50),
    average_points FLOAT
);
