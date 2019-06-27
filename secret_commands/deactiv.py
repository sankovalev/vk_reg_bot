# -*- coding: utf-8 -*-
import command_system
import MySQLdb
from notifications import Tip, Error, Success
from settings import DB_params as p
from settings import admins

def deactiv(user_id, message_words):
   if user_id not in admins:
      return 'Хмм, не понимаю тебя. Напиши ПОМОЩЬ, чтобы узнать доступные команды.', ''
   if len(message_words) != 2:
      return Tip['deactiv'], ''
   try:
      uid = message_words[1].upper()
   except:
      return Tip['deactiv'], ''
   db=MySQLdb.connect(host=p['host'], user=p['user'], passwd=p['passwd'], db=p['db'], charset = "utf8", use_unicode = True)
   c=db.cursor()
   #деактивируем занятие
   try:
      c.execute("""UPDATE Event SET Active=FALSE WHERE uID=%s""", [uid])
      db.commit()
      answer = Success['deactiv']
   except:
      answer = Error['deactiv']
   db.close()
   return answer, ''


deactiv_command = command_system.Command()

deactiv_command.keys = ['деактив', 'скрыть', 'деактивиров', 'deactivate']
deactiv_command.description = 'скрыть занятие из расписания'
deactiv_command.process = deactiv
deactiv_command.order = 4