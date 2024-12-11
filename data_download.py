"""
Загрузка данных об акциях из Интернета.
"""
import yfinance as yf


def fetch_stock_data(ticker: str, period: str = '1mo'):
    """
    Получение исторических данных об акциях для указанного тикера и временного периода.
    :param ticker: Тикер.
    :param period: Временной период.
    :return: DataFrame с данными.
    """
    stock = yf.Ticker(ticker)
    data = stock.history(period=period)
    return data


# Планируется перенести функцию в модуль вычислений (calculate).
def add_moving_average(data, window_size: int = 5):
    """
    Добавление в DataFrame колонки со скользящим средним, рассчитанным на основе цен закрытия.
    :param data: DataFrame с данными.
    :param window_size: Временное окно.
    :return: DataFrame с данными.
    """
    data['Moving_Average'] = data['Close'].rolling(window=window_size).mean()
    return data
