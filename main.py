import dateutil.parser as date_parser
import data_download as dd
import data_plotting as dplt
import calculate
import io_files


def main():
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

    print("Добро пожаловать в инструмент получения и построения графиков биржевых данных.")
    print("Вот несколько примеров биржевых тикеров, которые вы можете рассмотреть: AAPL (Apple Inc), "
          "GOOGL (Alphabet Inc), MSFT (Microsoft Corporation), AMZN (Amazon.com Inc), TSLA (Tesla Inc).")
    print("Общие периоды времени для данных об акциях включают: "
          "1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max.")
    print('Вместо общих периодов можно указать начальную и конечную даты временного периода.')

    start = None
    end = None
    period = 'max'
    ticker = input('Введите тикер акции (например, «AAPL» для Apple Inc): ')
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

    # Имя файла для сохранения графиков.
    filename = input('Для сохранения графиков введите имя PNG-файла (путь) без расширения '
                     f'(по умолчанию — {ticker}_{period}_stock_price_chart.png): ')
    if not filename:
        filename = None

    # Plot the data
    dplt.create_and_save_plot(stock_data, ticker, period, filename, rsi, macd)

    # Вычисление и вывод в консоль средней цены закрытия акций за заданный период.
    calculate.calculate_and_display_average_price(stock_data)

    # Уведомление пользователя, если цена акций колебалась более чем на заданный процент за период.
    while True:
        threshold = input('Укажите порог колебаний в процентах: ')
        try:
            threshold = float(threshold)
            break
        except ValueError:
            print('Ошибка! Требуется указать число. Для отделения целой части от дробной используйте точку.')
    calculate.notify_if_strong_fluctuations(stock_data, threshold)

    # Экспорт данных в CSV-файл.
    csv_file = input('Для сохранения данных введите имя CSV-файла (путь) без расширения (по умолчанию — stock): ')
    if io_files.export_data_to_csv(stock_data, csv_file):
        print(f'Данные экспортированы в «{csv_file if csv_file else 'stock'}.csv».')


if __name__ == "__main__":
    main()
