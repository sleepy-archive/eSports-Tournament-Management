import random
from datetime import date, timedelta

# ==========================================
# 1. HONKAI: STAR RAIL LORE DATA POOLS
# ==========================================

teams_data = [
    ("Astral Express Nameless", "Cosmos"), ("Stellaron Hunters", "Cosmos"),
    ("IPC Diamond Division", "Pier Point"), ("Ten Stonehearts", "Pier Point"),
    ("Belobog Supreme", "Jarilo-VI"), ("Wildfire Underground", "Jarilo-VI"),
    ("Cloud Knights Vanguard", "Xianzhou Luofu"), ("Ten-Lords Commission", "Xianzhou Luofu"),
    ("Penacony Dreamweavers", "Penacony"), ("Oak Family Aristocrats", "Penacony"),
    ("Genius Society Club", "Cosmos"), ("Intelligentsia Guild", "Cosmos"),
    ("Galaxy Rangers & Co.", "Cosmos"), ("Masked Fools Troupe", "Tavern"),
    ("Annihilation Gang", "Talia"), ("Antimatter Legion", "Cosmos"),
    ("Doctors of Chaos", "Cosmos"), ("Denizens of Abundance", "Cosmos"),
    ("The Swarm Propagation", "Cosmos"), ("Garden of Recollection", "Cosmos"),
    ("Mourning Actors", "Cosmos"), ("History Fictionologists", "Cosmos"),
    ("Knights of Beauty", "Cosmos"), ("Omen Vanguards", "Cosmos"),
    ("Xianzhou Alliance", "Xianzhou Zhuming"), ("Yaoqing Merlin's Claws", "Xianzhou Yaoqing"),
    ("Architects Vanguard", "Jarilo-VI"), ("Device IX Nihility", "Cosmos")
]

roles = [
    "Hunt Fragger", "Erudition IGL", "Destruction Flex", 
    "Preservation Tank", "Harmony Support", "Nihility Lurker", 
    "Abundance Healer", "Remembrance Controller", "Elation Specialist", 
    "Barking Specialist"
]

players_data = [
    "Trailblazer", "March 7th", "Dan Heng", "Himeko", "Welt Yang", 
    "Kafka", "Silver Wolf", "Firefly", "Blade", "Sam", "Mortenax Blade", "Silver Wolf LV.999",
    "Topaz", "Aventurine", "Jade", "Skott", "Opal", "Diamond", "Taravan Keane",
    "Bronya Rand", "Seele", "Gepard Landau", "Luka", "Serval", "Pela", "Clara", "Hook", "Natasha",
    "Jing Yuan", "Yanqing", "Fu Xuan", "Jingliu", "Huohuo", "Tingyun", "Qingque", "Sushang", "Bailu", "Guinaifen", "Jiaoqiu", "Yunli", "Feixiao", "Moze", "Lingsha", "Fugue", "Dan Heng | Imbibitor Lunae", "Luocha",
    "Sunday", "Robin", "Gallagher", "Misha", "Acheron", "Black Swan", "Sparkle", "Boothill", "Rappa",
    "Herta", "Ruan Mei", "Screwllum", "Stephen Lloyd", "Dr. Ratio",
    "Sampo Koski", "Aglaea", "Anaxa", "Cyrene", "Evernight", "Hyacine", "Castorice"
]

venue_names = [
    "Herta Space Station - Master Control Room", "Herta Space Station - Seclusion Zone",
    "Boulder Town Underground Fight Club", "Everwinter Hill - Stellaron Core", "Pillars of Creation",
    "Old Weapon Testing Ground", "Scalegorge Waterscape - Dragonprayer Terrace", 
    "Fyxestroll Garden - Suppression Tower", "Shackling Prison - Bottom Depths",
    "Palace of Astrum", "Penacony Grand Theater - Main Stage", "Radiant Feldspar - Poolside Arena", 
    "Clock Studios Theme Park", "Dewlight Pavilion - Sandpit", "SoulGlad Scorchsand Audition Venue",
    "Planarcadia - Wispae Amusement Park", "World in Canvas", "Echo of War: Doomsday Beast",
    "Echo of War: Phantylia the Undying", "Echo of War: Starcrusher Swarm King", "Echo of War: Septimus, Harmonious Choir"
]

map_names = [
    "Supply Zone Railway", "Base Zone Monitor Room", "Storage Zone Atrium",
    "Rivet Town Alleyways", "Everwinter Peak", "Corridor of Fading Echoes", "Robot Settlement Camp",
    "Cloudford Cargo Skiffs", "Alchemy Commission Furnace", "Stargazer Navalia Docks",
    "Golden Hour Dreamscape", "Dewlight Pavilion Cityscape", "Child's Dream", "Dream's Edge",
    "Seclusion Zone - Ruan Mei's Lab", "Shackling Prison Depth", "Skysplitter Helipad",
    "Dovebrook District", "Seafeld TV Tower", "Eternal Holy City Okhema"
]

game_modes = [
    "Payload (Trotter Escort)", "Team Deathmatch", "Capture the Stellaron", 
    "King of the Hill", "Swarm Survival", "Boss Raid", 
    "Memory of Chaos Speedrun", "Pure Fiction Showdown", 
    "Apocalyptic Shadow Boss Rush", "Divergent Universe Endless", 
    "Gold and Gears Draft", "Anomaly Arbitration"
]

tourney_names = [
    "Aetherium Wars Championship", "Boulder Town Super League", "Interastral Tournament Festival", 
    "Wardance Ceremony", "Simulated Universe Cup", "Clockie's Dreamplay Derby",
    "Aurum Alley Hustle", "Cosmicon Trade War", "Starward Mode Invitational"
]

broadcast_platforms = [
    "Interastral Peace Broadcast", "Owlbert's Twitch", "Clock Studios Network", 
    "Genius Society Archives", "Astral Express Data Bank", "Garden of Recollection Streams"
]

# --- GENERATION SETTINGS ---
NUM_TEAMS = len(teams_data)
NUM_PLAYERS = len(players_data)
TOTAL_MATCHES = 300   
TOTAL_GAMES = 1000    

def random_date(start_year=2024, end_year=2026):
    start = date(start_year, 1, 1)
    end = date(end_year, 12, 31)
    return start + timedelta(days=random.randint(0, (end - start).days))

# Helper to escape single quotes for SQL
def esc(val):
    return str(val).replace("'", "''")

# Helper to chunk large inserts to avoid SQL Server's 1000 row limit
def write_batches(f, table_name, columns, rows, batch_size=900):
    for i in range(0, len(rows), batch_size):
        batch = rows[i:i + batch_size]
        f.write(f"INSERT INTO {table_name} ({columns}) VALUES\n")
        f.write(",\n".join(batch) + ";\nGO\n\n")

# ==========================================
# 2. SQL GENERATION LOGIC
# ==========================================
with open("hsr_esports_master_seed.sql", "w", encoding="utf-8") as f:
    f.write("USE EsportsTournament;\nGO\n\n")
    f.write("-- NOTE: Execute this on an empty database (or truncate tables first) so IDENTITY keys start at 1\n\n")

    # 1. TOURNAMENTS
    f.write("-- 1. TOURNAMENTS\n")
    rows = []
    for i in range(15):
        start = random_date(2025, 2026)
        end = start + timedelta(days=random.randint(14, 45))
        rows.append(f"('{esc(random.choice(tourney_names))} Vol. {i+1}', '{start}', '{end}')")
    write_batches(f, "TOURNAMENTS", "tournament_name, start_date, end_date", rows)

    # 2. TEAMS
    f.write("-- 2. TEAMS\n")
    rows = [f"('{esc(team)}', '{esc(region)}')" for team, region in teams_data]
    write_batches(f, "TEAMS", "team_name, region", rows)

    # 3. VENUES
    f.write("-- 3. VENUES\n")
    rows = []
    for venue in venue_names:
        is_online = 1 if any(kw in venue for kw in ["Simulated", "Dreamscape", "World in Canvas"]) else random.choice([0, 1])
        loc = "Metaverse" if is_online else "Physical Domain"
        rows.append(f"('{esc(venue)}', '{esc(loc)}', {is_online})")
    write_batches(f, "VENUES", "name, location, is_online", rows)

    # 4. PLAYERS
    f.write("-- 4. PLAYERS\n")
    rows = []
    for name in players_data:
        role = "Barking Specialist" if name == "Skott" else random.choice(roles[:-1]) 
        rows.append(f"('{esc(name)}', '{esc(role)}')")
    write_batches(f, "PLAYERS", "name, role", rows)

    # 5. PATCHES
    f.write("-- 5. PATCHES\n")
    rows = []
    patch_versions = ["1.0", "1.4", "2.0", "2.2", "2.4", "3.0", "3.1", "4.0", "4.2", "4.3"]
    for pv in patch_versions:
        rows.append(f"('v{pv}', '{random_date(2024, 2026)}')")
    write_batches(f, "PATCHES", "version_number, release_date", rows)

    # 6. MAPS
    f.write("-- 6. MAPS\n")
    rows = []
    for map_name in map_names:
        rows.append(f"('{esc(map_name)}', '{esc(random.choice(game_modes))}')")
    write_batches(f, "MAPS", "map_name, game_mode", rows)

    # 7. TOURNAMENT_STAGES
    f.write("-- 7. TOURNAMENT STAGES\n")
    rows = []
    for i in range(45):
        rows.append(f"({random.randint(1, 15)}, '{esc(random.choice(['Group Stage', 'Playoffs', 'Quarterfinals', 'Semifinals', 'Grand Finals']))}')")
    write_batches(f, "TOURNAMENT_STAGES", "tournament_id, stage_name", rows)

    # 8. PLAYER_HISTORY
    f.write("-- 8. PLAYER HISTORY\n")
    rows = []
    for i in range(NUM_PLAYERS):
        rows.append(f"({i+1}, {random.randint(1, NUM_TEAMS)}, '{random_date(2024, 2025)}', NULL)")
    write_batches(f, "PLAYER_HISTORY", "player_id, team_id, join_date, leave_date", rows)

    # 9. MATCHES
    f.write("-- 9. MATCHES\n")
    rows = []
    for i in range(TOTAL_MATCHES):
        t1, t2 = random.sample(range(1, NUM_TEAMS + 1), 2)
        status = random.choice(['scheduled', 'live', 'completed'])
        winner = "NULL" if status != 'completed' else random.choice([t1, t2])
        fmt = random.choice(['Bo1', 'Bo3', 'Bo5', 'Bo7'])
        rows.append(f"({random.randint(1, 45)}, {t1}, {t2}, {winner}, {random.randint(1, len(venue_names))}, '{random_date(2025, 2026)}', '{status}', '{fmt}')")
    write_batches(f, "MATCHES", "stage_id, team1_id, team2_id, winner_team_id, venue_id, match_date, status, format", rows)

    # 10. BROADCASTS
    f.write("-- 10. BROADCASTS\n")
    rows = []
    for i in range(250):
        plat = random.choice(broadcast_platforms)
        domain = plat.split()[0].lower().replace("'", "")
        rows.append(f"({random.randint(1, TOTAL_MATCHES)}, '{esc(plat)}', 'https://{domain}.tv/stream/{random.randint(1000,9999)}', '{random.choice(['EN', 'JP', 'CN', 'KR'])}')")
    write_batches(f, "BROADCASTS", "match_id, platform, url, language", rows)

    # 11. GAMES
    f.write("-- 11. GAMES\n")
    rows = []
    for i in range(TOTAL_GAMES):
        winner = random.randint(1, NUM_TEAMS)
        rows.append(f"({random.randint(1, TOTAL_MATCHES)}, {random.randint(1, 10)}, {random.randint(1, 5)}, {random.randint(1, len(map_names))}, {winner}, {random.randint(1200, 4500)})")
    write_batches(f, "GAMES", "match_id, patch_id, game_number, map_id, winner_team_id, duration_seconds", rows)

    # 12. GAME_STATS
    f.write("-- 12. GAME STATS\n")
    rows = []
    for i in range(TOTAL_GAMES * 4):  
        player_id = random.randint(1, NUM_PLAYERS)
        
        if players_data[player_id - 1] == "Skott":
            pts, ast, rtg = 0, 99, 10.0
        else:
            pts = random.randint(0, 45)
            ast = random.randint(0, 25)
            rtg = round(random.uniform(4.0, 9.9), 1)
            
        rows.append(f"({random.randint(1, TOTAL_GAMES)}, {player_id}, {pts}, {ast}, {rtg})")
    write_batches(f, "GAME_STATS", "game_id, player_id, points_scored, assists, rating", rows)

print("✅ Master HSR Seed Script Generated with Escaped Strings and Chunking.")