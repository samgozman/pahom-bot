import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
import random
import time

PUBLIC_ID = -183833688
APP_ID = 7033657
BOT_ID = 521893394
DEEP_POSTS= 10
DEEP_COMMENTS= 2
LOGIN = 'login'
PASS = 'pass'

#
#vk_session = vk_api.VkApi(token='1ca9b0c2107cea97574ffb5e15eb9da073df3713500a1a741145a53923d4fa4110c3ef24e607c942e0cdf')
#vk = vk_session.get_api()

#longpoll = VkLongPoll (vk_session)
#for event in longpoll.listen():
#    if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
#        print('id{}: "{}"'.format(event.user_id, event.text), end='\n')

#        response_from_bot = event.text

#        vk.messages.send(
#            user_id=event.user_id,
#            random_id=get_random_id(),
#            message=response_from_bot
#        )

vk_session = vk_api.VkApi (LOGIN, PASS, app_id=APP_ID, scope=8192)
vk = vk_session.get_api()

vk_session.auth()

def createReplyComment (text, postID, replyComment, fromID =0):
    if fromID != BOT_ID:
        if fromID >0:
            user = vk.users.get (user_id = fromID)
            return (vk.wall.createComment(owner_id=PUBLIC_ID, post_id=postID, reply_to_comment=replyComment, message='[id{}|{}], {}'.format(str(fromID), user[0]['first_name'], text)))

def createComment (text, postID, fromID =0):
    if fromID != BOT_ID:
        if fromID >0:
            user = vk.users.get (user_id = fromID)
            return (vk.wall.createComment(owner_id=PUBLIC_ID, post_id=postID, message='[id{}|{}], {}'.format(str(fromID), user[0]['first_name'], text)))
        else:
            return (vk.wall.createComment(owner_id=PUBLIC_ID, post_id=postID, message= text))
while True:
    getPostFromPublic = vk.wall.get(count=DEEP_POSTS, owner_id=PUBLIC_ID)
    if getPostFromPublic['items']:
        for post in getPostFromPublic['items']:
            if post['comments']['count'] == 0:
                if random.random() > 0.5:
                    #post['text'] - текст записи для марковки
                    print ('57')
                    try:
                        createComment ('ТЕКСТ' + str (random.random()), post['id'])
                    except Exception:
                        time.sleep(5)
            if post['comments']['count'] > 0:
                    getCommentsFromPost = vk.wall.getComments (owner_id = PUBLIC_ID, post_id=post['id'], offset=0, count=DEEP_COMMENTS, extended=1, sort="desc")
                    if getCommentsFromPost['items']:
                        for comment in getCommentsFromPost['items']:
                            if random.random() > 0.5:
                                print('64')
                                #comment['text'] - текст комментария для марковки
                                try:
                                    createReplyComment('ТЕКСТ' + str (random.random()), post['id'], comment['id'],comment['from_id'])
                                except Exception:
                                    time.sleep(5)
                            if random.random() > 0.5:
                                #comment['text'] - текст комментария для марковки
                                print('69')
                                try:
                                    createComment ('ТЕКСТ' + str (random.random()), post['id'], comment['from_id'])
                                except Exception:
                                    time.sleep (5)
    time.sleep(10)