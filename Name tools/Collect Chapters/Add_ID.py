import os, json

def Launcher():
	Instructor = json.loads(open('./Instructor.mofish', 'r').read())
	Log = open('./log.txt', 'w')
	Content = []
	Location = 0
	while Location <= len(Instructor) - 1:
		Data = {}
		Data["ID"] = Location + 1
		Data["Chapter"] = Instructor[Location]["Chapter"]
		Data["Syllabus"] = Instructor[Location]["Syllabus"]
		Content.append(Data)
		Location += 1
	Log.write(json.dumps(Content))
	Log.flush()
Launcher()