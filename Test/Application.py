import os, re

def Locate_Questions(File):
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

		Location_2 = File.find(">", Location_1)
		Location_3 = File.find("<", Location_2)
		Content = File[Location_2 + 1 : Location_3]
		Feedback = Edge_Detection(File, Content, Special_Treatment, Location_1)
		if Feedback['Action'] == 1:
			Special_Treatment["©"] = 1
			Special_Treatment["Permission"] = 1
			Location_List.append(Feedback["Coordinate"])
			Location_1 += -1
			continue
		if Feedback['Action'] == 2:
			return None		
		Question_Number = re.sub(r'[\s]', '', Content)
		if not Question_Number.isdigit():
			Location_1 += 1
			continue


		Location_2 = File.find('<svg:tspan', Location_3) #-----------------< 题目检测
		Location_3 = File.find('>', Location_2)
		Location_4 = File.find('<', Location_3)
		Content = File[Location_3 + 1 : Location_4]
		Feedback = Edge_Detection(File, Content, Special_Treatment, Location_1)
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
				Location_1 = Location_2 + 1
				continue
		

		if len(re.sub(r'[\s]', '', Content)) <= 15:
			Location_1 = Location_2 + 1
			continue

		if len(re.sub(r'[\s]', '', Content)) != 0:
			Question_Number_List.append(Question_Number)
		Location_5 = Location_3
		Location_2 = File.find(' y="', Location_1)
		Location_3 = File.find('"', Location_2)
		Location_4 = File.find('"', Location_3 + 1)
		Coordinate = File[Location_3 + 1 : Location_4]
		Coordinate = Extract_Real_Coordinate(File, Coordinate, Location_1)
		Location_List.append(Coordinate)
		Location_1 = Location_5

def Extract_Real_Coordinate(File, Coordinate, Location):
	Y = float(Coordinate)
	Location_1 = Location
	Tag_List = []
	Used_Tag = []
	while 1:
		Location_1 = File.rfind('<', 0, Location_1)
		if Location_1 == -1 or Location_1 == 0:
			#print(Used_Tag)
			return round(Y, 4)
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
			print(Matrix_Content)
			if Matrix_Content[1] == '0' and Matrix_Content[2] == '0':
				Y = Y * float(Matrix_Content[3])
			Y = Y + float(Matrix_Content[5])	
		Location_1 += -1
	

def Edge_Detection(File, Content, Book, Location):
	#print(Content)
	Action = 0
	Location_1 = Location
	# if Content.find('UCLES') != -1 and Book['©'] == 0:
	# 	Book['©'] = 1
	# 	Action = 1
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
		Coordinate = Extract_Real_Coordinate(File, Coordinate, Location_1) - 5
		return {"Action": 1, "Coordinate": Coordinate}
	if Action == 2:
		return {"Action": 2}
	return {"Action": 0}

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

def Separate(File, Top, Bottom, Error):
	Location_1 = 0
	Content = ''
	while 1:
		#print(Location_1)
		Action = 0
		Location_1 = File.find('<', Location_1)
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
			Coordinate = Extract_Real_Coordinate(File, Coordinate, Location_1 - 1)
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
			Data["Minimun"] = Extract_Real_Coordinate(File, Data["Minimun"], Location_2)
			Data["Maximun"] = Extract_Real_Coordinate(File, Data["Maximun"], Location_2)
			#print(Data)
			if float(Data["Minimun"]) >= (Top - Error) and float(Data["Maximun"]) <= (Bottom + Error):
				Location_2 = File.find('>', Location_1)
				Location_2 = File.find('>', Location_2 + 1)
				Content = Content + File[Location_1 : Location_2 + 1]
				Action = 1
			Location_1 += 1

		if Action == 0:
			Location_1 += 1

def Launcher():
	Error = 1
	File = open('./test.svg', 'r', encoding='utf-8').read()
	print(Locate_Questions(File))
	Data = Locate_Questions(File)
	a = float(Data["Location_List"][1])
	b = float(Data["Location_List"][2])
	Content = Separate(File, a, b, Error)
	Log = open('./1.svg', 'w', encoding='utf-8')
	Log.write('<svg:svg xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:svg="http://www.w3.org/2000/svg" version="1.1">')
	Log.flush()
	Log.write(Content)
	Log.write('</svg:svg>')
	Log.flush()
	
	print('Done')

Launcher()
