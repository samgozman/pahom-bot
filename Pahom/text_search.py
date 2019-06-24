import re
import markovify
from pahom import settings
import tqdm
from collections import OrderedDict
import time
import random

FILE_ARRAY = []


def generatePizdec(count):
    # Генерация бредней пахома

    # Открываем исходный текст
    with open(settings.shiza_file) as f:
        text = f.read()
        f.close()

    # Строим модель
    text_model = markovify.Text(text)

    # Записываем наши познания в виде предложений
    global FILE_ARRAY
    # tqdm - для вывода в консоль процесса генерации
    for i in tqdm.tqdm(range(count)):
        sentence = text_model.make_sentence()
        FILE_ARRAY.append(sentence)
    # Удаляем дубликаты строк. В словаре не может быть одинаковых ключей :)
    FILE_ARRAY = list(OrderedDict.fromkeys(FILE_ARRAY))
    print(str(len(FILE_ARRAY)) + " generated")
    text_file = open(settings.markov_file, "w")
    text_file.write('\n'.join(map(str, FILE_ARRAY)))
    text_file.close()


def replaceExtraWords(message: str):
    # Удалить лишние слова для более быстрого поиска
    words_to_replace = (
        "в", "без", "до", "из", "к", "на", "по", "о", "от", "перед", "при", "через", "с", "у", "за", "над", "об", "под",
        "про", "для", "вблизи", "вглубь", "вдоль", "возле", "около", "вокруг", "впереди", "после", "а", "вдобавок",
        "именно", "также", "то", "тому", "что", "благо", "буде", "будто", "результате", "чего", "того", "связи", "тем",
        "силу", "случае", "если", "время", "как", "том", "ввиду", "вопреки", "вроде", "вследствие", "да", "еще", "и", "но",
        "дабы", "даже", "даром", "чтобы", "же", "едва", "лишь", "ежели", "бы", "не", "затем", "зато", "зачем", "все",
        "значит", "поэтому", "притом", "всетаки", "следовательно", "тогда", "ибо", "изза", "или", "кабы", "скоро", "словно",
        "только", "так", "както", "когда", "коли", "кроме", "ли", "либо", "между", "нежели", "столько", "сколько",
        "только.", "невзирая", "независимо", "несмотря", "ни", "однако", "особенно", "оттого", "отчего", "мере", "причине",
        "подобно", "пока", "покамест", "покуда", "поскольку", "потому", "почему", "прежде", "чем", "всем", "условии",
        "причем", "пускай", "пусть", "ради", "раз", "раньше", "тех", "пор", "более", "есть", "тоже", "чуть", "точно",
        "хотя", "чтоб", "ох", "ой", "пли", "ух", "фу", "фи", "ага", "ах", "тото", "эка", "шш", "вотвот", "др", "ты", "вы",
        "он", "эх", "ай", "эй", "эти", "эк", "его","я", "ты", "он", "она", "оно", "мы", "вы", "они", "себя", "мой", "твой",
        "свой", "ваш", "наш", "его", "её", "их", "кто", "что", "какой", "чей", "где", "который", "откуда", "сколько", "каковой",
        "каков", "зачем", "кто", "что", "какой", "который", "чей", "сколько", "каковой", "каков", "зачем", "когда", "тот", "этот",
        "столько", "такой", "таков", "сей", "всякий", "каждый", "сам", "самый", "любой", "иной", "другой", "весь", " никто",
        "ничто", "никакой", "ничей", "некого", "нечего", "незачем", "некто", "весь", "нечто", "некоторый", "несколько", "кто", "то",
        "что", "нибудь", "какой", "либо")
    # удаляем лишние союзы итд
    user_message_parsed = message.lower()
    for x in words_to_replace:
        regexp = re.compile(r'\b' + x + r'\b')
        user_message_parsed = re.sub(regexp, '', user_message_parsed)
    return user_message_parsed


def replaceSigns(message: str):
    # удалить лишние символы
    message = re.sub(r'[^a-zA-Zа-яА-Я0-9\- ]', '', message)
    # удалить лишние пробелы
    message = re.sub(r'\s+', ' ', message)
    return message

def txtToList(file_name):
    # перелапачиваем файл в массив строк
    file = open(file_name, "r")
    array = []
    for num, line in enumerate(file, 0):
        array.append(line)
    file_name.close()
    return array

def findAnswers(message_array: list):
    # находим вхождения слов из сообщения в марковку
    answers_dict = dict()
    answers_list = list()
    # Сортируем массив по убыванию, чтобы в выборку попали самые длинные слова
    message_array.sort(key=len, reverse=True)

    # Использовать в случае подгрузки модели из внешнего файла
    # global FILE_ARRAY
    # FILE_ARRAY = txtToList(settings.markov_file)

    for message in message_array:
        # Проверяем не более 5 вхождений, чтобы не перегружать сервер
        if message_array.index(message) >= 5:
            break
        # Открываем исходный текст и ищем в нем слово
        # Причем слово, которое входит внутрь слова тип ANO -> ANONIM
        arr = list()
        for line in FILE_ARRAY:
            if re.search(message, str(line).lower()):
                # print(line)
                arr.append(line)
        # Сохраняем в массив все ответы и в словарь с доступом по ключу для более быстрого доступа по ключу
        answers_list += arr
        answers_dict[message] = arr

    return answers_dict, answers_list


def prepareMessage(message: str):
    message = replaceSigns(replaceExtraWords(message))
    return message.split()


def findPairDuplicates(data: list):
    # Поиск пар дубликатов (для дальнейшего выбора наиболее релевантного ответа)
    data.sort()
    # print(data)
    pairs_data = list()
    for i in range(len(data) - 1):
        if data[i] == data[i + 1]:
            pairs_data.append(data[i])
    return pairs_data

# Тут пахом слегка поумнел, но не сильно))
def findDependencies(answers_dict: dict, answers_list: list):
    save_list = []
    global FILE_ARRAY

    # Если пришел пустой ответ
    if not answers_list:
        return random.choice(FILE_ARRAY)

    # Поиск первой пары
    my_list = findPairDuplicates(answers_list)

    # Если пар не нашлось, то выдать рандомный ответ из списка потенциальных ответов
    if not my_list:
        return random.choice(answers_list)

    # Если после первой выборки пришел пустой массив, то вернуть рандом
    while answers_list:
        save_list = my_list
        my_list = findPairDuplicates(my_list)
        if not my_list:
            break
    # Если на несколько слов найдено равное кол-во повторок, то вывести все
    if len(save_list) > 1:
        iterate_list = save_list
        save_list = ""
        for x in range(len(iterate_list)):
            save_list += str(iterate_list[x])
            # if x < len(iterate_list)-1:
            #     save_list += "\n"
    return ''.join(save_list)

def neurosPahomus(text_ms: str):
    # запускает всю цепочку пахома
    test_dict = findAnswers(prepareMessage(text_ms))
    answer = str(findDependencies(test_dict[0], test_dict[1]))
    return answer
#
# start_time = time.time()
# print(neurosPahomus("получению пособия"))
# print("--- %s seconds ---" % (time.time() - start_time))

# print(findDependencies(dict(), [10,20,20,30,30,40,40]))
# print(neurosPahomus("получении грядки"))

# generatePizdec(30000)
# print('done')