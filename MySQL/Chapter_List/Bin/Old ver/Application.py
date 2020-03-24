import os

def Get_Chapter():
    Syllabus = '0610'
    File = open('./file.txt', 'r').read()
    Log = open('./Log.txt', 'w')
    Location_1 = 0
    Chapter_List = []
    while 1:
        Location_1 = File.find('chapter:', Location_1)
        if Location_1 == -1:
            break
        Location_1 = File.find(':', Location_1)
        Location_2 = File.find('#', Location_1)
        Chapter = File[Location_1 + 1 : Location_2]
        Chapter_List.append(Chapter)
    for Item in Chapter_List:
        Content = '[<syllabus:' + Syllabus +'><number:' + str(Item) + '>]\n'
        Log.write(Content)
Get_Chapter()
    
