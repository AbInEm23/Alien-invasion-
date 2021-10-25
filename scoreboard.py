import pygame.font
from pygame.sprite import Group

from ship import Ship

class Scoreboard:
    """A class to report scoring information."""

    def __init__(self, ai_game):
        """Initialize scorekeeping attributes.""" # gives access to screen, settings, stats 
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats
        
        # Font settings for scoring information.
        self.text_color = (30, 30, 30) # set text color 
        self.font = pygame.font.SysFont(None, 48) # instantiate font object 

        # Prepare the initial score images.
        self.prep_score() #4
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        """Turn the score into a rendered image."""
    
        rounded_score = round(self.stats.score, -1) # rounds scores
        score_str = "{:,}".format(rounded_score) # Turns to string and passed to render 
        self.score_image = self.font.render(score_str, True,self.text_color, self.settings.bg_color) # to display clearly we pass the color of background and text 

        # Display the score at the top right of the screen.
        self.score_rect = self.score_image.get_rect() #3
        self.score_rect.right = self.screen_rect.right - 20 # set its right edge 20 pixels from the right edge of the screen
        self.score_rect.top = 20 # We then place the top edge 20 pixels down from the top of the screen

    def show_score(self):
        """Draw scores and level to the screen."""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)

    def prep_high_score(self):
        """Turn the high score into a rendered image."""
        high_score = round(self.stats.high_score, -1) #round the highscore and format it 
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.settings.bg_color) #render image 

        # Center the high score at the top of the screen.
        self.high_score_rect = self.high_score_image.get_rect() 
        self.high_score_rect.centerx = self.screen_rect.centerx #center image 
        self.high_score_rect.top = self.score_rect.top # set its top attribute to match the top of the score image

    def check_high_score(self):
        """Check to see if there's a new high score."""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()

    def prep_level(self):
        """Turn the level into a rendered image."""
        level_str = str(self.stats.level)
        self.level_image = self.font.render(level_str, True,self.text_color, self.settings.bg_color) # creates level 

        # Position the level below the score.
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right 
        self.level_rect.top = self.score_rect.bottom + 10 # leaves space between score and level 

    def prep_ships(self):
        """Show how many ships are left."""
        self.ships = Group() # creates empty group to hold ships 
        for ship_number in range(self.stats.ships_left): # loop that fills group
            ship = Ship(self.ai_game)
            ship.rect.x = 10 + ship_number * ship.rect.width # set ships to apperar next to each other with space 
            ship.rect.y = 10 #set ships at top left 
            self.ships.add(ship) #then add ship to group 