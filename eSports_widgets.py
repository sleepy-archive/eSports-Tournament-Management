import pygame
import math
import random
import time
import datetime
from typing import Dict, List, Tuple, Optional, Any

from eSports_config import Config, Assets
from eSports_gfx import Graphics

class FloatingHex:
    """
    Represents a decorative hexagon floating in the background.
    
    This widget manages its own position, rotation, and lifecycle (resetting
    when it moves off-screen).
    """

    def __init__(self, palette: Dict[str, Any]) -> None:
        """
        Initialize the floating hexagon.

        Args:
            palette (Dict[str, Any]): The color palette configuration.
        """
        self.x: float = 0
        self.y: float = 0
        self.size: int = 0
        self.speed: float = 0.0
        self.color: Tuple[int, int, int] = (0, 0, 0)
        self.rotation: float = 0.0
        
        self.reset(palette)
        # Randomize start Y to distribute hexes across the screen initially
        self.y = random.randint(0, Config.HEIGHT)

    def reset(self, palette: Dict[str, Any]) -> None:
        """
        Reset the hexagon's properties for a new lifecycle.

        Args:
            palette (Dict[str, Any]): The color palette to derive colors from.
        """
        self.size = random.randint(20, 50)
        self.x = random.randint(0, Config.WIDTH)
        # Start below the screen to float up
        self.y = Config.HEIGHT + 50
        self.speed = random.uniform(0.5, 1.5)
        
        # Randomly choose between the palette's dim color or a fixed dark slate
        # to add visual variety.
        dim_col = palette.get('dim', (30, 40, 50))
        self.color = random.choice([dim_col, (30, 40, 50)])
        self.rotation = random.uniform(0, 360)

    def update(self) -> None:
        """
        Update position and rotation. Resets if the hex moves off-screen.
        """
        self.y -= self.speed
        self.rotation += 0.2
        
        if self.y < -50: 
            self.size = random.randint(20, 50)
            self.x = random.randint(0, Config.WIDTH)
            self.speed = random.uniform(0.5, 1.5)
            self.y = Config.HEIGHT + 50

    def draw(self, surf: pygame.Surface) -> None:
        """
        Render the hexagon to the target surface.

        Args:
            surf (pygame.Surface): The surface to draw on.
        """
        Graphics.draw_hex_ring(
            surf, self.x, self.y, self.size, self.color, self.rotation, 1
        )


class EsportsCoreLog:
    """
    A scrollable log widget displaying system events and important messages.
    
    Features:
    - Important message banner (top).
    - Scrollable history (bottom).
    - Automatic text wrapping.
    - Performance optimizations (surface caching, view culling).
    """

    def __init__(self) -> None:
        """Initialize the log widget."""
        self.rect: pygame.Rect = pygame.Rect(0, 0, 0, 0)
        self.imp_rect: pygame.Rect = pygame.Rect(0, 0, 0, 0)
        self.std_rect: pygame.Rect = pygame.Rect(0, 0, 0, 0)
        
        self._cached_glass: Optional[pygame.Surface] = None
        
        self.imp_msg: str = "TOURNAMENT UPDATES"
        self.std_logs: List[str] = []
        
        self.is_hacked: bool = False
        self.hack_msg: str = ""
        
        # Scrolling state
        self.scroll_std: float = 0.0
        self.tgt_std: float = 0.0
        self.line_height: int = 14
        
        self.recalc_layout()
        
        self.add_log_direct("DATABANK_INIT_OK")
        self.add_log_direct("INTERASTRAL NETWORK CONNECTED")

    def recalc_layout(self) -> None:
        """
        Recalculate layout coordinates and regenerate cached surfaces.
        
        Should be called when screen resolution changes.
        """
        self.rect = pygame.Rect(Config.WIDTH - 320, 90, 300, 265)
        self.imp_rect = pygame.Rect(self.rect.x + 10, self.rect.y + 10, self.rect.width - 20, 40)
        self.std_rect = pygame.Rect(self.rect.x + 10, self.rect.y + 80, self.rect.width - 20, 150)
        
        self._cached_glass = pygame.Surface(self.rect.size, pygame.SRCALPHA)

    def set_important(self, text: str) -> None:
        """
        Set the high-priority message displayed at the top of the log.

        Args:
            text (str): The message to display.
        """
        self.imp_msg = text
        self.add_log_direct(f">> {text}")

    def add_log_direct(self, text: str) -> None:
        """
        Add a standard log entry with timestamp and wrapping.

        Args:
            text (str): The log message.
        """
        t_str = datetime.datetime.now().strftime("%H:%M:%S")
        prefix_first = f"[{t_str}] "
        prefix_indent = " " * len(prefix_first)
        
        # Calculate available width by subtracting the prefix render width
        prefix_width = Assets.FONTS["TINY"].size(prefix_first)[0]
        available_width = self.std_rect.width - 10 - prefix_width

        lines = Graphics.wrap_text(text, Assets.FONTS["TINY"], available_width)
        
        for i, line in enumerate(lines):
            prefix = prefix_first if i == 0 else prefix_indent
            self.std_logs.append(f"{prefix}{line}")
        
        # Prune old logs to prevent memory bloat
        if len(self.std_logs) > 500: 
            self.std_logs = self.std_logs[-500:]
            
        # Auto-scroll to bottom
        self.tgt_std = -float('inf')

    def handle_input(self, event: pygame.event.Event) -> None:
        """
        Handle mouse interaction (scrolling).

        Args:
            event (pygame.event.Event): The input event.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            if self.std_rect.collidepoint(mx, my):
                visible_h = self.std_rect.height - 10
                total_h = len(self.std_logs) * self.line_height
                
                scroll_step = 40
                
                if event.button == 4: # Scroll Up
                    self.tgt_std = min(0, self.tgt_std + scroll_step)
                elif event.button == 5 and total_h > visible_h: # Scroll Down
                    min_scroll = -(total_h - visible_h)
                    self.tgt_std = max(min_scroll, self.tgt_std - scroll_step)

    def update(self) -> None:
        """Update scrolling physics."""
        visible_h = self.std_rect.height - 10
        total_h = len(self.std_logs) * self.line_height
        
        if total_h < visible_h:
            self.tgt_std = 0
        else:
            min_scroll = -(total_h - visible_h)
            if self.tgt_std < min_scroll: 
                self.tgt_std = min_scroll
            if self.tgt_std > 0: 
                self.tgt_std = 0
            
        # Smooth interpolation (Lerp)
        self.scroll_std += (self.tgt_std - self.scroll_std) * 0.2

    def draw(self, surf: pygame.Surface, palette: Dict[str, Any]) -> None:
        """
        Render the log widget.

        Args:
            surf (pygame.Surface): Target surface.
            palette (Dict[str, Any]): Color palette.
        """
        # 1. Draw Background
        if self._cached_glass is None:
             self._cached_glass = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        
        fill = palette['fill']
        self._cached_glass.fill((fill[0], fill[1], fill[2], 90))
        surf.blit(self._cached_glass, self.rect.topleft)
        
        Graphics.draw_chamfered_rect(surf, self.rect, palette['accent'], 2)

        # 2. Draw Important Message Box
        if self.is_hacked:
            box_fill = (60, 10, 15)
            box_accent = (255, 40, 60)
            display_msg = self.hack_msg
        else:
            box_fill = palette['fill']
            box_accent = palette['accent']
            display_msg = self.imp_msg

        Graphics.draw_chamfered_rect(surf, self.imp_rect, box_fill, 0)
        Graphics.draw_chamfered_rect(surf, self.imp_rect, box_accent, 1)
        
        trunc_msg = Graphics.truncate_text(display_msg, Assets.FONTS["SUB"], self.imp_rect.width - 20)
        t = Assets.FONTS["SUB"].render(trunc_msg, True, box_accent)
        surf.blit(t, t.get_rect(center=self.imp_rect.center))

        # 3. Draw Header
        head = Assets.FONTS["TINY"].render("MATCH_LOG // HISTORY", True, palette['dim'])
        surf.blit(head, (self.std_rect.x, self.std_rect.y - 15))
        
        # 4. Draw Logs (Clipped)
        surf.set_clip(self.std_rect)
        
        start_y = self.std_rect.y + 5 + self.scroll_std
        
        # Optimization: Calculate mathematically which logs are currently visible based on scroll offset.
        first_idx = int((self.std_rect.y - start_y - self.line_height) / self.line_height)
        first_idx = max(0, first_idx)
        
        last_idx = int((self.std_rect.bottom - start_y) / self.line_height)
        last_idx = min(len(self.std_logs), last_idx + 1)
        
        for i in range(first_idx, last_idx):
            log = self.std_logs[i]
            ly = start_y + (i * self.line_height)
            
            # Highlight recent logs
            alpha = 255 if i > len(self.std_logs) - 5 else 180
            
            t = Assets.FONTS["TINY"].render(log, True, palette['text'])
            t.set_alpha(alpha)
            surf.blit(t, (self.std_rect.x + 5, ly))
            
        surf.set_clip(None)

class CentralCore:
    """
    The central UI element displaying status, descriptions, and animations.
    
    Handles the "breathing" animation and text transitions.
    """

    def __init__(self) -> None:
        """Initialize the central core widget."""
        self.rot_a: float = 0.0
        self.rot_b: float = 0.0
        
        self.tgt_txt: str = "TOURNAMENT UPDATES"
        self.tgt_desc: str = "WAITING FOR INPUT"
        self.disp_txt: str = self.tgt_txt
        self.disp_desc: str = self.tgt_desc
        
        # Animation states
        self.alpha: int = 255
        self.off_x: float = 0.0
        self.state: str = "IDLE" # IDLE, OUT, IN
        
        self.arrow_l: int = 0
        self.arrow_r: int = 0
        self.bob_phase: float = 0.0
        
        self.desc_map: Dict[str, str] = {
            "AETHERIUM WARS": "TOURNAMENT DASHBOARD // STAGES & DATES",
            "LIVE BROADCASTS": "INTERASTRAL FEEDS // ONGOING MATCHES",
            "ACTIVE ROSTERS": "COMPETITOR ASSIGNMENTS // TEAM DB",
            "GLOBAL STANDINGS": "LEADERBOARD // POINTS & RATING",
            "ELITE TIER": "TOP PERFORMERS // WARP TIER",
            "FULL SCHEDULE": "MATCH CALENDAR // ALL BRACKETS",
            "MATCH LOGS": "AUDIT LOG // STATUS CHANGES",
            "DISCONNECT": "TERMINATE SESSION // OFFLINE",
            "TOGGLE THEME": "VISUAL CONFIG // OPTICS TOGGLE",
            "COMBAT METRICS": "PERFORMANCE TRENDS // METRICS",
            "OVERVIEW": "AETHERIUM WARS // SUMMARY",
            "DATABANK OPS": "ROSTER OPS // DATABANK EDIT",
            "REGISTER PLAYER": "REGISTER // NEW COMPETITOR",
            "UPDATE MATCH": "UPDATE // MATCH STATUS",
            "ERASE RECORD": "ERASE // GAME STAT RECORD",
            "ROSTERS & TEAMS": "DATABANK // COMBATANTS",
            "MATCH TRACKER": "LIVE FEEDS // SCHEDULING",
            "SETTINGS": "SYSTEM CONFIG // ASTRAL EXPRESS"
        }

    def set_status(self, txt: str, custom_desc: Optional[str] = None) -> None:
        """
        Trigger a status change animation.

        Args:
            txt (str): The main status text.
            custom_desc (Optional[str]): Optional custom description. 
                                         If None, looks up in desc_map.
        """
        desc = custom_desc if custom_desc else self.desc_map.get(txt, "SELECTED // ACTIVE")
        
        if txt != self.tgt_txt or custom_desc:
            self.tgt_txt, self.tgt_desc = txt, desc
            self.state = "OUT"

    def update(self) -> None:
        """Update animations and transition state machine."""
        self.rot_a += 0.5
        self.rot_b -= 0.3
        self.bob_phase += 0.1
        
        if self.arrow_l > 0: self.arrow_l -= 1
        if self.arrow_r > 0: self.arrow_r -= 1

        # Text Transition State Machine
        if self.state == "OUT":
            self.off_x += (-100 - self.off_x) * 0.1
            self.alpha = max(0, self.alpha - 20)
            
            if self.alpha <= 0:
                self.disp_txt, self.disp_desc = self.tgt_txt, self.tgt_desc
                self.off_x = 100
                self.state = "IN"
                
        elif self.state == "IN":
            self.off_x += (0 - self.off_x) * 0.1
            self.alpha = min(255, self.alpha + 20)
            
            if self.alpha >= 255 and abs(self.off_x) < 1:
                self.state = "IDLE"

    def draw(self, surf: pygame.Surface, cx: int, cy: int, palette: Dict[str, Any]) -> None:
        """
        Render the central core.

        Args:
            surf (pygame.Surface): Target surface.
            cx (int): Center X coordinate.
            cy (int): Center Y coordinate.
            palette (Dict[str, Any]): Color palette.
        """
        # Draw rotating rings
        Graphics.draw_hex_ring(surf, cx, cy, 160, palette['dim'], self.rot_a, 4)
        Graphics.draw_hex_ring(surf, cx, cy, 220, palette['dim'], self.rot_b, 3)
        
        # Draw Side Arrows (Brackets)
        off = 260
        bob_offset = math.sin(self.bob_phase) * 5
        bracket_height = 60
        
        # Left Bracket
        col_l = palette['accent'] if self.arrow_l > 0 else palette['dim']
        left_x = cx - off + bob_offset
        pygame.draw.lines(surf, col_l, False, [(left_x, cy-bracket_height), (left_x-30, cy), (left_x, cy+bracket_height)], 4)
        
        # Right Bracket
        col_r = palette['accent'] if self.arrow_r > 0 else palette['dim']
        right_x = cx + off - bob_offset
        pygame.draw.lines(surf, col_r, False, [(right_x, cy-bracket_height), (right_x+30, cy), (right_x, cy+bracket_height)], 4)

        # Draw Clock
        t_str = datetime.datetime.now().strftime("%H:%M:%S")
        clock_text = Assets.FONTS["CLOCK"].render(f"INTERASTRAL_TIME // {t_str}", True, palette['dim'])
        surf.blit(clock_text, clock_text.get_rect(center=(cx, cy-70)))

        # Draw Status Text
        if self.alpha > 5:
            main_text = Assets.FONTS["CORE"].render(self.disp_txt, True, palette['text'])
            main_text.set_alpha(self.alpha)
            surf.blit(main_text, main_text.get_rect(center=(cx + self.off_x, cy - 10)))
            
            desc_text = Assets.FONTS["SUB"].render(self.disp_desc, True, palette['accent'])
            desc_text.set_alpha(self.alpha)
            surf.blit(desc_text, desc_text.get_rect(center=(cx + self.off_x, cy + 30)))

class FloatyButton:
    """
    A UI button that floats/bobs gently.
    
    Optimized to cache text rendering to minimize CPU usage.
    """

    def __init__(self, x: int, y: int, w: int, h: int, text: str) -> None:
        """
        Initialize the button.

        Args:
            x, y, w, h (int): Dimensions and position.
            text (str): Button label.
        """
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.base_y: float = float(y)
        self.cur_y: float = float(y)
        self.offset = random.uniform(0, 10)
        
        self._cached_text_surf: Optional[pygame.Surface] = None
        self._cached_text_sel_surf: Optional[pygame.Surface] = None
        self._last_palette_name: Optional[str] = None

    def update(self, selected: bool) -> None:
        """
        Update the vertical position (bobbing animation).

        Args:
            selected (bool): Whether the button is currently focused.
        """
        target = self.base_y + (-8 if selected else 0) + (math.sin(time.time()*2 + self.offset)*2)
        
        self.cur_y += (target - self.cur_y) * 0.05
        self.rect.y = int(self.cur_y)

    def draw(self, surf: pygame.Surface, selected: bool, p: Dict[str, Any]) -> None:
        """
        Render the button.

        Args:
            surf (pygame.Surface): Target surface.
            selected (bool): Focus state.
            p (Dict[str, Any]): Color palette.
        """
        # Regenerate cached text surfaces if the palette changes.
        if self._cached_text_surf is None or self._last_palette_name != p.get('name', ''):
            self._last_palette_name = p.get('name', '')
            self._cached_text_surf = Assets.FONTS["MAIN"].render(self.text, True, (150, 150, 150))
            self._cached_text_sel_surf = Assets.FONTS["MAIN"].render(self.text, True, p['text'])

        draw_rect = self.rect.copy()
        
        col = p['accent'] if selected else p['dim']
        
        Graphics.draw_chamfered_rect(surf, draw_rect, p['fill'], 0)
        Graphics.draw_chamfered_rect(surf, draw_rect, col, 3 if selected else 2)
        
        txt_surf = self._cached_text_sel_surf if selected else self._cached_text_surf
        if txt_surf:
            surf.blit(txt_surf, txt_surf.get_rect(center=self.rect.center))