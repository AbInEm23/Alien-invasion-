import sys 
from time import sleep
import pygame 

from settings import Settings 
from game_stats import GameStats
from ship import Ship 
from bullet import Bullet
from alien import Alien

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

        #Create an instance to store ganme stats 
        self.stats = GameStats(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()
        #helps create fleet of aliens 

        # Set the background color.
        self.bg_color = (230,230,230)

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()
            self.ship.update()
            self._update_bullets()
            self._update_aliens()
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
        self._check_bullet_alien_collisions()



    def _check_bullet_alien_collisions(self):
        #Respond to bullet alien collission 
        #remove both aliens and bullets after collision 
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True,True) 

        if not self.aliens:
            #Destroy existing bullets and create new fleet. 
            self.bullets.empty()
            self._create_fleet()

    def _update_aliens(self):
        #Update the positions of all aliens in the fleet 
        #if at edge update positions 
        self._check_fleet_edges()
        self.aliens.update()

        #Look for alien-ship collisions.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit() #looks for collisions between sprites and and groups 
            print("SHIP HIT!!!!")

        self._check_aliens_bottom()

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()

        #returns a list of all sprites in the group bullets, to draw all fired bullets 
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()  
        self.aliens.draw(self.screen)
         #draw ship

        pygame.display.flip()         # Make the most recently drawn screen visible. 

    def _ship_hit(self):
        #Respond to the ship being hit by the alien 
        #decrements ships_left.
        self.stats.ships_left -= 1 # after a ship is hit the number of ships left reduced by 1 

        #Get rid of any remaining aliens and bullets 
        self.aliens.empty() # use this to reset the game 
        self.bullets.empty()

        #create a new fleet and center the ship 
        self._create_fleet() # positions the objects to begin 
        self.ship.center_ship()

        #pause
        sleep(0.5) #dramatic pause to assess hit 

    def _check_aliens_bottom(self):
        #check if any aliens have reached the bottom of the screen
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom: #1 checks by comparing aliens position to bottom of screen 
                #Treat this the same as if the ship got hit 
                self._ship_hit() #if true we call ship hit 
                break 

    def _create_fleet(self):
        # Create an alien and find the number of aliens in a row.
        # Spacing between each alien is equal to one alien width.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width) # determine space 
        number_aliens_x = available_space_x // (2 * alien_width) # determine no of aliens 

        #Determine the number of rows of aliens that fit on the screen.
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        #Create the full fleet of aliens.
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        #Create an alien and place it in the row."""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number # in the loop we create a new alien and set its x coordinate value to keep in row
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

        #Creates the fleet of aliens 
        #Makes an alien
        alien = Alien(self)
        self.aliens.add(alien)
    
    def _check_fleet_edges(self):
        #responds appropriately if any alien reaches an edge
        for alien in self.aliens.sprites(): #1 if check edges return true we know we are at an edge 
            if alien.check_edges():
                self._change_fleet_direction() #2 because we are at an edge we call change direction 
                break
    
    def _change_fleet_direction(self):
        #DROP the entire fleet and change the fleets direction 
        for alien in self.aliens.sprites(): # we loop through each alien and drop each one using drop_speed 
            alien.rect.y += self.settings.fleet_drop_speed #3 we multiply it by -1 to move it left 
        self.settings.fleet_direction *= -1 


    

if __name__ == '__main__':
    # Make a game instance, and run the game. 
    ai = AlienInvasion()
    ai.run_game()



