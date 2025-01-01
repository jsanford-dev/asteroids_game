import sys
import pygame
from pygame.sprite import Group

from asteroids.settings import Settings
from asteroids.game_stats import GameStats
from asteroids.sound_manager import SoundManager
from asteroids.ship import Ship
from asteroids.asteroid import Asteroid

import asteroids.game_functions as gf

def run_game():
    # Initialise the game, settings, and screen object.
    pygame.init()
    pygame.mixer.init()
    game_settings = Settings()
    screen = pygame.display.set_mode(
        (game_settings.screen_width, game_settings.screen_length)
    )
    pygame.display.set_caption("Asteroids")

    # Create an instance to store game stats.
    stats = GameStats(game_settings)

    # Initialise sound manager
    sound_manager = SoundManager()

    # Make a ship, group of bullets, and an asteroid
    ship = Ship(game_settings, screen)
    bullets = Group()
    asteroids = Group()

    # Set up initial asteroids for start of game.
    def start_new_level():
        for _ in range(game_settings.initial_num_asteroids + game_settings.current_level - 1):
            Asteroid.create_asteroid(game_settings, screen, asteroids, ship)

    start_new_level()
    
    # Start the main the loop for the game.
    while True:
        gf.check_events(game_settings, screen, sound_manager, ship, bullets)

        if stats.game_active and not game_settings.paused:
            ship.update()
            asteroids.update()
            gf.update_bullets(game_settings, sound_manager, bullets, asteroids)
            gf.handle_ship_collisions(game_settings, stats, sound_manager, ship, bullets, asteroids)

            if len(asteroids) == 0:
                game_settings.current_level += 1
                start_new_level()
            
        gf.update_screen(game_settings, screen, ship, bullets, asteroids)

if __name__ == '__main__':
    run_game()
