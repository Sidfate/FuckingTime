# !/usr/bin/env python
# encoding: utf-8
from Tkinter import *
from PIL import ImageTk, Image, ImageFilter
import tkFileDialog
import tkMessageBox
import webbrowser
import copy


def action(deal):
    def deco(self):
        self.history.append(copy.deepcopy(self.image))
        deal(self)
        self.menu.winfo_children()[1].entryconfig(0, state=NORMAL)
        self.show_img()
        return deal

    return deco


class Power:
    def __init__(self, tk):
        self.root = tk
        self.menu = None
        self.main = None
        self.image = None
        self.history = []
        self.create_ui()

    def create_ui(self):
        menu_bar = Menu(self.root)
        # [file]
        file_menu = Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Open", command=self.open_img)
        file_menu.add_command(label="Save", command=self.save, state=DISABLED)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        menu_bar.add_cascade(label="File", menu=file_menu)

        # [edit]
        edit_menu = Menu(menu_bar, tearoff=0)
        edit_menu.add_command(label="Undo", command=self.undo, state=DISABLED)
        edit_menu.add_separator()
        edit_menu.add_command(label="Thumb", command=self.thumb, state=DISABLED)
        edit_menu.add_command(label="Blur", command=self.blur, state=DISABLED)
        # [edit] [rotate]
        rotate_menu = Menu(edit_menu, tearoff=0)
        rotate_menu.add_command(label="X", command=self.rotate_x, state=DISABLED)
        rotate_menu.add_command(label="Y", command=self.rotate_y, state=DISABLED)
        edit_menu.add_cascade(label="Rotate", menu=rotate_menu, state=DISABLED)
        edit_menu.add_command(label="Enhance", command=self.enhance, state=DISABLED)
        menu_bar.add_cascade(label="Edit", menu=edit_menu)

        # [help]
        help_menu = Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="Course", command=Power.course)
        help_menu.add_command(label="About...", command=Power.about)
        menu_bar.add_cascade(label="Help", menu=help_menu)

        edit_menu.rotate_menu = rotate_menu
        menu_bar.file_menu = file_menu
        menu_bar.edit_menu = edit_menu
        menu_bar.help_menu = help_menu

        self.menu = menu_bar
        self.main = Label(self.root, text="hello world", width=50, height=10)
        self.main.pack()
        self.root.config(menu=menu_bar)
        self.root.title("Power")

    def run(self):
        self.root.mainloop()

    def open_img(self):
        filename = tkFileDialog.askopenfilename(initialdir='E:/sidfate/py')
        if filename:
            self.menu.file_menu.entryconfig(1, state=NORMAL)
            for index in range(2, 6):
                self.menu.edit_menu.entryconfig(index, state=NORMAL)
                if index == 4:
                    self.menu.edit_menu.rotate_menu.entryconfig(0, state=NORMAL)
                    self.menu.edit_menu.rotate_menu.entryconfig(1, state=NORMAL)
            self.image = Image.open(filename)
            self.show_img()

    def save(self):
        filename = tkFileDialog.asksaveasfilename(initialdir='E:/sidfate/py')
        if filename:
            self.image.save(filename, 'jpeg')

    def show_img(self):
        img = ImageTk.PhotoImage(self.image)
        self.main.configure(text="", width=0, height=0, image=img)
        self.root.update_idletasks()
        self.run()

    @action
    def thumb(self):
        w, h = self.image.size
        self.image.thumbnail((w // 2, h // 2))

    @action
    def blur(self):
        self.image = self.image.filter(ImageFilter.BLUR)

    @action
    def rotate_x(self):
        # x-axial reversal
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)

    @action
    def rotate_y(self):
        # y-axial reversal
        self.image = self.image.transpose(Image.FLIP_TOP_BOTTOM)

    @action
    def enhance(self):
        self.image = self.image.filter(ImageFilter.DETAIL)

    def undo(self):
        his_len = len(self.history)
        if his_len == 1:
            self.menu.edit_menu.entryconfig(0, state=DISABLED)
        self.image = self.history.pop(his_len-1)
        self.show_img()

    @staticmethod
    def course():
        url = "http://121.41.44.79/category/python/tk/"
        webbrowser.open(url, new=0, autoraise=True)

    @staticmethod
    def about():
        tkMessageBox.showinfo("About Power", "Hello World")


root = Tk()
power = Power(root)
power.run()
