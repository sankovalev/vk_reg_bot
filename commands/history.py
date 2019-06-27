# -*- coding: utf-8 -*-
import command_system
import MySQLdb
from notifications import Error
from settings import DB_params as p

def history(user_id, message_words):
   db=MySQLdb.connect(host=p['host'], user=p['user'], passwd=p['passwd'], db=p['db'], charset = "utf8", use_unicode = True)
   c=db.cursor()
   try:
      c.execute("""SELECT t2.EventID, t2.StartTime, t2.FinishTime FROM Students t1, Activity t2 WHERE t1.id=t2.StudentID AND t1.idVK=%s AND t2.Start=TRUE AND t2.Finish=TRUE""", [str(user_id)])
      events = c.fetchall()
      title = 'Список уже посещенных занятий:\n\n'
      events_list = '' if len(events)!=0 else 'занятия отсутствуют'
      for event in events:
         uid = str(event[0]) if event[0]!=None else 'не задано'
         st_time = str(event[1]) if event[1]!=None else '-//-'
         fin_time = str(event[2]) if event[2]!=None else '-//-'
         events_list+='✔ ID занятия: '+uid+'\n'+'🚩 Время старта: '+st_time+'\n'+'🏁 Время финиша: '+fin_time+'\n\n'
      answer = title+events_list
   except:
      answer = Error['history']
   db.close()
   return answer, ''


history_command = command_system.Command()

history_command.keys = ['история', 'history', 'прошлое']
history_command.description = 'покажу твою историю посещений'
history_command.process = history
history_command.order = 9