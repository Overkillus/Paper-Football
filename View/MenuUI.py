import sys
import pygame
import Colours
from pygame import mixer
import Settings
# import tkinter as tk  # tkinter is used for GUI. Probably will have to use it at some point for any input

pygame.init()


class MenuUI:
    """
    Class representing menu view
    """

    # Art
    background = pygame.image.load("Art/lobby.png")
    title = pygame.image.load("Art/logo_small.png")
    settings_icon = pygame.image.load("Art/settings.png")
    sound_icon = pygame.image.load("Art/sound.png")
    sound_icon_off = pygame.image.load("Art/sound_off.png")
    button1_glow = pygame.image.load("Art/start_glow.png")
    button2_glow = pygame.image.load("Art/quit_glow.png")
    credits = pygame.image.load("Art/credits.png")
    credits_button = pygame.image.load("Art/credits_button.png")
    font = pygame.font.SysFont('arialbold', 30)

    # Sound
    mixer.music.load('Sound/background.wav')

    def __init__(self, controller):
        # State
        self.is_running = False

        # Context
        self.screen = controller.screen
        self.controller = controller

        # Sound button
        self.sound_rect = self.sound_icon.get_rect()
        # Settings button
        self.settings_rect = self.settings_icon.get_rect()
        # Credits
        self.credits_rect = self.credits.get_rect()
        # Credits button
        self.credits_button_rect = self.credits_button.get_rect()

        # Start and exit buttons
        button_w = 100
        button_h = 40
        button_y = 150
        button_x = 230
        self.button_1 = pygame.Rect(button_x, button_y, button_w, button_h)
        self.button_2 = pygame.Rect(button_x + 140, button_y, button_w, button_h)

        # Initiating sound
        if not Settings.sound_muted:
            mixer.music.play(-1)
            mixer.music.set_volume(Settings.sound_volume)

    def main(self):
        self.event_handler()
        # Ticking
        self.controller.delta_time += self.controller.clock.tick() / 1000.0
        while self.controller.delta_time > 1 / Settings.max_tps:
            self.controller.delta_time -= 1 / Settings.max_tps
            self.update()
            self.render()

    def event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.controller.close_game()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                self.controller.close_game()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_l:
                self.controller.change_view(self.controller.lobbyUI)
            # Mouse click
            elif event.type == pygame.MOUSEBUTTONUP:
                # Mouse click details
                mouse_pos = pygame.mouse.get_pos()
                # Toggle mute
                if self.sound_rect.collidepoint(mouse_pos) and Settings.sound_muted:
                    Settings.sound_muted = False
                    mixer.music.unpause()
                elif self.sound_rect.collidepoint(mouse_pos) and not Settings.sound_muted:
                    Settings.sound_muted = True
                    mixer.music.pause()
                # Open settings
                elif self.settings_rect.collidepoint(mouse_pos):
                    self.controller.change_view(self.controller.settingsUI)
                # Open Credits
                elif self.credits_button_rect.collidepoint(mouse_pos):
                    self.controller.change_view(self.controller.creditsUI)
                # Exit button
                elif self.button_2.collidepoint(mouse_pos):
                    self.controller.close_game()
                # Start button
                elif self.button_1.collidepoint(mouse_pos):
                    # Ensure connection, host server, join hosted server
                    if not self.controller.client.connected:
                        self.controller.client.start()
                        if self.controller.client.connected:
                            self.controller.client.quick_join()
                    # Swap to game
                    if self.controller.client.connected:
                        self.controller.change_view(self.controller.gameUI)

    def update(self):
        # Layout helper variables
        sw = self.screen.get_width()
        sh = self.screen.get_height()

        # Settings
        self.settings_rect.center = (40, sh-40)
        # Sound mute
        self.sound_rect.center = (100, sh-40)
        # Buttons (start/exit)
        self.button_1.center = (sw/2 - self.button_1.width, sh/3)
        self.button_2.center = (sw/2 + self.button_2.width, sh/3)
        # Credits
        self.credits_rect.bottomright = (sw - 20, sh-20)
        # Credits button
        self.credits_button_rect.topleft = (self.sound_rect.x + 60, self.sound_rect.y)


    def render(self):
        # Layout helper variables
        sw = self.screen.get_width()
        sh = self.screen.get_height()

        # Clear screen
        self.screen.fill((3, 15, 56))
        # Background image
        self.screen.blit(self.background,
                         (sw/2 - self.background.get_width()/2,
                          sh/2 - self.background.get_height()/2))
        # Title
        self.screen.blit(self.title,
                         (sw/2 - self.title.get_width()/2,
                          sh/10))
        # Settings
        self.screen.blit(self.settings_icon, self.settings_rect)
        # Credits
        self.screen.blit(self.credits, self.credits_rect)
        # Credits button
        self.screen.blit(self.credits_button, self.credits_button_rect)
        # Mute toggle
        if Settings.sound_muted:
            self.screen.blit(self.sound_icon_off, self.sound_rect)
        else:
            self.screen.blit(self.sound_icon, self.sound_rect)
        # Start and Exit buttons
        pygame.draw.rect(self.screen, Colours.CYAN, self.button_1)
        pygame.draw.rect(self.screen, Colours.PINK, self.button_2)
        draw_text('START', self.font, Colours.WHITE, self.screen, self.button_1.x + 18, self.button_1.y + 10)
        draw_text('QUIT', self.font, Colours.WHITE, self.screen, self.button_2.x + 25, self.button_2.y + 10)
        if self.button_1.collidepoint(pygame.mouse.get_pos()):
            self.screen.blit(self.button1_glow, (self.button_1[0]-5, self.button_1[1]-5))
        if self.button_2.collidepoint(pygame.mouse.get_pos()):
            self.screen.blit(self.button2_glow, (self.button_2[0]-5, self.button_2[1]-5))
        # Show new frame
        pygame.display.flip()

# Helper function
def draw_text(text, font, color, surface, x, y):
    text_object = font.render(text, 1, color)
    text_rect = text_object.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_object, text_rect)
