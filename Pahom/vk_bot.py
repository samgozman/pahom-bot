import vk_api
import time
import re
import random
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from pahom import dialogflow

# vk_session = vk_api.VkApi(token=settings.vk_public_token_1)
# vk = vk_session.get_api()

# longpoll = VkLongPoll (vk_session)
# for event in longpoll.listen():
#    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
#        print('id{}: "{}"'.format(event.user_id, event.text), end='\n')

#        response_from_bot = event.text

#        vk.messages.send(
#            user_id=event.user_id,
#            random_id=get_random_id(),
#            message=response_from_bot
#        )


class Bot:
    """
        Класс создания ВК бота. В него необходимо передать логин (телефонный номер), пароль и id приложения
    """
    def __init__(self, login, password, app_id, tg_token):
        """Constructor"""
        self.login = login
        self.password = password
        self.app_id = app_id
        self.tg_token = tg_token
        self.tg_chat_id = None
        self.captcha_key = None
        self.VK = self.connect()

    def tg_connect(self):
        updater = Updater(token=self.tg_token)
        dispatcher = updater.dispatcher
        return dispatcher, updater

    def tg_send_message(self, dispatcher, text):
        dispatcher.bot.send_message(chat_id=self.tg_chat_id, text=text)

    def captcha_handler(self, captcha):
        """ При возникновении капчи вызывается эта функция и ей передается объект
            капчи. Через метод get_url можно получить ссылку на изображение.
            Через метод try_again можно попытаться отправить запрос с кодом капчи
        """
        tg_dispatcher, updater = self.tg_connect()
        tg_text = "Enter captcha code {0}: ".format(captcha.get_url())
        self.tg_send_message(tg_dispatcher, tg_text)
        # Ждём ответа юзера
        key = None
        self.captcha_key = None
        while self.captcha_key is None:
            if self.captcha_key is not None:
                key = self.captcha_key
        self.captcha_key = None
        key = input("Enter captcha code {0}: ".format(captcha.get_url())).strip()
        print()

        # Пробуем снова отправить запрос с капчей
        return captcha.try_again(key)

    def connect(self, reauth=False):
        # Коннектиться в глобалке, если в try ошибка, то вызвать connect.
        # Аутентификация
        vk_session = vk_api.VkApi(self.login, self.password, app_id=self.app_id, scope=9220, captcha_handler=self.captcha_handler)
        vk = vk_session.get_api()
        vk_session.auth(reauth=reauth)
        return vk

    # Удалить отложенные записи на стене
    def wall_delete_postponed(self, post_ids):
        for post in post_ids:
            self.VK.wall.delete(post_id=post)
            if len(post_ids) > 1:
                time.sleep(0.333)

    # Получить отложенные записи на стене
    def get_wall_postponed(self):
        posts = self.VK.wall.get(filter='postponed', count=100)['items']
        post_ids = []
        for post in posts:
            post_ids.append(post['id'])
        return self.wall_delete_postponed(post_ids)

    # Сгенерировать отложенные записи на стене по 2шт в день
    def generate_wall(self, count=1):
        self.get_wall_postponed()
        current_time = time.time()
        for i in range(count):
            post_time = current_time + random.randint(0, 43200)
            current_time += 43200
            text = dialogflow.text_answer("", "Анон", True)
            self.VK.wall.post(publish_date=post_time, message=text)
            if count > 1:
                time.sleep(0.333)

    def reconnect(self):
        self.VK = self.connect(True)

    def create_comment(self, text, group_id, post_id, from_id=0):
        # text - текст поста
        if from_id > 0:
            user = self.VK.users.get(user_id=from_id)
            user_name = '[id{}|{}]'.format(str(from_id), user[0]['first_name'])
            comment = dialogflow.text_answer(text, user_name, True)
            # Если так случилось, что пахом ни к кому не обращается, то насильственно добавим обращение в начало
            if "[id" not in comment:
                comment = '[id{}|{}], {}'.format(str(from_id), user[0]['first_name'], comment)
            return self.VK.wall.createComment(owner_id=group_id, post_id=post_id, message=comment)
        else:
            comment = dialogflow.text_answer(text, "Анон", True)
            return self.VK.wall.createComment(owner_id=group_id, post_id=post_id, message=comment)

    def create_photos_comment(self, text, user_id, photo_id, user_name="Аноним"):
        comment = dialogflow.text_answer(text, user_name, True)
        self.VK.photos.createComment(owner_id=user_id, photo_id=photo_id, message=comment)

    def create_post(self, wall_id):
        post = dialogflow.text_answer("", 'Уважаемый аноним', True)
        try:
            return self.VK.wall.post(owner_id=wall_id,message=post)
        except Exception as e:
            print("VK Error (create_post): " + str(e) + " | With wall id: " + str(wall_id))

    def get_id(self, link):
        # получаем из ссылки на пользователя или группу его id
        # Убираем из ссылки все что адрес и всё что после занка "?"
        link_parsed = re.sub(r"(^[^.com]*.com\/)", "", link)
        link_parsed = re.sub(r"\?.*", "", link_parsed)

        try:
            group = self.VK.groups.getById(group_ids=link_parsed, fields='can_post')
            if group[0]['can_post'] ==1:
                if group[0]['id']:
                    return -1 * group[0]['id']
            else:
                print('Нельзя публиковать')
        except Exception as e:
            print("VK Error (get_id): " + str(e) + " | With link: " + link)

        try:
            user = self.VK.users.get(user_ids=link_parsed, fields='can_post')
            if user[0]['can_post'] == 1:
                if user[0]['id']:
                    return user[0]['id']
            else:
                print('Нельзя публиковать')
        except Exception as e:
            print("VK Error (get_id): " + str(e) + " | With link: " + link)

    def action_reply_to_post(self, link, count=1):
        # post - ссылка на пост, count - количество ответов
        # Из ссылки отбрасываем всё, что не ID поста и группы. Получаем содержимое поста.
        ids = re.sub(r'.+?(?=wall)wall', '', link)
        post = self.VK.wall.getById(posts=ids)
        ids = ids.split("_")
        for i in range(count):
            self.create_comment(post[0]['text'], int(ids[0]), int(ids[1]), post[0]['from_id'])
            if count > 1:
                time.sleep(10)

    def action_create_post(self, link: str, count=1):
        # Создаем пост в любом месте. Если стена закрыта, то в предложку (группа)
        # Из ссылки отбрасываем всё, что не ID поста и группы. Получаем содержимое поста.
        wall_id = self.get_id(link)
        for i in range(count):
            self.create_post(wall_id)
            if count > 1:
                time.sleep(10)

    def action_reply_to_comment(self, link):
        # Из ссылки отбрасываем всё, что не ID поста, группы и реплая
        link_without_http = re.sub(r'.+?(?=wall)wall', '', link)
        link_without_thread = re.sub(r"&.*","",link_without_http)
        # сохраняем реплай отдельно
        link_reply = re.sub(r'.*(?=reply)reply=', '', link_without_thread)
        # Удаляем реплай
        link_parsed_ids = re.sub(r"\?.*", "", link_without_thread).split('_')
        try:
            comment = self.VK.wall.getComment(owner_id=link_parsed_ids[0], comment_id=link_reply, extended=1)
        except Exception as e:
            print("VK Error (action_reply_to_comment): " + str(e) + " | With link: " + link)
        # Парсим коммент
        comment_text = comment['items'][0]['text']
        user_name = comment['profiles'][0]['first_name']
        user_id = comment['profiles'][0]['id']

        # Reply со сгенерированной марковкой на основе текста
        message = '[id{}|{}], {}'.format(str(user_id), user_name, dialogflow.text_answer(comment_text, user_name))
        try:
            self.VK.wall.createComment(owner_id=link_parsed_ids[0], post_id=link_parsed_ids[1], reply_to_comment=link_reply, message=message)
        except Exception as e:
            print("VK Error (action_reply_to_comment): " + str(e) + " | With link: " + link)

    def action_reply_to_photo(self, link, count=1):
        # Из ссылки отбрасываем всё, что не ID поста, группы и реплая
        link_without_http = re.sub(r'.+?(?=z)z=photo', '', link)
        link_without_trash = re.sub(r"%.*","",link_without_http)
        photo = self.VK.photos.getById(photos=link_without_trash)
        user_id = photo[0]['owner_id']
        photo_text = photo[0]['text']
        photo_id = photo[0]['id']
        if user_id > 0:
            user_name = self.VK.users.get(user_id=user_id)[0]['first_name']
        else:
            user_id = int(user_id) * -1
            user_name = self.VK.groups.getById(group_id=user_id)[0]['name']
        for i in range(count):
            self.create_photos_comment(photo_text, user_id, photo_id, user_name)
            if count > 1:
                time.sleep(10)

    def action_change_status(self, count=1):
        try:
            for i in range(count):
                self.VK.status.set(text=dialogflow.text_answer("", "Анон"))
                if count > 1:
                    time.sleep(10)
        except Exception as e:
            print("VK Error (action_change_status): " + str(e))
