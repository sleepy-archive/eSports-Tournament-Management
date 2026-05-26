import pygame
import random
import time
from typing import List, Dict, Any
from eSports_config import Config, Assets
from eSports_gfx import Graphics

class DataViewer:
    """Displays formatted table data returned from SQL."""
    def __init__(self) -> None:
        """Initializes the DataViewer component."""
        self.active: bool = False
        self.headers: List[str] = []
        self.data_rows: List[List[str]] = []
        self.prompt_text: str = "DATABANK RESULTS"
        
        self.scroll_y: float = 0.0
        self.tgt_scroll: float = 0.0
        
        self.overlay = pygame.Surface((Config.WIDTH, Config.HEIGHT))
        self.overlay.set_alpha(220)
        self.overlay.fill((5, 5, 8))
        
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.action_btn_rect = pygame.Rect(0, 0, 0, 0)
        self.recalc_layout()

    def recalc_layout(self) -> None:
        """Recalculates the layout dimensions based on the current window size."""
        cx, cy = Config.WIDTH // 2, Config.HEIGHT // 2
        self.rect = pygame.Rect(cx - 400, cy - 250, 800, 500)
        self.action_btn_rect = pygame.Rect(self.rect.right - 220, self.rect.bottom - 60, 200, 40)

    def open(self, title: str, headers: List[str], data: List[List[str]]) -> None:
        """
        Opens the viewer with the specified tabular data.

        Args:
            title (str): The title of the data view.
            headers (List[str]): The column headers.
            data (List[List[str]]): The rows of data to display.
        """
        self.active = True
        self.prompt_text = title
        self.headers = headers
        self.data_rows = data
        self.tgt_scroll = 0
        self.scroll_y = 0

    def update(self) -> None:
        """Updates the internal state and scrolling physics of the viewer."""
        self.scroll_y += (self.tgt_scroll - self.scroll_y) * 0.2
        if self.active:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]: self.tgt_scroll = min(0, self.tgt_scroll + 10)
            elif keys[pygame.K_DOWN]: 
                max_s = -max(0, len(self.data_rows) * 35 - 324)
                self.tgt_scroll = max(max_s, self.tgt_scroll - 10)

    def handle(self, e: pygame.event.Event) -> None:
        """
        Processes input events for the viewer.

        Args:
            e (pygame.event.Event): The Pygame event to process.
        """
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE or e.key == pygame.K_RETURN:
                self.active = False
        if e.type == pygame.MOUSEBUTTONDOWN:
            if e.button == 4: self.tgt_scroll = min(0, self.tgt_scroll + 40)
            elif e.button == 5: 
                max_s = -max(0, len(self.data_rows) * 35 - 324)
                self.tgt_scroll = max(max_s, self.tgt_scroll - 40)
            elif e.button == 1:
                if self.action_btn_rect.collidepoint(e.pos): self.active = False

    def draw(self, surf: pygame.Surface, p: Any) -> None:
        """
        Renders the data viewer to the target surface.

        Args:
            surf (pygame.Surface): The target surface.
            p (Any): The current color palette.
        """
        surf.blit(self.overlay, (0, 0))
        Graphics.draw_chamfered_rect(surf, self.rect, p['fill'], 0)
        Graphics.draw_chamfered_rect(surf, self.rect, p['accent'], 2)
        
        t = Assets.FONTS["CORE"].render(self.prompt_text, True, p['accent'])
        surf.blit(t, (self.rect.x + 30, self.rect.y + 20)) 

        lr = pygame.Rect(self.rect.x + 20, self.rect.y + 60, self.rect.w - 40, 360)
        pygame.draw.rect(surf, (10, 10, 12), lr)
        pygame.draw.rect(surf, p['dim'], lr, 1)
        
        num_cols = max(1, len(self.headers))
        col_w = lr.w / num_cols
        
        header_y = lr.y
        pygame.draw.rect(surf, p['fill'], (lr.x, header_y, lr.w, 35))
        pygame.draw.line(surf, p['dim'], (lr.x, header_y + 35), (lr.x + lr.w, header_y + 35), 2)
        for c_idx, h in enumerate(self.headers):
            hx = lr.x + (c_idx * col_w)
            h_trunc = Graphics.truncate_text(h, Assets.FONTS["SUB"], col_w - 20)
            ht = Assets.FONTS["SUB"].render(h_trunc, True, p['accent'])
            surf.blit(ht, (hx + 10, header_y + 8))
            if c_idx > 0:
                pygame.draw.line(surf, p['dim'], (hx, header_y), (hx, header_y + 35), 1)
                
        clip_rect = pygame.Rect(lr.x, lr.y + 36, lr.w, lr.h - 36)
        surf.set_clip(clip_rect)
        
        sy = clip_rect.y + self.scroll_y
        start_index = max(0, int((-self.scroll_y) // 35))
        end_index = min(len(self.data_rows), start_index + (clip_rect.h // 35) + 2)

        for i in range(start_index, end_index):
            fy = sy + i * 35
            row_data = self.data_rows[i]
            
            if i % 2 == 0:
                pygame.draw.rect(surf, (15, 15, 18), (lr.x, fy, lr.w, 35))
                
            for c_idx, cell in enumerate(row_data):
                cx = lr.x + (c_idx * col_w)
                cell_trunc = Graphics.truncate_text(str(cell), Assets.FONTS["SUB"], col_w - 20)
                ct = Assets.FONTS["SUB"].render(cell_trunc, True, p['text'])
                surf.blit(ct, (cx + 10, fy + 8))
                if c_idx > 0:
                    pygame.draw.line(surf, (30, 30, 35), (cx, fy), (cx, fy + 35), 1)
            pygame.draw.line(surf, (30, 30, 35), (lr.x, fy + 35), (lr.x + lr.w, fy + 35), 1)
            
        surf.set_clip(None)

        Graphics.draw_chamfered_rect(surf, self.action_btn_rect, p['fill'], 0)
        Graphics.draw_chamfered_rect(surf, self.action_btn_rect, p['accent'], 2)
        a_t = Assets.FONTS["MAIN"].render("CLOSE VIEWER", True, p['accent'])
        surf.blit(a_t, a_t.get_rect(center=self.action_btn_rect.center))

class GraphViewer:
    """Renders numerical datasets onto a smooth Catmull-Rom spline graph using Pygame."""
    def __init__(self) -> None:
        """Initializes the GraphViewer component."""
        self.active: bool = False
        self.datasets: List[Dict[str, Any]] = []
        self.prompt_text: str = "PERFORMANCE TRENDS"
        
        self.overlay = pygame.Surface((Config.WIDTH, Config.HEIGHT))
        self.overlay.set_alpha(220)
        self.overlay.fill((5, 5, 8))
        
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.action_btn_rect = pygame.Rect(0, 0, 0, 0)
        self.recalc_layout()

    def recalc_layout(self) -> None:
        """Recalculates the layout dimensions based on the current window size."""
        cx, cy = Config.WIDTH // 2, Config.HEIGHT // 2
        self.rect = pygame.Rect(cx - 450, cy - 250, 900, 500)
        self.action_btn_rect = pygame.Rect(self.rect.right - 220, self.rect.bottom - 60, 200, 40)

    def open(self, title: str, data: List[Dict[str, Any]]) -> None:
        """
        Opens the graph viewer with the provided dataset.

        Args:
            title (str): The title of the graph.
            data (List[Dict[str, Any]]): A list of datasets to plot. 
                                         Each dict should have 'name' and 'ratings'.
        """
        self.active = True
        self.prompt_text = title
        self.datasets = data

    def update(self) -> None:
        """Updates the internal state and animations of the graph viewer."""
        pass

    def handle(self, e: pygame.event.Event) -> None:
        """
        Processes input events for the graph viewer.

        Args:
            e (pygame.event.Event): The Pygame event to process.
        """
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE or e.key == pygame.K_RETURN:
                self.active = False
        if e.type == pygame.MOUSEBUTTONDOWN:
            if e.button == 1 and self.action_btn_rect.collidepoint(e.pos): 
                self.active = False

    def draw(self, surf: pygame.Surface, p: Any) -> None:
        """
        Renders the graph viewer to the target surface.

        Args:
            surf (pygame.Surface): The target surface.
            p (Any): The current color palette.
        """
        surf.blit(self.overlay, (0, 0))
        Graphics.draw_chamfered_rect(surf, self.rect, p['fill'], 0)
        Graphics.draw_chamfered_rect(surf, self.rect, p['accent'], 2)
        
        t = Assets.FONTS["CORE"].render(self.prompt_text, True, p['accent'])
        surf.blit(t, (self.rect.x + 30, self.rect.y + 20)) 

        # Plot Background Area
        gx, gy = self.rect.x + 40, self.rect.y + 80
        gw, gh = self.rect.width - 230, self.rect.height - 160
        pygame.draw.rect(surf, (15, 15, 20), (gx, gy, gw, gh))
        pygame.draw.rect(surf, p['dim'], (gx, gy, gw, gh), 1)
        
        for i in range(1, 5):
            y_line = gy + i * (gh / 5)
            pygame.draw.line(surf, (30, 30, 40), (gx, y_line), (gx + gw, y_line))
            
        if self.datasets:
            # Custom bluer tones for better readability without clashing
            line_colors = [(0, 255, 255), (50, 150, 250), (120, 200, 255), (0, 100, 200), (180, 230, 255)]

            all_ratings = [rating for dataset in self.datasets for rating in dataset.get('ratings', [])]
            if not all_ratings: return
            
            min_val, max_val = min(all_ratings), max(all_ratings)
            val_range = max(0.1, max_val - min_val) 
            
            legend_x, legend_y = gx + gw + 30, gy

            # Draw legend with colors
            for i, dataset in enumerate(self.datasets):
                color = line_colors[i % len(line_colors)]
                player_name = dataset.get('name', 'Unknown')
                pygame.draw.rect(surf, color, (legend_x, legend_y + i * 30, 15, 15))
                name_surf = Assets.FONTS["SUB"].render(player_name, True, p['text'])
                surf.blit(name_surf, (legend_x + 25, legend_y + i * 30))

            # Draw each player's data
            for i, dataset in enumerate(self.datasets):
                ratings = dataset.get('ratings', [])
                if not ratings: continue

                color = line_colors[i % len(line_colors)]
                screen_points = []
                num_points = len(ratings)
                for pt_idx, val in enumerate(ratings):
                    px = gx + (pt_idx / max(1, num_points - 1)) * gw
                    py = gy + gh - ((val - min_val) / val_range) * gh
                    screen_points.append((px, py))
                    
                # Interpolate for smoothness - increased segments for quality
                smooth_pts = Graphics.get_spline_points(screen_points, 30)
                if len(smooth_pts) > 1:
                    # Draw a slightly thicker line by drawing twice
                    pygame.draw.aalines(surf, color, False, smooth_pts)
                    offset_pts = [(pt[0], pt[1] + 1) for pt in smooth_pts]
                    pygame.draw.aalines(surf, color, False, offset_pts)

                # Draw individual dots and value labels
                for pt_idx, (px, py) in enumerate(screen_points):
                    pygame.draw.circle(surf, color, (int(px), int(py)), 5)
                    pygame.draw.circle(surf, p['bg'], (int(px), int(py)), 3)
                    
                    # Only draw labels for first and last points to avoid clutter
                    if pt_idx == 0 or pt_idx == len(screen_points) - 1:
                        val = ratings[pt_idx]
                        lbl = Assets.FONTS["TINY"].render(f"{val:.1f}", True, p['text'])
                        surf.blit(lbl, (px - lbl.get_width() // 2, py - 20))

        Graphics.draw_chamfered_rect(surf, self.action_btn_rect, p['fill'], 0)
        Graphics.draw_chamfered_rect(surf, self.action_btn_rect, p['accent'], 2)
        a_t = Assets.FONTS["MAIN"].render("CLOSE GRAPH", True, p['accent'])
        surf.blit(a_t, a_t.get_rect(center=self.action_btn_rect.center))


class FormScreen:
    """A data entry form for executing CRUD operations with visual feedback."""
    def __init__(self) -> None:
        """Initializes the FormScreen component."""
        self.active: bool = False
        self.title: str = ""
        self.fields: List[str] = []
        self.values: List[str] = []
        self.active_idx: int = 0
        self.submit_cb: Any = None
        
        self.overlay = pygame.Surface((Config.WIDTH, Config.HEIGHT))
        self.overlay.set_alpha(220)
        self.overlay.fill((5, 5, 8))
        
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.action_btn_rect = pygame.Rect(0, 0, 0, 0)
        self.recalc_layout()

    def recalc_layout(self) -> None:
        """Recalculates the layout dimensions."""
        cx, cy = Config.WIDTH // 2, Config.HEIGHT // 2
        self.rect = pygame.Rect(cx - 250, cy - 200, 500, 400)
        self.action_btn_rect = pygame.Rect(self.rect.right - 180, self.rect.bottom - 60, 160, 40)

    def open(self, title: str, fields: List[str], submit_cb: Any) -> None:
        """Opens the data entry form."""
        self.active = True
        self.title = title
        self.fields = fields
        self.values = ["" for _ in fields]
        self.active_idx = 0
        self.submit_cb = submit_cb

    def update(self) -> None:
        """Updates internal state; acts as a placeholder for future form animations."""
        pass

    def handle(self, e: pygame.event.Event) -> None:
        """Processes keyboard input and field selection."""
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE:
                self.active = False
            elif e.key == pygame.K_TAB or e.key == pygame.K_DOWN:
                self.active_idx = (self.active_idx + 1) % len(self.fields)
            elif e.key == pygame.K_UP:
                self.active_idx = (self.active_idx - 1) % len(self.fields)
            elif e.key == pygame.K_RETURN:
                self.active = False
                if self.submit_cb:
                    self.submit_cb(self.title, self.values)
            elif e.key == pygame.K_BACKSPACE:
                self.values[self.active_idx] = self.values[self.active_idx][:-1]
            else:
                if e.unicode.isprintable() and len(self.values[self.active_idx]) < 30:
                    self.values[self.active_idx] += e.unicode
                    
        elif e.type == pygame.MOUSEBUTTONDOWN:
            if e.button == 1 and self.action_btn_rect.collidepoint(e.pos):
                self.active = False
                if self.submit_cb:
                    self.submit_cb(self.title, self.values)
            # Field selection via mouse
            start_y = self.rect.y + 80
            for i in range(len(self.fields)):
                field_rect = pygame.Rect(self.rect.x + 40, start_y + i * 70, self.rect.w - 80, 40)
                if field_rect.collidepoint(e.pos): self.active_idx = i

    def draw(self, surf: pygame.Surface, palette: Any) -> None:
        """Renders the form fields and cursor."""
        surf.blit(self.overlay, (0, 0))
        Graphics.draw_chamfered_rect(surf, self.rect, palette['fill'], 0)
        Graphics.draw_chamfered_rect(surf, self.rect, palette['accent'], 2)
        
        title_surf = Assets.FONTS["CORE"].render(self.title, True, palette['accent'])
        surf.blit(title_surf, (self.rect.x + 30, self.rect.y + 20))
        
        start_y = self.rect.y + 80
        for i, (f, v) in enumerate(zip(self.fields, self.values)):
            lbl = Assets.FONTS["SUB"].render(f, True, palette['dim'])
            surf.blit(lbl, (self.rect.x + 40, start_y + i * 70 - 20))
            
            field_rect = pygame.Rect(self.rect.x + 40, start_y + i * 70, self.rect.w - 80, 40)
            col = palette['accent'] if i == self.active_idx else palette['dim']
            Graphics.draw_chamfered_rect(surf, field_rect, (10, 10, 15), 0)
            Graphics.draw_chamfered_rect(surf, field_rect, col, 2)
            
            txt = v + ("_" if i == self.active_idx and time.time() % 1 > 0.5 else "")
            value_text = Assets.FONTS["MAIN"].render(txt, True, palette['text'])
            surf.blit(value_text, (field_rect.x + 10, field_rect.y + 10))

        Graphics.draw_chamfered_rect(surf, self.action_btn_rect, palette['fill'], 0)
        Graphics.draw_chamfered_rect(surf, self.action_btn_rect, palette['accent'], 2)
        btn_text = Assets.FONTS["MAIN"].render("SUBMIT", True, palette['accent'])
        surf.blit(btn_text, btn_text.get_rect(center=self.action_btn_rect.center))