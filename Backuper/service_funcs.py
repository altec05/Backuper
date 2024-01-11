import datetime
from pathlib import Path
import os
import variables as vs
import messages as mes
import json
import shutil
from distutils.dir_util import copy_tree
import pytz


def str_to_true_date_format(new_date):
    return datetime.date.strftime(datetime.datetime.strptime(new_date, '%Y-%m-%d'), '%d.%m.%Y')


def true_date_format(new_date):
    return datetime.date.strftime(new_date, '%d.%m.%Y')


# Проверка на пустоту каталога
def empty_or_not(path):
    try:
        return next(os.scandir(path), None)
    except:
        return None


# Проверка запрашиваемого пути
def check_path(path):
    if os.path.exists(path):
        return True
    else:
        return False


# Получения словаря маршрутов из конфиг-файла
def read_config():
    file_path = vs.path_config
    if check_path(vs.path_config):
        with open(file_path, 'r') as f:
            loaded_dict = json.load(f)
        return loaded_dict
    else:
        return False


# Перезапись конфиг-файла словарем маршрутов
def update_config(paths):
    # Проверяем и создаем если нет конфиг-файла
    file_path = vs.path_config
    if not check_path(vs.path_config):
        try:
            if paths:
                if len(paths) > 0:
                    with open(file_path, 'w') as f:
                        json.dump(paths, f, ensure_ascii=False)

                    if check_path(vs.path_config):
                        return True
                else:
                    try:
                        os.remove(vs.path_config)
                        return True
                    except FileNotFoundError:
                        return False
            else:
                try:
                    os.remove(vs.path_config)
                    return True
                except FileNotFoundError:
                    return False
        except Exception as e:
            mes.showwarning('Создание конфигурационного файла',
                            f'Не удалось записать конфигурационный файл.\nПричина:\n[{e}]')
            return False
    else:
        try:
            if paths:
                if len(paths) > 0:
                    with open(file_path, 'w') as f:
                        json.dump(paths, f, ensure_ascii=False)
                else:
                    try:
                        os.remove(vs.path_config)
                        return True
                    except FileNotFoundError:
                        return False
                return True
            else:
                try:
                    os.remove(vs.path_config)
                    return True
                except FileNotFoundError:
                    return False
        except Exception as e:
            mes.showwarning('Перезапись конфигурационного файла',
                            f'Не удалось перезаписать конфигурационный файл.\nПричина:\n[{e}]')
            return False


def get_folder_path(path):
    send_data = path.replace(os.path.basename(path), '')
    return send_data


def backup(path, final_path, self, name, size):
    # Если это файл, а не папка
    if not os.path.isdir(path):
        # Копируем файл
        self.solo_backup_label.configure(text=f'Копирую: {path}, размер: {size}')
        try:
            result_file = shutil.copy2(path, final_path)
            vs.rez_list.append(
                f'{len(vs.rez_list) + 1}. "{name}":\nФайл "{result_file}" - успешно!\nиз: "{get_folder_path(path)}"\nв: "{final_path}".\n\n')
        except Exception as e:
            vs.rez_list.append(
                f'{len(vs.rez_list) + 1}. "{name}":\nФайл "{path}" не скопирован по причине: "{e}".\n\n')
    else:
        # Копируем дерево каталога из начального пути в конечную папку
        if os.path.isdir(path):
            self.solo_backup_label.configure(text=f'Копирую: {path}, размер: {size}')
            try:
                result = copy_tree(path, final_path)
                vs.rez_list.append(
                    f'{len(vs.rez_list) + 1}. "{name}":\nПапка "{path}" - успешно!\nв "{final_path}"\nФайлов: {len(result)}.\n\n')
            except Exception as e:
                vs.rez_list.append(
                    f'{len(vs.rez_list) + 1}. "{name}":\nПапка "{path}" не скопирована по причине: "{e}".\n\n')
        else:
            self.solo_backup_label.configure(text=f'Копирую: {path}, размер: {size}')
            try:
                result_file = shutil.copy2(path, final_path)
                vs.rez_list.append(
                    f'{len(vs.rez_list) + 1}. "{name}":\nФайл "{result_file}" - успешно!\nиз: "{get_folder_path(path)}"\nв: "{final_path}".\n\n')
            except Exception as e:
                vs.rez_list.append(
                    f'{len(vs.rez_list) + 1}. "{name}":\nФайл "{path}" не скопирован по причине: "{e}".\n\n')


# Резервное копирование по заданному пути
def backup_bd(from_path, to_path, name, on_date, amount, self):
    # Дата для создания папки текущего дня
    now_date = datetime.datetime.now().date().strftime("%d.%m.%Y")

    # Финальный путь с датой
    final_path = os.path.join(to_path, name, now_date)

    # Путь к финальной папке с именем, но без текущей даты для проверки существования
    root_dir = final_path.replace(now_date, '')

    # Если уже есть папка за текущую дату
    if empty_or_not(root_dir) is not None:
        self.solo_backup_label.configure(text=f'Очищаю старые копии в: {root_dir}')
        # Очищаем конечную папку, не трогая файлы с текущей датой
        clear_old_backups(root_dir, final_path, amount)

    if empty_or_not(final_path) is not None:
        if vs.clear_folder_before_flag:
            self.solo_backup_label.configure(text=f'Очищаю файлы в: {final_path}')
            # Очищаем конечную папку
            clear_folder(final_path)
        else:
            if mes.askyesno('Проверка пути для копирования',
                            f'Внимание! Конечная папка {final_path} содержит файлы. Очистить её и продолжить копирование?\n\nФайлы:\n{os.listdir(final_path)}'):
                self.solo_backup_label.configure(text=f'Очищаю файлы в: {final_path}')
                # Очищаем конечную папку
                clear_folder(final_path)

    # Если нет конечного пути, то создаем папку
    if not check_path(final_path):
        self.solo_backup_label.configure(text=f'Создаю путь: {final_path}')
        os.makedirs(final_path, exist_ok=True)

    for path in from_path:
        # Если путь для копирования существует
        if check_path(path):
            self.solo_backup_label.configure(text_color='yellow')
            self.solo_backup_label.configure(text=f'Копирую для "{name}":\n{path}')
            if on_date != 'False' and on_date != '':
                true_files = []
                files_temp = os.listdir(path)
                for file in files_temp:
                    # Устанавливаем часовой пояс Красноярска
                    timezone = pytz.timezone('Asia/Krasnoyarsk')

                    # Получаем время создания файла
                    temp1 = os.path.getctime(os.path.join(path, file))
                    utctime = pytz.utc.localize(datetime.datetime.utcfromtimestamp(temp1))
                    astimezone = utctime.astimezone(timezone)
                    localtime = timezone.normalize(astimezone).date()

                    # Получаем дату из маршрута для проверки
                    check_date = datetime.datetime.strptime(str(on_date), '%Y-%m-%d').date()

                    # Сверяем даты
                    if localtime == check_date:
                        true_files.append(os.path.join(path, file))
                if true_files:
                    for file in true_files:
                        # Размер копируемого файла в байтах
                        size = os.path.getsize(file)
                        # Переводим размер файла
                        n = 0
                        power = 2 ** 10
                        size_labels = {0: '', 1: 'К', 2: 'М', 3: 'Г', 4: 'Т'}
                        while size > power:
                            size /= power
                            n += 1
                        size_str = str(round(size, 2)) + size_labels[n] + 'б.'

                        backup(file, final_path, self, name, size_str)
                        vs.copied_routes.append(name)
                else:
                    vs.rez_list.append(
                        f'{len(vs.rez_list) + 1}. "{name}":\nНе найдены файлы!\nПо пути: {path}.\nЗа дату: "{true_date_format(on_date)}".\n\n')
            else:
                # Размер копируемого файла в байтах
                size = os.path.getsize(path)
                # Переводим размер файла
                n = 0
                power = 2 ** 10
                size_labels = {0: '', 1: 'К', 2: 'М', 3: 'Г', 4: 'Т'}
                while size > power:
                    size /= power
                    n += 1
                size_str = str(round(size, 2)) + size_labels[n] + 'б.'

                backup(path, final_path, self, name, size_str)
                vs.copied_routes.append(name)
        # Нечего копировать
        else:
            mes.showerror('Резервное копирование файлов', f'Ошибка: начальный путь не существует!\n\n{path}')


def clear_old_backups(root, pass_path, amount):
    paths = sorted(Path(root).iterdir(), key=os.path.getmtime)
    if len(paths) >= amount:
        ind = len(paths) - amount + 1

        for path in paths[: ind]:
            if str(path) == str(pass_path):
                continue
            else:
                try:
                    shutil.rmtree(path)
                except Exception as e:
                    mes.showwarning('Удаление старой копии', f'При попытке удаления старой копии файлов'
                                                             f' произошла ошибка!\n{e}\nУдаляли папку {path}')


# Удаление файла
def clear_file(file_path):
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    except Exception as e:
        mes.showwarning('Ошибка удаления', f'Ошибка удаления {file_path}. Причина: {e}.')


# Удаление файлов в папке
def clear_folder(path):
    folder = path
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        clear_file(file_path)
