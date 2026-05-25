USE EsportsTournament;
GO

SELECT 
    p.name AS Player_Name, 
    p.role, 
    gs.points_scored, 
    gs.assists, 
    gs.rating,
    g.game_number
FROM GAME_STATS gs
JOIN PLAYERS p ON gs.player_id = p.player_id
JOIN GAMES g ON gs.game_id = g.game_id
JOIN MATCHES m ON g.match_id = m.match_id
WHERE m.status = 'completed';