from idlelib import statusbar
from tkinter import *
import tkinter.messagebox
from pygame import mixer

# Window
root = Tk()
mixer.init()
root.geometry('500x550')
root.title("Settings")
root.iconbitmap(r'Art/settings.png')


# About Credits
def about_game():
    tkinter.messagebox.showinfo('Credits', 'Sound from:\n~Zapsplat.com, '
                                           '\n~PlayOnLoop.com, '
                                           '\n~http://www.freesfx.co.uk')


# How to play
def rules():
    tkinter.messagebox.showinfo('Rules', 'Two players are trying to score a goal in the opponents net with horizontal, '
                                         'vertical and diagonal moves.\nAlready used points can be re-used for a double'
                                         'move')


# menubar
menubar = Menu(root)
root.config(menu=menubar)

# submenu
subMenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="About", menu=subMenu)
subMenu.add_command(label="Credits", command=about_game)
subMenu.add_command(label="How to play", command=rules)

# text
text = Label(root, text='Game Settings')
text.pack(pady=10)


# button functions
muted = FALSE


def mute_music():
    global muted
    if muted:  # unmute music
        mixer.music.set_volume(0.5)
        volume1Btn.configure(image=volume1Photo)
        scale.set(50)
        muted = FALSE
    else:  # mute
        mixer.music.set_volume(0)
        volume1Btn.configure(image=mutePhoto)
        scale.set(0)
        muted = TRUE


def play_btn():
    mixer.music.load('background.wav')
    mixer.music.play()


def pause_btn():
    mixer.music.load('Sound/background.wav')
    mixer.music.stop()
    statusbar['text'] = "Paper football: music paused"


def set_vol(val):
    volume = int(val) / 100
    mixer.music.set_volume(volume)


def exit_btn():
    root.destroy()


# frame
middleframe = Frame(root, relief=RAISED, borderwidth=0)
middleframe.pack()

# Volume 1
volume1Photo = PhotoImage(file='Art/sound.png')
volume1Btn = Button(image=volume1Photo, command=mute_music)
volume1Btn.pack()
mutePhoto = PhotoImage(file='Art/sound_off.png')

# Volume button
volumePhoto = PhotoImage(file='Art/sound.png')
play_btn = Button(middleframe, image=volumePhoto, command=play_btn)
play_btn.pack(pady=5, padx=10)



# Mixer
scale = Scale(root, from_=0, to=100, orient=HORIZONTAL, command=set_vol)
scale.set(50)  # default value
mixer.music.set_volume(50)
scale.pack()

# Exit button
exitPhoto = PhotoImage(file='Art/exit.png')
exit_btn = Button(middleframe, image=exitPhoto, command=exit_btn)
exit_btn.pack(pady=5, padx=10)


# status bar
statusbar = Label(root, text="Paper Football", relief=SUNKEN, anchor=W)
statusbar.pack(side=BOTTOM, fill=X)

# loop
root.mainloop()
