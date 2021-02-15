import sys
import pygame
import Settings
import Colours
from pygame import mixer
from tkinter import *

import tkinter.messagebox
from idlelib import statusbar


class SettingsUI:
    """
    Class representing settings ui
    """
    # Art
    background = pygame.image.load("Art/lobby_bg.png")
    background = pygame.transform.scale(background, (Settings.screen_width, Settings.screen_height))
    setting_icon = pygame.image.load("Art/settings.png")
    exitIcon = pygame.image.load('Art/exit2.png')
    default_screen = pygame.image.load('Art/default_b.png')
    default_screen_selected = pygame.image.load('Art/default_b_selected.png')
    medium_screen = pygame.image.load('Art/medium_screen_b.png')
    medium_screen_selected = pygame.image.load('Art/medium_screen_b_selected.png')
    large_screen = pygame.image.load('Art/large_screen_b.png')
    large_screen_selected = pygame.image.load('Art/large_screen_b_selected.png')
    football_theme = pygame.image.load('Art/football_b.png')
    football_theme_selected = pygame.image.load('Art/football_b_selected.png')
    neon_theme = pygame.image.load('Art/neon_b.png')
    neon_theme_selected = pygame.image.load('Art/neon_b_selected.png')
    paper_theme = pygame.image.load('Art/paper_b.png')
    paper_theme_selected = pygame.image.load('Art/paper_b_selected.png')
    small_board = pygame.image.load('Art/board_size_s.png')
    small_board_selected = pygame.image.load('Art/board_size_s_selected.png')
    medium_board = pygame.image.load('Art/board_size_m.png')
    medium_board_selected = pygame.image.load('Art/board_size_m_selected.png')
    sound_off = pygame.image.load('Art/sound_off.png')
    sound_reduce = pygame.image.load('Art/sound_reduce.png')
    sound_increase = pygame.image.load('Art/sound_increase.png')

    fontTitle = pygame.font.SysFont('arialbold', 45)
    font = pygame.font.SysFont('arialbold', 30)

    mixer.music.load('Sound/background.wav')

    def __init__(self, controller):
        # State
        self.is_running = False

        # Context
        self.screen = controller.screen
        self.controller = controller

        # Buttons
        button_x = 325
        button_y = 320
        button_w = 25
        button_h = 25
        self.yellow_button = pygame.Rect(button_x, button_y, button_w, button_h)
        self.yellow_button_selected = pygame.Rect(button_x-2.5, button_y-2.5, button_w+5, button_h+5)
        self.pink_button = pygame.Rect(button_x + 35, button_y, button_w, button_h)
        self.pink_button_selected = pygame.Rect(button_x + 35 - 2.5, button_y - 2.5, button_w + 5, button_h + 5)
        self.cyan_button = pygame.Rect(button_x + 35*2, button_y, button_w, button_h)
        self.cyan_button_selected = pygame.Rect(button_x + 35*2 - 2.5, button_y - 2.5, button_w + 5, button_h + 5)
        self.red_button = pygame.Rect(button_x + 35*3, button_y, button_w, button_h)
        self.red_button_selected = pygame.Rect(button_x + 35*3 - 2.5, button_y - 2.5, button_w + 5, button_h + 5)
        self.green_button = pygame.Rect(button_x + 35*4, button_y, button_w, button_h)
        self.green_button_selected = pygame.Rect(button_x + 35*4 - 2.5, button_y - 2.5, button_w + 5, button_h + 5)
        self.orange_button = pygame.Rect(button_x + 35*5, button_y, button_w, button_h)
        self.orange_button_selected = pygame.Rect(button_x + 35*5 - 2.5, button_y - 2.5, button_w + 5, button_h + 5)
        self.exit_button = pygame.Rect(15, 25, self.setting_icon.get_width(), self.setting_icon.get_height())
        self.default_screen_button = self.default_screen.get_rect()
        self.exit_rect = self.exitIcon.get_rect()
        self.medium_screen_button = self.medium_screen.get_rect()
        self.large_screen_button = self.large_screen.get_rect()
        self.football_theme_button = self.football_theme.get_rect()
        self.neon_theme_button = self.neon_theme.get_rect()
        self.paper_theme_button = self.paper_theme.get_rect()
        self.small_board_button = self.small_board.get_rect()
        self.medium_board_button = self.medium_board.get_rect()
        self.sound_off_button = self.sound_off.get_rect()
        self.sound_reduce_button = self.sound_reduce.get_rect()
        self.sound_increase_button = self.sound_increase.get_rect()
        self.sound_off_button = pygame.Rect(220, 385, self.sound_off.get_width(), self.sound_off.get_height())
        self.sound_reduce_button = pygame.Rect(270, 385, self.sound_reduce.get_width(), self.sound_reduce.get_height())
        self.sound_increase_button = pygame.Rect(320, 385, self.sound_increase.get_width(), self.sound_increase.get_height())

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
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.controller.change_view(self.controller.menuUI)
            elif event.type == pygame.MOUSEBUTTONUP:
                # Mouse click
                mouse_pos = pygame.mouse.get_pos()
                # Volume Control
                if self.sound_off_button.collidepoint(mouse_pos):
                    mixer.music.set_volume(0.0)
                elif self.sound_reduce_button.collidepoint(mouse_pos):
                    mixer.music.set_volume(0.1)
                elif self.sound_increase_button.collidepoint(mouse_pos):
                    mixer.music.set_volume(0.2)

                # Resolution Settings
                if self.default_screen_button.collidepoint(mouse_pos):
                    self.screen = pygame.display.set_mode((Settings.default_screen_width, Settings.default_screen_height), pygame.RESIZABLE)
                elif self.medium_screen_button.collidepoint(mouse_pos):
                    self.screen = pygame.display.set_mode((1366, 768))
                elif self.large_screen_button.collidepoint(mouse_pos):
                    # self.screen = pygame.display.set_mode((1920, 1080))
                    self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                    Settings.screen_width = pygame.display.get_window_size()[0]
                    Settings.screen_width = pygame.display.get_window_size()[1]
                # Theme Settings
                if self.football_theme_button.collidepoint(mouse_pos):
                    ...
                elif self.neon_theme_button.collidepoint(mouse_pos):
                    ...
                elif self.paper_theme_button.collidepoint(mouse_pos):
                    ...

                # Board settings
                if self.small_board_button.collidepoint(mouse_pos):
                    ...
                elif self.medium_board_button.collidepoint(mouse_pos):
                    ...

                # Colour Settings
                if self.yellow_button.collidepoint(mouse_pos):
                    self.controller.gameUI.players[0].set_color(Colours.YELLOW)
                elif self.pink_button.collidepoint(mouse_pos):
                    self.controller.gameUI.players[0].set_color(Colours.PINK)
                elif self.cyan_button.collidepoint(mouse_pos):
                    self.controller.gameUI.players[0].set_color(Colours.CYAN)
                elif self.red_button.collidepoint(mouse_pos):
                    self.controller.gameUI.players[0].set_color(Colours.RED)
                elif self.green_button.collidepoint(mouse_pos):
                    self.controller.gameUI.players[0].set_color(Colours.GREEN)
                elif self.orange_button.collidepoint(mouse_pos):
                    self.controller.gameUI.players[0].set_color(Colours.ORANGE)

                # Back button
                if self.exit_button.collidepoint(mouse_pos):
                    self.controller.change_view(self.controller.menuUI)

    def update(self):
        sw = self.screen.get_width()
        sh = self.screen.get_height()
        rows = 7
        y_offset = 40

        # Resolution
        self.default_screen_button.center = (sw/2 - 50, sh/rows + y_offset)
        self.medium_screen_button.center = (sw/2 + 50, sh/rows + y_offset)
        self.large_screen_button.center = (sw/2 + 150, sh/rows + y_offset)

        # Theme
        self.football_theme_button.center =(sw / 2 - 75, 2*sh/rows + y_offset)
        self.neon_theme_button.center = (sw / 2 + 25, 2*sh/rows + y_offset)
        self.paper_theme_button.center = (sw / 2 + 125, 2*sh/rows + y_offset)

        # Size
        self.small_board_button.center = (sw / 2 - 65, 3*sh/rows + y_offset)
        self.medium_board_button.center = (sw / 2 + 5, 3*sh/rows + y_offset)

        # Colors
        self.yellow_button.center = (sw/2, 4*sh/rows + y_offset)
        self.yellow_button_selected.center = (sw/2, 4*sh/rows + y_offset)
        self.pink_button.center = (sw / 2 + 35, 4*sh/rows + y_offset)
        self.pink_button_selected.center = (sw / 2 + 35, 4*sh/rows + y_offset)
        self.cyan_button.center = (sw / 2 + 35*2, 4*sh/rows + y_offset)
        self.cyan_button_selected.center = (sw / 2 + 35*2, 4*sh/rows + y_offset)
        self.red_button.center = (sw / 2 + 35*3, 4*sh/rows + y_offset)
        self.red_button_selected.center = (sw / 2 + 35*3, 4*sh/rows + y_offset)
        self.green_button.center = (sw / 2 + 35*4, 4*sh/rows + y_offset)
        self.green_button_selected.center = (sw / 2 + 35*4, 4*sh/rows + y_offset)
        self.orange_button.center = (sw / 2 + 35*5, 4*sh/rows + y_offset)
        self.orange_button_selected.center = (sw / 2 + 35*5, 4*sh/rows + y_offset)

        # Sound
        self.sound_off_button.center = (sw / 2 - 100, 5 * sh / rows + y_offset)
        self.sound_reduce_button.center = (sw / 2 - 50, 5 * sh / rows + y_offset)
        self.sound_increase_button.center = (sw / 2, 5 * sh / rows + y_offset)

    def render(self):
        sw = self.screen.get_width()
        sh = self.screen.get_height()

        # Clear screen
        self.screen.fill((3, 15, 56))

        # Background
        self.screen.blit(self.background, (0, 0))

        # Settings title
        draw_text('Game Settings', self.fontTitle, Colours.WHITE, self.screen, sw/2 - 100, 32)

        # Exit Icon
        self.screen.blit(self.exitIcon, (15, 25))

        # Resolution
        draw_text('Resolution:', self.font, Colours.WHITE, self.screen, self.default_screen_button.x - 125, self.default_screen_button.y + 5)
        self.screen.blit(self.default_screen, self.default_screen_button)
        self.screen.blit(self.medium_screen, self.medium_screen_button)
        self.screen.blit(self.large_screen, self.large_screen_button)

        # Themes
        draw_text('Themes:', self.font, Colours.WHITE, self.screen, self.football_theme_button.x - 100, self.football_theme_button.y + 5)
        self.screen.blit(self.football_theme, self.football_theme_button)
        self.screen.blit(self.neon_theme, self.neon_theme_button)
        self.screen.blit(self.paper_theme, self.paper_theme_button)

        # Board size
        draw_text('Board Size:', self.font, Colours.WHITE, self.screen, self.small_board_button.x - 125, self.small_board_button.y + 5)
        self.screen.blit(self.small_board, self.small_board_button)
        self.screen.blit(self.medium_board, self.medium_board_button)

        # Colours
        draw_text('Select your colour:', self.font, Colours.WHITE, self.screen, self.yellow_button.x - 210, self.yellow_button.y)
        pygame.draw.rect(self.screen, Colours.YELLOW, self.yellow_button)
        pygame.draw.rect(self.screen, Colours.PINK, self.pink_button)
        pygame.draw.rect(self.screen, Colours.CYAN, self.cyan_button)
        pygame.draw.rect(self.screen, Colours.RED, self.red_button)
        pygame.draw.rect(self.screen, Colours.GREEN, self.green_button)
        pygame.draw.rect(self.screen, Colours.ORANGE, self.orange_button)

        # Sound
        draw_text('Sound:', self.font, Colours.WHITE, self.screen, self.sound_off_button.x - 97, self.sound_off_button.y + 10)
        self.screen.blit(self.sound_off, self.sound_off_button)
        self.screen.blit(self.sound_reduce, self.sound_reduce_button)
        self.screen.blit(self.sound_increase, self.sound_increase_button)

        # Buttons
        if self.default_screen_button.collidepoint(pygame.mouse.get_pos()):
            self.screen.blit(self.default_screen_selected, (self.default_screen_button.x, self.default_screen_button.y))
        if self.medium_screen_button.collidepoint(pygame.mouse.get_pos()):
            self.screen.blit(self.medium_screen_selected, (self.medium_screen_button.x, self.medium_screen_button.y))
        if self.large_screen_button.collidepoint(pygame.mouse.get_pos()):
            self.screen.blit(self.large_screen_selected, (self.large_screen_button.x, self.large_screen_button.y))
        if self.football_theme_button.collidepoint(pygame.mouse.get_pos()):
            self.screen.blit(self.football_theme_selected, (self.football_theme_button.x, self.football_theme_button.y))
        if self.neon_theme_button.collidepoint(pygame.mouse.get_pos()):
            self.screen.blit(self.neon_theme_selected, (self.neon_theme_button.x, self.neon_theme_button.y))
        if self.paper_theme_button.collidepoint(pygame.mouse.get_pos()):
            self.screen.blit(self.paper_theme_selected, (self.paper_theme_button.x, self.paper_theme_button.y))
        if self.small_board_button.collidepoint(pygame.mouse.get_pos()):
            self.screen.blit(self.small_board_selected, (self.small_board_button.x, self.small_board_button.y))
        if self.medium_board_button.collidepoint(pygame.mouse.get_pos()):
            self.screen.blit(self.medium_board_selected, (self.medium_board_button.x, self.medium_board_button.y))
        if self.yellow_button.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(self.screen, Colours.YELLOW, self.yellow_button_selected)
        if self.pink_button.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(self.screen, Colours.PINK, self.pink_button_selected)
        if self.cyan_button.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(self.screen, Colours.CYAN, self.cyan_button_selected)
        if self.red_button.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(self.screen, Colours.RED, self.red_button_selected)
        if self.green_button.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(self.screen, Colours.GREEN, self.green_button_selected)
        if self.orange_button.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(self.screen, Colours.ORANGE, self.orange_button_selected)

        # Volume Buttons
       # pygame.draw.rect(self.screen, Colours.GREY, self.button_1)
        #pygame.draw.rect(self.screen, Colours.GREY, self.button_2)
        #pygame.draw.rect(self.screen, Colours.GREY, self.button_3)
        #draw_text('25%', self.font, Colours.WHITE, self.screen, self.button_1.x + 18, self.button_1.y + 10)
        #draw_text('50%', self.font, Colours.WHITE, self.screen, self.button_2.x + 18, self.button_2.y + 10)
        #draw_text('100%', self.font, Colours.WHITE, self.screen, self.button_3.x + 8, self.button_3.y + 10)

        # Theme Buttons
        #pygame.draw.rect(self.screen, Colours.GREY, self.button_4)
        #pygame.draw.rect(self.screen, Colours.GREY, self.button_5)
        #draw_text('Neon', self.font, Colours.WHITE, self.screen, self.button_4.x + 8, self.button_4.y + 10)
        #draw_text('Paper', self.font, Colours.WHITE, self.screen, self.button_5.x + 8, self.button_5.y + 10)

        # Board Size
        #pygame.draw.rect(self.screen, Colours.GREY, self.button_6)
        #pygame.draw.rect(self.screen, Colours.GREY, self.button_7)
        #draw_text('13 x 9', self.font, Colours.WHITE, self.screen, self. button_6.x + 8, self.button_6.y + 10)
        #draw_text('19 x 15', self.font, Colours.WHITE, self.screen, self.button_7.x + 8, self.button_7.y + 10)

        # Screen Mode
        #pygame.draw.rect(self.screen, Colours.GREY, self.button_8)
        #pygame.draw.rect(self.screen, Colours.GREY, self.button_9)
        #draw_text('Full', self.font, Colours.WHITE, self.screen, self.button_8.x + 8, self.button_8.y + 10)
        #draw_text('Windowed', self.font, Colours.WHITE, self.screen, self.button_9.x + 8, self.button_9.y + 10)
        # Headers
        #draw_text('Volume', self.font, Colours.WHITE, self.screen, 135, 110)
        #draw_text('Theme', self.font, Colours.WHITE, self.screen, 135, 230)
        #draw_text('Board Size', self.font, Colours.WHITE, self.screen, 115, 350)
        #draw_text('Screen Mode', self.font, Colours.WHITE, self.screen, 450, 110)

        # Show new frame
        pygame.display.flip()


# Helper Function
def draw_text(text, font, color, surface, x, y):
    text_object = font.render(text, 1, color)
    text_rect = text_object.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_object, text_rect)
