import pygame
from settings import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, surface = pygame.Surface((TILESIZE, TILESIZE))):
        super().__init__(groups)
        self.image = surface
        self.rect = self.image.get_rect(topleft = pos)
        self.offsety = 0

        # #? --------------- centring non 64x64 objects --------------- => ora in "level.py"
        # if sprite_type == 'deco':
        #     if self.image.get_height() > TILESIZE:
        #         self.offsety = TILESIZE*(self.image.get_height()//TILESIZE-1)
        
        self.rect = self.image.get_rect(topleft = (pos[0], pos[1] - self.offsety))
        self.hitbox = self.rect.inflate(-10,-self.rect.height*0.60)