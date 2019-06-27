# -*- coding: utf-8 -*-
import command_system
import common
import MySQLdb
from settings import DB_params as p
from notifications import Tip, Error

def hello(user_id, message_words):
   #проверяем, есть ли студент в базе
   try:
      if common.check_register(user_id):
         answer = Tip['hello_old']
      else:
         answer = Tip['hello_new']
   except:
      answer = Error['hello']
      return answer, ''

   try:
      db=MySQLdb.connect(host=p['host'], user=p['user'], passwd=p['passwd'], db=p['db'], charset = "utf8", use_unicode = True)
      c=db.cursor()
      c.execute("""SELECT MAX(id) FROM Students UNION SELECT COUNT(*) FROM Activity""")
      res = c.fetchall()
      st_count = str(res[0][0])
      #reg_count = str(res[1][0])
      answer+='\n\n🤖 Мной пользуются уже '+st_count+' чел.'# \n📢 Отправлено приглашений: '+reg_count
   except:
      return answer, ''
   return answer, ''

hello_command = command_system.Command()

hello_command.keys = ['привет', 'hello', 'дратути', 'здравствуй', '.', 'здравствуйте', 'здраствуйте', 'здрасьте', 'салам', 'hi', 'ghbdtn', 'хай']
hello_command.description = 'поприветствую тебя и расскажу, что делать'
hello_command.process = hello
hello_command.order = 8