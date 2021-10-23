class GameStats:
    #Track stats for AI

    def __init__(self, ai_game):
        #initialize stats
        self.settings = ai_game.settings
        self.reset_stats()

        #start alien invasion in inactive state 
        self.game_active = False

    def reset_stats(self):
        #Initialize statistics that can change during the game
        self.ships_left = self.settings.ship_limit