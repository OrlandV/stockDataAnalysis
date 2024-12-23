import dateutil.parser as date_parser
import data_download as dd
import data_plotting as dplt
import calculate
import io_files


def input_period() -> tuple[str | None, str | None, str | None, int]:
    """
    Ввод временного периода.
    :return: Кортеж: дата начала, дата конца, общий период, номер режима.
    """
    start = None
    end = None
    period = 'max'
    while True:
        print('Выберите режим ввода временного периода:\n1 — общий период.\n2 — даты начала и конца.')
        mode = input('Режим: ')
        try:
            mode = int(mode)
            if mode not in (1, 2):
                raise ValueError('Требуется ввод цифры 1 или 2.')
            break
        except ValueError as err:
            print('Ошибка в введённых данных! Проверьте номер режима.', err)
    if mode == 1:
        while True:
            period = input('Введите период для данных (например, «1mo» для одного месяца): ')
            if period not in ('1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max'):
                print('Ошибка в введённых данных! Проверьте период. Ожидается один из вариантов: '
                      '1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max.')
            else:
                break
    else:
        while True:
            try:
                start = input('Введите дату начала временного периода для данных '
                              '(например, «2024-10-01» для 1 октября 2024): ')
                start = date_parser.parse(start).strftime('%Y-%m-%d')  # Парсинг-проверка даты.
                end = input('Введите дату конца временного периода для данных '
                            '(например, «2025-01-01» для 31 декабря 2024): ')
                end = date_parser.parse(end).strftime('%Y-%m-%d')  # Парсинг-проверка даты.
                break
            except ValueError as err:
                print('Ошибка в введённых данных! Проверьте даты.', err)
    return start, end, period, mode


def add_indicator(data, func, indicator: str) -> tuple:
    """
    Добавление в DataFrame колонки с индикатором.
    :param data: DataFrame с данными.
    :param func: Функция соответствующего индикатора.
    :param indicator: Наименование индикатора.
    :return: Кортеж: DataFrame с данными и флаг добавления графика индикатора.
    """
    while True:
        ind = input(f'Добавить индикатор {indicator}? y/N ')
        if ind == 'N':
            return data, False
        elif ind == 'y' or ind == 'Y':
            return func(data), True
        else:
            print('Ошибка ввода!')


def select_style() -> str | None:
    """
    Выбор стиля графиков.
    :return: Наименование стиля.
    """
    list_of_style = dplt.plt.style.available
    print('Выбор стиля графиков. Укажите номер желаемого стиля.')
    print('0 — default')
    for i, style in enumerate(list_of_style):
        print(f'{i + 1} — {style}')
    while True:
        style = input('Ваш выбор: ')
        try:
            style = int(style)
            ls = len(list_of_style)
            if style < 0 or style > ls:
                raise ValueError(f'Требуется указать целое число от 0 до {ls}.')
        except ValueError as err:
            print('Ошибка в введённых данных! Проверьте номер стиля.', err)
        else:
            if style == 0:
                style = None
            else:
                style = list_of_style[style - 1]
            break
    return style


def input_threshold() -> float:
    """
    Ввод порога колебаний.
    :return: Порог колебаний.
    """
    while True:
        threshold = input('Укажите порог колебаний в процентах: ')
        try:
            threshold = float(threshold)
            return threshold
        except ValueError:
            print('Ошибка! Требуется указать число. Для отделения целой части от дробной используйте точку.')


def main():
    print("Добро пожаловать в инструмент получения и построения графиков биржевых данных.")
    print("Вот несколько примеров биржевых тикеров, которые вы можете рассмотреть: AAPL (Apple Inc), "
          "GOOGL (Alphabet Inc), MSFT (Microsoft Corporation), AMZN (Amazon.com Inc), TSLA (Tesla Inc).")
    print("Общие периоды времени для данных об акциях включают: "
          "1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max.")
    print('Вместо общих периодов можно указать начальную и конечную даты временного периода.')

    ticker = input('Введите тикер акции (например, «AAPL» для Apple Inc): ')
    start, end, period, mode = input_period()

    # Fetch stock data
    stock_data = dd.fetch_stock_data(ticker, start, end, period)

    # Замена в именах файлов общего периода точными датами при втором режиме.
    if mode == 2:
        period = f'{start}_{end}'

    # Add moving average to the data
    stock_data = calculate.add_moving_average(stock_data)

    # Добавление в DataFrame колонки с индикатором RSI.
    stock_data, rsi = add_indicator(stock_data, calculate.add_rsi, 'RSI')

    # Добавление в DataFrame колонки с индикатором MACD.
    stock_data, macd = add_indicator(stock_data, calculate.add_macd, 'MACD')

    # Выбор стиля графиков.
    style = select_style()

    # Имя файла для сохранения графиков.
    filename = input('Для сохранения графиков введите имя PNG-файла (путь) без расширения '
                     f'(по умолчанию — {ticker}_{period}_stock_price_chart'
                     f'{'' if style is None else '_' + style}.png): ')
    if not filename:
        filename = None

    # Plot the data
    dplt.create_and_save_plot(stock_data, ticker, period, filename, rsi, macd, style)

    # Вычисление и вывод в консоль средней цены закрытия акций за заданный период.
    calculate.calculate_and_display_average_price(stock_data)

    # Уведомление пользователя, если цена акций колебалась более чем на заданный процент за период.
    calculate.notify_if_strong_fluctuations(stock_data, input_threshold())

    # Экспорт данных в CSV-файл.
    csv_file = input('Для сохранения данных введите имя CSV-файла (путь) без расширения (по умолчанию — stock): ')
    if io_files.export_data_to_csv(stock_data, csv_file):
        print(f'Данные экспортированы в «{csv_file if csv_file else 'stock'}.csv».')


if __name__ == "__main__":
    main()
