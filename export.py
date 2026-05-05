import tkinter as tk
from tkinter import ttk, filedialog
import os

class Export(ttk.Frame):
    def __init__(self, parent, full_name, save_new_iamge):
        super().__init__(parent)
        
        # var
        self.name_string = tk.StringVar()
        self.path_string = tk.StringVar()
        self.file_kind = tk.StringVar(value='jpg')
        self.full_name = full_name

        # trace
        self.name_string.trace_add('write', self.update_final_name)
        self.path_string.trace_add('write', self.update_final_name)
        self.file_kind.trace_add('write', self.update_final_name)

        # name_entry
        name_frame = ttk.Frame(self)
        name_frame.pack(fill='x', padx=20, pady=10)

        name_frame.columnconfigure(1, weight=1)

        name_label = ttk.Label(name_frame, text='File Name:')
        name_label.grid(row=0, column=0, sticky='w', padx=(0, 10))

        name_entry = ttk.Entry(name_frame, textvariable=self.name_string)
        name_entry.grid(row=0, column=1, sticky='ew')

        # choose dir
        choose_dir_button = ttk.Button(self, text= 'Select Folder', command= self.choose_dir)
        choose_dir_button.pack()

        # path_entry
        path_label = ttk.Label(self, textvariable=self.path_string)
        path_label.pack()

        # jpg png
        frame = ttk.Frame(self)
        frame.pack()
        
        jpg_button = ttk.Radiobutton(frame, variable= self.file_kind, text= 'JPG', value= 'jpg')
        png_button = ttk.Radiobutton(frame, variable= self.file_kind, text= 'PNG', value= 'png')

        jpg_button.pack(side= 'left')
        png_button.pack(side= 'right')

        # finale name
        final_name = ttk.Label(self, textvariable= self.full_name)
        final_name.pack()

        # export
        export_button = ttk.Button(self, text="Export Image", command= save_new_iamge)
        export_button.pack(pady=20)

    def choose_dir(self):
        self.path_string.set(filedialog.askdirectory())

    def update_final_name(self, *args):
        full_name = os.path.join(self.path_string.get(), f'{self.name_string.get()}.{self.file_kind.get()}')
        full_name = full_name.replace('\\', '/')
        full_name = full_name.replace(' ', '_')
        self.full_name.set(full_name)