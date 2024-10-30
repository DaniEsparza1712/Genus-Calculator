# -*- coding: utf-8 -*-
"""
@author: Daniel Esparza

The MIT License
Copyright © 2024 Carlos Daniel Esparza Osuna

Permission is hereby granted, free of charge, to any person
obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software
without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute,
sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions: The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software. THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE
AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""

from tkinter import *
from tkinter import filedialog
from genus import process_file, show_file


def browse_files():
    filename = filedialog.askopenfilename(title="Select a File", filetypes=(("OBJ file",
                                                                             "*.obj*"),))
    genus = process_file(filename)
    result_lbl.config(text=f"GENUS {genus}", font="Arial")
    show_file(filename)


window = Tk()
window.title('Genus Calculator')
window.config(background="#22283d")
window.geometry("400x320")

frame = Frame(window)
frame.pack(fill="x", side=TOP, padx=15, pady=80)
frameB = Frame(window)
frameB.pack(fill="x", side=BOTTOM, padx=15, pady=50)

explore_btn = Button(frame, text="Select file", background="#525e87", foreground="#dce2f7",
                     font="Arial", command=browse_files)
explore_btn.pack(side=TOP, fill="x")

result_lbl = Label(frameB, text="...", background="#22283d", foreground="#dce2f7")
result_lbl.pack(side=TOP, fill="x")

window.mainloop()
