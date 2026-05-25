USE EsportsTournament;
GO

CREATE VIEW vw_ActiveRosters AS
SELECT 
    t.team_name, 
    p.name AS player_name, 
    p.role, 
    ph.join_date
FROM TEAMS t
JOIN PLAYER_HISTORY ph ON t.team_id = ph.team_id
JOIN PLAYERS p ON ph.player_id = p.player_id
WHERE ph.leave_date IS NULL; -- NULL means they haven't left the team
GO