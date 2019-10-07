# -*- coding: utf-8 -*-
from flask import Flask, json, request, make_response, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_cors import CORS, cross_origin

from pahom import response


api = Flask(__name__)
api.config['JSON_AS_ASCII'] = False
CORS(api)
api.config['CORS_HEADERS'] = 'Content-Type'

limiter = Limiter(
    api,
    key_func=get_remote_address,
    default_limits=["2000 per day", "600 per hour"]
)


@api.route('/')
@limiter.limit("15/minute")
def index():
    resp = make_response("Привет, Пахом!")
    # Secure headers
    resp.headers['Content-Security-Policy'] = "default-src 'self'"
    resp.headers['X-Content-Type-Options'] = 'nosniff'
    resp.headers['X-Frame-Options'] = 'SAMEORIGIN'
    resp.headers['X-XSS-Protection'] = '1; mode=block'
    return resp


@api.route('/question', methods=['POST', 'OPTIONS'])
@cross_origin()
@limiter.limit("20/minute")
def post_question():
    if request.headers['Content-Type'] == 'application/json':
        message = json.loads(json.dumps(request.json))
        if 'author' in message and 'message' in message:
            resp = make_response(jsonify(reply=response.text_answer(message['message'], message['author'])))
            # Secure headers
            resp.headers['Content-Security-Policy'] = "default-src 'self'"
            resp.headers['X-Content-Type-Options'] = 'nosniff'
            resp.headers['X-Frame-Options'] = 'SAMEORIGIN'
            resp.headers['X-XSS-Protection'] = '1; mode=block'
            return resp, 201
    else:
        return "Fuck you!", 415
