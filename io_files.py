"""
Запись данных в файлы и чтение данных из файлов.
"""

import os


def export_data_to_csv(data, filename: str = 'stock') -> bool:
    """
    Экспорт данных в CSV.
    :param data: DataFrame с данными.
    :param filename: Имя CSV-файла (путь) без расширения.
    :return: Успех экспорта.
    """
    if not filename:  # Если пустая строка, то значение по умолчанию.
        filename = 'stock'
    filename += '.csv'
    try:
        # Если путь не существует, создать.
        path = os.path.dirname(filename)
        if path and not os.path.exists(path):
            os.mkdir(path)
        data.to_csv(filename)  # Экспорт DataFrame в CSV.
    except Exception as err:
        print('Возникла ошибка при экспорте данных в CSV.', err)
        return False
    else:
        return True
