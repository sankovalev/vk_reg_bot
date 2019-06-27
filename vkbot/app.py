from flask import Flask, request, json
from settings import token, confirmation_token
import messageHandler


app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello from vkbot!'

@app.route('/', methods=['POST'])
def processing():
    data = json.loads(request.data)
    if 'type' not in data.keys():
        return 'not vk'
    if data['type'] == 'confirmation':
        return confirmation_token
    elif data['type'] == 'message_new':
        messageHandler.create_answer(data['object'], token) #тут все данные по объекту передаем в Handler
        return 'ok'
    elif data['type'] == 'group_join':
        messageHandler.welcome_new_user(data['object'], token)
        return 'ok'