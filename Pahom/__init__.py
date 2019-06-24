#!/usr/bin/env python3.7
# Настройки
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import apiai
import json
import emoji

from pahom import settings
from pahom import text_search

# Подключаемся к ТГ
updater = Updater(token=settings.telegram_API_token)

intent_emoji = {
    "pahom.error": ":new_moon_with_face:",
    "pahom.agent.army": ":gun:",
    "pahom.agent.bio": ":pill:",
    "pahom.agent.busy": ":sweat_drops:",
    "pahom.agent.bye": ":runner:",
    "pahom.agent.chasha": ":evergreen_tree:",
    "pahom.agent.cinema": ":movie_camera:",
    "pahom.agent.culture": ":art:",
    "pahom.agent.emotion.agressive": ":rage:",
    "pahom.agent.emotion.crazy": ":scream:",
    "pahom.agent.emotion.negative": ":angry:",
    "pahom.agent.emotion.positive": ":ok_hand:",
    "pahom.agent.facts": ":zap:",
    "pahom.agent.god": ":pray:",
    "pahom.agent.gta": ":oncoming_police_car:",
    "pahom.agent.hello": ":wave:",
    "pahom.agent.it": ":floppy_disk:",
    "pahom.agent.kit": ":whale:",
    "pahom.agent.kolsk": ":o:",
    "pahom.agent.minecraft": ":space_invader:",
    "pahom.agent.navalny": ":tea:",
    "pahom.agent.novel": ":books:",
    "pahom.agent.patriot": ":ru:",
    "pahom.agent.photo": ":camera:",
    "pahom.agent.politic": ":circus_tent:",
    "pahom.agent.pony": ":rainbow:",
    "pahom.agent.putin": ":older_man:",
    "pahom.agent.ussr": ":bear:",
    "pahom.agent.vacancy": ":briefcase:",
    "pahom.agent.whoami": ":poop:",
    "pahom.agent.work": ":office:",
    "pahom.agent.xj9": ":princess:"
}

# Генерация бредней пахома при старте скрипта
text_search.generatePizdec(30000)


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

    request = apiai.ApiAI(settings.dialogFlow_API_token).text_request() # Токен API к Dialogflow
    request.version = 2 # версия API
    request.lang = 'ru' # На каком языке будет послан запрос
    request.session_id = 'dp10_bot' # ID Сессии диалога (нужно, чтобы потом учить бота)
    request.query = user_message # Посылаем запрос к ИИ с сообщением от юзера
    responseJson = json.loads(request.getresponse().read().decode('utf-8'))

    # Отладка вывода json ответа
    # print(json.dumps(responseJson, indent=4, sort_keys=True))

    response_name = responseJson['result']['metadata']['intentName'] # имя категории для определения тематики вопроса

    # Разбираем JSON и вытаскиваем ответ. Заменяем анонимы на имя юзера
    response = responseJson['result']['fulfillment']['speech']
    response = response.replace("ANONIM", name_user, 10)

    # print(intent_emoji[response_name])
    response = emoji.emojize(str(intent_emoji[response_name] + " "), use_aliases=True) + response

    # Если есть ответ от DialogFlow, то проверяем на тип ответа.
    # Если на вопрос нет ответа (pahom.error), то отдаём марковке
    if response:
        if response_name == "pahom.error":
            mark_sentence = emoji.emojize(str(intent_emoji[response_name] + " "), use_aliases=True) + text_search.neurosPahomus(user_message)
            bot.send_message(chat_id=update.message.chat_id, text=mark_sentence)  # марковка
        else:
            bot.send_message(chat_id=update.message.chat_id, text=response)
    else:
        bot.send_message(chat_id=update.message.chat_id, text='DialogFlow response error')
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

