class Settings():
    """ A class to store all settings for Asteroids."""

    def __init__(self):
        """ Initialise the game's settings."""
        # Screen settings.
        self.screen_width = 800
        self.screen_length = 600
        self.bg_colour = (0, 0, 0) # Background colour.

        # Ship settings.
        self.ship_speed_factor = 0.25
        self.rotation_speed = 0.15
        self.ship_scale = 0.5
        self.ship_limit = 3

        # Bullet settings.
        self.bullet_speed_factor = 1
        self.bullet_width = 5
        self.bullet_height = 5
        self.bullet_colour = 0, 205, 0
        self.bullets_allowed = 3
        self.max_bullet_distance = 400

        # Asteroid settings.
        self.asteroid_speed = 0.1
        self.initial_num_asteroids = 4
        self.current_level = 1
