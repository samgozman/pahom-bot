# -*- coding: utf-8 -*-
from pahom import jsonloads
from pahom import text_search


def text_answer(user_message, name_user):
    prepared_message = text_search.prepare_message(user_message)
    prepared_answer, response_name = jsonloads.text_answer(prepared_message)
    if prepared_answer is not None:
        # Добавляем к найденному ответу кусочек бредятины
        prepared_answer += ("\n" + text_search.neuros_pahomus(user_message))
        return prepared_answer.replace("ANONIM", name_user, 5)
    else:
        return text_search.neuros_pahomus(user_message).replace("ANONIM", name_user, 5)
