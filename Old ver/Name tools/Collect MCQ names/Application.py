import os
import time
import re
import json


def Collect_PDF_Names(File_Storage_Location, Log):
    Files = []
    for files in os.walk(File_Storage_Location, topdown=True):
        for name in files:
            if os.path.join(name).find('.pdf') != -1:
                Indicator = os.path.join(name).find('qp')
                #print(Indicator)
                if Indicator != -1:
                    Files.append(os.path.join(name))
    Location = 0
    while Location <= len(Files) - 1:
        Log.write('<' + Files[Location] + '>\n')
        Location += 1
    print('Finished')
    
def Analysis_PDF_Names(Instructor_Location_MCQ, Instructor_Location_Paper, Instructor_Location_Chapter, Log):
    Information = []
    Instructor_MCQ = open(Instructor_Location_MCQ, 'r').read()
    Instructor_Paper = open(Instructor_Location_Paper, 'r').read()
    Instructor_Chapter = open(Instructor_Location_Chapter, 'r').read()
    Location_1 = 0
    Question_ID_Count = 1
    while Location_1 <= len(Instructor_MCQ) - 1:
        Content = {}
        #0620_m18_2_2_ms  0620_m15_ms_22 0439_w17_ms_21 0439_w17_gt  0625_s03_ms_1.pdf
        #<0438_s13_qp_53.pdf>
        # print(Location_1)
        Location_1 = Instructor_MCQ.find('<', Location_1)
        Location_2 = Instructor_MCQ.find('>', Location_1)
        if Location_1 == -1:
            break
        Location_3 = Instructor_MCQ.find(':', Location_1, Location_2)
        File_Name = Instructor_MCQ[Location_1 + 1 : Location_3]
        Answer = Instructor_MCQ[Location_3 + 1 : Location_2]
        if Answer[0] == '#':
            Answer = 'None'

        Location_3 = File_Name.find('-')
        Paper_Name_Storage = File_Name[0 : Location_3]
        Location_3 = Instructor_Paper.find(Paper_Name_Storage)
        Location_4 = Instructor_Paper.rfind('{', 0, Location_3)
        Location_3 = Instructor_Paper.find('ID', Location_4)
        Location_4 = Instructor_Paper.find('"', Location_3)
        Location_3 = Instructor_Paper.find('"', Location_4 + 1)
        ID = Instructor_Paper[Location_4 + 1 : Location_3]

        Location_3 = Instructor_MCQ.find('@', Location_1, Location_2)
        Location_4 = Instructor_MCQ.find('.', Location_1, Location_2)
        Question_No = Instructor_MCQ[Location_3 + 1 : Location_4]
        # print(File_Name)
        # input()
        Location_3 = Instructor_Chapter.find(File_Name)
        if Location_3 == -1:
            Chapter = 'Bug'
        else:
            Location_3 = Instructor_Chapter.find('[', Location_3)
            Location_4 = Instructor_Chapter.find(']', Location_3)
            #Chapter_Content = Instructor_Chapter[Location_2 + 1 : Location_3]
            Chapter = list(set(re.sub(r"'|,",'', Instructor_Chapter[Location_3 + 1 : Location_4]).split(' ')))

        # Location_3 = File_Name.find('-')
        # Source = File_Name[0 : Location_3] + '.pdf'
        # Syllabus = Source[0 : 4]
        # Year = '20' + Source[6 : 8]
        # Month = Source[5]
        # Paper_type = 0
        # Varient = None




        Content["File_Name"] = File_Name
        Content["Question_Number"] = Question_No 
        Content["Answer"] = Answer 
        Content["Source"] = ID 
        Content["Question_ID"] = Question_ID_Count
        Content["Chapter"] = Chapter

        Information.append(Content)
        Question_ID_Count += 1
        Location_1 = Location_2

    Log.write(json.dumps(Information))
    Log.flush()
    print('Done')

def Launcher():
    File_Storage_Location = './'
    Instructor_Location_MCQ = './Instructor_mcq.mofish'
    Instructor_Location_Paper = './Instructor_paper.mofish'
    Instructor_Location_Chapter = './Instructor_chapter.mofish'
    Log = open('./LogFile.txt', 'w')

    while 1:
        print('Please choose function:\n\tCollect_PDF_Names: 1\n\tAnalysis_PDF_Names: 2')
        Answer = input()
        if Answer == '1':
            Collect_PDF_Names(File_Storage_Location, Log)
            break
        if Answer == '2':
            Analysis_PDF_Names(Instructor_Location_MCQ, Instructor_Location_Paper, Instructor_Location_Chapter, Log)
            break
Launcher()


