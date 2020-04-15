import mysql.connector
import os
import time
import re
import json

Database = mysql.connector.connect(
  host="localhost",
  user="mofish_root",
  password="W8Lm&s^NCY41RtD0",
  database="Mofish_Database"
)
cursor = Database.cursor()

def Send_Command():
  # Instructor_File = open('./Instructor.mofish', 'r')
  Instructor_File = open('/home/Python_MySQL/MCQ_Bank_Chapter/Instructor.mofish', 'r')
  Instructor = json.loads(Instructor_File.read())
  Command_Storage = 'insert into API_chapter_list (syllabus, chapter_number)value("{syllabus}", "{chapter_number}");'

  for Instructions in Instructor:
    syllabus = Instructions["Syllabus"]
    chapter_number = Instructions["Chapter"]

    Command = Command_Storage.format(syllabus=syllabus, chapter_number=chapter_number)
    print(Command)
    cursor.execute(Command)
    cursor.execute('COMMIT;')
    


Send_Command()
print('Done')
#https://blog.csdn.net/number1killer/article/details/77841565
#https://www.runoob.com/python/python-mysql.html