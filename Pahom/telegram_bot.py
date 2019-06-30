import logging
import re
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from pahom import dialogflow
from pahom import settings
from pahom import vk_bot

# Вывод лога ошибок
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def check_admin_privileges(bot,update):
    name_user = update.message.from_user.username
    # Проверяем есть ли юзер в админском составе. Если да, то выдать меню. Нет - выдать марковку))
    if name_user in settings.admin:
        return True
    else:
        bot.send_message(chat_id=update.message.chat_id, text=dialogflow.text_answer("топология", name_user, True))
        return False


def work(tg_token):
    # Подключаемся к ТГ
    updater = Updater(token=tg_token)

    # Токен API к Telegram
    dispatcher = updater.dispatcher
    # Обработка команд

    def start_command(bot, update):
        # Функция вызова стартовой команды
        name_user = update.message.from_user.first_name
        pahom_start = ("Здравствуй, " + name_user + "! "
                        "Я слабоумная, патриотическая, радиоактивная нейронная сеть Пахом ДП-10.  Со мной можно пообщаться на разные темы - от Путина до My little Pony. "
                        "Но предупреждаю: я первая в мире нейронная сеть страдающая аутизмом и шизофренией "
                        "(унаследовал от источника исследования - Дмитрия Пахомова aka 'Кровавого тирана' aka 'ДП-10' aka etc)"
                    )
        bot.send_message(chat_id=update.message.chat_id, text=pahom_start)

    def text_message(bot, update):
        # Функция считывания сообщеня и отправки ответа
        name_user = update.message.from_user.first_name
        user_message = str(update.message.text)

        bot.send_message(chat_id=update.message.chat_id, text=dialogflow.text_answer(user_message, name_user, True))

    def error(update, context):
        # Обработчик ошибок
        """Log Errors caused by Updates."""
        logger.warning('Update "%s" caused error "%s"', update, context.error)

    # Хендлеры
    updater.dispatcher.add_error_handler(error)

    def help_command(bot, update):
        # Функция вызова стартовой команды
        name_user = update.message.from_user.first_name
        pahom_help = "Help"
        if check_admin_privileges(bot,update):
            # vk_bot.action_dump_post("https://vk.com/club183833688?w=wall-183833688_483")
            vk_bot.action_create_post("https://vk.com/dveberezy")
        bot.send_message(chat_id=update.message.chat_id, text=pahom_help)

    start_command_handler = CommandHandler('start', start_command)
    help_command_handler = CommandHandler('help', help_command)
    text_message_handler = MessageHandler(Filters.text, text_message)
    # Добавляем хендлеры в диспетчер
    dispatcher.add_handler(start_command_handler)
    dispatcher.add_handler(help_command_handler)
    dispatcher.add_handler(text_message_handler)
    # Начинаем поиск обновлений
    updater.start_polling(clean=True)
    # Останавливаем бота, если были нажаты Ctrl + C
    updater.idle()
