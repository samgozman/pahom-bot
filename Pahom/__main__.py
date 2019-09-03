# -*- coding: utf-8 -*-
# !/usr/bin/env python3.7
from threading import Thread

from pahom import jsonloads
from pahom import settings
from pahom import telegram_bot
from pahom import text_search

if __name__ == '__main__':
    # Генерация бредней пахома при старте скрипта (кол-во строк)
    text_search.generate_model(300000)

    # Выгуражаем все JSON файлы в память для быстрой работы
    jsonloads.parse_json()

    # telegram_bot.work(settings.telegram_API_token_1)
    #
    # вызываем генерацию ключа api для вк.
    t1 = Thread(target=telegram_bot.work, args=(settings.telegram_API_token_1,))
    t2 = Thread(target=telegram_bot.work, args=(settings.telegram_API_token_2,))

    t1.start()
    t2.start()
    # t3.start()

    t1.join()
    t2.join()
    # t3.join()
