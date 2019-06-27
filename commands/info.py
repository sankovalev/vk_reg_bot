# -*- coding: utf-8 -*-
import command_system
import MySQLdb
import common
from notifications import Error, Tip
from settings import DB_params as p

def info(user_id, message_words):
   if not common.check_register(user_id):
      return Tip['info'], ''
   db=MySQLdb.connect(host=p['host'], user=p['user'], passwd=p['passwd'], db=p['db'], charset = "utf8", use_unicode = True)
   c=db.cursor()
   nf = '⛔'#не заполнено
   #достаем всю информацию о студенте
   try:
      c.execute("""SELECT * FROM Students WHERE idVK=%s""", [str(user_id)])
      data = c.fetchone()
      if data[3]!=None:
         group = data[3]; g_flag = '🛡️'
      else:
         group = 'не задано'; g_flag = nf
      if data[4]!=None:
         tutor = data[4]; t_flag = '🎽'
      else:
         tutor = 'не задано'; t_flag = nf
      if data[6]!=None:
         department = data[6]; d_flag = '🏛'
      else:
         department = 'не задано'; d_flag = nf
      answer = 'Вот, что мне известно о тебе: \n👤 ФИ: '+data[1]+' '+data[2]+'\n'+g_flag+' Группа: '+group+'\n'+t_flag+' Преподаватель: '+tutor+'\n'+d_flag+' Кафедра: '+department #+'\n'+a_flag+' Автопилот: '+autopilot
      tip = '\n\nТы можешь добавить или обновить информацию о группе, преподавателе и кафедре с помощью соответствующих команд. \nПример: ГРУППА 1234'

   except:
      answer = Error['info_student']
      tip = ''
   db.close()
   return answer+tip, ''

info_command = command_system.Command()

info_command.keys = ['инфо', 'информация', 'данные', 'info', 'information']
info_command.description = 'покажу твои регистрационные данные'
info_command.process = info
info_command.order = 1