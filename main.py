import sys
import pygame
from pygame.sprite import Group

from asteroids.settings import Settings
from asteroids.game_stats import GameStats
from asteroids.play_button import Button
from asteroids.sound_manager import SoundManager
from asteroids.ship import Ship
from asteroids.asteroid import Asteroid
import asteroids.game_functions as gf

def initilise_game():
    """Initialise game components and return them."""
    pygame.init()
    pygame.mixer.init()
    game_settings = Settings()
    screen = pygame.display.set_mode(
        (game_settings.screen_width, game_settings.screen_length)
    )
    pygame.display.set_caption("Asteroids")

    play_button = Button(game_settings, screen, "New Game")
    stats = GameStats(game_settings)
    sound_manager = SoundManager()
    bullets = Group()
    asteroids = Group()
    ship = None

    return game_settings, screen, play_button, stats, sound_manager, bullets, asteroids, ship

def run_game():
    # Initialise the game
    (
        game_settings, screen, play_button, stats,
        sound_manager, bullets, asteroids, ship
    ) = initilise_game()

    while True:
        gf.check_events(game_settings, stats, screen, sound_manager, play_button, ship, bullets)

        if stats.game_active and not game_settings.paused:
            if ship is None:
                ship = Ship(game_settings, screen)
                bullets.empty()
                asteroids.empty()
                gf.start_new_level(game_settings, screen, asteroids, ship)

            if stats.waiting_for_respawn:
                ship = gf.handle_respawn(stats, asteroids, ship, game_settings, screen)
            else:
                # Update game objects
                ship.update()
                asteroids.update()
                gf.update_bullets(game_settings, sound_manager, bullets, asteroids)
                gf.handle_ship_collisions(game_settings, stats, sound_manager, ship, bullets, asteroids)

                # Check if level is cleared
                if len(asteroids) == 0:
                    game_settings.current_level += 1
                    gf.start_new_level(game_settings, screen, asteroids, ship)

        # Render the updated screen
        gf.update_screen(game_settings, stats, screen, play_button, ship, bullets, asteroids)

if __name__ == '__main__':
    run_game()