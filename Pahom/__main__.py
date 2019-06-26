#!/usr/bin/env python3.7
from threading import Thread

from pahom import settings
from pahom import text_search
from pahom import telegram_bot
from pahom import jsonloads

if __name__ == '__main__':
    # Генерация бредней пахома при старте скрипта (кол-во строк)
    text_search.generate_model(100000)

    # Выгуражаем все JSON файлы в память для быстрой работы
    jsonloads.parse_json()

    # telegram_bot.work(settings.telegram_API_token_1)
    #

    t1 = Thread(target=telegram_bot.work, args=(settings.telegram_API_token_1,))
    t2 = Thread(target=telegram_bot.work, args=(settings.telegram_API_token_2,))

    t1.start()
    t2.start()

    t1.join()
    t2.join()
