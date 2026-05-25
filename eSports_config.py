import os
import pygame
from typing import List, Dict, Any

# ==========================================
# MODULE 1: CONFIGURATION & ASSETS
# ==========================================

class Config:
    """
    Central configuration management for the application.
    
    This class holds global constants, runtime settings, and utility methods
    for environment setup (directories, paths).
    """
    # Display settings
    WIDTH: int = 1280
    HEIGHT: int = 720
    FPS: int = 60
    
    # Visual Themes
    # Each palette defines the color scheme for the UI components.
    PALETTES: List[Dict[str, Any]] = [
        {"name": "CYAN", "bg": (10, 12, 16), "fill": (15, 20, 25), "accent": (0, 255, 255), "dim": (0, 100, 100), "text": (220, 225, 235), "dots": (20, 40, 50)},
        {"name": "ORANGE", "bg": (20, 10, 5), "fill": (30, 15, 10), "accent": (255, 140, 0), "dim": (120, 60, 0), "text": (255, 240, 220), "dots": (60, 30, 10)},
        {"name": "GREEN", "bg": (5, 10, 5), "fill": (0, 20, 0), "accent": (50, 255, 50), "dim": (0, 100, 0), "text": (200, 255, 200), "dots": (10, 50, 10)}
    ]

class Assets:
    """
    Asset management for the application.
    
    Handles loading and caching of resources such as fonts.
    """
    FONTS: Dict[str, pygame.font.Font] = {}

    @staticmethod
    def load_fonts() -> None:
        """
        Initialize and load application fonts.

        This method iterates through a list of preferred monospace fonts to ensure
        consistent UI rendering across different operating systems (Windows, Linux, macOS).
        It populates the Assets.FONTS dictionary with pygame.font.SysFont objects.
        """
        # List of preferred fonts in descending order of preference.
        # We prioritize fonts that look "techy" or "terminal-like".
        valid_fonts = [
            "Consolas",          # Windows default monospace
            "Courier New",       # Universal fallback
            "Liberation Mono",   # Linux common
            "DejaVu Sans Mono",  # Linux common
            "monospace"          # Generic system alias
        ]
        
        selected_font_name = "monospace" # Default fallback
        
        # Check which font is actually available on the system
        for name in valid_fonts:
            if pygame.font.match_font(name):
                selected_font_name = name
                break

        # Initialize font objects with specific sizes and styles
        # SysFont is used here to load from system installed fonts by name.
        Assets.FONTS["MAIN"] = pygame.font.SysFont(selected_font_name, 20, bold=True)
        Assets.FONTS["SUB"] = pygame.font.SysFont(selected_font_name, 16)
        Assets.FONTS["TINY"] = pygame.font.SysFont(selected_font_name, 12)
        Assets.FONTS["BIG"] = pygame.font.SysFont(selected_font_name, 32, bold=True)
        Assets.FONTS["CORE"] = pygame.font.SysFont(selected_font_name, 26, bold=True)
        Assets.FONTS["CLOCK"] = pygame.font.SysFont(selected_font_name, 14, bold=True)