from pahom import settings
from pahom import text_search
import apiai
import json
import emoji

def setConnect():
    request = apiai.ApiAI(settings.dialogFlow_API_token).text_request() # Токен API к Dialogflow
    request.version = 2 # версия API
    request.lang = 'ru' # На каком языке будет послан запрос
    request.session_id = 'dp10_bot' # ID Сессии диалога (нужно, чтобы потом учить бота)
    return request


def getResponse(user_message: str):
    # Посылаем запрос к DialogFlow с сообщением от юзера
    request = setConnect()
    request.query = user_message
    responseJson = json.loads(request.getresponse().read().decode('utf-8'))

    # Получить ответ
    answer = responseJson['result']['fulfillment']['speech']
    # Получить тематику вопроса
    theme = responseJson['result']['metadata']['intentName']
    return answer, theme


def getEmoji(response_name: str):
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


def getTextAnswer(user_message, name_user, markov_only=False):

    # Если markov_only true, тогда генерировать ТОЛЬКО марковку, без обращения в DialogFlow
    if markov_only:
        return str(getEmoji("pahom.error") + text_search.neurosPahomus(user_message).replace("ANONIM", name_user, 5))
    else:
        response, response_name = getResponse(user_message)
        # Проверка на пустой ответ
        if not response:
            return "DialogFlow response error"
        # Заменяем анонимы на имя юзера, добавляем смайлы
        smile = getEmoji(response_name)
        if response_name == "pahom.error":
            return str(smile + text_search.neurosPahomus(user_message).replace("ANONIM", name_user, 5))
        else:
            return str(smile + response.replace("ANONIM", name_user, 5))