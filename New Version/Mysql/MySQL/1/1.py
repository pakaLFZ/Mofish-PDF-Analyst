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
  command = 'insert into API_questionbank (filename, subject, papertype, month, year, question_number, chapter, answer)value('
  Counter = 0
  while Counter <= 6:
    command = command + '"' + str(Instructor[Counter]) + '", '
    Counter += 1
  command = command + '"' + str(Instructor[7]) + '");'
  
  #insert into API_questionbank (filename, subject, papertype, month, year, question_number, chapter, answer)value("0620_w18_qp_22-1_0@16.svg", "IGCSE/0620", "Paper 2", "October/November", "2018", "16", "1", "A",);
  print(command)
  cursor.execute(command)
  cursor.execute('COMMIT;')

Instructor_File = open('./Log.txt', 'r')
Instructor_Content = Instructor_File.read()
Instructor = []
Location = 0
##subject;paper;month;year;QuestionNumber;chapter1;answer;
#>0439_w17_qp_11-2_0@1.svg:IGCSE/Chemistry(US);Paper 1;October/November;2017;1;1;A;
while Location <= len(Instructor_Content) - 1:
  Instructor = []
  if Instructor_Content[Location] == '>':
    Location += 1
    Counter = 0
    while Counter <= 7:
      Content = ''
      while True:
        if Instructor_Content[Location] == ';':
          Location += 1
          Instructor.append(Content)
          break
        Content = Content + Instructor_Content[Location]
        Location += 1
      Counter += 1
  Location += 1
  Send_Command(Instructor)
    
    



# command = 'insert into API_questionbank (filename,year,month,papertype,answer)value("paper1",2020,11,1,"A");'
# cursor.execute(command)
# cursor.execute('COMMIT;')
print('Done')
#https://blog.csdn.net/number1killer/article/details/77841565
#https://www.runoob.com/python/python-mysql.html