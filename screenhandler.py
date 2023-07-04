from tkinter import *
from settings import *

class ScreenHandler:
    def load_screens(frames, main):
        for screen in frames:
            name = screen.__name__
            frame = screen(main.main_window, main)
            frame.grid(row=0, column=0, sticky="NSEW")
            main.screens[name] = frame

    def show_screen(page_name, main):
        frame = main.screens[page_name]
        frame.tkraise()