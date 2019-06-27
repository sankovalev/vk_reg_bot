import MySQLdb
from settings import DB_params as p

def check_register(user_id):
   db=MySQLdb.connect(host=p['host'], user=p['user'], passwd=p['passwd'], db=p['db'], charset = "utf8", use_unicode = True)
   c=db.cursor()
   c.execute("""SELECT count(*) FROM Students WHERE idVK=%s""", [str(user_id)])
   count = c.fetchone()[0]
   db.close()
   if int(count) == 0:
      return False
   else:
      return True

def check_letter(user_id):
   db=MySQLdb.connect(host=p['host'], user=p['user'], passwd=p['passwd'], db=p['db'], charset = "utf8", use_unicode = True)
   c=db.cursor()
   c.execute("""SELECT count(*) FROM Letter WHERE idVK=%s""", [str(user_id)])
   count = c.fetchone()[0]
   db.close()
   if int(count) == 0:
      return False
   else:
      return True

def add_letter(user_id):
   db=MySQLdb.connect(host=p['host'], user=p['user'], passwd=p['passwd'], db=p['db'], charset = "utf8", use_unicode = True)
   c=db.cursor()
   c.execute("""INSERT INTO Letter (idVK) VALUES (%s)""", [str(user_id)])
   db.commit()
   db.close()
   return