import re, os, time

def Get_File_List(File_Storage):
    File_Name_List = []
    for root, _, files in os.walk(File_Storage, topdown=True):
        for name in files:
            if re.match('.*(.svg)', os.path.join(name)) is not None:
                File_Name_List.append(os.path.join(name))
    return(File_Name_List)

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

def Get_File_Content(File_Name):
    File = open('./Files/' + File_Name, 'r', encoding='utf-8').read()
    Instructor = open('./Instructor.mofish', 'r').read()
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

def Evaluate_File(File_Name, Content, Log):
    Book = open('./Book.mofish', 'r').read()
    Chapter_List = []
    Chapter = {}
    for Item in Content:
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
                Location_4 = Book.rfind('***', 0, Location_1)
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
        # Log.write('\tChapter:' + Item + '---Value:' + str(Chapter[Item]) + '\n')
        # Log.flush()
    Chapter_Value = sorted(Chapter_Value)
    return [k for k,v in Chapter.items() if float(v) == float(Chapter_Value[-1])]

def Record_Result():
    Book = open('./Book.mofish', 'r').read()
    Chapter_List = []
    Location_1 = 0
    while 1:
        Location_1 = Book.find('***', Location_1)
        if Location_1 == -1:
            break
        Location_2 = Book.find(':', Location_1)
        Location_1 = Book.find('#', Location_2)
        Chapter = Book[Location_2 + 1 : Location_1]
        Chapter_List.append(Chapter)
    #检查文件夹是否创建

def Launcher():
    File_Storage = './Files'
    Log = open('./Log.txt', 'w')
    File_Name_List = Get_File_List(File_Storage)
    Bug_File = []
    for Item in File_Name_List:
        Content = Get_File_Content(Item)['content']
        File_Name = Get_File_Content(Item)['file_name']
        Chapter = Evaluate_File(File_Name, Content, Log)
        Log.write('<#' + File_Name + ':' + str(Chapter) + '>\n')
        Log.flush()
        if len(Chapter) >= 4 or len(Chapter) == 0:
            Bug_File.append(File_Name)
    Percentage = str(round((len(File_Name_List) - len(Bug_File)) / len(File_Name_List), 2) * 100) + '%'
    Log.write('\n\n###Bug File###\n')
    for Item in Bug_File:
        Log.write(str(Item) + '\n')
    Log.flush
    print(Percentage + 'of files have been classified successfully')
        
Launcher()

    

    
    