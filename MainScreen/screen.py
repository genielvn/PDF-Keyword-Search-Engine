from tkinter import * 
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from settings import *
from screenhandler import ScreenHandler
from algorithms import Algorithms
from pdfclass import PDF
import threading
import os 

class MainScreen(Frame):
    def __init__(self, parent, main):
        Frame.__init__(self, parent)

        self.main = main
        canvas = Canvas(self, height=WINDOW_HEIGHT, width=WINDOW_WIDTH, bd=0, highlightthickness=0, relief="ridge")
        canvas.place(x=0,y=0)
        
        self.PDF_files = {}

        self.load_elements(canvas)

    def load_elements(self, canvas):
        self.listbox_frame = Frame(canvas)

        self.lst_Files = Listbox(self.listbox_frame, selectmode=SINGLE, width=160, height=18)
        self.lst_Files.bind('<Double-1>', self.open_pdf)
        self.lst_Files.bind('<<ListboxSelect>>', self.show_text)
        self.lst_Files.pack(padx=10, pady=10, side=LEFT)

        self.scrbr_Files = Scrollbar(self.listbox_frame)
        self.scrbr_Files.pack(side=RIGHT, fill=Y)

        self.lst_Files.config(yscrollcommand = self.scrbr_Files.set)
        self.scrbr_Files.config(command=self.lst_Files.yview)

        self.listbox_frame.pack(padx=0, pady=0, side=TOP)

        # ===========

        self.buttons_frame = Frame(canvas)

        self.btn_Browse = Button(self.buttons_frame, text="Add", command=lambda: threading.Thread(target=self.browse_files()).start, height=3, width=35, borderwidth=5)
        self.btn_Browse.pack()

        self.btn_Clear = Button(self.buttons_frame, text="Clear", command=lambda: self.clear_files(), height=3, width=35, borderwidth=5)
        self.btn_Clear.pack(pady=20)

        self.btn_Search = Button(self.buttons_frame, text="Search", command=lambda: self.search(), height=5, width=35, borderwidth=5)
        self.btn_Search.pack(pady=10)

        self.buttons_frame.pack(padx=20, pady=0, side=RIGHT)

        # ==========

        self.txtbox_frame = Frame(canvas)

        self.txt_Content = Text(self.txtbox_frame, width=50, height=16)
        self.txt_Content.insert(END, "Click a file to preview.")
        self.txt_Content.config(state=DISABLED)
        self.scrbr_Content = Scrollbar(self.txtbox_frame)

        self.txt_Content.config(yscrollcommand = self.scrbr_Content.set)
        self.scrbr_Content.config(command=self.txt_Content.yview)

        self.txt_Content.pack(side=LEFT)
        self.scrbr_Content.pack(side=RIGHT, fill=Y)

        self.txtbox_frame.pack(padx=10, side=LEFT)

        # ==========

        self.search_include_frame = Frame(canvas)

        self.lbl_Include = Label(self.search_include_frame, text="Include the following keywords:", anchor=W)
        self.lbl_Include.pack(pady=10)

        self.txt_Include = Entry(self.search_include_frame, width=40)
        self.txt_Include.pack()

        self.search_include_frame.pack(pady=10, side=TOP)

        # self.search_include_bool_frame = Frame(canvas)

        # self.bool_Include = IntVar()
        # self.rdbtn_Include_AND = Radiobutton(self.search_include_bool_frame, text="AND", variable=self.bool_Include, value=0)
        # self.rdbtn_Include_OR = Radiobutton(self.search_include_bool_frame, text="OR", variable=self.bool_Include, value=1)
        # self.rdbtn_Include_AND.pack(side=LEFT)
        # self.rdbtn_Include_OR.pack(side=LEFT)

        # self.search_include_bool_frame.pack(side=TOP)

        # ==========

        self.search_exclude_frame = Frame(canvas)

        self.lbl_Exclude = Label(self.search_exclude_frame, text="Exclude the following keywords:", anchor=W)
        self.lbl_Exclude.pack(pady=10)

        self.txt_Exclude = Entry(self.search_exclude_frame, width=40)
        self.txt_Exclude.pack()

        self.search_exclude_frame.pack(pady=10, side=TOP)

        # self.search_exclude_bool_frame = Frame(canvas)

        # self.bool_Exclude = IntVar()
        # self.rdbtn_Exclude_AND = Radiobutton(self.search_exclude_bool_frame, text="AND", variable=self.bool_Exclude, value=0)
        # self.rdbtn_exclude_OR = Radiobutton(self.search_exclude_bool_frame, text="OR", variable=self.bool_Exclude, value=1)
        # self.rdbtn_Exclude_AND.pack(side=LEFT)
        # self.rdbtn_exclude_OR.pack(side=LEFT)

        # self.search_exclude_bool_frame.pack(side=TOP)

        # ==========

        self.lbl_Note = Label(canvas, text="Multiple keywords must be separated \nwith commas.", anchor=W)
        self.lbl_Note.pack(side=BOTTOM, pady=2)

        # ===========

        self.prg_Progress = ttk.Progressbar(canvas, orient=HORIZONTAL, length=200, mode="determinate", )
        self.lbl_Progress = Label(text="Loading Test...")


    def browse_files(self):
        file_paths = filedialog.askopenfilenames(filetypes=[("PDF Files", "*.pdf")])
        self.show_progress()
        i = 0
        j = len(file_paths)
        for file in file_paths:
            i += 1
            file_name = os.path.basename(file)
            self.update_progress(file_name, (i/j)*100)
            if self.duplicate(file):
                messagebox.showinfo(title="Duplicate Found", message=f"{file_name} is a duplicate. It will not be added on the list.")
                continue
            self.PDF_files[file] = PDF(file, file_name)
            self.lst_Files.insert(END, file)
        self.hide_progress()

    def duplicate(self, file):
        if file in self.lst_Files.get(0, END):
            return True
        return False

    def clear_files(self):
        self.change_text("")
        self.lst_Files.delete(0, END)
        self.PDF_files = {}

    def search(self):
        file_paths = self.lst_Files.get(0, END)

        included = Algorithms.split_keywords(self.txt_Include.get())
        excluded = Algorithms.split_keywords(self.txt_Exclude.get())

        for file in file_paths:
            current_file = self.PDF_files[file]
            for word in excluded:
                if Algorithms.search(current_file.content, word):
                    current_file.included = False
                    return
                current_file.included = True
            for word in included:
                if not Algorithms.search(current_file.content, word):
                    current_file.included = False
                    break
                current_file.included = True
                
    def open_pdf(self, event):
        get_selected = self.lst_Files.curselection()
        path = self.lst_Files.get(get_selected)
        os.startfile(path)

    def show_text(self, event):
        get_selected = self.lst_Files.curselection()

        path = self.lst_Files.get(get_selected)
        object = self.PDF_files[path]
        text = object.get_text()

        self.change_text(text)
    
    def change_text(self, text):
        self.txt_Content.config(state=NORMAL)
        self.txt_Content.delete('1.0', END)
        self.txt_Content.insert(END, text)
        self.txt_Content.config(state=DISABLED)
    
    def show_progress(self):
        self.prg_Progress.place(x=WINDOW_WIDTH/2, y=WINDOW_HEIGHT/2, anchor=CENTER)
        self.lbl_Progress.place(x=WINDOW_WIDTH/2, y=(WINDOW_HEIGHT/2)+30, anchor=CENTER)

    def update_progress(self, file_name, percentage):
        self.prg_Progress["value"] = percentage
        self.lbl_Progress["text"] = f"Loading {file_name}"
        self.main.main_window.update_idletasks()

    def hide_progress(self):
        self.prg_Progress.place_forget()
        self.lbl_Progress.place_forget()