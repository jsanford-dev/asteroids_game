import sys
import pygame
from pygame.sprite import Group

from asteroids.settings import Settings
from asteroids.ship import Ship

import asteroids.game_functions as gf

def run_game():
    # Initialise the game, settings, and screen object.
    pygame.init()
    game_settings = Settings()
    screen = pygame.display.set_mode(
        (game_settings.screen_width, game_settings.screen_length)
    )
    pygame.display.set_caption("Asteriods")

    # Make a ship
    ship = Ship(game_settings, screen)
    bullets = Group()

    # Start the main the loop for the game.
    while True:
        gf.check_events(game_settings, screen, ship, bullets)
        ship.update()
        gf.update_bullets(game_settings, bullets)
        gf.update_screen(game_settings, screen, ship, bullets)

if __name__ == '__main__':
    run_game()
