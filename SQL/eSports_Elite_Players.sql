USE EsportsTournament;
GO

SELECT name, role 
FROM PLAYERS 
WHERE player_id IN (
    SELECT player_id 
    FROM GAME_STATS 
    GROUP BY player_id 
    HAVING AVG(rating) > (SELECT AVG(rating) FROM GAME_STATS)
);