USE EsportsTournament;
GO

SELECT 
    p.name, 
    COUNT(gs.game_id) AS Total_Games_Played, 
    SUM(gs.points_scored) AS Total_Points, 
    AVG(gs.rating) AS Average_Rating
FROM GAME_STATS gs
JOIN PLAYERS p ON gs.player_id = p.player_id
GROUP BY p.name
HAVING COUNT(gs.game_id) >= 1 -- Adjust this number based on your sample data
ORDER BY Total_Points DESC;