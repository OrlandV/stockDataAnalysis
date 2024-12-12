"""
Вычисления.
"""


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
