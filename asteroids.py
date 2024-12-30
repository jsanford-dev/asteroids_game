import sys
import pygame
from pygame.sprite import Group

from asteroids.settings import Settings
from asteroids.sound_manager import SoundManager
from asteroids.ship import Ship
from asteroids.asteroid_target import Asteroid

import asteroids.game_functions as gf

def run_game():
    # Initialise the game, settings, and screen object.
    pygame.init()
    pygame.mixer.init()
    game_settings = Settings()
    screen = pygame.display.set_mode(
        (game_settings.screen_width, game_settings.screen_length)
    )
    pygame.display.set_caption("Asteriods")

    # Initialise sound manager
    sound_manager = SoundManager()

    # Make a ship, group of bullets, and an asteroid
    ship = Ship(game_settings, screen)
    bullets = Group()
    asteroids = Group()

    gf.create_asteroid(game_settings, screen, asteroids)

    # Start the main the loop for the game.
    while True:
        gf.check_events(game_settings, screen, sound_manager, ship, bullets)
        ship.update()
        asteroids.update()
        gf.update_bullets(game_settings, sound_manager, bullets, asteroids)
        gf.update_screen(game_settings, screen, ship, bullets, asteroids)

if __name__ == '__main__':
    run_game()
