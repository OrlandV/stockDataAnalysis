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
