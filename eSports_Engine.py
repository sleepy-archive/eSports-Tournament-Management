import pyodbc
import math
import random

class DatabaseManager:
    """Handles all MS SQL Server connections and query formatting for the UI."""
    
    def __init__(self) -> None:
        """Initializes the database connection configuration."""
        self.conn_str = (
            r"Driver={ODBC Driver 17 for SQL Server};"
            r"Server=ASPHYXIATED;" 
            r"Database=EsportsTournament;"
            r"Trusted_Connection=yes;"
        )

    def _fetch_data(self, query: str) -> list:
        """
        Executes a SQL query and retrieves the results.

        Args:
            query (str): The SQL query string to execute.

        Returns:
            list: A list of rows returned by the query, or an error message row upon failure.
        """
        conn = None
        try:
            conn = pyodbc.connect(self.conn_str, timeout=3)
            cursor = conn.cursor()
            cursor.execute(query)
            return cursor.fetchall()
        except Exception as e:
            return [(f"DB ERROR: {str(e)[:50]}",)]
        finally:
            if conn is not None:
                try: conn.close()
                except Exception: pass

    def get_tournament_summary(self) -> dict:
        """
        Retrieves a summary of all tournaments.

        Returns:
            dict: A dictionary containing 'headers' and 'rows' for the UI table.
        """
        query = "SELECT tournament_name, start_date, Total_Stages FROM vw_TournamentOverview;"
        rows = self._fetch_data(query)
        if not rows: return {"headers": ["MESSAGE"], "rows": [["NO RESULTS FOUND"]]}
        if isinstance(rows[0][0], str) and rows[0][0].startswith("DB ERROR"): return {"headers": ["ERROR"], "rows": [[r[0]] for r in rows]}
        return {"headers": ["TOURNAMENT NAME", "START DATE", "STAGES"], "rows": [[str(r[0]), str(r[1]), str(r[2])] for r in rows]}

    def get_live_venues(self) -> dict:
        """
        Retrieves a list of venues currently hosting live matches.

        Returns:
            dict: A dictionary containing 'headers' and 'rows' for the UI table.
        """
        query = """
            WITH LiveVenues AS (
                SELECT DISTINCT v.name, v.location, v.is_online, b.platform
                FROM VENUES v
                JOIN MATCHES m ON v.venue_id = m.venue_id
                LEFT JOIN BROADCASTS b ON m.match_id = b.match_id
                WHERE m.status = 'live'
            )
            SELECT name, location, is_online, COALESCE(STRING_AGG(platform, ', '), 'N/A')
            FROM LiveVenues
            GROUP BY name, location, is_online;
        """
        rows = self._fetch_data(query)
        if not rows: return {"headers": ["MESSAGE"], "rows": [["NO LIVE MATCHES FOUND"]]}
        if isinstance(rows[0][0], str) and rows[0][0].startswith("DB ERROR"): return {"headers": ["ERROR"], "rows": [[r[0]] for r in rows]}
        return {"headers": ["VENUE NAME", "LOCATION", "ONLINE STATUS", "PLATFORM(S)"], "rows": [[str(r[0]), str(r[1]), "ONLINE" if r[2] else "OFFLINE", str(r[3])] for r in rows]}

    def get_active_rosters(self) -> dict:
        """
        Retrieves the active player rosters across all teams.

        Returns:
            dict: A dictionary containing 'headers' and 'rows' for the UI table.
        """
        query = "SELECT team_name, player_name, role FROM vw_ActiveRosters ORDER BY team_name;"
        rows = self._fetch_data(query)
        if not rows: return {"headers": ["MESSAGE"], "rows": [["NO RESULTS FOUND"]]}
        if isinstance(rows[0][0], str) and rows[0][0].startswith("DB ERROR"): return {"headers": ["ERROR"], "rows": [[r[0]] for r in rows]}
        return {"headers": ["TEAM NAME", "PLAYER NAME", "ROLE"], "rows": [[str(r[0]), str(r[1]), str(r[2])] for r in rows]}

    def get_leaderboard(self) -> dict:
        """
        Retrieves player rankings based on total points scored and average rating.

        Returns:
            dict: A dictionary containing 'headers' and 'rows' for the UI table.
        """
        query = """
            SELECT p.name, SUM(gs.points_scored), AVG(gs.rating)
            FROM GAME_STATS gs JOIN PLAYERS p ON gs.player_id = p.player_id
            GROUP BY p.name HAVING COUNT(gs.game_id) >= 1 ORDER BY SUM(gs.points_scored) DESC;
        """
        rows = self._fetch_data(query)
        if not rows: return {"headers": ["MESSAGE"], "rows": [["NO RESULTS FOUND"]]}
        if isinstance(rows[0][0], str) and rows[0][0].startswith("DB ERROR"): return {"headers": ["ERROR"], "rows": [[r[0]] for r in rows]}
        return {"headers": ["RANK", "PLAYER", "TOTAL PTS", "AVG RATING"], "rows": [[str(i+1), str(r[0]), str(r[1]), f"{r[2]:.1f}"] for i, r in enumerate(rows)]}

    def get_elite_tier(self) -> dict:
        """
        Retrieves players who maintain an above-average performance rating.

        Returns:
            dict: A dictionary containing 'headers' and 'rows' for the UI table.
        """
        query = """
            SELECT name, role FROM PLAYERS WHERE player_id IN (
                SELECT player_id FROM GAME_STATS GROUP BY player_id 
                HAVING AVG(rating) > (SELECT AVG(rating) FROM GAME_STATS)
            );
        """
        rows = self._fetch_data(query)
        if not rows: return {"headers": ["MESSAGE"], "rows": [["NO RESULTS FOUND"]]}
        if isinstance(rows[0][0], str) and rows[0][0].startswith("DB ERROR"): return {"headers": ["ERROR"], "rows": [[r[0]] for r in rows]}
        return {"headers": ["PLAYER NAME", "ROLE"], "rows": [[str(r[0]), str(r[1])] for r in rows]}

    def get_full_schedule(self) -> dict:
        """
        Retrieves the comprehensive match schedule and current match statuses.

        Returns:
            dict: A dictionary containing 'headers' and 'rows' for the UI table.
        """
        query = """
            SELECT m.match_date, t1.team_name, t2.team_name, m.status
            FROM MATCHES m
            JOIN TEAMS t1 ON m.team1_id = t1.team_id
            JOIN TEAMS t2 ON m.team2_id = t2.team_id
            ORDER BY m.match_date DESC;
        """
        rows = self._fetch_data(query)
        if not rows: return {"headers": ["MESSAGE"], "rows": [["NO RESULTS FOUND"]]}
        if isinstance(rows[0][0], str) and rows[0][0].startswith("DB ERROR"): return {"headers": ["ERROR"], "rows": [[r[0]] for r in rows]}
        return {"headers": ["MATCH DATE", "TEAM 1", "TEAM 2", "STATUS"], "rows": [[str(r[0]), str(r[1]), str(r[2]), str(r[3])] for r in rows]}

    def get_audit_log(self) -> dict:
        """
        Retrieves the match status audit log for tracking system updates.

        Returns:
            dict: A dictionary containing 'headers' and 'rows' for the UI table.
        """
        query = "SELECT match_id, old_status, new_status, changed_at FROM MATCH_AUDIT_LOG ORDER BY changed_at DESC;"
        rows = self._fetch_data(query)
        if not rows: return {"headers": ["MESSAGE"], "rows": [["NO AUDIT LOGS FOUND"]]}
        if isinstance(rows[0][0], str) and rows[0][0].startswith("DB ERROR"): return {"headers": ["ERROR"], "rows": [[r[0]] for r in rows]}
        return {"headers": ["MATCH ID", "OLD STATUS", "NEW STATUS", "TIMESTAMP"], "rows": [[str(r[0]), str(r[1]), str(r[2]), str(r[3])[:16]] for r in rows]}

    def get_upcoming_matches_with_broadcasts(self) -> list:
        """Retrieves upcoming matches with their venues and broadcast platforms."""
        query = """
            SELECT t1.team_name, t2.team_name, v.name, COALESCE(b.platform, 'Local')
            FROM MATCHES m
            JOIN TEAMS t1 ON m.team1_id = t1.team_id
            JOIN TEAMS t2 ON m.team2_id = t2.team_id
            JOIN VENUES v ON m.venue_id = v.venue_id
            LEFT JOIN BROADCASTS b ON m.match_id = b.match_id
            WHERE m.status IN ('scheduled', 'live')
        """
        rows = self._fetch_data(query)
        if not rows or (isinstance(rows[0][0], str) and rows[0][0].startswith("DB ERROR")): return []
        return [[str(c) for c in r] for r in rows]

    def get_player_performance_data(self) -> list:
        """
        Retrieves performance trends for the top 5 players based on average rating.
        Fetches the last 15 ratings for each player.

        Returns:
            list: A list of dictionaries, each containing a player's name and their rating history.
                  e.g. [{'name': 'PlayerA', 'ratings': [7.1, 8.2, ...]}, ...]
        """
        conn = None
        try:
            conn = pyodbc.connect(self.conn_str, timeout=3)
            cursor = conn.cursor()

            # 1. Get top 5 players by average rating who have played at least 5 games
            top_players_query = """
                SELECT TOP 5 p.player_id, p.name
                FROM PLAYERS p
                JOIN GAME_STATS gs ON p.player_id = gs.player_id
                GROUP BY p.player_id, p.name
                HAVING COUNT(gs.game_id) >= 5
                ORDER BY AVG(gs.rating) DESC;
            """
            cursor.execute(top_players_query)
            top_players = cursor.fetchall()

            if not top_players: return []

            # 2. For each player, get their last 15 game ratings
            trends_data = []
            ratings_query = """
                SELECT TOP 15 gs.rating FROM GAME_STATS gs
                JOIN GAMES g ON gs.game_id = g.game_id JOIN MATCHES m ON g.match_id = m.match_id
                WHERE gs.player_id = ? ORDER BY m.match_date DESC, g.game_id DESC;
            """
            for player_id, player_name in top_players:
                cursor.execute(ratings_query, player_id)
                ratings_rows = cursor.fetchall()
                ratings = [row.rating for row in reversed(ratings_rows)]
                if ratings: trends_data.append({"name": str(player_name), "ratings": ratings})
            return trends_data
        except Exception: return [{"name": "DATABASE ERROR", "ratings": [1,1,1]}]
        finally:
            if conn is not None:
                try: conn.close()
                except Exception: pass

    def _execute_non_query(self, query: str, params: tuple) -> str:
        """
        Executes a data modification query (INSERT, UPDATE, DELETE).
        
        Args:
            query (str): The SQL query string.
            params (tuple): The parameters for the query.
            
        Returns:
            str: Success or error message.
        """
        conn = None
        try:
            conn = pyodbc.connect(self.conn_str, timeout=3)
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return "DB UPDATE SUCCESSFUL"
        except Exception as e:
            return f"DB ERROR: {str(e)[:50]}"
        finally:
            if conn is not None:
                try: conn.close()
                except Exception: pass

    def add_player(self, name: str, role: str) -> str:
        """Inserts a new player into the database."""
        query = "INSERT INTO PLAYERS (name, role) VALUES (?, ?);"
        return self._execute_non_query(query, (name, role))

    def update_match_status(self, match_id_str: str, status: str) -> str:
        """Updates the status of a specific match."""
        try:
            match_id = int(match_id_str)
        except ValueError:
            return "ERROR: MATCH ID MUST BE NUMERIC"
        query = "UPDATE MATCHES SET status = ? WHERE match_id = ?;"
        return self._execute_non_query(query, (status, match_id))

    def delete_game_stat(self, stat_id_str: str) -> str:
        """Deletes a game stat record from the database."""
        try:
            stat_id = int(stat_id_str)
        except ValueError:
            return "ERROR: STAT ID MUST BE NUMERIC"
        query = "DELETE FROM GAME_STATS WHERE stat_id = ?;"
        return self._execute_non_query(query, (stat_id,))