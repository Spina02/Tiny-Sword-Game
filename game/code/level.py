import pygame
from settings import *
from tile import Tile
from player import Player
from debug import debug
from support import *
from pytmx.util_pygame import load_pygame
import pytmx

class Level:
    def __init__(self):
        # get the display surface
        self.display_surface = pygame.display.get_surface()

        # sprite group setup
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        self.tmx_data = load_pygame(WORLD_TMX)
        self.create_map()

    def create_map(self):
        layouts = {
            'boundary' : import_csv_layout('game/map/map_bounds.csv'),
            'deco' : import_csv_layout('game/map/map_deco.csv'),
            'tree' : import_csv_layout('game/map/map_Tree.csv')
        }
        graphics = {
            #'grass' : import_folder('game/graphics/Terrain/...'),
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
                        if style == 'deco':
                            surf = graphics['deco'][int(col)]
                            Tile((x,y), [self.visible_sprites], 'deco', surf) #self.obstacle_sprites], 'deco', surf)
        
        
        self.player = Player((700,800), [self.visible_sprites], self.obstacle_sprites)
        

    def run(self):
        """
        update and draw the game
        """
        self.visible_sprites.custom_draw(self.player, self.tmx_data)
        self.visible_sprites.update()
        debug(self.player.status)

class YSortCameraGroup(pygame.sprite.Group):
    """
    Class of object sorted by 'y' to create camera
    """
    def __init__(self):

        #general setup
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0]//2
        self.half_height = self.display_surface.get_size()[1]//2
        self.offset = pygame.math.Vector2()

        #
        self.foam_frame = 0
        self.nextFrame = pygame.time.get_ticks()

        # creating the floor
        self.floor_surf = pygame.image.load('game/graphics/ground.png').convert()
        self.floor_rect = self.floor_surf.get_rect(topleft = (0,0))
        
    def custom_draw(self, player, tmx_data):
        """
        Draws the images on screen, keeping the camera centred on player
        """
        self.tmx_data = tmx_data

        # managing foam frames
        if pygame.time.get_ticks() > self.nextFrame:
            self.foam_frame = (self.foam_frame + 1)%6
            self.nextFrame += 100

        # getting offset
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        # drawing the floor
        #floor_offset_pos = self.floor_rect.topleft - self.offset
        #self.display_surface.blit(self.floor_surf, floor_offset_pos)
    #? ---------------------------- render levels ----------------------------
        ti = self.tmx_data.get_tile_image_by_gid
        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = ti(gid)
                    if tile:
                        offsety = 0
                        if layer == self.tmx_data.get_layer_by_name("foam"):
                            for gid, props in self.tmx_data.tile_properties.items():
                                if props['frames'] and tile == self.tmx_data.get_tile_image_by_gid(props['frames'][0].gid):
                                    tile = self.tmx_data.get_tile_image_by_gid(props['frames'][self.foam_frame].gid)
        
                        if layer != self.tmx_data.get_layer_by_name("deco"): #and layer != self.tmx_data.get_layer_by_name("tree"):
                            if tile.get_height() > TILESIZE:
                                offsety = TILESIZE*(tile.get_height()//TILESIZE-1)
                        offset_pos = (x*tmx_data.tilewidth, y*tmx_data.tileheight) - self.offset
                        self.display_surface.blit(tile, (offset_pos[0], offset_pos[1] - offsety))
    #?-----------------------------------------------------------------------------------

        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.hitbox.bottom):
            if sprite == player:
                offset_pos = (sprite.rect.topleft[0], sprite.rect.topleft[1]-25) - self.offset
            else:
                offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)

        #? --------------- debug hitbox ---------------
        """
        surf = pygame.Surface((player.hitbox_damage.width, player.hitbox_damage.height))
        surf.fill("red")
        self.display_surface.blit(surf,(player.hitbox_damage.topleft[0] - player.hitbox_damage.centerx + self.half_width, player.hitbox_damage.topleft[1] - player.hitbox_damage.centery + self.half_height))
        \"""
        surf = pygame.Surface((player.hitbox.width, player.hitbox.height))
        surf.fill("black")
        self.display_surface.blit(surf,(player.hitbox.topleft[0] - player.hitbox.centerx + self.half_width, player.hitbox.topleft[1] - player.hitbox.centery + self.half_height))
        """