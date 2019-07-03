import vk_api
import time
import re
from pahom import dialogflow
from pahom import settings

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


# Коннектиться в глобалке, если в try ошибка, то вызвать connect.
def connect(login, password, app_id, reauth=False):
    # Аутентификация
    vk_session = vk_api.VkApi(login, password, app_id=app_id, scope=9216)
    vk = vk_session.get_api()
    vk_session.auth(reauth=reauth)
    return vk


VK = connect(settings.vk_login, settings.vk_pass, settings.vk_app_id)


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


def action_reply_to_post(link, count=1):
    # post - ссылка на пост, count - количество ответов
    # коннектимся
    global VK
    # Из ссылки отбрасываем всё, что не ID поста и группы. Получаем содержимое поста.
    ids = re.sub(r'.+?(?=wall)wall', '', link)
    post = VK.wall.getById(posts=ids)
    ids = ids.split("_")
    for i in range(count):
        create_comment(VK, post[0]['text'], int(ids[0]), int(ids[1]), post[0]['from_id'])
        if count > 1:
            time.sleep(10)


def action_create_post(link: str, count=1):
    # Создаем пост в любом месте. Если стена закрыта, то в предложку (группа)
    global VK
    # Из ссылки отбрасываем всё, что не ID поста и группы. Получаем содержимое поста.
    wall_id = get_id(VK, link)
    for i in range(count):
        create_post(VK, wall_id)
        if count > 1:
            time.sleep(10)


def action_reply_to_comment(link):
    # коннектимся
    global VK
    # Из ссылки отбрасываем всё, что не ID поста, группы и реплая
    link_without_http = re.sub(r'.+?(?=wall)wall', '', link)
    link_without_thread = re.sub(r"&.*","",link_without_http)
    # сохраняем реплай отдельно
    link_reply = re.sub(r'.*(?=reply)reply=', '', link_without_thread)
    # Удаляем реплай
    link_parsed_ids = re.sub(r"\?.*", "", link_without_thread).split('_')
    try:
        comment = VK.wall.getComment(owner_id=link_parsed_ids[0], comment_id=link_reply, extended=1)
    except Exception as e:
        print("VK Error (action_reply_to_comment): " + str(e) + " | With link: " + link)
    # Парсим коммент
    comment_text = comment['items'][0]['text']
    user_name = comment['profiles'][0]['first_name']
    user_id = comment['profiles'][0]['id']

    # Reply со сгенерированной марковкой на основе текста
    message = '[id{}|{}], {}'.format(str(user_id), user_name, dialogflow.text_answer(comment_text, user_name))
    try:
        VK.wall.createComment(owner_id=link_parsed_ids[0], post_id=link_parsed_ids[1], reply_to_comment=link_reply, message=message)
    except Exception as e:
        print("VK Error (action_reply_to_comment): " + str(e) + " | With link: " + link)


def action_change_status(count=1):
    global VK
    try:
        for i in range(count):
            VK.status.set(text=dialogflow.text_answer("", "Анон"))
            if count > 1:
                time.sleep(10)
    except Exception as e:
        print("VK Error (action_change_status): " + str(e))
