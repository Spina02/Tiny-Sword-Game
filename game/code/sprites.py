import pygame
from settings import *

class Generic(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups, z=LAYERS['main']):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)
        self.z = z
        self.hitbox = self.rect.copy().inflate(-10,-self.rect.height*0.20)

class Deco(Generic):
    def __init__(self, pos, surf, groups, gid):
        super().__init__(pos, surf, groups)
        self.gid = gid
        self.hitbox = self.rect.copy().inflate(-self.rect.width*0.5,-self.rect.height*0.5)    

class Sprite(Generic):
    def __init__(self, pos, surf, groups, gid):
        super().__init__(pos, surf, groups)
        self.gid = gid
        self.hitbox = self.rect.copy().inflate(-self.rect.width*0.7,-self.rect.height*0.7)

class Foam(Generic):
    def __init__(self, pos, surf, groups, gid):
        super().__init__(pos, surf, groups, z = LAYERS["foam"])
        self.gid = gid
           
class Bound(Generic):
    def __init__(self, pos, surf, groups):
        super().__init__(pos, surf, groups)
        self.hitbox = self.rect.inflate(-10,-self.rect.height*0.20)

class Building(Generic):
    def __init__(self, pos, surf, groups):
        super().__init__(pos, surf, groups)
        self.hitbox = self.rect.inflate(-10,-self.rect.height*0.20)

class Tree(Generic):
    def __init__(self, pos, surf, groups, gid):
        super().__init__(pos, surf, groups)
        self.gid = gid
        self.hitbox = self.rect.inflate(-self.rect.width*0.50,-self.rect.height*0.30)

