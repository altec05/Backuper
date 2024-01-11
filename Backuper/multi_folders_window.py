import os
try:
    import tkinter
    from tkinter import ttk
except ImportError:
    import Tkinter
    import ttk
from PIL import Image

import customtkinter as CTk

import edit_path_window
import service_funcs
import variables as vs
import messages as mes


class MultiFoldersWindow(CTk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("800x350")

        self.title('Модерация маршрутов')
        self.resizable(width=False, height=False)
        self.iconbitmap('logo.ico')
        CTk.deactivate_automatic_dpi_awareness()

        self.clear_frame = CTk.CTkFrame(master=self, fg_color='transparent')
        self.clear_frame.pack(fill='x', ipadx=10, ipady=5, pady=5)

        self.textbox_frame = CTk.CTkFrame(master=self, fg_color='transparent')
        self.textbox_frame.pack(fill='both', ipadx=10, ipady=5, pady=5)

        self.name_frame = CTk.CTkFrame(master=self, fg_color='transparent')
        self.name_frame.pack(fill='x', ipadx=10, ipady=10, pady=10)

        self.textbox = CTk.CTkTextbox(master=self.textbox_frame, corner_radius=1)
        self.textbox.pack(padx=20, pady=5, fill="both", expand=True)

        # Заполняем виджет маршрутами, если есть
        self.update_textbox()

        self.b_clear_dict = CTk.CTkButton(self.clear_frame, text='Очистить список', command=self.clear_dict_paths)
        self.b_clear_dict.pack(padx=20, pady=5, side='right')

        self.e_path = CTk.CTkEntry(self.name_frame, placeholder_text="Укажите имя маршрута для взаимодействия", width=600)
        self.e_path.pack(padx=20, pady=5, side='left', fill='x')

        img_edit = CTk.CTkImage(light_image=Image.open("images/edit.gif"),
                                dark_image=Image.open("images/edit.gif"),
                                size=(20, 20))
        self.b_path_edit = CTk.CTkButton(self.name_frame, text='', command=self.show_edit_path_window, width=50,
                                         image=img_edit)
        self.b_path_edit.pack(padx=20, pady=5, side='left', fill='none')

        img_del = CTk.CTkImage(light_image=Image.open("images/del.gif"),
                                          dark_image=Image.open("images/del.gif"),
                                          size=(20, 20))
        self.b_path_del = CTk.CTkButton(self.name_frame, text='', command=self.del_path, width=50, image=img_del)
        self.b_path_del.pack(padx=10, pady=5, side='left', fill='none')

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

    # Перевод словаря в читабельный вид для виджета
    def get_paths(self, paths_dict):
        paths_str = ''
        # Получаем ключи
        paths_list = []
        for main_key in paths_dict:
            paths_list.append(main_key)
        paths_list.sort()
        for main_key in paths_list:
            if paths_dict[main_key]['on_date'] != 'False':
                if paths_dict[main_key]['today'] != 'False':
                    try:
                        paths_str += 'Имя:\t' +  main_key + '\nИз:\t' + str(paths_dict[main_key]['from_path']) + '\nВ:\t' + paths_dict[main_key]['to_path'] + '\nДата:\t' + service_funcs.str_to_true_date_format(paths_dict[main_key]['on_date']) + '\nТекущая:\t' + 'Да' + '\nМакс.Копий:\t' + str(paths_dict[main_key]['amount']) + '\nТолько ручной:\t' + paths_dict[main_key]['no_multiple'] + '\n\n'
                    except:
                        paths_str += 'Имя:\t' +  main_key + '\nИз:\t' + str(paths_dict[main_key]['from_path']) + '\nВ:\t' + paths_dict[main_key]['to_path'] + '\nДата:\t' + paths_dict[main_key]['on_date'] + '\nТекущая:\t' + 'Да' + '\nМакс.Копий:\t' + str(paths_dict[main_key]['amount']) + '\nТолько ручной:\t' + paths_dict[main_key]['no_multiple'] + '\n\n'
                else:
                    try:
                        paths_str += 'Имя:\t' + main_key + '\nИз:\t' + str(paths_dict[main_key]['from_path']) + '\nВ:\t' + paths_dict[main_key]['to_path'] + '\nДата:\t' + service_funcs.str_to_true_date_format(paths_dict[main_key]['on_date']) + '\nТекущая:\t' + 'Нет' + '\nМакс.Копий:\t' + str(paths_dict[main_key]['amount']) + '\nТолько ручной:\t' + paths_dict[main_key]['no_multiple'] + '\n\n'
                    except:
                        paths_str += 'Имя:\t' + main_key + '\nИз:\t' + str(paths_dict[main_key]['from_path']) + '\nВ:\t' + paths_dict[main_key]['to_path'] + '\nДата:\t' + paths_dict[main_key]['on_date'] + '\nТекущая:\t' + 'Нет' + '\nМакс.Копий:\t' + str(paths_dict[main_key]['amount']) + '\nТолько ручной:\t' + paths_dict[main_key]['no_multiple'] + '\n\n'
            else:
                paths_str += 'Имя:\t' +  main_key + '\nИз:\t' + str(paths_dict[main_key]['from_path']) + '\nВ:\t' + paths_dict[main_key]['to_path'] + '\nДата:\t' + 'Нет' + '\nТекущая:\t' + 'Нет' + '\nМакс.Копий:\t' + str(paths_dict[main_key]['amount']) + '\nТолько ручной:\t' + paths_dict[main_key]['no_multiple'] + '\n\n'
        return paths_str

    # Выход из окна настройки
    def dismiss(self):
        vs.toplevel_window = None
        vs.temp_name = ''
        vs.previous_window.deiconify()
        vs.previous_window = None
        self.grab_release()
        self.destroy()

    # Очистка словаря и формы
    def clear_dict_paths(self):
        if mes.askyesno('Очистка маршрутов', 'Вы действительно хотите очистить список маршрутов?'):
            # Очищаем словарь
            vs.multi_paths.clear()
            vs.copied_routes.clear()

            # Удаляем конфиг-файл
            try:
                os.remove(vs.path_config)
            except FileNotFoundError:
                pass

            # Очищаем виджет
            self.textbox.configure(state='normal')
            self.textbox.delete('1.0', tkinter.END)
            self.textbox.configure(state='disabled')

            mes.showinfo('Очистка маршрутов', 'Маршруты успешно очищены!')

            # Выходим из окна настройки
            self.dismiss()

    # Удаление маршрута
    def del_path(self):
        # Получаем имя маршрута из поля
        path = self.e_path.get().strip(' ')
        if path != '':
            # Если в словаре маршруты есть
            if len(vs.multi_paths) > 0:
                if mes.askyesno('Удаление маршрута', f'Вы действительно хотите удалить маршрут "{path}"?'):
                    # Удаляем маршрут по ключу
                    try:
                        del vs.multi_paths[path]
                        if path in vs.copied_routes:
                            vs.copied_routes.remove(path)
                        # Обновляем конфиг-файл
                        code = service_funcs.update_config(vs.multi_paths)
                        # Если обновлен без ошибок
                        if code:
                            self.textbox.configure(state='normal')
                            # Считываем из конфига маршруты
                            paths_dict = service_funcs.read_config()
                            # Если маршруты есть перезаписываем виджет
                            if paths_dict != False:
                                paths_str = ''
                                paths_str = self.get_paths(paths_dict)
                                self.textbox.delete("0.0", tkinter.END)
                                self.textbox.insert("0.0", paths_str)
                                self.textbox.configure(state='disabled')
                                mes.showinfo('Удаление маршрута', f'Маршрут "{path}" удален!')
                            # Если маршрутов больше нет, то очищаем виджет
                            else:
                                self.textbox.delete("0.0", tkinter.END)
                                self.textbox.configure(state='disabled')
                                mes.showinfo('Удаление маршрута', f'Маршрут "{path}" удален!')
                    except KeyError:
                        mes.showwarning('Удаление маршрута', f'Маршрут "{path}" не найден!')
            else:
                mes.showerror('Удаление маршрута', f'Список маршрутов пуст!')
        else:
            mes.showerror('Удаление маршрута', f'Укажите корректное имя маршрута!')

    def show_edit_path_window(self):
        name = self.e_path.get().strip(' ')
        if name:
            try:
                rez = vs.multi_paths.get(name)
                if rez:
                    vs.temp_from_pathes = rez['from_path']
                    vs.temp_to_path = rez['to_path']
                    vs.temp_date = rez['on_date']
                    if rez['today'] == 'False':
                        vs.today_flag = False
                    else:
                        vs.today_flag = True

                    vs.temp_amount = rez['amount']
                    vs.temp_no_multiple_flag = rez['no_multiple']

                    if vs.previous_toplevel_window is None:
                        vs.temp_name = name
                        # цикл по путям для получения имен файлов и вывода или путями
                        vs.toplevel_window = edit_path_window.EditPathWindow(self)
                        vs.previous_toplevel_window = self
                        self.withdraw()
            except:
                mes.showerror('Редактирование маршрута', 'Маршрут не найден!')
        else:
            mes.showerror('Редактирование маршрута', 'Укажите корректное имя маршрута!')
