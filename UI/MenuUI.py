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
    background = pygame.image.load("Art/lobby3_bg.png")
    background = pygame.transform.scale(background, (Settings.screen_width, Settings.screen_height))
    title = pygame.image.load("Art/logo_small.png")
    # title = pygame.transform.scale(title, (250, 80))
    settings_icon = pygame.image.load("Art/settings.png")  # TODO implement functionality to adjust various settings
    sound_icon = pygame.image.load("Art/sound.png")
    sound_icon_off = pygame.image.load("Art/sound_off.png")
    button1_glow = pygame.image.load("Art/start_glow.png")
    button2_glow = pygame.image.load("Art/quit_glow.png")
    # screen = pygame.display.set_mode((Settings.screen_width, Settings.screen_height))
    font = pygame.font.SysFont('arialbold', 30)

    # Sound
    mixer.music.load('Sound/background.wav')

    is_running = False

    def __init__(self, screen, controller):

        self.screen = screen
        self.controller = controller
        # Sound button
        self.sound_rect = self.sound_icon.get_rect(topleft=(75, 430))
        # Settings button
        self.settings_rect = self.settings_icon.get_rect(topleft=(15, 430))
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
        # while self.is_running:
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
                sys.exit(0)
            elif event.type == pygame.KEYDOWN and event.type == pygame.K_q:
                sys.exit(0)
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
                # Exit button
                elif self.button_2.collidepoint(mouse_pos):
                    sys.exit(0)
                # Start button
                elif self.button_1.collidepoint(mouse_pos):
                    # Swap to game
                    self.controller.game.is_running = True
                    # self.controller.menuUI.is_running = False
                    self.is_running = False

    def update(self):
        True  # Placeholder

    def render(self):
        # Clear screen
        self.screen.fill((0, 0, 0))
        # Background
        self.screen.blit(self.background, (0, 0))
        # Title
        self.screen.blit(self.title, (self.screen.get_width()/2 - self.title.get_width()/2, self.screen.get_height()/10))
        # Settings
        self.screen.blit(self.settings_icon, (15, 430))
        # Mute toggle
        if Settings.sound_muted:
            self.screen.blit(self.sound_icon_off, (75, 430))
        else:
            self.screen.blit(self.sound_icon, (75, 430))
        # Start and Exit buttons
        pygame.draw.rect(self.screen, Colours.CYAN, self.button_1)
        pygame.draw.rect(self.screen, Colours.PINK, self.button_2)
        draw_text('START', self.font, Colours.WHITE, self.screen, self.button_1.x + 18, self.button_1.y + 10)
        draw_text('QUIT', self.font, Colours.WHITE, self.screen, self.button_2.x + 25, self.button_2.y + 10)
        if self.button_1.collidepoint(pygame.mouse.get_pos()):
            self.screen.blit(self.button1_glow, (225, 145))
        if self.button_2.collidepoint(pygame.mouse.get_pos()):
            self.screen.blit(self.button2_glow, (365, 145))
        # Show new frame
        pygame.display.flip()


# Helper function
def draw_text(text, font, color, surface, x, y):
    text_object = font.render(text, 1, color)
    text_rect = text_object.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_object, text_rect)
