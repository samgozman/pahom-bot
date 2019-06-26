from pahom import settings
from pahom import text_search
from pahom import jsonloads
import apiai
import json
import emoji


def connect():
    request = apiai.ApiAI(settings.dialogFlow_API_token).text_request() # Токен API к Dialogflow
    request.version = 2 # версия API
    request.lang = 'ru' # На каком языке будет послан запрос
    request.session_id = 'dp10_bot' # ID Сессии диалога (нужно, чтобы потом учить бота)
    return request


def response(user_message: str):
    # Посылаем запрос к DialogFlow с сообщением от юзера
    request = connect()
    request.query = user_message
    responseJson = json.loads(request.getresponse().read().decode('utf-8'))

    # Получить ответ
    answer = responseJson['result']['fulfillment']['speech']
    # Получить тематику вопроса
    theme = responseJson['result']['metadata']['intentName']
    return answer, theme


def emojify(response_name: str):
    # Выдача emoji на основе категории ответа
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
    return str(emoji.emojize(str(intent_emoji[response_name] + " "), use_aliases=True))


def text_answer(user_message, name_user, no_dialogflow=True):

    # Если no_dialogflow True, тогда пытаемся найти ответ в json или генерим марковку, без обращения в DialogFlow
    if no_dialogflow:
        prepared_message = text_search.prepare_message(user_message)
        prepared_answer, response_name = jsonloads.text_answer(prepared_message)
        if prepared_answer is not None:
            # Добавляем к найденному ответу кусочек бредятины
            prepared_answer += ("\n" + text_search.neuros_pahomus(user_message))
            return str(emojify(str(response_name)) + prepared_answer.replace("ANONIM", name_user, 5))
        else:
            return str(emojify("pahom.error") + text_search.neuros_pahomus(user_message).replace("ANONIM", name_user, 5))
    else:
        response_message, response_name = response(user_message)
        # Проверка на пустой ответ
        if not response_message:
            return "DialogFlow response error"
        # Заменяем анонимы на имя юзера, добавляем смайлы
        smile = emojify(response_name)
        if response_name == "pahom.error":
            return str(smile + text_search.neuros_pahomus(user_message).replace("ANONIM", name_user, 5))
        else:
            return str(smile + response_message.replace("ANONIM", name_user, 5))