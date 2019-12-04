# -*- coding: utf-8 -*-
from pahom import jsonloads
from pahom import nonsense
import logging

# Вывод лога ошибок
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def text_answer(user_message, name_user):
    logger.info("Get TEXT: %s FROM %s" % (user_message, name_user))
    prepared_message = nonsense.prepare_message(user_message)
    prepared_answer, response_name = jsonloads.text_answer(prepared_message)
    if prepared_answer is not None:
        # # 1 Добавляем к найденному ответу кусочек бредятины
        # prepared_answer += ("\n" + nonsense.neuros_pahomus(user_message))
        # return prepared_answer.replace("ANONIM", name_user, 5)

        # 2   Используем найденный ответ как вопрос к марковке
        answer = prepared_answer + "\n" + nonsense.neuros_pahomus(prepared_answer)
        return answer.replace("ANONIM", name_user, 5)
    else:
        return nonsense.neuros_pahomus(user_message).replace("ANONIM", name_user, 5)
