# import mysql.connector
import os, re, time, json
def Launcher():
		# Database = mysql.connector.connect(
		# host="localhost",
		# user="mofish_root",
		# password="W8Lm&s^NCY41RtD0",
		# database="Mofish_Database"
		# )
		# cursor = Database.cursor()
		
		Instructor = json.loads(open('./Instructor.mofish', 'r').read())

def MCQ_Bank(Instructor):
	Command_Storage = 'insert into API_mcq_bank (svg_name, questionNo, answer, source_id)value("{svg_name}", "{question_no}", "{answer}", "{source_id}");'
	for Instructions in Instructor["mcq"]:
		svg_name = Instructions["File_Name"]
		question_no = Instructions["Question_Number"]
		answer = Instructions["Answer"]
		source_id = Instructions["Source"]
		Command = Command_Storage.format(svg_name=svg_name, question_no=question_no, answer=answer, source_id=source_id)
		Send_Command(Command)

def MCQ_Bank_Chapter_List(Instructor):
	Chapter_Instruction = Instructor["chapterList"]
	MCQ_Instructor = Instructor["mcq"]
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
							Send_Command(Command)

def Chapter(Instructor):
	Instructor = Instructor["chapterList"]
	Command_Storage = 'insert into API_chapter_list (syllabus, chapter_number)value("{syllabus}", "{chapter_number}");'

	for Instructions in Instructor:
		syllabus = Instructions["Syllabus"]
		chapter_number = Instructions["Chapter"]

		Command = Command_Storage.format(syllabus=syllabus, chapter_number=chapter_number)
		Send_Command(Command)

def Paper(Instructor):
	command = 'insert into API_paper_bank (paper_name, syllabus, year, month, paper_type, variant)value("{paper_name}", "{syllabus}", "{year}", "{month}", "{paper_type}", "{variant}");'

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

def Send_Command(Command):
		cursor.execute(Command)
		cursor.execute('COMMIT;')
