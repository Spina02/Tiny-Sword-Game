import pygame, sys, os
from pygame.locals import *
from settings import *
from level import Level

class Game:
    def __init__(self):

        # general setup
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("game")
        self.clock = pygame.time.Clock()

        self.level = Level()

    def run(self):
        """
        The game loop
        """
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            #self.screen.fill((71, 171, 169, 1))  
            self.level.run()
            pygame.display.update()
            self.clock.tick(FPS)
        
if __name__ == "__main__":
    game = Game()
    game.run()
    

    