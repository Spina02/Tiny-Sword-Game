import pygame
from pygame.locals import *
from settings import *
from support import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacles_sprites):
        super().__init__(groups) 
        self.charachter_path = "game/graphics/Factions/Knights/Troops/Warrior/Yellow/Warrior_Yellow.png"
        self.sprite_sheet = pygame.image.load(self.charachter_path)
        
        self.frame_width = self.sprite_sheet.get_width()/8
        self.frame_height = self.sprite_sheet.get_height()/8
        #print(f'{frame_height, frame_width}')
        self.image = self.sprite_sheet.subsurface((0, 0, self.frame_width, self.frame_height))
        
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0,-80)
        
        #graphic
        self.import_player_assets()
        self.status = "right_idle"
        self.frame_index = 0
        self.animation_speed = 0.06
        
        # movement
        self.direction = pygame.math.Vector2()
        self.speed = 3
        self.attacking = False
        self.attack_cooldown = 610
        self.attack_time = None

        self.obstacles_sprites = obstacles_sprites    
       
    def import_player_assets(self):
        
        self.animations = {
            # idel --> quando stai fermo immobile
            "right_idle": self.get_animation_frames(self.sprite_sheet, 0, 0, self.frame_height, self.frame_width, 1, 6),
            "right": self.get_animation_frames(self.sprite_sheet, 0, self.frame_height, self.frame_height, self.frame_width, 1, 6),
            "right_attack_1": self.get_animation_frames(self.sprite_sheet, 0, 2*self.frame_height, self.frame_height, self.frame_width, 1, 6),
            #"right_attack_2": self.get_animation_frames(self.sprite_sheet, 0, 3*TILESIZE, self.frame_height, self.frame_width, 1, 6),
            #"right_frontal_attack_1": self.get_animation_frames(self.sprite_sheet, 0, 4*TILESIZE, self.frame_height, self.frame_width, 1, 6),
            #"right_frontal_attack_2": self.get_animation_frames(self.sprite_sheet, 0, 5*TILESIZE, self.frame_height, self.frame_width, 1, 6),
            #"right_back_attack_1": self.get_animation_frames(self.sprite_sheet, 0, 6*TILESIZE, self.frame_height, self.frame_width, 1, 6),
            #"right_back_attack_2": self.get_animation_frames(self.sprite_sheet, 0, 7*TILESIZE, self.frame_height, self.frame_width, 1, 5),
            "left_idle": [pygame.transform.flip(frame, True, False) for frame in self.get_animation_frames(self.sprite_sheet, 0, 0, self.frame_height, self.frame_width, 1, 6)],
            "left": [pygame.transform.flip(frame, True, False) for frame in self.get_animation_frames(self.sprite_sheet, 0, self.frame_height, self.frame_height, self.frame_width, 1, 6)],
            "left_attack_1": [pygame.transform.flip(frame, True, False) for frame in self.get_animation_frames(self.sprite_sheet, 0, 2*self.frame_height, self.frame_height, self.frame_width, 1, 6)],

        }
        
        
        print(self.animations)
        
    def get_animation_frames(self, sheet, start_x, start_y, size_x, size_y, rows, columns):
        frames = []
        print("Finding frames...\n")
        for row in range(rows):
            for col in range(columns):
                frame = sheet.subsurface((start_x + col * size_x, start_y + row * size_y, size_x, size_y))
                #resized_surface = pygame.transform.scale(frame, (64, 48))
                frames.append(frame)
                #frames.append(resized_surface)
        print(f"Frames are: {frames}")
        return frames
    
    def get_status(self):
        
        #idle status
        if self.direction.x == 0 and self.direction.y == 0:
            if not 'idle' in self.status and not "attack" in self.status:
                self.status = self.status + "_idle"


        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0
            if not "attack" in self.status:
                self.frame_index = 0
                if "idle" in self.status:
                    #overwrite idle
                    self.status = self.status.replace("_idle", '_attack_1')
                else:
                    self.status = self.status + "_attack_1" 
                    
        else:
            if 'attack' in self.status:
                self.status = self.status.replace("_attack_1", "_idle")
    
    def input(self):
        keys = pygame.key.get_pressed()
        if not self.attacking:
            if keys[K_UP]:
                self.direction.y = -1
            elif keys[K_DOWN]:
                self.direction.y = 1
            else:
                self.direction.y = 0
            
            if keys[K_RIGHT]:
                self.direction.x = 1
                self.status = 'right'
            elif keys[K_LEFT]:
                self.direction.x = -1
                self.status = 'left'
            
            else:
                self.direction.x = 0
                
            # attack input
            if keys[pygame.K_SPACE] and not self.attacking:
                
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                print("attack")

    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        
        self.hitbox.x += self.direction.x*speed
        self.collision("horizontal")
        self.hitbox.y += self.direction.y*speed
        self.collision("vertical")
        self.rect.center = self.hitbox.center

    def collision(self, direction):
        if direction == "horizontal":
            for sprite in self.obstacles_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0: # moving right
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0: # moving left
                        self.hitbox.left = sprite.hitbox.right
        
        if direction == "vertical":
            for sprite in self.obstacles_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0: # moving down
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0: # moving up
                        self.hitbox.top = sprite.hitbox.bottom        

    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        
        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.attacking = False

    def animate(self):
        animation = self.animations[self.status]
        
        # loop over the fram index
        self.frame_index += self.animation_speed
        if self.frame_index > len(animation):
            self.frame_index = 0
            
        #set the image
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)
    
    def update(self):
        # update and draw the game
        self.input()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move(self.speed)