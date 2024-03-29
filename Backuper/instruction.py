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


class InstructionWindow(CTk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("1400x600+500+300")
        self.title('Инструкция к программе')
        self.resizable(width=True, height=False)
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

    # Выход из окна настройки
    def dismiss(self):
        vs.toplevel_window = None
        vs.temp_name = ''
        vs.previous_window.deiconify()
        vs.previous_window = None
        self.grab_release()
        self.destroy()

    def update_textbox(self):
        instruction_str = self.get_instruction_row()

        self.textbox.configure(state='normal')
        self.textbox.delete('0.0', tkinter.END)
        self.textbox.insert("0.0", instruction_str)
        self.textbox.configure(state='disabled')

    def get_instruction_row(self):
        instruction_row = """Как взаимодействовать с программой?

        1. Для начала работы создайте маршрут:
        
            - Кнопка "Добавить маршрут".
            - Укажите наименование маршрута.
            
            - Укажите откуда осуществлять копирование:
                1. Если требуется копировать файлы, укажите галку "Файлы" в правой части окна.
                2. Если требуется копировать файлы за конкретную дату, укажите галку "Файлы из каталога по дате" и укажите дату по кнопке "Указать дату", после чего увидите её в поле.
                3. Если требуется копировать файлы всегда за текущую дату, укажите галку "Файлы из каталога по дате" и галку "Всегда текущая дата", после чего увидите её в поле.
                4. Если требуется копировать папку и её содержимое, то не указывайте галки.
                После выбора типа копируемых объектов укажите начальный путь по кнопке "Указать откуда", после чего увидите его в поле рядом.
            
            - Укажите куда осуществлять копирование:
                В указанной папке будет создана папка с наименованием маршрута и далее создана папка с текущей датой, куда и будет произведено копирование.
            
            - Укажите максимальное количество резервных копий, хранимых в конечной папке.
            
            - Укажите требуется ли учитывать маршрут при множественном копировании. В случае включения галки маршрут будет исключен и будет копироваться лишь при выборочном (ручном) копировании.
            
            - По кнопке "Добавить маршрут" сохраните маршрут.
        
        2. Для того чтобы увидеть список всех маршрутов и редактировать/удалить один из них перейдите в окно редактирования по кнопке "Настроить".
        
            - Для взаимодействия впишите наименование маршрута в поле в нижней части экрана и нажмите необходимую кнопку.
                Окно редактирования маршрута содержит функционал аналогичный окну создания маршрута.
                
            - Для очистки всех маршрутов нажмите кнопку "Очистить список в верхней части окна" и подтвердите удаление.
        
        3. Для запуска одиночного копирования перейдите в окно старта по кнопке "Выборочное копирование", после чего выберите маршрут и начните копирование.
        
        4. Для запуска массового копирования по всем маршрутам нажмите кнопку "Начать" в правой части окна.
        
        5. Если при копировании вы согласны на очистку конечной папки, если она уже существует, то оставьте галку "Очищать конечную папку" включенной. Для отображения подтверждения отключите её.
        
        6. Для смены темы приложения выберите в выпадающем списке в нижней части окна 'Light' - для светлой, 'Dark' - для темной и 'System' - для темы согласно выбранной теме в вашей операционной системе.
        """
        return instruction_row

