import pygame, sys, os
from pygame.locals import *
from settings import *
from math import sin

class Cursor():
    def __init__(self):
        pygame.mouse.set_visible(False)
        self.cursor_img = pygame.image.load('game/graphics/UI/Pointers/01.png')
        self.cursor_rect = self.cursor_img.get_rect()
        self.cursor_rect.center = pygame.mouse.get_pos()
        self.click = False
        self.click_time = self.click_time = pygame.time.get_ticks();
        self.click_cooldown = 200

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                self.click = True
                self.click_time = pygame.time.get_ticks();
        
        self.cooldowns()

    def cooldowns(self):
        """
        Define cooldowns for actions as 'click'
        """
        current_time = pygame.time.get_ticks()
        if self.click:
            if current_time - self.click_time >= self.click_cooldown:
                self.click = False
            else:
                if current_time - self.click_time <= self.click_cooldown/2:
                    self.cursor_rect.center = (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1] + 4)
                else:
                    self.cursor_rect.center = (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
        else:
            self.cursor_rect.center = pygame.mouse.get_pos()
        
