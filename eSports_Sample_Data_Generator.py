import random
from datetime import date, timedelta

# --- MASSIVE ANIME DATA POOLS ---
first_names = [
    "Goku", "Vegeta", "Naruto", "Sasuke", "Luffy", "Zoro", "Ichigo", "Edward", "Light", "Lelouch", # Shonen/Classics
    "Eren", "Levi", "Mikasa", "Gintoki", "Kagura", "Gon", "Killua", "Jotaro", "Dio", "Guts", # Action/Seinen
    "Shinji", "Rei", "Asuka", "Lain", "Motoko", "Spike", "Faye", "Koyomi", "Hitagi", "Shinobu", # Cult/Sci-Fi/Monogatari
    "Rimuru", "Ainz", "Subaru", "Kazuma", "Tanya", "Shiroe", "Saitama", "Mob", "Denji", "Aki" # Isekai/Modern
]
last_names = [
    "Uzumaki", "Uchiha", "Monkey", "Kurosaki", "Elric", "Yagami", "Lamperouge", "Yeager", "Ackerman", 
    "Sakata", "Freecss", "Zoldyck", "Kujo", "Brando", "Ikari", "Ayanami", "Soryu", "Iwakura", "Kusanagi", 
    "Spiegel", "Araragi", "Senjougahara", "Oshino", "Tempest", "Ooal Gown", "Natsuki", "Degurechaff", "Hayakawa"
]
roles = ["IGL", "Lurker", "Support", "Entry Fragger", "Flex", "Anchor", "Sniper", "Controller", "Initiator", "Duelist"]
regions = ["Tokyo-3", "Soul Society", "Grand Line", "Hidden Leaf", "Amestris", "Cyberia", "Roanapur", "Aincrad", "Kansai"]

team_names = [
    "Akatsuki", "Straw Hat Pirates", "Phantom Troupe", "Survey Corps", "Black Knights", "NERV", 
    "SOS Brigade", "Fairy Tail", "Night Raid", "Passione", "Stardust Crusaders", "Gotei 13", 
    "State Alchemists", "Section 9", "Lagoon Company", "Future Gadget Lab", "Odd Jobs Gin", "Espada"
]

venue_names = [
    "Tenkaichi Budokai Arena", "U.A. High Stadium", "Heavens Arena", "Dark Tournament Ring", 
    "Cell Games Arena", "Tokyo Dome (Underground)", "Cyberia Club", "Mabe Village Square"
]

map_names = ["Planet Namek", "Wall Maria", "Shibuya Station", "Hueco Mundo", "Final Valley", "Kamurocho", "Wired Layer 3"]
game_modes = ["Bomb Defusal", "Hostage Rescue", "Team Deathmatch", "Capture the Flag", "King of the Hill", "Payload"]

tourney_names = ["Dark Tournament", "Holy Grail War", "Chunin Exams", "Tournament of Power", "Grand Magic Games", "VMMO Championship"]

# --- GENERATION SETTINGS ---
NUM_ROWS = 100 # Total items per major table (100 players, 100 teams, etc.)
TOTAL_MATCHES = 150
TOTAL_GAMES = 300

def random_date(start_year=2024, end_year=2026):
    start = date(start_year, 1, 1)
    end = date(end_year, 12, 31)
    return start + timedelta(days=random.randint(0, (end - start).days))

# --- SQL GENERATION LOGIC ---
with open("master_anime_seed.sql", "w", encoding="utf-8") as f:
    f.write("USE EsportsTournament;\nGO\n\n")
    f.write("-- NOTE: Execute this on an empty database (or truncate tables first) so IDENTITY keys start at 1\n\n")

    # 1. TOURNAMENTS (Base size 20)
    f.write("-- 1. TOURNAMENTS\nINSERT INTO TOURNAMENTS (tournament_name, start_date, end_date) VALUES\n")
    rows = []
    for i in range(20):
        start = random_date(2025, 2026)
        end = start + timedelta(days=random.randint(14, 45))
        rows.append(f"('{random.choice(tourney_names)} Vol. {i+1}', '{start}', '{end}')")
    f.write(",\n".join(rows) + ";\nGO\n\n")

    # 2. TEAMS (Base size NUM_ROWS)
    f.write("-- 2. TEAMS\nINSERT INTO TEAMS (team_name, region) VALUES\n")
    rows = []
    for i in range(NUM_ROWS):
        team = f"{random.choice(team_names)} {random.choice(['Alpha', 'Black', 'Zero', 'Ex', 'Red', 'Prime', ''])}".strip()
        rows.append(f"('{team}', '{random.choice(regions)}')")
    f.write(",\n".join(rows) + ";\nGO\n\n")

    # 3. VENUES (Base size 30)
    f.write("-- 3. VENUES\nINSERT INTO VENUES (name, location, is_online) VALUES\n")
    rows = []
    for i in range(30):
        is_online = random.choice([0, 1])
        loc = "Wired Network" if is_online else random.choice(regions)
        rows.append(f"('{random.choice(venue_names)} - Area {i+1}', '{loc}', {is_online})")
    f.write(",\n".join(rows) + ";\nGO\n\n")

    # 4. PLAYERS (Base size NUM_ROWS * 2)
    f.write("-- 4. PLAYERS\nINSERT INTO PLAYERS (name, role) VALUES\n")
    rows = []
    for i in range(NUM_ROWS * 2):
        name = f"{random.choice(first_names)} {random.choice(last_names)}"
        rows.append(f"('{name}', '{random.choice(roles)}')")
    f.write(",\n".join(rows) + ";\nGO\n\n")

    # 5. PATCHES (Base size 15)
    f.write("-- 5. PATCHES\nINSERT INTO PATCHES (version_number, release_date) VALUES\n")
    rows = []
    for i in range(15):
        rows.append(f"('v{random.randint(1,4)}.{random.randint(0,9)}.{i}', '{random_date(2024, 2025)}')")
    f.write(",\n".join(rows) + ";\nGO\n\n")

    # 6. MAPS (Base size 20)
    f.write("-- 6. MAPS\nINSERT INTO MAPS (map_name, game_mode) VALUES\n")
    rows = []
    for i in range(20):
        rows.append(f"('{random.choice(map_names)}', '{random.choice(game_modes)}')")
    f.write(",\n".join(rows) + ";\nGO\n\n")

    # 7. TOURNAMENT_STAGES (Assign to tournaments 1-20)
    f.write("-- 7. TOURNAMENT STAGES\nINSERT INTO TOURNAMENT_STAGES (tournament_id, stage_name) VALUES\n")
    rows = []
    for i in range(50):
        rows.append(f"({random.randint(1, 20)}, '{random.choice(['Group Stage', 'Quarterfinals', 'Semifinals', 'Grand Finals'])}')")
    f.write(",\n".join(rows) + ";\nGO\n\n")

    # 8. PLAYER_HISTORY (Assign players 1-200 to teams 1-100)
    f.write("-- 8. PLAYER HISTORY\nINSERT INTO PLAYER_HISTORY (player_id, team_id, join_date, leave_date) VALUES\n")
    rows = []
    for i in range(NUM_ROWS * 2):
        rows.append(f"({i+1}, {random.randint(1, NUM_ROWS)}, '{random_date(2024, 2025)}', NULL)")
    f.write(",\n".join(rows) + ";\nGO\n\n")

    # 9. MATCHES
    f.write("-- 9. MATCHES\nINSERT INTO MATCHES (stage_id, team1_id, team2_id, winner_team_id, venue_id, match_date, status, format) VALUES\n")
    rows = []
    for i in range(TOTAL_MATCHES):
        t1, t2 = random.sample(range(1, NUM_ROWS + 1), 2)
        status = random.choice(['scheduled', 'live', 'completed'])
        winner = "NULL" if status != 'completed' else random.choice([t1, t2])
        fmt = random.choice(['Bo1', 'Bo3', 'Bo5'])
        rows.append(f"({random.randint(1, 50)}, {t1}, {t2}, {winner}, {random.randint(1, 30)}, '{random_date(2025, 2026)}', '{status}', '{fmt}')")
    f.write(",\n".join(rows) + ";\nGO\n\n")

    # 10. BROADCASTS (Attach to Matches)
    f.write("-- 10. BROADCASTS\nINSERT INTO BROADCASTS (match_id, platform, url, language) VALUES\n")
    rows = []
    for i in range(100):
        plat = random.choice(['Twitch', 'YouTube', 'NicoNico'])
        rows.append(f"({random.randint(1, TOTAL_MATCHES)}, '{plat}', 'https://{plat.lower()}.tv/esports_stream_{i}', '{random.choice(['EN', 'JP', 'KR'])}')")
    f.write(",\n".join(rows) + ";\nGO\n\n")

    # 11. GAMES
    f.write("-- 11. GAMES\nINSERT INTO GAMES (match_id, patch_id, game_number, map_id, winner_team_id, duration_seconds) VALUES\n")
    rows = []
    for i in range(TOTAL_GAMES):
        rows.append(f"({random.randint(1, TOTAL_MATCHES)}, {random.randint(1, 15)}, {random.randint(1, 5)}, {random.randint(1, 20)}, NULL, {random.randint(900, 3600)})")
    f.write(",\n".join(rows) + ";\nGO\n\n")

    # 12. GAME_STATS
    f.write("-- 12. GAME STATS\nINSERT INTO GAME_STATS (game_id, player_id, points_scored, assists, rating) VALUES\n")
    rows = []
    for i in range(TOTAL_GAMES * 2):
        pts = random.randint(0, 60)
        ast = random.randint(0, 25)
        rtg = round(random.uniform(4.0, 10.0), 1)
        rows.append(f"({random.randint(1, TOTAL_GAMES)}, {random.randint(1, NUM_ROWS * 2)}, {pts}, {ast}, {rtg})")
    f.write(",\n".join(rows) + ";\nGO\n\n")

print("Master Anime Seed Script Generated: master_anime_seed.sql")