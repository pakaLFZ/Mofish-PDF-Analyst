import os, sys, re

def Launcher():
	fileLocation = "E:/0Mofish/PDF/Table-14_Q/Mofish-PDF-Analyst/New Version/Spliter/Product-0608"
	productLocation = "./product"
	File_List = Get_File_List(fileLocation)

	if not os.path.exists(fileLocation):
		os.makedirs(fileLocation)
	if not os.path.exists(productLocation):
		os.makedirs(productLocation)

	PRINT('>', 0)
	Location = 0
	while Location <= len(File_List) - 1:
		if Location % 500 == 0:
			PRINT('-', 0)
		File_Content = open(fileLocation + '/' + File_List[Location], 'r', encoding="utf-8").read()
		File_Content = locateText(File_Content)
		Product = open(productLocation + "/" + File_List[Location], "w", encoding="utf-8")
		Product.write(File_Content)
		Product.flush()
		Location += 1
	PRINT('', 1)
	print("done")

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

def locateText(svg):
	location_1 = 0
	fileLength = len(svg) - 1
	content = ""
	while location_1 <= fileLength:
		location_2 = svg.find("<svg:tspan", location_1)
		if location_2 == -1:
			content += svg[location_1 :]
			return content
		location_3 = svg.find(" x=", location_2)
		location_4 = svg.find('"', location_3 + 4)
		xCoordinates = svg[location_3 + 4 : location_4]

		location_5 = svg.find(">", location_2)
		location_6 = svg.find("<", location_5 + 1)
		text = svg[location_5 + 1 : location_6]
		if len(text) == 0:
			content += svg[location_1 : location_6]
			location_1 = location_6
			continue
		if text[0] == " ":
			location_7 = xCoordinates.find(" ")
			xCoordinates = xCoordinates[location_7 + 1 : ]
			text = text[1 : ]
		
		content += svg[location_1 : location_3 + 4]
		content += xCoordinates
		content += svg[location_4 : location_5 + 1]
		content += text
		location_1 = location_6
Launcher()
		


		
