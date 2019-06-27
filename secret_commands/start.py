# -*- coding: utf-8 -*-
import command_system
import MySQLdb
from settings import admins
from notifications import Tip, Error, Success
from settings import DB_params as p
import datetime

def start(user_id, message_words):
   if user_id not in admins:
      return 'Хмм, не понимаю тебя. Напиши ПОМОЩЬ, чтобы узнать доступные команды.', ''
   if len(message_words) == 1:
      return Tip['start'], ''
   answer = start_time(user_id, message_words) if message_words[1].upper() == 'ВРЕМЯ' else start_notime(user_id, message_words)
   return answer, ''

def start_notime(user_id, message_words):
   hashes = message_words[1:]
   db=MySQLdb.connect(host=p['host'], user=p['user'], passwd=p['passwd'], db=p['db'], charset = "utf8", use_unicode = True)
   c=db.cursor()
   #заносим их все в базу
   try:
      for hash in hashes:
         c.execute("""UPDATE Activity SET Start=TRUE WHERE SecretKey=%s""", [hash])
      db.commit()
      answer = Success['start']
   except:
      answer = Error['start']
   db.close()
   try:
      with open("Admin_LOGS.txt", "a") as log:
          log.write(str(datetime.datetime.now())+" Admin "+str(user_id) +" added "+str(len(hashes))+" starting people (no time)\n")
   except:
       pass
   return answer

def start_time(user_id, message_words):
   hashes_times = message_words[2:]
   if len(hashes_times) % 2 != 0:
      return Tip['start'], ''
   db=MySQLdb.connect(host=p['host'], user=p['user'], passwd=p['passwd'], db=p['db'], charset = "utf8", use_unicode = True)
   c=db.cursor()
   #заносим их всех в базу
   composite_list = [hashes_times[x:x+2] for x in range(0, len(hashes_times),2)]
   try:
      for hash_time in composite_list:
         if hash_time[1].count(':')==2:
            c.execute("""UPDATE Activity SET Start=TRUE, StartTime=%s WHERE SecretKey=%s""", [hash_time[1], hash_time[0]])
      db.commit()
      answer = Success['start_time']
   except:
      answer = Error['start_time']
   db.close()
   try:
    #   logging.basicConfig(filename="Admin_LOGS.txt", level=logging.INFO)
    #   logging.info("Admin "+str(user_id) +" added "+str(len(composite_list))+" starting people (with time)")
      with open("Admin_LOGS.txt", "a") as log:
          log.write(str(datetime.datetime.now())+" Admin "+str(user_id) +" added "+str(len(composite_list))+" starting people (with time)\n")
   except:
       pass
   return answer

start_command = command_system.Command()

start_command.keys = ['старт', 'список1', 'start']
start_command.description = 'добавить стартовавших (расширенная)'
start_command.process = start
start_command.order = 5