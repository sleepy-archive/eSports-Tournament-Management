USE EsportsTournament;
GO

-- 1. Insert 15 Tournaments
INSERT INTO TOURNAMENTS (tournament_name, start_date, end_date) VALUES
('Waifu Wars Spring Split', '2026-01-10', '2026-03-15'),
('Waifu Wars Summer Split', '2026-06-01', '2026-08-20'),
('Shounen Showdown', '2026-04-05', '2026-05-10'),
('The Holy Grail War', '2026-09-01', '2026-09-14'),
('Chunin Exams Invitational', '2026-10-10', '2026-11-15'),
('Cell Games 2026', '2026-11-20', '2026-11-25'),
('Grand Magic Games', '2026-07-01', '2026-07-15'),
('U.A. Sports Festival', '2026-05-15', '2026-05-30'),
('Dark Tournament', '2026-02-01', '2026-03-01'),
('Vytal Festival Tournament', '2026-08-01', '2026-08-15'),
('Kengan Annihilation', '2026-12-01', '2026-12-31'),
('Ragnarok Arena', '2026-03-20', '2026-04-20'),
('Shaman Fight Tokyo', '2026-06-15', '2026-07-20'),
('Isekai Championship', '2026-01-05', '2026-02-15'),
('Tokyo Anime Award Fest Clash', '2026-09-20', '2026-10-05');

-- 2. Insert 15 Teams
INSERT INTO TEAMS (team_name, region) VALUES
('Straw Hat Pirates', 'Grand Line'),
('Akatsuki', 'Hidden Rain'),
('Survey Corps', 'Paradis'),
('Hashira Corps', 'Japan'),
('Phantom Troupe', 'Meteor City'),
('Black Bulls', 'Clover Kingdom'),
('Fairy Tail Guild', 'Fiore'),
('NERV Evangelions', 'Tokyo-3'),
('Night Raid', 'Capital'),
('SOS Brigade', 'North High'),
('Passione', 'Italy'),
('Joestar Bloodline', 'Global'),
('Yorozuya', 'Edo'),
('Z Fighters', 'Earth'),
('Karasuno Crows', 'Miyagi');

-- 3. Insert 15 Venues
INSERT INTO VENUES (name, location, is_online) VALUES
('Tokyo Dome', 'Tokyo, Japan', 0),
('Saitama Super Arena', 'Saitama, Japan', 0),
('U.A. Stadium', 'Musutafu, Japan', 0),
('Heavens Arena', 'Padokea Republic', 0),
('Final Valley', 'Land of Fire', 0),
('Planet Namek Ruins', 'Namek System', 0),
('Soul Society Arena', 'Seireitei', 0),
('Aincrad Floor 1', 'Virtual Reality', 1),
('Wall Maria District', 'Shiganshina', 0),
('Tartarus Prison Arena', 'Oceanic', 0),
('Infinity Castle', 'Dimensional', 1),
('Marineford Plaza', 'Grand Line', 0),
('Kamurocho Hills', 'Tokyo, Japan', 0),
('Hyperbolic Time Chamber', 'Kami Lookout', 1),
('Yggdrasil Server', 'Online', 1);

-- 4. Insert 15 Players (The Waifus & Heroes)
INSERT INTO PLAYERS (name, role) VALUES
('Asuna Yuuki', 'IGL / Flex'),
('Megumin', 'Burst Damage'),
('Rem', 'Support'),
('Zero Two', 'Entry Fragger'),
('Makima', 'Strategist / Controller'),
('Power', 'Chaotic Fragger'),
('Mikasa Ackerman', 'Slayer'),
('Erza Scarlet', 'Tank / Flex'),
('Saber (Artoria)', 'Melee / IGL'),
('Rin Tohsaka', 'Sniper / Magic'),
('Hinata Hyuga', 'Scout / Support'),
('Kurisu Makise', 'Analyst / Support'),
('Shinobu Kocho', 'Assassin'),
('Nezuko Kamado', 'Brawler'),
('Aqua', 'Healer (Useless)');

-- 5. Insert 15 Patches
INSERT INTO PATCHES (version_number, release_date) VALUES
('v1.0.1', '2026-01-01'), ('v1.0.2', '2026-01-15'), ('v1.1.0', '2026-02-01'),
('v1.1.5', '2026-02-20'), ('v1.2.0', '2026-03-10'), ('v2.0.0', '2026-04-01'),
('v2.0.1', '2026-04-15'), ('v2.1.0', '2026-05-01'), ('v2.2.0', '2026-06-01'),
('v3.0.0', '2026-07-01'), ('v3.0.5', '2026-07-20'), ('v3.1.0', '2026-08-15'),
('v4.0.0', '2026-09-01'), ('v4.1.0', '2026-10-01'), ('v5.0.0', '2026-11-01');

-- 6. Insert 15 Maps
INSERT INTO MAPS (map_name, game_mode) VALUES
('Konoha Village', 'Capture the Flag'),
('Hueco Mundo', 'Team Deathmatch'),
('Shibuya Incident', 'Payload'),
('Shiganshina District', 'Survival'),
('Wano Country', 'King of the Hill'),
('Dressrosa', 'Battle Royale'),
('Alabasta Desert', 'Team Deathmatch'),
('Enies Lobby', 'Payload'),
('Marineford', 'Domination'),
('Kamino Ward', 'Capture the Flag'),
('Tokyo-3', 'Defend the Core'),
('Kyoto Temples', 'Search and Destroy'),
('Osaka Castle', 'King of the Hill'),
('Sapporo Snow Festival', 'Team Deathmatch'),
('Okinawa Beach Episode', 'Free For All');

-- 7. Insert 15 Tournament Stages
INSERT INTO TOURNAMENT_STAGES (tournament_id, stage_name) VALUES
(1, 'Group A'), (1, 'Group B'), (1, 'Quarterfinals'), (1, 'Semifinals'), (1, 'Grand Finals'),
(2, 'Play-ins'), (2, 'Group Stage'), (2, 'Playoffs Round 1'), (2, 'Semifinals'), (2, 'Finals'),
(3, 'Preliminaries'), (3, 'Bracket Stage'), (4, 'Night 1 Clash'), (4, 'Night 2 Clash'), (4, 'Holy Grail Finals');

-- 8. Insert 15 Player Histories (Mapping Players to Teams)
INSERT INTO PLAYER_HISTORY (player_id, team_id, join_date, leave_date) VALUES
(1, 8, '2025-01-01', NULL),      -- Asuna in NERV
(2, 10, '2025-02-15', NULL),     -- Megumin in SOS Brigade
(3, 10, '2025-03-10', NULL),     -- Rem in SOS Brigade
(4, 8, '2025-04-20', NULL),      -- Zero Two in NERV
(5, 5, '2025-01-05', NULL),      -- Makima in Phantom Troupe
(6, 5, '2025-06-11', NULL),      -- Power in Phantom Troupe
(7, 3, '2024-01-01', NULL),      -- Mikasa in Survey Corps
(8, 7, '2024-05-12', NULL),      -- Erza in Fairy Tail
(9, 11, '2025-08-18', NULL),     -- Saber in Passione
(10, 11, '2025-09-01', NULL),    -- Rin in Passione
(11, 2, '2024-10-10', '2025-12-31'), -- Hinata was in Akatsuki (Left)
(11, 14, '2026-01-01', NULL),    -- Hinata joined Z Fighters
(12, 1, '2025-07-07', NULL),     -- Kurisu in Straw Hats
(13, 4, '2024-03-03', NULL),     -- Shinobu in Hashira Corps
(14, 4, '2025-01-15', NULL);     -- Nezuko in Hashira Corps

-- 9. Insert 15 Matches
INSERT INTO MATCHES (stage_id, team1_id, team2_id, winner_team_id, venue_id, match_date, status, format) VALUES
(1, 8, 10, 8, 1, '2026-01-12', 'completed', 'Bo3'),
(2, 5, 3, 5, 2, '2026-01-13', 'completed', 'Bo3'),
(3, 8, 5, 8, 3, '2026-01-20', 'completed', 'Bo5'),
(6, 7, 11, 11, 4, '2026-06-05', 'completed', 'Bo1'),
(7, 11, 4, 4, 5, '2026-06-10', 'completed', 'Bo3'),
(11, 1, 2, NULL, 6, '2026-04-06', 'scheduled', 'Bo3'),
(11, 14, 13, NULL, 7, '2026-04-07', 'scheduled', 'Bo3'),
(13, 11, 8, NULL, 11, '2026-09-02', 'live', 'Bo5'),
(1, 4, 7, 4, 8, '2026-01-14', 'completed', 'Bo3'),
(2, 1, 14, 1, 9, '2026-01-15', 'completed', 'Bo3'),
(4, 4, 1, 1, 10, '2026-01-25', 'completed', 'Bo5'),
(5, 8, 1, 8, 1, '2026-01-30', 'completed', 'Bo5'),
(12, 5, 2, NULL, 12, '2026-04-15', 'scheduled', 'Bo5'),
(8, 4, 8, NULL, 13, '2026-06-20', 'scheduled', 'Bo3'),
(15, 10, 3, NULL, 1, '2026-09-25', 'scheduled', 'Bo1');

-- 10. Insert 15 Broadcasts
INSERT INTO BROADCASTS (match_id, platform, url, language) VALUES
(1, 'Twitch', 'twitch.tv/waifuwars', 'English'),
(2, 'YouTube', 'youtube.com/animeesports', 'Japanese'),
(3, 'Twitch', 'twitch.tv/waifuwars', 'English'),
(4, 'Twitch', 'twitch.tv/magicgames', 'Spanish'),
(5, 'YouTube', 'youtube.com/hashiracorps', 'Japanese'),
(6, 'Twitch', 'twitch.tv/shounenshowdown', 'English'),
(7, 'Twitch', 'twitch.tv/shounenshowdown', 'English'),
(8, 'YouTube', 'youtube.com/holygrail', 'Global'),
(9, 'Twitch', 'twitch.tv/waifuwars', 'English'),
(10, 'Twitch', 'twitch.tv/waifuwars', 'Korean'),
(11, 'YouTube', 'youtube.com/animeesports', 'English'),
(12, 'Twitch', 'twitch.tv/waifuwars', 'English'),
(13, 'YouTube', 'youtube.com/shounenshowdown', 'Japanese'),
(14, 'Twitch', 'twitch.tv/summersplit', 'English'),
(15, 'Twitch', 'twitch.tv/tokyoanime', 'Japanese');

-- 11. Insert 15 Games (Linked to Matches)
INSERT INTO GAMES (match_id, patch_id, game_number, map_id, winner_team_id, duration_seconds) VALUES
(1, 1, 1, 1, 8, 1800), (1, 1, 2, 2, 10, 2100), (1, 1, 3, 3, 8, 1950), -- Match 1: NERV beats SOS 2-1
(2, 1, 1, 4, 5, 1500), (2, 1, 2, 5, 5, 1600),                          -- Match 2: Phantom Troupe sweeps Survey Corps
(3, 2, 1, 6, 8, 2400), (3, 2, 2, 7, 5, 2200), (3, 2, 3, 8, 8, 2500), -- Match 3 partial games
(4, 9, 1, 9, 11, 1200),                                                -- Match 4: Passione wins Bo1
(5, 9, 1, 10, 4, 1800), (5, 9, 2, 11, 11, 1900), (5, 9, 3, 12, 4, 2000),-- Match 5: Hashira beats Passione 2-1
(9, 1, 1, 13, 4, 1700), (9, 1, 2, 14, 4, 1650),                        -- Match 9: Hashira sweeps Fairy Tail
(10, 1, 1, 15, 1, 2100);                                               -- Match 10: Straw Hats game 1

-- 12. Insert 15 Game Stats (Linking Players to Games)
INSERT INTO GAME_STATS (game_id, player_id, points_scored, assists, rating) VALUES
(1, 1, 25, 10, 9.5),  -- Asuna (NERV)
(1, 4, 18, 5, 8.0),   -- Zero Two (NERV)
(1, 2, 10, 2, 5.5),   -- Megumin (SOS Brigade) - used explosion once
(1, 3, 5, 15, 8.2),   -- Rem (SOS Brigade)
(4, 5, 30, 8, 9.8),   -- Makima (Phantom Troupe)
(4, 6, 22, 1, 7.5),   -- Power (Phantom Troupe)
(4, 7, 15, 5, 6.0),   -- Mikasa (Survey Corps)
(9, 9, 12, 4, 7.0),   -- Saber (Passione)
(9, 10, 8, 12, 7.5),  -- Rin (Passione)
(10, 13, 20, 5, 8.8), -- Shinobu (Hashira)
(10, 14, 15, 8, 8.0), -- Nezuko (Hashira)
(13, 13, 28, 2, 9.2), -- Shinobu again
(13, 8, 10, 3, 6.5),  -- Erza (Fairy Tail)
(15, 12, 5, 20, 9.0), -- Kurisu (Straw Hats)
(15, 11, 12, 10, 8.5);-- Hinata (Z Fighters)
GO