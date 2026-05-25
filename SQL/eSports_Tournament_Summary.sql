USE EsportsTournament;
GO

CREATE VIEW vw_TournamentOverview AS
SELECT 
    t.tournament_name, 
    t.start_date, 
    t.end_date,
    COUNT(s.stage_id) AS Total_Stages
FROM TOURNAMENTS t
LEFT JOIN TOURNAMENT_STAGES s ON t.tournament_id = s.tournament_id
GROUP BY t.tournament_name, t.start_date, t.end_date;
GO