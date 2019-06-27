# -*- coding: utf-8 -*-
import command_system
from settings import token
import vkapi
import MySQLdb
import hashlib
import random
import common
import pyqrcode
from notifications import Tip, Error
from settings import DB_params as p

def train(user_id, message_words):
   if not common.check_register(user_id):
      return Tip['info'], ''
   if len(message_words) != 3:
      return Tip['train'], ''
   db=MySQLdb.connect(host=p['host'], user=p['user'], passwd=p['passwd'], db=p['db'], charset = "utf8", use_unicode = True)
   c=db.cursor()
   uid = message_words[2].upper()

   #и получаем id пользователя, а заодно узнаем, есть ли у него незаполненные поля, чтобы потом кинуть ему подсказку
   try:
      c.execute("""SELECT id FROM Students WHERE idVK=%s""", [user_id])
      id = c.fetchone()[0]
      c.execute("""SELECT COUNT(*) FROM Students St WHERE idVK=%s AND St.Group IS NOT NULL AND St.Tutor IS NOT NULL AND St.Department IS NOT NULL""", [user_id])
      tip = True if c.fetchone()[0]==0 else False
   except:
      db.close()
      return Error['train_reg'], ''
   if tip:
      db.close()
      return Error['train_info'], ''

   #проверяем, активно ли занятие
   try:
      c.execute("""SELECT Active, Day FROM Event WHERE uID=%s""", [uid])
      result = c.fetchone()
      active = result[0]
      day = result[1]
      if active==False:
         db.close()
         return Tip['train_day'], ''
   except:
      db.close()
      return Error['train_day'], ''

   #добавляем участника к событию и присылаем ему QR-код
   #но сначала проверяем, вдруг он уже добавлялся
   try:
      c.execute("""SELECT SecretKey FROM Activity WHERE StudentID=%s AND EventID=%s""", [id, uid])
      h = c.fetchone()
      if h==None:
         try:
            code = random.randint(11, 997)*(int(user_id)%9973) + random.randint(11, 9997)
            hcode = hashlib.md5(str(code).encode('utf8'))
            hash = hcode.hexdigest()
            c.execute("""INSERT INTO Activity (StudentID, EventID, SecretKey) VALUES (%s, %s, %s)""",[id, uid, hash])
            c.execute("""INSERT INTO User_Event (User_id, Event) VALUES (%s, %s)""", [user_id, uid]) #для дальнейшей генерации кнопок
            db.commit()
            db.close()
            #делаем картинку
            qr = pyqrcode.create(hash)
            qr.png('QR/'+hash+'.png', scale=10) #делаем картинку
         except:
            db.rollback()
            db.close()
            return Error['train_add'], ''
      else:
         hash = h[0]
   except:
      db.close()
      return Error['train_check'], ''

   try:
      attachment = vkapi.send_image(token, user_id, hash)
      answer = '✅ Ты в списке участников на занятие '+str(uid)+', которое состоится '+str(day)+'.\nПокажи этот QR-код на регистрации!📱'
      return answer, attachment
   except:
      return Error['train_send'], ''

train_command = command_system.Command()

train_command.keys = ['иду', 'go', 'погнали', 'отработка']
train_command.description = 'если собираешься пойти на занятие'
train_command.process = train
train_command = 6