import pygame
from settings import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, sprite_type, surface = pygame.Surface((TILESIZE, TILESIZE))):
        super().__init__(groups)
        self.sprite_type = sprite_type
        self.image = surface
        self.offsetx = 0
        self.offsety = 0
        if sprite_type == 'deco':
            if self.image.get_height() > TILESIZE:
                self.offsety = TILESIZE*(self.image.get_height()//TILESIZE-1)
            self.rect = self.image.get_rect(topleft = (pos[0] + self.offsetx, pos[1] - self.offsety))
        else:
            self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0,-10)
