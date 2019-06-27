import vk_api
import random
import time
from pahom import dialogflow

DEEP_POSTS = 3
DEEP_COMMENTS = 2


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


def work(login, password, app_id, bot_id, public_id):

    # Аутентификация
    vk_session = vk_api.VkApi(login, password, app_id=app_id, scope=8192)
    vk = vk_session.get_api()
    vk_session.auth()
    
    def create_reply_comment(text, post_id, reply_comment, from_id=0):
        # text - текст юзера
        if from_id != bot_id:
            if from_id > 0:
                user = vk.users.get(user_id=from_id)
                user_name = '[id{}|{}]'.format(str(from_id), user[0]['first_name'])
                comment = dialogflow.text_answer(text, user_name, True)
                if "[id" not in comment:
                    comment = '[id{}|{}], {}'.format(str(from_id), user[0]['first_name'], comment)
                return vk.wall.createComment(owner_id=public_id, post_id=post_id,
                                             reply_to_comment=reply_comment,
                                             message=comment)

    def create_comment(text, post_id, from_id=0):
        # text - текст поста
        if from_id != bot_id:
            if from_id > 0:
                user = vk.users.get(user_id=from_id)
                user_name = '[id{}|{}]'.format(str(from_id), user[0]['first_name'])
                comment = dialogflow.text_answer(text, user_name, True)
                # Если так случилось, что пахом ни к кому не обращается, то насильственно добавим обращение в начало
                if "[id" not in comment:
                    comment = '[id{}|{}], {}'.format(str(from_id), user[0]['first_name'], comment)
                return vk.wall.createComment(owner_id=public_id, post_id=post_id, message=comment)
            else:
                comment = dialogflow.text_answer(text, "Анон", True)
                return vk.wall.createComment(owner_id=public_id, post_id=post_id, message=comment)

    # Вечный цикл
    while True:
        get_post_from_public = vk.wall.get(count=DEEP_POSTS, owner_id=public_id)
        if get_post_from_public['items']:
            for post in get_post_from_public['items']:
                if post['comments']['count'] == 0:
                    if random.random() > 0.5:
                        # post['text'] - текст записи для марковки
                        try:
                            create_comment(post['text'], post['id'])
                        except Exception as e:
                            print("Error " + str(e))
                            time.sleep(5)
                if post['comments']['count'] > 0:
                        get_comments_from_post = vk.wall.getComments(owner_id=public_id,
                                                                     post_id=post['id'], offset=0,
                                                                     count=DEEP_COMMENTS, extended=1,
                                                                     sort="desc")
                        if get_comments_from_post['items']:
                            for comment in get_comments_from_post['items']:
                                if random.random() > 0.5:
                                    # comment['text'] - текст комментария для марковки
                                    try:
                                        create_reply_comment(comment['text'], post['id'], comment['id'], comment['from_id'])
                                    except Exception as e:
                                        print("Error " + str(e))
                                        time.sleep(5)
                                if random.random() > 0.5:
                                    # comment['text'] - текст комментария для марковки
                                    try:
                                        create_comment(comment['text'], post['id'], comment['from_id'])
                                    except Exception as e:
                                        print("Error " + str(e))
                                        time.sleep(5)
        time.sleep(10)
