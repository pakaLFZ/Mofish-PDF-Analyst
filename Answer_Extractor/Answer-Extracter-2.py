import os
import time
import re

File_Storage_Location = './Files'
LogFile_Storage_Location = './LogFile.txt'
LogFile = open(LogFile_Storage_Location, 'w')
File_Name_List = []
File_Number = 0
#程序缓存
Finished_File_List = []
Answer = []
Answer_Gathered_Number = -1
File_Required = 'NO_FILE'

def Answer_Extractor_Launcher(File, File_Name_List, File_Number, LogFile):
    global File_Required
    #Paper_Name = Speculate_Question_Paper()
    Answer = []
    LogFile.write('File used: ' + File_Name_List[File_Number] + '\n')
    Inspector_Location = 0
    while Inspector_Location <= len(File) - 1:
        First_Font_Size = ''
        Second_Font_Size = ''
        Question_Number_Storage = ''
        Question_Answer_Storage = ''
        Type = 1
        if File[Inspector_Location : Inspector_Location + 9] == '<svg:defs':
            Location_Storage = File.find("</svg:defs>")
            Inspector_Location = Location_Storage + 11

        if File[Inspector_Location : Inspector_Location + 10] == '<svg:style':
            Location_Storage = File.find("</svg:style>")
            Inspector_Location = Location_Storage + 12

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
            Block_A = 1
            Block_B = 0
            while Block_A:
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
                # print(File[Inspector_Location - 20: Inspector_Location + 10] + '     str:' + File[Inspector_Location] + '  ' + str(Inspector_Location))
                # input()
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
    
    Answer_Gathered_Number == len(Answer) / 2
    # print(Answer)
    # input()
    #Write log
    if len(Answer) >= 1:
        Inspector_Location = 0
        while Inspector_Location <= len(Answer) - 1:
            LogFile.write(Answer[Inspector_Location] + ':' + Answer[Inspector_Location + 1] + '\n')
            Inspector_Location += 2
        LogFile.flush()
        #0620_m16_ms_12-1.svg
        if Answer_Gathered_Number < 40 and str(Answer[-2]) != "40":
            Location_Storage = File_Name_List[File_Number].find('-')
            Location_Storage_1 = File_Name_List[File_Number].find('.')
            Page_Number = File_Name_List[File_Number][Location_Storage + 1 : Location_Storage_1]
            Page_Number = str(int(Page_Number) + 1)
            File_Required = File_Name_List[File_Number][0 : Location_Storage] + '-' + Page_Number + '.svg'
            # print(File_Required)
            # input()

        else:
            File_Required = 'NO_FILE'


def Print_Time(File_Start_Time, TIME_START, File_Name_List, Start_File_Name_List, File_Number):
    os.system("cls")
    print(File_Start_Time + '    Processing files in : ' + File_Storage_Location)
    print("Mofish Pastpaper Separator   Ver.15  |")

    if Start_File_Name_List - len(File_Name_List) >= 1:
        # 时间计算
        Average_Time = (time.perf_counter() - TIME_START) / (Start_File_Name_List - len(File_Name_List))
        Average_Time_Left = Average_Time * len(File_Name_List)

        if time.perf_counter() - TIME_START > 60:
            Second_left = (time.perf_counter() - TIME_START) - ((time.perf_counter() - TIME_START) // 60) * 60
            print('Total time taken: ' + str(int((time.perf_counter() - TIME_START) / 60)) + 'min ' + str(round(Second_left, 2)) + 's', end='')
        else:
            print('Total time taken: ' +
                  str(round(time.perf_counter() - TIME_START, 2)) + 's', end='')
        print('    Average Time taken: ' + str(round((time.perf_counter() - TIME_START) / (Start_File_Name_List - len(File_Name_List)), 2)) + 's per file', end='')
        if Average_Time_Left > 60:
            Second_left = Average_Time_Left - (Average_Time_Left // 60) * 60
            print('    Averge time left: ' + str(int(Average_Time_Left // 60)
                                                 ) + 'min ' + str(round(Second_left, 2)) + 's', end='\n')
        else:
            print('    Averge time left: ' +
                  str(round(Average_Time_Left, 2)) + 's', end='\n\n')
    else:
        print('Total time taken: ' +
              str(round(time.perf_counter() - TIME_START, 2)) + 's', end='')
    #print('Processing file: ' + File_Name_List[File_Number])
    print('    Processed ' + str(Start_File_Name_List - len(File_Name_List)) + ' files; ', end='')
    print(str(len(File_Name_List)) + ' File(s) left', end='')
    Percentage = (Start_File_Name_List - len(File_Name_List)) / Start_File_Name_List
    Percentage_Left = 1 - Percentage
    Percentage_Block = 0
    Percentage_Left_Block = 0
    print('\n\n      |', end='')
    while Percentage_Block <= Percentage:
        print('#', end='')
        Percentage_Block += 0.02
    while Percentage_Left_Block <= Percentage_Left:
        print(' ', end='')
        Percentage_Left_Block += 0.02
    print('|', end='  ')
    print(str(round(Percentage * 100, 2)) + '%', end='\n\n')


TIME_START = time.perf_counter()
TIME_STORAGE = time.perf_counter()
for root, dirs, files in os.walk(File_Storage_Location, topdown=True):
    for name in files:
        if re.match('.*(.svg)', os.path.join(name)) is not None:
                File_Name_List.append(os.path.join(name))
Start_File_Name_List = len(File_Name_List)
while len(File_Name_List) > 0:
    File_Start_Time = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    Print_Time(File_Start_Time, TIME_START, File_Name_List, Start_File_Name_List, File_Number)
    if File_Required == 'NO_FILE':
        Test = 0
        Target_Number = 2
        Inspector_Location = 0
        while Inspector_Location <= len(File_Name_List) - 1:
            Location_Storage = File_Name_List[Inspector_Location].find('-')
            Location_Storage_1 = File_Name_List[Inspector_Location].find('.')
            Page_Number = File_Name_List[Inspector_Location][Location_Storage + 1 : Location_Storage_1]
            #print(Page_Number)
            if Page_Number == '1':
                del File_Name_List[Inspector_Location]
                Inspector_Location = 0
            if Page_Number == str(Target_Number):
                Test = 1
                break
            Inspector_Location += 1

            if Inspector_Location == len(File_Name_List) - 1 and Test == 0:
                Target_Number += 1
                Inspector_Location = 0
                
        if Test == 0:               
            LogFile.write('\n\n###Lefted files:\n')
            Inspector_Location = 0
            while Inspector_Location <= len(File_Name_List) - 1:
                LogFile.write('@' + File_Name_List[Inspector_Location] + '\n')
                Inspector_Location += 1
            LogFile.flush()
            break

        File_Number = Inspector_Location
        File_Location = File_Storage_Location + '/' + File_Name_List[File_Number]
        File_open = open(File_Location, 'r', encoding='utf-8')
        File = File_open.read()
        Answer_Extractor_Launcher(File, File_Name_List, File_Number, LogFile)
        del File_Name_List[File_Number]
    else:
        try:
            File_Location = File_Storage_Location + '/' + File_Required
            File_open = open(File_Location, 'r', encoding='utf-8')
            File = File_open.read()
            Answer_Extractor_Launcher(File, File_Name_List, File_Number, LogFile)
            del File_Name_List[File_Number]
        except:
            LogFile.write('###File "'+ File_Required +'" does not exit###\n')
            LogFile.flush()
            File_Required = 'NO_FILE'
print('Process Finished')
                