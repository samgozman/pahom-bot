#!/usr/bin/env python3.7
from threading import Thread

from pahom import settings
from pahom import text_search
from pahom import telegram_bot

# Генерация бредней пахома при старте скрипта
text_search.generatePizdec(500)

# telegram_bot.work(settings.telegram_API_token_1)
#

token1: str = settings.telegram_API_token_1
token2: str = settings.telegram_API_token_2

t1 = Thread(target=telegram_bot.work, args=(token1,))
t2 = Thread(target=telegram_bot.work, args=(token2,))

t1.start()
t2.start()

t1.join()
t2.join()