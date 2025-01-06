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
        
        # Screen wrapping logic
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
        """Draw the asteroid at it's current location."""
        self.screen.blit(self.image, self.rect)

    @staticmethod
    def create_asteroid(game_settings, screen, asteroids, ship):
        """Create an asteroid ensuring that it does not spawn near the ship."""
        while True:
            # Generate asteroid
            asteroid = Asteroid(game_settings, screen)
            asteroid.rect.x = random.randint(0, game_settings.screen_width - asteroid.rect.width)
            asteroid.rect.y = random.randint(0, game_settings.screen_length - asteroid.rect.height)
            asteroid.x = float(asteroid.rect.x)
            asteroid.y = float(asteroid.rect.y)

            # Check distance from the ship
            if ship:
                dx = asteroid.rect.centerx - ship.rect.centerx
                dy = asteroid.rect.centery - ship.rect.centery
                distance = math.sqrt(dx ** 2 + dy ** 2)
                                    
                if distance > game_settings.asteroid_respawn_safe_radius:
                    asteroids.add(asteroid)
                    break
            else:
                asteroids.add(asteroids)
                break