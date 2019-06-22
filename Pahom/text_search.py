import re
import time


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
        "он", "эх", "ай", "эй", "эти", "эк", "его")
    # удаляем лишние союзы итд
    user_message_parsed = message.lower()
    for x in words_to_replace:
        regexp = re.compile(r'\b' + x + r'\b')
        user_message_parsed = re.sub(regexp, '', user_message_parsed)
    return user_message_parsed


def replaceSigns(message: str):
    # удалить лишние символы
    message = re.sub(r'[^a-zA-Zа-яА-Я ]', '', message)
    # удалить лишние пробелы
    message = re.sub(r'\s+', ' ', message)
    return message


def findAnswers(message_array: list):
    # находим вхождения слов из сообщения в марковку
    answers_dict = dict()

    # Сортируем массив по убыванию, чтобы в выборку попали самые длинные слова
    message_array.sort(key=len, reverse=True)

    # перелапачиваем файл в массив строк
    file_name = open("data/markov.txt", "r")
    file_array = []
    for num, line in enumerate(file_name, 0):
        file_array.append(line)

    for message in message_array:
        # Проверяем не более 5 вхождений, чтобы не перегружать сервер
        if message_array.index(message) >= 5:
            break
        # Открываем исходный текст и ищем в нем слово
        # Причем слово, которое входит внутрь слова тип ANO -> ANONIM
        arr = list()
        for line in file_array:
            if re.search(message, str(line).lower()):
                # print(line)
                arr.append(line)
        answers_dict[message] = arr

    file_name.close()
    return answers_dict


def prepareMessage(message: str):
    message = replaceSigns(replaceExtraWords(message))
    return message.split()


# start_time = time.time()
# text_ms = "Kek,   lole! k на и в Нет kek гы гыебать ПИДОР,,,,,"
# print(text_ms)
# print("превращается в:")
# print(prepareMessage(text_ms))
# print(findAnswers(prepareMessage(text_ms)))
# print("--- %s seconds ---" % (time.time() - start_time))
