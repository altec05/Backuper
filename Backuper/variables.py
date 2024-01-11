import datetime
import os

import changes_list

# Текущая версия программы
app_version = changes_list.last_change_version
app_last_edit_version = changes_list.last_change_data

# Файл config для хранения путей копирования
path_config = os.path.abspath('config.json')

# Папка "Документы" пользователя
usr_docs = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Documents')
# Папка "Рабочий стол"
usr_desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
# Последняя открытая папка
last_folder = ''

# Переменная состояния верхнего окна
toplevel_window = None
previous_toplevel_window = None
previous_window = None

# Название папки и абсолютный путь к папке для одиночного копирования
solo_folder = ''
solo_folder_path = ''

# Получение нового пути для множественного копирования
date_flag = False
file_flag = False
file_flag_edit = False

# Указание даты для файлов в каталоге
date_today_true = datetime.date.strftime(datetime.date.today(), '%d.%m.%Y')
date_today = datetime.date.today()
temp_date = ''
temp_from_pathes_old = []
temp_from_names_old = []

# Количество копий
temp_amount = 3

# Перезапись и удаление файлов
clear_folder_before_flag = True

# Без множественного копирования
temp_no_multiple_flag = False


# Указание перезаписи даты на текущую дату при проверке
today_flag = False
temp_date_old = ''
temp_new_path = []
temp_to_path = ''
temp_from_pathes = []
temp_from_names = []
temp_name = ''

# Хранение путей для множественного копирования
multi_paths = {}

# Результат копирования
rez_list = []

# Список маршрутов, для которых уже прошло копирование
copied_routes = []
