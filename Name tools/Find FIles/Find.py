import os
import re

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

def Bug_File_Copier(Root):     
    Bug_File_Location_Storage = './Sink'
    File_Location_Storage = Space_Eliminator(Root)
    File_Product_Location_Storage = Space_Eliminator(Bug_File_Location_Storage)
    Command_Storage = 'copy ' + File_Location_Storage + ' ' + File_Product_Location_Storage
    os.system(Command_Storage)

def Function():
    File_Storage = './'
    File_Location_List = []
    File_Name_List = []
    File_Required = []
    Missing = []
    Instructor = open('./Instructor.mofish', 'r').read()

    for root, dirs, files in os.walk(File_Storage, topdown=True):
        for name in files:
            if re.match('.*(.pdf)', os.path.join(name)) is not None:
                File_Location_List.append(os.path.join(root) + '/' + os.path.join(name))
                File_Name_List.append(os.path.join(name))
    print('Finished finding roots')
    Location_1 = 0
    while 1:
        Location_1 = Instructor.find('<', Location_1)
        if Location_1 == -1:
            break
        Location_2 = Instructor.find('>', Location_1)
        File_Required.append(Instructor[Location_1 + 1 : Location_2])
        Location_1 = Location_2
    print('Finished reading Instructor')

    while len(File_Required) != 0:
        print(len(File_Required))
        Location = 0
        while Location <= len(File_Location_List) - 1:
            Detector = File_Location_List[Location].find(File_Required[0])
            if Detector == -1:
                Location += 1
            else:
                Bug_File_Copier(File_Location_List[Location])
                del File_Required[0]
                break
            if Location == len(File_Location_List):
                Missing.append(File_Required[0])
                del File_Required[0]
    Log = open('./Missing_File.mofish', 'w')
    while len(Missing) != 0:
        Log.write('<' + Missing[0] + '>\n')
        Log.flush()
        del Missing[0]

Function()

