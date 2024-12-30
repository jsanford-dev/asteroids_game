import random
import math

import pygame
from pygame.sprite import Sprite

class Asteroid(Sprite):
    """A class to represent a single asteriod."""
    def __init__(self, game_settings, screen):
        """Initialise the asteroid."""
        super().__init__()
        self.screen = screen
        self.game_settings = game_settings

        # Load the asteroid image and set its rect attribute.
        self.image = pygame.image.load('assets/images/asteroid.bmp')
        self.rect = self.image.get_rect()

        # Store asteroids exact postion as floats for precision.
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        # Randomise velocity for straight-line movement.
        angle = random.uniform(0, 2 * math.pi)
        self.velocity_x = game_settings.asteroid_speed * math.cos(angle)
        self.velocity_y = game_settings.asteroid_speed * math.sin(angle)

    def update(self):
        """Update the asteroid's postion based on it's velocity."""
        self.x += self.velocity_x
        self.y += self.velocity_y

        if self.x < -self.rect.width:
            self.x = self.game_settings.screen_width
        elif self.x > self.game_settings.screen_width:
            self.x = -self.rect.width

        if self.y < -self.rect.height:
            self.y = self.game_settings.screen_length
        elif self.y > self.game_settings.screen_length:
            self.y = -self.rect.height

        # Update the rect postion
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

    def blitme(self):
        """Draw the alien at it's current location."""
        self.screen.blit(self.image, self.rect)