command_list = []

class Command:
   def __init__(self):
       self.__keys = [] #свойство: ключи, по которым обращаемся к команде(в строчном виде)
       self.description = '' #справка по командам бота
       self.order = 0
       command_list.append(self)

    #
   @property
   def keys(self):
       return self.__keys

    #
   @keys.setter
   def keys(self, mas):
       for k in mas:
           self.__keys.append(k.lower())

    #тут формируем ответ
   def process(self):
       pass