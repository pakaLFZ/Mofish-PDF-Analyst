import os
import time
import re
import json

#Instructor = open('./Instructor.txt', 'r').read(

def Content_Input_Online():
    Chapter_List = []
    End = 0
    while not End:
        print('\n----------------------\n')
        print('Type in chapter. (Type in "/" to stop)')
        Chapter = ''
        while 1:
            Chapter = input()
            if Chapter == '/':
                End = 1
                break
            try:
                Chapter = str(round(float(Chapter), 1))
                break
            except:
                print('\n----------------------\n')
                print('"' + Chapter + '"is not a chapter. Please type in a number. (Type in "/" to stop)')
        
        Content = []
        while not End:
            print('\n----------------------\n')
            print('Chapter: ' + str(Chapter))
            print('Input content. (Type in "/" to stop)')
            Content_Storage = input()
            if Content_Storage == '/':
                break
            Content_Storage = list(set(re.sub(r'[^\w\s]',' ',Content_Storage).split(' ')))
            Content = Content + Content_Storage

        if not End:
            Instructor = open('Instructor.mofish', 'r').read()
            Location = 0
            while Location <= len(Content) - 1:
                if len(Content[Location]) == 0:
                    del Content[Location]
                    continue
                Content[Location] = Safety_Check(Content[Location])
                if Instructor.find(Content[Location]) != -1:
                    del Content[Location]
                    continue
                Location += 1

            Json_Content = {"chapter": Chapter, "content": Content}
            Chapter_List.append(Json_Content)
    return Chapter_List

def Content_Input_Offline():
    try:
        Text = open('./Text.txt', 'r', encoding='utf-8').read()
        Instructor = open('Instructor.mofish', 'r').read()
        #Book = open('./Biology.mofish', 'r', encoding='utf-8').read()
    except:
        print("Please check the existance of files 'Instructor.mofish' and 'Text.txt' ")
        print("The program will be terminated in 10s")
        #Instructor = open('Instructor.mofish', 'w')
        time.sleep(10)
        os._exit(0)
    Chapter_List = []
    Start = 0
    End = 0
    while 1:
        Start = Text.find('<#', Start)
        if Start == -1:
            break
        End = Text.find('#>', Start)
        Topic_1 = Text.find('[', Start, End)
        Topic_2 = Text.find(']', Start, End)
        Topic = Text[Topic_1 + 1 : Topic_2]
        Start = Topic_2 + 1
        Content = list(set(re.sub(r'[^\w\s]|\r|\n',' ',Text[Start : End]).split(' ')))
        Location = 0
        #Final_Content = []
        while Location <= len(Content) - 1:
            Content[Location] = Safety_Check(Content[Location])
            if len(Content[Location]) == 0 or Instructor.find(Content[Location]) != -1 or not Content[Location].isalpha():
                del Content[Location]
                continue
            Location += 1
        Content = set(Content)
        # while Location <= len(Content) - 1:
        #     if Book.find(Content[Location]) != -1 and Instructor.find(Content[Location]) == -1:
        #         if len(Content[Location]) == 0:
        #             del Content[Location]
        #             continue
        #         Final_Content.append(Content[Location])
        #     Location += 1
        Json_Content = {"chapter": Topic, "content": Content}
        Chapter_List.append(Json_Content)
        Start = End
    return Chapter_List   

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

def Get_Value(Chapter_List):
    Word_List_Count = []
    Word_List_Complete = []
    for Component in Chapter_List:
        for Word in Component["content"]:
            Word_List_Complete.append(Word)
    Word_List_Count = set(Word_List_Complete)


    Vocabulary_List = {}
    Peak = 1
    for Component in Word_List_Count:
        Number = Word_List_Complete.count(Component)
        Vocabulary_List[Component] = Number

        if Number > Peak:
            Peak = Number

    Vocabulary_Value = Vocabulary_List
    for Component in Word_List_Count:
        Vocabulary_Value[Component] = round(Peak / int(Vocabulary_Value[Component]), 4)
    
    return Vocabulary_Value

def Write_Log(Chapter_List, Vocabulary_Value):
    Log = open('./Log.txt', 'w')
    for Component in Chapter_List:
        try:
            Log.write('{ #chapter:' + Component["chapter"] + '#\n')
        except:
            print('\n######################')
            print('Something wrong with the chapter writing. Please check that a chapter is enclosed by "[]"')
            print("The program will be terminated in 10s")
            time.sleep(10)
        for Word in Component["content"]:
            try:
                Log.write('\t<' + Word + ':' + str(Vocabulary_Value[Word]) + '>\n')
            except:
                print('Cannot write "' + '<' + Word + ':' + str(Vocabulary_Value[Word]) + '>"')
        Log.write('}\n')

def Launcher():
    Answer = ''
    while 1:
        print('\n----------------------\n')
        print('Please choose input type:\n\t1. By hand\n\t2. By document (Using the "Text.txt" file)')
        print('Please Enter "1" or "2"')
        Answer = input()
        if str(Answer) == '1' or str(Answer) == '2':
            break
    Chapter_List = []
    if str(Answer) == '1':
        Chapter_List = Content_Input_Online()
    if str(Answer) == '2':
        Chapter_List = Content_Input_Offline()
    Vocabulary_Value = Get_Value(Chapter_List)
    Write_Log(Chapter_List, Vocabulary_Value)
    print('\n----------------------\n')
    print('Done')
    time.sleep(10)

Launcher()
