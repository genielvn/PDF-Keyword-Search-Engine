from tkinter import *
from settings import *
from MainScreen import screen as ms
from screenhandler import ScreenHandler
import traceback

class MainWindow():
    def __init__(self, master):
        self.main_window = Frame(master)

        self.main_window.pack(fill="both", expand=True)
        self.main_window.grid_rowconfigure(0, weight=1)
        self.main_window.grid_columnconfigure(0, weight=1)

        # Add all your frames here.
        list_of_screens = [ms.MainScreen]

        self.screens = {}

        ScreenHandler.load_screens(list_of_screens, self)
        ScreenHandler.show_screen("MainScreen", self)

class App(Tk):
    def __init__(self):
        super().__init__()

        self.title(TITLE)
        self.geometry('%dx%d+%d+%d' % (WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_X, WINDOW_Y))
        
        self.window = MainWindow(self)

        self.iconphoto(True, PhotoImage(file=FILE_ICON))

        self.resizable(0,0)
        self.mainloop()

try:
    App()
except Exception as e:
    import ctypes
    ctypes.windll.user32.MessageBoxW(0, f"An exception has occured. \n\nException:\n{repr(e)}\n{str(e)}\n\nCheck the traceback.txt for more details.", "Error", 0x10)

    with open('traceback.txt', 'w+') as f:
        traceback.print_exc(file=f)