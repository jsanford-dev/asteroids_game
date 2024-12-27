import sys
import pygame
import math

from asteroids.bullet import Bullet

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

def check_keyup_events(event, ship):
    """Respond to key releases."""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
    elif event.key == pygame.K_UP:
        ship.moving_up = False

def update_screen(game_settings, screen, ship, bullets):
    """Update images on the screen and flip to the new screen."""
    # Redraw the screen during each pass through the loop.
    screen.fill(game_settings.bg_colour)

    for bullet in bullets.sprites():
        bullet.draw_bullet()

    ship.blitme()

    # Make the most recently drawn screen visable.
    pygame.display.flip()

def update_bullets(game_settings, bullets):
    """Update positions of bullets and handle their lifecycle."""
    bullets.update()

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