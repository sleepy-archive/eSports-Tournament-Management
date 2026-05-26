import sys
import queue
import threading
import time
import pygame
import random

import eSports_Engine as db_engine
from eSports_config import Assets, Config
from eSports_gfx import Graphics
from eSports_Screens import DataViewer, GraphViewer, FormScreen
from eSports_widgets import CentralCore, FloatingHex, FloatyButton, EsportsCoreLog

class LayoutManager:
    """Manages the main UI layout, navigation state, and asynchronous data loading."""
    
    def __init__(self) -> None:
        """Initializes the layout manager, UI components, and state variables."""
        self.focus_area: str = "TOP"
        self.focus_idx: int = 0
        self.mode: str = 'OVERVIEW'
        
        self.loading: bool = False
        self.load_prog: float = 0.0
        self.vis_load_prog: float = 0.0
        self.load_txt: str = ""
        
        self.db = db_engine.DatabaseManager()
        self.ui_queue: queue.Queue = queue.Queue()
        
        self.core = CentralCore()
        self.log = EsportsCoreLog()
        self.viewer = DataViewer()
        self.graph_viewer = GraphViewer()
        self.form_screen = FormScreen()
        
        self.tabs = ["OVERVIEW", "ROSTERS & TEAMS", "MATCH TRACKER", "DATABANK OPS", "SETTINGS"]
        self.actions = {
            'OVERVIEW': ['AETHERIUM WARS', 'LIVE BROADCASTS', 'COMBAT METRICS'],
            'ROSTERS & TEAMS': ['ACTIVE ROSTERS', 'GLOBAL STANDINGS', 'ELITE TIER'],
            'MATCH TRACKER':  ['FULL SCHEDULE', 'MATCH LOGS'],
            'DATABANK OPS': ['REGISTER PLAYER', 'UPDATE MATCH', 'ERASE RECORD'],
            'SETTINGS':  ['TOGGLE THEME', 'DISCONNECT']
        }
        
        self.tab_btns = []
        self.act_btns = []
        self._cached_palette_name = None
        self._top_bar_surf = None
        self._overlay_surf = None

        self.last_ticker_time = time.time()
        self.ticker_items = []
        self.ticker_idx = 0
        
        self.fan_names = [
            "Kafka", "Silver Wolf", "Blade", "Dan Heng", "March 7th", "Jing Yuan", 
            "Seele", "Bronya", "Himeko", "Welt", "Acheron", "Aventurine", "Black Swan", 
            "Sparkle", "Skott", "Firefly", "Ruan Mei", "Dr. Ratio", "Topaz", "Jade", 
            "Sunday", "Robin", "Gallagher", "Boothill", "Tingyun", "Qingque", "Clara", 
            "Hook", "Sampo", "Guinaifen", "Huohuo", "Feixiao", "Lingsha", "Moze", "Yunli",
            "Pom-Pom", "Peppy", "Diting", "Clockie", "Hanunue", "Origami_Bird",
            "TrashCanEnthusiast", "Nameless_001", "IPC_Worker_404", "Belobog_Citizen", 
            "Xianzhou_Local", "Penacony_Dreamer", "Herta_Puppet_013", "Gamer_SilverWolf_Fan", 
            "Masked_Fool_99", "Elation_Follower", "Trailblazer_Simp", "Galactic_Batter", 
            "Astral_Express_Conductor", "Cloud_Knight_Recruit", "Trotter_Lover", 
            "Praise_The_Amber_Lord", "Genius_Society_Fan"
        ]
        self.fan_comments = [
            "Excited, can't wait!", "This is going to be epic!", "My bets are in!", 
            "Let's gooooo!", "I hope they play well.", "Hype!!", "Will be watching live!", 
            "Can't believe this matchup!!", "WOOF WOOF BARK BARK!", "ALL IN!", 
            "I rate this match 0 points!", "May the best team win.", "Setting seas ablaze!", 
            "Is there a prize for guessing the winner?", "I'll stream this later!", 
            "Good luck, have fun!", "Skill issue if they lose this.", "Such a beautiful play!", 
            "Can't wait to analyze the stats.", "Who's the sponsor for this?", 
            "Are we getting free Stellar Jades for watching?", "Absolute cinema.",
            "Praise the Amber Lord!", "Where's Pom-Pom when you need them?", 
            "I bet 500 Stellar Jades on this!", "This match is pure Elation!", 
            "My dreamscape connection is lagging, who's winning?", "gg ez", "What a throw!", 
            "Is this broadcast sponsored by the IPC?", "I should be researching, but this is too good.", 
            "Rules are made to be broken!", "They need to buff Destruction characters.", 
            "Harmony supports diff.", "If they lose, I'm jumping into a trash can.", 
            "Are we getting a rerun of this match?", "Clockie says: Tick-tock, time's up!", 
            "May this match be blessed by Akivili.", "Bro forgot to bring a healer.", 
            "That ultimate was perfectly timed!", "I've been waiting for this matchup since the Amber Era started.", 
            "Can they beat the Antimatter Legion though?", "The Swarm is less annoying than that team's comp.", 
            "I'm shaking right now!", "Penacony's stadium looks amazing on stream.", 
            "Who let bro cook???", "Boooooring, next match please.", "Wait, did they just do that?!", 
            "I need a highlight clip of that ASAP.", "This is going down in the Data Bank!"
        ]
        
        self._start_ticker_fetch()

        self._refresh_dock()

    def _start_ticker_fetch(self) -> None:
        """Starts the background thread for fetching ticker data."""
        t = threading.Thread(target=self._fetch_ticker_data)
        t.daemon = True
        t.start()

    def _fetch_ticker_data(self) -> None:
        """Continuously fetches upcoming match broadcasts and fan comments to populate the UI ticker."""
        while True:
            try:
                rows = self.db.get_upcoming_matches_with_broadcasts()
                if rows:
                    items = []
                    for r in rows:
                        items.append(f"{r[0]} VS {r[1]} @ {r[2]} [LIVE: {r[3]}]")
                        items.append(f"@{random.choice(self.fan_names)}: {random.choice(self.fan_comments)}")
                    self.ui_queue.put(("TICKER_UPDATE", items))
            except Exception:
                pass
            time.sleep(60)

    def _refresh_dock(self) -> None:
        """Refreshes the navigation buttons based on the current active tab."""
        self.tab_btns.clear()
        tab_width, spacing = 210, 15
        total_tab_w = len(self.tabs) * tab_width + (len(self.tabs) - 1) * spacing
        start_x_tabs = (Config.WIDTH - total_tab_w) // 2
        for i, tab_name in enumerate(self.tabs):
            x_pos = start_x_tabs + i * (tab_width + spacing)
            self.tab_btns.append(FloatyButton(x_pos, 15, tab_width, 40, tab_name))

        self.act_btns.clear()
        action_labels = self.actions.get(self.mode, [])
        btn_width = 280
        total_act_w = len(action_labels) * btn_width + (len(action_labels) - 1) * spacing
        start_x_acts = (Config.WIDTH - total_act_w) // 2
        for i, label in enumerate(action_labels):
            x_pos = start_x_acts + i * (btn_width + spacing)
            self.act_btns.append(FloatyButton(x_pos, Config.HEIGHT - 90, btn_width, 60, label))
        
        if self.focus_area == "BOTTOM": 
            self.focus_idx = min(self.focus_idx, max(0, len(self.act_btns) - 1))

    def _thread_task(self, action: str) -> None:
        """
        Executes a database query asynchronously to prevent blocking the main render loop.
        
        Args:
            action (str): The requested database action to execute.
        """
        try:
            self.ui_queue.put(("PROGRESS", 0.2))
            self.ui_queue.put(("LOG", f"QUERYING: {action}"))
            
            rows = []
            if action == 'AETHERIUM WARS': rows = self.db.get_tournament_summary()
            elif action == 'LIVE BROADCASTS': rows = self.db.get_live_venues()
            elif action == 'ACTIVE ROSTERS': rows = self.db.get_active_rosters()
            elif action == 'GLOBAL STANDINGS': rows = self.db.get_leaderboard()
            elif action == 'ELITE TIER': rows = self.db.get_elite_tier()
            elif action == 'FULL SCHEDULE': rows = self.db.get_full_schedule()
            elif action == 'MATCH LOGS': rows = self.db.get_audit_log()
            elif action == 'COMBAT METRICS': rows = self.db.get_player_performance_data()
            
            self.ui_queue.put(("PROGRESS", 1.0))
            time.sleep(0.3) 
            if action == 'COMBAT METRICS':
                self.ui_queue.put(("SHOW_GRAPH", {"title": action, "data": rows}))
            else:
                self.ui_queue.put(("SHOW_DATA", {"title": action, "data": rows}))
                
        except Exception:
            self.ui_queue.put(("IMPORTANT", "DATABASE CONNECTION ERROR"))
        finally:
            self.ui_queue.put(("FINISH", None))

    def execute_task(self, action: str) -> None:
        """
        Initiates an asynchronous background task for data retrieval.
        
        Args:
            action (str): The action requested by the user.
        """
        self.core.set_status(action)
        self.loading = True
        self.load_prog, self.vis_load_prog = 0.0, 0.0
        self.load_txt = action
        self.log.add_log_direct(f"REQUESTING: {action}")
        t = threading.Thread(target=self._thread_task, args=(action,))
        t.daemon = True
        t.start()

    def execute_crud(self, action: str, values: list) -> None:
        """Initiates an asynchronous background task for data manipulation (CRUD)."""
        self.core.set_status(action)
        self.loading = True
        self.load_prog, self.vis_load_prog = 0.0, 0.0
        self.load_txt = action
        self.log.add_log_direct(f"EXECUTING: {action}")
        t = threading.Thread(target=self._thread_crud_task, args=(action, values))
        t.daemon = True
        t.start()

    def _thread_crud_task(self, action: str, values: list) -> None:
        """
        Executes a database CRUD operation asynchronously.
        
        Args:
            action (str): The requested database manipulation action.
            values (list): Form input values to be processed.
        """
        try:
            self.ui_queue.put(("PROGRESS", 0.4))
            time.sleep(0.3)
            
            res = "UNKNOWN OPERATION"
            if action == 'REGISTER PLAYER': res = self.db.add_player(values[0], values[1])
            elif action == 'UPDATE MATCH': res = self.db.update_match_status(values[0], values[1])
            elif action == 'ERASE RECORD': res = self.db.delete_game_stat(values[0])
            
            self.ui_queue.put(("PROGRESS", 1.0))
            time.sleep(0.3) 
            
            self.ui_queue.put(("IMPORTANT", res))
            self.ui_queue.put(("LOG", res))
        except Exception as e:
            self.ui_queue.put(("IMPORTANT", f"DATABASE ERROR: {e}"))
        finally:
            self.ui_queue.put(("FINISH", None))

    def _process_queue(self) -> None:
        """Processes inter-thread communication messages from the background data loader."""
        try:
            while True:
                kind, data = self.ui_queue.get_nowait()
                if kind == "LOG": self.log.add_log_direct(data)
                elif kind == "IMPORTANT": self.log.set_important(data)
                elif kind == "PROGRESS": self.load_prog = data
                elif kind == "SHOW_DATA": self.viewer.open(data['title'], data['data']['headers'], data['data']['rows'])
                elif kind == "SHOW_GRAPH": self.graph_viewer.open(data['title'], data['data'])
                elif kind == "FINISH": self.loading = False
                elif kind == "TICKER_UPDATE": self.ticker_items = data
        except queue.Empty:
            pass

    def trigger_action(self, text: str, app: 'App') -> None:
        """
        Dispatches the appropriate action based on button input.
        
        Args:
            text (str): The text identifier of the action.
            app (App): The main application instance.
        """
        if self.loading: return
        if text == "DISCONNECT":
            pygame.quit()
            sys.exit()
        elif text == "TOGGLE THEME": 
            app.toggle_theme()
            self.log.add_log_direct("THEME SWAPPED")
        elif text == "REGISTER PLAYER": self.form_screen.open("REGISTER PLAYER", ["PLAYER NAME", "ROLE (e.g. IGL)"], self.execute_crud)
        elif text == "UPDATE MATCH": self.form_screen.open("UPDATE MATCH", ["MATCH ID", "NEW STATUS (e.g. live)"], self.execute_crud)
        elif text == "ERASE RECORD": self.form_screen.open("ERASE RECORD", ["STAT ID"], self.execute_crud)
        else:
            self.execute_task(text)

    def handle_input(self, event: pygame.event.Event, app: 'App') -> None:
        """
        Handles incoming user input events.
        
        Args:
            event (pygame.event.Event): The Pygame event to evaluate.
            app (App): The main application instance.
        """
        if self.form_screen.active: return self.form_screen.handle(event)
        if self.graph_viewer.active: return self.graph_viewer.handle(event)
        if self.viewer.active: return self.viewer.handle(event)
        if self.loading: return
        
        if event.type == pygame.MOUSEBUTTONDOWN and self.log.rect.collidepoint(event.pos):
            return self.log.handle_input(event)

        if event.type == pygame.MOUSEMOTION:
            for i, b in enumerate(self.tab_btns):
                if b.rect.collidepoint(event.pos): self.focus_area, self.focus_idx = "TOP", i
            for i, b in enumerate(self.act_btns):
                if b.rect.collidepoint(event.pos): self.focus_area, self.focus_idx = "BOTTOM", i

        if event.type == pygame.MOUSEBUTTONDOWN:
            for i, b in enumerate(self.tab_btns):
                if b.rect.collidepoint(event.pos):
                    self.mode = self.tabs[i]
                    self._refresh_dock()
                    self.core.set_status(self.mode)
            for i, b in enumerate(self.act_btns):
                if b.rect.collidepoint(event.pos): self.trigger_action(b.text, app)

        if event.type == pygame.KEYDOWN:
            self._handle_keyboard(event, app)

    def _handle_keyboard(self, event: pygame.event.Event, app: 'App') -> None:
        """
        Processes keyboard navigation and actions.
        
        Args:
            event (pygame.event.Event): The keyboard event to evaluate.
            app (App): The main application instance.
        """
        if event.key == pygame.K_DOWN and self.focus_area == "TOP":
            self.focus_area = "BOTTOM"
            self.focus_idx = 0
            if self.act_btns: self.core.set_status(self.act_btns[0].text)
        elif event.key == pygame.K_UP and self.focus_area == "BOTTOM":
            self.focus_area = "TOP"
            for i, t in enumerate(self.tabs):
                if t == self.mode: self.focus_idx = i
            self.core.set_status(self.mode)
        
        btns = self.tab_btns if self.focus_area == "TOP" else self.act_btns
        if btns:
            if event.key == pygame.K_RIGHT:
                self.focus_idx = (self.focus_idx + 1) % len(btns)
                self.core.arrow_r = 10
            elif event.key == pygame.K_LEFT:
                self.focus_idx = (self.focus_idx - 1) % len(btns)
                self.core.arrow_l = 10
            
            if self.focus_area == "TOP":
                self.mode = self.tabs[self.focus_idx]
                self._refresh_dock()
                self.core.set_status(self.mode)
            else:
                self.core.set_status(self.act_btns[self.focus_idx].text)

        if event.key == pygame.K_RETURN and self.focus_area == "BOTTOM":
            self.trigger_action(self.act_btns[self.focus_idx].text, app)

    def update(self) -> None:
        """Updates the layout components, processing animations and state changes."""
        self._process_queue() 
        if self.loading: self.vis_load_prog += (self.load_prog - self.vis_load_prog) * 0.2
        if self.viewer.active: self.viewer.update()
        if self.graph_viewer.active: self.graph_viewer.update()
        if self.form_screen.active: self.form_screen.update()

        if time.time() - self.last_ticker_time > 1.0:
            self.last_ticker_time = time.time()
            
            # Silver Wolf Easter Egg (5% chance per tick)
            if random.random() < 0.05:
                self.log.is_hacked = True
                self.log.hack_msg = random.choice(["SYSTEM INTEGRITY COMPROMISED", "SILVER_WOLF.EXE // HACK FAILED", "UNAUTHORIZED ACCESS DETECTED"])
            else:
                self.log.is_hacked = False
                if self.ticker_items:
                    self.ticker_idx = (self.ticker_idx + 1) % len(self.ticker_items)
                    self.log.set_important(self.ticker_items[self.ticker_idx])
            
        self.log.update()
        self.core.update()
        for i, b in enumerate(self.tab_btns): b.update(self.focus_area == "TOP" and self.focus_idx == i)
        if not self.loading:
            for i, b in enumerate(self.act_btns): b.update(self.focus_area == "BOTTOM" and self.focus_idx == i)

    def draw(self, surf: pygame.Surface, p) -> None:
        """
        Renders the complete UI layout to the target surface.
        
        Args:
            surf (pygame.Surface): The target surface to draw upon.
            p (dict): The active color palette dictionary.
        """
        if self._cached_palette_name != p['name']:
            self._cached_palette_name = p['name']
            self._top_bar_surf = None
            self._overlay_surf = None

        self.core.draw(surf, Config.WIDTH//2, Config.HEIGHT//2, p)
        
        if self._top_bar_surf is None:
            self._top_bar_surf = pygame.Surface((Config.WIDTH, 70))
            self._top_bar_surf.set_alpha(200)
            self._top_bar_surf.fill(p['fill'])
        
        surf.blit(self._top_bar_surf, (0, 0))
        pygame.draw.line(surf, p['dim'], (0, 70), (Config.WIDTH, 70), 2)
        
        for i, b in enumerate(self.tab_btns): b.draw(surf, (self.focus_area == "TOP" and self.focus_idx == i), p)
        
        if not self.loading:
            for i, b in enumerate(self.act_btns): b.draw(surf, (self.focus_area == "BOTTOM" and self.focus_idx == i), p)
        else:
            self._draw_loading_overlay(surf, p)

        self.log.draw(surf, p)
        if self.graph_viewer.active: self.graph_viewer.draw(surf, p)
        if self.viewer.active: self.viewer.draw(surf, p)
        if self.form_screen.active: self.form_screen.draw(surf, p)

    def _draw_loading_overlay(self, surf, p):
        """
        Draws the progress overlay while asynchronous queries are running.
        
        Args:
            surf (pygame.Surface): The target surface.
            p (dict): The active color palette dictionary.
        """
        if self._overlay_surf is None:
            self._overlay_surf = pygame.Surface((Config.WIDTH, Config.HEIGHT))
            self._overlay_surf.set_alpha(180)
            self._overlay_surf.fill(p['bg'])
            
        surf.blit(self._overlay_surf, (0, 0))
        cx, cy = Config.WIDTH // 2, Config.HEIGHT // 2
        br = pygame.Rect(cx - 250, cy - 75, 500, 150)
        
        Graphics.draw_chamfered_rect(surf, br, p['fill'], 0)
        Graphics.draw_chamfered_rect(surf, br, p['accent'], 2)
        
        t = Assets.FONTS["BIG"].render(f"QUERYING // {self.load_txt}", True, p['text'])
        surf.blit(t, (br.x + 30, br.y + 30))
        
        pygame.draw.rect(surf, (10, 15, 20), (br.x + 30, br.y + 90, 440, 20))
        pygame.draw.rect(surf, p['accent'], (br.x + 30, br.y + 90, int(440 * self.vis_load_prog), 20))
        
        pc = Assets.FONTS["SUB"].render(f"{int(self.vis_load_prog * 100)}%", True, p['accent'])
        surf.blit(pc, (br.right - 60, br.y + 65))

class App:
    """The core application class handling Pygame initialization and the main execution loop."""
    
    def __init__(self) -> None:
        """Initializes Pygame, loads assets, and prepares the main window."""
        pygame.init()
        Assets.load_fonts()
        self.screen = pygame.display.set_mode((Config.WIDTH, Config.HEIGHT), vsync=1)
        pygame.display.set_caption("ESPORTS DB // TERMINAL")
        self.clock = pygame.time.Clock()
        self.pidx = 0
        
        self.layout = LayoutManager()
        self.bg_hexes = [FloatingHex(Config.PALETTES[0]) for _ in range(30)]
        
        try:
            pygame.mixer.music.load("assets/Game Time! · Planarcadia Battle Theme - Honkai_ Star Rail 4.0 OST.mp3")
            pygame.mixer.music.play(-1)
        except Exception:
            pass

    def toggle_theme(self) -> None:
        """Cycles through the available visual color themes."""
        self.pidx = (self.pidx + 1) % len(Config.PALETTES)
        Graphics.clear_cache()
        for h in self.bg_hexes: h.reset(Config.PALETTES[self.pidx])

    def run(self) -> None:
        """Executes the main application loop."""
        while True:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                self.layout.handle_input(e, self)
            
            for h in self.bg_hexes: h.update()
            
            self.layout.update()
            
            p = Config.PALETTES[self.pidx]
            self.screen.fill(p['bg'])
            self.screen.blit(Graphics.get_dot_grid(p['dots']), (0,0))
            for h in self.bg_hexes: h.draw(self.screen)
            
            self.layout.draw(self.screen, p)
            
            pygame.display.flip()
            self.clock.tick(Config.FPS)

if __name__ == "__main__":
    App().run()