import pygame, sys, os
from pygame.locals import *
from settings import *
from gui import *
from level import Level
import pyautogui

class Game:
    def __init__(self):

        # general setup
        pygame.init()
        self.screen = pygame.display.set_mode(pyautogui.size(), pygame.FULLSCREEN | pygame.HWSURFACE | pygame.SCALED, vsync=1)
        pygame.display.set_caption("game")
        self.clock = pygame.time.Clock()
        self.level = Level()
        self.cursor = Cursor()

    def run(self):
        """
        The game loop
        """
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                        
                if event.type == pygame.MOUSEBUTTONUP:
                    self.level.all_sprites.cursor.do_click()
            
            self.level.run()
            pygame.display.update()
            self.clock.tick(FPS)
        
if __name__ == "__main__":
    game = Game()
    game.run()