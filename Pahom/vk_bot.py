import vk_api
import random
import time
import re
from pahom import dialogflow
from pahom import settings

TOKEN = ""
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


def connect(login, password, app_id):
    # Аутентификация
    vk_session = vk_api.VkApi(login, password, app_id=app_id, scope=8192)
    vk = vk_session.get_api()
    vk_session.auth()
    return vk


def create_comment(vk, text, group_id, post_id, from_id=0):
    # text - текст поста
    if from_id > 0:
        user = vk.users.get(user_id=from_id)
        user_name = '[id{}|{}]'.format(str(from_id), user[0]['first_name'])
        comment = dialogflow.text_answer(text, user_name, True)
        # Если так случилось, что пахом ни к кому не обращается, то насильственно добавим обращение в начало
        if "[id" not in comment:
            comment = '[id{}|{}], {}'.format(str(from_id), user[0]['first_name'], comment)
        return vk.wall.createComment(owner_id=group_id, post_id=post_id, message=comment)
    else:
        comment = dialogflow.text_answer(text, "Анон", True)
        return vk.wall.createComment(owner_id=group_id, post_id=post_id, message=comment)


def create_post(vk, wall_id):
    post = dialogflow.text_answer("", 'Уважаемый аноним', True)
    try:
        return vk.wall.post(owner_id=wall_id,message=post)
    except Exception as e:
        print("VK Error (create_post): " + str(e) + " | With wall id: " + str(wall_id))


def get_id(vk, link):
    # получаем из ссылки на пользователя или группу его id
    # Убираем из ссылки все что адрес и всё что после занка "?"
    link_parsed = re.sub(r"(^[^.com]*.com\/)", "", link)
    link_parsed = re.sub(r"\?.*", "", link_parsed)

    try:
        group = vk.groups.getById(group_ids=link_parsed)
        if group[0]['id']:
            return -1 * group[0]['id']
    except Exception as e:
        print("VK Error (get_id): " + str(e) + " | With link: " + link)

    try:
        user = vk.users.get(user_ids=link_parsed)
        if user[0]['id']:
            return user[0]['id']
    except Exception as e:
        print("VK Error (get_id): " + str(e) + " | With link: " + link)


def action_dump_post(link, count=1):
    # post - ссылка на пост, count - количество ответов
    # коннектимся
    vk = connect(settings.vk_login,settings.vk_pass,settings.vk_app_id)
    # Из ссылки отбрасываем всё, что не ID поста и группы. Получаем содержимое поста.
    ids = re.sub('.+?(?=wall)wall', '', link)
    post = vk.wall.getById(posts=ids)
    ids = ids.split("_")
    for i in range(count):
        create_comment(vk, post[0]['text'], int(ids[0]), int(ids[1]), post[0]['from_id'])
        if count > 1:
            time.sleep(10)


def action_create_post(link: str, count=1):
    # Создаем пост в любом месте. Если стена закрыта, то в предложку (группа)
    vk = connect(settings.vk_login, settings.vk_pass, settings.vk_app_id)
    # Из ссылки отбрасываем всё, что не ID поста и группы. Получаем содержимое поста.
    wall_id = get_id(vk, link)
    for i in range(count):
        create_post(vk, wall_id)
        if count > 1:
            time.sleep(10)
