# -*- coding: utf-8 -*-
import logging
import os
from multiprocessing import Process

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from pahom import dialogflow
from pahom import settings
from pahom import vk_bot

# Вывод лога ошибок
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def check_admin_privileges(bot, update):
    name_user = update.message.from_user.username
    # Проверяем есть ли юзер в админском составе. Если да, то выдать меню. Нет - выдать марковку))
    if name_user in settings.admin:
        return True
    else:
        return False


def tg_connect(reauth=False):
    # ТК телеграмм является контрольной панелью для управления ВК ботом, то и создадим его здесь
    # Удаляем файл со старыми настройками
    vk_settings_file = str(os.path.dirname(settings.THIS_FOLDER)) + "/vk_config.v2.json"
    if os.path.isfile(vk_settings_file):
        os.remove(vk_settings_file)
    return vk_bot.Bot(settings.vk_login, settings.vk_pass, settings.vk_app_id, reauth)


vkbot = tg_connect()


def admin_commands(user_message: str, chat_id, bot, update):
    global vkbot
    # Выполняем админские комманды из ТГ над ВК ботом
    if "%%" in user_message:
        ms = user_message.split(" ")
        try:
            if "change status" in user_message or "изменить статус" in user_message:
                # Проверка на наличие аргумента. Если нету, то дефолт
                if len(ms) < 4 or ms[3] == "":
                    ms.append(1)
                vkbot.action_change_status(int(ms[3]))
            elif "reply to comment" in user_message or "ответить на коммент" in user_message:
                vkbot.action_reply_to_comment(ms[4])
            elif "create post" in user_message or "создать пост" in user_message:
                if len(ms) < 5 or ms[4] == "":
                    ms.append(1)
                vkbot.action_create_post(ms[3], int(ms[4]))
            elif "reply to post" in user_message or "ответить на пост" in user_message:
                if len(ms) < 6 or ms[5] == "":
                    ms.append(1)
                vkbot.action_reply_to_post(ms[4], int(ms[5]))
            elif "reply to photo" in user_message or "ответить на фото" in user_message:
                if len(ms) < 6 or ms[5] == "":
                    ms.append(1)
                vkbot.action_reply_to_photo(ms[4], int(ms[5]))
            elif "generate wall" in user_message or "сгенерировать стену" in user_message:
                if len(ms) < 4 or ms[3] == "":
                    ms.append(1)
                vkbot.generate_wall(int(ms[3]))
                bot.send_message(chat_id=chat_id, text="Закончил задачу")
            elif "reconnect" in user_message or "подключение" in user_message:
                vkbot = tg_connect(True)
        except Exception as e:
            print("VK Error in TG (admin_commands): " + str(e) + " | Trying to reconnect ")
            vkbot = tg_connect(True)
            bot.send_message(chat_id=chat_id, text="Всвязи с ошибкой выполнил реконнект. Попробуй снова!")
        # Баг - пытается отправить, когда задача уже завершена
        # bot.send_message(chat_id=update.message.chat_id, text="Закончил задачу")


def work(tg_token):
    # Подключаемся к ТГ
    updater = Updater(token=tg_token)

    # Токен API к Telegram
    dispatcher = updater.dispatcher

    # Обработка команд

    def start_command(bot, update):
        # Функция вызова стартовой команды
        name_user = update.message.from_user.first_name
        pahom_start = ("Здравствуй, " + name_user + "! "
                                                    "Я слабоумная, патриотическая, радиоактивная нейронная сеть Пахом ДП-10.  Со мной можно пообщаться на разные темы - от Путина до My little Pony. "
                                                    "Но предупреждаю: я первая в мире нейронная сеть страдающая аутизмом и шизофренией "
                                                    "(унаследовал от источника исследования - Дмитрия Пахомова aka 'Кровавого тирана' aka 'ДП-10' aka etc)"
                       )
        bot.send_message(chat_id=update.message.chat_id, text=pahom_start)

    def text_message(bot, update):
        # Функция считывания сообщеня и отправки ответа
        name_user = update.message.from_user.first_name
        user_message = str(update.message.text)
        if check_admin_privileges(bot, update):
            # Выделяем отдельный процесс для ВК комманд
            t = Process(target=admin_commands, args=(user_message, update.message.chat_id, bot, update))
            t.start()
        bot.send_message(chat_id=update.message.chat_id, text=dialogflow.text_answer(user_message, name_user, True))

    def error(update, context):
        # Обработчик ошибок
        """Log Errors caused by Updates."""
        logger.warning('Update "%s" caused error "%s"', update, context.error)

    def help_command(bot, update):
        if check_admin_privileges(bot, update):
            pahom_help = """
Доступные админские команды:
%% изменить статус ЧИСЛО - изменяет статус аккаунта раз в 5 секунд ЧИСЛО раз. Если ЧИСЛО пустое, то изменяет 1 раз. (или change status)
%% ответить на пост ССЫЛКА ЧИСЛО - отвечает на пост по ССЫЛКА ЧИСЛО раз. Ссылка вида https://vk.com/wall-183833688_517. Если ЧИСЛО пустое, то отвечает 1 раз. (или reply to post)
%% создать пост ССЫЛКА ЧИСЛО - создаёт пост по ССЫЛКА (будь то паблик или человек) ЧИСЛО раз. Ссылка вида https://vk.com/wempire_dimstona. Если ЧИСЛО пустое, то создаёт 1 раз. (или create post)
%% ответить на коммент ССЫЛКА - отвечает на коммент по ССЫЛКА. Ссылка вида https://vk.com/wall-183833688_490?reply=492&thread=491 (или reply to comment)
%% ответить на фото ССЫЛКА - отвечает на коммент по ССЫЛКА. (или reply to photo)
%% подключение - выполнить переподключение к ВК (или reconnect)
%% сгенерировать стену ЧИСЛО - удаляет старые отложенные посты и генерит новые
            """
            bot.send_message(chat_id=update.message.chat_id, text=pahom_help)

    # Хендлеры
    updater.dispatcher.add_error_handler(error)

    start_command_handler = CommandHandler('start', start_command)
    help_command_handler = CommandHandler('help', help_command)
    text_message_handler = MessageHandler(Filters.text, text_message)
    # Добавляем хендлеры в диспетчер
    dispatcher.add_handler(start_command_handler)
    dispatcher.add_handler(help_command_handler)
    dispatcher.add_handler(text_message_handler)
    # Начинаем поиск обновлений
    updater.start_polling(clean=True)
    # Останавливаем бота, если были нажаты Ctrl + C
    updater.idle()
