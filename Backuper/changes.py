import os

import changes_list

try:
    import tkinter
    from tkinter import ttk
except ImportError:
    import Tkinter
    import ttk

import customtkinter as CTk
from PIL import Image
from tkcalendar import Calendar

import service_funcs
import variables as vs
import tkinter.filedialog as fd
import messages as mes


class ChangesWindow(CTk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("950x400")

        self.title('Список изменений')
        self.resizable(width=False, height=False)
        self.iconbitmap('logo.ico')
        CTk.deactivate_automatic_dpi_awareness()

        self.textbox = CTk.CTkTextbox(master=self, corner_radius=1, wrap=tkinter.WORD)
        self.textbox.pack(padx=20, pady=5, fill="both", expand=True)

        # Заполняем виджет маршрутами, если есть
        self.update_textbox()

        # Фокусировка и перенаправление нажатий на окно
        self.focus()
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", lambda: self.dismiss())  # перехватываем нажатие на крестик

    def dismiss(self):
        vs.toplevel_window = vs.previous_toplevel_window
        vs.previous_toplevel_window.deiconify()
        vs.previous_toplevel_window = None
        self.grab_release()
        self.destroy()

    def update_textbox(self):
        changes_str = changes_list.changes_row

        self.textbox.configure(state='normal')
        self.textbox.delete('0.0', tkinter.END)
        self.textbox.insert("0.0", changes_str)
        self.textbox.configure(state='disabled')
