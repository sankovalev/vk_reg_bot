# -*- coding: utf-8 -*-
import command_system
import MySQLdb
import common
from notifications import Tip, Error, Success
from settings import DB_params as p

def tutor(user_id, message_words):
   if not common.check_register(user_id):
      return Tip['tutor_update'], ''
   if len(message_words) != 2:
      return Tip['tutor'], ''

   db=MySQLdb.connect(host=p['host'], user=p['user'], passwd=p['passwd'], db=p['db'], charset = "utf8", use_unicode = True)
   c=db.cursor()
   #обновляем препода
   try:
      c.execute("""UPDATE Students SET Students.Tutor=%s WHERE idVK=%s""", [message_words[1].title(), str(user_id)])
      db.commit()
      answer = Success['tutor']
   except:
      db.rollback()
      answer = Error['tutor']
   db.close()
   return answer, ''

tutor_command = command_system.Command()

tutor_command.keys = ['препод', 'преподаватель', 'преподователь', 'физрук', 'tutor']
tutor_command.description = 'обновлю информацию о твоем преподавателе'
tutor_command.process = tutor
tutor_command.order = 4