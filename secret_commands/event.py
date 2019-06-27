# -*- coding: utf-8 -*-
import command_system
import datetime
import MySQLdb
from notifications import Tip, Error, Success
from settings import DB_params as p
from settings import admins

def event(user_id, message_words):
   if user_id not in admins:
      return 'Хмм, не понимаю тебя. Напиши ПОМОЩЬ, чтобы узнать доступные команды.', ''
   if len(message_words) != 5:
      return Tip['event'], ''
   try:
      year = message_words[1] if len(message_words[1])==4 else datetime.datetime.now().year
      month = message_words[2] if message_words[2][0]!='0' else message_words[2][1]
      day = message_words[3] if message_words[3][0]!='0' else message_words[3][1]
      uid = message_words[4]
   except:
      return Tip['event'], ''

   db=MySQLdb.connect(host=p['host'], user=p['user'], passwd=p['passwd'], db=p['db'], charset = "utf8", use_unicode = True)
   c=db.cursor()
   #добавляем новое занятие
   try:
      d = datetime.date(int(year), int(month), int(day))
      c.execute("""INSERT INTO Event (Day, Active, uID) VALUES (%s, True, %s)""", [d, uid])
      db.commit()
      answer = Success['event']
   except:
      answer = Error['event']
   db.close()
   return answer, ''

event_command = command_system.Command()

event_command.keys = ['занятие', 'велнес', 'тренировка']
event_command.description = 'добавить дату нового занятия'
event_command.process = event
event_command.order = 1