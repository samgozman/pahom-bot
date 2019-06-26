import json
import os
import random

from pahom import settings

# Путь до папки с json файлами
PATH = str(settings.THIS_FOLDER) + "/data/json/dialog-flow/intents"
# Спарсеный JSON прячется тут
JSON = dict()

def listOfFiles():
    files = list()
    for file in os.listdir(PATH):
        if file.endswith(".json"):
            files.append(file)
    return files


def openJson():
    # Переносит все json файлы в структуру вида:
    # answers -> intent_name -> items
    # questions -> intent_name -> items
    files = listOfFiles()
    answers_dict = dict()
    questions_dict = dict()
    global JSON
    for file in files:
        items = []
        file_path = PATH + '/' + file
        file_json = open(file_path)
        data = json.load(file_json)
        if "usersays" not in file:
            questions_dict[file.replace('.json', '')] = data['responses'][0]['messages'][0]['speech']
        else:
            for item in data:
                items.append(item['data'][0]['text'])
            answers_dict[file.split('_')[0]] = items
        file_json.close()
    JSON['answers'] = answers_dict
    JSON['questions'] = questions_dict


def findMatchIntent(message=[]):
    message.sort()
    matches_dict = dict()
    # Ищем вхождения слов сообщения в вопросы
    global JSON
    answers = JSON['answers']
    for intent in answers:
        matches = []
        for word in message:
            for answer in answers[intent]:
                if word in ''.join(answer).lower():
                    matches.append(answer)
        matches_dict[intent] = matches
    # Сортируем словарь по количеству элементов ключа и выводим название ключа (первого самого большого)
    key = sorted(matches_dict, key=lambda k: len(matches_dict[k]), reverse=True)[0]
    # Если пустой результат
    if len(matches_dict[key]) < 1:
        key = None
    return key


def getAnswer(message=[]):
    response_name = findMatchIntent(message)
    if response_name is not None:
        global JSON
        return random.choice(JSON['questions'][response_name]), response_name
    else:
        return None, None

# openJson()
# print(findMatchIntent(['пока', 'здоров']))
# print(getAnswer(['пока', 'здоров']))
