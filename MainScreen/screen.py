from tkinter import * 
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from settings import *
from algorithms import StringMatching
from algorithms import StringManipulate
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
        self.included_files = {}

        self.load_elements(canvas)

    def load_elements(self, canvas):
        self.txtbox_frame = Frame(canvas)

        self.txt_Content = Text(self.txtbox_frame, width=52, height=35)
        self.txt_Content.insert(END, "Click a file to preview.")
        self.txt_Content.config(state=DISABLED)
        self.scrbr_Content = Scrollbar(self.txtbox_frame)

        self.txt_Content.config(yscrollcommand = self.scrbr_Content.set)
        self.scrbr_Content.config(command=self.txt_Content.yview)

        self.txt_Content.pack(side=LEFT)
        self.scrbr_Content.pack(side=RIGHT, fill=Y)

        self.txtbox_frame.pack(padx=10, side=LEFT)

        # ==========
        
        self.listbox_frame = Frame(canvas)

        self.lst_Files = Listbox(self.listbox_frame, selectmode=SINGLE, width=85, height=18)
        self.lst_Files.bind('<Double-1>', self.open_pdf)
        self.lst_Files.bind('<<ListboxSelect>>', self.show_text)
        self.lst_Files.pack(padx=5, pady=10, side=LEFT)

        self.scrbr_Files = Scrollbar(self.listbox_frame)
        self.scrbr_Files.pack(side=RIGHT, fill=Y)

        self.lst_Files.config(yscrollcommand = self.scrbr_Files.set)
        self.scrbr_Files.config(command=self.lst_Files.yview)

        self.listbox_frame.pack(padx=0, pady=0, side=TOP)

        # ===========

        self.buttons_frame = Frame(canvas)

        self.btn_Browse = Button(self.buttons_frame, text="Add/Upload", command=lambda: threading.Thread(target=self.browse_files()).start, height=3, width=35, borderwidth=5)
        self.btn_Browse.pack()

        self.btn_Clear = Button(self.buttons_frame, text="Clear", command=lambda: self.clear_files(), height=3, width=35, borderwidth=5)
        self.btn_Clear.pack(pady=20)

        self.btn_Search = Button(self.buttons_frame, text="Search", command=lambda: self.search(), height=5, width=35, borderwidth=5)
        self.btn_Search.pack(pady=10)

        self.btn_Reset = Button(canvas, text="Reset", command=lambda: self.revert(), height=2, width=15, borderwidth=5)
        self.btn_Clear.place()

        self.buttons_frame.pack(padx=20, pady=0, side=RIGHT)

        # ==========

        self.search_include_frame = Frame(canvas)

        self.lbl_Include = Label(self.search_include_frame, text="Search Keywords:", anchor=W)
        self.lbl_Include.pack(anchor=W)

        self.txt_Include = Entry(self.search_include_frame, width=40)
        self.txt_Include.pack(pady=10)

        self.lbl_Include_bool = Label(self.search_include_frame, text="Booleans: ", anchor=W)
        self.lbl_Include_bool.pack(anchor=W)

        self.bool_Include = IntVar()
        self.rdbtn_Include_AND = Radiobutton(self.search_include_frame, text="AND", variable=self.bool_Include, value=0)
        self.rdbtn_Include_OR = Radiobutton(self.search_include_frame, text="OR", variable=self.bool_Include, value=1)
        self.rdbtn_Include_AND.pack(anchor=W)
        self.rdbtn_Include_OR.pack(anchor=W)

        self.lbl_Note = Label(self.search_include_frame, text="Multiple keywords must be separated \nwith commas.", anchor=W)
        self.lbl_Note.pack(side=BOTTOM, pady=15)

        self.lbl_Count = Label(self.search_include_frame, text=f"{len(self.included_files)}/{len(self.PDF_files)} shown.", anchor=W)
        self.lbl_Count.pack(side=BOTTOM, pady=15, anchor=W)

        self.search_include_frame.pack(pady=15, side=TOP)


        # ==========

        self.prg_Progress = ttk.Progressbar(canvas, orient=HORIZONTAL, length=200, mode="determinate", )
        self.lbl_Progress = Label(text="Loading Test...")

        # self.search_exclude_frame = Frame(canvas)

        # self.lbl_Exclude = Label(self.search_exclude_frame, text="Exclude the following keywords:", anchor=W)
        # self.lbl_Exclude.pack(pady=10)

        # self.txt_Exclude = Entry(self.search_exclude_frame, width=40)
        # self.txt_Exclude.pack()

        # self.search_exclude_frame.pack(pady=10, side=TOP)

        # self.search_exclude_bool_frame = Frame(canvas)

        # self.bool_Exclude = IntVar()
        # self.rdbtn_Exclude_AND = Radiobutton(self.search_exclude_bool_frame, text="AND", variable=self.bool_Exclude, value=0)
        # self.rdbtn_exclude_OR = Radiobutton(self.search_exclude_bool_frame, text="OR", variable=self.bool_Exclude, value=1)
        # self.rdbtn_Exclude_AND.pack(side=LEFT)
        # self.rdbtn_exclude_OR.pack(side=LEFT)

        # self.search_exclude_bool_frame.pack(side=TOP)

        # ==========

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
            self.update_progress(f"Loading {file_name}", (i/j)*100)
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
        self.revert()

    def update_list(self, files):
        self.lst_Files.delete(0, END)
        for file in files:
            self.lst_Files.insert(END, file)
        self.lbl_Count["text"] = f"{len(self.included_files)}/{len(self.PDF_files)} shown."

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
        self.txt_Include.delete(0, END)
        self.lbl_Count["text"] = f"{len(self.included_files)}/{len(self.PDF_files)} shown."

        # self.txt_Exclude.delete(0, END)
        self.hide_revert_button()

    def search(self):
        file_paths = self.lst_Files.get(0, END)
        if len(file_paths) == 0:
            messagebox.showwarning(title="Empty Search Files", message="There are no files to search. Please upload a file or click the reset button after search.")
            return
        
        keywords = StringManipulate.split_keywords(self.txt_Include.get())
        # excluded = StringManipulate.split_keywords(self.txt_Exclude.get())

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
            
            if self.bool_Include.get() == 0:
                for word in keywords:
                    if not StringMatching.search(current_file.content, word):
                        current_file.included = False
                        break
                    current_file.included = True
            else:
                for word in keywords:
                    self.update_progress(f"Searching {word} in {current_file.file_name}", (i/j)*100)
                    if StringMatching.search(current_file.content, word):
                        current_file.included = True
                        break
                    current_file.included = False

            if current_file.included:
                self.included_files[file] = current_file

            # AND_indicator = True if self.bool_Include.get() == 0 else False

            # for word in keywords:
            #     current_file.included = False
                
            #     self.update_progress(f"Searching {word} in {current_file.file_name}", (i/j)*100)
            #     keyword_found = StringMatching.search(current_file.content, word)
            #     if AND_indicator and not keyword_found:
            #         current_file.included = False
            #         break
            #     elif not AND_indicator and keyword_found:
            #         current_file.included = True
            #         break

            #     current_file.included = True

        messagebox.showinfo(title=f"Results", message=f"Search found {len(self.included_files)} result/s.")
        self.update_list(self.included_files)
        self.hide_progress()
        self.show_revert_button()
                
    def open_pdf(self, event):
        get_selected = self.lst_Files.curselection()
        file_name = self.lst_Files.get(get_selected)
        current_PDF = self.PDF_files[file_name]
        get_path = current_PDF.file_path
        os.startfile(get_path)

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

    def update_progress(self, text, percentage):
        self.prg_Progress["value"] = percentage
        self.lbl_Progress["text"] = text
        self.main.main_window.update_idletasks()

    def hide_progress(self):
        self.prg_Progress.place_forget()
        self.lbl_Progress.place_forget()

    def show_revert_button(self):
        self.btn_Reset.place(x=840, y=240)

    def hide_revert_button(self):
        self.btn_Reset.place_forget()
        
    def revert(self):
        self.included_files = self.PDF_files
        self.set_all_included()
        self.update_list(self.PDF_files)
        self.hide_revert_button()
        self.lbl_Count["text"] = f"{len(self.included_files)}/{len(self.PDF_files)} shown."
        
    def set_all_included(self):
        for file in self.PDF_files:
            self.PDF_files[file].included = True