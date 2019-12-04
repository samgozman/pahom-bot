# -*- coding: utf-8 -*-
# !/usr/bin/env python3.7
from threading import Thread

from pahom import jsonloads
from pahom import settings
from pahom import telegram_bot
from pahom import nonsense
from pahom import rest

if __name__ == '__main__':
    # Генерация бредней пахома при старте скрипта (кол-во строк)
    nonsense.generate_model(100000)
    # Выгуражаем все JSON файлы в память для быстрой работы
    jsonloads.parse_json()
    # telegram_bot.work(settings.telegram_API_token_1)

    t1 = Thread(target=telegram_bot.work, args=(settings.telegram_API_token_1,))
    # t2 = Thread(target=rest.api.run, args=('0.0.0.0',))
    # t2.daemon = True

    t1.start()
    # t2.start()

    t1.join()
    # t2.join()

    rest.api.run(host='0.0.0.0', ssl_context=('/root/.acme.sh/shavlu.ga/shavlu.ga.cer', '/root/.acme.sh/shavlu.ga/shavlu.ga.key'))


