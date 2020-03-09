import os
import time
import re
import threading

File_Storage_Location = './'
Instructor_Location_MCQ = './Instructor_mcq.mofish'
Instructor_Location_Paper = './Instructor_paper.mofish'
Log = open('./LogFile.txt', 'w')

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
    
def Analysis_PDF_Names(Instructor_Location_MCQ, Instructor_Location_Paper, Log):
    Instructor = open(Instructor_Location_MCQ, 'r').read()
    Reference = open(Instructor_Location_Paper, 'r').read()
    Location_1 = 0
    ID_Count = 1
    while Location_1 <= len(Instructor) - 1:
        #0620_m18_2_2_ms  0620_m15_ms_22 0439_w17_ms_21 0439_w17_gt  0625_s03_ms_1.pdf
        #<0438_s13_qp_53.pdf>
        print(Location_1)
        Location_1 = Instructor.find('<', Location_1)
        Location_2 = Instructor.find('>', Location_1)
        if Location_1 == -1:
            break
        Location_3 = Instructor.find(':', Location_1, Location_2)
        File_Name = Instructor[Location_1 + 1 : Location_3]
        Answer = Instructor[Location_3 + 1 : Location_2]
        if Answer[0] == '#':
            Answer = 'None'

        Location_3 = File_Name.find('-')
        Paper_Name_Storage = File_Name[0 : Location_3]
        Location_3 = Reference.find(Paper_Name_Storage)
        Location_4 = Reference.rfind('{', 0, Location_3)
        Location_3 = Reference.find('ID', Location_4)
        Location_4 = Reference.find('"', Location_3)
        Location_3 = Reference.find('"', Location_4 + 1)
        ID = Reference[Location_4 + 1 : Location_3]

        Location_3 = Instructor.find('@', Location_1, Location_2)
        Location_4 = Instructor.find('.', Location_1, Location_2)
        Question_No = Instructor[Location_3 + 1 : Location_4]


        Location_3 = File_Name.find('-')
        Source = File_Name[0 : Location_3] + '.pdf'
        Syllabus = Source[0 : 4]
        Year = '20' + Source[6 : 8]
        Month = Source[5]
        Paper_type = 0
        Varient = None



        Log.write('{\n')
        #Log.write('\t#ID:"' + str(ID_Count) + '",\n')
        Log.write('\t#File_Name:"' + str(File_Name) + '",\n')
        Log.write('\t#ID:"' + str(Question_No) + '",\n')
        Log.write('\t#Answer:"' + str(Answer) + '",\n')
        Log.write('\t#Chapter:"None",\n')
        Log.write('\t#Source:"' + str(ID) + '",\n')
        Log.write('}\n')
        Log.flush()

        ID_Count += 1
        Location_1 = Location_2

while 1:
    print('Please choose function:\n\tCollect_PDF_Names: 1\n\tAnalysis_PDF_Names: 2')
    Answer = input()
    if Answer == '1':
        Collect_PDF_Names(File_Storage_Location, Log)
        break
    if Answer == '2':
        Analysis_PDF_Names(Instructor_Location_MCQ, Instructor_Location_Paper, Log)
        break
        


