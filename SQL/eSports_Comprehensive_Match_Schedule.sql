USE EsportsTournament;
GO

SELECT 
    m.match_date, 
    s.stage_name, 
    t1.team_name AS Team_1, 
    t2.team_name AS Team_2, 
    m.format,
    m.status
FROM MATCHES m
JOIN TOURNAMENT_STAGES s ON m.stage_id = s.stage_id
JOIN TEAMS t1 ON m.team1_id = t1.team_id
JOIN TEAMS t2 ON m.team2_id = t2.team_id
ORDER BY m.match_date DESC;