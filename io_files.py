"""
Запись данных в файлы и чтение данных из файлов.
"""

import os


def make_path(filename: str):
    """
    Создание пути до файла.
    :param filename: Путь к файлу.
    """
    path = os.path.dirname(filename)
    if path and not os.path.exists(path):
        os.mkdir(path)


def save_plot(plt, filename: str) -> bool:
    """
    Сохранение графиков в файл.
    :param plt: Графики matplotlib.pyplot.
    :param filename: Путь к файлу.
    :return: Успех операции.
    """
    make_path(filename)
    plt.savefig(filename)
    return True


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
        make_path(filename)  # Если путь не существует, создать.
        data.to_csv(filename)  # Экспорт DataFrame в CSV.
    except Exception as err:
        print('Возникла ошибка при экспорте данных в CSV.', err)
        return False
    else:
        return True
