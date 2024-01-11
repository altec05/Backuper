import os

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


class EditPathWindow(CTk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("950x400")

        self.title('Изменение маршрута')
        self.resizable(width=False, height=False)
        self.iconbitmap('logo.ico')
        CTk.deactivate_automatic_dpi_awareness()

        # Лейбл
        self.label_frame = CTk.CTkFrame(master=self, fg_color='transparent')
        self.label_frame.pack(fill='x', ipadx=10, ipady=10, pady=10, padx=20)

        # Имя
        self.name_frame = CTk.CTkFrame(master=self, fg_color='transparent')
        self.name_frame.pack(fill='x', ipadx=10, ipady=10, pady=5, padx=20)

        # Дата
        self.date_frame = CTk.CTkFrame(master=self, fg_color='transparent')
        self.date_frame.pack(fill='x', ipadx=10, ipady=10, pady=5, padx=20)

        # Откуда
        self.from_frame = CTk.CTkFrame(master=self, fg_color='transparent')
        self.from_frame.pack(fill='x', ipadx=10, ipady=10, pady=5, padx=20)

        # Куда
        self.to_frame = CTk.CTkFrame(master=self, fg_color='transparent')
        self.to_frame.pack(fill='x', ipadx=10, ipady=10, pady=5, padx=20)

        # Максимальное количество копий в папке
        self.amount_frame = CTk.CTkFrame(master=self, fg_color='transparent')
        self.amount_frame.pack(fill='x', ipadx=10, ipady=10, pady=5, padx=20)

        # Сохранить изменения
        self.confirm_frame = CTk.CTkFrame(master=self, fg_color='transparent')
        self.confirm_frame.pack(fill='x', ipadx=10, ipady=10, padx=20)

        self.label = CTk.CTkLabel(self.label_frame, text=f"Укажите новые параметры для выбранного маршрута '{vs.temp_name}'")
        self.label.pack(fill='x')

        self.e_name = CTk.CTkEntry(self.name_frame, placeholder_text="Наименование пути", width=350)
        self.e_name.pack(fill='x')
        self.e_name.insert(0, vs.temp_name)
        self.e_name.configure(state='disabled')

        def checkbox_date_event():
            if vs.temp_from_pathes and not vs.temp_from_pathes_old:
                vs.temp_from_pathes_old = vs.temp_from_pathes
                vs.temp_from_pathes = []
                self.e_path_from.configure(state='normal')
                self.e_path_from.delete(0, tkinter.END)
                self.e_path_from.insert(0, str(vs.temp_from_pathes_old))
                self.e_path_from.configure(state='disabled')
            elif vs.temp_from_pathes_old and not vs.temp_from_pathes:
                vs.temp_from_pathes = vs.temp_from_pathes_old
                vs.temp_from_pathes_old = []

                self.e_path_from.configure(state='normal')
                self.e_path_from.delete(0, tkinter.END)
                self.e_path_from.insert(0, str(vs.temp_from_pathes))
                self.e_path_from.configure(state='disabled')

            vs.date_flag = self.date_checkbox.get()
            if vs.date_flag:
                self.file_from_checkbox.deselect()
                self.file_from_checkbox.configure(state='disabled')
                self.b_date.configure(state='normal')
                vs.file_flag = self.file_from_checkbox.get()
                self.today_checkbox.configure(state='normal')

                if vs.temp_date != '' and vs.temp_date != 'False':
                    self.e_data.configure(state='normal')
                    self.e_data.delete(0, tkinter.END)
                    try:
                        self.e_data.insert(0, service_funcs.str_to_true_date_format(vs.temp_date))
                    except:
                        try:
                            self.e_data.insert(0, service_funcs.true_date_format(vs.temp_date))
                        except:
                            self.e_data.insert(0, vs.temp_date)
                    self.e_data.configure(state='disabled')
                else:
                    self.e_data.configure(state='normal')
                    self.e_data.delete(0, tkinter.END)
                    # self.e_data.insert(0, vs.temp_date)
                    self.e_data.configure(state='disabled')
            else:
                self.file_from_checkbox.configure(state='normal')
                self.today_checkbox.deselect()
                self.today_checkbox.configure(state='disabled')
                self.b_date.configure(state='disabled')
                self.e_data.configure(state='normal')
                self.e_data.delete(0, tkinter.END)
                self.e_data.configure(state='disabled')
                vs.today_flag = False
                vs.date_flag = False

        self.date_checkbox = CTk.CTkCheckBox(master=self.date_frame,
                                             text="Файлы из каталога по дате",
                                             command=checkbox_date_event, onvalue=True, offvalue=False,
                                             corner_radius=6, border_width=1)
        self.date_checkbox.pack(side='left', ipadx=5, ipady=5, pady=5, anchor='w')

        def checkbox_today_event():
            vs.today_flag = self.today_checkbox.get()
            if vs.today_flag:
                vs.temp_date_old = vs.temp_date
                vs.temp_date = str(vs.date_today)
                self.b_date.configure(state='disabled')

                self.e_data.configure(state='normal')
                self.e_data.delete(0, tkinter.END)
                if vs.temp_date != '':
                    try:
                        self.e_data.insert(0, service_funcs.str_to_true_date_format(vs.temp_date))
                    except:
                        try:
                            self.e_data.insert(0, service_funcs.true_date_format(vs.temp_date))
                        except:
                            self.e_data.insert(0, vs.temp_date)
                self.e_data.configure(state='disabled')
            else:
                vs.today_flag = self.today_checkbox.get()
                if vs.temp_date_old != 'False':
                    vs.temp_date = vs.temp_date_old
                else:
                    vs.temp_date = ''
                vs.temp_date_old = ''
                self.b_date.configure(state='normal')
                self.e_data.configure(state='normal')
                self.e_data.delete(0, tkinter.END)
                if vs.temp_date != '':
                    try:
                        self.e_data.insert(0, service_funcs.str_to_true_date_format(vs.temp_date))
                    except:
                        try:
                            self.e_data.insert(0, service_funcs.true_date_format(vs.temp_date))
                        except:
                            self.e_data.insert(0, vs.temp_date)
                self.e_data.configure(state='disabled')

        self.today_checkbox = CTk.CTkCheckBox(master=self.date_frame,
                                              text="Всегда текущая дата",
                                              command=checkbox_today_event, onvalue=True, offvalue=False,
                                              corner_radius=6, border_width=1)
        self.today_checkbox.pack(side='left', ipadx=5, ipady=5, pady=5, padx=25, anchor='w')

        self.b_date = CTk.CTkButton(self.date_frame, text='Указать дату', command=self.get_date, state='disabled')
        self.b_date.pack(padx=10, pady=5, side='left')

        self.e_data = CTk.CTkEntry(self.date_frame, placeholder_text="Дата", width=100, state='disabled')
        self.e_data.pack(padx=25, pady=5, side='left')

        vs.file_flag_edit = False

        self.b_path_from = CTk.CTkButton(self.from_frame, text='Указать откуда', command=self.add_from_folder)
        self.b_path_from.pack(pady=5, side='left')

        self.e_path_from = CTk.CTkEntry(self.from_frame, placeholder_text="Скопировать из", width=650)
        self.e_path_from.pack(padx=10, side='left')
        # self.e_path_from.insert(0, vs.temp_from_path)
        self.e_path_from.insert(0, str(vs.temp_from_pathes))
        self.e_path_from.configure(state='disabled')

        def checkbox_event():
            vs.file_flag_edit = self.file_from_checkbox.get()
            self.clear_e_from()
            vs.temp_date = ''
            vs.temp_date_old = ''

        self.file_from_checkbox = CTk.CTkCheckBox(master=self.from_frame,
                                                  text="Файлы",
                                                  command=checkbox_event, onvalue=True, offvalue=False,
                                                  corner_radius=6, border_width=1)
        self.file_from_checkbox.pack(side='left', ipadx=5, ipady=5, pady=5, anchor='w')

        img_del = CTk.CTkImage(light_image=Image.open("images/del.gif"),
                               dark_image=Image.open("images/del.gif"),
                               size=(20, 20))

        self.b_e_path_from_del = CTk.CTkButton(self.from_frame, text='', command=self.clear_e_from, width=50,
                                               image=img_del)
        self.b_e_path_from_del.pack(padx=10, pady=5, side='left')

        self.b_path_to = CTk.CTkButton(self.to_frame, text='Указать куда', command=self.add_to_folder)
        self.b_path_to.pack(pady=5, side='left')

        self.e_path_to = CTk.CTkEntry(self.to_frame, placeholder_text="Скопировать в", width=800)
        self.e_path_to.pack(padx=10, pady=5, side='right')
        self.e_path_to.insert(0, vs.temp_to_path)
        self.e_path_to.configure(state='disabled')

        self.l_amount = CTk.CTkLabel(self.amount_frame, text="Максимум копий:")
        self.l_amount.pack(fill='x', side='left')

        self.e_amount = CTk.CTkEntry(self.amount_frame, state='normal', width=50)
        self.e_amount.pack(padx=20, side='left')
        self.e_amount.insert(0, vs.temp_amount)

        def no_multiple_checkbox_event():
            vs.temp_no_multiple_flag = self.no_multiple_checkbox.get()

        self.no_multiple_checkbox = CTk.CTkCheckBox(master=self.amount_frame,
                                                  text="Не участвовать в множественном копировании",
                                                  command=no_multiple_checkbox_event, onvalue=True, offvalue=False,
                                                  corner_radius=6, border_width=1)
        self.no_multiple_checkbox.pack(side='left', ipadx=5, ipady=5, pady=5, anchor='w')

        if vs.temp_no_multiple_flag == 'True':
            self.no_multiple_checkbox.select()

        self.b_confirm = CTk.CTkButton(self.amount_frame, text='Сохранить', command=self.confirm)
        self.b_confirm.pack(padx=10, side='right')

        self.focus()
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", lambda: self.dismiss())  # перехватываем нажатие на крестик

        if vs.temp_date != '' and vs.temp_date != 'False':
            self.e_data.configure(state='normal')
            self.e_data.insert(0, service_funcs.str_to_true_date_format(vs.temp_date))
            self.e_data.configure(state='disabled')
            vs.date_flag = True
            self.date_checkbox.select()
            self.file_from_checkbox.configure(state='disabled')
            self.b_date.configure(state='normal')
            if vs.today_flag:
                vs.temp_date_old = vs.temp_date
                vs.temp_date = str(vs.date_today)

                self.e_data.configure(state='normal')
                self.e_data.delete(0, tkinter.END)
                try:
                    self.e_data.insert(0, service_funcs.str_to_true_date_format(vs.temp_date))
                except:
                    try:
                        self.e_data.insert(0, service_funcs.true_date_format(vs.temp_date))
                    except:
                        self.e_data.insert(0, vs.temp_date)
                self.e_data.configure(state='disabled')
                self.today_checkbox.select()
                self.b_date.configure(state='disabled')
        else:
            self.today_checkbox.deselect()
            self.today_checkbox.configure(state='disabled')


    def clear_edit_temps(self):
        vs.file_flag_edit = False
        vs.temp_name = ''
        vs.temp_from_path = ''
        vs.temp_to_path = ''
        vs.file_flag = False
        vs.today_flag = False
        vs.date_flag = False
        vs.temp_date_old = ''
        vs.temp_from_pathes_old = []
        vs.temp_from_names_old = []
        vs.temp_amount = 3
        vs.temp_no_multiple_flag = False

    def get_date(self):
        def print_sel():
            vs.temp_date = str(cal.selection_get())
            self.e_data.configure(state='normal')
            self.e_data.delete(0, tkinter.END)
            self.e_data.insert(0, service_funcs.str_to_true_date_format(vs.temp_date))
            self.e_data.configure(state='disabled')
            top.grab_release()
            top.destroy()

        top = tkinter.Toplevel(self)
        top.focus()
        top.grab_set()

        now_day, now_month, now_year = vs.date_today_true.split('.')

        cal = Calendar(top,
                       font="Calibri 12", selectmode='day', year=int(now_year), month=int(now_month), day=int(now_day))
        cal.pack(fill="both", expand=True)
        ttk.Button(top, text="OK", command=print_sel).pack()

    def clear_e_from(self):
        self.e_path_from.configure(state='normal')
        self.e_path_from.delete(0, tkinter.END)
        self.e_path_from.configure(state='disabled')
        vs.temp_from_names.clear()
        vs.temp_from_pathes.clear()
        vs.temp_new_path.clear()
        vs.temp_from_pathes_old.clear()
        vs.temp_from_names_old.clear()

    def dismiss(self):
        # Заполняем виджет маршрутами, если есть
        paths_dict = service_funcs.read_config()
        vs.previous_toplevel_window.textbox.configure(state='normal')
        vs.previous_toplevel_window.textbox.delete('0.0', tkinter.END)
        if paths_dict != False:
            paths_str = vs.previous_toplevel_window.get_paths(paths_dict)
            vs.previous_toplevel_window.textbox.insert("0.0", paths_str)
        vs.previous_toplevel_window.textbox.configure(state='disabled')
        vs.toplevel_window = vs.previous_toplevel_window
        vs.previous_toplevel_window.deiconify()
        vs.previous_toplevel_window = None
        self.clear_edit_temps()
        self.grab_release()
        self.destroy()

    def confirm(self):
        name = vs.temp_name
        if name:
            amount = self.e_amount.get()
            if amount.isdigit():
                if 0 < int(amount) < 8:
                    if service_funcs.read_config() != False:
                        vs.multi_paths = service_funcs.read_config()
                    if vs.multi_paths == '':
                        vs.multi_paths = {}

                    uniq_flag = False

                    if not vs.temp_from_pathes and vs.temp_from_pathes_old:
                        vs.temp_from_pathes = vs.temp_from_pathes_old

                    for path in vs.temp_from_pathes:
                        if vs.temp_to_path + '/' == service_funcs.get_folder_path(path):
                            uniq_flag = True

                    if vs.temp_to_path != '' and len(vs.temp_from_pathes) > 0 and not uniq_flag:
                        uniq_name_flag = False
                        if vs.multi_paths:
                            for key in vs.multi_paths:
                                if name == key and name != vs.temp_name:
                                    uniq_name_flag = True
                        if not uniq_name_flag:
                            vs.temp_name = name
                            vs.temp_amount = int(amount)

                            no_multiple = 'False'
                            if vs.temp_no_multiple_flag:
                                no_multiple = 'True'

                            if vs.temp_date:
                                if vs.today_flag:
                                    vs.multi_paths[name] = {
                                        'from_path': vs.temp_from_pathes,
                                        'to_path': vs.temp_to_path,
                                        'on_date': vs.temp_date,
                                        'today': 'True',
                                        'amount': vs.temp_amount,
                                        'no_multiple': no_multiple
                                    }
                                else:
                                    vs.multi_paths[name] = {
                                        'from_path': vs.temp_from_pathes,
                                        'to_path': vs.temp_to_path,
                                        'on_date': vs.temp_date,
                                        'today': 'False',
                                        'amount': vs.temp_amount,
                                        'no_multiple': no_multiple
                                    }
                            else:
                                vs.multi_paths[name] = {
                                    'from_path': vs.temp_from_pathes,
                                    'to_path': vs.temp_to_path,
                                    'on_date': 'False',
                                    'today': 'False',
                                    'amount': vs.temp_amount,
                                    'no_multiple': no_multiple
                                }

                            # Перезаписываем конфиг
                            code = service_funcs.update_config(vs.multi_paths)
                            if code:
                                mes.showinfo('Добавление маршрута', f'Маршрут {name} успешно изменен!')
                                vs.temp_name = ''
                                vs.temp_from_path = ''
                                vs.temp_to_path = ''
                                vs.temp_name = ''
                                vs.temp_date = 'False'

                                vs.date_flag = False

                                vs.today_flag = False
                                vs.temp_date_old = ''

                                vs.temp_amount = 3

                                vs.temp_no_multiple_flag = False
                                self.no_multiple_checkbox.deselect()
                                vs.temp_no_multiple_flag = self.no_multiple_checkbox.get()

                                self.dismiss()
                        else:
                            mes.showerror('Ошибка добавления имени', f'Указанное имя маршрута "{name}" уже есть в списке!')
                    else:
                        mes.showerror('Ошибка добавления пути', 'Укажите корректные пути копирования!')
                else:
                    mes.showerror('Ошибка указания количества', 'Количество копий должно быть числом от 1 до 7!')
            else:
                mes.showerror('Ошибка указания количества', 'Количество копий должно быть числом!')
        else:
            mes.showerror('Ошибка добавления пути', 'Укажите корректное имя маршрута!')

    def add_from_folder(self):
        initial = vs.usr_desktop
        vs.temp_new_path = []
        # vs.temp_from_pathes = []
        vs.temp_from_names = []
        if vs.last_folder == '':
            if not vs.file_flag_edit:
                folder = fd.askdirectory(title="Укажите папку из которой требуется провести копирование",
                                         initialdir=initial)
                if folder != '':
                    vs.temp_from_pathes = []
                    vs.temp_new_path = []
                    vs.temp_new_path.append(folder)
                    vs.last_folder = service_funcs.get_folder_path(folder)
            else:
                vs.temp_new_path = fd.askopenfilenames(title="Укажите файлы, которые требуется скопировать",
                                                       initialdir=initial)
                if vs.temp_new_path:
                    vs.last_folder = service_funcs.get_folder_path(vs.temp_new_path[0])
                else:
                    vs.temp_new_path = []
        else:
            if not vs.file_flag_edit:
                folder = fd.askdirectory(title="Укажите папку из которой требуется провести копирование",
                                         initialdir=vs.last_folder)
                if folder != '':
                    vs.temp_from_pathes = []
                    vs.temp_new_path = []
                    vs.temp_new_path.append(folder)
                    vs.last_folder = service_funcs.get_folder_path(folder)
            else:
                vs.temp_new_path = fd.askopenfilenames(title="Укажите файлы, которые требуется копировать",
                                                       initialdir=vs.last_folder)
                if vs.temp_new_path:
                    vs.last_folder = service_funcs.get_folder_path(vs.temp_new_path[0])
                else:
                    vs.temp_new_path = []
        if vs.temp_new_path:
            for path in vs.temp_new_path:
                vs.temp_from_pathes.append(path)
            for path in vs.temp_from_pathes:
                vs.temp_from_names.append(os.path.basename(path))

            names_str = ''
            for name in vs.temp_from_names:
                names_str += name + '; '

            self.e_path_from.configure(state='normal')
            self.e_path_from.delete(0, tkinter.END)
            self.e_path_from.insert(0, names_str)
            self.e_path_from.configure(state='disabled')
            vs.temp_new_path = []

    def add_to_folder(self):
        initial = vs.usr_desktop
        if vs.last_folder == '':
            vs.temp_new_path = fd.askdirectory(title="Укажите папку в которую требуется провести копирование",
                                               initialdir=initial)
        else:
            vs.temp_new_path = fd.askdirectory(title="Укажите папку в которую требуется провести копирование",
                                               initialdir=vs.last_folder)
        if vs.temp_new_path != '':
            vs.last_folder = vs.temp_new_path
            self.e_path_to.configure(state='normal')
            self.e_path_to.delete(0, tkinter.END)
            vs.temp_to_path = ''
            self.e_path_to.insert(0, vs.temp_new_path)
            vs.temp_to_path = vs.temp_new_path
            vs.temp_new_path = ''
            self.e_path_to.configure(state='disabled')
