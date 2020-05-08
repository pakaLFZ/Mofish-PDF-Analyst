import os, re, time, json, sys

def Launcher():
	# File_Position = 'E:/0Mofish/PDF/Table-14_Q/Test' #'E:/0Mofish/PDF/Table-23/B-Product'
	File_Position = '../Spliter/B-Product-Done'
	Problem_Positiom = './Problems'
	Book_Location = './Book'
	Instructor = json.loads(open('./Source/Answer_Bank.json', 'r').read())
	Chapter_List = json.loads(open('./Source/Chapter_List.mofish', 'r').read())
	Safety_Instructor = open('./Source/Safety_Instructor.mofish', 'r').read()
	Log = open('./Log.json', 'w')
	if not os.path.exists(File_Position):
		os.makedirs(File_Position)
	if not os.path.exists(Problem_Positiom):
		os.makedirs(Problem_Positiom)
	if not os.path.exists(Book_Location):
		os.makedirs(Book_Location)

	File_List = Get_File_List(File_Position)

	#分类
	PRINT('>', 0)
	Location = 0
	Chapter_Data = []
	while Location <= len(File_List) - 1:
		if Location % 500 == 0:
			PRINT('-', 0)
		File_Content = Get_File_Content(File_List[Location], File_Position, Safety_Instructor)
		Content = {}
		Content["file"] = File_List[Location]
		Content["chapter"] = Classify_File(File_List[Location], File_Content, Book_Location)
		Chapter_Data.append(Content)
		Location += 1
	PRINT('', 1)


	#对答案
	PRINT('>', 1)
	File_List_Storage = File_List
	Answer_List = Match_Answer(File_List_Storage, Instructor, File_Position, Problem_Positiom)


	
	
	#分析PDF name
	PRINT('>', 1)
	Paper_List = Get_Paper_List(Get_File_List(File_Position))
	Final_Data = {}
	Final_Data["mcq"] = Analysis_PDF_Names(Answer_List, Paper_List, Chapter_Data)
	Final_Data['chapterList'] = Chapter_List
	Final_Data['paperList'] = Paper_List

	
	Log.write(json.dumps(Final_Data))
	Log.flush()
	
def Pinput(Content):
	print(Content)
	input()

def PRINT(Content, Check):
	if Check == 1:
		sys.stdout.write(Content +'\n')
		sys.stdout.flush()
	else:
		sys.stdout.write(Content)
		sys.stdout.flush()

def Get_File_List(File_Position):
	Files = []
	for root, dirs, files in os.walk(File_Position, topdown=True):
		for name in files:
			if re.match('.*(.svg)', os.path.join(name)) is not None:
				Files.append(os.path.join(name))
	return Files

def Space_Eliminator(Name):	 
	Name = re.sub('/','\\', Name)
	while Name.find(' ') != -1:
		Location_1 = Name.find(' ')
		Location_1 = Name.rfind('\\', 0, Location_1)
		Location_2 = Name.find('\\', Location_1 + 1)
		if Location_2 == -1:
			Location_2 = len(Name) - 1
		Name = Name[0 : Location_1] + '"' + Name[Location_1 + 1 : Location_2] + '"' + Name[Location_2 : len(Name) - 1]
	return Name

def Bug_File_Copier(File_Name, File_Storage, Problem_Storage):	  #将有问题的文件复制到BugFile文件夹内
	File_Location_Storage = ''
	Command_Storage = ''
	File_Location = File_Storage + '/' + File_Name
	File_Location_Storage = Space_Eliminator(File_Location)
	Bug_File_Location_Storage = Problem_Storage + '/' + File_Name
	File_Product_Location_Storage = Space_Eliminator(Bug_File_Location_Storage)
	Command_Storage = 'copy ' + File_Location_Storage + ' ' + File_Product_Location_Storage
	os.system(Command_Storage)

def Safety_Check(Word):
	try:
		Word = Word.lower()
		if Word[-3:] == 'ing':
			Word = Word[:-3]
		if Word[-2:] == 'es':
			Word == Word[:-2]
		if Word[-2:] == 'ed':
			Word == Word[:-2]
		if Word[-1] == 's':
			Word = Word[:-1]
	except:
		pass
	return Word

def Choose_Book(Name):
	Chemistry = '0438, 0620, 5070'
	Biology = '0610, 5090' 
	Physics = '0625, 5054'
	if Chemistry.find(Name) != -1:
		return 'Chemistry'
	if Biology.find(Name) != -1:
		return 'Biology'
	if Physics.find(Name) != -1:
		return 'Physics'

def Get_Paper_List(File_List):
	Paper_Name = []
	for File in File_List:
		Location = File.find('@')
		Paper_Name.append(File[0 : Location])
	Paper_List = list(set(Paper_Name))
	Id_Count = 1
	Data = []
	for Paper in Paper_List:
		Year = ''
		Month = ''
		Syllabus = ''
		try:
			Syllabus = Paper[0 : 4]
			Year = '20' + Paper[6 : 8]
			Month = Paper[5]
			Paper_type = 0
			Variant = ''
		except:
			pass

		try:
			if Paper[8 : 11] == '_2_':
				Paper_type = 2
			if Paper[12 : 15] == '_2':
				Paper_type = 2
				Variant = Paper[15]
			if Paper[11 : 13] == '_2':
				Paper_type = 2
				Variant = Paper[13]

			if Paper[8 : 11] == '_1_':
				Paper_type = 1
			if Paper[12 : 15] == '_1':
				Paper_type = 1
				Variant = Paper[15]
			if Paper[11 : 13] == '_1':
				Paper_type = 1
				Variant = Paper[13]
			if Variant == '.':
				Variant = ''
		except:
			pass
		Variant = str(Paper_type) + str(Variant)

		Information = {}
		Information['id'] = Id_Count
		Information['paperName'] = Paper
		Information['syllabus'] = Syllabus
		Information['year'] = Year
		Information['month'] = Month
		Information['paperType'] = Paper_type
		Information['variant'] = Variant
		Data.append(Information)
		Id_Count += 1
	return Data

def Get_File_Content(File_Name, File_Storage, Instructor):
	File = open(File_Storage + '/' + File_Name, 'r', encoding='utf-8').read()
	Location_1 = 0
	Content = ''
	while 1:
		Location_1 = File.find('tspan', Location_1)
		if Location_1 == -1:
			break
		Location_2 = File.find('>', Location_1)
		Location_1 = File.find('<', Location_1)
		Sentence = File[Location_2 + 1 : Location_1]
		Content = Content + Sentence
	Content = list(set(re.sub(r'[^\w\s]|\r|\n',' ',Content).split(' ')))

	Location = 0
	while Location <= len(Content) - 1:
		Content[Location] = Safety_Check(Content[Location])
		if Instructor.find(Content[Location]) != -1 or not Content[Location].isalpha():
			del Content[Location]
			continue
		Location += 1
	return {"content":Content, "file_name":File_Name}

def Match_Answer(File_Name_List, Instructor, File_Storage, Problem_Storage):
	Data = []
	while len(File_Name_List) != 0:
		Bug_File = []
		Content = {"file": File_Name_List[0]}

		Location_1 = File_Name_List[0].find('@')
		Location_2 = File_Name_List[0].find('.')
		Question_Number = File_Name_List[0][Location_1 + 1 : Location_2]

		Paper_Name = File_Name_List[0][0 : Location_1]
		Paper_Name = Paper_Name.replace("qp", "ms")

		try:
			Answer = Instructor[Paper_Name][Question_Number]
			Content["answer"] = Answer
			Data.append(Content)
		except:
			Content["answer"] = '#Bug'
			Data.append(Content)
		del File_Name_List[0]
	return Data

def Classify_File(File_Name, Content, Book_Location):
	Book = ''
	if Choose_Book(File_Name[0 : 4]) == 'Chemistry':
		Book = open(Book_Location + '/Chemistry.txt', 'r').read()
	if Choose_Book(File_Name[0 : 4]) == 'Biology':
		Book = open(Book_Location + '/Biology.txt', 'r').read()
	if Choose_Book(File_Name[0 : 4]) == 'Physics':
		Book = open(Book_Location + '/Physics.txt', 'r').read()
	Chapter_List = []
	Chapter = {}
	for Item in Content["content"]:
		if Book.find(Item) != -1:
			Location_1 = 0
			while 1:
				Location_1 = Book.find(Item, Location_1)
				if Location_1 == -1:
					break
				Boundary = Book.find('}', Location_1)
				Location_2 = Book.find(':', Location_1, Boundary)
				Location_3 = Book.find('>', Location_2, Boundary)
				if Location_2 == -1 or Location_3 == -1:
					print('Bug')
					print(Book[Location_1 - 50 : Location_1 + 50], end='\n\n')
					print(Book[Location_1])
				Value = Book[Location_2 + 1 : Location_3]
				Location_4 = Book.rfind('chapter', 0, Location_1)
				Location_5 = Book.find(':', Location_4)
				Location_6 = Book.find('#', Location_4)
				Chapter_Storage = Book[Location_5 + 1 : Location_6]
   
				if Chapter_Storage in Chapter.keys():
					Chapter[Chapter_Storage] = float(Chapter[Chapter_Storage]) + float(Value)
				else:
					Chapter_List.append(Chapter_Storage)
					Chapter[Chapter_Storage] = Value
				Location_1 = Location_3
	for Item in Chapter_List:
		Chapter[Item] = round(float(Chapter[Item]), 2)
	Chapter_Value = []
	Chapter_List.sort()
	for Item in Chapter_List:
		Chapter_Value.append(Chapter[Item])
	
	Chapter_Value = sorted(Chapter_Value)
	
	return [k for k,v in Chapter.items() if float(v) == float(Chapter_Value[-1])]

def Analysis_PDF_Names(MCQ_Data, Paper_List, Chapter_Data):
	Information = []
	Instructor_Paper = Paper_List
	Instructor_Chapter = Chapter_Data
	# Location_1 = 0
	Question_ID_Count = 1
	for File in MCQ_Data:
		Content = {}
		File_Name = File["file"]
		Answer = File["answer"]
		if Answer[0] == '#':
			Answer = 'None'

		Location_3 = File_Name.find('@')
		Paper_Name = File_Name[0 : Location_3]
		ID = -1
		for Item in Paper_List:
			# print(Item["paperName"])
			# print(Paper_Name)
			# input()
			if Item["paperName"].find(Paper_Name) != -1:
				ID = Item['id']

		# Location_3 = Instructor_Paper.find(Paper_Name)
		# Location_4 = Instructor_Paper.rfind('{', 0, Location_3)
		# Location_3 = Instructor_Paper.find('ID', Location_4)
		# Location_4 = Instructor_Paper.find('"', Location_3)
		# Location_3 = Instructor_Paper.find('"', Location_4 + 1)
		# ID = Instructor_Paper[Location_4 + 1 : Location_3]

		Location_3 = File_Name.find('@')
		Location_4 = File_Name.find('.')
		Question_No = File_Name[Location_3 + 1 : Location_4]
		# print(File_Name)
		# input()
		Check = 0
		for items in Instructor_Chapter:
			if items["file"] == File_Name:
				Chapter = items["chapter"]
				Check = 1
		if Check == 0:
			Chapter = 'Bug'


		Content["File_Name"] = File_Name
		Content["Question_Number"] = Question_No 
		Content["Answer"] = Answer 
		Content["Source"] = ID 
		Content["Question_ID"] = Question_ID_Count
		Content["Chapter"] = Chapter

		Information.append(Content)
		Question_ID_Count += 1

	return Information

Launcher()