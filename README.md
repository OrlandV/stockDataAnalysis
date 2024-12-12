# Анализ и визуализация данных об акциях

Консольное приложение, которое
1. загружает из Интернета исторические данные об акциях для указанного тикера и временного периода,
2. рассчитывает скользящее среднее для цен закрытия,
3. строит графики для цен закрытия и скользящего среднего и сохраняет их в PNG-файл,
4. вычисляет и выводит в консоль среднюю цену закрытия акций за указанный период,
5. уведомляет пользователя (в консоли), если цена акций колебалась более чем на заданный процент за период.

## ⚙ Зависимости

Разработка и тестирование производились на стеке:

![Static Badge](https://img.shields.io/badge/Python-3.12.7-%233776AB)
![Static Badge](https://img.shields.io/badge/yfinance-0.2.50-black)
![Static Badge](https://img.shields.io/badge/pandas-2.2.3-black)
![Static Badge](https://img.shields.io/badge/matplotlib-3.9.3-black)

Установка библиотек:
```bash
pip install yfinance pandas matplotlib
```

## 🖥 Использование

1. Запуск приложения производится командой
    ```bash
    python main.py
    ```

2. После приветствия и краткого описания приложение попросит ввести тикер.
    ```text
    Добро пожаловать в инструмент получения и построения графиков биржевых данных.
    Вот несколько примеров биржевых тикеров, которые вы можете рассмотреть: AAPL (Apple Inc), GOOGL (Alphabet Inc), MSFT (Microsoft Corporation), AMZN (Amazon.com Inc), TSLA (Tesla Inc).
    Общие периоды времени для данных о запасах включают: 1д, 5д, 1мес, 3мес, 6мес, 1г, 2г, 5л, 10л, с начала года, макс.
    Введите тикер акции (например, «AAPL» для Apple Inc): 
    ```

3. После ввода тикера, приложение попросит ввести период для данных.
    ```text
    Введите период для данных (например, '1mo' для одного месяца): 
    ```

4. Загружаются данные из Интернета.
5. Рассчитывается скользящее среднее.
6. Строятся графики цены закрытия и скользящего среднего.
7. Графики сохраняются в PNG-файл.
8. В консоль выводится сообщение о сохранении графиков.
9. В консоль выводится средняя цена закрытия акций за заданный период.
10. Приложение просит указать порог колебаний в процентах.
    ```text
    Укажите порог колебаний в процентах: 
    ```
    Если пользователь ошибся во вводе, приложение вернётся к вводу, объявив об ошибке.
    ```text
    Ошибка! Требуется указать число. Для отделения целой части от дробной используйте точку.
    Укажите порог колебаний в процентах: 
    ```
11. Уведомление пользователя, если цена акций колебалась более чем на заданный процент за период.
