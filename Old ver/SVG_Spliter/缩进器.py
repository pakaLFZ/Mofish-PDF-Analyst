import os
import time

# MHTML 选项
File_Name = '1'
MHTML_File_Location = './' + File_Name + '.svg'
MHTML_File_Open = open(MHTML_File_Location, 'r', encoding='utf-8')
MHTML_File = MHTML_File_Open.read()
MHTML_File_Length = len(MHTML_File)
# 导出文件选项
HTML_File_Location = './' + File_Name + '_Tabbed.svg'
HTML_File = open(HTML_File_Location, 'w+', encoding='utf-8')


# 程序设置
global Inspector_Location, Run_Check, Tab_Number, End_Tag, Last_Tab_Recorder
Run_Check = 1
Inspector_Location = 0
Tab_Number = 0
End_Tag = 0
Last_Tab_Recorder = 0


def Tab_Write():
    global Tab_Number, HTML_File
    Tab_Number_Storage = Tab_Number
    Tab_While_GoOn = 0
    if Tab_Number_Storage > 0:
        Tab_While_GoOn = 1
    HTML_File.write('\n')
    while Tab_While_GoOn:
        HTML_File.write('\t')
        HTML_File.flush()
        Tab_Number_Storage = Tab_Number_Storage - 1
        if Tab_Number_Storage <= 0:
            Tab_While_GoOn = 0


def Find_Labels():
    global Inspector_Location, End_Tag, Tab_Number, Last_Tab_Recorder
    while Inspector_Location <= MHTML_File_Length - 1:
        if MHTML_File[Inspector_Location] == '<':
            if MHTML_File[Inspector_Location + 1] == '/':
                if Last_Tab_Recorder == 1:
                    Last_Tab_Recorder = 0
                else:
                    Tab_Number += -1
                    Tab_Write()
            else:
                if Last_Tab_Recorder == 0:
                    Tab_Write()
                    Last_Tab_Recorder = 1
                else:
                    Tab_Number += 1
                    Tab_Write()
            HTML_File.write('<')
            HTML_File.flush()
            Inspector_Location += 1
            while Inspector_Location <= MHTML_File_Length - 1:
                HTML_File.write(MHTML_File[Inspector_Location])
                HTML_File.flush()
                Inspector_Location += 1
                if MHTML_File[Inspector_Location - 1] == '>':
                    break
        if Inspector_Location <= MHTML_File_Length - 1 and MHTML_File[Inspector_Location] != '<':
            HTML_File.write(MHTML_File[Inspector_Location])
            HTML_File.flush()
            Inspector_Location += 1


Find_Labels()
print('Finish')
