import os, re, time, sys

def Launcher():
	Error = 1 # 上下边框容错
	Shift = 15 # 留边高度
	Font = 1 #是否加入字体
	Length = 0 #第一句话的判定长度
	Detect_Question_Content_Length = False
	File_Storage = 'E:/0Mofish/PDF/Table-17/All-MCQ-Raw-PDF/svgdump'
	if not os.path.exists(File_Storage):
		os.makedirs(File_Storage)
	Product_Storage = './B-Product'
	if not os.path.exists(Product_Storage):
		os.makedirs(Product_Storage)
	Bug_Storage = './B-Bug'
	if not os.path.exists(Bug_Storage):
		os.makedirs(Bug_Storage)
	
	Log = open('./B-Log.txt', 'w')
	File_List = []
	Start_Time = time.perf_counter()
	print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '---Start')

	for _, _, files in os.walk(File_Storage, topdown=True): # root dirs files
		for name in files:
			if re.match('.*(.svg)', os.path.join(name)) is not None:
				File_List.append(os.path.join(name))
	Index = 0
	PRINT('-', 1)
	for Root in File_List:
		if Index % 500 == 0:
			Print_Time(Start_Time, Index, len(File_List))
		#print('#', end='')
		if Root[-6 :-4] == '-1':
			continue
		Log.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '---Process file: ' + Root + '\n')
		Log.flush()
		File = open(File_Storage + '/' + Root, 'r', encoding='utf-8').read()
		
		Data = Locate_Questions(File, Length, Detect_Question_Content_Length)
		#print('a')
		if Data == None:
			continue
		if len(Data["Location_List"]) >= 9:
			Log.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '---BUG>>>' + Root + '<<< Too many question\n')
			Log.flush()
			Bug_File_Copier(Root, File_Storage, Bug_Storage)
		if len(Data["Location_List"]) <= 1:
			Log.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '---BUG>>>' + Root + '<<< No question\n')
			Log.flush()
			Bug_File_Copier(Root, File_Storage, Bug_Storage)
			continue
		Location = 0
		while Location <= len (Data["Location_List"]) - 2:
			try:
				Top = float(Data["Location_List"][Location])
				Bottom = float(Data["Location_List"][Location + 1])
				Content = Separate(File, Top, Bottom, Error, Font)
				if Content == None:
					Location += 1
					continue

				Location_1 = Root.find('-')
				Paper_Name = Root[0 : Location_1]

				Product = open(Product_Storage + '/' + Paper_Name + '@' + Data["Question_Number_List"][Location] + '.svg', 'w', encoding='utf-8')
				Product.write('<svg:svg xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:svg="http://www.w3.org/2000/svg" version="1.1">')
				Product.write('<svg:g transform="translate(0, -' + str(Top - Shift) + ')">')
				Product.flush()
				Product.write(Content)
				Product.write('</svg:g>')
				Product.write('</svg:svg>')
				Product.flush()
			except:
				Log.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '---BUG>>>' + Root)
				Log.flush()
			Location += 1
		Index += 1
	print('Done')

def Print_Time(Start_Time, Index, Max_Index):
	os.system('cls')
	PRINT('Start time ' + str(round(Start_Time, 2)) + ' ', 1)
	PRINT('Time taken ' + str(round(time.perf_counter() - Start_Time, 2)) + ' ', 1)
	PRINT('Processed ' + str(Index) + ' files (' + str(round(Index * 100 / Max_Index, 0)) + '%)', 1)
	if Index == 0:
		pass
	else:
		PRINT('Average time left: ' + str(round(((time.perf_counter() - Start_Time) / Index) * (Max_Index - Index), 1)) + 's', 1)

def Separate(File, Top, Bottom, Error, Font):
	Location_1 = 0
	Content = ''
	if Font == 1:
		Location_2 = File.find('<svg:defs')
		Location_3 = File.find('</svg:defs')
		Content = File[Location_2 : Location_3] + '</svg:defs>'
	while 1:
		#print(Location_1)
		Action = 0
		Location_1 = File.find('<', Location_1, len(File) - 1)
		if Location_1 == -1:
			return Content

		if File[Location_1 : Location_1 + 7] == '<svg:g ':
			Location_2 = File.find('>', Location_1)
			Content = Content + File[Location_1 : Location_2 + 1]
			Location_1 += 1
			Action = 1

		if File[Location_1 : Location_1 + 7] == '</svg:g':
			Location_2 = File.find('>', Location_1)
			Content = Content + File[Location_1 : Location_2 + 1]
			Location_1 += 1
			Action = 1

		if File[Location_1 : Location_1 + 9] == '<svg:text':
			Location_2 = File.find('>', Location_1)
			Content = Content + File[Location_1 : Location_2 + 1]
			Location_1 += 1
			Action = 1

		if File[Location_1 : Location_1 + 10] == '</svg:text':
			Location_2 = File.find('>', Location_1)
			Content = Content + File[Location_1 : Location_2 + 1]
			Location_1 += 1
			Action = 1

		if File[Location_1 : Location_1 + 10] == '<svg:tspan':
			Location_2 = File.find(" y=", Location_1)
			Location_3 = File.find('"', Location_2)
			Location_4 = File.find('"', Location_3 + 1)
			Coordinate = File[Location_3 + 1 : Location_4]
			Coordinate_Content = Extract_Real_Coordinate_Y(File, Coordinate, Location_1 - 1)
			Coordinate = Coordinate_Content["Y"]
			if Coordinate_Content["Safe"] == 1:
				return None
			if Coordinate >= Top - Error and Coordinate < Bottom - Error:
				Location_2 = File.find('>', Location_1)
				Location_2 = File.find('>', Location_2 + 1)
				Content = Content + File[Location_1 : Location_2 + 1]
				Action = 1
			Location_1 += 1
		
		if File[Location_1 : Location_1 + 10] == '<svg:image':
			Location_2 = File.find(" y=", Location_1)
			Location_3 = File.find('"', Location_2)
			Location_4 = File.find('"', Location_3 + 1)
			Coordinate = File[Location_3 + 1 : Location_4]
			
			Location_3 = File.find('<', Location_1 + 1)

			Coordinate_Content = Extract_Real_Coordinate_Y(File, Coordinate, Location_3 - 1)
			Coordinate = Coordinate_Content["Y"]
			if Coordinate_Content["Safe"] == 1:
				return None
			if Coordinate >= Top - Error and Coordinate < Bottom - Error:
				Location_2 = File.find('>', Location_1)
				Location_2 = File.find('>', Location_2 + 1)
				Content = Content + File[Location_1 : Location_2 + 1]
				Action = 1
			Location_1 += 1	

		if File[Location_1 : Location_1 + 9] == '<svg:path':
			Location_2 = File.find(" d=", Location_1)
			Location_3 = File.find('"', Location_2)
			Location_4 = File.find('"', Location_3 + 1)
			Coordinate = File[Location_3 + 1 : Location_4]
			Data = Path(Coordinate)
			Minimun = Extract_Real_Coordinate_Y(File, Data["Minimun"], Location_2)
			Maximun = Extract_Real_Coordinate_Y(File, Data["Maximun"], Location_2)
			if Minimun["Safe"] == 1 or Maximun["Safe"] == 1:
				return None
			if Minimun["Y"] >= (Top - Error) and Maximun["Y"] <= (Bottom + Error):
				Location_2 = File.find('>', Location_1)
				Location_2 = File.find('>', Location_2 + 1)
				Content = Content + File[Location_1 : Location_2 + 1]
				Action = 1
			Location_1 += 1

		if Action == 0 and Location_1 != -1:
			Location_1 += 1

def Space_Eliminator(Name):  # 在使用系统cmd复制bug文件的时候，会牵扯到路径。指令中的路径不能直接有空格。这个def的作用是在相关的地方加上""
	Name_Storage_1 = ''
	Name_Storage_2 = ''

	Inner_Inspector_Location = 0
	while Inner_Inspector_Location <= len(Name) - 1:
		if Name[Inner_Inspector_Location] == '/':
			Name_Storage_1 = Name_Storage_1 + '\\'
			Inner_Inspector_Location += 1
		if Inner_Inspector_Location <= len(Name) - 1:
			Name_Storage_1 = Name_Storage_1 + Name[Inner_Inspector_Location]
			Inner_Inspector_Location += 1

	Inner_Inspector_Location = 0
	while Inner_Inspector_Location <= len(Name_Storage_1) - 1:
		if Name_Storage_1[Inner_Inspector_Location] == ' ':
			Space_Check = 1
			while Space_Check:
				if Name_Storage_1[Inner_Inspector_Location] == '\\':
					Inner_Inspector_Location += 1
					Name_Storage_2 = Name_Storage_1[:
													Inner_Inspector_Location] + '"'
					while 1:
						if Inner_Inspector_Location >= len(Name_Storage_1):
							Space_Check = 0
							break
						if Name_Storage_1[Inner_Inspector_Location] == '\\':
							Name_Storage_2 = Name_Storage_2 + '"\\'
							Inner_Inspector_Location += 1
							Space_Check = 0
							break
						Name_Storage_2 = Name_Storage_2 + \
							Name_Storage_1[Inner_Inspector_Location]
						Inner_Inspector_Location += 1
				if Space_Check == 1:
					Inner_Inspector_Location += -1
		if Inner_Inspector_Location <= len(Name_Storage_1) - 1:
			Name_Storage_2 = Name_Storage_2 + \
				Name_Storage_1[Inner_Inspector_Location]
			Inner_Inspector_Location += 1
	return(Name_Storage_2)

def Bug_File_Copier(Root, File_Storage, Bug_Storage):  # 将有问题的文件复制到BugFile文件夹内
	pass
	# Service_Type = 0
	# Command_Storage = ''
	# Bug = Space_Eliminator(Bug_Storage + '/' + Root)
	# File = Space_Eliminator(File_Storage + '/' + Root)
	# if Service_Type == 0:
	# 	Command_Storage = 'copy ' + File + ' ' + Bug
	# 	os.system(Command_Storage)
	# if Service_Type == 1:
	# 	Command_Storage = 'cp ' + File + ' ' + Bug
	# 	os.system(Command_Storage)

def Locate_Questions(File, Length, Length_Check):
	Location_1 = 0
	Location_List = []
	Question_Number_List = []
	Special_Treatment = {
		'©':0,
		'Permission':0,
		'BLANK PAGE':0
	}
	while 1:
		Location_1 = File.find('<svg:tspan', Location_1) #-----------------< 题号码检测
		if Location_1 == -1:
			return {"Location_List": sorted(Location_List), "Question_Number_List": Question_Number_List}
		Location_2 = File.find('font-family',Location_1)
		Location_3 = File.find('"', Location_2)
		Location_4 = File.find('"', Location_3 + 1)
		Font_Family_1 = File[Location_3 + 1 : Location_4]

		Location_2 = File.find(' x="', Location_1) + 4
		Location_3 = File.find('"', Location_2)
		Coordinates_Storage = File[Location_2 : Location_3].split(' ')
		Content = Extract_Real_Coordinate_X(File, Coordinates_Storage[0], Location_1)
		X = Content["X"]
		if X > 49.9 or X < 45:
			Location_1 += 1
			continue

		Location_2 = File.find(">", Location_1)
		Location_3 = File.find("<", Location_2)
		Content = File[Location_2 + 1 : Location_3]
		Feedback = Edge_Detection(File, Content, Special_Treatment, Location_1)
		if Feedback["Safe"] == 0:
			return None
		if Feedback['Action'] == 1:
			Special_Treatment["©"] = 1
			Special_Treatment["Permission"] = 1
			Location_List.append(Feedback["Coordinate"])
			Location_1 += -1
			continue
		if Feedback['Action'] == 2:
			return None		
		Question_Number = re.sub(r'[\s]', '', Content)
		try:
			if int(Question_Number) > 40:
				Location_1 += 1
				continue
			if not Question_Number.isdigit():
				Location_1 += 1
				continue
		except:
			Location_1 += 1
			continue


		Location_2 = File.find('<svg:tspan', Location_3) #-----------------< 题目检测
		Location_3 = File.find('>', Location_2)
		Location_4 = File.find('<', Location_3)
		Content = File[Location_3 + 1 : Location_4]
		Feedback = Edge_Detection(File, Content, Special_Treatment, Location_1)
		if Feedback["Safe"] == 0:
			return None
		if Feedback['Action'] == 1:
			Special_Treatment["©"] = 1
			Special_Treatment["Permission"] = 1
			Location_List.append(Feedback["Coordinate"])
			Location_1 += -1
			continue
		if Feedback['Action'] == 2:
			return None	

		Location_2 = File.find('font-family',Location_2)
		Location_3 = File.find('"', Location_2)
		Location_4 = File.find('"', Location_3 + 1)
		Font_Family_2 = File[Location_3 + 1 : Location_4]
		if Font_Family_1 == Font_Family_2:
			if Font_Family_1 != 'Helvetica':
				Location_1 += 1
				continue
		

		if Length_Check:
			if len(re.sub(r'[\s]', '', Content)) <= Length:
				Location_1 += 1
				continue


		Question_Number_List.append(Question_Number)
		Location_2 = File.find(' y="', Location_1)
		Location_3 = File.find('"', Location_2)
		Location_4 = File.find('"', Location_3 + 1)
		Coordinate = File[Location_3 + 1 : Location_4]
		Content = Extract_Real_Coordinate_Y(File, Coordinate, Location_1)
		Coordinate = Content["Y"] - 5
		if Content["Safe"] >= 15:
			return None
		Location_List.append(Coordinate)
		Location_1 += 1

def Extract_Real_Coordinate_Y(File, Coordinate, Location):
	Y = float(Coordinate)
	Location_1 = Location
	Tag_List = []
	Used_Tag = []
	Matrix_Count = 0
	while 1:
		Location_1 = File.rfind('<', 0, Location_1)
		if Location_1 == -1 or Location_1 == 0:
			#print(Used_Tag)
			return {"Y": round(Y, 4), "Safe": Matrix_Count}
		if File[Location_1 + 1] == '/':
			Location_2 = File.find('>', Location_1)
			Tag_List.append(File[Location_1 + 2 : Location_2])
			Location_1 += -1
			continue
		Location_2 = File.find(' ', Location_1)
		if File[Location_1 + 1 : Location_2] in Tag_List:
			Location_2 = Tag_List.index(File[Location_1 + 1 : Location_2])
			del Tag_List[Location_2]
			Location_1 += -1
			continue
		

		Location_2 = File.find('>', Location_1)
		Trans_Location = File.find(' transform="', Location_1, Location_2)
		if Trans_Location == -1:
			Location_1 += -1
			continue

		Location_2 = File.find(' ', Location_1)
		Used_Tag.append(File[Location_1 + 1 : Location_2])

		Location_3 = File.find('"', Trans_Location)
		Location_4 = File.find('"', Location_3 + 1)
		Transform_Content = File[Location_3 + 1 : Location_4]

		if Transform_Content.find('scale') != -1:
			Location_2 = Transform_Content.find('scale')
			Location_3 = Transform_Content.find('(', Location_2)
			Location_4 = Transform_Content.find(')', Location_3)
			Scale_Content = re.sub(r',','',Transform_Content[Location_3 + 1 : Location_4]).split(' ')
			Y = Y * float(Scale_Content[-1])

		if Transform_Content.find('translate') != -1:
			Location_2 = Transform_Content.find('translate')
			Location_3 = Transform_Content.find('(', Location_2)
			Location_4 = Transform_Content.find(')', Location_3)
			Scale_Content = re.sub(r',','',Transform_Content[Location_3 + 1 : Location_4]).split(' ')
			Y = Y + float(Scale_Content[-1])

		if Transform_Content.find('matrix') != -1:
			Location_2 = Transform_Content.find('matrix')
			Location_3 = Transform_Content.find('(', Location_2)
			Location_4 = Transform_Content.find(')', Location_3)
			Matrix_Content = Transform_Content[Location_3 + 1 : Location_4].split(' ')
			if Matrix_Content[1] == '0' and Matrix_Content[2] == '0':
				Y = Y * float(Matrix_Content[3])
			else:
				Matrix_Count += 1
			Y = Y + float(Matrix_Content[5])	
		Location_1 += -1

def Extract_Real_Coordinate_X(File, Coordinate, Location):
	X = float(Coordinate)
	Location_1 = Location
	Tag_List = []
	Used_Tag = []
	Matrix_Count = 0
	while 1:
		Location_1 = File.rfind('<', 0, Location_1)
		if Location_1 == -1 or Location_1 == 0:
			#print(Used_Tag)
			return {"X": round(X , 4), "Safe": Matrix_Count}
		if File[Location_1 + 1] == '/':
			Location_2 = File.find('>', Location_1)
			Tag_List.append(File[Location_1 + 2 : Location_2])
			Location_1 += -1
			continue
		Location_2 = File.find(' ', Location_1)
		if File[Location_1 + 1 : Location_2] in Tag_List:
			Location_2 = Tag_List.index(File[Location_1 + 1 : Location_2])
			del Tag_List[Location_2]
			Location_1 += -1
			continue
		

		Location_2 = File.find('>', Location_1)
		Trans_Location = File.find(' transform="', Location_1, Location_2)
		if Trans_Location == -1:
			Location_1 += -1
			continue

		Location_2 = File.find(' ', Location_1)
		Used_Tag.append(File[Location_1 + 1 : Location_2])

		Location_3 = File.find('"', Trans_Location)
		Location_4 = File.find('"', Location_3 + 1)
		Transform_Content = File[Location_3 + 1 : Location_4]

		if Transform_Content.find('scale') != -1:
			Location_2 = Transform_Content.find('scale')
			Location_3 = Transform_Content.find('(', Location_2)
			Location_4 = Transform_Content.find(')', Location_3)
			Scale_Content = re.sub(r',','',Transform_Content[Location_3 + 1 : Location_4]).split(' ')
			X = X * float(Scale_Content[0])

		if Transform_Content.find('translate') != -1:
			Location_2 = Transform_Content.find('translate')
			Location_3 = Transform_Content.find('(', Location_2)
			Location_4 = Transform_Content.find(')', Location_3)
			Scale_Content = re.sub(r',','',Transform_Content[Location_3 + 1 : Location_4]).split(' ')
			X = X + float(Scale_Content[0])

		if Transform_Content.find('matrix') != -1:
			Location_2 = Transform_Content.find('matrix')
			Location_3 = Transform_Content.find('(', Location_2)
			Location_4 = Transform_Content.find(')', Location_3)
			Matrix_Content = Transform_Content[Location_3 + 1 : Location_4].split(' ')
			if Matrix_Content[1] == '0' and Matrix_Content[2] == '0':
				X = X * float(Matrix_Content[0])
			else:
				Matrix_Count += 1
			X = X + float(Matrix_Content[4])	
		Location_1 += -1

def Edge_Detection(File, Content, Book, Location):
	Action = 0
	Safe = 1
	Location_1 = Location
	if Content.find('©') != -1 and Book['©'] == 0:
		Book['©'] = 1
		Action = 1
	if Content.find('Permission') != -1 and Book['Permission'] == 0:
		Book['Permission'] = 1
		Action = 1
	if Content.find('BLANK PAGE') != -1 and Book['BLANK PAGE'] == 0:
		Book['BLANK PAGE'] = 1
		Action = 2
	
	if Action == 1:
		Location_2 = File.find(' y="', Location_1)
		Location_3 = File.find('"', Location_2)
		Location_4 = File.find('"', Location_3 + 1)
		Coordinate = File[Location_3 + 1 : Location_4]
		Content = Extract_Real_Coordinate_Y(File, Coordinate, Location_1)
		Coordinate = Content["Y"] - 5
		if Content["Safe"] >= 15:
			Safe = 0
		return {"Action": 1, "Coordinate": Coordinate, "Safe": Safe}
	if Action == 2:
		return {"Action": 2, "Safe": Safe}
	return {"Action": 0, "Safe": Safe}

def Path(Data):
	Data = re.sub(r'[A-Z]','', Data).split(' ')
	while ' ' in Data:
		Location = Data.index(' ')
		del Data[Location]
	while '' in Data:
		Location = Data.index('')
		del Data[Location]
	Location = 1
	Minimun = 99999999999999999
	Maximun = 0
	while Location <= len(Data) - 1:
		if float(Data[Location]) < float(Minimun):
			Minimun = Data[Location]
		if float(Data[Location]) > float(Maximun):
			Maximun = Data[Location]
		Location += 2
	return {"Minimun": round(float(Minimun), 4), "Maximun": round(float(Maximun), 4)}

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


Launcher()

