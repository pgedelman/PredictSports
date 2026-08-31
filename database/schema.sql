USE predict_sports;

-- Table for leagues
CREATE TABLE leagues (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE
);

-- Table for seasons
CREATE TABLE seasons (
    id INT AUTO_INCREMENT PRIMARY KEY,
    league_id INT NOT NULL,
    year INT NOT NULL
);

-- Table for teams
CREATE TABLE teams (
    id INT AUTO_INCREMENT PRIMARY KEY,
    league_id INT NOT NULL,
    name VARCHAR(100) NOT NULL,
    abbreviation VARCHAR(10)
);

-- Table for games
CREATE TABLE games (
    id INT AUTO_INCREMENT PRIMARY KEY,
    week INT NOT NULL, 
    season_id INT NOT NULL,
    home_team_id INT NOT NULL,
    away_team_id INT NOT NULL,
    home_team_stats INT NOT NULL,
    away_team_stats INT NOT NULL
);

-- Table for game stats
CREATE TABLE game_stats (
    id INT AUTO_INCREMENT PRIMARY KEY,
    game_id INT NOT NULL,
    team_id INT NOT NULL,
    overtime BOOLEAN NOT NULL,
    outcome BOOLEAN NOT NULL,
    win_percentage DECIMAL(5, 2) NOT NULL,
    game_location BOOLEAN NOT NULL,
    opponent_id INT NOT NULL,
    points_scored INT NOT NULL,
    points_allowed INT NOT NULL,
    passes_completed INT NOT NULL,
    passes_attempted INT NOT NULL,
    passing_yards INT NOT NULL,
    passing_td INT NOT NULL,
    interceptions INT NOT NULL,
    times_sacked INT NOT NULL,
    yards_sacked INT NOT NULL,
    yards_per_attempt DECIMAL(5, 2) NOT NULL,
    net_yards_per_attempt DECIMAL(5, 2) NOT NULL,
    completion_rate DECIMAL(5, 2) NOT NULL,
    passer_rating DECIMAL(5, 2) NOT NULL,
    rushing_attempts INT NOT NULL,
    rushing_yards INT NOT NULL,
    rushing_yards_per_attempt DECIMAL(5, 2) NOT NULL,
    rushing_td INT NOT NULL,
    field_goals_made INT NOT NULL,
    field_goals_attempted INT NOT NULL,
    extra_points_made INT NOT NULL,
    extra_points_attempted INT NOT NULL,
    punts INT NOT NULL,
    punting_yards INT NOT NULL,
    third_down_conversions INT NOT NULL,
    third_down_attempts INT NOT NULL,
    fourth_down_conversions INT NOT NULL,
    fourth_down_attempts INT NOT NULL,
    time_in_possession INT
);

CREATE TABLE avg_5 (
    id INT AUTO_INCREMENT PRIMARY KEY,
    game_id INT NOT NULL,
    team_id INT NOT NULL,
    overtime BOOLEAN NOT NULL,
    outcome BOOLEAN NOT NULL,
    win_percentage DECIMAL(5, 2) NOT NULL,
    game_location BOOLEAN NOT NULL,
    opponent_id INT NOT NULL,
    points_scored INT NOT NULL,
    points_allowed INT NOT NULL,
    passes_completed INT NOT NULL,
    passes_attempted INT NOT NULL,
    passing_yards INT NOT NULL,
    passing_td INT NOT NULL,
    interceptions INT NOT NULL,
    times_sacked INT NOT NULL,
    yards_sacked INT NOT NULL,
    yards_per_attempt DECIMAL(5, 2) NOT NULL,
    net_yards_per_attempt DECIMAL(5, 2) NOT NULL,
    completion_rate DECIMAL(5, 2) NOT NULL,
    passer_rating DECIMAL(5, 2) NOT NULL,
    rushing_attempts INT NOT NULL,
    rushing_yards INT NOT NULL,
    rushing_yards_per_attempt DECIMAL(5, 2) NOT NULL,
    rushing_td INT NOT NULL,
    field_goals_made INT NOT NULL,
    field_goals_attempted INT NOT NULL,
    extra_points_made INT NOT NULL,
    extra_points_attempted INT NOT NULL,
    punts INT NOT NULL,
    punting_yards INT NOT NULL,
    third_down_conversions INT NOT NULL,
    third_down_attempts INT NOT NULL,
    fourth_down_conversions INT NOT NULL,
    fourth_down_attempts INT NOT NULL,
    time_in_possession INT
);

CREATE TABLE predictive_stats (
    id INT AUTO_INCREMENT PRIMARY KEY,
    game_id INT NOT NULL,  
    team1_id INT NOT NULL, 
    team2_id INT NOT NULL, 
    previous10_id INT,     
    avg5_id INT,           
    avg10_id INT,         
    avg25_id INT
);

-- Add Foreign Keys
ALTER TABLE seasons
ADD FOREIGN KEY (league_id) REFERENCES leagues(id) ON DELETE CASCADE;

ALTER TABLE teams
ADD FOREIGN KEY (league_id) REFERENCES leagues(id) ON DELETE CASCADE;

ALTER TABLE games
ADD FOREIGN KEY (season_id) REFERENCES seasons(id) ON DELETE CASCADE,
ADD FOREIGN KEY (home_team_id) REFERENCES teams(id) ON DELETE CASCADE,
ADD FOREIGN KEY (away_team_id) REFERENCES teams(id) ON DELETE CASCADE;

ALTER TABLE game_stats
ADD FOREIGN KEY (game_id) REFERENCES games(id) ON DELETE CASCADE,
ADD FOREIGN KEY (team_id) REFERENCES teams(id) ON DELETE CASCADE,
ADD FOREIGN KEY (opponent_id) REFERENCES teams(id) ON DELETE CASCADE;

-- Indexes
CREATE INDEX idx_game_id ON game_stats(game_id);
CREATE INDEX idx_team_id ON game_stats(team_id);
CREATE INDEX idx_season_id ON games(season_id);