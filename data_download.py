"""
Загрузка данных об акциях из Интернета.
"""
import yfinance as yf


def fetch_stock_data(ticker: str, start: str | None = None, end: str | None = None, period: str = 'max'):
    """
    Получение исторических данных об акциях для указанного тикера и временного периода.
    :param ticker: Тикер.
    :param start: Дата начала временного периода.
    :param end: Дата конца временного периода.
    :param period: Временной период.
    :return: DataFrame с данными.
    """
    stock = yf.Ticker(ticker)
    data = stock.history(start=start, end=end, period=period)
    return data
