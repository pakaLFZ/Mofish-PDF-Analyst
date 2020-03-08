import mysql.connector
import os
import time
import re

Database = mysql.connector.connect(
  host="localhost",
  user="mofish_root",
  password="W8Lm&s^NCY41RtD0",
  database="Mofish_Database"
)
cursor = Database.cursor()

def Send_Command(Instructor):
  command = 'insert into API_mcq_bank (svg_name, question_no, answer, chapter, source_id)value('
  Counter = 0
  while Counter <= len(Instructor) - 2:
    command = command + '"' + str(Instructor[Counter]) + '", '
    Counter += 1
  command = command + '"' + str(Instructor[-1]) + '");'
  

  print(command)
  # input()
  cursor.execute(command)
  cursor.execute('COMMIT;')

Instructor_File = open('/home/Python_MySQL/MCQ_Bank/Instructor.mofish', 'r')
# Instructor_File = open('./Instructor.mofish', 'r')
Instructor = Instructor_File.read()
Command = []
Location_1 = 0


'''svg_name, question_no, answer, chapter, source_id'''
while Location_1 <= len(Instructor) - 1:
  Command = []
  Location_1 = Instructor.find('{', Location_1)
  Location_2 = Instructor.find('}', Location_1)
  if Location_1 == -1:
    break
  Counter = 1
  Location_3 = Location_1
  while Counter <= 5: # original 7
    Location_3 = Instructor.find('"', Location_3 + 1, Location_2)
    Location_4 = Instructor.find('"', Location_3 + 1, Location_2)
    Command.append(Instructor[Location_3 + 1 : Location_4])
    Location_3 = Location_4
    Counter += 1

  Send_Command(Command)
  Location_1 = Location_2


  
print('Done')
#https://blog.csdn.net/number1killer/article/details/77841565
#https://www.runoob.com/python/python-mysql.html