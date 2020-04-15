import os
import time
import win32api,win32con #需要Pip安装pywin
import re
import threading
File_Name_List = []
File_Storage_Location = './Files'
LogFile_Storage_Location = './Log.txt'
LogFile = open(LogFile_Storage_Location, 'w')
File_Number = 0
    
def Speculate_Question_Paper():
    global File_Name_List, File_Number, LogFile
    File_Name_Storage = File_Name_List[File_Number]
    File_Identity = []
    if File_Name_Storage[0 : 4] == '0620': 
        File_Identity.append('IGCSE/0620')
    if File_Name_Storage[0 : 4] == '0439':
        File_Identity.append('IGCSE/0439')
    if File_Name_Storage[9 : 11] == 'qp':
        File_Identity.append('Paper ' + str(File_Name_Storage[12]))
    if File_Name_Storage[13 : 15] == 'qp':
        File_Identity.append('Paper ' + str(File_Name_Storage[9]))
    if File_Name_Storage[5] == 'm':
        File_Identity.append('February/March')
    if File_Name_Storage[5] == 's':
        File_Identity.append('May/June')
    if File_Name_Storage[5] == 'w':
        File_Identity.append('October/November')
    File_Identity.append('20' + str(File_Name_Storage[6 : 8]))

    Inspector_Location = 0
    On_Progress = 1
    Question_Number = ''
    while Inspector_Location >= -len(File_Name_Storage) and On_Progress:
        if File_Name_Storage[Inspector_Location] == '@':
            Inspector_Location += 1
            while True:
                if File_Name_Storage[Inspector_Location] == '.':
                    File_Identity.append(Question_Number)
                    On_Progress = 0
                    break
                Question_Number = Question_Number + File_Name_Storage[Inspector_Location]
                Inspector_Location += 1

        Inspector_Location += -1

    Paper_Name_Location = 0
    Paper_Name = ''
    while Paper_Name_Location <= len(File_Identity) - 1:
        Paper_Name = Paper_Name + str(File_Identity[Paper_Name_Location]) + ';'
        Paper_Name_Location += 1
    #IGCSE/Chemistry(US);Paper 1;October/November;2017;
    return(Paper_Name)

for root, dirs, files in os.walk(File_Storage_Location, topdown=True):
    for name in files:
        if re.match('.*(.svg)', os.path.join(name)) is not None:
                File_Name_List.append(os.path.join(name))

while File_Number <= len(File_Name_List) - 1:
    print(File_Number)
    LogFile.write('>' + File_Name_List[File_Number] + ';')
    LogFile.flush()
    Paper_Identity = Speculate_Question_Paper()
    #IGCSE/Chemistry(US);Paper 1;October/November;2017;
    #subject;paper;month;year;QuestionNumber;chapter1;answer;
    LogFile.write(Paper_Identity)
    LogFile.write('1;A;\n')
    LogFile.flush()
    File_Number += 1
print('Done')

