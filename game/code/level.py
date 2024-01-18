import pygame
from settings import *
from tile import Tile
from player import Player
from debug import debug
from support import *
from random import choice

class Level:
    def __init__(self):
        # get the display surface
        self.display_surface = pygame.display.get_surface()

        # sprite group setup
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        self.create_map()

    def create_map(self):
        layouts = {
            'boundary' : import_csv_layout('game/map/map_bounds.csv'),
            'deco' : import_csv_layout('game/map/map_deco.csv')
        }
        graphics = {
            'grass' : import_folder('game/graphics/Terrain/...'),
            'deco' : import_folder('game/graphics/Deco')
        }

        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == 'boundary':
                            Tile((x,y), [self.obstacle_sprites], 'invisible')
                        # if style == 'grass':
                        #     random_grass_image = choice(graphics['grass'])
                        #     Tile((x,y), [self.visible_sprites, self.obstacle_sprites], 'grass', random_grass_image)
                        if style == 'deco':
                            
                            surf = graphics['deco'][int(col)]
                            Tile((x,y), [self.visible_sprites, self.obstacle_sprites], 'deco', surf)



        #         if col == 'x':
        #             Tile((x,y), [self.visible_sprites, self.obstacle_sprites])
        #         if col == 'p':
        #             self.player = Player((x,y), [self.visible_sprites], self.obstacle_sprites)
        self.player = Player((700,700), [self.visible_sprites], self.obstacle_sprites)

    def run(self):

        # update and draw the game
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()
        # debug(self.player.direction)

class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):

        #general setup
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0]//2
        self.half_height = self.display_surface.get_size()[1]//2
        self.offset = pygame.math.Vector2()

        # creating the floor
        self.floor_surf = pygame.image.load('game/graphics/ground.png').convert()
        self.floor_rect = self.floor_surf.get_rect(topleft = (0,0))

    def custom_draw(self, player):

        # getting offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height


        #drawing the floor
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf, floor_offset_pos)

        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)