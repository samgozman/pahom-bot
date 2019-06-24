from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from pahom import settings
from pahom import dialogflow

def work(tg_token):
    # Подключаемся к ТГ
    updater = Updater(token=tg_token)

    # Токен API к Telegram
    dispatcher = updater.dispatcher
    name_user = ""
    # Обработка команд


    def startCommand(bot, update):
        name_user = update.message.from_user.first_name

        PahomStart = ("Здравствуй, " + name_user + "! "
                        "Я слабоумная, патриотическая, радиоактивная нейронная сеть Пахом ДП-10.  Со мной можно пообщаться на разные темы - от Путина до My little Pony. "
                        "Но предупреждаю: я первая в мире нейронная сеть страдающая аутизмом и шизофренией "
                        "(унаследовал от источника исследования - Дмитрия Пахомова aka 'Кровавого тирана' aka 'ДП-10' aka etc)"
                    )
        bot.send_message(chat_id=update.message.chat_id, text=PahomStart)


    def textMessage(bot, update):
        name_user = update.message.from_user.first_name
        user_message = str(update.message.text)
        bot.send_message(chat_id=update.message.chat_id, text=dialogflow.getTextAnswer(user_message, name_user, True))


    # Хендлеры
    start_command_handler = CommandHandler('start', startCommand)
    text_message_handler = MessageHandler(Filters.text, textMessage)
    # Добавляем хендлеры в диспетчер
    dispatcher.add_handler(start_command_handler)
    dispatcher.add_handler(text_message_handler)
    # Начинаем поиск обновлений
    updater.start_polling(clean=True)
    # Останавливаем бота, если были нажаты Ctrl + C
    updater.idle()
