# -*- coding: utf-8 -*-
import command_system
import MySQLdb
import common
from notifications import Tip, Error, Success
from settings import DB_params as p

def department(user_id, message_words):
   if not common.check_register(user_id):
      return Tip['department_update'], ''
   if (len(message_words) == 2 and message_words[1].upper() in ['АФК', 'АФКО', 'ФВ', 'ФОФ', 'ПРОФКОМ']):
      db=MySQLdb.connect(host=p['host'], user=p['user'], passwd=p['passwd'], db=p['db'], charset = "utf8", use_unicode = True)
      c=db.cursor()
   else:
      return Tip['department'], ''

   try:
      #обновляем кафедру
      c.execute("""UPDATE Students SET Students.Department=%s WHERE idVK=%s""", [message_words[1].upper(), str(user_id)])
      db.commit()
   except:
      db.rollback()
      answer = Error['department']
   db.close()
   answer = Success['department']
   return answer, ''

department_command = command_system.Command()

department_command.keys = ['кафедра', 'department', 'каф', 'dep']
department_command.description = 'обновлю информацию о твоей кафедре'
department_command.process = department
department_command.order = 5