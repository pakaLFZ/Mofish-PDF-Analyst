
import os
import time
import re
import json

def Launcher():
	Log = open('./Log.txt', 'w')
	Instructor_File = open('./1.txt', 'r')
	Instructor = Instructor_File.read()
	Location_1 = 0
	Chapter = []
	while 1:
		Content = {}
		Location_1 = Instructor.find('chapter', Location_1)
		if Location_1 == -1:
			break
		Location_2 = Instructor.find(':', Location_1)
		Location_3 = Instructor.find('#', Location_1)
		Content["Syllabus"] = '###'
		Content["Chapter"] = Instructor[Location_2 + 1 : Location_3]
		Chapter.append(Content)
		Location_1 = Location_3
	Log.write(json.dumps(Chapter))
Launcher()



