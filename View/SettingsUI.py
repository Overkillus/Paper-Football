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
    exitIcon = pygame.image.load('Art/exit2.png')
    default_screen = pygame.image.load('Art/default_b.png')
    default_screen_selected = pygame.image.load('Art/default_b_selected.png')
    medium_screen = pygame.image.load('Art/medium_screen_b.png')
    medium_screen_selected = pygame.image.load('Art/medium_screen_b_selected.png')
    large_screen = pygame.image.load('Art/large_screen_b.png')
    large_screen_selected = pygame.image.load('Art/large_screen_b_selected.png')
    native_screen = pygame.image.load('Art/native.png')
    native_screen_selected = pygame.image.load('Art/native_selected.png')
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

        # Exit
        self.exit_button = self.exitIcon.get_rect()

        # Color Buttons
        color_button = pygame.Rect(0, 0, 25, 25)
        color_button_selected = pygame.Rect(0, 0, 34, 34)
        # Colors player 1
        self.yellow_button_p1 = color_button.copy()
        self.yellow_button_selected_p1 = color_button_selected.copy()
        self.pink_button_p1 = color_button.copy()
        self.pink_button_selected_p1 = color_button_selected.copy()
        self.cyan_button_p1 = color_button.copy()
        self.cyan_button_selected_p1 = color_button_selected.copy()
        self.red_button_p1 = color_button.copy()
        self.red_button_selected_p1 = color_button_selected.copy()
        self.green_button_p1 = color_button.copy()
        self.green_button_selected_p1 = color_button_selected.copy()
        self.orange_button_p1 = color_button.copy()
        self.orange_button_selected_p1 = color_button_selected.copy()
        # Colors player 2
        self.yellow_button_p2 = color_button.copy()
        self.yellow_button_selected_p2 = color_button_selected.copy()
        self.pink_button_p2 = color_button.copy()
        self.pink_button_selected_p2 = color_button_selected.copy()
        self.cyan_button_p2 = color_button.copy()
        self.cyan_button_selected_p2 = color_button_selected.copy()
        self.red_button_p2 = color_button.copy()
        self.red_button_selected_p2 = color_button_selected.copy()
        self.green_button_p2 = color_button.copy()
        self.green_button_selected_p2 = color_button_selected.copy()
        self.orange_button_p2 = color_button.copy()
        self.orange_button_selected_p2 = color_button_selected.copy()
        # Resolution
        self.default_screen_button = self.default_screen.get_rect()
        self.medium_screen_button = self.medium_screen.get_rect()
        self.large_screen_button = self.large_screen.get_rect()
        self.native_screen_button = self.native_screen.get_rect()
        # Theme
        self.football_theme_button = self.football_theme.get_rect()
        self.neon_theme_button = self.neon_theme.get_rect()
        self.paper_theme_button = self.paper_theme.get_rect()
        # Size
        self.small_board_button = self.small_board.get_rect()
        self.medium_board_button = self.medium_board.get_rect()
        # Sound
        self.sound_off_button = self.sound_off.get_rect()
        self.sound_reduce_button = self.sound_reduce.get_rect()
        self.sound_increase_button = self.sound_increase.get_rect()

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
                    mixer.music.set_volume(mixer.music.get_volume() - 0.1)
                elif self.sound_increase_button.collidepoint(mouse_pos):
                    mixer.music.set_volume(mixer.music.get_volume() + 0.1)

                # Resolution Settings
                if self.default_screen_button.collidepoint(mouse_pos):
                    self.screen = pygame.display.set_mode((Settings.default_screen_width, Settings.default_screen_height), pygame.RESIZABLE)
                    Settings.is_native = False
                    # scale buttons
                    self.default_screen = pygame.transform.scale(self.default_screen, (92, 34))
                    self.default_screen_selected = pygame.transform.scale(self.default_screen_selected, (92, 34))
                    self.medium_screen = pygame.transform.scale(self.medium_screen, (92, 34))
                    self.medium_screen_selected = pygame.transform.scale(self.medium_screen_selected, (92, 34))
                    self.large_screen = pygame.transform.scale(self.large_screen, (92, 34))
                    self.large_screen_selected = pygame.transform.scale(self.large_screen_selected, (92, 34))
                    self.native_screen = pygame.transform.scale(self.native_screen, (92, 34))
                    self.native_screen_selected = pygame.transform.scale(self.native_screen_selected, (92, 34))
                    self.football_theme = pygame.transform.scale(self.football_theme, (92, 34))
                    self.football_theme_selected = pygame.transform.scale(self.football_theme_selected, (92, 34))
                    self.neon_theme = pygame.transform.scale(self.neon_theme, (92, 34))
                    self.neon_theme_selected = pygame.transform.scale(self.neon_theme_selected, (92, 34))
                    self.paper_theme = pygame.transform.scale(self.paper_theme, (92, 34))
                    self.paper_theme_selected = pygame.transform.scale(self.paper_theme_selected, (92, 34))
                    self.small_board = pygame.transform.scale(self.small_board, (64, 34))
                    self.small_board_selected = pygame.transform.scale(self.small_board_selected, (64, 34))
                    self.medium_board = pygame.transform.scale(self.medium_board, (64, 34))
                    self.medium_board_selected = pygame.transform.scale(self.medium_board_selected, (64, 34))
                    self.sound_off = pygame.transform.scale(self.sound_off, (59, 54))
                    self.sound_reduce = pygame.transform.scale(self.sound_reduce, (59, 54))
                    self.sound_increase = pygame.transform.scale(self.sound_increase, (59, 54))
                    self.exitIcon = pygame.transform.scale(self.exitIcon, (32, 53))

                elif self.medium_screen_button.collidepoint(mouse_pos):
                    self.screen = pygame.display.set_mode((1366, 768), pygame.RESIZABLE)
                    Settings.is_native = False
                    # scale buttons
                    self.default_screen = pygame.transform.scale(self.default_screen, (110,38))
                    self.default_screen_selected = pygame.transform.scale(self.default_screen_selected, (110, 38))
                    self.medium_screen = pygame.transform.scale(self.medium_screen, (110, 38))
                    self.medium_screen_selected = pygame.transform.scale(self.medium_screen_selected, (110, 38))
                    self.large_screen = pygame.transform.scale(self.large_screen, (110, 38))
                    self.large_screen_selected = pygame.transform.scale(self.large_screen_selected, (110, 38))
                    self.native_screen = pygame.transform.scale(self.native_screen, (110, 38))
                    self.native_screen_selected = pygame.transform.scale(self.native_screen_selected, (110, 38))
                    self.football_theme = pygame.transform.scale(self.football_theme, (110, 38))
                    self.football_theme_selected = pygame.transform.scale(self.football_theme_selected, (110, 38))
                    self.neon_theme = pygame.transform.scale(self.neon_theme, (110, 38))
                    self.neon_theme_selected = pygame.transform.scale(self.neon_theme_selected, (110, 38))
                    self.paper_theme = pygame.transform.scale(self.paper_theme, (110, 38))
                    self.paper_theme_selected = pygame.transform.scale(self.paper_theme_selected, (110, 38))
                    self.small_board = pygame.transform.scale(self.small_board, (76, 38))
                    self.small_board_selected = pygame.transform.scale(self.small_board_selected, (76, 38))
                    self.medium_board = pygame.transform.scale(self.medium_board, (76, 38))
                    self.medium_board_selected = pygame.transform.scale(self.medium_board_selected, (76, 38))
                    self.sound_off = pygame.transform.scale(self.sound_off, (70, 64))
                    self.sound_reduce = pygame.transform.scale(self.sound_reduce, (70, 64))
                    self.sound_increase = pygame.transform.scale(self.sound_increase, (70, 64))
                    self.exitIcon = pygame.transform.scale(self.exitIcon, (38, 63))

                elif self.large_screen_button.collidepoint(mouse_pos):
                    self.screen = pygame.display.set_mode((1920, 1080), pygame.RESIZABLE)
                    Settings.is_native = False
                    # scale buttons
                    self.default_screen = pygame.transform.scale(self.default_screen, (128, 47))
                    self.default_screen_selected = pygame.transform.scale(self.default_screen_selected, (128, 47))
                    self.medium_screen = pygame.transform.scale(self.medium_screen, (128, 47))
                    self.medium_screen_selected = pygame.transform.scale(self.medium_screen_selected, (128, 47))
                    self.large_screen = pygame.transform.scale(self.large_screen, (128, 47))
                    self.large_screen_selected = pygame.transform.scale(self.large_screen_selected, (128, 47))
                    self.native_screen = pygame.transform.scale(self.native_screen, (128, 47))
                    self.native_screen_selected = pygame.transform.scale(self.native_screen_selected, (128, 47))
                    self.football_theme = pygame.transform.scale(self.football_theme, (128, 47))
                    self.football_theme_selected = pygame.transform.scale(self.football_theme_selected, (128, 47))
                    self.neon_theme = pygame.transform.scale(self.neon_theme, (128, 47))
                    self.neon_theme_selected = pygame.transform.scale(self.neon_theme_selected, (128, 47))
                    self.paper_theme = pygame.transform.scale(self.paper_theme, (128, 47))
                    self.paper_theme_selected = pygame.transform.scale(self.paper_theme_selected, (128, 47))
                    self.small_board = pygame.transform.scale(self.small_board, (89, 47))
                    self.small_board_selected = pygame.transform.scale(self.small_board_selected, (89, 47))
                    self.medium_board = pygame.transform.scale(self.medium_board, (89, 47))
                    self.medium_board_selected = pygame.transform.scale(self.medium_board_selected, (89, 47))
                    self.sound_off = pygame.transform.scale(self.sound_off, (85, 77))
                    self.sound_reduce = pygame.transform.scale(self.sound_reduce, (85, 77))
                    self.sound_increase = pygame.transform.scale(self.sound_increase, (85, 77))
                    self.exitIcon = pygame.transform.scale(self.exitIcon, (47, 74))

                elif self.native_screen_button.collidepoint(mouse_pos):
                    self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                    Settings.screen_width = pygame.display.get_window_size()[0]
                    Settings.screen_width = pygame.display.get_window_size()[1]
                    Settings.is_native = True
                    # scale buttons
                    self.default_screen = pygame.transform.scale(self.default_screen, (128, 47))
                    self.default_screen_selected = pygame.transform.scale(self.default_screen_selected, (128, 47))
                    self.medium_screen = pygame.transform.scale(self.medium_screen, (128, 47))
                    self.medium_screen_selected = pygame.transform.scale(self.medium_screen_selected, (128, 47))
                    self.large_screen = pygame.transform.scale(self.large_screen, (128, 47))
                    self.large_screen_selected = pygame.transform.scale(self.large_screen_selected, (128, 47))
                    self.native_screen = pygame.transform.scale(self.native_screen, (128, 47))
                    self.native_screen_selected = pygame.transform.scale(self.native_screen_selected, (128, 47))
                    self.football_theme = pygame.transform.scale(self.football_theme, (128, 47))
                    self.football_theme_selected = pygame.transform.scale(self.football_theme_selected, (128, 47))
                    self.neon_theme = pygame.transform.scale(self.neon_theme, (128, 47))
                    self.neon_theme_selected = pygame.transform.scale(self.neon_theme_selected, (128, 47))
                    self.paper_theme = pygame.transform.scale(self.paper_theme, (128, 47))
                    self.paper_theme_selected = pygame.transform.scale(self.paper_theme_selected, (128, 47))
                    self.small_board = pygame.transform.scale(self.small_board, (89, 47))
                    self.small_board_selected = pygame.transform.scale(self.small_board_selected, (89, 47))
                    self.medium_board = pygame.transform.scale(self.medium_board, (89, 47))
                    self.medium_board_selected = pygame.transform.scale(self.medium_board_selected, (89, 47))
                    self.exitIcon = pygame.transform.scale(self.exitIcon, (47, 74))

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

                # Colour player 1 Settings
                if self.yellow_button_p1.collidepoint(mouse_pos):
                    self.controller.gameUI.players[0].set_color(Colours.YELLOW)
                elif self.pink_button_p1.collidepoint(mouse_pos):
                    self.controller.gameUI.players[0].set_color(Colours.PINK)
                elif self.cyan_button_p1.collidepoint(mouse_pos):
                    self.controller.gameUI.players[0].set_color(Colours.CYAN)
                elif self.red_button_p1.collidepoint(mouse_pos):
                    self.controller.gameUI.players[0].set_color(Colours.RED)
                elif self.green_button_p1.collidepoint(mouse_pos):
                    self.controller.gameUI.players[0].set_color(Colours.GREEN)
                elif self.orange_button_p1.collidepoint(mouse_pos):
                    self.controller.gameUI.players[0].set_color(Colours.ORANGE)

                # Colour player 2 Settings
                if self.yellow_button_p2.collidepoint(mouse_pos):
                    self.controller.gameUI.players[1].set_color(Colours.YELLOW)
                elif self.pink_button_p2.collidepoint(mouse_pos):
                    self.controller.gameUI.players[1].set_color(Colours.PINK)
                elif self.cyan_button_p2.collidepoint(mouse_pos):
                    self.controller.gameUI.players[1].set_color(Colours.CYAN)
                elif self.red_button_p2.collidepoint(mouse_pos):
                    self.controller.gameUI.players[1].set_color(Colours.RED)
                elif self.green_button_p2.collidepoint(mouse_pos):
                    self.controller.gameUI.players[1].set_color(Colours.GREEN)
                elif self.orange_button_p2.collidepoint(mouse_pos):
                    self.controller.gameUI.players[1].set_color(Colours.ORANGE)

                # Back button
                if self.exit_button.collidepoint(mouse_pos):
                    self.controller.change_view(self.controller.menuUI)

    def update(self):
        sw = self.screen.get_width()
        sh = self.screen.get_height()
        rows = 8
        y_offset = 40

        # Exit
        self.exit_button.topleft = (20, 20)

        # Resolution
        self.default_screen_button.center = (sw/2 - 50, sh/rows + y_offset)
        self.medium_screen_button.center = (sw/2 + 50, sh/rows + y_offset)
        self.large_screen_button.center = (sw/2 + 150, sh/rows + y_offset)
        self.native_screen_button.center = (sw/2 + 250, sh/rows + y_offset)

        # Theme
        self.football_theme_button.center =(sw / 2 - 75, 2*sh/rows + y_offset)
        self.neon_theme_button.center = (sw / 2 + 25, 2*sh/rows + y_offset)
        self.paper_theme_button.center = (sw / 2 + 125, 2*sh/rows + y_offset)

        # Size
        self.small_board_button.center = (sw / 2 - 65, 3*sh/rows + y_offset)
        self.medium_board_button.center = (sw / 2 + 5, 3*sh/rows + y_offset)

        # Colors player 1
        self.yellow_button_p1.center = (20 + sw / 2, 4 * sh / rows + y_offset)
        self.yellow_button_selected_p1.center = (20 + sw / 2, 4 * sh / rows + y_offset)
        self.pink_button_p1.center = (20 + sw / 2 + 40, 4 * sh / rows + y_offset)
        self.pink_button_selected_p1.center = (20 + sw / 2 + 40, 4 * sh / rows + y_offset)
        self.cyan_button_p1.center = (20 + sw / 2 + 40 * 2, 4 * sh / rows + y_offset)
        self.cyan_button_selected_p1.center = (20 + sw / 2 + 40 * 2, 4 * sh / rows + y_offset)
        self.red_button_p1.center = (20 + sw / 2 + 40 * 3, 4 * sh / rows + y_offset)
        self.red_button_selected_p1.center = (20 + sw / 2 + 40 * 3, 4 * sh / rows + y_offset)
        self.green_button_p1.center = (20 + sw / 2 + 40 * 4, 4 * sh / rows + y_offset)
        self.green_button_selected_p1.center = (20 + sw / 2 + 40 * 4, 4 * sh / rows + y_offset)
        self.orange_button_p1.center = (20 + sw / 2 + 40 * 5, 4 * sh / rows + y_offset)
        self.orange_button_selected_p1.center = (20 + sw / 2 + 40 * 5, 4 * sh / rows + y_offset)

        # Colors player 2
        self.yellow_button_p2.center = (20 + sw / 2, 5 * sh / rows + y_offset)
        self.yellow_button_selected_p2.center = (20 + sw / 2, 5 * sh / rows + y_offset)
        self.pink_button_p2.center = (20 + sw / 2 + 40, 5 * sh / rows + y_offset)
        self.pink_button_selected_p2.center = (20 + sw / 2 + 40, 5 * sh / rows + y_offset)
        self.cyan_button_p2.center = (20 + sw / 2 + 40 * 2, 5 * sh / rows + y_offset)
        self.cyan_button_selected_p2.center = (20 + sw / 2 + 40 * 2, 5 * sh / rows + y_offset)
        self.red_button_p2.center = (20 + sw / 2 + 40 * 3, 5 * sh / rows + y_offset)
        self.red_button_selected_p2.center = (20 + sw / 2 + 40 * 3, 5 * sh / rows + y_offset)
        self.green_button_p2.center = (20 + sw / 2 + 40 * 4, 5 * sh / rows + y_offset)
        self.green_button_selected_p2.center = (20 + sw / 2 + 40 * 4, 5 * sh / rows + y_offset)
        self.orange_button_p2.center = (20 + sw / 2 + 40 * 5, 5 * sh / rows + y_offset)
        self.orange_button_selected_p2.center = (20 + sw / 2 + 40 * 5, 5 * sh / rows + y_offset)

        # Sound
        self.sound_off_button.center = (sw / 2 - 100, 6 * sh / rows + y_offset)
        self.sound_reduce_button.center = (sw / 2 - 50, 6 * sh / rows + y_offset)
        self.sound_increase_button.center = (sw / 2, 6 * sh / rows + y_offset)

    def render(self):
        sw = self.screen.get_width()
        sh = self.screen.get_height()

        # Clear screen
        self.screen.fill((3, 15, 56))

        # Settings title
        draw_text('Game Settings', self.fontTitle, Colours.WHITE, self.screen, sw/2 - 100, 32)

        # Exit Icon
        self.screen.blit(self.exitIcon, self.exit_button)

        # Resolution
        draw_text('Resolution:', self.font, Colours.WHITE, self.screen, self.default_screen_button.x - 125, self.default_screen_button.y + 5)
        self.screen.blit(self.default_screen, self.default_screen_button)
        self.screen.blit(self.medium_screen, self.medium_screen_button)
        self.screen.blit(self.large_screen, self.large_screen_button)
        self.screen.blit(self.native_screen, self.native_screen_button)

        # Themes
        draw_text('Themes:', self.font, Colours.WHITE, self.screen, self.football_theme_button.x - 100, self.football_theme_button.y + 5)
        self.screen.blit(self.football_theme, self.football_theme_button)
        self.screen.blit(self.neon_theme, self.neon_theme_button)
        self.screen.blit(self.paper_theme, self.paper_theme_button)

        # Board size
        draw_text('Board Size:', self.font, Colours.WHITE, self.screen, self.small_board_button.x - 125, self.small_board_button.y + 5)
        self.screen.blit(self.small_board, self.small_board_button)
        self.screen.blit(self.medium_board, self.medium_board_button)

        # Colours player 1
        draw_text('Select your colour:', self.font, Colours.WHITE, self.screen, self.yellow_button_p1.x - 230, self.yellow_button_p1.y)
        pygame.draw.rect(self.screen, Colours.YELLOW, self.yellow_button_p1)
        pygame.draw.rect(self.screen, Colours.PINK, self.pink_button_p1)
        pygame.draw.rect(self.screen, Colours.CYAN, self.cyan_button_p1)
        pygame.draw.rect(self.screen, Colours.RED, self.red_button_p1)
        pygame.draw.rect(self.screen, Colours.GREEN, self.green_button_p1)
        pygame.draw.rect(self.screen, Colours.ORANGE, self.orange_button_p1)

        # Colours player 2
        draw_text('Select enemy colour:', self.font, Colours.WHITE, self.screen, self.yellow_button_p1.x - 230, self.yellow_button_p2.y)
        pygame.draw.rect(self.screen, Colours.YELLOW, self.yellow_button_p2)
        pygame.draw.rect(self.screen, Colours.PINK, self.pink_button_p2)
        pygame.draw.rect(self.screen, Colours.CYAN, self.cyan_button_p2)
        pygame.draw.rect(self.screen, Colours.RED, self.red_button_p2)
        pygame.draw.rect(self.screen, Colours.GREEN, self.green_button_p2)
        pygame.draw.rect(self.screen, Colours.ORANGE, self.orange_button_p2)

        # Sound
        draw_text('Sound:', self.font, Colours.WHITE, self.screen, self.sound_off_button.x - 97, self.sound_off_button.y + 10)
        self.screen.blit(self.sound_off, self.sound_off_button)
        self.screen.blit(self.sound_reduce, self.sound_reduce_button)
        self.screen.blit(self.sound_increase, self.sound_increase_button)

        # Buttons select highlight
        pos = pygame.mouse.get_pos()
        # Resolution
        if self.default_screen_button.collidepoint(pos) or pygame.display.get_window_size() == (Settings.default_screen_width, Settings.default_screen_height):
            self.screen.blit(self.default_screen_selected, (self.default_screen_button.x, self.default_screen_button.y))
        if self.medium_screen_button.collidepoint(pos) or pygame.display.get_window_size() == (1366, 768):
            self.screen.blit(self.medium_screen_selected, (self.medium_screen_button.x, self.medium_screen_button.y))
        if self.large_screen_button.collidepoint(pos) or pygame.display.get_window_size() == (1920, 1080):
            self.screen.blit(self.large_screen_selected, (self.large_screen_button.x, self.large_screen_button.y))
        if self.native_screen_button.collidepoint(pos) or Settings.is_native:
            self.screen.blit(self.native_screen_selected, (self.native_screen_button.x, self.native_screen_button.y))

        # Theme
        if self.football_theme_button.collidepoint(pos):
            self.screen.blit(self.football_theme_selected, (self.football_theme_button.x, self.football_theme_button.y))
        if self.neon_theme_button.collidepoint(pos):
            self.screen.blit(self.neon_theme_selected, (self.neon_theme_button.x, self.neon_theme_button.y))
        if self.paper_theme_button.collidepoint(pos):
            self.screen.blit(self.paper_theme_selected, (self.paper_theme_button.x, self.paper_theme_button.y))

        # Size
        if self.small_board_button.collidepoint(pos):
            self.screen.blit(self.small_board_selected, (self.small_board_button.x, self.small_board_button.y))
        if self.medium_board_button.collidepoint(pos):
            self.screen.blit(self.medium_board_selected, (self.medium_board_button.x, self.medium_board_button.y))

        # Color player 1
        if self.yellow_button_p1.collidepoint(pos) or self.controller.gameUI.players[0].get_color() == Colours.YELLOW:
            pygame.draw.rect(self.screen, Colours.YELLOW, self.yellow_button_selected_p1)
        if self.pink_button_p1.collidepoint(pos) or self.controller.gameUI.players[0].get_color() == Colours.PINK:
            pygame.draw.rect(self.screen, Colours.PINK, self.pink_button_selected_p1)
        if self.cyan_button_p1.collidepoint(pos) or self.controller.gameUI.players[0].get_color() == Colours.CYAN:
            pygame.draw.rect(self.screen, Colours.CYAN, self.cyan_button_selected_p1)
        if self.red_button_p1.collidepoint(pos) or self.controller.gameUI.players[0].get_color() == Colours.RED:
            pygame.draw.rect(self.screen, Colours.RED, self.red_button_selected_p1)
        if self.green_button_p1.collidepoint(pos) or self.controller.gameUI.players[0].get_color() == Colours.GREEN:
            pygame.draw.rect(self.screen, Colours.GREEN, self.green_button_selected_p1)
        if self.orange_button_p1.collidepoint(pos) or self.controller.gameUI.players[0].get_color() == Colours.ORANGE:
            pygame.draw.rect(self.screen, Colours.ORANGE, self.orange_button_selected_p1)

        # Color player 2
        if self.yellow_button_p2.collidepoint(pos) or self.controller.gameUI.players[1].get_color() == Colours.YELLOW:
            pygame.draw.rect(self.screen, Colours.YELLOW, self.yellow_button_selected_p2)
        if self.pink_button_p2.collidepoint(pos) or self.controller.gameUI.players[1].get_color() == Colours.PINK:
            pygame.draw.rect(self.screen, Colours.PINK, self.pink_button_selected_p2)
        if self.cyan_button_p2.collidepoint(pos) or self.controller.gameUI.players[1].get_color() == Colours.CYAN:
            pygame.draw.rect(self.screen, Colours.CYAN, self.cyan_button_selected_p2)
        if self.red_button_p2.collidepoint(pos) or self.controller.gameUI.players[1].get_color() == Colours.RED:
            pygame.draw.rect(self.screen, Colours.RED, self.red_button_selected_p2)
        if self.green_button_p2.collidepoint(pos) or self.controller.gameUI.players[1].get_color() == Colours.GREEN:
            pygame.draw.rect(self.screen, Colours.GREEN, self.green_button_selected_p2)
        if self.orange_button_p2.collidepoint(pos) or self.controller.gameUI.players[1].get_color() == Colours.ORANGE:
            pygame.draw.rect(self.screen, Colours.ORANGE, self.orange_button_selected_p2)

        # Show new frame
        pygame.display.flip()


# Helper Function
def draw_text(text, font, color, surface, x, y):
    text_object = font.render(text, 1, color)
    text_rect = text_object.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_object, text_rect)
