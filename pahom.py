# Настройки
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import apiai, json, markovify

updater = Updater(token='800954163:AAFX12rmEPkiF567sPYN8X22AuryUuMiR3Q', request_kwargs={
    'proxy_url': 'socks5://172.104.238.234:2016/',
    'urllib3_proxy_kwargs': {
        'username': 'cock',
        'password': 'kukareku'
    }
})

# Get raw text as string.
with open("shiza.txt") as f:
    text = f.read()

# Build the model.
text_model = markovify.Text(text)

# Токен API к Telegram
dispatcher = updater.dispatcher
# Обработка команд
def startCommand(bot, update):
    if message.chat.username == "":
        nameuser = message.chat.first_name + " " + message.chat.last_name
    else:
        nameuser = message.chat.username
    PahomStart = ("Здравствуй, " + nameuser + "! "
                    "Я слабоумная, патриотическая, радиоактивная нейронная сеть Пахом ДП-10.  Со мной можно пообщаться на разные темы - от Путина до My little Pony. "
                    "Но предупреждаю: я первая в мире нейронная сеть страдающая аутизмом и шизофренией "
                    "(унаследовал от источника исследования - Дмитрия Пахомова aka 'Кровавого тирана' aka 'ДП-10' aka etc)"
                )
    bot.send_message(chat_id=update.message.chat_id, text=PahomStart)
def textMessage(bot, update):
    request = apiai.ApiAI('01a00134d0b848c9827aa4de126cee01').text_request() # Токен API к Dialogflow
    request.version = 2 # версия API
    request.lang = 'ru' # На каком языке будет послан запрос
    request.session_id = 'dp10_bot' # ID Сессии диалога (нужно, чтобы потом учить бота)
    request.query = update.message.text # Посылаем запрос к ИИ с сообщением от юзера
    responseJson = json.loads(request.getresponse().read().decode('utf-8'))

    # print(json.dumps(responseJson, indent=4, sort_keys=True))
    responseID = responseJson['result']['action'] # action_name диалога для определения тематики вопроса
    print(responseID)
    response = responseJson['result']['fulfillment']['speech'] # Разбираем JSON и вытаскиваем ответ
    # Если есть ответ от бота - присылаем юзеру, если нет - бот его не понял
    if response:
        bot.send_message(chat_id=update.message.chat_id, text=response)
    else:
        # Print five randomly-generated sentences
        bot.send_message(chat_id=update.message.chat_id, text=text_model.make_sentence())
        # bot.send_message(chat_id=update.message.chat_id, text='DialogFlow response error')
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
