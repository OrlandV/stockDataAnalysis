"""
Вычисления.
"""


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
