import pygame
from pygame.locals import *
from settings import *

class Player(pygame.sprite.Sprite):
    """
    Is one of the main classes of the project, it deals the manipulation the player.
    #### Player(pos, groups, obstacle_sprites):
    - @pos = is the initial position of the player
    - @groups = is the sprite group to which this class should belong
    - @obstacle_sprites = is the group of obstacle for this class
    """
    def __init__(self, pos, groups, obstacle_sprites):
        super().__init__(groups) 

        #? ---------- general settinges ------------
        self.n_frame = 1
        self.n_anim = 1

        #? --------------- load image --------------
        self.images = None
        self.image = self.img_init(PLAYER_IMG, 6, 8).convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)

        #? ------------- define hitbox -------------
        self.hitbox = pygame.Rect(self.rect.topleft[0], self.rect.topleft[1], 32, 20)
        #hitbox_size = (45, 60)

        #? ------------- graphic setup -------------
        self.import_player_assets()
        self.status = 'down'
        self.frame_index = 0
        self.nextFrame = pygame.time.get_ticks()

        #? ---------------- movement ----------------
        self.direction = pygame.math.Vector2()
        self.speed = (0.5*FPS//30)
        self.attacking = False
        self.attack_cooldown = 500
        self.attack_time = None

        self.obstacle_sprites = obstacle_sprites

    def import_player_assets(self):
        """
            Defines animations as a dictionary:\n
            -----
            animations = {
                "anim_name" : (int anim_idx, bool flip)
            }.
        """
        self.animations = { #? -> each tuple is (n_anim, flip),
            'up_idle' : (0, 1),'down_idle' : (0, 0),'left_idle' : (0, 1),'right_idle' : (0, 0),
            'up': (1, 1), 'down' : (1,0), 'left' : (1,1), 'right': (1,0), 
            'up_attack' : (6,1), 'down_attack' : (2,0), 'left_attack' : (3,1), 'right_attack' : (3,0)
        }

    def img_init(self, image, n_frame, n_anim):
        """
        #### Initialize player image
        ---
        #### Parameters
        - @image = filename of the image
        - @n_frame = number of frame in a row of the image
        - @n_anim = numbero of animations in a column of the image
        """
        self.n_frame = n_frame
        self.n_anim = n_anim
        self.images = [[] for _ in range(self.n_anim)]

        img = pygame.image.load(image).convert_alpha()
        self.originalWidth = img.get_width() // n_frame
        self.originalHeight = img.get_height() // n_anim

        for animNo in range(self.n_anim):
            for frameNo in range(self.n_frame):
                start_x = frameNo * self.originalWidth
                start_y = animNo * self.originalHeight
                frame = img.subsurface((start_x, start_y, self.originalWidth, self.originalHeight))
                self.images[animNo].append(frame)
        # print(f"Frames are: {self.images}")

        self.currentImage = 0
        return self.images[0][0]
        
    def changeImage(self, anim, flip = 0):
        """
        #### Changes the image of the sprite to the one specified
        ---
        #### Parameters:
        - @anim = the animation index in the image
        - @flip = 1 if the image needs to be flipped horizontally [default = 0]
        """
        self.currentImage = (anim, self.frame_index)
        self.image = pygame.transform.flip(self.images[anim][self.frame_index], flip, 0)
        self.mask = pygame.mask.from_surface(self.image)

    def input(self):
        """

        manages the inputs from keyboard
        """
        keys = pygame.key.get_pressed()

        if not self.attacking:
            # movement input
            if keys[K_UP]:
                self.direction.y = -1
                self.status = 'up'
            elif keys[K_DOWN]:
                self.direction.y = 1
                self.status = 'down'
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
            if keys[K_SPACE] and not self.attacking:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()

        
    def get_status(self):
        """
        Manages player status:
        - idle
        - movement
        - attack
        - ...
        """
        # idle status
        if self.direction.x == 0 == self.direction.y:
            if not 'idle' in self.status and not 'attack' in self.status:
                self.status += '_idle'
                self.frame_index = 0
        # attacking status
        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0
            if not 'attack' in self.status:
                if 'idle' in self.status:
                    self.status = self.status.replace('_idle', '_attack')
                else:
                    self.status += '_attack'
                self.frame_index = 0
        # any other status
        else:
            if 'attack' in self.status:
                self.status = self.status.replace('_attack', '')
                #self.frame_index = 0

    def move(self, speed):    
        """
        Manages the movement of the player checking for collisions
        """   
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        
        self.hitbox.x += self.direction.x*speed
        self.collision("horizontal")
        self.hitbox.y += self.direction.y*speed
        self.collision("vertical")
        self.rect.center = self.hitbox.center

    def collide_mask_rect(self, hitbox_1, hitbox_2):
        """
        turns the two rects given in input into masks before
        checking for collisions
        """
        xoffset = hitbox_2.midleft[0] - hitbox_1.midleft[0]
        yoffset = hitbox_2.midbottom[1] - hitbox_1.midbottom[1]
        try:
            leftmask = hitbox_1.mask
        except AttributeError:
            leftmask = pygame.mask.Mask(hitbox_1.size, True)
        try:
            rightmask = hitbox_2.mask
        except AttributeError:
            rightmask = pygame.mask.Mask(hitbox_2.size, True)
        return leftmask.overlap(rightmask, (xoffset, yoffset))

    def collision(self, direction):
        """
        Manages the collisions
        """
        # TODO: implementare meglio le masks

        if direction == "horizontal":
            for sprite in self.obstacle_sprites:
                #if self.collide_mask_rect(self.hitbox, sprite.hitbox): # check between rects converted to masks
                if sprite.hitbox.colliderect(self.hitbox): # check between rects
                    if self.direction.x > 0: # moving right
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0: # moving left
                        self.hitbox.left = sprite.hitbox.right
        if direction == "vertical":
            for sprite in self.obstacle_sprites:
                #if self.collide_mask_rect(self.hitbox, sprite.hitbox):
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0: # moving down
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0: # moving up
                        self.hitbox.top = sprite.hitbox.bottom
                    
    def cooldowns(self):
        """
        Define cooldowns for actions as 'attack'
        """
        current_time = pygame.time.get_ticks()
        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.attacking = False
                self.frame_index = 0

    def animate(self):
        """
        Animates the player managing frames
        """
        (animation, flip) = self.animations[self.status]
        if pygame.time.get_ticks() > self.nextFrame:
            self.frame_index = (self.frame_index + 1) % (self.n_frame)
            self.nextFrame += 100

            self.changeImage(animation, flip)
            self.rect = self.image.get_rect(center = (self.hitbox.centerx, self.hitbox.centery))

    def update(self):
        """
        Update and draw the game
        """
        self.input()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move(self.speed)