"""
Визуализация данных.
"""
import matplotlib.pyplot as plt
import pandas as pd


def create_and_save_plot(data, ticker: str, period: str, filename: str | None = None) -> None:
    """
    Создание графика, отображающего цены закрытия и скользящие средние.
    Предоставляет возможность сохранения графика в файл.
    :param data: DataFrame с данными.
    :param ticker: Тикер.
    :param period: Временной период.
    :param filename: Путь и имя файла для сохранения.
    """
    plt.figure(figsize=(10, 6))

    if 'Date' not in data:
        if pd.api.types.is_datetime64_any_dtype(data.index):
            dates = data.index.to_numpy()
            plt.plot(dates, data['Close'].values, label='Цена закрытия')
            plt.plot(dates, data['Moving_Average'].values, label='Скользящее среднее')
        else:
            print("Информация о дате отсутствует или не имеет распознаваемого формата.")
            return
    else:
        if not pd.api.types.is_datetime64_any_dtype(data['Date']):
            data['Date'] = pd.to_datetime(data['Date'])
        plt.plot(data['Date'], data['Close'], label='Цена закрытия')
        plt.plot(data['Date'], data['Moving_Average'], label='Скользящее среднее')

    plt.title(f"{ticker} Цена акций с течением времени")
    plt.xlabel("Дата")
    plt.ylabel("Цена")
    plt.legend()

    if filename is None:
        filename = f"{ticker}_{period}_stock_price_chart.png"

    plt.savefig(filename)
    print(f"Графики сохранены как {filename}")
