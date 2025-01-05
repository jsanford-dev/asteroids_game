import pygame.font
from pygame.sprite import Group

from asteroids.ship import Ship

class Scoreboard():
    """A class to report scoring information."""
    def __init__(self, game_settings, screen, stats):
        """Initialise scorekeeping attributes."""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.game_settings = game_settings
        self.stats = stats

        # Font settings for scoring information
        self.text_colour = (0, 205, 0)
        self.font = pygame.font.SysFont(None, 48)

        # Prepare the initial images
        self.prep_score()
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        """Turn the score into a rendered image."""
        score_str = f"Score: {self.stats.score}"
        self.score_image = self.font.render(score_str, True, self.text_colour,
                                            self.game_settings.bg_colour)
        
        # Display the score at the top right of the screen.
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_level(self):
        """Turn the level into a rendered image."""
        level_str = f"Level: {self.game_settings.current_level}"
        self.level_image = self.font.render(level_str, True,
                            self.text_colour, self.game_settings.bg_colour)
        
        # Position the level below the score
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        """Show how many ships are left."""
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.game_settings, self.screen)

            scaled_image = ship.original_image
            ship.rect = scaled_image.get_rect()

            # Position the ships on the scoreboard
            ship.rect.x = 10 + ship_number * (ship.rect.width + 10)  # Add spacing
            ship.rect.y = 20

            # Create a new sprite with the scaled image
            ship.image = scaled_image
            self.ships.add(ship)

    def show_score(self):
        """Draw score, items and lives to the screen."""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)

