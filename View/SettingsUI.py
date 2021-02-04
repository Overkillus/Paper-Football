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
        self.default_screen_button = pygame.Rect(250, 95, self.default_screen.get_width(), self.default_screen.get_height())
        self.medium_screen_button = pygame.Rect(350, 95, self.medium_screen.get_width(), self.medium_screen.get_height())
        self.large_screen_button = pygame.Rect(450, 95, self.large_screen.get_width(), self.large_screen.get_height())
        self.football_theme_button = pygame.Rect(225, 170, self.football_theme.get_width(), self.football_theme.get_height())
        self.neon_theme_button = pygame.Rect(325, 170, self.neon_theme.get_width(), self.neon_theme.get_height())
        self.paper_theme_button = pygame.Rect(425, 170, self.paper_theme.get_width(), self.paper_theme.get_height())
        self.small_board_button = pygame.Rect(250, 245, self.small_board.get_width(), self.small_board.get_height())
        self.medium_board_button = pygame.Rect(320, 245, self.medium_board.get_width(), self.medium_board.get_height())
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
                self.controller.change_view(self.controller.menuUI)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.controller.change_view(self.controller.menuUI)
            elif event.type == pygame.MOUSEBUTTONUP:
                # Mouse click
                mouse_pos = pygame.mouse.get_pos()
                # Increase volume
                if self.sound_off_button.collidepoint(mouse_pos):
                    mixer.music.set_volume(0.0)
                elif self.sound_reduce_button.collidepoint(mouse_pos):
                    mixer.music.set_volume(0.5)
                elif self.sound_increase_button.collidepoint(mouse_pos):
                    mixer.music.set_volume(1.0)

                # Back button
                if self.exit_button.collidepoint(mouse_pos):
                    self.controller.change_view(self.controller.menuUI)

    def update(self):
        pass

    def render(self):
        # Clear screen
        self.screen.fill((0, 0, 0))

        # Background
        self.screen.blit(self.background, (0, 0))

        # Settings title
        draw_text('Game Settings', self.font, Colours.WHITE, self.screen, 300, 30)

        # Exit Icon
        self.screen.blit(self.exitIcon, (15, 25))

        # Resolution
        draw_text('Resolution:', self.font, Colours.WHITE, self.screen, 125, 100)
        self.screen.blit(self.default_screen, (250, 95))
        self.screen.blit(self.medium_screen, (350, 95))
        self.screen.blit(self.large_screen, (450, 95))

        # Themes
        draw_text('Themes:', self.font, Colours.WHITE, self.screen, 125, 175)
        self.screen.blit(self.football_theme, (225, 170))
        self.screen.blit(self.neon_theme, (325, 170))
        self.screen.blit(self.paper_theme, (425, 170))

        # Board size
        draw_text('Board Size:', self.font, Colours.WHITE, self.screen, 125, 250)
        self.screen.blit(self.small_board, (250, 245))
        self.screen.blit(self.medium_board, (320, 245))

        # Colours
        draw_text('Select your colour:', self.font, Colours.WHITE, self.screen, 125, 325)
        pygame.draw.rect(self.screen, Colours.YELLOW, self.yellow_button)
        pygame.draw.rect(self.screen, Colours.PINK, self.pink_button)
        pygame.draw.rect(self.screen, Colours.CYAN, self.cyan_button)
        pygame.draw.rect(self.screen, Colours.RED, self.red_button)
        pygame.draw.rect(self.screen, Colours.GREEN, self.green_button)
        pygame.draw.rect(self.screen, Colours.ORANGE, self.orange_button)

        # Sound
        draw_text('Sound:', self.font, Colours.WHITE, self.screen, 125, 400)
        self.screen.blit(self.sound_off, (220, 385))
        self.screen.blit(self.sound_reduce, (270, 385))
        self.screen.blit(self.sound_increase, (320, 385))

        # Buttons
        if self.default_screen_button.collidepoint(pygame.mouse.get_pos()):
            self.screen.blit(self.default_screen_selected, (250, 95))
        if self.medium_screen_button.collidepoint(pygame.mouse.get_pos()):
            self.screen.blit(self.medium_screen_selected, (350, 95))
        if self.large_screen_button.collidepoint(pygame.mouse.get_pos()):
            self.screen.blit(self.large_screen_selected, (450, 95))
        if self.football_theme_button.collidepoint(pygame.mouse.get_pos()):
            self.screen.blit(self.football_theme_selected, (225, 170))
        if self.neon_theme_button.collidepoint(pygame.mouse.get_pos()):
            self.screen.blit(self.neon_theme_selected, (325, 170))
        if self.paper_theme_button.collidepoint(pygame.mouse.get_pos()):
            self.screen.blit(self.paper_theme_selected, (425, 170))
        if self.small_board_button.collidepoint(pygame.mouse.get_pos()):
            self.screen.blit(self.small_board_selected, (250, 245))
        if self.medium_board_button.collidepoint(pygame.mouse.get_pos()):
            self.screen.blit(self.medium_board_selected, (320, 245))
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

# Window
# root = Tk()
# root.geometry('768x550')
# root.title("Settings")
# root.iconbitmap(r'Art/settings.png')


# About Credits
# def about_game():
#   tkinter.messagebox.showinfo('Credits', 'Sound from:\n~Zapsplat.com, '
#             '\n~PlayOnLoop.com, '
#            '\n~http://www.freesfx.co.uk')


# How to play
# def rules():
#   tkinter.messagebox.showinfo('Rules', 'Two players are trying to score a goal in the opponents net with horizontal, '
#                                       'vertical and diagonal moves.\nAlready used points can be re-used for a double'
#                                      'move')


# menubar
# menubar = Menu(root)
# root.config(menu=menubar)

# submenu
# subMenu = Menu(menubar, tearoff=0)
# menubar.add_cascade(label="About", menu=subMenu)
# subMenu.add_command(label="Credits", command=about_game)
# subMenu.add_command(label="How to play", command=rules)

# text
# text = Label(root, text='Game Settings')
# text.pack(pady=10)


# button functions
# muted = FALSE


# def mute_music():
# global muted
# if muted:  # unmute music
# mixer.music.set_volume(0.5)
# volume1Btn.configure(image=volume1Photo)
# scale.set(50)
#   muted = FALSE
#   #else:  # mute
#    mixer.music.set_volume(0)
#     volume1Btn.configure(image=mutePhoto)
#      scale.set(0)
#       muted = TRUE


# def play_btn():
#  mixer.music.load('background.wav')
#   mixer.music.play()


# def pause_btn():
# mixer.music.load('../Sound/background.wav')
#  mixer.music.stop()
#   statusbar['text'] = "Paper football: music paused"


# def set_vol(val):
# volume = int(val) / 100
# mixer.music.set_volume(volume)


# def exit_btn():
#   root.destroy()

# frame
# middleframe = Frame(root, relief=RAISED, borderwidth=0)
# middleframe.pack()

# Volume 1
# volume1Photo = PhotoImage(file='../Art/sound.png')
# volume1Btn = Button(image=volume1Photo, command=mute_music)
# volume1Btn.pack()
# mutePhoto = PhotoImage(file='../Art/sound_off.png')

# Volume button
# volumePhoto = PhotoImage(file='../Art/sound.png')
# play_btn = Button(middleframe, image=volumePhoto, command=play_btn)
# play_btn.pack(pady=5, padx=10)

# Mixer
# scale = Scale(root, from_=0, to=100, orient=HORIZONTAL, command=set_vol)
# scale.set(50)  # default value
# mixer.music.set_volume(50)
# scale.pack()

# Exit button
# exitPhoto = PhotoImage(file='../Art/exit.png')
# exit_btn = Button(middleframe, image=exitPhoto, command=exit_btn)
# exit_btn.pack(pady=5, padx=10)


# status bar
# statusbar = Label(root, text="Paper Football", relief=SUNKEN, anchor=W)
# statusbar.pack(side=BOTTOM, fill=X)

# loop
# root.mainloop()
