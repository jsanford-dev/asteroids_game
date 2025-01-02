import pygame.font

class Button():
    def __init__(self, game_settings, screen, msg):
        """Initialise button attributes"""
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # Button Properties
        self.width, self.height = 200, 50
        self.button_colour = (0, 0, 0)
        self.text_colour = (0, 205, 0)
        self.font = pygame.font.SysFont(None, 48)

        self.rect = pygame.Rect(0, 0 , self.width, self.height)
        self.rect.center = self.screen_rect.center

        self.prep_msg(msg)

    def prep_msg(self, msg):
        """Turn msg into a rendered image and center text on the button."""
        self.msg_image = self.font.render(msg, True, self.text_colour, 
                                          self.button_colour)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        # Draw blank button and then draw message/
        self.screen.fill(self.button_colour, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)