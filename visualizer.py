import pygame
import numpy as np
from config import *

class Visualizer:
    """Real-time visualization of the digital biosphere"""
    
    def __init__(self, universe):
        pygame.init()
        
        self.universe = universe
        self.width = GRID_WIDTH * CELL_SIZE
        self.height = GRID_HEIGHT * CELL_SIZE + 150  # Extra space for stats
        
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("GENESIS - Digital Biosphere")
        
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 24)
        self.small_font = pygame.font.Font(None, 18)
        
        self.paused = False
    
    def draw_energy(self):
        """Draw energy grid"""
        for y in range(self.universe.height):
            for x in range(self.universe.width):
                energy = self.universe.energy_grid[y][x]
                if energy > 0:
                    # Green intensity based on energy amount
                    intensity = min(255, int(energy / MAX_ENERGY_PER_CELL * 255))
                    color = (0, intensity, 0)
                    
                    rect = pygame.Rect(
                        x * CELL_SIZE,
                        y * CELL_SIZE,
                        CELL_SIZE,
                        CELL_SIZE
                    )
                    pygame.draw.rect(self.screen, color, rect)
    
    def draw_organisms(self):
        """Draw all organisms"""
        for organism in self.universe.organisms:
            x = organism.x * CELL_SIZE
            y = organism.y * CELL_SIZE
            
            # Draw organism with its genetic color
            color = organism.get_color()
            
            # Size based on energy
            size = min(CELL_SIZE, max(2, int(organism.energy / 50)))
            
            pygame.draw.circle(
                self.screen,
                color,
                (x + CELL_SIZE // 2, y + CELL_SIZE // 2),
                size
            )
    
    def draw_stats(self):
        """Draw statistics panel"""
        stats = self.universe.get_stats()
        
        y_offset = GRID_HEIGHT * CELL_SIZE + 10
        
        # Background for stats
        stats_rect = pygame.Rect(0, GRID_HEIGHT * CELL_SIZE, self.width, 150)
        pygame.draw.rect(self.screen, (20, 20, 20), stats_rect)
        
        # Title
        title = self.font.render("GENESIS - Digital Evolution", True, (0, 255, 0))
        self.screen.blit(title, (10, y_offset))
        
        # Stats
        stats_text = [
            f"Tick: {stats['tick']}",
            f"Population: {stats['population']} (Peak: {stats['peak_population']})",
            f"Births: {stats['total_births']} | Deaths: {stats['total_deaths']}",
            f"Avg Energy: {stats['avg_organism_energy']:.1f}",
            f"Total Energy in World: {stats['total_energy']:.0f}",
        ]
        
        for i, text in enumerate(stats_text):
            rendered = self.small_font.render(text, True, (200, 200, 200))
            self.screen.blit(rendered, (10, y_offset + 30 + i * 20))
        
        # Controls
        controls = self.small_font.render(
            "SPACE: Pause | ESC: Quit | R: Reset",
            True,
            (150, 150, 150)
        )
        self.screen.blit(controls, (self.width - 300, y_offset + 30))
        
        # Pause indicator
        if self.paused:
            pause_text = self.font.render("PAUSED", True, (255, 255, 0))
            self.screen.blit(pause_text, (self.width // 2 - 50, y_offset))
    
    def handle_events(self):
        """Handle user input"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                elif event.key == pygame.K_SPACE:
                    self.paused = not self.paused
                elif event.key == pygame.K_r:
                    return 'reset'
        
        return True
    
    def render(self):
        """Render one frame"""
        # Clear screen
        self.screen.fill((0, 0, 0))
        
        # Draw layers
        if SHOW_ENERGY:
            self.draw_energy()
        
        self.draw_organisms()
        
        if SHOW_STATS:
            self.draw_stats()
        
        # Update display
        pygame.display.flip()
        self.clock.tick(FPS)
    
    def is_paused(self):
        return self.paused
    
    def close(self):
        pygame.quit()
