import os, re, json

def Launcher():
	File_Location = './Files'
	Files = Get_File_List(File_Location)
	Answer = {}
	for File in Files:
		File_Content = open(File_Location + '/' + File, 'r', encoding='utf-8').read()
		# if File_Content.find('Teachers’ version') != -1 or File_Content.find('Number') != -1:
		# 	Answer[File[0: -5]] = Find_Answer_Ver_2(File_Content)
		# else:
		# 	Answer[File[0: -5]] = Find_Answer_Ver_1(File_Content)
		# if int(File[6 : 8]) >= 17:
		# 	Answer_Storage = Method_1(File_Content)
		# 	if len(Answer_Storage) < 30:
		# 		Answer_Storage = Find_Answer_Ver_2(File_Content)
		# 	Answer[File[0: -5]] = Answer_Storage
		# else:
		# 	Answer_Storage = Method_3(File_Content)
		# 	if len(Answer_Storage) < 30:
		# 		Answer_Storage = Find_Answer_Ver_2(File_Content)
		# 		if len(Answer_Storage) < 30:
		# 			Answer_Storage = Method_1(File_Content)
		# 	Answer[File[0: -5]] = Answer_Storage
		Answer[File[0: -5]] = Method_Switcher(File_Content, File)
	Log = open('./log.json', 'w')
	Log.write(json.dumps(Answer))
	Log.flush()
	print(Answer)
	print('Done')

def Method_Switcher(File_Content, File):
		Answer_Storage = Method_1(File_Content)
		if len(Answer_Storage) >= 35:
			Answer_Storage["method"] = "method 1"
			return Answer_Storage
		# Answer_Storage = Method_2(File_Content)
		# if len(Answer_Storage) >= 35:
		# 	Answer_Storage["method"] = "method 2"
		# 	return Answer_Storage
		Answer_Storage = Method_3(File_Content)
		if len(Answer_Storage) >= 35:
			Answer_Storage["method"] = "method 3"
			return Answer_Storage
		Answer_Storage = Method_4(File_Content)
		Answer_Storage["method"] = "method 4"
		return Answer_Storage

def Get_File_List(File_Position):
	Files = []
	for root, dirs, files in os.walk(File_Position, topdown=True):
		for name in files:
			if name.find('.html') != -1:
				Files.append(os.path.join(name))
	return Files

def Find_Answer_Ver_2(File):
	Answer = Method_1(File)
	# Answer = Method_2(File)
	if len(Answer) < 30:
		Answer = Method_2(File)
		# Answer = Method_1(File)
	return Answer

def Method_1(File): #10
	Answer_List = {}
	File_Length = len(File) - 1
	Location_1 = 0
	while Location_1 <= File_Length:
		Location_1 = File.find('<div', Location_1)
		if Location_1 == -1:
			break
		Location_1_B = File.find('</div', Location_1)
		Content_Q = Tag(File, Location_1, 1)
		if not Content_Q.isdigit:
			Location_1 += 1
			continue
		Location_2 = File.find('<span', Location_1, Location_1_B)
		if Location_2 == -1:
			Location_1 += 1
			continue
		Location_2 = File.find('<span', Location_2 + 1, Location_1_B)
		if Location_2 == -1:
			Location_1 += 1
			continue
		Location_2 = File.find('>', Location_2, Location_1_B)
		Location_3=File.find('<', Location_2, Location_1_B)
		Content_A = File[Location_2 + 1 : Location_3].replace(' ', '')
		if not Content_A.isalpha() or len(Content_A) > 1:
			Location_1 += 1
			continue
		Answer_List[Content_Q] = Content_A

		Location_2 = File.find('<span', Location_3 + 1)
		Location_2 = File.find('>', Location_2)
		Location_3 = File.find('<', Location_2)
		Content_Q = File[Location_2 + 1 : Location_3].replace(' ', '')
		
		Location_2 = File.find('<span', Location_3 + 1)
		Location_2 = File.find('>', Location_2)
		Location_3 = File.find('<', Location_2)
		Content_A = File[Location_2 + 1 : Location_3].replace(' ', '')
		if not Content_A.isalpha() or len(Content_A) > 1:
			Location_1 += 1
			continue
		Answer_List[Content_Q] = Content_A 
		Location_1 += 1
		
	return Answer_List

def Method_2(File):
	Answer_List = {}
	File_Length = len(File) - 1
	Location_1 = -1
	while Location_1 <= File_Length:
		Location_1 = File.find('<div', Location_1 + 1)
		if Location_1 == -1:
			break
		Content_Q = Tag(File, Location_1, 1).replace(' ', '')
		# Pinput(Content_Q)
		if not Content_Q.isdigit():
			Location_1 += 1
			continue
		Location_1 = File.find('<div', Location_1 + 1)
		Content_A = Tag(File, Location_1, 1).replace(' ', '')
		if not Content_A.isalpha() or not len(Content_A) == 1:
			Location_1 += 1
			continue
		Answer_List[Content_Q] = Content_A
		Location_1 = File.find('<div', Location_1 + 1)
	return Answer_List

def Method_3(File):
	# Pinput("Method 3")
	Answer_List = {}
	File_Length = len(File) - 1
	Location_1 = -1
	while Location_1 <= File_Length:
		Location_1 = File.find('<div', Location_1 + 1)
		if Location_1 == -1:
			break
		Content_Q = Tag(File, Location_1, 1)
		# Pinput("Content_Q " + Content_Q)
		if not Content_Q.isdigit():
			continue
		# Pinput('----')
		Location_1 = File.find('<div', Location_1 + 1)
		Content_A = Tag(File, Location_1, 1)
		# Pinput("Content_A " + Content_A)
		if not Content_A.isalpha() or not len(Content_A) == 1:
			continue
		# Pinput('#####')
		Answer_List[Content_Q] = Content_A
	return Answer_List

# def Method_4(File):
# 	Location_1 = 0
# 	File_Length = len(File) - 1
# 	Answer_List = {}
# 	while Location_1 <= File_Length:
# 		Location_1 = File.find('<div', Location_1)
# 		if Location_1 == -1:
# 			break
# 		Location_2 = File.find('>', Location_1 + 1)
# 		Location_3 = File.find('<', Location_2 + 1)
# 		Content = File[Location_2 + 1 : Location_3].split(' ')
# 		# Pinput(Content)
# 		if len(Content) >= 2:
# 			if Content[0].isdigit():
# 				if Content[1].isalpha() and len(Content[1]) == 1:
# 					Answer_List[Content[0]] = Content[1]
# 		if len(Content) == 1:
# 			if str(Content[0]) == '1':
# 				Location_2 = File.find('</div', Location_1)
# 				Content = File[Location_1 : Location_2]
# 				if Content.find('A </span>') != 0:
# 					Answer_List['1'] = 'A'
# 				if Content.find('B </span>') != 0:
# 					Answer_List['1'] = 'B'
# 				if Content.find('C </span>') != 0:
# 					Answer_List['1'] = 'C'
# 				if Content.find('D </span>') != 0:
# 					Answer_List['1'] = 'D'
# 		Location_1 += 1
# 	return Answer_List

def Method_4(File):
	Location_1 = 0
	File_Length = len(File) - 1
	Answer_List = {}
	while Location_1 <= File_Length:
		Location_1 = File.find('<div', Location_1)
		if Location_1 == -1:
			break
		Location_2 = File.find('>', Location_1 + 1)
		Location_3 = File.find('<', Location_2 + 1)
		Content = File[Location_2 + 1 : Location_3].split(' ')
		# Pinput(Content)
		if len(Content) >= 2:
			if Content[0].isdigit():
				if Content[1].isalpha() and len(Content[1]) == 1:
					Answer_List[Content[0]] = Content[1]
		# if len(Content) == 1:
		# 	if str(Content[0]) == '1':
		# 		Location_2 = File.find('</div', Location_1)
		# 		Content = File[Location_1 : Location_2]
		# 		if Content.find('A </span>') != 0:
		# 			Answer_List['1'] = 'A'
		# 		if Content.find('B </span>') != 0:
		# 			Answer_List['1'] = 'B'
		# 		if Content.find('C </span>') != 0:
		# 			Answer_List['1'] = 'C'
		# 		if Content.find('D </span>') != 0:
		# 			Answer_List['1'] = 'D'
		Location_1 += 1
	return Answer_List


def Tag(File, Location, Type):
	if Type == 0:
		Location_A = File.find('>', Location)
		return Location_A
	if Type == 1:
		Location_A = File.find('>', Location)
		Location_B = File.find('<', Location_A)
		Content = File[Location_A + 1 : Location_B].replace(' ', '')
		return Content

def Pinput(content):
	# pass
	print(content)
	input()

Launcher()
