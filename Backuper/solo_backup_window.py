try:
    import tkinter
    from tkinter import ttk
except ImportError:
    import Tkinter
    import ttk

import customtkinter as CTk
import service_funcs
import variables as vs
import messages as mes


class SoloBackupWindow(CTk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("850x385")

        self.title('Выбор маршрута для запуска выборочного копирования')
        self.resizable(width=False, height=False)
        self.iconbitmap('logo.ico')
        CTk.deactivate_automatic_dpi_awareness()

        self.textbox_frame = CTk.CTkFrame(master=self, fg_color='transparent')
        self.textbox_frame.pack(fill='both', ipadx=10, ipady=5, pady=5)

        self.name_frame = CTk.CTkFrame(master=self, fg_color='transparent')
        self.name_frame.pack(fill='x', ipadx=10, ipady=10, pady=10)

        self.label_status_frame = CTk.CTkFrame(master=self, fg_color='transparent')
        self.label_status_frame.pack(fill='x', ipadx=10, ipady=10, pady=10)

        self.textbox = CTk.CTkTextbox(master=self.textbox_frame, corner_radius=1)
        self.textbox.pack(padx=20, pady=5, fill="both", expand=True)

        # Заполняем виджет маршрутами, если есть
        self.update_textbox()

        self.e_path = CTk.CTkOptionMenu(master=self.name_frame,
                                                             values=self.get_names_list(), width=180)
        self.e_path.pack(side='left', pady=5, padx=25)

        # self.e_path = CTk.CTkEntry(self.name_frame, placeholder_text="Укажите имя маршрута для взаимодействия", width=600)
        # self.e_path.pack(padx=20, pady=5, side='left', fill='x')

        self.start = CTk.CTkButton(self.name_frame, command=self.start_backup_for_path, width=150, text='Начать копирование')
        self.start.pack(padx=20, pady=5, side='right', fill='none')

        self.solo_backup_label = CTk.CTkLabel(master=self.label_status_frame, text='Ожидание начала копирования...',
                                              wraplength=450,
                                              text_color='red', anchor='e')
        self.solo_backup_label.pack(side='left', pady=5, padx=20)

        # Фокусировка и перенаправление нажатий на окно
        self.focus()
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", lambda: self.dismiss())  # перехватываем нажатие на крестик
        self.bind('<Map>', self.update_textbox())  # перехватываем разворачивание для обновления

    def update_textbox(self):
        # Заполняем виджет маршрутами, если есть
        paths_dict = service_funcs.read_config()
        if paths_dict != False:
            paths_str = ''
            paths_str = self.get_paths(paths_dict)

            self.textbox.configure(state='normal')
            self.textbox.delete('0.0', tkinter.END)
            self.textbox.insert("0.0", paths_str)
            self.textbox.configure(state='disabled')

            vs.multi_paths = paths_dict

    def get_names_list(self):
        names = []
        paths_dict = service_funcs.read_config()
        if paths_dict != False:
            names = self.get_names(paths_dict)
        return names

    # Получение списка имен маршрутов
    def get_names(self, paths_dict):
        names_list = []
        for main_key in paths_dict:
            names_list.append(main_key)
        names_list.sort()
        return names_list

    # Перевод словаря в читабельный вид для виджета
    def get_paths(self, paths_dict):
        paths_str = ''
        paths_list = []
        for main_key in paths_dict:
            paths_list.append(main_key)
        paths_list.sort()
        for main_key in paths_list:
            if paths_dict[main_key]['on_date'] != 'False':
                if paths_dict[main_key]['today'] != 'False':
                    try:
                        paths_str += 'Имя:\t' +  main_key + '\nИз:\t' + str(paths_dict[main_key]['from_path']) + '\nВ:\t' + paths_dict[main_key]['to_path'] + '\nДата:\t' + service_funcs.str_to_true_date_format(paths_dict[main_key]['on_date']) + '\nТекущая:\t' + 'Да' + '\nМакс.Копий:\t' + str(paths_dict[main_key]['amount']) + '\n\n'
                    except:
                        paths_str += 'Имя:\t' +  main_key + '\nИз:\t' + str(paths_dict[main_key]['from_path']) + '\nВ:\t' + paths_dict[main_key]['to_path'] + '\nДата:\t' + paths_dict[main_key]['on_date'] + '\nТекущая:\t' + 'Да' + '\nМакс.Копий:\t' + str(paths_dict[main_key]['amount']) + '\n\n'
                else:
                    try:
                        paths_str += 'Имя:\t' + main_key + '\nИз:\t' + str(paths_dict[main_key]['from_path']) + '\nВ:\t' + paths_dict[main_key]['to_path'] + '\nДата:\t' + service_funcs.str_to_true_date_format(paths_dict[main_key]['on_date']) + '\nТекущая:\t' + 'Нет' + '\nМакс.Копий:\t' + str(paths_dict[main_key]['amount']) + '\n\n'
                    except:
                        paths_str += 'Имя:\t' + main_key + '\nИз:\t' + str(paths_dict[main_key]['from_path']) + '\nВ:\t' + paths_dict[main_key]['to_path'] + '\nДата:\t' + paths_dict[main_key]['on_date'] + '\nТекущая:\t' + 'Нет' + '\nМакс.Копий:\t' + str(paths_dict[main_key]['amount']) + '\n\n'
            else:
                paths_str += 'Имя:\t' +  main_key + '\nИз:\t' + str(paths_dict[main_key]['from_path']) + '\nВ:\t' + paths_dict[main_key]['to_path'] + '\nДата:\t' + 'Нет' + '\nТекущая:\t' + 'Нет' + '\nМакс.Копий:\t' + str(paths_dict[main_key]['amount']) + '\n\n'
        return paths_str

    # Выход из окна настройки
    def dismiss(self):
        vs.toplevel_window = None
        vs.temp_name = ''
        vs.previous_window.deiconify()
        vs.previous_window = None
        self.grab_release()
        self.destroy()

    # Удаление маршрута
    def start_backup_for_path(self):
        # Получаем имя маршрута из поля
        path = self.e_path.get()
        if path != '':
            if not path in vs.copied_routes:
                paths_dicts = service_funcs.read_config()
                paths_list = []
                if paths_dicts != False:
                    for main_key in paths_dicts:
                        paths_list.append(main_key)
                    paths_list.sort()
                    if path in paths_list:
                        self.solo_backup_label.configure(text_color='yellow')
                        self.solo_backup_label.configure(text=f'Подготовка копирования для "{path}"...')
                        main_key = path
                        name = main_key
                        from_path = paths_dicts[main_key]['from_path']
                        to_path = paths_dicts[main_key]['to_path']
                        on_date = paths_dicts[main_key]['on_date']
                        today = paths_dicts[main_key]['today']
                        amount = paths_dicts[main_key]['amount']
                        if today == 'True':
                            on_date = vs.date_today

                        service_funcs.backup_bd(from_path, to_path, name, on_date, amount, self)
                        self.solo_backup_label.configure(text='Копирование завершено!')
                        self.solo_backup_label.configure(text_color='green')

                        # Выводим отчет о копировании
                        if vs.rez_list:
                            out_str = ''
                            if len(vs.rez_list) <= 13:
                                for rez in vs.rez_list:
                                    out_str += rez
                            else:
                                out_str = f'Объектов обработано: {len(vs.rez_list)}'
                            mes.showinfo('Результаты резервного копирования', out_str)

                        vs.rez_list.clear()

                        self.solo_backup_label.configure(text='Ожидание начала копирования...')
                        self.solo_backup_label.configure(text_color='red')
                    else:
                        mes.showerror('Выбор маршрута', f'Маршрут {path} не найден!')
                else:
                    mes.showerror('Выбор маршрута', f'Список маршрутов пуст!')
            else:
                mes.showerror('Выбор маршрута', f'В этой сессии для маршрута уже проводилось копирование, а повторное'
                                                f' запрещено!\n\nДля повтора перезапустите программу.')
        else:
            mes.showerror('Выбор маршрута', f'Укажите корректное имя маршрута!')
