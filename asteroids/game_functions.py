import sys
import pygame
import math
from time import sleep

from asteroids.ship import Ship
from asteroids.bullet import Bullet
from asteroids.asteroid import Asteroid

# Handle user actions
def check_events(game_settings, stats, screen, sound_manager, play_button, ship, bullets):
    """ Respond to keypresses and mouse events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, game_settings, screen, sound_manager, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(stats, play_button, mouse_x, mouse_y)

def check_play_button(stats, play_button, mouse_x, mouse_y):
    """Start new game when the player clicks 'New Game.'"""
    if play_button.rect.collidepoint(mouse_x, mouse_y):
        stats.game_active = True

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

def update_screen(game_settings, stats, screen, play_button, ship, bullets, asteroid):
    """Update images on the screen and flip to the new screen."""

    screen.fill(game_settings.bg_colour)

    for bullet in bullets.sprites():
        bullet.draw_bullet()

    if ship is not None and not stats.waiting_for_respawn:
        ship.blitme()

    asteroid.draw(screen)

    # Draw the play button if the game is inactive
    if not stats.game_active:
        play_button.draw_button()

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
            stats.waiting_for_respawn = True
            stats.respawn_safe = False
            stats.collision_timer = pygame.time.get_ticks()
        else:
            stats.game_active = False

def is_safe_zone_clear(asteroids, center, radius):
    """ Check if the safe zone around reswapn is clear of asteroids."""
    for asteroid in asteroids:
        dx = asteroid.rect.centerx - center[0]
        dy = asteroid.rect.centery - center[1]
        distance = math.sqrt(dx ** 2 + dy ** 2)
        if distance < radius:
            return False
    return True

def start_new_level(game_settings, screen, asteroids, ship):
    """Start new level by creating asteroids."""
    for _ in range(game_settings.initial_num_asteroids + game_settings.current_level - 1):
        Asteroid.create_asteroid(game_settings, screen, asteroids, ship)

def handle_respawn(stats, asteroids, ship, game_settings, screen):
    """Handle ship respawn after a collision."""
    if pygame.time.get_ticks() - stats.collision_timer < 2000:
        asteroids.update()
    else:
        safe_zone_center = (game_settings.screen_width / 2, game_settings.screen_length / 2)
        safe_zone_radius = game_settings.ship_respawn_safe_zone_radius
        stats.respawn_safe = is_safe_zone_clear(asteroids, safe_zone_center, safe_zone_radius)
        asteroids.update()

        if stats.respawn_safe:
            ship = Ship(game_settings, screen)
            ship.centerx = game_settings.screen_width / 2
            ship.centery = game_settings.screen_length / 2
            ship.rect.center = (ship.centerx, ship.centery)
            stats.waiting_for_respawn = False
        
    return ship
        

