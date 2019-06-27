# -*- coding: utf-8 -*-
import command_system
import MySQLdb
from settings import admins
from notifications import Tip, Error, Success
from settings import DB_params as p
import datetime

def finish(user_id, message_words):
   if user_id not in admins:
      return 'Хмм, не понимаю тебя. Напиши ПОМОЩЬ, чтобы узнать доступные команды.', ''
   if len(message_words) == 1:
      return Tip['finish'], ''
   answer = finish_time(user_id, message_words) if message_words[1].upper() == 'ВРЕМЯ' else finish_notime(user_id, message_words)
   return answer, ''

def finish_notime(user_id, message_words):
   hashes = message_words[1:]
   db=MySQLdb.connect(host=p['host'], user=p['user'], passwd=p['passwd'], db=p['db'], charset = "utf8", use_unicode = True)
   c=db.cursor()
   #заносим их все в базу
   try:
      for hash in hashes:
         c.execute("""UPDATE Activity SET Finish=TRUE WHERE SecretKey=%s""", [hash])
      db.commit()
      answer = Success['finish']
   except:
      answer = Error['finish']
   db.close()
   try:
       with open("Admin_LOGS.txt", "a") as log:
          log.write(str(datetime.datetime.now())+" Admin "+str(user_id) +" added "+str(len(hashes))+" finishers (no time)\n")
   except:
       pass
   return answer

def finish_time(user_id, message_words):
   hashes_times = message_words[2:]
   if len(hashes_times) % 2 != 0:
      return Tip['finish'], ''
   db=MySQLdb.connect(host=p['host'], user=p['user'], passwd=p['passwd'], db=p['db'], charset = "utf8", use_unicode = True)
   c=db.cursor()
   #заносим их всех в базу
   composite_list = [hashes_times[x:x+2] for x in range(0, len(hashes_times),2)]
   try:
      for hash_time in composite_list:
         if hash_time[1].count(':')==2:
            c.execute("""UPDATE Activity SET Finish=TRUE, FinishTime=%s WHERE SecretKey=%s""", [hash_time[1], hash_time[0]])
      db.commit()
      answer = Success['finish_time']
   except:
      answer = Error['finish_time']
   db.close()
   try:
       with open("Admin_LOGS.txt", "a") as log:
          log.write(str(datetime.datetime.now())+" Admin "+str(user_id) +" added "+str(len(composite_list))+" finishers (with time)\n")
   except:
       pass
   return answer

finish_command = command_system.Command()

finish_command.keys = ['финиш', 'список2', 'finish']
finish_command.description = 'добавить финишировавших (расширенная)'
finish_command.process = finish
finish_command.order = 6