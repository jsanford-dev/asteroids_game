import pygame.font

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

    def show_score(self):
        """Draw score to the screen."""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.level_image, self.level_rect)
