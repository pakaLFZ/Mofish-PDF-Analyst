import os
import time
#import win32api,win32con #需要Pip安装pywin
import re
import threading

#File storage information
SVG_Storage = "./SVGs"
SVGFile_Location_List = []
SVGFile_Name_List = []
Product_Storage_Location = "./Product"
SVGFile_Number = 0
Bug_File_Location = './Product/BugFile'
#File information
Inspector_Location = 0
SVGFile_Height = ''
SVGFile_Transformation_Recorder = []
SVGFile_Taglist = []
SVGFile_Transformation_TagLabel = 0
Coordinate_X = ''
Coordinate_Y = ''
Coordinate_Y_List = []
Coordinate_X_List = []
#File indicators
SVGFile_TagEnd_Indicator = 1 # 0 means that the tag is not finished and the words between will be recorded
#SVG基础信息储存
SVGFile_Header = '<svg:svg xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:svg="http://www.w3.org/2000/svg" version="1.1">'
SVGFile_Separation_Point = []
SVGFile_Upper_Blank = 15    #分割后SVG顶部留白区域
#Other information
Time_Start = time.perf_counter()
Time_Storage = time.perf_counter()
#Time_Taken_List = []
Blank_Page_Check = 1
#Bug Storage
Broken_Matrix = 0    #检测有多少不能处理的Matrix


#Other function
def Space_Eliminator(Name):  #在使用系统cmd复制bug文件的时候，会牵扯到路径。指令中的路径不能直接有空格。这个def的作用是在相关的地方加上""
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

def Bug_File_Copier():   #将有问题的文件复制到BugFile文件夹内
    global SVGFile_Location_List, SVGFile_Number, Bug_File_Location, SVGFile_Name_List
    File_Location_Storage = ''
    Command_Storage = ''
    File_Location_Storage = Space_Eliminator(SVGFile_Location_List[SVGFile_Number])
    Bug_File_Location_Storage = Bug_File_Location + '/' + SVGFile_Name_List[SVGFile_Number]
    File_Product_Location_Storage = Space_Eliminator(Bug_File_Location_Storage)
    Command_Storage = 'copy ' + File_Location_Storage + ' ' + File_Product_Location_Storage
    print(Command_Storage)
    os.system(Command_Storage)
#Rewrite SVG
def Finding_Elements(SVGFile):   #寻找所有的tranformation，并将他们记录下来。为之后修改坐标做准备
    global Inspector_Location, SVGFile_Transformation_Recorder, Broken_Matrix, Blank_Page_Check, Bug_Reporter, SVGFile_Number, SVGFile_Location_List
    SVGFile_Transformation_Recorder.append(SVGFile_Transformation_TagLabel)
    while Inspector_Location <= len(SVGFile) - 1:
        #Matrix
        if SVGFile[Inspector_Location : Inspector_Location + 7] == 'matrix(':
            Inspector_Location += 7
            First_Number = ''
            Second_Number = ''
            Third_Number = ''
            Last_Number = ''
            Translation_First_Number = ''
            Translation_Last_Number = ''
            
            while True:
                if SVGFile[Inspector_Location] == ' ':
                    Inspector_Location += 1
                    break
                First_Number = First_Number + SVGFile[Inspector_Location]
                Inspector_Location += 1
            while True:
                if SVGFile[Inspector_Location] == ' ':
                    Inspector_Location += 1
                    break
                Second_Number = Second_Number + SVGFile[Inspector_Location]
                Inspector_Location += 1
            while True:
                if SVGFile[Inspector_Location] == ' ':
                    Inspector_Location += 1
                    break
                Third_Number = Third_Number + SVGFile[Inspector_Location]
                Inspector_Location += 1
            while True:
                if SVGFile[Inspector_Location] == ' ':
                    Inspector_Location += 1
                    break
                Last_Number = Last_Number + SVGFile[Inspector_Location]
                Inspector_Location += 1
            while True:
                if SVGFile[Inspector_Location] == ' ':
                    Inspector_Location += 1
                    break
                Translation_First_Number = Translation_First_Number + SVGFile[Inspector_Location]
                Inspector_Location += 1
            while True:
                if SVGFile[Inspector_Location] == ')':
                    Inspector_Location += 1
                    break
                Translation_Last_Number = Translation_Last_Number + SVGFile[Inspector_Location]
                Inspector_Location += 1
            
            if float(Third_Number) != 0.0 or float(Second_Number) != 0.0:
                Matrix_Storage = 'Matrix(' + First_Number + ' ' + Second_Number + ' ' + Third_Number + ' ' + Last_Number + ' ' + Translation_First_Number + ' ' + Translation_Last_Number + ')'
                #print('##Unexpected matrix attribute: ' + Matrix_Storage)
                Broken_Matrix += 1
                Bug_Reporter.write('File: ' + str(SVGFile_Location_List[SVGFile_Number]) + '\n' + '##Unexpected matrix attribute: ' + Matrix_Storage + '\n')
                Bug_Reporter.flush()

            
            SVGFile_Transformation_Recorder.append('Start_Translation')
            SVGFile_Transformation_Recorder.append(float(Translation_First_Number))
            SVGFile_Transformation_Recorder.append(float(Translation_Last_Number))
            SVGFile_Transformation_Recorder.append('End_Translation')
            SVGFile_Transformation_Recorder.append('Start_Scale')
            SVGFile_Transformation_Recorder.append(First_Number)
            if Last_Number[0] != '-':
                SVGFile_Transformation_Recorder.append(float(First_Number))
            if Last_Number[0] == '-':
                SVGFile_Transformation_Recorder.append(float(First_Number) * -1)
            SVGFile_Transformation_Recorder.append('End_Scale')

        #Translation
        if SVGFile[Inspector_Location : Inspector_Location + 10] == 'translate(':
            Inspector_Location += 10
            SVGFile_Transformation_Recorder.append('Start_Translation')
            Translation_Width_Storage = ''
            Translation_Height_Storage = ''
            while True:
                if SVGFile[Inspector_Location] == ' ' or SVGFile[Inspector_Location] == ')':
                    SVGFile_Transformation_Recorder.append(Translation_Width_Storage)
                    Inspector_Location += 1
                    break
                Translation_Width_Storage = Translation_Width_Storage + SVGFile[Inspector_Location]
                Inspector_Location += 1
            while True:
                if SVGFile[Inspector_Location] == ' ' or SVGFile[Inspector_Location] == ')':
                    Inspector_Location += 1
                    SVGFile_Transformation_Recorder.append(Translation_Height_Storage)
                    break
                Translation_Height_Storage = Translation_Height_Storage + SVGFile[Inspector_Location]
                Inspector_Location += 1
            SVGFile_Transformation_Recorder.append('End_Translation')
        #Scale
        if SVGFile[Inspector_Location : Inspector_Location + 6] == 'scale(':
            Inspector_Location += 6
            SVGFile_Transformation_Recorder.append('Start_Scale')
            Scale_Width_Storage = ''
            Scale_Height_Storage = ''
            #X coordinate
            while True:
                if SVGFile[Inspector_Location : Inspector_Location + 2] == ', ':
                    Inspector_Location += 2
                    break
                if SVGFile[Inspector_Location] == ' ':
                    Inspector_Location += 1
                    break
                Scale_Width_Storage = Scale_Width_Storage + SVGFile[Inspector_Location]
                Inspector_Location += 1
            SVGFile_Transformation_Recorder.append(float(Scale_Width_Storage))
            #Y coordinate
            while True:
                if SVGFile[Inspector_Location] == ')':
                    Inspector_Location += 1
                    break
                Scale_Height_Storage = Scale_Height_Storage + SVGFile[Inspector_Location]
                Inspector_Location += 1

            SVGFile_Transformation_Recorder.append(float(Scale_Height_Storage))
            SVGFile_Transformation_Recorder.append('End_Scale')

        if SVGFile[Inspector_Location] == '"':
            Inspector_Location += 1
            break
    
        Inspector_Location += 1

def Coordinate_X_Converter():    #根据Finding_Elements记录下来的transformation记录（SVGFile_Transformation_Recorder）修改坐标值
    global Coordinate_X_List, SVGFile_Transformation_Recorder, SVGFile_Transformation_TagLabel, SVGFile_Product
    Inner_Inspector_Location = -1
    while len(SVGFile_Transformation_Recorder) >= 1:
        if str(SVGFile_Transformation_Recorder[Inner_Inspector_Location]).isdigit():
            Inner_Inspector_Location += -1
        else:
            if str(SVGFile_Transformation_Recorder[Inner_Inspector_Location]) == 'End_Translation':
                #提取Translation内容
                Inner_Inspector_Location += -2
                Inner_List_Inspector_Location = 0
                while Inner_List_Inspector_Location <= len(Coordinate_X_List) - 1:
                    Coordinate_X_List[Inner_List_Inspector_Location] = float(Coordinate_X_List[Inner_List_Inspector_Location]) + float(SVGFile_Transformation_Recorder[Inner_Inspector_Location])
                    Inner_List_Inspector_Location += 1
                Inner_Inspector_Location += -2
            if str(SVGFile_Transformation_Recorder[Inner_Inspector_Location]) == 'End_Scale':
                Inner_Inspector_Location += -2
                Inner_List_Inspector_Location = 0
                while Inner_List_Inspector_Location <= len(Coordinate_X_List) - 1:
                    Coordinate_X_List[Inner_List_Inspector_Location] = float(Coordinate_X_List[Inner_List_Inspector_Location]) * float(SVGFile_Transformation_Recorder[Inner_Inspector_Location])
                    Inner_List_Inspector_Location += 1
                Inner_Inspector_Location += -2
            if str(SVGFile_Transformation_Recorder[Inner_Inspector_Location]) == '1':
                break

def Coordinate_X_Analyst():      #有时坐标是一串的，它的作用是将一串坐标变成一个list
    global Coordinate_X, Coordinate_X_List, SVGFile_Transformation_Recorder, SVGFile_Transformation_TagLabel, SVGFile_Product
    Inner_Inspector_Location = 0
    Coordinate_X_List = []
    #将坐标由字符串转换成list
    while Inner_Inspector_Location <= len(Coordinate_X) - 1:
        Coordinate_X_Inner_Storage = ''
        while True:
            if Coordinate_X[Inner_Inspector_Location] == ' ':
                Inner_Inspector_Location += 1
                Coordinate_X_List.append(Coordinate_X_Inner_Storage)
                break
            Coordinate_X_Inner_Storage = Coordinate_X_Inner_Storage + Coordinate_X[Inner_Inspector_Location]
            Inner_Inspector_Location += 1
            if Inner_Inspector_Location > len(Coordinate_X) - 1:
                Coordinate_X_List.append(Coordinate_X_Inner_Storage)
                break
    #开始转换
    Coordinate_X_Converter()
    #将List变成string
    Coordinate_X = ''
    for List_Component in Coordinate_X_List:
        Coordinate_X = Coordinate_X + str(List_Component) + ' '
    Coordinate_X = Coordinate_X[:-1]
    SVGFile_Product.write('x="')
    SVGFile_Product.write(Coordinate_X)
    SVGFile_Product.write('" ')
    SVGFile_Product.flush()

def Coordinate_Y_Converter():
    global Coordinate_Y_List, SVGFile_Transformation_Recorder, SVGFile_Transformation_TagLabel, SVGFile_Product
    Inner_Inspector_Location = -1
    while len(SVGFile_Transformation_Recorder) >= 1:
        if str(SVGFile_Transformation_Recorder[Inner_Inspector_Location]).isdigit():
            Inner_Inspector_Location += -1
        else:
            if str(SVGFile_Transformation_Recorder[Inner_Inspector_Location]) == 'End_Translation':
                #提取Translation内容
                Inner_Inspector_Location += -1
                Inner_List_Inspector_Location = 0
                while Inner_List_Inspector_Location <= len(Coordinate_Y_List) - 1:
                    Coordinate_Y_List[Inner_List_Inspector_Location] = float(Coordinate_Y_List[Inner_List_Inspector_Location]) + float(SVGFile_Transformation_Recorder[Inner_Inspector_Location])
                    Inner_List_Inspector_Location += 1
                Inner_Inspector_Location += -3
            if str(SVGFile_Transformation_Recorder[Inner_Inspector_Location]) == 'End_Scale':
                Inner_Inspector_Location += -1
                Inner_List_Inspector_Location = 0
                while Inner_List_Inspector_Location <= len(Coordinate_Y_List) - 1:
                    Coordinate_Y_List[Inner_List_Inspector_Location] = float(Coordinate_Y_List[Inner_List_Inspector_Location]) * float(SVGFile_Transformation_Recorder[Inner_Inspector_Location])
                    Inner_List_Inspector_Location += 1
                Inner_Inspector_Location += -3
            if str(SVGFile_Transformation_Recorder[Inner_Inspector_Location]) == '1':
                break

def Coordinate_Y_Analyst():
    global Coordinate_Y, Coordinate_Y_List, SVGFile_Transformation_Recorder, SVGFile_Transformation_TagLabel, SVGFile_Product
    Inner_Inspector_Location = 0
    Coordinate_Y_List = []
    #将坐标由字符串转换成list
    while Inner_Inspector_Location <= len(Coordinate_Y) - 1:
        Coordinate_Y_Inner_Storage = ''
        while Inner_Inspector_Location <= len(Coordinate_Y) - 1:
            if Coordinate_Y[Inner_Inspector_Location] == ' ':
                Inner_Inspector_Location += 1
                Coordinate_Y_List.append(Coordinate_Y_Inner_Storage)
                break
            Coordinate_Y_Inner_Storage = Coordinate_Y_Inner_Storage + Coordinate_Y[Inner_Inspector_Location]
            Inner_Inspector_Location += 1
        Coordinate_Y_List.append(Coordinate_Y_Inner_Storage)
                
    #开始转换
    Coordinate_Y_Converter()
    #将List变成string
    Coordinate_Y = ''
    for List_Component in Coordinate_Y_List:
        Coordinate_Y = Coordinate_Y + str(List_Component) + ' '
    Coordinate_Y = Coordinate_Y[:-1]
    SVGFile_Product.write('y="')
    SVGFile_Product.write(Coordinate_Y)
    SVGFile_Product.write('" ')
    SVGFile_Product.flush()
                    
def Path_Route_Analyst():        #将Path里的坐标提炼出来用Coordinate_X_Converter()和Coordinate_Y_Converter()转换坐标
    global Path_Route, SVGFile_Transformation_Recorder, SVGFile_Transformation_TagLabel, SVGFile_Product, Coordinate_X_List, Coordinate_Y_List
    Inner_Inspector_Location = 0
    Path_Route_List = []
    #将坐标由字符串转换成list
    while Inner_Inspector_Location <= len(Path_Route) - 1:
        Path_Route_Inner_Storage = ''
        while Inner_Inspector_Location <= len(Path_Route) - 1:
            if Path_Route[Inner_Inspector_Location] == ' ':
                Path_Route_List.append(Path_Route_Inner_Storage)
                Inner_Inspector_Location += 1
                break
            Path_Route_Inner_Storage = Path_Route_Inner_Storage + Path_Route[Inner_Inspector_Location]
            Inner_Inspector_Location += 1
        if Inner_Inspector_Location > len(Path_Route) - 1:
            Path_Route_List.append(Path_Route_Inner_Storage)
    #转换
    Inner_Inspector_Location = 0
    X_Check = 1 #用来检测该坐标是否为X轴坐标，1为是，0为不是
    while Inner_Inspector_Location <= len(Path_Route_List) - 1:
        # print(Path_Route_List[Inner_Inspector_Location])
        if Path_Route_List[Inner_Inspector_Location] != 'M' and Path_Route_List[Inner_Inspector_Location] != 'L' and Path_Route_List[Inner_Inspector_Location] != 'H' and Path_Route_List[Inner_Inspector_Location] != 'C' and Path_Route_List[Inner_Inspector_Location] != 'V' and Path_Route_List[Inner_Inspector_Location] != 'S' and Path_Route_List[Inner_Inspector_Location] != 'Q' and Path_Route_List[Inner_Inspector_Location] != 'T' and Path_Route_List[Inner_Inspector_Location] != 'A' and Path_Route_List[Inner_Inspector_Location] != 'Z':
            if X_Check == 1 and Inner_Inspector_Location <= len(Path_Route_List) - 1:
                Coordinate_X_List = []
                Coordinate_X_List.append(Path_Route_List[Inner_Inspector_Location])
                Coordinate_X_Converter()
                Path_Route_List[Inner_Inspector_Location] = str(Coordinate_X_List[0])
                Inner_Inspector_Location += 1
                X_Check = 0
            if X_Check == 0 and Inner_Inspector_Location <= len(Path_Route_List) - 1:
                Coordinate_Y_List = []
                Coordinate_Y_List.append(Path_Route_List[Inner_Inspector_Location])
                Coordinate_Y_Converter()
                Path_Route_List[Inner_Inspector_Location] = str(Coordinate_Y_List[0])
                Inner_Inspector_Location += 1
                X_Check = 1
        else:
            Inner_Inspector_Location += 1
    Path_Route = ''
    for List_Component in Path_Route_List:
        Path_Route = Path_Route + str(List_Component) + ' '
    Path_Route = Path_Route[:-1]
    SVGFile_Product.write('d="')
    SVGFile_Product.write(Path_Route)
    SVGFile_Product.write('" ')
    SVGFile_Product.flush()

def Stroke_Width_Analyst():     #修改线条宽度
    global Stroke_Width, SVGFile_Transformation_Recorder, SVGFile_Transformation_TagLabel, SVGFile_Product
    Inner_Inspector_Location = -1
    while len(SVGFile_Transformation_Recorder) >= 1:
        if str(SVGFile_Transformation_Recorder[Inner_Inspector_Location]).isdigit():
            Inner_Inspector_Location += -1
        else:
            if str(SVGFile_Transformation_Recorder[Inner_Inspector_Location]) == 'End_Translation':
                Inner_Inspector_Location += -4
            if str(SVGFile_Transformation_Recorder[Inner_Inspector_Location]) == 'End_Scale':
                Inner_Inspector_Location += -2
                Stroke_Width = float(Stroke_Width) * float(SVGFile_Transformation_Recorder[Inner_Inspector_Location])
                Inner_Inspector_Location += -2
            if str(SVGFile_Transformation_Recorder[Inner_Inspector_Location]) == '1':
                break

def Font_Size_Analyst():        #修改字体宽度
    global Font_Size, SVGFile_Transformation_Recorder, SVGFile_Transformation_TagLabel, SVGFile_Product
    Inner_Inspector_Location = -1
    while len(SVGFile_Transformation_Recorder) >= 1:
        if str(SVGFile_Transformation_Recorder[Inner_Inspector_Location]).isdigit():
            Inner_Inspector_Location += -1
        else:
            if str(SVGFile_Transformation_Recorder[Inner_Inspector_Location]) == 'End_Translation':
                Inner_Inspector_Location += -4
            if str(SVGFile_Transformation_Recorder[Inner_Inspector_Location]) == 'End_Scale':
                Inner_Inspector_Location += -2
                Font_Size = float(Font_Size) * float(SVGFile_Transformation_Recorder[Inner_Inspector_Location])
                Inner_Inspector_Location += -2
            if str(SVGFile_Transformation_Recorder[Inner_Inspector_Location]) == '1':
                break

def Rewrite_SVG():              #去除文件中的transformation并利用以上工具转换坐标
    global Inspector_Location, Blank_Page_Check, SVGFile, SVGFile_Product, SVGFile_Taglist, SVGFile_Transformation_TagLabel, SVGFile_Transformation_Recorder, Path_Route, Coordinate_X, Coordinate_Y, SVGFile_Product_Open_Location, Stroke_Width, Font_Size, OutMode_Indicator, SVGFile_Product_Open_Location
    Inspector_Location = 0
    SVGFile_Product_Open_Location = Product_Storage_Location + '/' + SVGFile_Name_List[SVGFile_Number]
    SVGFile_Open = open(SVGFile_Location_List[SVGFile_Number], 'r', encoding='utf-8')
    SVGFile = SVGFile_Open.read()
    SVGFile_Product = open(SVGFile_Product_Open_Location, 'w', encoding='utf-8')
    while Inspector_Location <= len(SVGFile) - 1:
        #print('Inspector: ' + str(Inspector_Location) + '    Code: ' + SVGFile[Inspector_Location - 10 : Inspector_Location + 10])
        if SVGFile[Inspector_Location] == '<' and SVGFile[Inspector_Location + 1] != '/':
            InTag_Transform_Exist = 0
            #print('a')
            while Inspector_Location <= len(SVGFile) - 1:
                #Detection for transformations
                if SVGFile[Inspector_Location : Inspector_Location + 10] == 'transform=':
                    Inspector_Location += 11
                    SVGFile_Transformation_TagLabel += 1
                    Finding_Elements(SVGFile)
                    InTag_Transform_Exist = 1
                    SVGFile_Taglist.append(SVGFile_Transformation_TagLabel)
                #Writing for the question content
                #检测坐标
                #print('1')
                if SVGFile[Inspector_Location : Inspector_Location + 2] == 'y=' and SVGFile[Inspector_Location - 1] == ' ':
                    Coordinate_Y = ''
                    Inspector_Location += 3
                    while True:
                        if SVGFile[Inspector_Location] == '"':
                            Inspector_Location += 1
                            break
                        Coordinate_Y = Coordinate_Y + SVGFile[Inspector_Location]
                        Inspector_Location += 1
                    Coordinate_Y_Analyst()
                
                if SVGFile[Inspector_Location : Inspector_Location + 2] == 'x=' and SVGFile[Inspector_Location - 1] == ' ':
                    Coordinate_X = ''
                    Inspector_Location += 3
                    while True:
                        if SVGFile[Inspector_Location] == '"':
                            Inspector_Location += 1
                            break
                        Coordinate_X = Coordinate_X + SVGFile[Inspector_Location]
                        Inspector_Location += 1
                    Coordinate_X_Analyst()
                
                if SVGFile[Inspector_Location : Inspector_Location + 2] == 'd=' and SVGFile[Inspector_Location - 1] == ' ':
                    Path_Route = ''
                    Inspector_Location += 3
                    while True:
                        if SVGFile[Inspector_Location] == '"':
                            Inspector_Location += 1
                            break
                        Path_Route = Path_Route + SVGFile[Inspector_Location]
                        Inspector_Location += 1
                    Path_Route_Analyst()
                
                if SVGFile[Inspector_Location : Inspector_Location + 13] == 'stroke-width=' and SVGFile[Inspector_Location - 1] == ' ':
                    Inspector_Location += 14
                    SVGFile_Product.write('stroke-width="')
                    SVGFile_Product.flush()
                    Stroke_Width_Recorder = ''
                    while True:
                        if SVGFile[Inspector_Location] == '"':
                            Inspector_Location += 1
                            break
                        Stroke_Width_Recorder = Stroke_Width_Recorder + SVGFile[Inspector_Location]
                        Inspector_Location += 1
                    Stroke_Width = float(Stroke_Width_Recorder[:-2])
                    Stroke_Width_Analyst()
                    SVGFile_Product.write(str(Stroke_Width) + 'px')
                    SVGFile_Product.write('" ')
                    SVGFile_Product.flush()
                #print('5')
                if SVGFile[Inspector_Location : Inspector_Location + 11] == 'font-size="' and SVGFile[Inspector_Location - 1] == ' ':
                    Inspector_Location += 11
                    SVGFile_Product.write('font-size="')
                    SVGFile_Product.flush()
                    Font_Size_Recorder = ''
                    while True:
                        if SVGFile[Inspector_Location] == '"':
                            Inspector_Location += 1
                            break
                        Font_Size_Recorder = Font_Size_Recorder + SVGFile[Inspector_Location]
                        Inspector_Location += 1
                    Font_Size = float(Font_Size_Recorder[:-2])
                    Font_Size_Analyst()
                    SVGFile_Product.write(str(Font_Size) + 'px')
                    SVGFile_Product.write('" ')
                    SVGFile_Product.flush()
                #print('6')
                if SVGFile[Inspector_Location] == '>':
                    SVGFile_Product.write('>')
                    SVGFile_Product.flush()
                    Inspector_Location += 1
                    while True:
                        if SVGFile[Inspector_Location : Inspector_Location + 10] == 'BLANK PAGE':
                            Blank_Page_Check = 0
                            break
                        if SVGFile[Inspector_Location] == '<':
                            break
                        SVGFile_Product.write(SVGFile[Inspector_Location])
                        SVGFile_Product.flush()
                        Inspector_Location += 1
                    #Record for Taglist
                    if InTag_Transform_Exist == 0:
                        SVGFile_Taglist.append(0)
                        InTag_Transform_Exist = 0
                    #结束循环
                    break
                #print('7')
                #Writing for the tag content
                SVGFile_Product.write(SVGFile[Inspector_Location])
                SVGFile_Product.flush()
                Inspector_Location += 1
            #print('b')
        
        if SVGFile[Inspector_Location : Inspector_Location + 2] == '</':
            #Dealing with the recording of Tags
            if len(SVGFile_Taglist) != 0:
                if SVGFile_Taglist[-1] != 0:
                    # print(SVGFile_Transformation_Recorder)
                    # print(SVGFile_Taglist)
                    SVGFile_Taglist = SVGFile_Taglist[:-1]
                    while True:
                        if SVGFile_Transformation_Recorder[-1] == SVGFile_Transformation_TagLabel:
                            SVGFile_Transformation_Recorder = SVGFile_Transformation_Recorder[:-1]
                            SVGFile_Transformation_TagLabel += -1
                            break
                        SVGFile_Transformation_Recorder = SVGFile_Transformation_Recorder[:-1]
                else:
                    SVGFile_Taglist = SVGFile_Taglist[:-1]
            #Filling the tag content
            while Inspector_Location <= len(SVGFile) - 1:
                if SVGFile[Inspector_Location] == '>':
                    SVGFile_Product.write('>')
                    SVGFile_Product.flush()
                    Inspector_Location += 1
                    break
                SVGFile_Product.write(SVGFile[Inspector_Location])
                SVGFile_Product.flush()
                Inspector_Location += 1
        
        if Inspector_Location <= len(SVGFile) - 1:
            if SVGFile[Inspector_Location] != '<':
                Inspector_Location += 1
# Separate SVG
def Find_Separation_Location(SVGFile):  #寻找分割点
    global SVGFile_Separation_Point
    SU_Inspector_Location = 0
    while SU_Inspector_Location < len(SVGFile) - 1:
        if SVGFile[SU_Inspector_Location : SU_Inspector_Location + 10] == '<svg:tspan':
            if SVGFile[SU_Inspector_Location + 24 : SU_Inspector_Location + 31] == 'g_font_' or SVGFile[SU_Inspector_Location + 24 : SU_Inspector_Location + 33] == 'Helvetica':
                SU_Inspector_Location_3 = SU_Inspector_Location + 31
                Font_Type_No_1 = ''
                while True:
                    if SVGFile[SU_Inspector_Location_3] == '"':
                        break
                    Font_Type_No_1 = Font_Type_No_1 + SVGFile[SU_Inspector_Location_3]
                    SU_Inspector_Location_3 += 1
                It_Is_Question_Number = 0
                First_Task = 0
                Second_Task = 0
                First_Block = 0
                SU_Inspector_Location_1 = SU_Inspector_Location
                SU_Inspector_Location += 1
                while True:
                    if SVGFile[SU_Inspector_Location_1] == '>':
                        SU_Inspector_Location_1 += 1
                        break
                    SU_Inspector_Location_1 += 1
                First_Number = 0
                while True:
                    if First_Number == 0:
                        if SVGFile[SU_Inspector_Location_1].isdigit() and SVGFile[SU_Inspector_Location_1] != ' ':
                            SU_Inspector_Location_1 += 1
                            First_Number = 1
                        else:
                            break
                    else:
                        if SVGFile[SU_Inspector_Location_1].isdigit() or SVGFile[SU_Inspector_Location_1] == ' ':
                            SU_Inspector_Location_1 += 1
                        else:
                            break
                    if SVGFile[SU_Inspector_Location_1] == '<':
                        First_Task = 1
                        break
                    
                #Get rid of </svg:tspan>
                while First_Task:
                    if SVGFile[SU_Inspector_Location_1] == '>':
                        First_Block = 1
                        SU_Inspector_Location_1 += 1
                        break
                    SU_Inspector_Location_1 += 1
                while First_Task:
                    if SVGFile[SU_Inspector_Location_1] == '>': 
                        break
                    if SVGFile[SU_Inspector_Location_1 : SU_Inspector_Location_1 + 7] == 'g_font_' and First_Block == 1:
                        SU_Inspector_Location_3 = SU_Inspector_Location_1 + 7
                        Font_Type_No_2 = ''
                        while True:
                            if SVGFile[SU_Inspector_Location_3] == '"':
                                break
                            Font_Type_No_2 = Font_Type_No_2 + SVGFile[SU_Inspector_Location_3]
                            SU_Inspector_Location_3 += 1
                        if Font_Type_No_1 != Font_Type_No_2:
                            Second_Task = 1
                        break
                    
                    if SVGFile[SU_Inspector_Location_1 : SU_Inspector_Location_1 + 9] == 'Helvetica' and First_Block == 1:
                        Second_Task = 1

                    SU_Inspector_Location_1 += 1
                Sentence_Length = 0
                while Second_Task:
                    if SVGFile[SU_Inspector_Location_1] == '>':
                        SU_Inspector_Location_1 += 1
                        while True:
                            if SVGFile[SU_Inspector_Location] == '©' or SVGFile[SU_Inspector_Location : SU_Inspector_Location + 5] == '0620/':
                                SU_Inspector_Location_1 = SU_Inspector_Location
                                SU_Inspector_Location += 1
                                Coordinate_Storage = ''
                                Block_End = 1
                                while Block_End:
                                    if SVGFile[SU_Inspector_Location_1 : SU_Inspector_Location_1 + 3] == 'y="':
                                        SU_Inspector_Location_1 += 3
                                        while True:
                                            if SVGFile[SU_Inspector_Location_1] == '"':
                                                SVGFile_Separation_Point.append(Coordinate_Storage)
                                                Block_End = 0
                                                break
                                            Coordinate_Storage = Coordinate_Storage + SVGFile[SU_Inspector_Location_1]
                                            SU_Inspector_Location_1 += 1
                                    SU_Inspector_Location_1 += -1
                         
                            if SVGFile[SU_Inspector_Location_1] == ' ':
                                SU_Inspector_Location_1 += 1
                            else:
                                It_Is_Question_Number = 1
                                SU_Inspector_Location_1 += 1
                            Sentence_Length += 1
                            if SVGFile[SU_Inspector_Location_1] == '<':
                                Second_Task = 0
                                break
                    SU_Inspector_Location_1 += 1
                if It_Is_Question_Number == 1 and Sentence_Length >= 4:
                    Block_End = 1
                    while Block_End:
                        Coordinate_Storage = ''
                        if SVGFile[SU_Inspector_Location : SU_Inspector_Location + 3] == 'y="' and SVGFile[SU_Inspector_Location - 1] == ' ':
                            SU_Inspector_Location += 3
                            while True:
                                if SVGFile[SU_Inspector_Location] == '"':
                                    SVGFile_Separation_Point.append(Coordinate_Storage)
                                    SU_Inspector_Location += 1
                                    Block_End = 0
                                    break
                                Coordinate_Storage = Coordinate_Storage + SVGFile[SU_Inspector_Location]
                                SU_Inspector_Location += 1
                        SU_Inspector_Location += 1                   
        
        if SVGFile[SU_Inspector_Location] == '©' or SVGFile[SU_Inspector_Location : SU_Inspector_Location + 5] == '0620/':
            SU_Inspector_Location_1 = SU_Inspector_Location
            SU_Inspector_Location += 1
            Coordinate_Storage = ''
            Block_End = 1
            while Block_End:
                if SVGFile[SU_Inspector_Location_1 : SU_Inspector_Location_1 + 3] == 'y="':
                    SU_Inspector_Location_1 += 3
                    while True:
                        if SVGFile[SU_Inspector_Location_1] == '"':
                            SVGFile_Separation_Point.append(Coordinate_Storage)
                            Block_End = 0
                            break
                        Coordinate_Storage = Coordinate_Storage + SVGFile[SU_Inspector_Location_1]
                        SU_Inspector_Location_1 += 1
                SU_Inspector_Location_1 += -1
            # print('@')
            # print(SVGFile_Separation_Point)
        SU_Inspector_Location += 1
    #排序 从左到右按从小到大排序
    SVGFile_Separation_Point_Storage = ''
    SU_Inspector_Location_2 = 0
    while True:
        Sequence_Check = 0 #如果为0，则表示顺序已经正确
        if SU_Inspector_Location_2 <= len(SVGFile_Separation_Point) - 2:
            if float(SVGFile_Separation_Point[SU_Inspector_Location_2]) - float(SVGFile_Separation_Point[SU_Inspector_Location_2 + 1]) > 0:
                SVGFile_Separation_Point_Storage = SVGFile_Separation_Point[SU_Inspector_Location_2]
                SVGFile_Separation_Point[SU_Inspector_Location_2] = SVGFile_Separation_Point[SU_Inspector_Location_2 + 1]
                SVGFile_Separation_Point[SU_Inspector_Location_2 + 1] = SVGFile_Separation_Point_Storage
                SU_Inspector_Location_2 += 1
                Sequence_Check = 1
            else:
                SU_Inspector_Location_2 += 1
        
        if SU_Inspector_Location_2 >= len(SVGFile_Separation_Point) - 1:
            if Sequence_Check == 1:
                SU_Inspector_Location_2 = 0
            else:
                break
            #SU_Inspector_Location_2 = 0
    if len(SVGFile_Separation_Point) <= 1:
        SVGFile_Separation_Point = []
    # print("    File " + SVGFile_Name_List[SVGFile_Number] + "'s separation points are:    ", end = '')
    # print(SVGFile_Separation_Point)
    #过滤
    SVGFile_Separation_Point_Storage = []
    SU_Inspector_Location_2 = 0
    while SU_Inspector_Location_2 <= len(SVGFile_Separation_Point) - 2:
        if SVGFile_Separation_Point[SU_Inspector_Location_2] != SVGFile_Separation_Point[SU_Inspector_Location_2 + 1]:
            SVGFile_Separation_Point_Storage.append(SVGFile_Separation_Point[SU_Inspector_Location_2])
        SU_Inspector_Location_2 += 1
        if SU_Inspector_Location_2 == len(SVGFile_Separation_Point) - 1:
            SVGFile_Separation_Point_Storage.append(SVGFile_Separation_Point[SU_Inspector_Location_2])
    SVGFile_Separation_Point = SVGFile_Separation_Point_Storage

def Start_Separation(SVGFile):
    global SVGFile_Separation_Point, Question_Number, Target_Height, Bug_Reporter, SVGFile_Number, SVGFile_Name_List, Broken_Matrix
    Question_Count = len(SVGFile_Separation_Point) - 1
    if Question_Count <= 1 or Question_Count > 6:
        if Broken_Matrix <= 3:
            Bug_Reporter.write(SVGFile_Name_List[SVGFile_Number])
            Bug_Reporter.write('\n')
            Bug_Reporter.flush()
            Bug_File_Copier()
    Question_Number = 0
    #Find the number of questions
    while Question_Number <= Question_Count - 1 and Broken_Matrix <= 4:
        #print('    Extracting one question', end = '')
        
        SU_Inspector_Location = 1
        Product = open(Product_Storage_Location + '/WareHouse' + '/' + SVGFile_Name_List[SVGFile_Number][:-4] + '_' + str(Question_Number) + '.svg', 'w', encoding='utf-8')
        Product.write(SVGFile_Header)
        Product.flush()
        Upper_Boundary = float(SVGFile_Separation_Point[Question_Number]) #上边界
        Lower_Boundary = float(SVGFile_Separation_Point[Question_Number + 1]) #下边界
        while SU_Inspector_Location <= len(SVGFile) - 1:
            if SVGFile[SU_Inspector_Location : SU_Inspector_Location + 3] == 'y="' and SVGFile[SU_Inspector_Location - 1] == ' ':
                SU_Inspector_Location += 3
                Coordinate_Y_Storage = ''
                while True:
                    if SVGFile[SU_Inspector_Location] == '"':
                        break
                    Coordinate_Y_Storage = Coordinate_Y_Storage + SVGFile[SU_Inspector_Location]
                    SU_Inspector_Location += 1
                #假如Y值在区间内
                if float(Coordinate_Y_Storage) >= Upper_Boundary - 5.5 and float(Coordinate_Y_Storage) < Lower_Boundary - 5.5:
                    #Record the label
                    while True:
                        if SVGFile[SU_Inspector_Location] == '<':
                            SU_Inspector_Location += 1
                            break
                        SU_Inspector_Location += -1
                    Label_Storage = '<'
                    End_Label_Count = 0
                    while True:
                        if SVGFile[SU_Inspector_Location] == '>':
                            if End_Label_Count == 1:
                                SU_Inspector_Location += 1
                                break
                            else:
                                End_Label_Count = 1
                        Label_Storage = Label_Storage + SVGFile[SU_Inspector_Location]
                        SU_Inspector_Location += 1
                    Label_Storage = Label_Storage + ">"
                    Product.write(Label_Storage)
                    Product.flush()
            
            if SVGFile[SU_Inspector_Location : SU_Inspector_Location + 9] == '<svg:path':
                Highest_Point = 0
                Lowest_Point = 9999999999999999999999999999999999999
                In_Tag_Check = 1
                while In_Tag_Check:
                    if SVGFile[SU_Inspector_Location : SU_Inspector_Location + 3] == 'd="' and SVGFile[SU_Inspector_Location - 1] == ' ':
                        SU_Inspector_Location += 4
                        Y_Value_Storage = ''
                        In_Tag_Check = 1
                        while In_Tag_Check:
                            Y_Value_Storage = ''
                            if SVGFile[SU_Inspector_Location] == 'Z' or SVGFile[SU_Inspector_Location] == '"':
                                break
                            if SVGFile[SU_Inspector_Location] == ' ':
                                SU_Inspector_Location += 1

                                while True:
                                    if SVGFile[SU_Inspector_Location] == ' ':
                                        SU_Inspector_Location += 1
                                        break
                                    SU_Inspector_Location += 1

                                while True:
                                    if SVGFile[SU_Inspector_Location] == ' ' or SVGFile[SU_Inspector_Location] == '"':
                                        if float(Y_Value_Storage) < Lowest_Point:
                                            Lowest_Point = float(Y_Value_Storage)
                                        if float(Y_Value_Storage) > Highest_Point:
                                            Highest_Point = float(Y_Value_Storage)
                                        if SVGFile[SU_Inspector_Location + 1] == 'M' or SVGFile[SU_Inspector_Location + 1] == 'L' or SVGFile[SU_Inspector_Location + 1] == 'C':
                                            SU_Inspector_Location += 2
                                        if SVGFile[SU_Inspector_Location + 1] == 'Z' or SVGFile[SU_Inspector_Location] == '"':
                                            In_Tag_Check = 0
                                        break
                                    Y_Value_Storage = Y_Value_Storage + SVGFile[SU_Inspector_Location]
                                    SU_Inspector_Location += 1
                    SU_Inspector_Location += 1

                if Lowest_Point >= Upper_Boundary and Highest_Point < Lower_Boundary:
                    Keep_Writing_Path_Tag = 1
                    while Keep_Writing_Path_Tag:
                        if SVGFile[SU_Inspector_Location : SU_Inspector_Location + 9] == '<svg:path':
                            SU_Inspector_Location += 9
                            Product.write('<svg:path')
                            Product.flush()

                            End_Tag_Indicator = 0 
                            while True:
                                if SVGFile[SU_Inspector_Location] == '>':
                                    if End_Tag_Indicator == 1:
                                        Product.write('>')
                                        Product.flush()
                                        SU_Inspector_Location += 1
                                        Keep_Writing_Path_Tag = 0
                                        break
                                    if End_Tag_Indicator == 0:
                                        End_Tag_Indicator = 1
                                Product.write(SVGFile[SU_Inspector_Location])
                                Product.flush()
                                SU_Inspector_Location += 1

                        SU_Inspector_Location += -1
    
            if SVGFile[SU_Inspector_Location : SU_Inspector_Location + 9] == '<svg:text':
                Product.write('<svg:text  xml:space="preserve">')
                Product.flush()
                SU_Inspector_Location += 9

            if SVGFile[SU_Inspector_Location : SU_Inspector_Location + 10] == '</svg:text':
                Product.write('</svg:text>')
                Product.flush()
                SU_Inspector_Location += 10

            if SVGFile[SU_Inspector_Location : SU_Inspector_Location + 9] == '<svg:defs':
                while True:
                    if SVGFile[SU_Inspector_Location : SU_Inspector_Location + 11] == '</svg:defs>':
                        SU_Inspector_Location += 11
                        Product.write('</svg:defs>')
                        Product.flush()
                        break
                    Product.write(SVGFile[SU_Inspector_Location])
                    Product.flush()
                    SU_Inspector_Location += 1

            SU_Inspector_Location += 1
        Product.write('</svg:svg>')
        Product.flush()
        Product.close()
        Relocate_Rewrite_Coordinates()
        Question_Number += 1
        
        #print('  ---Finished')

def Separation():
    global SVGFile, SVGFile_Separation_Point, SVGFile_Product_Open_Location
    SVGFile_Open = open(SVGFile_Product_Open_Location, 'r', encoding='utf-8')
    SVGFile = SVGFile_Open.read()
    SVGFile_Separation_Point = []
    #print('  Defining the Target-Height', end='')
    Find_Separation_Location(SVGFile)
    #print('    ---Success')
    #print('  Start file separation')
    Start_Separation(SVGFile)

def Relocate_Rewrite_Coordinates():     #分割后的文件的坐标仍然是在页面中的位置，它将它们移上去
    global Question_Number, SVGFile, Target_Height, SVGFile_Number, Product_Storage_Location, SVGFile_Name_List, SVGFile_Upper_Blank
    SVGFile_Open = open(Product_Storage_Location + '/WareHouse' + '/' + SVGFile_Name_List[SVGFile_Number][:-4] + '_' + str(Question_Number) + '.svg', 'r', encoding='utf-8')
    SVGFile = SVGFile_Open.read()
    Target_Height = float(SVGFile_Separation_Point[Question_Number])

    Product = open(Product_Storage_Location + '/WareHouse' + '/' + SVGFile_Name_List[SVGFile_Number][:-4] + '_' + str(Question_Number) + '.svg', 'w', encoding='utf-8')
    Inspector_Location = 0
    while Inspector_Location <= len(SVGFile) - 1:
        #print('Point 1')
        if SVGFile[Inspector_Location : Inspector_Location + 3] == 'y="' and SVGFile[Inspector_Location - 1] == ' ':
            Inspector_Location += 3
            Y_Value_Storage = ''
            while True:
                if SVGFile[Inspector_Location] == '"':
                    Product.write('y="' + str(float(Y_Value_Storage) - (Target_Height - SVGFile_Upper_Blank) ))
                    Product.flush()
                    break
                Y_Value_Storage = Y_Value_Storage + SVGFile[Inspector_Location]
                Inspector_Location += 1
        
        if SVGFile[Inspector_Location : Inspector_Location + 3] == 'd="' and SVGFile[Inspector_Location - 1] == ' ':
            Inspector_Location += 4

            Product.write('d="M')
            Product.flush()

            Y_Value_Storage = ''
            In_Tag_Check = 1
            while In_Tag_Check:
                #print('Point 2')
                Y_Value_Storage = ''
                if SVGFile[Inspector_Location] == '"':
                    Product.write('" ')
                    Product.flush()
                    Inspector_Location += 1
                    break

                if SVGFile[Inspector_Location] == ' ':
                    Product.write(' ')
                    Product.flush()
                    Inspector_Location += 1

                    if SVGFile[Inspector_Location] == 'M':
                        Product.write('M ')
                        Product.flush()
                        Inspector_Location += 2
                    if SVGFile[Inspector_Location] == 'L':
                        Product.write('L ')
                        Product.flush()
                        Inspector_Location += 2
                    if SVGFile[Inspector_Location] == 'C':
                        Product.write('C ')
                        Product.flush()
                        Inspector_Location += 2
                    
                    while True:
                        if SVGFile[Inspector_Location] == ' ':
                            Product.write(' ')
                            Product.flush()
                            Inspector_Location += 1
                            break
                        Product.write(SVGFile[Inspector_Location])
                        Product.flush()
                        Inspector_Location += 1
                    while True:
                        if SVGFile[Inspector_Location] == ' ' or SVGFile[Inspector_Location] == '"':
                            Product.write(str(float(Y_Value_Storage) - (Target_Height - SVGFile_Upper_Blank)))
                            Product.flush()
                            if SVGFile[Inspector_Location] == ' ':
                                Product.write(' ')
                                Product.flush()
                            if SVGFile[Inspector_Location + 1] == 'M':
                                Product.write('M')
                                Product.flush()
                                Inspector_Location += 2
                            if SVGFile[Inspector_Location + 1] == 'L':
                                Product.write('L')
                                Product.flush()
                                Inspector_Location += 2
                            if SVGFile[Inspector_Location + 1] == 'C':
                                Product.write('C')
                                Product.flush()
                                Inspector_Location += 2

                            if SVGFile[Inspector_Location + 1] == 'Z':
                                Product.write('Z')
                                Product.flush()
                                Inspector_Location += 2
                            break
                        
                        Y_Value_Storage = Y_Value_Storage + SVGFile[Inspector_Location]
                        Inspector_Location += 1
        Product.write(SVGFile[Inspector_Location])
        Product.flush()
        Inspector_Location += 1
#Print time
def Print_Time():
    global SVGFile_Number, Time_Start
    os.system("cls")
    print("Mofish Pastpaper Separator [For Chemistry Multiple Choice]   Ver.15\n")
    if SVGFile_Number >= 1:
        #时间计算
        Average_Time = (time.perf_counter() - Time_Start) / SVGFile_Number
        Average_Time_Left = Average_Time * (len(SVGFile_Name_List) - SVGFile_Number)
        if time.perf_counter() - Time_Start > 60:
            Second_left = (time.perf_counter() - Time_Start) - ((time.perf_counter() - Time_Start) // 60) * 60
            print('Total time taken: ' + str(int((time.perf_counter() - Time_Start) // 60)) + 'min ' + str(round(Second_left, 2)) + 's', end='')
        else:
            print('Total time taken: ' + str(round(time.perf_counter() - Time_Start, 2)) + 's', end='')   
        print('    Average Time taken: ' + str(round((time.perf_counter() - Time_Start) / SVGFile_Number, 2)) + 's per file', end='')
        if Average_Time_Left > 60:
            Second_left = Average_Time_Left - (Average_Time_Left // 60) * 60
            print('    Averge time left: ' + str(int(Average_Time_Left // 60)) + 'min ' + str(round(Second_left, 2)) + 's', end='\n\n')
        else:
            print('    Averge time left: ' + str(round(Average_Time_Left, 2)) + 's', end='\n\n')   
    else:
        print('Total time taken: ' + str(round(time.perf_counter() - Time_Start, 2)) + 's', end='')

    print('    Processed ' + str(SVGFile_Number) + ' files; ' + str(len(SVGFile_Name_List) - SVGFile_Number) + ' File(s) left', end='')
    Percentage = (SVGFile_Number + 1) / len(SVGFile_Name_List)
    Percentage_Left = 1 - Percentage
    Percentage_Block = 0
    Percentage_Left_Block = 0
    print('    Processing file: ' + SVGFile_Name_List[SVGFile_Number], end = '')
    print('\n      |', end='')
    while Percentage_Block <= Percentage:
        print('#', end='')
        Percentage_Block += 0.02
    while Percentage_Left_Block <= Percentage_Left:
        print(' ', end='')
        Percentage_Left_Block += 0.02
    print('|', end='  ')
    print(str(round(Percentage * 100, 2)) + '%', end='\n\n')


os.system("cls")
#获取所有文件地址
for root, dirs, files in os.walk(SVG_Storage, topdown=True):
    for name in files:
        if re.match('.*(.svg)', os.path.join(name)) is not None:
                SVGFile_Location_List.append(os.path.join(root) + '/' + os.path.join(name))
                SVGFile_Name_List.append(os.path.join(name))

Bug_Reporter_Open_Location = Product_Storage_Location + '/' + 'Bug_Reporter.txt'
Bug_Reporter = open(Bug_Reporter_Open_Location, 'w', encoding='utf-8')

while SVGFile_Number <= len(SVGFile_Name_List) - 1:
    Blank_Page_Check = 1
    if SVGFile_Name_List[SVGFile_Number][-6 : -4] == '-1': #不处理试卷封面
        SVGFile_Number += 1
    #显示部分
    Print_Time()

    #print("Start rewriting: " + SVGFile_Name_List[SVGFile_Number], end='  ')
    Bug_Reporter.write("Start rewriting: " + SVGFile_Name_List[SVGFile_Number]) #writing logfile
    Bug_Reporter.flush()
    Rewrite_SVG()  #去除Matrix
    #print("  ---Complete")
    Bug_Reporter.write('  ---Complete' + '\n')
    Bug_Reporter.flush()
    if Blank_Page_Check == 0:
        #print('--BLANK PAGE--')
        Bug_Reporter.write('--BLANK PAGE--' + '\n')
        Bug_Reporter.flush()
    else:
        #print("Separate: " + SVGFile_Name_List[SVGFile_Number])
        Bug_Reporter.write("Separate: " + SVGFile_Name_List[SVGFile_Number] + '\n')
        Bug_Reporter.flush()
        Separation()
        #print("Finished one page")
        Bug_Reporter.write("Finished one page" + '\n')
        Bug_Reporter.flush()
        Broken_Matrix = 0
    #结尾
    SVGFile_Number += 1
    # Time_Storage = time.perf_counter()
    # Time_Taken_List.append(round(time.perf_counter() - Time_Storage, 3))


Time_End = time.perf_counter()
print('End of process. Total time taken: ' + str(round(Time_End - Time_Start, 3)) + 's')
