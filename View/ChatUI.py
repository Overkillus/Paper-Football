import pygame, sys
import numpy

pygame.init()


class ChatUI:

    # Art
    # temporary chat image/icon
    chat_icon = pygame.image.load("Art/question_black.png")
    background = (0, 0, 0)

    font = pygame.font.SysFont('arialbold', 30)

    def __init__(self, controller):
        # State
        self.is_running = False

        # Context
        self.screen = controller.screen
        self.controller = controller

        # Buttons
        button_x = 325
        button_y = 320
        button_w = self.chat_icon.get_width()
        button_h = self.chat_icon.get_height()

        self.chat_button = pygame.Rect(button_x, button_y, button_w, button_h)

    def main(self):
        self.event_handler()
        self.render()

    def event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.type == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_pos = pygame.mouse.get_pos()
                if self.chat_button.collidepoint(mouse_pos):
                    ...

    def render(self):
        # Clear screen
        self.screen.fill((0, 0, 0))

        # Background
        self.screen.blit(self.background, (0, 0))
        self.draw_text('Chat', self.font, (255, 255, 255), self.screen, 300, 30)
        self.screen.blit(self.chat_button, (325, 320, self.chat_icon.get_width(), self.chat_icon.get_height()))

    def draw_text(text, font, color, surface, x, y):
        text_object = font.render(text, 1, color)
        text_rect = text_object.get_rect()
        text_rect.topleft = (x, y)
        surface.blit(text_object, text_rect)