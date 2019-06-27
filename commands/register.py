# -*- coding: utf-8 -*-
import command_system
import MySQLdb
import common
from notifications import Tip, Error, Success
from settings import DB_params as p

def register(user_id, message_words):
   if len(message_words) != 3:
      return Tip['register'], ''
   db=MySQLdb.connect(host=p['host'], user=p['user'], passwd=p['passwd'], db=p['db'], charset = "utf8", use_unicode = True)
   c=db.cursor()
   #проверяем, есть ли студент в базе
   try:
      if common.check_register(user_id):
         answer = Success['register_check']
         return answer, ''
   except:
      answer = Error['register_check']
      return answer, ''

   #регистрируем нового студента, если его нет в базе
   try:
      c.execute("""INSERT INTO Students (Surname, Name, idVK) VALUES (upper(%s), upper(%s), %s)""",
            [message_words[1], message_words[2], str(user_id)])
      db.commit()
   except:
      db.rollback()
      answer = Error['register_new']
      return answer, ''
   db.close()
   answer = Success['register']
   return answer, ''

register_command = command_system.Command()

register_command.keys = ['регистрация', 'зарегай', 'register', 'регай']
register_command.description = 'добавлю тебя в базу'
register_command.process = register
register_command.order = 2