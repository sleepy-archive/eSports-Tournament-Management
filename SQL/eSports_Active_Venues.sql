USE EsportsTournament;
GO

SELECT name, location, is_online
FROM VENUES v
WHERE EXISTS (
    SELECT 1 
    FROM MATCHES m 
    WHERE m.venue_id = v.venue_id AND m.status = 'live'
);