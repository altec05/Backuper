import os

try:
    import tkinter
    from tkinter import ttk
except ImportError:
    import Tkinter
    import ttk
# import tkinter
# from tkinter import ttk
from PIL import Image
from tkcalendar import Calendar

import customtkinter as CTk

import service_funcs
import variables as vs
import tkinter.filedialog as fd
import messages as mes


class AddFolderWindow(CTk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("950x400")

        self.title('Добавление пути')
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

        # Добавить
        self.confirm_frame = CTk.CTkFrame(master=self, fg_color='transparent')
        self.confirm_frame.pack(fill='x', ipadx=10, ipady=10, padx=20)

        self.label = CTk.CTkLabel(self.label_frame, text="Укажите параметры для нового пути")
        self.label.pack(fill='x')

        self.e_name = CTk.CTkEntry(self.name_frame, placeholder_text="Наименование пути", width=350)
        self.e_name.pack(fill='x')

        vs.date_flag = False

        def checkbox_date_event():
            vs.date_flag = self.date_checkbox.get()
            if vs.date_flag:
                vs.temp_date_old = ''
                vs.temp_date = ''
                self.file_from_checkbox.configure(state='disabled')
                self.today_checkbox.configure(state='normal')
                self.b_date.configure(state='normal')
                self.file_from_checkbox.deselect()
                vs.file_flag = self.file_from_checkbox.get()
                self.clear_e_from()
                self.e_data.configure(state='normal')
                self.e_data.delete(0, tkinter.END)
                if vs.temp_date != '':
                    self.e_data.insert(0, service_funcs.str_to_true_date_format(vs.temp_date))
                self.e_data.configure(state='disabled')
                self.today_checkbox.configure(state='normal')
            else:
                self.file_from_checkbox.configure(state='normal')
                self.today_checkbox.deselect()
                self.today_checkbox.configure(state='disabled')
                self.b_date.configure(state='disabled')
                self.e_data.configure(state='normal')
                self.e_data.delete(0, tkinter.END)
                self.e_data.configure(state='disabled')
                vs.temp_date = ''
                vs.temp_date_old = ''
                vs.today_flag = False
                vs.date_flag = False

        self.date_checkbox = CTk.CTkCheckBox(master=self.date_frame,
                                             text="Файлы из каталога по дате",
                                             command=checkbox_date_event, onvalue=True, offvalue=False,
                                             corner_radius=6, border_width=1)
        self.date_checkbox.pack(side='left', ipadx=5, ipady=5, pady=5, anchor='w')

        vs.today_flag = False

        def checkbox_today_event():
            vs.today_flag = self.today_checkbox.get()
            if vs.today_flag:
                vs.temp_date_old = vs.temp_date
                vs.temp_date = str(vs.date_today)
                self.b_date.configure(state='disabled')
                self.e_data.configure(state='normal')
                self.e_data.delete(0, tkinter.END)
                if vs.temp_date != '' and vs.temp_date != 'False':
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
                vs.temp_date = vs.temp_date_old
                vs.temp_date_old = ''
                self.b_date.configure(state='normal')
                self.e_data.configure(state='normal')
                self.e_data.delete(0, tkinter.END)
                if vs.temp_date != '' and vs.temp_date != 'False':
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
                                             corner_radius=6, border_width=1, state='disabled')
        self.today_checkbox.pack(side='left', ipadx=5, ipady=5, pady=5, padx=25, anchor='w')

        self.b_date = CTk.CTkButton(self.date_frame, text='Указать дату', command=self.get_date, state='disabled')
        self.b_date.pack(padx=10, pady=5, side='left')

        self.e_data = CTk.CTkEntry(self.date_frame, placeholder_text="Дата", width=80, state='disabled')
        self.e_data.pack(padx=25, pady=5, side='left')

        vs.file_flag = False

        self.b_path_from = CTk.CTkButton(self.from_frame, text='Указать откуда', command=self.add_from_folder)
        self.b_path_from.pack(pady=5, side='left')

        self.e_path_from = CTk.CTkEntry(self.from_frame, placeholder_text="Скопировать из", state='disabled', width=650)
        self.e_path_from.pack(padx=10, side='left')

        def checkbox_event():
            vs.file_flag = self.file_from_checkbox.get()
            self.clear_e_from()

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

        self.clear_e_from()

        self.b_path_to = CTk.CTkButton(self.to_frame, text='Указать куда', command=self.add_to_folder)
        self.b_path_to.pack(pady=5, side='left')

        self.e_path_to = CTk.CTkEntry(self.to_frame, placeholder_text="Скопировать в", state='disabled', width=800)
        self.e_path_to.pack(padx=10, pady=5, side='right')

        self.l_amount = CTk.CTkLabel(self.amount_frame, text="Максимум копий:")
        self.l_amount.pack(fill='x', side='left')

        self.e_amount = CTk.CTkEntry(self.amount_frame, state='normal', width=50)
        self.e_amount.pack(padx=20, side='left')
        self.e_amount.insert(0, 3)

        self.b_confirm = CTk.CTkButton(self.amount_frame, text='Добавить маршрут', command=self.confirm)
        self.b_confirm.pack(padx=10, side='right')

        self.focus()
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", lambda: self.dismiss())  # перехватываем нажатие на крестик

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
        vs.temp_new_path = []

    def clear_add_temps(self):
        vs.temp_name = ''
        vs.file_flag = False
        vs.today_flag = False
        vs.date_flag = False
        vs.temp_date = ''
        vs.temp_to_path = ''
        vs.temp_new_path = []
        vs.temp_date_old = ''
        vs.temp_from_pathes = []
        vs.temp_from_names = []
        vs.temp_amount = 3

    def dismiss(self):
        vs.toplevel_window = None
        self.clear_add_temps()
        vs.previous_window.deiconify()
        vs.previous_window = None
        self.grab_release()
        self.destroy()

    def confirm(self):
        name = self.e_name.get().strip(' ')
        if name:
            amount = self.e_amount.get()
            if amount.isdigit():
                if 0 < int(amount) < 8:
                    if service_funcs.read_config() != False:
                        vs.multi_paths = service_funcs.read_config()
                    if vs.multi_paths == '':
                        vs.multi_paths = {}

                    uniq_flag = False

                    for path in vs.temp_from_pathes:
                        if vs.temp_to_path + '/' == service_funcs.get_folder_path(path):
                            uniq_flag = True

                    if vs.temp_to_path != '' and len(vs.temp_from_pathes) > 0 and not uniq_flag:
                        uniq_name_flag = False
                        if vs.multi_paths:
                            for key in vs.multi_paths:
                                if name == key:
                                    uniq_name_flag = True
                        if not uniq_name_flag:
                            vs.temp_name = name
                            vs.temp_amount = int(amount)
                            if vs.temp_date:
                                if vs.today_flag:
                                    vs.multi_paths[name] = {
                                        'from_path': vs.temp_from_pathes,
                                        'to_path': vs.temp_to_path,
                                        'on_date': vs.temp_date,
                                        'today': 'True',
                                        'amount': vs.temp_amount
                                    }
                                else:
                                    vs.multi_paths[name] = {
                                        'from_path': vs.temp_from_pathes,
                                        'to_path': vs.temp_to_path,
                                        'on_date': vs.temp_date,
                                        'today': 'False',
                                        'amount': vs.temp_amount
                                    }
                            else:
                                vs.multi_paths[name] = {
                                    'from_path': vs.temp_from_pathes,
                                    'to_path': vs.temp_to_path,
                                    'on_date': 'False',
                                    'today': 'False',
                                    'amount': vs.temp_amount
                                }
                            # Перезаписываем конфиг
                            code = service_funcs.update_config(vs.multi_paths)
                            if code:
                                mes.showinfo('Добавление маршрута', f'Маршрут {name} успешно записан!')
                                self.e_name.delete(0, tkinter.END)
                                vs.temp_name = ''

                                self.e_path_from.configure(state='normal')
                                self.e_path_from.delete(0, tkinter.END)
                                self.e_path_from.configure(state='disabled')
                                vs.temp_from_path = ''

                                self.e_path_to.configure(state='normal')
                                self.e_path_to.delete(0, tkinter.END)
                                self.e_path_to.configure(state='disabled')
                                vs.temp_to_path = ''

                                vs.temp_date = ''
                                vs.date_flag = False
                                self.b_date.configure(state='disabled')
                                self.e_data.configure(state='normal')
                                self.e_data.delete(0, tkinter.END)
                                self.e_data.configure(state='disabled')
                                self.date_checkbox.deselect()

                                vs.file_flag = False
                                self.file_from_checkbox.deselect()
                                vs.file_flag = self.file_from_checkbox.get()
                                self.clear_e_from()

                                vs.today_flag = False
                                self.today_checkbox.deselect()
                                self.today_checkbox.configure(state='disabled')
                                vs.temp_date_old = ''

                                vs.temp_amount = 3
                                self.e_amount.configure(state='normal')
                                self.e_amount.delete(0, tkinter.END)
                                self.e_amount.insert(0, vs.temp_amount)
                                self.e_amount.configure(state='disabled')
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
        vs.temp_from_names = []
        if vs.last_folder == '':
            if not vs.file_flag:
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
            if not vs.file_flag:
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
