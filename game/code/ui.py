import pygame
from settings import *

class UI:
    def __init__(self):
        #general
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)
        
        self.exp_bar_rect = pygame.Rect(2*PADDING_X + PLAYER_BOX_SIZE, 2*PADDING_Y, EXP_BAR_WIDTH, EXP_BAR_HEIGHT)
        self.health_bar_rect = pygame.Rect(2*PADDING_X + PLAYER_BOX_SIZE, EXP_BAR_HEIGHT + 3*PADDING_Y, HEALTH_BAR_WIDTH, BAR_HEIGHT)
        self.energy_bar_rect = pygame.Rect(2*PADDING_X + PLAYER_BOX_SIZE, EXP_BAR_HEIGHT + BAR_HEIGHT + 4*PADDING_Y, ENERGY_BAR_WIDTH, BAR_HEIGHT)
    
    def show_bar(self, current, max_amount, bg_rect, color, player, energy = False):
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

        if energy:
            pygame.draw.line(self.display_surface, "black", (bg_rect.x + ENERGY_BAR_WIDTH*15/player.stats["energy"] ,bg_rect.y), (bg_rect.x + ENERGY_BAR_WIDTH*15/player.stats["energy"] ,bg_rect.y + BAR_HEIGHT - 1), 2)
       
    def show_exp(self, exp):
        text_surf = self.font.render(str(int(exp)), False, TEXT_COLOR)   # str perché serve una strigna ocme paramentro
        x = WIDTH - text_surf.get_width()
        y = HEIGHT - text_surf.get_height()
        text_rect = text_surf.get_rect(bottomright = (x, y))
        
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, text_rect.inflate(20, 10))
        
        self.display_surface.blit(text_surf, text_rect)
        
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, text_rect.inflate(20, 10), 3, 5)
        
    def selection_box(self, left, top):
        bg_rect = pygame.Rect(left, top, ITEM_BOX_SIZE, ITEM_BOX_SIZE)
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)    
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)   

    def stats_box(self, left, top):
        bg_rect = pygame.Rect(left, top, PLAYER_BOX_SIZE, PLAYER_BOX_SIZE)
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)    
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)
        
    def weapon_overlay(self, weapon_index):
        bg_rect = self.selection_box(PADDING_X, HEIGHT - 2*PADDING_Y - ITEM_BOX_SIZE)

        #self.display_surface.blit(weapon_surf, weapon_rect)
        
    def display(self, player):

        stats_rect = self.stats_box(PADDING_X, 2*PADDING_Y)
        self.show_bar(player.exp, player.stats["exp"], self.exp_bar_rect, EXP_COLOR, player)
        self.show_bar(player.health, player.stats["health"], self.health_bar_rect, HEALTH_COLOR, player)
        self.show_bar(player.energy, player.stats["energy"], self.energy_bar_rect, ENERGY_COLOR, player, True)
        
        self.show_exp(player.exp)
        
        self.weapon_overlay(player.weapon_index)