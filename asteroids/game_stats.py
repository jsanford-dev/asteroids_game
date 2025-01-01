class GameStats():
    """Track statistics for Asteroids."""
    def __init__(self, game_settings):
        """Initialise statistics."""
        self.game_settings = game_settings
        self.reset_stats()
        self.game_active = True

    def reset_stats(self):
        """Initialise statistics that can change during the game."""
        self.ships_left = self.game_settings.ship_limit