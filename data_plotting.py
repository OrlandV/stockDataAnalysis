"""
Визуализация данных.
"""
import matplotlib.pyplot as plt
import pandas as pd
from io_files import save_plot
import plotly.graph_objs as go
from plotly.subplots import make_subplots


def create_and_save_plot(data, ticker: str, period: str, filename: str | None = None,
                         rsi: bool = False, macd: bool = False, std: bool = False, style: str | None = None) -> None:
    """
    Создание графика, отображающего цены закрытия и скользящие средние.
    Предоставляет возможность добавления индикаторов RSI, MACD и STD, а так же сохранения графика в файл.
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
            plt_std = axs[rows - 1]
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


def inter_plot(data, ticker: str, rsi: bool = False, macd: bool = False, std: bool = False) -> None:
    """
    Создание интерактивного графика, отображающего цены закрытия и скользящие средние.
    Предоставляет возможность добавления индикаторов RSI, MACD и STD.
    :param data: DataFrame с данными.
    :param ticker: Тикер.
    :param rsi: Флаг добавления индикатора RSI.
    :param macd: Флаг добавления индикатора MACD.
    :param std: Флаг добавления индикатора STD — стандартного отклонения.
    """
    rows = 1 + rsi + macd + std

    # Вариант 1. Под курсором выводится информация по всем фигурам.
    # layout = dict(
    #     hoversubplots="axis",
    #     title=dict(text=f"{ticker} Цена акций с течением времени"),
    #     hovermode="x",
    #     grid=dict(rows=rows, columns=1)
    # )
    # data_ = []
    # if 'Date' not in data:
    #     if pd.api.types.is_datetime64_any_dtype(data.index):
    #         dates = data.index.to_numpy()
    #         data_.append(go.Scatter(x=dates, y=data['Close'].values, xaxis="x", yaxis="y", name='Цена закрытия'))
    #         data_.append(go.Scatter(x=dates, y=data['Moving_Average'].values, xaxis="x", yaxis="y",
    #                                 name='Скользящее среднее'))
    #         if rsi:
    #             data_.append(go.Scatter(x=dates, y=pd.Series(30, dates), xaxis="x", yaxis="y2", line=dict(width=1),
    #                                     hovertemplate='<extra></extra>', showlegend=False))
    #             data_.append(go.Scatter(x=dates, y=pd.Series(70, dates), xaxis="x", yaxis="y2", line=dict(width=1),
    #                                     hovertemplate='<extra></extra>', showlegend=False))
    #             data_.append(go.Scatter(x=dates, y=data['RSI'].values, xaxis="x", yaxis="y2", name='RSI',
    #                                     showlegend=False))
    #         if macd:
    #             data_.append(go.Scatter(x=dates, y=pd.Series(0, dates), xaxis="x", yaxis="y3", showlegend=False,
    #                                     line=dict(color='#000000', width=0.5), hovertemplate='<extra></extra>'))
    #             data_.append(go.Scatter(x=dates, y=data['MACD_S'].values, xaxis="x", yaxis="y3", name='MACD_S',
    #                                     line=dict(color='#FF6D00'), showlegend=False))
    #             data_.append(go.Scatter(x=dates, y=data['MACD'].values, xaxis="x", yaxis="y3", name='MACD',
    #                                     line=dict(color='#2962FF'), showlegend=False))
    #             data_.append(go.Bar(x=dates, y=data['MACD_H'].values, xaxis="x", yaxis="y3", name='MACD_H',
    #                                 marker=dict(color='#26A69A'), showlegend=False))
    #         if std:
    #             data_.append(go.Scatter(x=dates, y=pd.Series(0, dates), xaxis="x", yaxis="y4", showlegend=False,
    #                                     line=dict(color='#000000', width=0.5), hovertemplate='<extra></extra>'))
    #             data_.append(go.Scatter(x=dates, y=data['STD'].values, xaxis="x", yaxis="y4", name='STD',
    #                                     showlegend=False))
    #     else:
    #         print("Информация о дате отсутствует или не имеет распознаваемого формата.")
    #         return
    # else:
    #     if not pd.api.types.is_datetime64_any_dtype(data['Date']):
    #         data['Date'] = pd.to_datetime(data['Date'])
    #     data_.append(go.Scatter(x=data['Date'], y=data['Close'], xaxis="x", yaxis="y", name='Цена закрытия'))
    #     data_.append(go.Scatter(x=data['Date'], y=data['Moving_Average'], xaxis="x", yaxis="y",
    #                             name='Скользящее среднее'))
    #     if rsi:
    #         data_.append(go.Scatter(x=data['Date'], y=pd.Series(30, data['Date']), xaxis="x", yaxis="y2",
    #                                 line=dict(width=1), hovertemplate='<extra></extra>', showlegend=False))
    #         data_.append(go.Scatter(x=data['Date'], y=pd.Series(70, data['Date']), xaxis="x", yaxis="y2",
    #                                 line=dict(width=1), hovertemplate='<extra></extra>', showlegend=False))
    #         data_.append(go.Scatter(x=data['Date'], y=data['RSI'], xaxis="x", yaxis="y2", name='RSI',
    #                                 showlegend=False))
    #     if macd:
    #         data_.append(go.Scatter(x=data['Date'], y=pd.Series(0, data['Date']), xaxis="x", yaxis="y3",
    #                                 line=dict(color='#000000', width=0.5), hovertemplate='<extra></extra>',
    #                                 showlegend=False))
    #         data_.append(go.Scatter(x=data['Date'], y=data['MACD_S'], xaxis="x", yaxis="y3", name='MACD_S',
    #                                 line=dict(color='#FF6D00'), showlegend=False))
    #         data_.append(go.Scatter(x=data['Date'], y=data['MACD'], xaxis="x", yaxis="y3", name='MACD',
    #                                 line=dict(color='#2962FF'), showlegend=False))
    #         data_.append(go.Bar(x=data['Date'], y=data['MACD_H'], xaxis="x", yaxis="y3", name='MACD_H',
    #                             marker=dict(color='#26A69A'), showlegend=False))
    #     if std:
    #         data_.append(go.Scatter(x=data['Date'], y=pd.Series(0, data['Date']), xaxis="x", yaxis="y4",
    #                                 line=dict(color='#000000', width=0.5), hovertemplate='<extra></extra>',
    #                                 showlegend=False))
    #         data_.append(go.Scatter(x=data['Date'], y=data['STD'], xaxis="x", yaxis="y4", name='STD',
    #                                 showlegend=False))
    # fig = go.Figure(data=data_, layout=layout)

    # Вариант 2. Высота фигур индикаторов 1/3 высоты основной фигуры.
    if macd:
        row_macd = 2 if not rsi else 3
    fig = make_subplots(rows=rows, cols=1, row_heights=[1 if r else 3 for r in range(rows)])
    if 'Date' not in data:
        if pd.api.types.is_datetime64_any_dtype(data.index):
            dates = data.index.to_numpy()
            fig.add_trace(go.Scatter(x=dates, y=data['Close'].values, name='Цена закрытия'), 1, 1)
            fig.add_trace(go.Scatter(x=dates, y=data['Moving_Average'].values, name='Скользящее среднее'), 1, 1)
            if rsi:
                fig.add_trace(go.Scatter(x=dates, y=pd.Series(30.0, dates), showlegend=False, line=dict(width=1),
                                         hovertemplate='<extra></extra>'), 2, 1)
                fig.add_trace(go.Scatter(x=dates, y=pd.Series(70.0, dates), showlegend=False, line=dict(width=1),
                                         hovertemplate='<extra></extra>'), 2, 1)
                fig.add_trace(go.Scatter(x=dates, y=data['RSI'].values, name='RSI', showlegend=False), 2, 1)
            if macd:
                fig.add_trace(go.Scatter(x=dates, y=pd.Series(0, dates), hovertemplate='<extra></extra>',
                                         line=dict(color='#000000', width=0.5), showlegend=False), row_macd, 1)
                fig.add_trace(go.Scatter(x=dates, y=data['MACD_S'].values, line=dict(color='#FF6D00'),
                                         showlegend=False, name='MACD_S'), row_macd, 1)
                fig.add_trace(go.Scatter(x=dates, y=data['MACD'].values, line=dict(color='#2962FF'),
                                         showlegend=False, name='MACD'), row_macd, 1)
                fig.add_trace(go.Bar(x=dates, y=data['MACD_H'].values, marker=dict(color='#26A69A'), name='MACD_H',
                                     showlegend=False), row_macd, 1)
            if std:
                fig.add_trace(go.Scatter(x=dates, y=pd.Series(0, dates), hovertemplate='<extra></extra>',
                                         showlegend=False, line=dict(color='#000000', width=0.5)), rows, 1)
                fig.add_trace(go.Scatter(x=dates, y=data['STD'].values, name='STD', showlegend=False), rows, 1)
        else:
            print("Информация о дате отсутствует или не имеет распознаваемого формата.")
            return
    else:
        if not pd.api.types.is_datetime64_any_dtype(data['Date']):
            data['Date'] = pd.to_datetime(data['Date'])
        fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name='Цена закрытия'), 1, 1)
        fig.add_trace(go.Scatter(x=data['Date'], y=data['Moving_Average'], name='Скользящее среднее'), 1, 1)
        if rsi:
            fig.add_trace(go.Scatter(x=data['Date'], y=pd.Series(30.0, data['Date']), showlegend=False,
                                     hovertemplate='<extra></extra>', line=dict(width=1)), 2, 1)
            fig.add_trace(go.Scatter(x=data['Date'], y=pd.Series(70.0, data['Date']), showlegend=False,
                                     hovertemplate='<extra></extra>', line=dict(width=1)), 2, 1)
            fig.add_trace(go.Scatter(x=data['Date'], y=data['RSI'], name='RSI', showlegend=False), 2, 1)
        if macd:
            fig.add_trace(go.Scatter(x=data['Date'], y=pd.Series(0, data['Date']), showlegend=False,
                                     hovertemplate='<extra></extra>', line=dict(color='#000000', width=0.5)),
                          row_macd, 1)
            fig.add_trace(go.Scatter(x=data['Date'], y=data['MACD_S'], line=dict(color='#FF6D00'), name='MACD_S',
                                     showlegend=False), row_macd, 1)
            fig.add_trace(go.Scatter(x=data['Date'], y=data['MACD'], line=dict(color='#2962FF'), name='MACD',
                                     showlegend=False), row_macd, 1)
            fig.add_trace(go.Bar(x=data['Date'], y=data['MACD_H'], marker=dict(color='#26A69A'), name='MACD_H',
                                 showlegend=False), row_macd, 1)
        if std:
            fig.add_trace(go.Scatter(x=data['Date'], y=pd.Series(0, data['Date']), showlegend=False,
                                     hovertemplate='<extra></extra>', line=dict(color='#000000', width=0.5)), rows, 1)
            fig.add_trace(go.Scatter(x=data['Date'], y=data['STD'], name='STD', showlegend=False), rows, 1)
    fig.update_layout(
        hovermode='x',
        legend=dict(x=1, y=1.04, xanchor='right', yanchor='top'),
        legend_orientation='h',
        title=f"{ticker} Цена акций с течением времени",
        yaxis_title='Цена'
    )
    if rsi:
        fig.update_xaxes(showticklabels=False, row=1, col=1)
        fig.update_yaxes(title='RSI', row=2, col=1)
    if macd:
        fig.update_xaxes(showticklabels=False, row=row_macd - 1, col=1)
        fig.update_yaxes(title='MACD', row=row_macd, col=1)
    if std:
        fig.update_xaxes(showticklabels=False, row=rows - 1, col=1)
        fig.update_yaxes(title='STD', row=rows, col=1)
    fig.update_xaxes(title='Дата', row=rows, col=1)

    fig.show()
