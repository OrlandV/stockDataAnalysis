"""
Визуализация данных.
"""
import matplotlib.pyplot as plt
import pandas as pd
from io_files import save_plot


def create_and_save_plot(data, ticker: str, period: str, filename: str | None = None,
                         rsi: bool = False, macd: bool = False, std: bool = False, style: str | None = None) -> None:
    """
    Создание графика, отображающего цены закрытия и скользящие средние.
    Предоставляет возможность добавления индикаторов RSI и MACD, а так же сохранения графика в файл.
    :param data: DataFrame с данными.
    :param ticker: Тикер.
    :param period: Временной период.
    :param filename: Путь и имя файла для сохранения.
    :param rsi: Флаг добавления индикатора RSI.
    :param macd: Флаг добавления индикатора MACD.
    :param std: Флаг добавления индикатора STD — стандартного отклонения.
    :param style: Стиль графиков.
    """
    rows = 1 + rsi + macd + std
    if style:
        plt.style.use(style)
    if rows == 1:  # Индикаторы не добавлять.
        plt.figure(figsize=(10, 6))
        plt.title(f"{ticker} Цена акций с течением времени")
        plt.ylabel('Цена')
        plt_c_mv = plt
    else:  # Добавление индикаторов.
        fig, axs = plt.subplots(rows, 1, layout='constrained', figsize=(15, 6 * rows))
        plt_c_mv = axs[0]
        plt_c_mv.set_title(f"{ticker} Цена акций с течением времени")
        plt_c_mv.set_ylabel('Цена')
        if macd:
            plt_macd = axs[1] if not rsi else axs[2]
        if std:
            plt_std = axs[1] if rows == 2 else axs[2] if rows == 3 else axs[3]
    if 'Date' not in data:
        if pd.api.types.is_datetime64_any_dtype(data.index):
            dates = data.index.to_numpy()
            plt_c_mv.plot(dates, data['Close'].values, label='Цена закрытия')
            plt_c_mv.plot(dates, data['Moving_Average'].values, label='Скользящее среднее')
            if rsi:
                axs[1].plot(dates, pd.Series(30.0, index=dates), linewidth=1)
                axs[1].plot(dates, pd.Series(70.0, index=dates), linewidth=1)
                axs[1].plot(dates, data['RSI'].values)
            if macd:
                plt_macd.plot(dates, pd.Series(0, dates), color='black', linewidth=0.5)
                plt_macd.plot(dates, data['MACD_S'].values, color='#FF6D00')
                plt_macd.plot(dates, data['MACD'].values, color='#2962FF')
                plt_macd.bar(dates, data['MACD_H'].values, color='#26A69A')
                # color=('#26A69A' if data['MACD_H'].values.all() and data['MACD_H'].values.all() > 0 else '#FF5252')
            if std:
                plt_std.plot(dates, pd.Series(0, dates), color='black', linewidth=0.5)
                plt_std.plot(dates, data['STD'].values)
        else:
            print("Информация о дате отсутствует или не имеет распознаваемого формата.")
            return
    else:
        if not pd.api.types.is_datetime64_any_dtype(data['Date']):
            data['Date'] = pd.to_datetime(data['Date'])
        plt_c_mv.plot(data['Date'], data['Close'], label='Цена закрытия')
        plt_c_mv.plot(data['Date'], data['Moving_Average'], label='Скользящее среднее')
        if rsi:
            axs[1].plot(data['Date'], pd.Series(30.0, index=data['Date']), linewidth=1)
            axs[1].plot(data['Date'], pd.Series(70.0, index=data['Date']), linewidth=1)
            axs[1].plot(data['Date'], data['RSI'])
        if macd:
            plt_macd.plot(data['Date'], pd.Series(0, data['Date']), color='black', linewidth=0.5)
            plt_macd.plot(data['Date'], data['MACD_S'], color='#FF6D00')
            plt_macd.plot(data['Date'], data['MACD'], color='#2962FF')
            plt_macd.bar(data['Date'], data['MACD_H'], color='#26A69A')
            # color=('#26A69A' if data['MACD_H'] and data['MACD_H'] > 0 else '#FF5252')
        if std:
            plt_std.plot(data['Date'], pd.Series(0, data['Date']), color='black', linewidth=0.5)
            plt_std.plot(data['Date'], data['STD'])
    plt_c_mv.legend()
    plt_c_mv.grid()
    if rsi:
        axs[1].set_ylabel('RSI')
        axs[1].grid()
    if macd:
        plt_macd.set_ylabel('MACD')
        plt_macd.grid()
    if std:
        plt_std.set_ylabel('STD')
        plt_std.grid()
    plt.xlabel("Дата")

    filename = (f'{ticker}_{period}_stock_price_chart{'' if style is None else '_' + style}.png'
                if filename is None else filename + '.png')
    save_plot(plt, filename)
