try:
    import tkinter
    from tkinter.messagebox import showerror, showwarning, showinfo, askyesno
except ImportError:
    import Tkinter as tkinter
    import ttk

from tkinter.messagebox import showerror, showwarning, showinfo, askyesno


def open_info(title, text):
    showinfo(title=title, message=text)


def open_warning(title, text):
    showwarning(title=title, message=text)


def open_error(title, text):
    showerror(title=title, message=text)
