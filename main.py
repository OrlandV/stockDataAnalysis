import data_download as dd
import data_plotting as dplt
import calculate
import io_files


def main():
    print("Добро пожаловать в инструмент получения и построения графиков биржевых данных.")
    print("Вот несколько примеров биржевых тикеров, которые вы можете рассмотреть: AAPL (Apple Inc), "
          "GOOGL (Alphabet Inc), MSFT (Microsoft Corporation), AMZN (Amazon.com Inc), TSLA (Tesla Inc).")
    print("Общие периоды времени для данных о запасах включают: "
          "1д, 5д, 1мес, 3мес, 6мес, 1г, 2г, 5л, 10л, с начала года, макс.")

    ticker = input("Введите тикер акции (например, «AAPL» для Apple Inc): ")
    period = input("Введите период для данных (например, '1mo' для одного месяца): ")

    # Fetch stock data
    stock_data = dd.fetch_stock_data(ticker, period)

    # Add moving average to the data
    stock_data = calculate.add_moving_average(stock_data)

    # Plot the data
    dplt.create_and_save_plot(stock_data, ticker, period)

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
