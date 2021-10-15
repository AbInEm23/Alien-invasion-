import sys 
import pygame 

from settings import Settings 
from ship import Ship 
from bullet import Bullet

class AlienInvasion: 
    #"""Overall class to manage game assets and behavior."""

    def __init__(self):
        #"""Initialize the game, and create game resources."""

        #Initializes the background settings that Pygame needs to work properly
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        #creates a display window on which we will draw all the games graphical elements
        #self.screen is a surface, which is the part of the screen an elemnt can be displayed 
        #A tuple that defines the dimension of the game window

        pygame.display.set_caption("AlienInvasion")
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()

        # Set the background color.
        self.bg_color = (230,230,230)

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()
            self.ship.update()
            self._update_bullets()
            self.bullets.update()
            # Watch for keyboard and mouse events (an event is an action that the user performs while playing the game ).
            
            self._update_screen()
    def _check_events(self):
         #Responds to key presses and mouse events
        for event in pygame.event.get():
            #event.get(): this function returns a list of events that have taken place since the last time it was called 
            if event.type == pygame.QUIT:
                 sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
               
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
            #Move the ship to the right by taps.
             #self.ship.rect.x += 1
            # Redraw the screen during each pass through the loop 
    def _fire_bullet(self):
        #create a new bullet and add it to the bullets group
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            #create an instance of a bullet and call it new bullet 
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        #update position of bullets and get rid of old bullets
        #update bullet positions. 
                    #Get rid of bullets that have dissappeared
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0: #check to see if bullet is gone then remove 
                self.bullets.remove(bullet)
            #print(len(self.bullets)) {to check if bullets were deleting}

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()

        #returns a list of all sprites in the group bullets, to draw all fired bullets 
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()  
         #draw ship


        # Make the most recently drawn screen visible. 
        pygame.display.flip()

if __name__ == '__main__':
    # Make a game instance, and run the game. 
    ai = AlienInvasion()
    ai.run_game()



