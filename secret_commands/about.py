# -*- coding: utf-8 -*-
import command_system
import MySQLdb
from notifications import Tip, Error, Success
from settings import DB_params as p
from settings import admins

def about(user_id, message_words):
   if user_id not in admins:
      return 'Хмм, не понимаю тебя. Напиши ПОМОЩЬ, чтобы узнать доступные команды.', ''
   if len(message_words) != 3:
      return Tip['about'], ''
   try:
      uid = message_words[1].upper()
      desc = message_words[2]
   except:
      return Tip['about'], ''
   db=MySQLdb.connect(host=p['host'], user=p['user'], passwd=p['passwd'], db=p['db'], charset = "utf8", use_unicode = True)
   c=db.cursor()
   #добавляем описание занятия
   try:
      c.execute("""UPDATE Event SET Info=%s WHERE uID=%s""", [desc, uid])
      db.commit()
      answer = Success['about']
   except:
      answer = Error['about']
   db.close()
   return answer, ''


about_command = command_system.Command()

about_command.keys = ['описание', 'ссылка', 'about']
about_command.description = 'добавить информацию и занятии'
about_command.process = about
about_command.order = 2