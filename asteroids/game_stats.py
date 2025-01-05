class GameStats():
    """Track statistics for Asteroids."""
    def __init__(self, game_settings):
        """Initialise statistics."""
        self.game_settings = game_settings
        self.reset_stats()
        self.game_active = False
        self.collision_timer = 0

    def reset_stats(self):
        """Initialise statistics that can change during the game."""
        self.ships_left = self.game_settings.ship_limit
        self.waiting_for_respawn = False
        self.respawn_safe = False
        self.collision_timer = 0
        self.score = 0