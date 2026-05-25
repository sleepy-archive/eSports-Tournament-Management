-- 1. Create the Database
CREATE DATABASE EsportsTournament;
GO

USE EsportsTournament;
GO

-- 2. Create Independent Tables
CREATE TABLE TOURNAMENTS (
    tournament_id INT IDENTITY(1,1) PRIMARY KEY,
    tournament_name VARCHAR(255) NOT NULL,
    start_date DATE,
    end_date DATE
);

CREATE TABLE TEAMS (
    team_id INT IDENTITY(1,1) PRIMARY KEY,
    team_name VARCHAR(255) NOT NULL,
    region VARCHAR(100)
);

CREATE TABLE VENUES (
    venue_id INT IDENTITY(1,1) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    location VARCHAR(255),
    is_online BIT DEFAULT 0 -- 0 for False, 1 for True
);

CREATE TABLE PLAYERS (
    player_id INT IDENTITY(1,1) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    role VARCHAR(100)
);

CREATE TABLE PATCHES (
    patch_id INT IDENTITY(1,1) PRIMARY KEY,
    version_number VARCHAR(50) NOT NULL,
    release_date DATE
);

CREATE TABLE MAPS (
    map_id INT IDENTITY(1,1) PRIMARY KEY,
    map_name VARCHAR(255) NOT NULL,
    game_mode VARCHAR(100)
);

-- 3. Create First-Level Dependent Tables
CREATE TABLE TOURNAMENT_STAGES (
    stage_id INT IDENTITY(1,1) PRIMARY KEY,
    tournament_id INT NOT NULL,
    stage_name VARCHAR(100), -- e.g., Groups, Playoffs
    CONSTRAINT FK_Stage_Tournament FOREIGN KEY (tournament_id) REFERENCES TOURNAMENTS(tournament_id)
);

CREATE TABLE PLAYER_HISTORY (
    history_id INT IDENTITY(1,1) PRIMARY KEY,
    player_id INT NOT NULL,
    team_id INT NOT NULL,
    join_date DATE NOT NULL,
    leave_date DATE NULL, -- NULL indicates they are currently active on the team
    CONSTRAINT FK_History_Player FOREIGN KEY (player_id) REFERENCES PLAYERS(player_id),
    CONSTRAINT FK_History_Team FOREIGN KEY (team_id) REFERENCES TEAMS(team_id)
);

-- 4. Create Second-Level Dependent Tables (MATCHES)
CREATE TABLE MATCHES (
    match_id INT IDENTITY(1,1) PRIMARY KEY,
    stage_id INT NOT NULL,
    team1_id INT NOT NULL,
    team2_id INT NOT NULL,
    winner_team_id INT NULL, -- NULL until the match is completed
    venue_id INT,
    match_date DATE,
    status VARCHAR(50), -- scheduled, live, completed
    format VARCHAR(50), -- Bo1, Bo3, Bo5
    CONSTRAINT FK_Match_Stage FOREIGN KEY (stage_id) REFERENCES TOURNAMENT_STAGES(stage_id),
    CONSTRAINT FK_Match_Team1 FOREIGN KEY (team1_id) REFERENCES TEAMS(team_id),
    CONSTRAINT FK_Match_Team2 FOREIGN KEY (team2_id) REFERENCES TEAMS(team_id),
    CONSTRAINT FK_Match_Winner FOREIGN KEY (winner_team_id) REFERENCES TEAMS(team_id),
    CONSTRAINT FK_Match_Venue FOREIGN KEY (venue_id) REFERENCES VENUES(venue_id)
);

-- 5. Create Third-Level Dependent Tables
CREATE TABLE BROADCASTS (
    broadcast_id INT IDENTITY(1,1) PRIMARY KEY,
    match_id INT NOT NULL,
    platform VARCHAR(100), -- Twitch, YouTube
    url VARCHAR(500),
    language VARCHAR(50),
    CONSTRAINT FK_Broadcast_Match FOREIGN KEY (match_id) REFERENCES MATCHES(match_id)
);

CREATE TABLE GAMES (
    game_id INT IDENTITY(1,1) PRIMARY KEY,
    match_id INT NOT NULL,
    patch_id INT,
    game_number INT, -- Game 1, Game 2
    map_id INT,
    winner_team_id INT NULL,
    duration_seconds INT,
    CONSTRAINT FK_Game_Match FOREIGN KEY (match_id) REFERENCES MATCHES(match_id),
    CONSTRAINT FK_Game_Patch FOREIGN KEY (patch_id) REFERENCES PATCHES(patch_id),
    CONSTRAINT FK_Game_Map FOREIGN KEY (map_id) REFERENCES MAPS(map_id),
    CONSTRAINT FK_Game_Winner FOREIGN KEY (winner_team_id) REFERENCES TEAMS(team_id)
);

-- 6. Create Fourth-Level Dependent Tables
CREATE TABLE GAME_STATS (
    stat_id INT IDENTITY(1,1) PRIMARY KEY,
    game_id INT NOT NULL,
    player_id INT NOT NULL,
    points_scored INT DEFAULT 0,
    assists INT DEFAULT 0,
    rating FLOAT,
    CONSTRAINT FK_Stat_Game FOREIGN KEY (game_id) REFERENCES GAMES(game_id),
    CONSTRAINT FK_Stat_Player FOREIGN KEY (player_id) REFERENCES PLAYERS(player_id)
);
GO

-- 7. Audit Log
CREATE TABLE MATCH_AUDIT_LOG (
    log_id INT IDENTITY(1,1) PRIMARY KEY,
    match_id INT,
    old_status VARCHAR(50),
    new_status VARCHAR(50),
    changed_at DATETIME DEFAULT GETDATE()
);
GO