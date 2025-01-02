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

def run_game():
    # Initialise the game, settings, and screen object.
    pygame.init()
    pygame.mixer.init()
    game_settings = Settings()
    screen = pygame.display.set_mode(
        (game_settings.screen_width, game_settings.screen_length)
    )
    pygame.display.set_caption("Asteroids")

    # Make a play button
    play_button = Button(game_settings, screen, "New Game")

    # Create an instance to store game stats.
    stats = GameStats(game_settings)

    # Initialise sound manager
    sound_manager = SoundManager()

    # Make a ship, group of bullets, and an asteroid
    bullets = Group()
    asteroids = Group()
    ship = None

    # Set up initial asteroids for start of game.
    def start_new_level():
        for _ in range(game_settings.initial_num_asteroids + game_settings.current_level - 1):
            Asteroid.create_asteroid(game_settings, screen, asteroids, ship)
    
    # Start the main the loop for the game.
    while True:
        gf.check_events(game_settings, stats, screen, sound_manager, play_button, ship, bullets)

        if stats.game_active and not game_settings.paused:
            if ship is None:
                ship = Ship(game_settings, screen)
                bullets.empty()
                asteroids.empty()
                start_new_level()
            
            if stats.waiting_for_respawn:
                if pygame.time.get_ticks() - stats.collision_timer < 2000:
                    asteroids.update()
                    gf.update_bullets(game_settings, sound_manager, bullets, asteroids)
                else:
                    safe_zone_center = (game_settings.screen_width / 2, game_settings.screen_length / 2)
                    safe_zone_radius = game_settings.ship_respawn_safe_zone_radius
                    stats.respawn_safe = gf.is_safe_zone_clear(asteroids, safe_zone_center, safe_zone_radius)

                    if stats.respawn_safe:
                        ship = Ship(game_settings, screen)
                        ship.centerx = game_settings.screen_width / 2
                        ship.centery = game_settings.screen_length / 2
                        ship.rect.center = (ship.centerx, ship.centery)
                        stats.waiting_for_respawn = False
            else:
                ship.update()
                asteroids.update()
                gf.update_bullets(game_settings, sound_manager, bullets, asteroids)
                gf.handle_ship_collisions(game_settings, stats, sound_manager, ship, bullets, asteroids)

                if len(asteroids) == 0:
                    game_settings.current_level += 1
                    start_new_level()
            
        gf.update_screen(game_settings, stats, screen, play_button, ship, bullets, asteroids)

if __name__ == '__main__':
    run_game()
