"""
Вычисления.
"""

# from technical_indicator.momentum import RSI, MACDHistogram
# pandas_ta и stock-indicators оказались несовместимы с текущим стеком.


def add_moving_average(data, window_size: int = 5):
    """
    Добавление в DataFrame колонки со скользящим средним, рассчитанным на основе цен закрытия.
    :param data: DataFrame с данными.
    :param window_size: Временное окно.
    :return: DataFrame с данными.
    """
    data['Moving_Average'] = data['Close'].rolling(window=window_size).mean()
    return data


def calculate_and_display_average_price(data) -> None:
    """
    Вычисление и вывод в консоль средней цены закрытия акций за заданный период.
    :param data: DataFrame с данными.
    """
    ap = data['Close'].mean()
    print(f'Средняя цена: {ap:.4f}')


def notify_if_strong_fluctuations(data, threshold: float) -> None:
    """
    Уведомление пользователя, если цена акций колебалась более чем на заданный процент за период.
    :param data: DataFrame с данными.
    :param threshold: Порог колебаний.
    """
    fluctuation = (data['Close'].max() - data['Close'].min()) / data['Close'].mean() * 100
    if fluctuation > threshold:
        print(f'Цена акций колебалась на {fluctuation:.2f} %.')


def add_rsi(data, period: int = 14):
    """
    Добавление в DataFrame колонки с индикатором RSI.
    :param data: DataFrame с данными.
    :param period: Длина периода (или количество периодов).
    :return: DataFrame с данными.
    """
    # Вариант с использованием technical_indicator работает некорректно.
    # rsi = RSI(data['Close'].to_numpy(), period)
    # data['RSI'] = rsi.calculate_rsi('numpy_array')

    delta = data['Close'].diff(1)
    gain = delta.clip(lower=0)
    loss = delta.clip(upper=0)
    avg_gain = gain.rolling(window=period, min_periods=period).mean()
    avg_loss = loss.abs().rolling(window=period, min_periods=period).mean()
    for i, row in enumerate(avg_gain.iloc[period + 1:]):
        avg_gain.iloc[i + period + 1] = (avg_gain.iloc[i + period] * (period - 1) + gain.iloc[i + period + 1]) / period
    for i, row in enumerate(avg_loss.iloc[period + 1:]):
        avg_loss.iloc[i + period + 1] = (avg_loss.iloc[i + period] * (period - 1) - loss.iloc[i + period + 1]) / period
    rs = avg_gain / avg_loss
    data['RSI'] = 100 - (100 / (1.0 + rs))
    return data


def add_macd(data, fast_periods: int = 12, slow_periods: int = 26, signal_periods: int = 9):
    """
    Добавление в DataFrame колонки с индикатором MACD.
    :param data: DataFrame с данными.
    :param fast_periods: Количество периодов (F) для более быстрой скользящей средней. Должно быть больше 0.
    :param slow_periods: Количество периодов для более медленной скользящей средней.
        Должно быть больше, чем fast_periods.
    :param signal_periods: Количество периодов (P) для скользящей средней MACD. Должно быть больше или равно 0.
    :return: DataFrame с данными.
    """
    # Вариант с использованием technical_indicator работает некорректно.
    # macd_histogram = MACDHistogram(data['Close'].to_numpy(), fast_periods, slow_periods, signal_periods)
    # data['MACD'] = macd_histogram.calculate_macd_histogram('numpy_array')

    k = data['Close'].ewm(span=fast_periods, adjust=False, min_periods=fast_periods).mean()
    d = data['Close'].ewm(span=slow_periods, adjust=False, min_periods=slow_periods).mean()
    macd = k - d
    macd_s = macd.ewm(span=signal_periods, adjust=False, min_periods=signal_periods).mean()
    macd_h = macd - macd_s
    data['MACD'] = data.index.map(macd)
    data['MACD_H'] = data.index.map(macd_h)
    data['MACD_S'] = data.index.map(macd_s)
    return data


def add_std(data, window: int = 20):
    data['STD'] = data['Close'].rolling(window).std()
    return data
