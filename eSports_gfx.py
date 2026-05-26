import pygame
import math
from typing import List, Tuple, Union, Optional
from eSports_config import Config

class Graphics:
    """
    Static utility class for rendering custom UI elements and handling graphical operations.
    
    This class provides methods for drawing geometric shapes (chamfered rectangles, hexagons),
    generating background grids, and handling text layout (wrapping). It utilizes caching
    to optimize rendering performance for static elements like the background grid.
    """

    # Cache for the background dot grid to prevent expensive redraws.
    _grid_cache: Optional[Tuple[pygame.Surface, Tuple[int, int, int]]] = None

    @staticmethod
    def get_dot_grid(color: Tuple[int, int, int]) -> pygame.Surface:
        """
        Retrieve or generate the background dot grid surface.

        This method employs a caching strategy. If a grid with the specified color
        has already been generated, it returns the cached Surface. Otherwise, it
        creates a new Surface, draws the grid, and updates the cache.

        Args:
            color (Tuple[int, int, int]): The RGB color for the grid dots.

        Returns:
            pygame.Surface: A surface containing the rendered dot grid.
        """
        if Graphics._grid_cache is not None:
            cached_surface, cached_color = Graphics._grid_cache
            if cached_color == color:
                return cached_surface

        surface = pygame.Surface((Config.WIDTH, Config.HEIGHT))
        surface.set_colorkey((0, 0, 0))
        surface.fill((0, 0, 0))

        # Draw dots in a grid pattern with 30px spacing.
        for x in range(0, Config.WIDTH, 30):
            for y in range(0, Config.HEIGHT, 30):
                pygame.draw.circle(surface, color, (x, y), 1)

        Graphics._grid_cache = (surface, color)
        return surface

    @staticmethod
    def clear_cache() -> None:
        """
        Invalidate the graphics cache.

        This should be called when global display settings change (e.g., resolution)
        to force regeneration of cached assets.
        """
        Graphics._grid_cache = None

    @staticmethod
    def draw_chamfered_rect(
        surf: pygame.Surface, 
        rect: Union[pygame.Rect, Tuple[int, int, int, int]], 
        color: Tuple[int, int, int], 
        width: int = 0, 
        cut: int = 10
    ) -> None:
        """
        Draw a rectangle with chamfered (cut) corners.

        This creates a "sci-fi" or "tech" aesthetic compared to standard rounded rectangles.
        It also renders a subtle drop shadow if the shape is filled (width=0).

        Args:
            surf (pygame.Surface): The target surface to draw on.
            rect (Union[pygame.Rect, Tuple]): The bounding rectangle (x, y, w, h).
            color (Tuple[int, int, int]): The RGB color of the shape.
            width (int, optional): Line width. 0 fills the shape. Defaults to 0.
            cut (int, optional): The size of the corner cut in pixels. Defaults to 10.
        """
        # Unpack rectangle coordinates. Works for both tuples and pygame.Rect objects.
        if isinstance(rect, pygame.Rect):
            x, y, w, h = rect.x, rect.y, rect.width, rect.height
        else:
            x, y, w, h = rect

        # Calculate the 8 points of the chamfered polygon starting top-left, moving clockwise.
        points = [
            (x + cut, y),       # Top-Left (start of top edge)
            (x + w - cut, y),   # Top-Right (end of top edge)
            (x + w, y + cut),   # Top-Right (start of right edge)
            (x + w, y + h - cut), # Bottom-Right (end of right edge)
            (x + w - cut, y + h), # Bottom-Right (start of bottom edge)
            (x + cut, y + h),   # Bottom-Left (end of bottom edge)
            (x, y + h - cut),   # Bottom-Left (start of left edge)
            (x, y + cut)        # Top-Left (end of left edge)
        ]

        # Draw drop shadow for filled shapes.
        if width == 0:
            shadow_points = [(p[0] + 4, p[1] + 4) for p in points]
            pygame.draw.polygon(surf, (5, 5, 5), shadow_points)

        pygame.draw.polygon(surf, color, points, width)

    @staticmethod
    def draw_hex_ring(
        surf: pygame.Surface, 
        x: float, 
        y: float, 
        radius: float, 
        color: Tuple[int, int, int], 
        rotation: float, 
        width: int = 2
    ) -> None:
        """
        Draw a hexagon outline centered at (x, y).

        Args:
            surf (pygame.Surface): The target surface.
            x (float): Center X coordinate.
            y (float): Center Y coordinate.
            radius (float): Distance from center to vertex.
            color (Tuple[int, int, int]): RGB color.
            rotation (float): Rotation angle in degrees.
            width (int, optional): Line thickness. Defaults to 2.
        """
        points = []
        for i in range(6):
            ang_deg = 60 * i + rotation
            ang_rad = math.radians(ang_deg)
            
            px = x + radius * math.cos(ang_rad)
            py = y + radius * math.sin(ang_rad)
            points.append((px, py))

        pygame.draw.polygon(surf, color, points, width)

    @staticmethod
    def wrap_text(text: str, font: pygame.font.Font, max_width: int) -> List[str]:
        """
        Wrap text to fit within a specified width.

        Handles standard space-based word wrapping.

        Args:
            text (str): The input string.
            font (pygame.font.Font): The font used for size calculations.
            max_width (int): The maximum width in pixels allowed per line.

        Returns:
            List[str]: A list of strings, where each string is a line.
        """
        if not text:
            return []

        words = text.split(' ')
        lines = []
        current_line = []

        for word in words:
            test_line_words = current_line + [word]
            test_line_str = ' '.join(test_line_words)
            
            if font.size(test_line_str)[0] < max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                    current_line = [word]
                else:
                    # Edge case: The word itself is wider than max_width.
                    lines.append(word)
                    current_line = []

        if current_line:
            lines.append(' '.join(current_line))
            
        return lines

    @staticmethod
    def truncate_text(text: str, font: pygame.font.Font, max_width: float) -> str:
        """
        Truncate text with an ellipsis if it exceeds the maximum width.

        Args:
            text (str): The input string.
            font (pygame.font.Font): The font used for size calculations.
            max_width (float): The maximum width in pixels allowed.

        Returns:
            str: The original string if it fits, otherwise the truncated string ending with '...'.
        """
        if font.size(text)[0] <= max_width:
            return text
            
        ellipsis = "..."
        if font.size(ellipsis)[0] > max_width:
            return ""
            
        truncated = text
        while truncated and font.size(truncated + ellipsis)[0] > max_width:
            truncated = truncated[:-1]
            
        return truncated + ellipsis

    @staticmethod
    def get_spline_points(points: List[Tuple[float, float]], num_segments: int = 15) -> List[Tuple[float, float]]:
        """Generates a smooth Catmull-Rom spline through a list of points."""
        if len(points) < 3:
            return points
        
        # Duplicate start and end points for curve calculation
        pts = [points[0]] + points + [points[-1]]
        smooth_points = []
        
        for i in range(1, len(pts) - 2):
            p0, p1, p2, p3 = pts[i-1], pts[i], pts[i+1], pts[i+2]
            for t_step in range(num_segments):
                t = t_step / num_segments
                t2 = t * t
                t3 = t2 * t
                
                x = 0.5 * ((2 * p1[0]) + (-p0[0] + p2[0]) * t + (2 * p0[0] - 5 * p1[0] + 4 * p2[0] - p3[0]) * t2 + (-p0[0] + 3 * p1[0] - 3 * p2[0] + p3[0]) * t3)
                y = 0.5 * ((2 * p1[1]) + (-p0[1] + p2[1]) * t + (2 * p0[1] - 5 * p1[1] + 4 * p2[1] - p3[1]) * t2 + (-p0[1] + 3 * p1[1] - 3 * p2[1] + p3[1]) * t3)
                smooth_points.append((x, y))
                
        smooth_points.append(pts[-2]) # Ensure the exact final point is captured
        return smooth_points