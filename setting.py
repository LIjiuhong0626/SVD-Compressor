import tkinter as tk
from tkinter import ttk

class Setting(ttk.Frame):
    def __init__(self, parent, choose_func, path_string, compute, k_int, creat_new_image, ratio_func, data):
        super().__init__(parent)
        self.ratio = tk.StringVar(value= 'Energy Retained')
        self.ratio_func = ratio_func
        self.s = None

        # grid
        self.rowconfigure((0, 2), weight= 2)
        self.rowconfigure((1, 3), weight= 1)
        self.columnconfigure(0, weight= 1)

        # choose image
        choose_image_frame = ttk.Frame(self)
        choose_image_frame.grid(column= 0, row= 0, sticky= 'nesw')

        choose_button = ttk.Button(choose_image_frame, text= 'Select Image', command= choose_func)
        choose_button.pack()

        path_label = ttk.Label(choose_image_frame, textvariable=path_string)
        path_label.pack(expand=True)

        # svd
        svd_frame = ttk.Frame(self)
        svd_frame.grid(column= 0, row= 1, sticky= 'nesw')

        svd_button = ttk.Button(svd_frame, text= 'Compute SVD', command= compute)
        svd_button.pack()

        # k_frame
        self.k_int = k_int
        self.k_int.trace_add('write', self.limit_int)

        k_frame = ttk.Frame(self)
        k_frame.grid(column= 0, row= 2, sticky= 'ew')

        k_frame.columnconfigure((0, 1), weight= 1, uniform= 'a')
        k_frame.rowconfigure((0, 1, 2), weight= 1, uniform= 'a')

        k_label = ttk.Label(k_frame, text= 'Target K-value')
        k_label.grid(column= 0, row= 0, sticky= 'nesw')

        k_entry = ttk.Entry(k_frame, textvariable=self.k_int)
        k_entry.grid(column= 1, row= 0, sticky= 'we')

        self.k_scale = ttk.Scale(k_frame, variable= self.k_int, from_= 0, to= 100, command= self.func)
        self.k_scale.grid(column= 0, columnspan=2, row= 1, sticky= 'nesw')
        
        self.ratio_display = ttk.Label(k_frame, textvariable= self.ratio)
        self.ratio_display.grid(column= 0, columnspan= 2, row=3, sticky= 'nesw')

        # creat new image
        new_image = ttk.Frame(self)
        new_image.grid(column=0, row=4, sticky= 'nesw')

        creat_image_button = ttk.Button(new_image, text='Generate Preview', command=creat_new_image)
        creat_image_button.pack()
    
    def limit_int(self, *args):# k_int 变了就变了
        try:
            k_val = self.k_int.get()
        except tk.TclError:
            return

        try:
            k = int(k_val)
            if self.s is not None:
                res = self.ratio_func(self.s, k)
                self.ratio.set(f"Energy Retained: {res}")
        except (ValueError, TypeError):
            pass
     
    def func(self, value):
        value = float(value)
        k = int(value)
        self.k_int.set(k)