# -*- coding: utf-8 -*-
import logging
import os
from multiprocessing import Process

from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

from pahom import response
from pahom import settings

# Вывод лога ошибок
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def work(tg_token):
    # Подключаемся к ТГ
    updater = Updater(tg_token, use_context=True)

    # Токен API к Telegram
    dispatcher = updater.dispatcher

    # Обработка команд

    def start_command(update: Update, context: CallbackContext):
        # Функция вызова стартовой команды
        bot = context.bot
        name_user = update.message.from_user.first_name
        pahom_start = ("Здравствуй, " + name_user + "! "
                                                    "Я слабоумная, патриотическая, радиоактивная нейронная сеть Пахом ДП-10.  Со мной можно пообщаться на разные темы - от Путина до My little Pony. "
                                                    "Но предупреждаю: я первая в мире нейронная сеть страдающая аутизмом и шизофренией "
                                                    "(унаследовал от источника исследования - Дмитрия Пахомова aka 'Кровавого тирана' aka 'ДП-10' aka etc)"
                       )
        bot.send_message(chat_id=update.message.chat_id, text=pahom_start)

    def text_message(update: Update, context: CallbackContext):
        # Функция считывания сообщеня и отправки ответа
        bot = context.bot
        name_user = update.message.from_user.first_name
        user_message = str(update.message.text)
        bot.send_message(chat_id=update.message.chat_id, text=response.text_answer(user_message, name_user))

    def error(update, context):
        logger.warning('Update "%s" caused error "%s"', update, context.error)

    # Хендлеры
    updater.dispatcher.add_error_handler(error)

    start_command_handler = CommandHandler('start', start_command)
    text_message_handler = MessageHandler(Filters.text, text_message)
    # Добавляем хендлеры в диспетчер
    dispatcher.add_handler(start_command_handler)
    dispatcher.add_handler(text_message_handler)
    # Начинаем поиск обновлений
    updater.start_polling(clean=True)
    # Останавливаем бота, если были нажаты Ctrl + C
    updater.idle()
