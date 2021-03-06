import pygame 
from pygame.sprite import Sprite

class Alien(Sprite):
    # A class to represent a single alien fleet 
    def __init__(self,ai_game):
        # initialize the alien and set its starting position 
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings #creating a settings parameter to access alien speed 

        #load the alien image and set its rect attribute 
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        #start each new alien near the top left of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        #store the aliens exact horizontal position.
        self.x = float(self.rect.x)

    def update(self):
        #Move the alien to the right 
        self.x += (self.settings.alien_speed * self.settings.fleet_direction) 
        # if fleet is positive moves right if negative moves left 
        # we use this to update the position of the alien 

        self.rect.x = self.x 

    
    def check_edges(self):
        #Return true  if alien is at edge of screen 
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            # the alien is at the edge if the if the attribute of its rect is >= to the right attribute of the screen 
            return True

