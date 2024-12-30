import pygame

class SoundManager:
    """A class to manage game sounds."""

    def __init__(self):
        """Initialise the mixer and load sounds."""
        pygame.mixer.init()
        self.sounds = {
            "bullet": pygame.mixer.Sound('assets/audio/bullet.wav'),
            "explosion": pygame.mixer.Sound('assets/audio/explosion.wav'),
            # Add other sounds here.
        }

    def play_sound(self, sound_name):
        """Play a sound by name."""
        if sound_name in self.sounds:
            self.sounds[sound_name].play()
        else:
            print(f"Sound '{sound_name}' not found.")