import os
import time
import re
import threading

File_Storage_Location = './'
Instructor_Storage_Location = './Instructor.txt'
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
    
def Analysis_PDF_Names(Instructor_Storage_Location, Log):
    Instructor = open(Instructor_Storage_Location, 'r').read()
    Location = 0
    while Location <= len(Instructor) - 1:
        #0620_m18_2_2_ms  0620_m15_ms_22 0439_w17_ms_21 0439_w17_gt  0625_s03_ms_1.pdf
        #<0438_s13_qp_53.pdf>
        print(Location)
        Location = Instructor.find('<', Location)
        Location_1 = Instructor.find('>', Location)
        if Location_1 == -1:
            break
        File_Name = Instructor[Location + 1 : Location_1]
        try:
            if int(File_Name[-6]) > 2:
                Location = Location_1
                continue
        except:
            pass
        Syllabus = File_Name[0 : 4]
        Year = '20' + File_Name[6 : 8]
        Month = File_Name[5]
        Paper_type = 0
        Varient = None

        if File_Name[8 : 11] == '_2_':
            Paper_type = 2
        if File_Name[12 : 15] == '_2':
            Paper_type = 2
            Varient = File_Name[15]
        if File_Name[11 : 13] == '_2':
            Paper_type = 2
            Varient = File_Name[13]

        if File_Name[8 : 11] == '_1_':
            Paper_type = 1
        if File_Name[12 : 15] == '_1':
            Paper_type = 1
            Varient = File_Name[15]
        if File_Name[11 : 13] == '_1':
            Paper_type = 1
            Varient = File_Name[13]
        Log.write('{\n')
        Log.write('\t#Paper name:"' + str(File_Name) + '",\n')
        Log.write('\t#Syllabus:"' + str(Syllabus) + '",\n')
        Log.write('\t#Year:"' + str(Year) + '",\n')
        Log.write('\t#Month:"' + str(Month) + '",\n')
        Log.write('\t#Paper_type:"' + str(Paper_type) + '",\n')
        Log.write('\t#Varient:"' + str(Varient) + '",\n')
        Log.write('}\n')

        Location = Location_1

while 1:
    print('Please choose function:\n\tCollect_PDF_Names: 1\n\tAnalysis_PDF_Names: 2')
    Answer = input()
    if Answer == '1':
        Collect_PDF_Names(File_Storage_Location, Log)
        break
    if Answer == '2':
        Analysis_PDF_Names(Instructor_Storage_Location, Log)
        break
        


