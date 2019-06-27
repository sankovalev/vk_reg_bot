import command_system
import operator
from settings import admins

commands = ['препод', 'инфо', 'кафедра', 'иду', 'помощь', 'привет', 'регистрация', 'группа', 'расписание', 'история']
#secret_commands = ['занятие', 'настарте', 'нафинише', 'экспорт']

def help(user_id, message_words):
   answer = 'Список доступных команд:\n\n'
   com = []
   sec_com = []
   for c in command_system.command_list:
      com.append(c) if c.keys[0].lower() in commands else sec_com.append(c)
   com.sort(key=operator.attrgetter('order'))
   sec_com.sort(key=operator.attrgetter('order'))
   for c in com:
      answer += c.keys[0].upper() + ' - ' + c.description + '\n'

   if len(sec_com)>0 and user_id in admins:
      answer += '\n🚧 Для организаторов: 🚧\n'
      for c in sec_com:
         answer += c.keys[0].upper() + ' - ' + c.description + '\n'
   answer += '\nДля получения подробной информации о команде введи ее название 👇'
   return answer, ''

help_command = command_system.Command()

help_command.keys = ['помощь', 'помоги', 'help']
help_command.description = 'покажу список команд'
help_command.process = help
help_command.order = 10