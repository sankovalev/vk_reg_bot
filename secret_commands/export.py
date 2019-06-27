# -*- coding: utf-8 -*-
import command_system
import vkapi
from settings import token
from translit import transliterate
import csv
import MySQLdb
from settings import admins
from notifications import Tip, Error
from settings import DB_params as p

def export(user_id, message_words):
   if user_id not in admins:
      return 'Хмм, не понимаю тебя. Напиши ПОМОЩЬ, чтобы узнать доступные команды.', ''
   if len(message_words) != 3:
      return Tip['export'], ''
   department = message_words[1].upper()
   event_id = message_words[2].upper()
   db=MySQLdb.connect(host=p['host'], user=p['user'], passwd=p['passwd'], db=p['db'], charset = "utf8", use_unicode = True)
   c=db.cursor()
   #идентификатор занятия знаем, теперь получаем список студентов, а потом распределим по кафедрам
   try:
      c.execute("""SELECT t1.Surname, t1.Name, t1.Group, t1.Tutor, t1.Department, t2.StartTime, t2.FinishTime
                    FROM Students t1, Activity t2
                    WHERE t1.id=t2.StudentID and t2.Start=True
                    and t2.Finish=True and t1.Department=%s and t2.EventID=%s""", [department, event_id])
      active_students = c.fetchall()
      dep_eng = ''
      if department=='АФК':
         dep_eng = 'AFK'
      elif department=='АФКО':
         dep_eng = 'AFKO'
      elif department=='ФВ':
         dep_eng = 'FV'
      filename = transliterate(dep_eng+'_'+event_id)+'.csv'
      create_file(active_students, filename)
      attachments = vkapi.send_file(token, user_id, active_students, filename, department)
      answer = 'Готово! Файл содержит список студентов, посетивших занятие '+event_id+' с кафедры '+department+'.'
   except:
      db.close()
      answer = Error['export_stud']
      attachments = ''
   return answer, attachments


def create_file(active_students, filename):
   Header = (('Фамилия', 'Имя', 'Группа', 'Преподаватель', 'Кафедра', 'Старт', 'Финиш'),)
   with open('CSV/'+filename, 'w') as f:
      writer = csv.writer(f)
      writer.writerows(Header)
      writer.writerows(active_students)
   return


export_command = command_system.Command()

export_command.keys = ['Экспорт', 'дайсписок', 'export']
export_command.description = 'получить список участников'
export_command.process = export
export_command.order = 7