class Settings:
    """A class to store all settings for Alien invasion"""
    def __init__(self):
        #initialize games static settings
        #sscreen settings 
        self.screen_width = 1200 # define dimensions of the game window 
        self.screen_height = 800
        self.bg_color = (230,230,230) #background color 

        #ship settings
        #self.ship_speed = 1.5
        self.ship_limit = 3

        #Bullet settings 
        #self.bullet_speed = 1.5
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (255,0,0)
        self.bullets_allowed = 5

        #Alien settings
        #self.alien_speed = 1.0
        self.fleet_drop_speed = 10

        #how quickly the game speeds up 
        self.speedup_scale = 1.1

        # How quickly the alien point values increase
        self.score_scale = 1.5

        self.initialize_dynamic_settings()
        #fleet_direction of 1 represents right; -1 represent left 
        #self.fleet_direction = 1

    def initialize_dynamic_settings(self):
        #initialize settings throughout the game 
        self.ship_speed = 1.5
        self.bullet_speed = 3.0
        self.alien_speed = 1.0 

        #fleet_direction of 1 represents right; -1 represents left. 
        self.fleet_direction = 1 

        #scoring 
        self.alien_points = 50

    def increase_speed(self):
        #increases speed settings and alien point values 
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale # to increase the speed we multiply each speed by the speedup scale 
        self.alien_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)
        print(self.alien_points)