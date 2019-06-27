# -*- coding: utf-8 -*-
import command_system
import MySQLdb
from notifications import Error
from settings import DB_params as p

def schedule(user_id, message_words):
   db=MySQLdb.connect(host=p['host'], user=p['user'], passwd=p['passwd'], db=p['db'], charset = "utf8", use_unicode = True)
   c=db.cursor()
   try:
      c.execute("""SELECT Day, Info, uID FROM Event WHERE Active=True ORDER BY Day""")
      events = c.fetchall()
      title = 'Вот список событий, на которые открыта регистрация:\n\n'
      events_list = '' if len(events)!=0 else 'занятия отсутствуют'
      for event in events:
          uid = str(event[2]) if event[2]!=None else 'не задано'
          day = str(event[0]) if event[0]!=None else 'не задан'
          info = str(event[1]) if event[1]!=None else 'отсутствует'
          events_list+='⚡ ID занятия: '+uid+'\n'+'🗓 Дата: '+day+'\n'+'📄 Информация о занятии: '+info+'\n\n'
      answer = title+events_list
   except:
      answer = Error['schedule']
   db.close()
   return answer, ''


schedule_command = command_system.Command()

schedule_command.keys = ['расписание', 'schedule', 'следующее']
schedule_command.description = 'покажу ближайшие занятия'
schedule_command.process = schedule
schedule_command.order = 7