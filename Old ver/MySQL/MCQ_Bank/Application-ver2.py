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
  Instructor_File = open('/home/Python_MySQL/MCQ_Bank/Instructor.mofish', 'r')
  Instructor = json.loads(Instructor_File.read())
  Command_Storage = 'insert into API_mcq_bank (svg_name, questionNo, answer, source_id)value("{svg_name}", "{question_no}", "{answer}", "{source_id}");'

  for Instructions in Instructor:
    svg_name = Instructions["File_Name"]
    question_no = Instructions["Question_Number"]
    answer = Instructions["Answer"]
    source_id = Instructions["Source"]
    Command = Command_Storage.format(svg_name=svg_name, question_no=question_no, answer=answer, source_id=source_id)
    print(Command)
    cursor.execute(Command)
    cursor.execute('COMMIT;')
    


Send_Command()
print('Done')
#https://blog.csdn.net/number1killer/article/details/77841565
#https://www.runoob.com/python/python-mysql.html