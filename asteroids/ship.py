import pygame
import math

class Ship():
    def __init__(self, game_settings, screen):
        """ Initialise the ship and set its starting position."""
        self.screen = screen
        self.game_settings = game_settings

        # Load the ship image and get its rect.
        self.image = pygame.image.load('assets/images/ship.bmp')
        self.original_image = pygame.transform.scale(self.image, (
            int(self.image.get_width() * self.game_settings.ship_scale),
            int(self.image.get_height() * self.game_settings.ship_scale)
        ))
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # Start each new ship in the center of the screen.
        self.rect.center = self.screen_rect.center

        # Store a decimal value for the ships center
        self.centerx = float(self.rect.centerx)
        self.centery = float(self.rect.centery)

        # Movement flag
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False

        # Rotation angle
        self.angle = 0

    def update(self):
        """ Update the ship's position and handle screen wrapping."""
        # Update horizontal movement (x-axis)
        if self.moving_right:
            self.angle -= self.game_settings.rotation_speed
        if self.moving_left:
            self.angle += self.game_settings.rotation_speed

        # Normalise the angle of ship keep between 0 and 360
        self.angle %= 360

        # Update vertical movement (y-axis) and adjust ship direction
        if self.moving_up:
            radians = math.radians(self.angle)
            dx = math.sin(radians) * self.game_settings.ship_speed_factor
            dy = -math.cos(radians) * self.game_settings.ship_speed_factor

            self.centerx -= dx
            self.centery += dy

        # Handle screen wrapping horizontally
        if self.rect.right < 0:
            self.centerx = self.screen_rect.right
        elif self.rect.left > self.screen_rect.right:
            self.centerx = 0

        # Handle screen wrapping vertically
        if self.rect.bottom < 0:
            self.centery = self.screen_rect.bottom
        elif self.rect.top > self.screen_rect.bottom:
            self.centery = 0

        # Update rect object from self.centerx and self.centery
        self.rect.centerx = self.centerx
        self.rect.centery = self.centery

    def blitme(self):
        """ Draw the ship at the current location."""
        rotated_image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = rotated_image.get_rect(center=self.rect.center)
        self.screen.blit(rotated_image, self.rect)
