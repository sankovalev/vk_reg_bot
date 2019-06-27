# -*- coding: utf-8 -*-
import vkapi
import MySQLdb
import os
import json
import common
import importlib
from settings import admins, DB_params as p
from command_system import command_list
from notifications import Tip
import re

bot_active = True;

def load_modules(user_id):
   # путь от рабочей директории, ее можно изменить в настройках приложения
   files = os.listdir("commands")
   modules = filter(lambda x: x.endswith('.py'), files)
   for m in modules:
      importlib.import_module("commands." + m[0:-3])

   secret_files = os.listdir("secret_commands")
   secret_modules = filter(lambda x: x.endswith('.py'), secret_files)
   if user_id in admins:
      for m in secret_modules:
         importlib.import_module("secret_commands." + m[0:-3])

def get_answer(user_id, message):
    # Сообщение и файл по умолчанию, если распознать не удастся
    if bot_active==False:
        if user_id in admins:
            return 'Я прилег отдохнуть.', ''
        else:
            return 'Извини, я сейчас обновляюсь. Напиши мне попозже :)', ''

    if not common.check_letter(user_id):
        common.add_letter(user_id)
        return Tip['hello_new'], ''
    answer = "Хм, не понимаю тебя 😐\nНапиши ПОМОЩЬ, чтобы узнать доступные команды."
    attachment = ''
    message = re.sub('[\[!@#$&)(*\]]', '', message)
    message_words = message.split()
    for c in command_list:
        if message_words[0].lower() in c.keys:  #первое слово в сообщении (команда)
            answer, attachment = c.process(user_id, message_words)
    return answer, attachment


def welcome_new_user(data, token):
   user_id = data['user_id']
   message = 'привет'
   load_modules(user_id)
   answer, attachment = get_answer(user_id, message)
   vkapi.send_message(user_id, token, answer, attachment)

def create_answer(data, token):
   user_id = data['user_id'] #id пользователя ВК
   message = data['body'] #сообщение пользователя
   load_modules(user_id)
   answer, attachment = get_answer(user_id, message)
#   vkapi.send_message(user_id, token, answer, attachment)
   vkapi.send_message_with_buttons(user_id, token, answer, attachment, str(json.dumps(build_buttons(user_id), ensure_ascii=False)) )

FIRST_LINE = [{
         "action": {"type": "text", "label": "Инфо"},
         "color": "primary"},
        {
         "action": {"type": "text", "label": "Расписание"},
         "color": "default"}]

SECOND_LINE = [{
         "action": {"type": "text", "label": "История"},
         "color": "default"},
        {
         "action": {"type": "text", "label": "Помощь"},
         "color": "primary"}]

def generate_event_buttons(events_id):
   KEYBOARD_EVENTS = []
   for i, event_id in enumerate(events_id):
       KEYBOARD_EVENTS.append([{
         "action": {"type": "text", "label": "Иду на " + event_id.upper()},
         "color": "positive"}])
   return KEYBOARD_EVENTS

def build_buttons(user_id): #тут по-хорошему нужно передать айдишник юзера и персонально для него выводить события
   buttons = [FIRST_LINE, SECOND_LINE]
   db=MySQLdb.connect(host=p['host'], user=p['user'], passwd=p['passwd'], db=p['db'], charset = "utf8", use_unicode = True)
   c=db.cursor()
   try:
      c.execute("""SELECT Day, uID FROM Event WHERE Active=True ORDER BY Day""")
      events = c.fetchall()
      events_id = []
      for event in events:
          isreg = c.execute("""SELECT count(*) FROM User_Event WHERE User_id=%s AND Event=%s""", [user_id, event[1]])
          isreg = True if c.fetchone()[0]==0 else False
          if event[1]!=None and isreg:
             events_id.append(str(event[1]))
      KEYBOARD_EVENTS = generate_event_buttons(events_id)
      for KEYBOARD_EVENT in KEYBOARD_EVENTS:
         buttons.insert(0, KEYBOARD_EVENT)
   except:
      pass
   db.close()
   KEYBOARD_MAIN = { "one_time": False, "buttons": buttons }
   return KEYBOARD_MAIN


