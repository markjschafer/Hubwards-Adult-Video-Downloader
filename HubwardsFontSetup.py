'''
MIT License

Copyright (c) 2021 Mark Schafer

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''
import tkinter as tk
from tkinter import ttk
from tkinter import Tk, font
from tkinter.ttk import Button, Label
import HubwardsConst as AppC
import os
import sys

class App:
    def __init__(self, master: Tk) -> None:
        self.master = master
        self.Ffamily = font.families()
        self.counter = 0
        if AppC.FontFamily != "":
            self.family = AppC.FontFamily
        else:
            self.family = self.Ffamily[self.counter]
        self.size = AppC.FontSize

        # Creating a Font object of "TkDefaultFont"
        self.defaultFont = font.nametofont("TkDefaultFont")

        # Overriding default-font with custom settings
        # i.e changing font-family, size and weight
        self.defaultFont.configure(family=self.family,
                                size=19,
                                weight=font.BOLD)

        # Label widget
        self.label = Label(TAB5_TOP, text="")
        self.label.grid(row=1, column=1)
        # Button widget
        self.btn = Button(TAB5_TOP, text="Next Font Family", command=self.next)
        self.btn.grid(row=2, column=2, columnspan=2)

        self.btn = Button(TAB5_TOP, text="Increase Size", command=self.up)
        self.btn.grid(row=2, column=4) #, columnspan=2)

        self.btn = Button(TAB5_TOP, text="Decrease Size", command=self.down)
        self.btn.grid(row=2, column=5) #, columnspan=2)

        self.label1 = Label(TAB5_TOP, text=self.family+"("+str(self.size)+")")
        self.label1.grid(row=2, column=6, columnspan=2)

        self.btn = Button(TAB5_TOP, text="Save Font", command=self.Sfont)
        self.btn.grid(row=2, column=9) #, columnspan=2)

        self.btn = Button(TAB5_TOP, text="Save Size", command=self.Ssize)
        self.btn.grid(row=2, column=10) #, columnspan=2)

    def Sfont(self):
        os.rename("PornhubConst.py", "PornhubConst.out")
        fout = open("PornhubConst.py", "w")
        fin = open("PornhubConst.out", "r")
        for line in fin:
            if "FontFamily" in line:
                fout.write("FontFamily = '"+self.family+"'\n")
            else:
                fout.write(line)
        fin.close()
        fout.close()
        os.remove("PornhubConst.out")

    def Ssize(self):
        os.rename("PornhubConst.py", "PornhubConst.out")
        fout = open("PornhubConst.py", "w")
        fin = open("PornhubConst.out", "r")
        for line in fin:
            if "FontSize" in line:
                fout.write("FontSize = "+str(self.size)+"\n")
            else:
                fout.write(line)
        fin.close()
        fout.close()
        os.remove("PornhubConst.out")

    def up(self):
        self.size += 2
        self.label1['text'] = self.family+"("+str(self.size)+")"
        self.defaultFont.configure(family=self.family,
                                size=self.size,
                                weight=font.BOLD)

    def down(self):
        self.size -= 2
        self.label1['text'] = self.family+"("+str(self.size)+")"
        self.defaultFont.configure(family=self.family,
                                size=self.size,
                                weight=font.BOLD)

    def next(self):
        self.counter += 1
        self.family = self.Ffamily[self.counter]
        self.label1['text'] = self.family+"("+str(self.size)+")"
        self.defaultFont.configure(family=self.family,
                                size=self.size,
                                weight=font.BOLD)




if __name__ == "__main__":
    # Top level widget
    root = Tk()
    style = ttk.Style(root)
    root.tk.call('source', AppC.themePath)
    ttk.Style().theme_use(AppC.styleTheme)

    TAB5_PANEV = ttk.PanedWindow(root, orient=tk.VERTICAL, width=1900, height=1050)
    TAB5_PANEV.pack(fill='both', expand=True)
    TAB5_TOP = ttk.Label(TAB5_PANEV)
    TAB5_PANEV.add(TAB5_TOP, weight=1)
    TAB5_BOT = ttk.Label(TAB5_PANEV)
    TAB5_PANEV.add(TAB5_BOT, weight=3)

    # Setting app title
    root.title("Changing Default Font")


#    print(font.names())
    app = App(root)

    # Mainloop to run application
    # infinitely
    root.mainloop()
