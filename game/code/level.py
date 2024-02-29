import pygame
from settings import *
from tile import Tile
from player import Player
from debug import debug
from support import *
from pytmx.util_pygame import load_pygame
from sprites import *
import pytmx
from gui import Cursor
from ui import UI

class Level:
    def __init__(self):
        # get the display surface
        self.display_surface = pygame.display.get_surface()

        # sprite groups
        self.all_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        self.tree_sprites = pygame.sprite.Group()
        # self.interaction_sprites = pygame.sprite.Group()

        self.setup()
        self.ui = UI()
        
    def setup(self):
        self.tmx_data = load_pygame(WORLD_TMX)
        ti = self.tmx_data.get_tile_image_by_gid

        # managing animation setup
        self.frame_index = 0
        self.nextFrame = pygame.time.get_ticks()

        # foam
        for x, y, gid in self.tmx_data.get_layer_by_name('foam'):
            if gid:
                foam = ti(gid)
                offsety = TILESIZE*(foam.get_height()//TILESIZE-1)
                Foam((x*TILESIZE, y*TILESIZE - offsety), foam, [self.all_sprites], gid)

        # ground
        for layer in ['sand', 'grass_0', 'shadows_0', 'rock_0', 'grass_1', 'shadows_1', 'rock_1', 'grass_2', 'bridge']:
            for x, y, surf in self.tmx_data.get_layer_by_name(layer).tiles():
                if surf:
                    Generic((x*TILESIZE, y*TILESIZE), surf, self.all_sprites, LAYERS[layer])

        # deco
        for x, y, gid in self.tmx_data.get_layer_by_name('deco'):
            if gid:
                surf = ti(gid)
                offsety = TILESIZE*(surf.get_height()//TILESIZE-1)
                Deco((x*TILESIZE, y*TILESIZE - offsety), surf, [self.all_sprites], gid)

        # trees
        for x, y, gid in self.tmx_data.get_layer_by_name('tree'):
            if gid:
                tree = ti(gid)
                offsety = TILESIZE*(tree.get_height()//TILESIZE-1)
                Tree(
                    pos = (x*TILESIZE, y*TILESIZE - offsety),
                    surf = tree,
                    groups = [self.all_sprites,
                            self.obstacle_sprites,
                            self.tree_sprites],
                    gid = gid)
                
        # buildings
        for obj in self.tmx_data.get_layer_by_name('buildings'):
            if obj.name == 'Castle' or  obj.name == 'Tower' or obj.name == 'House':
                build = ti(obj.gid)
                offsety = TILESIZE*(build.get_height()//TILESIZE-1)
                Building((obj.x, obj.y), obj.image, [self.all_sprites, self.obstacle_sprites])

        ## sprites
        #for x, y, gid in self.tmx_data.get_layer_by_name('sprites'):
        #    sprite = ti(gid)
        #    if sprite:
        #        offsety = TILESIZE*(sprite.get_height()//TILESIZE-1)
        #        Sprite((x*TILESIZE, y*TILESIZE - offsety), sprite, [self.all_sprites], gid)

        # bounds
        for x, y, surf in self.tmx_data.get_layer_by_name('bounds').tiles():
            Bound((x*TILESIZE, y*TILESIZE),
                    pygame.Surface((TILESIZE, TILESIZE)), [self.obstacle_sprites])

        # Player
        for obj in self.tmx_data.get_layer_by_name('player'):
            if obj.name == 'Start':
                self.player = Player(
                    pos = (obj.x, obj.y),
                    groups = self.all_sprites,
                    obstacle_sprites = self.obstacle_sprites,
                    tree_sprites = self.tree_sprites)

    def run(self):
        ti = self.tmx_data.get_tile_image_by_gid

        # drawing logic
        self.display_surface.fill((71, 171, 169, 1)) ## paints sea
        self.all_sprites.custom_draw(self.player)

        # managing animated frames
        if pygame.time.get_ticks() > self.nextFrame:
            self.frame_index = self.frame_index + 1
            self.nextFrame += 100

            for sprite in self.all_sprites:
                if hasattr(sprite, 'gid'):
                    props = self.tmx_data.get_tile_properties_by_gid(sprite.gid)
                    if props and props['frames'] and sprite.image == ti(props['frames'][(self.frame_index-1)%len(props["frames"])].gid):
                        sprite.image = ti(props['frames'][self.frame_index%len(props["frames"])].gid)

        self.all_sprites.update()
        self.ui.display(self.player)


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()
        self.cursor = Cursor()

    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - WIDTH / 2
        self.offset.y = player.rect.centery - HEIGHT / 2

        for layer in LAYERS.values():
            for sprite in sorted(self.sprites(), key=lambda sprite: sprite.hitbox.bottom):
                if sprite.z == layer:
                    if sprite == player:
                        offset_pos = (sprite.rect.topleft[0], sprite.rect.topleft[1]-32) - self.offset
                    else:
                        offset_pos = sprite.rect.topleft - self.offset
                    self.display_surface.blit(sprite.image, offset_pos)

                    # analytics
                    # if sprite.z == LAYERS['main']:
                    #     #pygame.draw.rect(self.display_surface, 'red', offset_rect, 5)
                    #     hitbox_rect = sprite.hitbox.copy()
                    #     hitbox_rect.center = offset_rect.center
                    #     pygame.draw.rect(self.display_surface, 'green', hitbox_rect, 5)
        
        self.cursor.update()
        self.display_surface.blit(self.cursor.cursor_img, self.cursor.cursor_rect) # draw the cursor
