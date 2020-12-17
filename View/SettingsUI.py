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
    font = pygame.font.SysFont('arialbold', 30)

    mixer.music.load('Sound/background.wav')

    def __init__(self, controller):
        # State
        self.is_running = False

        # Context
        self.screen = controller.screen
        self.controller = controller

        # Exit menu button
        self.exit_rect = self.exitIcon.get_rect(topleft=(70, 80))

        # Buttons
        button_w = 70
        button_h = 40
        self.button_1 = pygame.Rect(35, 150, button_w, button_h)
        self.button_2 = pygame.Rect(135, 150, button_w, button_h)
        self.button_3 = pygame.Rect(235, 150, button_w, button_h)
        self.button_4 = pygame.Rect(90, 270, button_w, button_h)
        self.button_5 = pygame.Rect(190, 270, button_w, button_h)
        self.button_6 = pygame.Rect(90, 390, button_w, button_h)
        self.button_7 = pygame.Rect(190, 390, button_w + 20, button_h)
        self.button_8 = pygame.Rect(400, 150, button_w + 20, button_h)
        self.button_9 = pygame.Rect(530, 150, button_w + 40, button_h)

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
                if self.button_1.collidepoint(mouse_pos):
                    mixer.music.set_volume(0.25)
                elif self.button_2.collidepoint(mouse_pos):
                    mixer.music.set_volume(0.5)
                elif self.button_3.collidepoint(mouse_pos):
                    mixer.music.set_volume(1.0)
                # Back button
                elif self.exit_rect.collidepoint(mouse_pos):
                    self.controller.change_view(self.controller.menuUI)

    def update(self):
        pass

    def render(self):
        # Clear screen
        self.screen.fill((0, 0, 0))

        # Background
        self.screen.blit(self.background, (0, 0))

        # Settings title
        draw_text('Game Settings', self.font, Colours.WHITE, self.screen, 270, 30)

        # Exit Icon
        self.screen.blit(self.exitIcon, (15, 25))

        # Volume Buttons
        pygame.draw.rect(self.screen, Colours.GREY, self.button_1)
        pygame.draw.rect(self.screen, Colours.GREY, self.button_2)
        pygame.draw.rect(self.screen, Colours.GREY, self.button_3)
        draw_text('25%', self.font, Colours.WHITE, self.screen, self.button_1.x + 18, self.button_1.y + 10)
        draw_text('50%', self.font, Colours.WHITE, self.screen, self.button_2.x + 18, self.button_2.y + 10)
        draw_text('100%', self.font, Colours.WHITE, self.screen, self.button_3.x + 8, self.button_3.y + 10)

        # Theme Buttons
        pygame.draw.rect(self.screen, Colours.GREY, self.button_4)
        pygame.draw.rect(self.screen, Colours.GREY, self.button_5)
        draw_text('Neon', self.font, Colours.WHITE, self.screen, self.button_4.x + 8, self.button_4.y + 10)
        draw_text('Paper', self.font, Colours.WHITE, self.screen, self.button_5.x + 8, self.button_5.y + 10)

        # Board Size
        pygame.draw.rect(self.screen, Colours.GREY, self.button_6)
        pygame.draw.rect(self.screen, Colours.GREY, self.button_7)
        draw_text('13 x 9', self.font, Colours.WHITE, self.screen, self. button_6.x + 8, self.button_6.y + 10)
        draw_text('19 x 15', self.font, Colours.WHITE, self.screen, self.button_7.x + 8, self.button_7.y + 10)

        # Screen Mode
        pygame.draw.rect(self.screen, Colours.GREY, self.button_8)
        pygame.draw.rect(self.screen, Colours.GREY, self.button_9)
        draw_text('Full', self.font, Colours.WHITE, self.screen, self.button_8.x + 8, self.button_8.y + 10)
        draw_text('Windowed', self.font, Colours.WHITE, self.screen, self.button_9.x + 8, self.button_9.y + 10)
        # Headers
        draw_text('Volume', self.font, Colours.WHITE, self.screen, 135, 110)
        draw_text('Theme', self.font, Colours.WHITE, self.screen, 135, 230)
        draw_text('Board Size', self.font, Colours.WHITE, self.screen, 115, 350)
        draw_text('Screen Mode', self.font, Colours.WHITE, self.screen, 450, 110)

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
