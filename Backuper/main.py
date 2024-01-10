import customtkinter as CTk
import threading
import psutil

import about
import instruction

try:
    import tkinter
    from tkinter import ttk
except ImportError:
    import Tkinter
    import ttk
from functools import partial

import service_funcs
import variables as vs
from add_window import AddFolderWindow
from multi_folders_window import MultiFoldersWindow
from solo_backup_window import SoloBackupWindow
import messages as mes


def change_appearance_mode_event(new_appearance_mode):
    CTk.set_appearance_mode(new_appearance_mode)


class App(CTk.CTk):
    def __init__ (self):
        super().__init__()

        self.geometry("825x280")
        self.title("Backuper")
        self.resizable (False, False)
        self.iconbitmap('logo.ico')
        CTk.set_default_color_theme("dark-blue")
        CTk.set_appearance_mode("system")
        CTk.deactivate_automatic_dpi_awareness()

        # Фреймы

        # Одиночное резервное копирование
        self.solo_backup_frame = CTk.CTkFrame(master=self, fg_color='transparent')
        self.solo_backup_frame.pack(fill='x', ipadx=10, pady=5)

        self.multi_frame = CTk.CTkFrame(master=self, fg_color='transparent')
        self.multi_frame.pack(fill='x', ipadx=10, pady=25)

        # Лейбл множественного копирования
        self.multi_backup_label_frame = CTk.CTkFrame(master=self.multi_frame, fg_color='transparent')
        self.multi_backup_label_frame.pack(fill='x', ipadx=10, pady=10)

        # Настройка множественного резервного копирования
        self.multi_backup_frame = CTk.CTkFrame(master=self.multi_frame, fg_color='transparent')
        self.multi_backup_frame.pack(fill='x', ipadx=10)

        # # Статус копирования
        # self.status_frame = CTk.CTkFrame(master=self, fg_color='transparent', height=100)
        # self.status_frame.pack(fill='x', ipadx=10, pady=5)

        # Опции приложения
        self.options_frame = CTk.CTkFrame(master=self, fg_color='transparent', height=100)
        self.options_frame.pack(fill='x', ipadx=10, ipady=5, pady=15)

        # Кнопки
        # Одиночное резервное копирование
        self.solo_backup_button = CTk.CTkButton(master=self.solo_backup_frame, text='Выборочное копирование', width=180, command=self.show_solo_backup_window)
        self.solo_backup_button.pack(side='left', pady=5, padx=25)

        self.solo_backup_label = CTk.CTkLabel(master=self.solo_backup_frame, text='Ожидание начала копирования...', wraplength=450,
                                               text_color='red', anchor='w')
        self.solo_backup_label.pack(side='left', pady=5)

        # Заголовок множественного резервного копирования
        self.multi_backup_options_label = CTk.CTkLabel(master=self.multi_backup_label_frame, text='Множественное копирование по заданным маршрутам', text_color=('green', 'white'), anchor='w')
        self.multi_backup_options_label.pack(side='left', padx=25)

        # Добавить папку для массового копирования
        self.add_multi_backup_folder_button = CTk.CTkButton(master=self.multi_backup_frame,
                                                            text='Добавить маршрут', width=150,
                                                            command=self.show_add_window)
        self.add_multi_backup_folder_button.pack(side='left', padx=25)

        # Отображение записанных папок для копирования
        self.show_multi_backup_folders_button = CTk.CTkButton(master=self.multi_backup_frame, text='Настроить', width=150, command=self.show_multi_folders_window)
        self.show_multi_backup_folders_button.pack(side='left', padx=5)

        # Множественное резервное копирование
        self.start_multi_backup_button = CTk.CTkButton(master=self.multi_backup_frame, text='Начать', fg_color=(('green', 'darkgreen')), width=150, command=self.start_thread)
        self.start_multi_backup_button.pack(side='right', padx=25)

        def checkbox_event():
            vs.clear_folder_before_flag = self.chb_folder_clear.get()

        self.chb_folder_clear = CTk.CTkCheckBox(master=self.multi_backup_frame,
                                                  text="Очищать конечную папку",
                                                  command=checkbox_event, onvalue=True, offvalue=False,
                                                  corner_radius=6, border_width=1)
        self.chb_folder_clear.pack(side='right', ipadx=5, ipady=5, pady=5, padx=5, anchor='w')

        vs.clear_folder_before_flag = True
        self.chb_folder_clear.select()

        # self.status_label = CTk.CTkLabel(master=self.status_frame, text='Ожидание...',
        #                                       wraplength=450,
        #                                       text_color='red', anchor='w')
        # self.status_label.pack(side='left', padx=20)

        # Опции приложения
        # Смена темы
        self.appearance_mode_option_menu = CTk.CTkOptionMenu(master=self.options_frame,
                                                             values=["System", "Light", "Dark"],
                                                             command=change_appearance_mode_event, width=180)
        self.appearance_mode_option_menu.pack(side='left', pady=5, padx=20)

        # О программе
        self.show_about_button = CTk.CTkButton(master=self.options_frame, text='О программе', width=125,
                                               command=self.show_about)
        self.show_about_button.pack(side='right', pady=5, padx=25)

        # Инструкция
        self.show_instruction_button = CTk.CTkButton(master=self.options_frame, text='Инструкция', width=125,
                                                     command=self.show_instruction)
        self.show_instruction_button.pack(side='right', pady=5, padx=25)

        self.toplevel_window = None

    def show_solo_backup_window(self):
        # Заполняем виджет маршрутами, если есть
        paths_dict = service_funcs.read_config()
        if paths_dict != False:
            vs.multi_paths = paths_dict

        # Если в словаре маршруты есть
        if len(vs.multi_paths) > 0:
            if vs.toplevel_window is None:
                vs.toplevel_window = SoloBackupWindow(self)
                vs.previous_window = self
                self.withdraw()
        else:
            mes.showwarning('Модерация маршрутов', f'Список маршрутов пуст')

    def show_multi_folders_window(self):
        # Заполняем виджет маршрутами, если есть
        paths_dict = service_funcs.read_config()
        if paths_dict != False:
            vs.multi_paths = paths_dict

        # Если в словаре маршруты есть
        if len(vs.multi_paths) > 0:
            if vs.toplevel_window is None:
                vs.toplevel_window = MultiFoldersWindow(self)
                vs.previous_window = self
                self.withdraw()
        else:
            mes.showwarning('Модерация маршрутов', f'Список маршрутов пуст')

    def show_add_window(self):
        if vs.toplevel_window is None:
            vs.toplevel_window = AddFolderWindow(self)
            vs.previous_window = self
            self.withdraw()

        # if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
        #     self.toplevel_window = AddFolderWindow(self)  # create window if its None or destroyed
        # else:
        #     self.toplevel_window.focus()  # if window exists focus it

    def start_multi_backuping(self):
        paths_dicts = service_funcs.read_config()
        paths_list = []
        if paths_dicts != False:
            for main_key in paths_dicts:
                paths_list.append(main_key)
            paths_list.sort()
            for main_key in paths_list:
                name = main_key
                from_path = paths_dicts[main_key]['from_path']
                to_path = paths_dicts[main_key]['to_path']
                on_date = paths_dicts[main_key]['on_date']
                today = paths_dicts[main_key]['today']
                amount = paths_dicts[main_key]['amount']
                if today == 'True':
                    on_date = vs.date_today
                if not name in vs.copied_routes:
                    service_funcs.backup_bd(from_path, to_path, name, on_date, amount, self)
                else:
                    vs.rez_list.append(
                        f'{len(vs.rez_list) + 1}. В этой сессии для маршрута "{name}" уже проводилось копирование, а повторное'
                                                f' запрещено!\n\nДля повтора перезапустите программу.\n\n')
            self.solo_backup_label.configure(text='Копирование завершено!')
            self.solo_backup_label.configure(text_color='green')
            # Выводим отчет о копировании
            if vs.rez_list:
                out_str = ''
                for rez in vs.rez_list:
                    out_str += rez
                mes.showinfo('Результаты резервного копирования', out_str)
            vs.rez_list.clear()
            # mes.showwarning('Резервное копирование', 'Процесс копирования завершен!\n\nПриложение будет закрыто для сброса системного кэша.')
            # self.on_close()

    def show_about(self):
        if vs.toplevel_window is None:
            vs.toplevel_window = about.AboutWindow(self)
            vs.previous_window = self
            self.withdraw()

    def show_instruction(self):
        if vs.toplevel_window is None:
            vs.toplevel_window = instruction.InstructionWindow(self)
            vs.previous_window = self
            self.withdraw()

    def on_close(root):
        root.destroy()

    def check_thread(self, thread):
        if thread.is_alive():
            # if CTk.get_appearance_mode() == 'Dark':
            #     self.status_label.configure(text='Ожидайте выполнения программы...', text_color='yellow')
            # else:
            #     self.status_label.configure(text='Ожидайте выполнения программы...', text_color='black')
            self.after(100, lambda: self.check_thread(thread))
        else:
            self.solo_backup_button.configure(state='normal')
            self.add_multi_backup_folder_button.configure(state='normal')
            self.show_multi_backup_folders_button.configure(state='normal')
            self.start_multi_backup_button.configure(state='normal')
            self.chb_folder_clear.configure(state='normal')
            self.appearance_mode_option_menu.configure(state='normal')
            self.show_about_button.configure(state='normal')
            self.show_instruction_button.configure(state='normal')
            # self.status_label.configure(text='Процесс копирования завершен!')

            mes.showwarning('Резервное копирование',
                            'Процесс копирования завершен!\n\nПриложение будет закрыто для сброса системного кэша.')
            self.on_close()

    def start_thread(self):
        self.solo_backup_button.configure(state='disabled')
        self.add_multi_backup_folder_button.configure(state='disabled')
        self.show_multi_backup_folders_button.configure(state='disabled')
        self.start_multi_backup_button.configure(state='disabled')
        self.chb_folder_clear.configure(state='disabled')
        self.appearance_mode_option_menu.configure(state='disabled')
        self.show_about_button.configure(state='disabled')
        self.show_instruction_button.configure(state='disabled')
        # self.status_label.configure(text='Старт резервного копирования...')

        mes.showwarning('Предупреждение о нагрузках', 'Внимание!\n\nПри копировании большого количества файлов интерфейс программы может не отвечать, дождитесь уведомления об окончании!')

        thread = threading.Thread(target=self.start_multi_backuping, daemon=True)
        thread.start()
        self.check_thread(thread)


if __name__ == "__main__":
    app = App()
    app.protocol("WM_DELETE_WINDOW", partial(app.on_close))
    app.mainloop()
