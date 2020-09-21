import re, os, json

def GetFileList(location):
    fileList = []
    for _, _, files in os.walk(location, topdown=True): # root dirs files
        for name in files:
            if re.match('.*(.svg)', os.path.join(name)) is not None:
                fileList.append(os.path.join(name))
    return fileList

def Launcher():
    print("start")
    if not os.path.exists("./data.json"):
        data = open("./data.json", "w")
        data_storage = DATA()
        data_storage = json.dumps(data_storage)
        data.write(data_storage)
        data.flush()
    data = open("./data.json", "r").read()
    data = json.loads(data)
    targetLocation = data["targetLocation"]
    fileList = GetFileList(targetLocation)
    paperNameList = PaperNameList(fileList)
    Merger(data, paperNameList, fileList)
    print("finished")

def PaperNameList(fileList):
    paperNameList = []
    for item in fileList:
        name = item[ : item.find("@") ]
        if not name in paperNameList:
            paperNameList.append(name)
    return paperNameList

def Merger(data, paperNameList, fileList):
    pageLength = data["pageLength"]
    source = data["source"]
    questionGroup = data["questionGroup"]
    fileLocation = data["targetLocation"]
    productLocation = data["productLocation"]
    svgHeader = data["svgHeader"]
    svgTail = data["svgTail"]
    initalPageLength = data["initialPageLength"]
    levelofshift_Y = data["shiftY"]
    levelofshift_X = data["shiftX"]
    shift = '<svg:g transform="translate(0, {height})">'
    questionName = '<svg:g transform="translate({width}, {height})"><svg:text font-size= "15px" font-weight="bold">{name}</svg:text></svg:g>'

    if not os.path.exists(fileLocation):
        os.makedirs(fileLocation)
    if not os.path.exists(productLocation):
        os.makedirs(productLocation)

    targetBank = RearrangeFileList(fileList)

    for group in questionGroup:
        groupName = group[0]
        start = group[1]
        end = group[2]
        groupLocation = productLocation + "/" + groupName

        pageNo = 0
        currentPageLength = initalPageLength
        outputData = ""

        if not os.path.exists(groupLocation):
            os.makedirs(groupLocation)
        
        for question in targetBank:
            # PINPUT(question)
            questionNo = question[
                question.find("@") + 1:
                question.find(".")
            ]

            if int(questionNo) >= start and int(questionNo) <= end:
                questionLocation = fileLocation + '/' + question
                File = open(questionLocation, 'r', encoding="utf-8").read()
                FileHeight = MeasureHeight(File)

                
                if currentPageLength + FileHeight + 5 * levelofshift_Y > pageLength:
                    pageLocation = groupLocation + "/" + str(pageNo) + ".svg"
                    pageOutput = open(pageLocation, "w", encoding="utf-8")
                    svgOutput = svgHeader + outputData + svgTail
                    pageOutput.write(svgOutput)
                    pageOutput.flush()
                    pageOutput.close()

                    pageNo += 1
                    currentPageLength = initalPageLength
                    outputData = ""

                questionData = ExtractQuestionData(File)
                name = ExtractQuestionName(question)
                if source:
                    outputData += questionName.format(width=levelofshift_X, height=currentPageLength + 2 * levelofshift_Y, name=name)
                outputData += shift.format(height=currentPageLength + 3 * levelofshift_Y) + questionData + "</svg:g>"
                currentPageLength += FileHeight + 5 * levelofshift_Y

        if len(outputData) != 0:
            pageLocation = groupLocation + "/" + str(pageNo) + ".svg"
            pageOutput = open(pageLocation, "w", encoding="utf-8")
            svgOutput = svgHeader + outputData + svgTail
            pageOutput.write(svgOutput)
            pageOutput.flush()
            pageOutput.close()

def Extract_Real_Coordinate(File, coordinate, location):
    Y = float(coordinate)
    location_1 = location
    Tag_List = []
    Used_Tag = []
    Matrix_Count = 0
    while 1:
        location_1 = File.rfind('<', 0, location_1)
        if location_1 == -1 or location_1 == 0:
            #print(Used_Tag)
            return Y
        if File[location_1 + 1] == '/':
            location_2 = File.find('>', location_1)
            Tag_List.append(File[location_1 + 2 : location_2])
            location_1 += -1
            continue
        location_2 = File.find(' ', location_1)
        if File[location_1 + 1 : location_2] in Tag_List:
            location_2 = Tag_List.index(File[location_1 + 1 : location_2])
            del Tag_List[location_2]
            location_1 += -1
            continue
        

        location_2 = File.find('>', location_1)
        Trans_location = File.find(' transform="', location_1, location_2)
        if Trans_location == -1:
            location_1 += -1
            continue

        location_2 = File.find(' ', location_1)
        Used_Tag.append(File[location_1 + 1 : location_2])

        location_3 = File.find('"', Trans_location)
        location_4 = File.find('"', location_3 + 1)
        Transform_Content = File[location_3 + 1 : location_4]

        if Transform_Content.find('scale') != -1:
            location_2 = Transform_Content.find('scale')
            location_3 = Transform_Content.find('(', location_2)
            location_4 = Transform_Content.find(')', location_3)
            Scale_Content = re.sub(r',','',Transform_Content[location_3 + 1 : location_4]).split(' ')
            Y = Y * float(Scale_Content[-1])

        if Transform_Content.find('translate') != -1:
            location_2 = Transform_Content.find('translate')
            location_3 = Transform_Content.find('(', location_2)
            location_4 = Transform_Content.find(')', location_3)
            Scale_Content = re.sub(r',','',Transform_Content[location_3 + 1 : location_4]).split(' ')
            Y = Y + float(Scale_Content[-1])

        if Transform_Content.find('matrix') != -1:
            location_2 = Transform_Content.find('matrix')
            location_3 = Transform_Content.find('(', location_2)
            location_4 = Transform_Content.find(')', location_3)
            Matrix_Content = Transform_Content[location_3 + 1 : location_4].split(' ')
            if Matrix_Content[1] == '0' and Matrix_Content[2] == '0':
                Y = Y * float(Matrix_Content[3])
            else:
                Matrix_Count += 1
            Y = Y + float(Matrix_Content[5])    
        location_1 += -1

def MeasureHeight(File):
    minimun = 99999999999999999999999
    maximun = -99999999999999999999999
    Location_1 = 0
    while True:
        Action = 0
        Location_1 = File.find('<', Location_1, len(File) - 1)
        if Location_1 == -1:
            break

        if File[Location_1 : Location_1 + 10] == '<svg:tspan':
            Location_2 = File.find(" y=", Location_1)
            Location_3 = File.find('"', Location_2)
            Location_4 = File.find('"', Location_3 + 1)
            Coordinate = File[Location_3 + 1 : Location_4]
            Coordinate_Content = Extract_Real_Coordinate(File, Coordinate, Location_1 - 1)
            Coordinate = Coordinate_Content
            if Coordinate > maximun:
                maximun = Coordinate
            if Coordinate < minimun:
                minimun = Coordinate
            Location_1 += 1
        
        if File[Location_1 : Location_1 + 10] == '<svg:image':
            Location_2 = File.find(" y=", Location_1)
            Location_3 = File.find('"', Location_2)
            Location_4 = File.find('"', Location_3 + 1)
            Coordinate = File[Location_3 + 1 : Location_4]
            
            Location_3 = File.find('<', Location_1 + 1)

            Coordinate_Content = Extract_Real_Coordinate(File, Coordinate, Location_3 - 1)
            Coordinate = Coordinate_Content
            if Coordinate > maximun:
                maximun = Coordinate
            if Coordinate < minimun:
                minimun = Coordinate
            Location_1 += 1

        if File[Location_1 : Location_1 + 9] == '<svg:path':
            Location_2 = File.find(" d=", Location_1)
            Location_3 = File.find('"', Location_2)
            Location_4 = File.find('"', Location_3 + 1)
            Coordinate = File[Location_3 + 1 : Location_4]
            Data = Path(Coordinate, False)
            Minimun = Extract_Real_Coordinate(File, Data["Minimun"], Location_2)
            Maximun = Extract_Real_Coordinate(File, Data["Maximun"], Location_2)
            # if Minimun["Safe"] == 1 or Maximun["Safe"] == 1:
            #   return None
          
            if Maximun > maximun:
                maximun = Maximun
            if Minimun < minimun:
                minimun = Minimun
            Location_1 += 1

        if Action == 0 and Location_1 != -1:
            Location_1 += 1
    
    data = {
        "minimun": minimun,
        "maximun": maximun,
    }
    return maximun
 
def Path(Data, debugIndicator):
	rawData = Data
	Data = re.sub(r'[A-Z]','', Data).split(' ')
	while ' ' in Data:
		Location = Data.index(' ')
		del Data[Location]
	while '' in Data:
		Location = Data.index('')
		del Data[Location]
	Location = 1
	Minimun = 99999999999999999
	Maximun = -9999999999999999999999999999
	while Location <= len(Data) - 1:
		if float(Data[Location]) < float(Minimun):
			Minimun = Data[Location]
		if float(Data[Location]) > float(Maximun):
			Maximun = Data[Location]
		Location += 2
	return {"Minimun": round(float(Minimun), 4), "Maximun": round(float(Maximun), 4), "coordinateList": Data}

def ExtractQuestionData(File):
    data = File[
        File.find("<svg:g") :
        File.rfind("</svg:g>") + 8
    ]

    return data

def ExtractQuestionName(fileName):
    name = "File   {name}, question {no}"
    no = fileName[ fileName.find("@") + 1 : fileName.find(".") ]
    paper = fileName[ : fileName.find("@") ]
    return name.format(name=paper, no=no)

def DATA():
    data = {
            "questionGroup": [
                [
                    "group 1",
                    1,
                    5
                ],
                [
                    "group 2",
                    6,
                    10
                ],
                [
                    "group 3",
                    11,
                    15
                ]
            ],
            "pageLength": 720,
            "source": True,
            "targetLocation": "D:/0dataBank/Pastpapers/Economics/B-Product",
            "productLocation": "./product",
            "svgHeader": "<svg:svg xmlns:xlink=\"http://www.w3.org/1999/xlink\" xmlns:svg=\"http://www.w3.org/2000/svg\" version=\"1.1\"><svg:g transform='translate(0, 30)'>",
            "svgTail":"</svg:g></svg:svg>",
            "initialPageLength":5,
            "debug": {},
            "shiftY": 5,
            "shiftX": 30
        }
    return data

def RearrangeFileList(fileList):
    paperNameList = PaperNameList(fileList)
    paperNameList = sorted(paperNameList, key=lambda x: x[6 : 8])
    data = []
    paperNameList = sorted(paperNameList, reverse=True)

    for paper in paperNameList:
        list_storage = []
        for question in fileList:
            if question.find(paper) != -1:
                list_storage.append(question)
        list_storage = sorted(list_storage, key=lambda item : int(item[ item.find("@") + 1 : item.find(".") ]))
        
        for item in list_storage:
            data.append(item)
    return data

def PRINT(content):
    print(content,flush=True)
def PINPUT(content):
    print(content, flush=True)
    input()

Launcher()