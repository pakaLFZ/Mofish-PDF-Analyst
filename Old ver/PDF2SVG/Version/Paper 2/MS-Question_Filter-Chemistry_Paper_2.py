import os
import time
import win32api,win32con #需要Pip安装pywin
import re

#文件基础信息
File_Storage = "E:/0Mofish/DOWN LOAD/Chemistry" 
File_Location_List = []
File_Name_List = []
JS_File_Location = 'E:/0Mofish/PDF/Table 9/'
#Information storage
File_Number = 1
File_Match_Number = 0
Time_Start = time.perf_counter()

def Get_File_List():
    global File_Number, File_Match_Number, Time_Start, Time_Storage, File_Storage, File_Location_List, File_Name_List, Time_Storage
    for root, dirs, files in os.walk(File_Storage, topdown=True):
        for name in files:
            File_Number += 1
            if re.match('.*(.pdf)', os.path.join(name)) is not None:  # 0620_m18_2_2_qp  0620_m15_qp_22 0439_w17_ms_21 0439_w17_gt
                File_Match = 0
                if os.path.join(name)[8 : 11] == '_ms'and os.path.join(name)[11 : 13] == '_2' and float(os.path.join(name)[6 : 8]) > 15:
                    File_Match = 1
                if os.path.join(name)[8 : 11] == '_2_'and os.path.join(name)[13 : 15] == 'ms':
                    File_Match = 1
    
                if File_Match == 1:
                    File_Location_List.append(os.path.join(root) + '/' + os.path.join(name))
                    File_Name_List.append(os.path.join(name))

                    File_Match_Number += 1
                    Time_Storage = time.perf_counter()
                    # os.system("cls")
                    print('Matched ' + str(File_Match_Number) + ' file(s)')
                    print('Matching file No.' + str(File_Number))
                    print('Time taken: ' + str(round(Time_Storage - Time_Start, 3)) + 's')
                    Convert_File()

def Space_Eliminator(Name):
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
                    Name_Storage_2 = Name_Storage_1[: Inner_Inspector_Location] + '"'
                    while True:
                        if Inner_Inspector_Location >= len(Name_Storage_1):
                            Space_Check = 0
                            break
                        if Name_Storage_1[Inner_Inspector_Location] == '\\':
                            Name_Storage_2 = Name_Storage_2 + '"\\'
                            Inner_Inspector_Location += 1
                            Space_Check = 0
                            break
                        Name_Storage_2 = Name_Storage_2 + Name_Storage_1[Inner_Inspector_Location]
                        Inner_Inspector_Location += 1
                if Space_Check == 1:
                    Inner_Inspector_Location += -1
        if Inner_Inspector_Location <= len(Name_Storage_1) - 1:
            Name_Storage_2 = Name_Storage_2 + Name_Storage_1[Inner_Inspector_Location]
            Inner_Inspector_Location += 1
    return(Name_Storage_2)

def Convert_File():
    #copy E:\0Mofish\PDF\"Table 9"\Chemistry\0620_s10_qp_63.pdf E:\0Mofish\DOWNLOAD\a.pdf
    global File_Location_List, File_Name_List
    print('Conversion starts')
    File_Location_Storage = ''
    Command_Storage = ''

    File_Location_Storage = Space_Eliminator(File_Location_List[-1])
    File_Product_Location_Storage = Space_Eliminator(JS_File_Location) + File_Name_List[-1]
    Command_Storage = 'copy ' + File_Location_Storage + ' ' + File_Product_Location_Storage
    print(Command_Storage)
    os.system(Command_Storage)

    Command_Storage = 'node pdf2svg.js ' + File_Name_List[-1]
    os.system(Command_Storage)
    print('Finished one File')


Get_File_List()

Time_Storage = time.perf_counter()
os.system("cls")
for Name in File_Name_List:
    print(Name)

print('\n\n')
print('File list: Paper 2')
print('Matched ' + str(File_Match_Number) + ' file(s)')
print('Time taken: ' + str(round(Time_Storage - Time_Start, 3)) + 's')
print('File list is above')

