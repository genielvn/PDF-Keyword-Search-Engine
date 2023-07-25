from tkinter import * 
from tkinter import filedialog
from tkinter import messagebox
from tkinter import font
from algorithms import StringMatching
from algorithms import StringManipulate
from pdfclass import PDF
from settings import *
import customtkinter as ctk
import threading
import os

class MainFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.master = master

        self.PDF_files = {}
        self.included_files = {}

        self.load_elements() 

    def load_elements(self):
        self.txt_Content = ctk.CTkTextbox(master=self.master, width=400, height=570)
        self.txt_Content.insert("end", "Click a file to preview.")
        self.txt_Content.configure(state="disabled")
        self.txt_Content.place(x=10, y=15)

        # ==========
        self.listbox_frame = Frame(self.master)
        
        listbox_font = font.Font(size=15)
        self.lst_Files = Listbox(self.listbox_frame, width=49, height=13, selectmode=SINGLE, background="#1e1e1e", foreground="white", borderwidth=0, highlightthickness=0, font=listbox_font)
        self.lst_Files.bind('<Double-1>', self.open_pdf)
        self.lst_Files.bind('<<ListboxSelect>>', self.show_text)
        self.lst_Files.pack(side=LEFT, fill=Y)

        self.scrbr_Files = Scrollbar(self.listbox_frame)
        self.scrbr_Files.pack(side=RIGHT, fill=Y)

        self.lst_Files.config(yscrollcommand = self.scrbr_Files.set)
        self.scrbr_Files.config(command=self.lst_Files.yview)

        self.listbox_frame.place(x=420, y=15)

        # ==========
        
        self.btn_Browse = ctk.CTkButton(master=self.master, text="Add/Upload", command=lambda: threading.Thread(target=self.browse_files()).start, width=220, height=55)
        self.btn_Browse.place(x=760, y=340)

        self.btn_Clear = ctk.CTkButton(master=self.master, text="Clear", command=lambda: self.clear_files(), width=220, height=60)
        self.btn_Clear.place(x=760, y=405)

        self.btn_Search = ctk.CTkButton(master=self.master, text="Search", command=lambda: self.search(), width=220, height=90)
        self.btn_Search.place(x=760, y=480)

        self.btn_Reset = ctk.CTkButton(master=self.master, text="Reset", command=lambda: self.revert())

        # ==========

        self.lbl_Keywords = ctk.CTkLabel(master=self.master, text="Search Keywords:", anchor=W)
        self.lbl_Keywords.place(x=420, y=340)

        self.txt_Keywords = ctk.CTkEntry(master=self.master, width=320)
        self.txt_Keywords.place(x=420, y=370)

        self.lbl_Keywords_bool = ctk.CTkLabel(master=self.master, text="Booleans:", anchor=W)
        self.lbl_Keywords_bool.place(x=420, y=420)

        self.bool_Keywords = IntVar()
        self.rdbtn_Keywords_AND = ctk.CTkRadioButton(master=self.master, text="AND", variable=self.bool_Keywords, value=0)
        self.rdbtn_Keywords_OR = ctk.CTkRadioButton(master=self.master, text="OR", variable=self.bool_Keywords, value=1)
        self.rdbtn_Keywords_AND.place(x=420, y=450)
        self.rdbtn_Keywords_OR.place(x=420, y=480)

        self.lbl_Count = ctk.CTkLabel(master=self.master, text=f"{len(self.included_files)}/{len(self.PDF_files)} shown.", anchor=W)
        self.lbl_Count.place(x=420, y=520)

        self.lbl_Note = ctk.CTkLabel(master=self.master, text="* Multiple keywords must be separated with commas.", anchor=W)
        self.lbl_Note.place(x=420, y=550)

        # ==========

        self.prg_Progress = ctk.CTkProgressBar(master=self.master, width=200, mode="determinate")
        self.lbl_Progress = ctk.CTkLabel(master=self.master, text="Loading Test...")


    def browse_files(self):
        file_paths = filedialog.askopenfilenames(filetypes=[("PDF Files", "*.pdf")])
        if len(file_paths) == 0:
            return
        self.load_files(file_paths)

    def load_files(self, file_paths):
        i = 0
        j = len(file_paths)
        self.show_progress()
        for file in file_paths:
            i += 1
            file_name = os.path.basename(file)
            name_only, ext = os.path.splitext(file_name)

            self.update_progress(f"Loading {file_name}", (i/j))
            if self.duplicate(name_only):
                res = messagebox.askquestion(title="Duplicate Found", message=f"{file_name} is a duplicate. Do you wish to add it on the list?", icon='warning')
                if res == 'no':
                    continue
                self.PDF_files[name_only].duplicate += 1
                name_only = f"{name_only} ({(self.PDF_files[name_only].duplicate)})"
            self.PDF_files[name_only] = PDF(file, file_name)
        self.included_files = self.PDF_files
        self.hide_progress()
        self.update_list(self.PDF_files)
        # self.revert()

    def open_pdf(self, event):
        get_selected = self.lst_Files.curselection()
        file_name = self.lst_Files.get(get_selected)
        current_PDF = self.PDF_files[file_name]
        get_path = current_PDF.file_path
        os.startfile(get_path)

    def update_list(self, files):
        self.lst_Files.delete(0, END)
        for file in files:
            self.lst_Files.insert(END, file)
        self.lbl_Count.configure(text= f"{len(self.included_files)}/{len(self.PDF_files)} shown.")

    def duplicate(self, file):
        if file in self.lst_Files.get(0, END):
            return True
        return False

    def clear_files(self):
        if len(self.PDF_files) == 0:
            return
        
        res = messagebox.askquestion(title="Clear", message=f"{len(self.PDF_files)} file/s will be removed on the list. Do you wish to continue? \n(You can reset the list after search instead of uploading the files again.)", icon='warning')
        if res == 'no':
            return
        
        self.change_text("Click a file to preview.")
        self.lst_Files.delete(0, END)
        self.PDF_files = {}
        self.included_files = {}
        self.txt_Keywords.delete(0, END)
        self.lbl_Count.configure(text= f"{len(self.included_files)}/{len(self.PDF_files)} shown.")
        self.hide_revert_button()

    def search(self):
        file_paths = self.lst_Files.get(0, END)
        if len(file_paths) == 0:
            messagebox.showwarning(title="Empty Search Files", message="There are no files to search. Please upload a file or click the reset button after search.")
            return
        
        keywords = StringManipulate.split_keywords(self.txt_Keywords.get())

        if len(keywords) == 0:
            messagebox.showwarning(title="Empty Search Keyword", message="Please input at least one keyword to search.")
            return

        self.included_files = {}

        i = 0
        j = len(file_paths)
        self.show_progress()

        for file in file_paths:
            i += 1

            current_file = self.PDF_files[file]

            current_file.included = True
            
            if self.bool_Keywords.get() == 0:
                for word in keywords:
                    if not StringMatching.search(current_file.content, word):
                        current_file.included = False
                        break
                    current_file.included = True
            else:
                for word in keywords:
                    self.update_progress(f"Searching {word} in {current_file.file_name}", (i/j))
                    if StringMatching.search(current_file.content, word):
                        current_file.included = True
                        break
                    current_file.included = False

            if current_file.included:
                self.included_files[file] = current_file

        messagebox.showinfo(title=f"Results", message=f"Search found {len(self.included_files)} result/s.")
        self.update_list(self.included_files)
        self.hide_progress()
        self.show_revert_button()

    def show_text(self, event):
        get_selected = self.lst_Files.curselection()

        path = self.lst_Files.get(get_selected)
        object = self.PDF_files[path]
        text = object.get_text()

        self.change_text(text)

    def change_text(self, text):
        self.txt_Content.configure(state="normal")
        self.txt_Content.delete('1.0', "end")
        self.txt_Content.insert("end", text)
        self.txt_Content.configure(state="disabled")

    def show_progress(self):
        self.prg_Progress.place(x=WINDOW_WIDTH/2, y=WINDOW_HEIGHT/2, anchor=CENTER)
        self.lbl_Progress.place(x=WINDOW_WIDTH/2, y=(WINDOW_HEIGHT/2)+30, anchor=CENTER)

    def update_progress(self, text, percentage):
        self.prg_Progress.set(percentage)
        self.lbl_Progress.configure(text=text)
        self.master.update_idletasks()

    def hide_progress(self):
        self.prg_Progress.place_forget()
        self.lbl_Progress.place_forget()

    def show_revert_button(self):
        self.btn_Reset.place(x=810, y=290)

    def hide_revert_button(self):
        self.btn_Reset.place_forget()
        
    def revert(self):
        self.included_files = self.PDF_files
        self.set_all_included()
        self.update_list(self.PDF_files)
        self.hide_revert_button()
        self.lbl_Count.configure(text= f"{len(self.included_files)}/{len(self.PDF_files)} shown.")

    def set_all_included(self):
        for file in self.PDF_files:
            self.PDF_files[file].included = True

