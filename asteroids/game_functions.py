import sys
from time import sleep
import pygame
import math

from asteroids.bullet import Bullet
from asteroids.asteroid import Asteroid

# Handle user actions
def check_events(game_settings, screen, sound_manager, ship, bullets):
    """ Respond to keypresses and mouse events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, game_settings, screen, sound_manager, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)

def check_keydown_events(event, game_settings, screen, sound_manager, ship, bullets):
    """Respond to keypresses."""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_UP:
        ship.moving_up = True
    elif event.key == pygame.K_SPACE:
        if len(bullets) < game_settings.bullets_allowed:
            new_bullet = Bullet(game_settings, screen, ship)
            bullets.add(new_bullet)
            sound_manager.play_sound('bullet')
    elif event.key == pygame.K_p:
        game_settings.paused = not game_settings.paused

def check_keyup_events(event, ship):
    """Respond to key releases."""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
    elif event.key == pygame.K_UP:
        ship.moving_up = False

def update_screen(game_settings, screen, ship, bullets, asteroid):
    """Update images on the screen and flip to the new screen."""

    screen.fill(game_settings.bg_colour)

    for bullet in bullets.sprites():
        bullet.draw_bullet()

    ship.blitme()
    asteroid.draw(screen)

    pygame.display.flip()

# Handle bullets
def update_bullets(game_settings, sound_manager, bullets, asteroid):
    """Update bullets and handle collisions."""
    bullets.update()
    handle_bullet_removal(game_settings, bullets)
    handle_bullet_collisions(sound_manager, bullets, asteroid)

def handle_bullet_removal(game_settings, bullets):
    """Handle bullets that exceed distance or go out of bounds."""
    for bullet in bullets.copy():
        # Update the distance traveled
        dx = bullet.x - bullet.start_x
        dy = bullet.y - bullet.start_y
        total_distance = math.sqrt(dx ** 2 + dy ** 2)

        # Remove the bullet if it has traveled beyond the maximum allowed distance
        if total_distance >= game_settings.max_bullet_distance:
            bullets.remove(bullet)
            continue

        # Wrap the bullet position if it moves out of bounds
        if bullet.x > game_settings.screen_width:
            bullet.x = bullet.x - game_settings.screen_width
            bullet.start_x = bullet.start_x - game_settings.screen_width
        elif bullet.x < 0:
            bullet.x = bullet.x + game_settings.screen_width
            bullet.start_x = bullet.start_x + game_settings.screen_width

        if bullet.y > game_settings.screen_length:
            bullet.y = bullet.y - game_settings.screen_length
            bullet.start_y = bullet.start_y - game_settings.screen_length
        elif bullet.y < 0:
            bullet.y = bullet.y + game_settings.screen_length
            bullet.start_y = bullet.start_y + game_settings.screen_length

        # Update the bullet's rect position after wrapping
        bullet.rect.centerx = bullet.x
        bullet.rect.centery = bullet.y

def handle_bullet_collisions(sound_manager, bullets, asteroids):
    """Check for and handle collisions between bullets and asteroids."""
    collisions = pygame.sprite.groupcollide(bullets, asteroids, True, True)
    if collisions:
        sound_manager.play_sound('explosion')

# Handle ship
def handle_ship_collisions(game_settings, stats, sound_manager, ship, bullets, asteroids):
    """Check for and handle collisions between ship and asteroids."""
    collided_asteroid = pygame.sprite.spritecollideany(ship, asteroids)
    if collided_asteroid:
        sound_manager.play_sound('explosion')
        asteroids.remove(collided_asteroid)
        bullets.empty()

        if stats.ships_left > 0:
            # Decrement ships left
            stats.ships_left -= 1

            # Pause
            sleep(0.5)
            
            # Recenter the ship to middle of screen
            ship.centerx = game_settings.screen_width / 2
            ship.centery = game_settings.screen_length / 2
            ship.rect.center = (ship.centerx, ship.centery)

        else:
            stats.game_active = False



        

