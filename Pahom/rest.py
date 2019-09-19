# -*- coding: utf-8 -*-
from flask import Flask, json, request
from pahom import response


api = Flask(__name__)
api.config['JSON_AS_ASCII'] = False


@api.route('/')
def index():
    return "Привет, Пахом!"


@api.route('/question', methods=['POST'])
def post_question():
    if request.headers['Content-Type'] == 'application/json':
        message = json.loads(json.dumps(request.json))
        if 'author' in message and 'message' in message:
            return response.text_answer(message['message'], message['author']), 201
    else:
        return "Fuck you!", 415
