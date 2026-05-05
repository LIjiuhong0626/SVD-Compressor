import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from setting import *
from export import *
from PIL import Image
import svd
from pillow_heif import register_heif_opener

class App(tk.Tk):
    def __init__(self):
        # setting
        super().__init__()
        self.geometry('400x600')
        self.title('SVD-Based Image Reconstruction')
        register_heif_opener() 

        # var
        self.path_string = tk.StringVar()
        self.k_int = tk.IntVar()
        self.original_image = None
        self.new_image = None
        self.save_path = tk.StringVar(value = 'full_name')
        self.u, self.s, self.vt =0, 0, 0
        self.data = [self.u, self.s, self.vt]
        

        # weidgets
        notebook = ttk.Notebook(self)
        notebook.pack(expand= True, fill= 'both')
        self.setting = Setting(notebook, self.choose_func, self.path_string, self.compute,self.k_int, self.creat_new_image, svd.ratio, self.data)
        self.export = Export(notebook, self.save_path, self.save_new_image)

        notebook.add(self.setting, text= 'Setting')
        notebook.add(self.export, text= 'Export')

        # run
        self.mainloop()

    def choose_func(self):
        file_path = filedialog.askopenfilename(
            title="选择图片",
            initialdir="/",  # 初始打开的目录
            filetypes=(("JPEG files", "*.jpg"), ("PNG files", "*.png"), ("HEIC files", "*.heic"), ("All files", "*.*"))
        )

        self.path_string.set(file_path)
        self.original_image = Image.open(file_path)

        try:
            self.export.name_string.set(os.path.basename(file_path).split('.')[0])
        except Exception:
            self.export.name_string.set('file name')

        # print(self.original_image.filename)

    def compute(self):
        try:
            self.u, self.s, self.vt = svd.svd(self.original_image)
            messagebox.showinfo('成功','计算完成')
            # print(self.u, self.s, self.vt)
            k_max = len(self.s[0])
            self.setting.k_scale.configure(to=k_max)
            self.setting.s = self.s
        except AttributeError:
            messagebox.showinfo("警告", "请先选择图片")

    def creat_new_image(self):
        try:
            self.new_image = svd.stack(self.u, self.s, self.vt, self.k_int.get())
            self.new_image.show()
        except Exception:
            messagebox.showinfo("警告", "请先计算")

    def save_new_image(self):
        if self.new_image is not None:
            if not os.path.dirname(self.save_path.get()):
                messagebox.showwarning("警告", "请先选择保存目录")
                return
            self.new_image.save(self.save_path.get())
            messagebox.showinfo("成功", "图片已保存")
        else:
            messagebox.showwarning("警告", "请先生成预览图")

app = App()