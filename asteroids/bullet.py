import pygame
from pygame.sprite import Sprite
import math

class Bullet(Sprite):
    """A class to manage bullets fired from the ship."""

    def __init__(self, game_settings, screen, ship):
        """Create a bullet object at the ship's current position."""
        super().__init__()
        self.screen = screen

        # Create a bullet rect at (0, 0) and then set the current position.
        self.rect = pygame.Rect(0, 0, game_settings.bullet_width,
                                game_settings.bullet_height)
        self.rect.center = ship.rect.center  # Start bullet at the ship's position

        # Store the bullet's position as decimal values for precision.
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        # Store the angle of the ship when the bullet is fired
        self.angle = ship.angle

        # Bullet properties
        self.colour = game_settings.bullet_colour
        self.speed_factor = game_settings.bullet_speed_factor

        # Track the bullet's initial position for travel distance.
        self.start_x = self.x
        self.start_y = self.y

    def update(self):
        """Move the bullet in the direction of the ship's angle."""
        # Convert the angle to radians
        radians = math.radians(self.angle)

        # Calculate the movement for both x and y components
        dx = math.sin(radians) * self.speed_factor
        dy = -math.cos(radians) * self.speed_factor  # Negative for Pygame's y-axis

        # Update the bullet's position
        self.x -= dx
        self.y += dy

        # Update the rect position
        self.rect.x = self.x
        self.rect.y = self.y

    def draw_bullet(self):
        """Draw the bullet to the screen."""
        pygame.draw.rect(self.screen, self.colour, self.rect)