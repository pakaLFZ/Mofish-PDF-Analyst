import os
import time
import win32api,win32con #需要Pip安装pywin
import re
import threading

File_Storage_Location = 'E:/0Mofish/PDF/Table-13/Files'
LogFile_Storage_Location = 'E:/0Mofish/PDF/Table-13/LogFile.txt'
LogFile = open(LogFile_Storage_Location, 'w')
File_Name_List = []
File_Location_List = []
File_Number = 0
#程序缓存
Finished_File_List = []
Answer = []
Answer_Gathered_Number = -1
Paper_list = []
File_Used = []


#os.system("cls")
#print('\n\nStart time: ' + str(Time_Start), end = '\n\n')
for root, dirs, files in os.walk(File_Storage_Location, topdown=True):
    for name in files:
        if re.match('.*(.svg)', os.path.join(name)) is not None:
                File_Location_List.append(os.path.join(root) + '/' + os.path.join(name))
                File_Name_List.append(os.path.join(name))


def Answer_Extractor_Launcher():
    global File, File_Name_List, File_Number, Answer, LogFile, Answer_Gathered_Number, Paper_list
    #Paper_Name = Speculate_Question_Paper()
    Paper_Name = ''
    Inspector_Location = 0
    Answer = []
    while True:
        if File_Name_List[File_Number][Inspector_Location] == '-':
            break
        Paper_Name = Paper_Name + File_Name_List[File_Number][Inspector_Location]
        Inspector_Location += 1
    if Answer_Gathered_Number == 40 or Answer_Gathered_Number == -1:
        Paper_list.append(Paper_Name)
        Answer_Gathered_Number = 0
        LogFile.write('Paper: ' + Paper_Name + '\n')
        LogFile.flush()
    LogFile.write('File used: ' + File_Name_List[File_Number] + '\n')
    Inspector_Location = 0
    while Inspector_Location <= len(File) - 1:
        First_Font_Size = ''
        Second_Font_Size = ''
        Question_Number_Storage = ''
        Question_Answer_Storage = ''
        Type = 1
        if File[Inspector_Location : Inspector_Location + 9] == '<svg:defs':
            while True:
                if File[Inspector_Location : Inspector_Location + 10] == '</svg:defs':
                    Inspector_Location += 11
                    break
                Inspector_Location += 1
        if File[Inspector_Location : Inspector_Location + 10] == '<svg:style':
            while True:
                if File[Inspector_Location : Inspector_Location + 11] == '</svg:style':
                    Inspector_Location += 11
                    break
                Inspector_Location += 1
        if File[Inspector_Location : Inspector_Location + 7] == 'g_font_':
            Inspector_Location += 7
            Is_Question = 1
            #Get the first font size
            while True:
                if File[Inspector_Location] == '"':
                    Inspector_Location += 1
                    break
                First_Font_Size = First_Font_Size + File[Inspector_Location]
                Inspector_Location += 1
            # print(File[Inspector_Location - 20: Inspector_Location + 10] + '     ' + File[Inspector_Location] + '  ' + str(Inspector_Location))
            # input()
            Block_A = 1
            Block_B = 0
            while Block_A:
                #print(File[Inspector_Location - 20: Inspector_Location + 10] + '     ' + File[Inspector_Location] + '  ' + str(Inspector_Location))
                #input()
                if File[Inspector_Location] == '>':
                    Inspector_Location += 1
                    while True:
                        if File[Inspector_Location : Inspector_Location + 2] == '</':
                            Block_A = 0
                            while True:
                                if File[Inspector_Location] == '>':
                                    Inspector_Location += 1
                                    break
                                Inspector_Location += 1
                            break
                        if File[Inspector_Location].isdigit():
                            Is_Question = 1
                            Question_Number_Storage = Question_Number_Storage + File[Inspector_Location]
                            Inspector_Location += 1
                        if File[Inspector_Location] == ' ':
                            Inspector_Location += 1
                        if not File[Inspector_Location].isdigit():
                            if File[Inspector_Location] != ' ' and File[Inspector_Location] != '<':
                                Block_A = 0
                                Block_B = 0
                                Is_Question = 0
                                if File[Inspector_Location] == 'A':
                                    if File[Inspector_Location + 1] == ' ' or File[Inspector_Location + 1] == '<':
                                        Question_Answer_Storage = 'A'
                                        Type = 2
                                        #print('Get A')
                                if File[Inspector_Location] == 'B':
                                    if File[Inspector_Location + 1] == ' ' or File[Inspector_Location + 1] == '<':
                                        Question_Answer_Storage = 'B'
                                        Type = 2
                                        #print('Get B')
                                if File[Inspector_Location] == 'C':
                                    if File[Inspector_Location + 1] == ' ' or File[Inspector_Location + 1] == '<':
                                        Question_Answer_Storage = 'C'
                                        Type = 2
                                        #print('Get C')
                                if File[Inspector_Location] == 'D':
                                    if File[Inspector_Location + 1] == ' ' or File[Inspector_Location + 1] == '<':
                                        Question_Answer_Storage = 'D'
                                        Type = 2
                                        #print('Get D')
                                break
                Inspector_Location += 1
            while Is_Question and Block_B:
                print(File[Inspector_Location - 20: Inspector_Location + 10] + '     str:' + File[Inspector_Location] + '  ' + str(Inspector_Location))
                input()
                if File[Inspector_Location : Inspector_Location + 7] == 'g_font_':
                    Inspector_Location += 7
                    while True:
                        if File[Inspector_Location] == '"':
                            Inspector_Location += 1
                            Block_B = 0
                            if First_Font_Size == Second_Font_Size:
                                Is_Question = 0
                            break
                        Second_Font_Size = Second_Font_Size + File[Inspector_Location]
                        Inspector_Location += 1
                Inspector_Location += 1
            
            while Is_Question:
                #print('C')
                if File[Inspector_Location] == '>':
                    Inspector_Location += 1
                    break
                Inspector_Location += 1
            while Is_Question:
                #print('D')
                if File[Inspector_Location] == 'A' or File[Inspector_Location] == 'B' or File[Inspector_Location] == 'C' or File[Inspector_Location] == 'D' or File[Inspector_Location] == ' ':
                    if File[Inspector_Location] == 'A':
                        Question_Answer_Storage = 'A'
                        Inspector_Location += 1
                    if File[Inspector_Location] == 'B':
                        Question_Answer_Storage = 'B'
                        Inspector_Location += 1
                    if File[Inspector_Location] == 'C':
                        Question_Answer_Storage = 'C'
                        Inspector_Location += 1
                    if File[Inspector_Location] == 'D':
                        Question_Answer_Storage = 'D'
                        Inspector_Location += 1
                    if File[Inspector_Location] == ' ':
                        Inspector_Location += 1
                else:
                    if File[Inspector_Location] == '<':
                        if len(Question_Answer_Storage) >= 1 and len(Question_Number_Storage) >= 1:
                            Answer.append(Question_Number_Storage)
                            Answer.append(Question_Answer_Storage)
                        break
                    else:
                        break
            if Type == 2:
                if len(Question_Answer_Storage) >= 1 and len(Question_Number_Storage) >= 1:
                    Answer.append(Question_Number_Storage)
                    Answer.append(Question_Answer_Storage)
        Inspector_Location += 1
    
    #Sort
    Inspector_Location = 0
    Execution = 0
    while len(Answer) >= 2:
        if int(Answer[Inspector_Location]) > int(Answer[Inspector_Location + 2]):
            Number_Storage = Answer[Inspector_Location]
            Answer_Storage = Answer[Inspector_Location + 1]
            Answer[Inspector_Location] = Answer[Inspector_Location + 2]
            Answer[Inspector_Location + 1] = Answer[Inspector_Location + 3]
            Answer[Inspector_Location + 2] = Number_Storage
            Answer[Inspector_Location + 3] = Answer_Storage
            Execution = 1
            Inspector_Location += 2
        else:
            Inspector_Location += 2
        if Inspector_Location >= len(Answer) - 3:
            if Execution == 1:
                Inspector_Location = 0
                Execution = 0          
            else:
                break
    
    Answer_Gathered_Number += len(Answer) / 2

    #Write log
    Inspector_Location = 0
    while Inspector_Location <= len(Answer) - 1:
        LogFile.write(Answer[Inspector_Location] + ':' + Answer[Inspector_Location + 1] + '\n')
        Inspector_Location += 2
    LogFile.flush()

def Print_Percentage():
    global File_Number, File_Name_List, Finished_File_List
    Percentage = len(Finished_File_List) / len(File_Name_List)
    Percentage_Left = 1 - Percentage
    Percentage_Block = 0
    Percentage_Left_Block = 0
    print('    Processing file: ' + File_Name_List[File_Number], end = '')
    print('\n      |', end='')
    while Percentage_Block <= Percentage:
        print('#', end='')
        Percentage_Block += 0.02
    while Percentage_Left_Block <= Percentage_Left:
        print(' ', end='')
        Percentage_Left_Block += 0.02
    print('|', end='  ')
    print(str(round(Percentage * 100, 2)) + '%', end='\n\n')

def Print_Time():
    global Time_Start, File_Name_List, File_Number, Finished_File_List
    if File_Number >= 1:
        #时间计算
        Average_Time = (time.perf_counter() - Time_Start) / File_Number
        Average_Time_Left = Average_Time * (len(File_Name_List) - len(Finished_File_List))
        if time.perf_counter() - Time_Start > 60:
            Second_left = (time.perf_counter() - Time_Start) - ((time.perf_counter() - Time_Start) // 60) * 60
            print('Total time taken: ' + str(int((time.perf_counter() - Time_Start) // 60)) + 'min ' + str(round(Second_left, 2)) + 's', end='')
        else:
            print('Total time taken: ' + str(round(time.perf_counter() - Time_Start, 2)) + 's', end='')   
        print('    Average Time taken: ' + str(round((time.perf_counter() - Time_Start) / File_Number, 2)) + 's per file', end='')
        if Average_Time_Left > 60:
            Second_left = Average_Time_Left - (Average_Time_Left // 60) * 60
            print('    Averge time left: ' + str(int(Average_Time_Left // 60)) + 'min ' + str(round(Second_left, 2)) + 's', end='\n\n')
        else:
            print('    Averge time left: ' + str(round(Average_Time_Left, 2)) + 's', end='\n\n')   
    else:
        print('Total time taken: ' + str(round(time.perf_counter() - Time_Start, 2)) + 's', end='')

def A_Print_Percentage():
    global File_Number, File_Name_List
    Percentage = (File_Number + 1) / len(File_Name_List)
    Percentage_Left = 1 - Percentage
    Percentage_Block = 0
    Percentage_Left_Block = 0
    print('    Processing file: ' + File_Name_List[File_Number], end = '')
    print('\n      |', end='')
    while Percentage_Block <= Percentage:
        print('#', end='')
        Percentage_Block += 0.02
    while Percentage_Left_Block <= Percentage_Left:
        print(' ', end='')
        Percentage_Left_Block += 0.02
    print('|', end='  ')
    print(str(round(Percentage * 100, 2)) + '%', end='\n\n')

def A_Print_Time():
    global Time_Start, File_Name_List, File_Number
    if File_Number >= 1:
        #时间计算
        Average_Time = (time.perf_counter() - Time_Start) / File_Number
        Average_Time_Left = Average_Time * (len(File_Name_List) - File_Number)
        if time.perf_counter() - Time_Start > 60:
            Second_left = (time.perf_counter() - Time_Start) - ((time.perf_counter() - Time_Start) // 60) * 60
            print('Total time taken: ' + str(int((time.perf_counter() - Time_Start) // 60)) + 'min ' + str(round(Second_left, 2)) + 's', end='')
        else:
            print('Total time taken: ' + str(round(time.perf_counter() - Time_Start, 2)) + 's', end='')   
        print('    Average Time taken: ' + str(round((time.perf_counter() - Time_Start) / File_Number, 2)) + 's per file', end='')
        if Average_Time_Left > 60:
            Second_left = Average_Time_Left - (Average_Time_Left // 60) * 60
            print('    Averge time left: ' + str(int(Average_Time_Left // 60)) + 'min ' + str(round(Second_left, 2)) + 's', end='\n\n')
        else:
            print('    Averge time left: ' + str(round(Average_Time_Left, 2)) + 's', end='\n\n')   
    else:
        print('Total time taken: ' + str(round(time.perf_counter() - Time_Start, 2)) + 's', end='')

def Print_Information():
    global File_Name_List, File_Number, Finished_File_List
    os.system("cls")
    print('Total file number: ' + str(len(File_Name_List)))
    print('Processing file No.' + str(len(Finished_File_List)))
    print(str(len(File_Name_List) - File_Number - 1) + ' file(s) left')
    Print_Time()
    Print_Percentage()

def Speculate_Question_Paper():
    # 0620_m18_2_2_qp  0620_m15_qp_22 0439_w17_ms_21 0439_w17_gt
    global File_Name_List, File_Number
    File_Name_Storage = File_Name_List[File_Number]
    File_Identity = []
    if File_Name_Storage[0 : 4] == '0620' or File_Name_Storage[0 : 4] == '0439':
        File_Identity.append('Chemistry')
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

    Paper_Name_Location = 0
    Paper_Name = ''
    while Paper_Name_Location <= len(File_Identity) - 1:
        Paper_Name = Paper_Name + str(File_Identity[Paper_Name_Location]) + ' '
        Paper_Name_Location += 1
    return(Paper_Name)

Time_Start = time.perf_counter()
LogFile.write('Start Extracting answers\n')

while len(File_Name_List) > len(Finished_File_List):
    Repeated = 0
    Inner_File_Number = 0
    while Inner_File_Number <= len(File_Name_List) - 1:
        #print('A')
        Inspector_Location = 0
        Finished_Check = 0
        while Inspector_Location <= len(Finished_File_List) - 1:
            if File_Name_List[Inner_File_Number] == Finished_File_List[Inspector_Location]:
                Finished_Check = 1
                break
            Inspector_Location += 1
        if Finished_Check == 0:
            File_Number = Inner_File_Number
            Print_Information()
            File_open = open(File_Location_List[File_Number], 'r', encoding='utf-8')
            File = File_open.read()
            Answer_Extractor_Launcher()
            Finished_File_List.append(File_Name_List[File_Number])

        Inner_File_Number += 1


# while File_Number <= len(File_Name_List) - 1:#
#     if File_Name_List[File_Number][-5] != '0':
#         Print_Information()
#         File_open = open(File_Location_List[File_Number], 'r', encoding='utf-8')
#         File = File_open.read()
#         Answer_Extractor_Launcher()
#         Finished_File_List.append(File_Name_List[File_Number])
#     File_Number += 1

Paper_Number = 0
LogFile.write('\n---Summarize----\n')
while Paper_Number <= len(Paper_list) - 1:
    LogFile.write(Paper_list[Paper_Number] + '\n')
    Paper_Number += 1
LogFile.write('Total paper number: ' + str(len(Paper_list)) + '\n')
LogFile.write('Total time taken: ' + str(time.perf_counter() - Time_Start) + 's\n')
LogFile.flush()
print('Progression finished!  ' + str(len(Paper_list)) + ' unit(s) of answer has been extracted!')

