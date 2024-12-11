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
