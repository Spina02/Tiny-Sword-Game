import pygame
from settings import *

class UI:
    def __init__(self):
        #general
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)
        
        self.health_bar_rect = pygame.Rect(WIDTH*0.005, HEIGHT*0.01, HEALTH_BAR_WIDTH, BAR_HEIGHT)
        self.energy_bar_rect = pygame.Rect(WIDTH*0.005, HEIGHT*0.03, ENERGY_BAR_WIDTH, BAR_HEIGHT)
    
    def show_bar(self, current, max_amount, bg_rect, color):
        #? draw bg
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)
       
        #? converting stat to pixel 
        ratio = current / max_amount
        current_width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width = current_width
    
        #? draw bar
        pygame.draw.rect(self.display_surface, color, current_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)
       
    def show_exp(self, exp):
        text_surf = self.font.render(str(int(exp)), False, TEXT_COLOR)   # str perché serve una strigna ocme paramentro
        x = self.display_surface.get_size()[0] - 20
        y = self.display_surface.get_size()[1] - 60
        text_rect = text_surf.get_rect(bottomright = (x, y))
        
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, text_rect.inflate(20, 10))
        
        self.display_surface.blit(text_surf, text_rect)
        
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, text_rect.inflate(20, 10), 3)
        
    def selection_box(self, left, top):
        bg_rect = pygame.Rect(left, top, ITEM_BOX_SIZE, ITEM_BOX_SIZE)
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)    
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)    
        
    def weapon_overlay(self, weapon_index):
        bg_rect = self.selection_box(WIDTH*0.01, HEIGHT*0.91)

        #self.display_surface.blit(weapon_surf, weapon_rect)
        
    def display(self, player):
        self.show_bar(player.health, player.stats["health"], self.health_bar_rect, HEALTH_COLOR)
        self.show_bar(player.energy, player.stats["energy"], self.energy_bar_rect, ENERGY_COLOR)
        
        self.show_exp(player.exp)
        
        
        self.weapon_overlay(player.weapon_index)