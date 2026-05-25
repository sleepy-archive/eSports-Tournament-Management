USE EsportsTournament;
GO

CREATE TRIGGER trg_MatchStatusAudit
ON MATCHES
AFTER UPDATE
AS
BEGIN
    -- Only trigger if the status column was specifically updated
    IF UPDATE(status)
    BEGIN
        INSERT INTO MATCH_AUDIT_LOG (match_id, old_status, new_status)
        SELECT 
            i.match_id, 
            d.status AS old_status, 
            i.status AS new_status
        FROM inserted i
        JOIN deleted d ON i.match_id = d.match_id
        -- Ensure we only log if the status actually changed
        WHERE i.status <> d.status;
    END
END;
GO