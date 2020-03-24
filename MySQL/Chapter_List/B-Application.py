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

def Check_Syllabus(Name):
  if Name == '0438':
    return '0620'
  if Name == '5054':
    return '0625'
  if Name == '5070':
    return '0620'
  if Name == '5090':
    return '0610'
  else:
    return Name

def Send_Command():
  # MCQ_Instructor_File = open('./Instructor_MCQ.mofish', 'r')
  MCQ_Instructor_File = open('/home/Python_MySQL/MCQ_Bank_Chapter/Instructor_MCQ.mofish', 'r')
  #Chapter_Instruction_File = open('./Instructor.mofish', 'r')
  Chapter_Instruction_File = open('/home/Python_MySQL/MCQ_Bank_Chapter/Instructor.mofish', 'r')

  Chapter_Instruction = json.loads(Chapter_Instruction_File.read())
  MCQ_Instructor = json.loads(MCQ_Instructor_File.read())
  Command_Storage = 'insert into API_mcq_bank_chapter (mcq_bank_id, chapter_list_id)value("{mcq_bank_id}", "{chapter_list_id}");'

  for Instructions in MCQ_Instructor:
    mcq_bank_id = Instructions["Question_ID"]
    Syllabus = Check_Syllabus(Instructions["File_Name"][0 : 4])
    Chapter_List = Instructions["Chapter"]
    if Chapter_List == 'Bug':
      continue
    else:
      for Chapter in Chapter_List:
        chapter_list_id = ''
        for Item in Chapter_Instruction:
          if Item["Chapter"] == Chapter:
            if Item["Syllabus"] == str(Syllabus):
              chapter_list_id = Item["ID"]
              Command = Command_Storage.format(mcq_bank_id=mcq_bank_id, chapter_list_id=chapter_list_id)
              print(Command)
              cursor.execute(Command)
              cursor.execute('COMMIT;')
        

          

  

Send_Command()
print('Done')
#https://blog.csdn.net/number1killer/article/details/77841565
#https://www.runoob.com/python/python-mysql.html