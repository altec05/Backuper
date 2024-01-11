try:
    import tkinter
    from tkinter import ttk
except ImportError:
    import Tkinter
    import ttk

import customtkinter as CTk
import variables as vs
from datetime import datetime
from changes import ChangesWindow


class AboutWindow(CTk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("600x350+500+300")
        self.title('О программе')
        self.resizable(width=False, height=False)
        self.iconbitmap('logo.ico')
        CTk.deactivate_automatic_dpi_awareness()

        label_text_up = f'Сведения о программе "Backuper"\n\n© Разработка и права: Домашенко Иван Константинович / ' \
                        f'Отдел ИТ\n\n\nПрограмма была разработана с целью упрощения создания ' \
                        f'резервных копий\nбаз данных и иных необходимых файлов или директорий\n' \
                        f'Программа написана с применением языка программирования Python v3.11'
        label_text_center = f'Версия программы - ver. {vs.app_version} от {vs.app_last_edit_version}'
        label_text_down = f'КГКУЗ "Красноярский краевой центр крови №1"\n\n2024 - {datetime.now().year}'

        self.label_up = CTk.CTkLabel(self, text=label_text_up, wraplength=550)
        self.label_up.pack(padx=20, pady=15)

        self.label_center = CTk.CTkLabel(self, text=label_text_center, wraplength=550, anchor='center')
        self.label_center.pack(padx=20, pady=20)

        self.show_changes_button = CTk.CTkButton(master=self, text='Изменения', width=125,
                                                 command=self.show_changes)
        self.show_changes_button.pack(pady=5, padx=5)

        self.label_down = CTk.CTkLabel(self, text=label_text_down)
        self.label_down.pack(padx=20, pady=25)

        # Фокусировка и перенаправление нажатий на окно
        self.focus()
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", lambda: self.dismiss())  # перехватываем нажатие на крестик

    # Выход из окна настройки
    def dismiss(self):
        vs.toplevel_window = None
        vs.temp_name = ''
        vs.previous_window.deiconify()
        vs.previous_window = None
        self.grab_release()
        self.destroy()

    def show_changes(self):
        if vs.previous_toplevel_window is None:
            vs.toplevel_window = ChangesWindow(self)
            vs.previous_toplevel_window = self
            self.withdraw()
