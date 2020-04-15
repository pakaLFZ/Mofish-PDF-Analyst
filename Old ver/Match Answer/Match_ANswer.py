import os
import time
import re

File_Storage_Location = './Files'
LogFile_Storage_Location = './LogFile.txt'
Instructor_Location = './Instructor.txt'
Instructor = open(Instructor_Location, 'r').read()
LogFile = open(LogFile_Storage_Location, 'w')
File_Name_List = []

#程序缓存
Bug_File = []

def Space_Eliminator(Name):     #在使用系统cmd复制bug文件的时候，会牵扯到路径。指令中的路径不能直接有空格。这个def的作用是在相关的地方加上""
    Name_Storage_1 = ''
    Name_Storage_2 = ''

    Inner_Inspector_Location = 0
    while Inner_Inspector_Location <= len(Name) - 1:
        if Name[Inner_Inspector_Location] == '/':
            Name_Storage_1 = Name_Storage_1 + '\\'
            Inner_Inspector_Location += 1
        if Inner_Inspector_Location <= len(Name) - 1:
            Name_Storage_1 = Name_Storage_1 + Name[Inner_Inspector_Location]
            Inner_Inspector_Location += 1

    Inner_Inspector_Location = 0
    while Inner_Inspector_Location <= len(Name_Storage_1) - 1:
        if Name_Storage_1[Inner_Inspector_Location] == ' ':
            Space_Check = 1
            while Space_Check:
                if Name_Storage_1[Inner_Inspector_Location] == '\\':
                    Inner_Inspector_Location += 1
                    Name_Storage_2 = Name_Storage_1[:
                                                    Inner_Inspector_Location] + '"'
                    while 1:
                        if Inner_Inspector_Location >= len(Name_Storage_1):
                            Space_Check = 0
                            break
                        if Name_Storage_1[Inner_Inspector_Location] == '\\':
                            Name_Storage_2 = Name_Storage_2 + '"\\'
                            Inner_Inspector_Location += 1
                            Space_Check = 0
                            break
                        Name_Storage_2 = Name_Storage_2 + \
                            Name_Storage_1[Inner_Inspector_Location]
                        Inner_Inspector_Location += 1
                if Space_Check == 1:
                    Inner_Inspector_Location += -1
        if Inner_Inspector_Location <= len(Name_Storage_1) - 1:
            Name_Storage_2 = Name_Storage_2 + \
                Name_Storage_1[Inner_Inspector_Location]
            Inner_Inspector_Location += 1
    return(Name_Storage_2)

def Bug_File_Copier(File_Name):      #将有问题的文件复制到BugFile文件夹内
    File_Location_Storage = ''
    Command_Storage = ''
    File_Location = './Files/' + File_Name
    File_Location_Storage = Space_Eliminator(File_Location)
    Bug_File_Location_Storage = './Problems/' + File_Name
    File_Product_Location_Storage = Space_Eliminator(Bug_File_Location_Storage)
    Command_Storage = 'copy ' + File_Location_Storage + ' ' + File_Product_Location_Storage
    os.system(Command_Storage)

TIME_START = time.perf_counter()
TIME_STORAGE = time.perf_counter()
for root, dirs, files in os.walk(File_Storage_Location, topdown=True):
    for name in files:
        if re.match('.*(.svg)', os.path.join(name)) is not None:
                File_Name_List.append(os.path.join(name))

while len(File_Name_List) != 0:
    print(len(File_Name_List))
    LogFile.write('<' + File_Name_List[0])
    LogFile.flush()

    Location_1 = File_Name_List[0].find('@')
    Location_2 = File_Name_List[0].find('.')
    Question_Number = File_Name_List[0][Location_1 + 1 : Location_2]

    Location_1 = File_Name_List[0].find('-')
    Paper_Name = File_Name_List[0][0 : Location_1]
    Paper_Name = Paper_Name.replace("qp", "ms")

    Location_1 = Instructor.find(Paper_Name)
    if Location_1 == -1:
        LogFile.write(':#Cannot find "' + Paper_Name + '"#>\n')
        LogFile.flush()
        del File_Name_List[0]

        Bug_File.append(Paper_Name)
        Bug_File.append('Missing')
        try:
            Bug_File_Copier(File_Name_List[0])
        except:
            pass
        continue
    Location_1 = Instructor.find('%', Location_1)
    Location_2 = Instructor.find('%', Location_1 + 1)
    if Location_2 == -1:
        Location_2 = len(Instructor) - 1
    # print('>>' + Question_Number)
    # input()
    Location_3 = Instructor.find(Question_Number, Location_1, Location_2)
    if Location_3 == -1:
        LogFile.write(':#Cannot find question "' + Question_Number + '"#>\n')
        LogFile.flush()
        del File_Name_List[0]

        Bug_File.append(Paper_Name)
        Bug_File.append('Missing Question: '+ Question_Number)
        try:
            Bug_File_Copier(File_Name_List[0])
        except:
            pass
        continue
    Location_4 = Instructor.find(':', Location_3)
    Location_5 = Instructor.find('>', Location_3)
    Answer = Instructor[Location_4 + 1 : Location_5]
    if Answer[0] != '#' and Answer[0] != 'A' and Answer[0] != 'B' and Answer[0] != 'C' and Answer[0] != 'D':
        Answer = '##Bug--"' + Answer + '"##'
    LogFile.write(':' + Answer + '>\n')
    del File_Name_List[0]

Bug_Recorder = []
Location = 0
while Location <= len(Bug_File) - 1:
    Location_1 = 0
    action = 0
    while Location_1 <= len(Bug_Recorder) - 1:
        # print('R:' + str(len(Bug_Recorder)) + '//' + str(Location_1))
        # print('F:' + str(len(Bug_File)) + "//" + str(Location))
        if Bug_Recorder[Location_1] == Bug_File[Location]:
            action = 1
            break
        Location_1 += 2
    if action == 0:
        Bug_Recorder.append(Bug_File[Location])
        Location += 1
    else:
        action = 0
        Location += 2

Bug_File = Bug_Recorder
LogFile.write('\n\n\n######BUG TIME######\n')
LogFile.flush()
Location = 0
while Location <= len(Bug_File) - 1:
    LogFile.write(Bug_File[Location] + '---' + Bug_File[Location + 1] + '\n')
    LogFile.flush()
    Location += 2

    


