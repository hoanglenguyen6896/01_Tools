#!python3

import tkinter
from tkinter import font
from tkinter import filedialog
from tkinter import messagebox

import os
import subprocess

import pyresize

WIN_X=550
WIN_Y=300

def _row(row):
    ROW_MULTI = 20
    return row*ROW_MULTI

def _col(col):
    COL_MUL = 10
    return col*COL_MUL

resize_app = tkinter.Tk()
resize_app.title("Resize Image")
resize_app.geometry(f"{WIN_X}x{WIN_Y}")
resize_app.resizable(True, True)
resize_app.bind('<Escape>', lambda e, w=resize_app: w.destroy())
esc_lable = tkinter.Label(resize_app,
                            text="Press Escape key on keyboard to close this window.",
                            font=font.Font(size=12)).place(x=_col(8), y=_row(0))

# Input path
input_lable = tkinter.Label(resize_app, text="Input:", font=font.Font(size=12))
input_lable.place(x=0, y=_row(2))

input_entry = tkinter.Entry(resize_app, width=60)
input_entry.place(x=_col(6), y=_row(2.2))
input_entry.insert(0, pyresize.IN_IMG_DIR)
input_entry.xview_moveto(fraction=1)

def input_browse_button_action():
    # Allow user to select a directory and store it in global var
    # called folder_path
    filename = filedialog.askdirectory()
    if filename:
        input_entry.delete(0, tkinter.END)
        input_entry.insert(0, filename)

input_browse_button = tkinter.Button(text="Browse", command=input_browse_button_action)
input_browse_button.place(x=_col(45), y=_row(2))

def input_open_button_action():
    # Allow user to select a directory and store it in global var
    # called folder_path
    url = input_entry.get()
    url = url.replace("/", "\\")
    print(url)
    if os.path.isdir(url):
        subprocess.run(["explorer", url])
    else:
        messagebox.showerror("Error", f"Invalid input path {input_entry.get()}")
input_open_button = tkinter.Button(text="Open", command=input_open_button_action)
input_open_button.place(x=_col(50), y=_row(2))

# Out path
output_lable = tkinter.Label(resize_app, text="Output:", font=font.Font(size=12))
output_lable.place(x=0, y=_row(4))

output_entry = tkinter.Entry(resize_app, width=60)
output_entry.place(x=_col(6), y=_row(4.2))
output_entry.insert(0, pyresize.OUT_IMG_DIR)
output_entry.xview_moveto(fraction=1)

def output_browse_button_action():
    # Allow user to select a directory and store it in global var
    # called folder_path
    filename = filedialog.askdirectory()
    if filename:
        output_entry.delete(0, tkinter.END)
        output_entry.insert(0, filename)

output_browse_button = tkinter.Button(text="Browse", command=output_browse_button_action)
output_browse_button.place(x=_col(45), y=_row(4))

def output_open_action():
    # Allow user to select a directory and store it in global var
    # called folder_path
    url = output_entry.get()
    url = url.replace("/", "\\")
    print(url)
    if os.path.isdir(url):
        subprocess.run(["explorer", url])
    else:
        messagebox.showerror("Error", f"Invalid output path {output_entry.get()}")
output_open_button = tkinter.Button(text="Open", command=output_open_action)
output_open_button.place(x=_col(50), y=_row(4))

# Author
def author_select_button_action():
    if author_check_var.get() == 1:
        author_entry.config(state="normal")
    else:
        author_entry.config(state="disable")
author_check_var = tkinter.BooleanVar()
author_check_button = tkinter.Checkbutton(resize_app,
                                text="Author",
                                variable=author_check_var,
                                onvalue=1, offvalue=0,
                                command=author_select_button_action)
author_check_button.place(x=_col(0), y=_row(6))

author_entry = tkinter.Entry(resize_app, width=20)
author_entry.place(x=_col(8), y=_row(6.2))
author_entry.insert(0, "")
author_entry.xview_moveto(fraction=1)
if author_check_var.get() == 1:
    author_entry.config(state="normal")
else:
    author_entry.config(state="disable")

# Logo
def logo_select_action():
    if logo_check_var.get() == 1:
        logo_entry.config(state="normal")
    else:
        logo_entry.config(state="disable")

logo_check_var = tkinter.BooleanVar()
logo_check_button = tkinter.Checkbutton(resize_app,
                                text="Add logo",
                                variable=logo_check_var,
                                onvalue=1, offvalue=0,
                                command=logo_select_action)
logo_check_button.place(x=_col(0), y=_row(8))

logo_entry = tkinter.Entry(resize_app, width=50)
logo_entry.place(x=_col(8), y=_row(8.2))
logo_entry.insert(0, pyresize.LOGO_PATH + "/yody.png")
logo_entry.xview_moveto(fraction=1)
if logo_check_var.get() == 1:
    logo_entry.config(state="normal")
else:
    logo_entry.config(state="disable")

def logo_browse_button_action():
    # Allow user to select a directory and store it in global var
    # called folder_path
    if logo_check_var.get() == 1:
        filename = filedialog.askopenfilename()
        if filename:
            logo_entry.delete(0, tkinter.END)
            logo_entry.insert(0, filename)
logo_browse_button = tkinter.Button(text="Browse", command=logo_browse_button_action)
logo_browse_button.place(x=_col(40), y=_row(8))

# Add execute button
def image_process_button_action():
    _author = None
    _logo = None
    if author_check_var.get() == 1:
        _author = author_entry.get()
    else:
        _author == None
    if logo_check_var.get() == 1:
        _logo = logo_entry.get()
        if not os.path.isfile(_logo):
            messagebox.showerror("Error", (_logo, "does not exist or is not a file"))
    else:
        _logo == None

    if not os.path.isdir(input_entry.get()):
        messagebox.showerror("Error", "Invalid input path")
    else:
        tmp = pyresize.all_image_stuff(
            input_entry.get(),
            output_entry.get(),
            _author,
            _logo
        )
        err = tmp.resize_all_image_in_input_subdirs()
        if err == 0:
            messagebox.showinfo("Info", "Done")


image_process_button = tkinter.Button(text="EXECUTE", command=image_process_button_action)
image_process_button.config(height=5, width=75)
image_process_button.place(x=0, y=200)

# Reload button
def reload_button_action():
    print("To be implemented")
    pass
reload_button = tkinter.Button(text="RELOAD", command=reload_button_action)
reload_button.place(x=0, y=0)

resize_app.mainloop()
