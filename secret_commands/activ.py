# -*- coding: utf-8 -*-
import command_system
import MySQLdb
from notifications import Tip, Error, Success
from settings import DB_params as p
from settings import admins

def activ(user_id, message_words):
   if user_id not in admins:
      return 'Хмм, не понимаю тебя. Напиши ПОМОЩЬ, чтобы узнать доступные команды.', ''
   if len(message_words) != 2:
      return Tip['activ'], ''
   try:
      uid = message_words[1].upper()
   except:
      return Tip['activ'], ''
   db=MySQLdb.connect(host=p['host'], user=p['user'], passwd=p['passwd'], db=p['db'], charset = "utf8", use_unicode = True)
   c=db.cursor()
   #деактивируем занятие
   try:
      c.execute("""UPDATE Event SET Active=TRUE WHERE uID=%s""", [uid])
      db.commit()
      answer = Success['activ']
   except:
      answer = Error['activ']
   db.close()
   return answer, ''


activ_command = command_system.Command()

activ_command.keys = ['актив', 'показать', 'активировать', 'activate']
activ_command.description = 'показать занятие в расписании'
activ_command.process = activ
activ_command.order = 3