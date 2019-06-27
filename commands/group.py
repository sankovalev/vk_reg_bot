# -*- coding: utf-8 -*-
import command_system
import MySQLdb
import common
from notifications import Tip, Error, Success
from settings import DB_params as p

def group(user_id, message_words):
   if not common.check_register(user_id):
      return Tip['group_update'], ''
   if len(message_words) != 2:
      return Tip['group'], ''

   db=MySQLdb.connect(host=p['host'], user=p['user'], passwd=p['passwd'], db=p['db'], charset = "utf8", use_unicode = True)
   c=db.cursor()
   #обновляем группу
   try:
      c.execute("""SELECT COUNT(*) FROM Students WHERE idVK=%s""", [user_id])
      if c.fetchone()[0]==0:
          db.close()
          return Tip['group_update'], ''

      c.execute("""UPDATE Students SET Students.Group=%s WHERE idVK=%s""", [message_words[1].upper(), str(user_id)])
      db.commit()
   except:
      db.rollback()
      answer = Error['group']
   db.close()
   answer = Success['group']
   return answer, ''

group_command = command_system.Command()

group_command.keys = ['группа', 'група', 'group']
group_command.description = 'обновлю информацию о группе'
group_command.process = group
group_command.order = 3