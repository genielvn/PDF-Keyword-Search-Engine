from settings import *
from MainScreen import screen as ms
import traceback
import customtkinter as ctk

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode("system") 
        ctk.set_default_color_theme("blue") 

        self.title(TITLE)
        self.geometry('%dx%d+%d+%d' % (WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_X, WINDOW_Y))

        self.frame = ms.MainFrame(self)
        # self.iconphoto(True, PhotoImage(file=FILE_ICON))

        self.resizable(0,0)
        self.mainloop()

try:
    App()
    print("exited")
except Exception as e:
    import ctypes
    ctypes.windll.user32.MessageBoxW(0, f"An exception has occured. \n\nException:\n{repr(e)}\n{str(e)}\n\nCheck the traceback.txt for more details.", "Error", 0x10)

    with open('traceback.txt', 'w+') as f:
        traceback.print_exc(file=f)