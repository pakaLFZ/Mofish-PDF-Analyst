import os
import time
# import win32api,win32con #需要Pip安装pywin
import re
import threading

# File storage information
SVG_STORAGE = "./SVGs"
SVG_FILE_LOCATION_LIST = []
SVG_FILE_NAME_LIST = []
PRODUCT_STORAGE_LOCATION = "./Product"
SVG_FILE_NUMBER = 0
BUG_FILE_LOCATION = './Product/BugFile'
# File information
INSPECTOR_LOCATION = 0
SVG_FILE_HEIGHT = ''
SVG_FILE_TRANSFORMATION_RECORDER = []
SVG_FILE_TAGLIST = []
SVG_FILE_TRANSFORMATION_TAG_LABEL = 0
COORDINATE_X = ''
COORDINATE_Y = ''
COORDINATE_X_LIST = []
COORDINATE_Y_LIST = []

# File indicators
# 0 means that the tag is not finished and the words between will be recorded
SVG_FILE_TAG_END_INDICATOR = 1
# SVG基础信息储存
SVG_FILE_HEADER = '<svg:svg xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:svg="http://www.w3.org/2000/svg" version="1.1">'
SVG_FILE_SEPARATION_POINT = []
SVG_FILE_UPPER_BLANK = 15  # 分割后SVG顶部留白区域
# Other information
TIME_START = time.perf_counter()
TIME_STORAGE = time.perf_counter()
#Time_Taken_List = []
BLACK_PAGE_CHECK = 1
# Bug Storage
BROKEN_MATRIX = 0  # 检测有多少不能处理的Matrix


# Other function
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
                    Name_Storage_2 = Name_Storage_1[:
                                                    Inner_Inspector_Location] + '"'
                    while True:
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


def Bug_File_Copier():
    global SVG_FILE_LOCATION_LIST, SVG_FILE_NUMBER, BUG_FILE_LOCATION, SVG_FILE_NAME_LIST
    File_Location_Storage = ''
    Command_Storage = ''
    File_Location_Storage = Space_Eliminator(
        SVG_FILE_LOCATION_LIST[SVG_FILE_NUMBER])
    Bug_File_Location_Storage = BUG_FILE_LOCATION + \
        '/' + SVG_FILE_NAME_LIST[SVG_FILE_NUMBER]
    File_Product_Location_Storage = Space_Eliminator(Bug_File_Location_Storage)
    Command_Storage = 'copy ' + File_Location_Storage + \
        ' ' + File_Product_Location_Storage
    print(Command_Storage)
    os.system(Command_Storage)
# Rewrite SVG


def Finding_Elements(SVGFile):
    global INSPECTOR_LOCATION, SVG_FILE_TRANSFORMATION_RECORDER, BROKEN_MATRIX, BLACK_PAGE_CHECK, Bug_Reporter, SVG_FILE_NUMBER, SVG_FILE_LOCATION_LIST
    SVG_FILE_TRANSFORMATION_RECORDER.append(SVG_FILE_TRANSFORMATION_TAG_LABEL)
    while INSPECTOR_LOCATION <= len(SVGFile) - 1:
        # Matrix
        if SVGFile[INSPECTOR_LOCATION: INSPECTOR_LOCATION + 7] == 'matrix(':
            INSPECTOR_LOCATION += 7
            First_Number = ''
            Second_Number = ''
            Third_Number = ''
            Last_Number = ''
            Translation_First_Number = ''
            Translation_Last_Number = ''

            while True:
                if SVGFile[INSPECTOR_LOCATION] == ' ':
                    INSPECTOR_LOCATION += 1
                    break
                First_Number = First_Number + SVGFile[INSPECTOR_LOCATION]
                INSPECTOR_LOCATION += 1
            while True:
                if SVGFile[INSPECTOR_LOCATION] == ' ':
                    INSPECTOR_LOCATION += 1
                    break
                Second_Number = Second_Number + SVGFile[INSPECTOR_LOCATION]
                INSPECTOR_LOCATION += 1
            while True:
                if SVGFile[INSPECTOR_LOCATION] == ' ':
                    INSPECTOR_LOCATION += 1
                    break
                Third_Number = Third_Number + SVGFile[INSPECTOR_LOCATION]
                INSPECTOR_LOCATION += 1
            while True:
                if SVGFile[INSPECTOR_LOCATION] == ' ':
                    INSPECTOR_LOCATION += 1
                    break
                Last_Number = Last_Number + SVGFile[INSPECTOR_LOCATION]
                INSPECTOR_LOCATION += 1
            while True:
                if SVGFile[INSPECTOR_LOCATION] == ' ':
                    INSPECTOR_LOCATION += 1
                    break
                Translation_First_Number = Translation_First_Number + \
                    SVGFile[INSPECTOR_LOCATION]
                INSPECTOR_LOCATION += 1
            while True:
                if SVGFile[INSPECTOR_LOCATION] == ')':
                    INSPECTOR_LOCATION += 1
                    break
                Translation_Last_Number = Translation_Last_Number + \
                    SVGFile[INSPECTOR_LOCATION]
                INSPECTOR_LOCATION += 1

            if float(Third_Number) != 0.0 or float(Second_Number) != 0.0:
                Matrix_Storage = 'Matrix(' + First_Number + ' ' + Second_Number + ' ' + Third_Number + \
                    ' ' + Last_Number + ' ' + Translation_First_Number + \
                    ' ' + Translation_Last_Number + ')'
                # print('##Unexpected matrix attribute: ' + Matrix_Storage)
                BROKEN_MATRIX += 1
                Bug_Reporter.write(
                    'File: ' + str(SVG_FILE_LOCATION_LIST[SVG_FILE_NUMBER]) + '\n' + '##Unexpected matrix attribute: ' + Matrix_Storage + '\n')
                Bug_Reporter.flush()

            SVG_FILE_TRANSFORMATION_RECORDER.append('Start_Translation')
            SVG_FILE_TRANSFORMATION_RECORDER.append(
                float(Translation_First_Number))
            SVG_FILE_TRANSFORMATION_RECORDER.append(
                float(Translation_Last_Number))
            SVG_FILE_TRANSFORMATION_RECORDER.append('End_Translation')
            SVG_FILE_TRANSFORMATION_RECORDER.append('Start_Scale')
            SVG_FILE_TRANSFORMATION_RECORDER.append(First_Number)
            if Last_Number[0] != '-':
                SVG_FILE_TRANSFORMATION_RECORDER.append(float(First_Number))
            if Last_Number[0] == '-':
                SVG_FILE_TRANSFORMATION_RECORDER.append(
                    float(First_Number) * -1)
            SVG_FILE_TRANSFORMATION_RECORDER.append('End_Scale')

        # Translation
        if SVGFile[INSPECTOR_LOCATION: INSPECTOR_LOCATION + 10] == 'translate(':
            INSPECTOR_LOCATION += 10
            SVG_FILE_TRANSFORMATION_RECORDER.append('Start_Translation')
            Translation_Width_Storage = ''
            Translation_Height_Storage = ''
            while True:
                if SVGFile[INSPECTOR_LOCATION] == ' ' or SVGFile[INSPECTOR_LOCATION] == ')':
                    SVG_FILE_TRANSFORMATION_RECORDER.append(
                        Translation_Width_Storage)
                    INSPECTOR_LOCATION += 1
                    break
                Translation_Width_Storage = Translation_Width_Storage + \
                    SVGFile[INSPECTOR_LOCATION]
                INSPECTOR_LOCATION += 1
            while True:
                if SVGFile[INSPECTOR_LOCATION] == ' ' or SVGFile[INSPECTOR_LOCATION] == ')':
                    INSPECTOR_LOCATION += 1
                    SVG_FILE_TRANSFORMATION_RECORDER.append(
                        Translation_Height_Storage)
                    break
                Translation_Height_Storage = Translation_Height_Storage + \
                    SVGFile[INSPECTOR_LOCATION]
                INSPECTOR_LOCATION += 1
            SVG_FILE_TRANSFORMATION_RECORDER.append('End_Translation')
        # Scale
        if SVGFile[INSPECTOR_LOCATION: INSPECTOR_LOCATION + 6] == 'scale(':
            INSPECTOR_LOCATION += 6
            SVG_FILE_TRANSFORMATION_RECORDER.append('Start_Scale')
            Scale_Width_Storage = ''
            Scale_Height_Storage = ''
            # X coordinate
            while True:
                if SVGFile[INSPECTOR_LOCATION: INSPECTOR_LOCATION + 2] == ', ':
                    INSPECTOR_LOCATION += 2
                    break
                if SVGFile[INSPECTOR_LOCATION] == ' ':
                    INSPECTOR_LOCATION += 1
                    break
                Scale_Width_Storage = Scale_Width_Storage + \
                    SVGFile[INSPECTOR_LOCATION]
                INSPECTOR_LOCATION += 1
            SVG_FILE_TRANSFORMATION_RECORDER.append(float(Scale_Width_Storage))
            # Y coordinate
            while True:
                if SVGFile[INSPECTOR_LOCATION] == ')':
                    INSPECTOR_LOCATION += 1
                    break
                Scale_Height_Storage = Scale_Height_Storage + \
                    SVGFile[INSPECTOR_LOCATION]
                INSPECTOR_LOCATION += 1

            SVG_FILE_TRANSFORMATION_RECORDER.append(float(Scale_Height_Storage))
            SVG_FILE_TRANSFORMATION_RECORDER.append('End_Scale')

        if SVGFile[INSPECTOR_LOCATION] == '"':
            INSPECTOR_LOCATION += 1
            break

        INSPECTOR_LOCATION += 1


def Coordinate_X_Converter():
    global COORDINATE_X_LIST, SVG_FILE_TRANSFORMATION_RECORDER, SVG_FILE_TRANSFORMATION_TAG_LABEL, SVGFile_Product
    Inner_Inspector_Location = -1
    while len(SVG_FILE_TRANSFORMATION_RECORDER) >= 1:
        if str(SVG_FILE_TRANSFORMATION_RECORDER[Inner_Inspector_Location]).isdigit():
            Inner_Inspector_Location += -1
        else:
            if str(SVG_FILE_TRANSFORMATION_RECORDER[Inner_Inspector_Location]) == 'End_Translation':
                # 提取Translation内容
                Inner_Inspector_Location += -2
                Inner_List_Inspector_Location = 0
                while Inner_List_Inspector_Location <= len(COORDINATE_X_LIST) - 1:
                    COORDINATE_X_LIST[Inner_List_Inspector_Location] = float(
                        COORDINATE_X_LIST[Inner_List_Inspector_Location]) + float(SVG_FILE_TRANSFORMATION_RECORDER[Inner_Inspector_Location])
                    Inner_List_Inspector_Location += 1
                Inner_Inspector_Location += -2
            if str(SVG_FILE_TRANSFORMATION_RECORDER[Inner_Inspector_Location]) == 'End_Scale':
                Inner_Inspector_Location += -2
                Inner_List_Inspector_Location = 0
                while Inner_List_Inspector_Location <= len(COORDINATE_X_LIST) - 1:
                    COORDINATE_X_LIST[Inner_List_Inspector_Location] = float(
                        COORDINATE_X_LIST[Inner_List_Inspector_Location]) * float(SVG_FILE_TRANSFORMATION_RECORDER[Inner_Inspector_Location])
                    Inner_List_Inspector_Location += 1
                Inner_Inspector_Location += -2
            if str(SVG_FILE_TRANSFORMATION_RECORDER[Inner_Inspector_Location]) == '1':
                break


def Coordinate_X_Analyst():
    global COORDINATE_X, COORDINATE_X_LIST, SVG_FILE_TRANSFORMATION_RECORDER, SVG_FILE_TRANSFORMATION_TAG_LABEL, SVGFile_Product
    Inner_Inspector_Location = 0
    COORDINATE_X_LIST = []
    # 将坐标由字符串转换成list
    while Inner_Inspector_Location <= len(COORDINATE_X) - 1:
        Coordinate_X_Inner_Storage = ''
        while True:
            if COORDINATE_X[Inner_Inspector_Location] == ' ':
                Inner_Inspector_Location += 1
                COORDINATE_X_LIST.append(Coordinate_X_Inner_Storage)
                break
            Coordinate_X_Inner_Storage = Coordinate_X_Inner_Storage + \
                COORDINATE_X[Inner_Inspector_Location]
            Inner_Inspector_Location += 1
            if Inner_Inspector_Location > len(COORDINATE_X) - 1:
                COORDINATE_X_LIST.append(Coordinate_X_Inner_Storage)
                break
    # 开始转换
    Coordinate_X_Converter()
    # 将List变成string
    COORDINATE_X = ''
    for List_Component in COORDINATE_X_LIST:
        COORDINATE_X = COORDINATE_X + str(List_Component) + ' '
    COORDINATE_X = COORDINATE_X[:-1]
    SVGFile_Product.write('x="')
    SVGFile_Product.write(COORDINATE_X)
    SVGFile_Product.write('" ')
    SVGFile_Product.flush()


def Coordinate_Y_Converter():
    global COORDINATE_Y_LIST, SVG_FILE_TRANSFORMATION_RECORDER, SVG_FILE_TRANSFORMATION_TAG_LABEL, SVGFile_Product
    Inner_Inspector_Location = -1
    while len(SVG_FILE_TRANSFORMATION_RECORDER) >= 1:
        if str(SVG_FILE_TRANSFORMATION_RECORDER[Inner_Inspector_Location]).isdigit():
            Inner_Inspector_Location += -1
        else:
            if str(SVG_FILE_TRANSFORMATION_RECORDER[Inner_Inspector_Location]) == 'End_Translation':
                # 提取Translation内容
                Inner_Inspector_Location += -1
                Inner_List_Inspector_Location = 0
                while Inner_List_Inspector_Location <= len(COORDINATE_Y_LIST) - 1:
                    COORDINATE_Y_LIST[Inner_List_Inspector_Location] = float(
                        COORDINATE_Y_LIST[Inner_List_Inspector_Location]) + float(SVG_FILE_TRANSFORMATION_RECORDER[Inner_Inspector_Location])
                    Inner_List_Inspector_Location += 1
                Inner_Inspector_Location += -3
            if str(SVG_FILE_TRANSFORMATION_RECORDER[Inner_Inspector_Location]) == 'End_Scale':
                Inner_Inspector_Location += -1
                Inner_List_Inspector_Location = 0
                while Inner_List_Inspector_Location <= len(COORDINATE_Y_LIST) - 1:
                    COORDINATE_Y_LIST[Inner_List_Inspector_Location] = float(
                        COORDINATE_Y_LIST[Inner_List_Inspector_Location]) * float(SVG_FILE_TRANSFORMATION_RECORDER[Inner_Inspector_Location])
                    Inner_List_Inspector_Location += 1
                Inner_Inspector_Location += -3
            if str(SVG_FILE_TRANSFORMATION_RECORDER[Inner_Inspector_Location]) == '1':
                break


def Coordinate_Y_Analyst():
    global COORDINATE_Y, COORDINATE_Y_LIST, SVG_FILE_TRANSFORMATION_RECORDER, SVG_FILE_TRANSFORMATION_TAG_LABEL, SVGFile_Product
    Inner_Inspector_Location = 0
    COORDINATE_Y_LIST = []
    # 将坐标由字符串转换成list
    while Inner_Inspector_Location <= len(COORDINATE_Y) - 1:
        Coordinate_Y_Inner_Storage = ''
        while Inner_Inspector_Location <= len(COORDINATE_Y) - 1:
            if COORDINATE_Y[Inner_Inspector_Location] == ' ':
                Inner_Inspector_Location += 1
                COORDINATE_Y_LIST.append(Coordinate_Y_Inner_Storage)
                break
            Coordinate_Y_Inner_Storage = Coordinate_Y_Inner_Storage + \
                COORDINATE_Y[Inner_Inspector_Location]
            Inner_Inspector_Location += 1
        COORDINATE_Y_LIST.append(Coordinate_Y_Inner_Storage)

    # 开始转换
    Coordinate_Y_Converter()
    # 将List变成string
    COORDINATE_Y = ''
    for List_Component in COORDINATE_Y_LIST:
        COORDINATE_Y = COORDINATE_Y + str(List_Component) + ' '
    COORDINATE_Y = COORDINATE_Y[:-1]
    SVGFile_Product.write('y="')
    SVGFile_Product.write(COORDINATE_Y)
    SVGFile_Product.write('" ')
    SVGFile_Product.flush()


def Path_Route_Analyst():
    global Path_Route, SVG_FILE_TRANSFORMATION_RECORDER, SVG_FILE_TRANSFORMATION_TAG_LABEL, SVGFile_Product, COORDINATE_X_LIST, COORDINATE_Y_LIST
    Inner_Inspector_Location = 0
    Path_Route_List = []
    # 将坐标由字符串转换成list
    while Inner_Inspector_Location <= len(Path_Route) - 1:
        Path_Route_Inner_Storage = ''
        while Inner_Inspector_Location <= len(Path_Route) - 1:
            if Path_Route[Inner_Inspector_Location] == ' ':
                Path_Route_List.append(Path_Route_Inner_Storage)
                Inner_Inspector_Location += 1
                break
            Path_Route_Inner_Storage = Path_Route_Inner_Storage + \
                Path_Route[Inner_Inspector_Location]
            Inner_Inspector_Location += 1
        if Inner_Inspector_Location > len(Path_Route) - 1:
            Path_Route_List.append(Path_Route_Inner_Storage)
    # 转换
    Inner_Inspector_Location = 0
    X_Check = 1  # 用来检测该坐标是否为X轴坐标，1为是，0为不是
    while Inner_Inspector_Location <= len(Path_Route_List) - 1:
        # print(Path_Route_List[Inner_Inspector_Location])
        if Path_Route_List[Inner_Inspector_Location] != 'M' and Path_Route_List[Inner_Inspector_Location] != 'L' and Path_Route_List[Inner_Inspector_Location] != 'H' and Path_Route_List[Inner_Inspector_Location] != 'C' and Path_Route_List[Inner_Inspector_Location] != 'V' and Path_Route_List[Inner_Inspector_Location] != 'S' and Path_Route_List[Inner_Inspector_Location] != 'Q' and Path_Route_List[Inner_Inspector_Location] != 'T' and Path_Route_List[Inner_Inspector_Location] != 'A' and Path_Route_List[Inner_Inspector_Location] != 'Z':
            if X_Check == 1 and Inner_Inspector_Location <= len(Path_Route_List) - 1:
                COORDINATE_X_LIST = []
                COORDINATE_X_LIST.append(
                    Path_Route_List[Inner_Inspector_Location])
                Coordinate_X_Converter()
                Path_Route_List[Inner_Inspector_Location] = str(
                    COORDINATE_X_LIST[0])
                Inner_Inspector_Location += 1
                X_Check = 0
            if X_Check == 0 and Inner_Inspector_Location <= len(Path_Route_List) - 1:
                COORDINATE_Y_LIST = []
                COORDINATE_Y_LIST.append(
                    Path_Route_List[Inner_Inspector_Location])
                Coordinate_Y_Converter()
                Path_Route_List[Inner_Inspector_Location] = str(
                    COORDINATE_Y_LIST[0])
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


def Stroke_Width_Analyst():
    global Stroke_Width, SVG_FILE_TRANSFORMATION_RECORDER, SVG_FILE_TRANSFORMATION_TAG_LABEL, SVGFile_Product
    Inner_Inspector_Location = -1
    while len(SVG_FILE_TRANSFORMATION_RECORDER) >= 1:
        if str(SVG_FILE_TRANSFORMATION_RECORDER[Inner_Inspector_Location]).isdigit():
            Inner_Inspector_Location += -1
        else:
            if str(SVG_FILE_TRANSFORMATION_RECORDER[Inner_Inspector_Location]) == 'End_Translation':
                Inner_Inspector_Location += -4
            if str(SVG_FILE_TRANSFORMATION_RECORDER[Inner_Inspector_Location]) == 'End_Scale':
                Inner_Inspector_Location += -2
                Stroke_Width = float(
                    Stroke_Width) * float(SVG_FILE_TRANSFORMATION_RECORDER[Inner_Inspector_Location])
                Inner_Inspector_Location += -2
            if str(SVG_FILE_TRANSFORMATION_RECORDER[Inner_Inspector_Location]) == '1':
                break


def Font_Size_Analyst():
    global Font_Size, SVG_FILE_TRANSFORMATION_RECORDER, SVG_FILE_TRANSFORMATION_TAG_LABEL, SVGFile_Product
    Inner_Inspector_Location = -1
    while len(SVG_FILE_TRANSFORMATION_RECORDER) >= 1:
        if str(SVG_FILE_TRANSFORMATION_RECORDER[Inner_Inspector_Location]).isdigit():
            Inner_Inspector_Location += -1
        else:
            if str(SVG_FILE_TRANSFORMATION_RECORDER[Inner_Inspector_Location]) == 'End_Translation':
                Inner_Inspector_Location += -4
            if str(SVG_FILE_TRANSFORMATION_RECORDER[Inner_Inspector_Location]) == 'End_Scale':
                Inner_Inspector_Location += -2
                Font_Size = float(
                    Font_Size) * float(SVG_FILE_TRANSFORMATION_RECORDER[Inner_Inspector_Location])
                Inner_Inspector_Location += -2
            if str(SVG_FILE_TRANSFORMATION_RECORDER[Inner_Inspector_Location]) == '1':
                break


def Rewrite_SVG():
    global INSPECTOR_LOCATION, BLACK_PAGE_CHECK, SVGFile, SVGFile_Product, SVG_FILE_TAGLIST, SVG_FILE_TRANSFORMATION_TAG_LABEL, SVG_FILE_TRANSFORMATION_RECORDER, Path_Route, COORDINATE_X, COORDINATE_Y, SVGFile_Product_Open_Location, Stroke_Width, Font_Size, OutMode_Indicator, SVGFile_Product_Open_Location
    INSPECTOR_LOCATION = 0
    SVGFile_Product_Open_Location = PRODUCT_STORAGE_LOCATION + \
        '/' + SVG_FILE_NAME_LIST[SVG_FILE_NUMBER]
    SVGFile_Open = open(
        SVG_FILE_LOCATION_LIST[SVG_FILE_NUMBER], 'r', encoding='utf-8')
    SVGFile = SVGFile_Open.read()
    SVGFile_Product = open(SVGFile_Product_Open_Location,
                           'w', encoding='utf-8')
    while INSPECTOR_LOCATION <= len(SVGFile) - 1:
        #print('Inspector: ' + str(INSPECTOR_LOCATION) + '    Code: ' + SVGFile[INSPECTOR_LOCATION - 10 : INSPECTOR_LOCATION + 10])
        if SVGFile[INSPECTOR_LOCATION] == '<' and SVGFile[INSPECTOR_LOCATION + 1] != '/':
            InTag_Transform_Exist = 0
            # print('a')
            while INSPECTOR_LOCATION <= len(SVGFile) - 1:
                # Detection for transformations
                if SVGFile[INSPECTOR_LOCATION: INSPECTOR_LOCATION + 10] == 'transform=':
                    INSPECTOR_LOCATION += 11
                    SVG_FILE_TRANSFORMATION_TAG_LABEL += 1
                    Finding_Elements(SVGFile)
                    InTag_Transform_Exist = 1
                    SVG_FILE_TAGLIST.append(SVG_FILE_TRANSFORMATION_TAG_LABEL)
                # Writing for the question content
                # 检测坐标
                # print('1')
                if SVGFile[INSPECTOR_LOCATION: INSPECTOR_LOCATION + 2] == 'y=' and SVGFile[INSPECTOR_LOCATION - 1] == ' ':
                    COORDINATE_Y = ''
                    INSPECTOR_LOCATION += 3
                    while True:
                        if SVGFile[INSPECTOR_LOCATION] == '"':
                            INSPECTOR_LOCATION += 1
                            break
                        COORDINATE_Y = COORDINATE_Y + \
                            SVGFile[INSPECTOR_LOCATION]
                        INSPECTOR_LOCATION += 1
                    Coordinate_Y_Analyst()

                if SVGFile[INSPECTOR_LOCATION: INSPECTOR_LOCATION + 2] == 'x=' and SVGFile[INSPECTOR_LOCATION - 1] == ' ':
                    COORDINATE_X = ''
                    INSPECTOR_LOCATION += 3
                    while True:
                        if SVGFile[INSPECTOR_LOCATION] == '"':
                            INSPECTOR_LOCATION += 1
                            break
                        COORDINATE_X = COORDINATE_X + \
                            SVGFile[INSPECTOR_LOCATION]
                        INSPECTOR_LOCATION += 1
                    Coordinate_X_Analyst()

                if SVGFile[INSPECTOR_LOCATION: INSPECTOR_LOCATION + 2] == 'd=' and SVGFile[INSPECTOR_LOCATION - 1] == ' ':
                    Path_Route = ''
                    INSPECTOR_LOCATION += 3
                    while True:
                        if SVGFile[INSPECTOR_LOCATION] == '"':
                            INSPECTOR_LOCATION += 1
                            break
                        Path_Route = Path_Route + SVGFile[INSPECTOR_LOCATION]
                        INSPECTOR_LOCATION += 1
                    Path_Route_Analyst()

                if SVGFile[INSPECTOR_LOCATION: INSPECTOR_LOCATION + 13] == 'stroke-width=' and SVGFile[INSPECTOR_LOCATION - 1] == ' ':
                    INSPECTOR_LOCATION += 14
                    SVGFile_Product.write('stroke-width="')
                    SVGFile_Product.flush()
                    Stroke_Width_Recorder = ''
                    while True:
                        if SVGFile[INSPECTOR_LOCATION] == '"':
                            INSPECTOR_LOCATION += 1
                            break
                        Stroke_Width_Recorder = Stroke_Width_Recorder + \
                            SVGFile[INSPECTOR_LOCATION]
                        INSPECTOR_LOCATION += 1
                    Stroke_Width = float(Stroke_Width_Recorder[:-2])
                    Stroke_Width_Analyst()
                    SVGFile_Product.write(str(Stroke_Width) + 'px')
                    SVGFile_Product.write('" ')
                    SVGFile_Product.flush()
                # print('5')
                if SVGFile[INSPECTOR_LOCATION: INSPECTOR_LOCATION + 11] == 'font-size="' and SVGFile[INSPECTOR_LOCATION - 1] == ' ':
                    INSPECTOR_LOCATION += 11
                    SVGFile_Product.write('font-size="')
                    SVGFile_Product.flush()
                    Font_Size_Recorder = ''
                    while True:
                        if SVGFile[INSPECTOR_LOCATION] == '"':
                            INSPECTOR_LOCATION += 1
                            break
                        Font_Size_Recorder = Font_Size_Recorder + \
                            SVGFile[INSPECTOR_LOCATION]
                        INSPECTOR_LOCATION += 1
                    Font_Size = float(Font_Size_Recorder[:-2])
                    Font_Size_Analyst()
                    SVGFile_Product.write(str(Font_Size) + 'px')
                    SVGFile_Product.write('" ')
                    SVGFile_Product.flush()
                # print('6')
                if SVGFile[INSPECTOR_LOCATION] == '>':
                    SVGFile_Product.write('>')
                    SVGFile_Product.flush()
                    INSPECTOR_LOCATION += 1
                    while True:
                        if SVGFile[INSPECTOR_LOCATION: INSPECTOR_LOCATION + 10] == 'BLANK PAGE':
                            BLACK_PAGE_CHECK = 0
                            break
                        if SVGFile[INSPECTOR_LOCATION] == '<':
                            break
                        SVGFile_Product.write(SVGFile[INSPECTOR_LOCATION])
                        SVGFile_Product.flush()
                        INSPECTOR_LOCATION += 1
                    # Record for Taglist
                    if InTag_Transform_Exist == 0:
                        SVG_FILE_TAGLIST.append(0)
                        InTag_Transform_Exist = 0
                    # 结束循环
                    break
                # print('7')
                # Writing for the tag content
                SVGFile_Product.write(SVGFile[INSPECTOR_LOCATION])
                SVGFile_Product.flush()
                INSPECTOR_LOCATION += 1
            # print('b')

        if SVGFile[INSPECTOR_LOCATION: INSPECTOR_LOCATION + 2] == '</':
            # Dealing with the recording of Tags
            if len(SVG_FILE_TAGLIST) != 0:
                if SVG_FILE_TAGLIST[-1] != 0:
                    # print(SVG_FILE_TRANSFORMATION_RECORDER)
                    # print(SVG_FILE_TAGLIST)
                    SVG_FILE_TAGLIST = SVG_FILE_TAGLIST[:-1]
                    while True:
                        if SVG_FILE_TRANSFORMATION_RECORDER[-1] == SVG_FILE_TRANSFORMATION_TAG_LABEL:
                            SVG_FILE_TRANSFORMATION_RECORDER = SVG_FILE_TRANSFORMATION_RECORDER[:-1]
                            SVG_FILE_TRANSFORMATION_TAG_LABEL += -1
                            break
                        SVG_FILE_TRANSFORMATION_RECORDER = SVG_FILE_TRANSFORMATION_RECORDER[:-1]
                else:
                    SVG_FILE_TAGLIST = SVG_FILE_TAGLIST[:-1]
            # Filling the tag content
            while INSPECTOR_LOCATION <= len(SVGFile) - 1:
                if SVGFile[INSPECTOR_LOCATION] == '>':
                    SVGFile_Product.write('>')
                    SVGFile_Product.flush()
                    INSPECTOR_LOCATION += 1
                    break
                SVGFile_Product.write(SVGFile[INSPECTOR_LOCATION])
                SVGFile_Product.flush()
                INSPECTOR_LOCATION += 1

        if INSPECTOR_LOCATION <= len(SVGFile) - 1:
            if SVGFile[INSPECTOR_LOCATION] != '<':
                INSPECTOR_LOCATION += 1
# Separate SVG


def Find_Separation_Location(SVGFile):  # 寻找分割点
    global SVG_FILE_SEPARATION_POINT
    SU_Inspector_Location = 0
    while SU_Inspector_Location < len(SVGFile) - 1:
        if SVGFile[SU_Inspector_Location: SU_Inspector_Location + 10] == '<svg:tspan':
            if SVGFile[SU_Inspector_Location + 24: SU_Inspector_Location + 31] == 'g_font_' or SVGFile[SU_Inspector_Location + 24: SU_Inspector_Location + 33] == 'Helvetica':
                SU_Inspector_Location_3 = SU_Inspector_Location + 31
                Font_Type_No_1 = ''
                while True:
                    if SVGFile[SU_Inspector_Location_3] == '"':
                        break
                    Font_Type_No_1 = Font_Type_No_1 + \
                        SVGFile[SU_Inspector_Location_3]
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

                # Get rid of </svg:tspan>
                while First_Task:
                    if SVGFile[SU_Inspector_Location_1] == '>':
                        First_Block = 1
                        SU_Inspector_Location_1 += 1
                        break
                    SU_Inspector_Location_1 += 1
                while First_Task:
                    if SVGFile[SU_Inspector_Location_1] == '>':
                        break
                    if SVGFile[SU_Inspector_Location_1: SU_Inspector_Location_1 + 7] == 'g_font_' and First_Block == 1:
                        SU_Inspector_Location_3 = SU_Inspector_Location_1 + 7
                        Font_Type_No_2 = ''
                        while True:
                            if SVGFile[SU_Inspector_Location_3] == '"':
                                break
                            Font_Type_No_2 = Font_Type_No_2 + \
                                SVGFile[SU_Inspector_Location_3]
                            SU_Inspector_Location_3 += 1
                        if Font_Type_No_1 != Font_Type_No_2:
                            Second_Task = 1
                        break

                    if SVGFile[SU_Inspector_Location_1: SU_Inspector_Location_1 + 9] == 'Helvetica' and First_Block == 1:
                        Second_Task = 1

                    SU_Inspector_Location_1 += 1
                Sentence_Length = 0
                while Second_Task:
                    if SVGFile[SU_Inspector_Location_1] == '>':
                        SU_Inspector_Location_1 += 1
                        while True:
                            if SVGFile[SU_Inspector_Location] == '©' or SVGFile[SU_Inspector_Location: SU_Inspector_Location + 5] == '0620/':
                                SU_Inspector_Location_1 = SU_Inspector_Location
                                SU_Inspector_Location += 1
                                Coordinate_Storage = ''
                                Block_End = 1
                                while Block_End:
                                    if SVGFile[SU_Inspector_Location_1: SU_Inspector_Location_1 + 3] == 'y="':
                                        SU_Inspector_Location_1 += 3
                                        while True:
                                            if SVGFile[SU_Inspector_Location_1] == '"':
                                                SVG_FILE_SEPARATION_POINT.append(
                                                    Coordinate_Storage)
                                                Block_End = 0
                                                break
                                            Coordinate_Storage = Coordinate_Storage + \
                                                SVGFile[SU_Inspector_Location_1]
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
                        if SVGFile[SU_Inspector_Location: SU_Inspector_Location + 3] == 'y="' and SVGFile[SU_Inspector_Location - 1] == ' ':
                            SU_Inspector_Location += 3
                            while True:
                                if SVGFile[SU_Inspector_Location] == '"':
                                    SVG_FILE_SEPARATION_POINT.append(
                                        Coordinate_Storage)
                                    SU_Inspector_Location += 1
                                    Block_End = 0
                                    break
                                Coordinate_Storage = Coordinate_Storage + \
                                    SVGFile[SU_Inspector_Location]
                                SU_Inspector_Location += 1
                        SU_Inspector_Location += 1

        if SVGFile[SU_Inspector_Location] == '©' or SVGFile[SU_Inspector_Location: SU_Inspector_Location + 5] == '0620/':
            SU_Inspector_Location_1 = SU_Inspector_Location
            SU_Inspector_Location += 1
            Coordinate_Storage = ''
            Block_End = 1
            while Block_End:
                if SVGFile[SU_Inspector_Location_1: SU_Inspector_Location_1 + 3] == 'y="':
                    SU_Inspector_Location_1 += 3
                    while True:
                        if SVGFile[SU_Inspector_Location_1] == '"':
                            SVG_FILE_SEPARATION_POINT.append(Coordinate_Storage)
                            Block_End = 0
                            break
                        Coordinate_Storage = Coordinate_Storage + \
                            SVGFile[SU_Inspector_Location_1]
                        SU_Inspector_Location_1 += 1
                SU_Inspector_Location_1 += -1
            # print('@')
            # print(SVG_FILE_SEPARATION_POINT)
        SU_Inspector_Location += 1
    # 排序 从左到右按从小到大排序
    SVGFile_Separation_Point_Storage = ''
    SU_Inspector_Location_2 = 0
    while True:
        Sequence_Check = 0  # 如果为0，则表示顺序已经正确
        if SU_Inspector_Location_2 <= len(SVG_FILE_SEPARATION_POINT) - 2:
            if float(SVG_FILE_SEPARATION_POINT[SU_Inspector_Location_2]) - float(SVG_FILE_SEPARATION_POINT[SU_Inspector_Location_2 + 1]) > 0:
                SVGFile_Separation_Point_Storage = SVG_FILE_SEPARATION_POINT[SU_Inspector_Location_2]
                SVG_FILE_SEPARATION_POINT[SU_Inspector_Location_2] = SVG_FILE_SEPARATION_POINT[SU_Inspector_Location_2 + 1]
                SVG_FILE_SEPARATION_POINT[SU_Inspector_Location_2 +
                                         1] = SVGFile_Separation_Point_Storage
                SU_Inspector_Location_2 += 1
                Sequence_Check = 1
            else:
                SU_Inspector_Location_2 += 1

        if SU_Inspector_Location_2 >= len(SVG_FILE_SEPARATION_POINT) - 1:
            if Sequence_Check == 1:
                SU_Inspector_Location_2 = 0
            else:
                break
            #SU_Inspector_Location_2 = 0
    if len(SVG_FILE_SEPARATION_POINT) <= 1:
        SVG_FILE_SEPARATION_POINT = []
    # print("    File " + SVG_FILE_NAME_LIST[SVG_FILE_NUMBER] + "'s separation points are:    ", end = '')
    # print(SVG_FILE_SEPARATION_POINT)
    # 过滤
    SVGFile_Separation_Point_Storage = []
    SU_Inspector_Location_2 = 0
    while SU_Inspector_Location_2 <= len(SVG_FILE_SEPARATION_POINT) - 2:
        if SVG_FILE_SEPARATION_POINT[SU_Inspector_Location_2] != SVG_FILE_SEPARATION_POINT[SU_Inspector_Location_2 + 1]:
            SVGFile_Separation_Point_Storage.append(
                SVG_FILE_SEPARATION_POINT[SU_Inspector_Location_2])
        SU_Inspector_Location_2 += 1
        if SU_Inspector_Location_2 == len(SVG_FILE_SEPARATION_POINT) - 1:
            SVGFile_Separation_Point_Storage.append(
                SVG_FILE_SEPARATION_POINT[SU_Inspector_Location_2])
    SVG_FILE_SEPARATION_POINT = SVGFile_Separation_Point_Storage


def Start_Separation(SVGFile):
    global SVG_FILE_SEPARATION_POINT, Question_Number, Target_Height, Bug_Reporter, SVG_FILE_NUMBER, SVG_FILE_NAME_LIST, BROKEN_MATRIX
    Question_Count = len(SVG_FILE_SEPARATION_POINT) - 1
    if Question_Count <= 1 or Question_Count > 6:
        if BROKEN_MATRIX <= 3:
            Bug_Reporter.write(SVG_FILE_NAME_LIST[SVG_FILE_NUMBER])
            Bug_Reporter.write('\n')
            Bug_Reporter.flush()
            Bug_File_Copier()
    Question_Number = 0
    # Find the number of questions
    while Question_Number <= Question_Count - 1 and BROKEN_MATRIX <= 4:
        #print('    Extracting one question', end = '')

        SU_Inspector_Location = 1
        Product = open(PRODUCT_STORAGE_LOCATION + '/WareHouse' + '/' +
                       SVG_FILE_NAME_LIST[SVG_FILE_NUMBER][:-4] + '_' + str(Question_Number) + '.svg', 'w', encoding='utf-8')
        Product.write(SVG_FILE_HEADER)
        Product.flush()
        Upper_Boundary = float(
            SVG_FILE_SEPARATION_POINT[Question_Number])  # 上边界
        Lower_Boundary = float(
            SVG_FILE_SEPARATION_POINT[Question_Number + 1])  # 下边界
        while SU_Inspector_Location <= len(SVGFile) - 1:
            if SVGFile[SU_Inspector_Location: SU_Inspector_Location + 3] == 'y="' and SVGFile[SU_Inspector_Location - 1] == ' ':
                SU_Inspector_Location += 3
                Coordinate_Y_Storage = ''
                while True:
                    if SVGFile[SU_Inspector_Location] == '"':
                        break
                    Coordinate_Y_Storage = Coordinate_Y_Storage + \
                        SVGFile[SU_Inspector_Location]
                    SU_Inspector_Location += 1
                # 假如Y值在区间内
                if float(Coordinate_Y_Storage) >= Upper_Boundary - 5.5 and float(Coordinate_Y_Storage) < Lower_Boundary - 5.5:
                    # Record the label
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
                        Label_Storage = Label_Storage + \
                            SVGFile[SU_Inspector_Location]
                        SU_Inspector_Location += 1
                    Label_Storage = Label_Storage + ">"
                    Product.write(Label_Storage)
                    Product.flush()

            if SVGFile[SU_Inspector_Location: SU_Inspector_Location + 9] == '<svg:path':
                Highest_Point = 0
                Lowest_Point = 9999999999999999999999999999999999999
                In_Tag_Check = 1
                while In_Tag_Check:
                    if SVGFile[SU_Inspector_Location: SU_Inspector_Location + 3] == 'd="' and SVGFile[SU_Inspector_Location - 1] == ' ':
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
                                            Lowest_Point = float(
                                                Y_Value_Storage)
                                        if float(Y_Value_Storage) > Highest_Point:
                                            Highest_Point = float(
                                                Y_Value_Storage)
                                        if SVGFile[SU_Inspector_Location + 1] == 'M' or SVGFile[SU_Inspector_Location + 1] == 'L' or SVGFile[SU_Inspector_Location + 1] == 'C':
                                            SU_Inspector_Location += 2
                                        if SVGFile[SU_Inspector_Location + 1] == 'Z' or SVGFile[SU_Inspector_Location] == '"':
                                            In_Tag_Check = 0
                                        break
                                    Y_Value_Storage = Y_Value_Storage + \
                                        SVGFile[SU_Inspector_Location]
                                    SU_Inspector_Location += 1
                    SU_Inspector_Location += 1

                if Lowest_Point >= Upper_Boundary and Highest_Point < Lower_Boundary:
                    Keep_Writing_Path_Tag = 1
                    while Keep_Writing_Path_Tag:
                        if SVGFile[SU_Inspector_Location: SU_Inspector_Location + 9] == '<svg:path':
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

            if SVGFile[SU_Inspector_Location: SU_Inspector_Location + 9] == '<svg:text':
                Product.write('<svg:text  xml:space="preserve">')
                Product.flush()
                SU_Inspector_Location += 9

            if SVGFile[SU_Inspector_Location: SU_Inspector_Location + 10] == '</svg:text':
                Product.write('</svg:text>')
                Product.flush()
                SU_Inspector_Location += 10

            if SVGFile[SU_Inspector_Location: SU_Inspector_Location + 9] == '<svg:defs':
                while True:
                    if SVGFile[SU_Inspector_Location: SU_Inspector_Location + 11] == '</svg:defs>':
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
    global SVGFile, SVG_FILE_SEPARATION_POINT, SVGFile_Product_Open_Location
    SVGFile_Open = open(SVGFile_Product_Open_Location, 'r', encoding='utf-8')
    SVGFile = SVGFile_Open.read()
    SVG_FILE_SEPARATION_POINT = []
    #print('  Defining the Target-Height', end='')
    Find_Separation_Location(SVGFile)
    #print('    ---Success')
    #print('  Start file separation')
    Start_Separation(SVGFile)


def Relocate_Rewrite_Coordinates():
    global Question_Number, SVGFile, Target_Height, SVG_FILE_NUMBER, PRODUCT_STORAGE_LOCATION, SVG_FILE_NAME_LIST, SVG_FILE_UPPER_BLANK
    SVGFile_Open = open(PRODUCT_STORAGE_LOCATION + '/WareHouse' + '/' +
                        SVG_FILE_NAME_LIST[SVG_FILE_NUMBER][:-4] + '_' + str(Question_Number) + '.svg', 'r', encoding='utf-8')
    SVGFile = SVGFile_Open.read()
    Target_Height = float(SVG_FILE_SEPARATION_POINT[Question_Number])

    Product = open(PRODUCT_STORAGE_LOCATION + '/WareHouse' + '/' +
                   SVG_FILE_NAME_LIST[SVG_FILE_NUMBER][:-4] + '_' + str(Question_Number) + '.svg', 'w', encoding='utf-8')
    INSPECTOR_LOCATION = 0
    while INSPECTOR_LOCATION <= len(SVGFile) - 1:
        #print('Point 1')
        if SVGFile[INSPECTOR_LOCATION: INSPECTOR_LOCATION + 3] == 'y="' and SVGFile[INSPECTOR_LOCATION - 1] == ' ':
            INSPECTOR_LOCATION += 3
            Y_Value_Storage = ''
            while True:
                if SVGFile[INSPECTOR_LOCATION] == '"':
                    Product.write(
                        'y="' + str(float(Y_Value_Storage) - (Target_Height - SVG_FILE_UPPER_BLANK)))
                    Product.flush()
                    break
                Y_Value_Storage = Y_Value_Storage + SVGFile[INSPECTOR_LOCATION]
                INSPECTOR_LOCATION += 1

        if SVGFile[INSPECTOR_LOCATION: INSPECTOR_LOCATION + 3] == 'd="' and SVGFile[INSPECTOR_LOCATION - 1] == ' ':
            INSPECTOR_LOCATION += 4

            Product.write('d="M')
            Product.flush()

            Y_Value_Storage = ''
            In_Tag_Check = 1
            while In_Tag_Check:
                #print('Point 2')
                Y_Value_Storage = ''
                if SVGFile[INSPECTOR_LOCATION] == '"':
                    Product.write('" ')
                    Product.flush()
                    INSPECTOR_LOCATION += 1
                    break

                if SVGFile[INSPECTOR_LOCATION] == ' ':
                    Product.write(' ')
                    Product.flush()
                    INSPECTOR_LOCATION += 1

                    if SVGFile[INSPECTOR_LOCATION] == 'M':
                        Product.write('M ')
                        Product.flush()
                        INSPECTOR_LOCATION += 2
                    if SVGFile[INSPECTOR_LOCATION] == 'L':
                        Product.write('L ')
                        Product.flush()
                        INSPECTOR_LOCATION += 2
                    if SVGFile[INSPECTOR_LOCATION] == 'C':
                        Product.write('C ')
                        Product.flush()
                        INSPECTOR_LOCATION += 2

                    while True:
                        if SVGFile[INSPECTOR_LOCATION] == ' ':
                            Product.write(' ')
                            Product.flush()
                            INSPECTOR_LOCATION += 1
                            break
                        Product.write(SVGFile[INSPECTOR_LOCATION])
                        Product.flush()
                        INSPECTOR_LOCATION += 1
                    while True:
                        if SVGFile[INSPECTOR_LOCATION] == ' ' or SVGFile[INSPECTOR_LOCATION] == '"':
                            Product.write(
                                str(float(Y_Value_Storage) - (Target_Height - SVG_FILE_UPPER_BLANK)))
                            Product.flush()
                            if SVGFile[INSPECTOR_LOCATION] == ' ':
                                Product.write(' ')
                                Product.flush()
                            if SVGFile[INSPECTOR_LOCATION + 1] == 'M':
                                Product.write('M')
                                Product.flush()
                                INSPECTOR_LOCATION += 2
                            if SVGFile[INSPECTOR_LOCATION + 1] == 'L':
                                Product.write('L')
                                Product.flush()
                                INSPECTOR_LOCATION += 2
                            if SVGFile[INSPECTOR_LOCATION + 1] == 'C':
                                Product.write('C')
                                Product.flush()
                                INSPECTOR_LOCATION += 2

                            if SVGFile[INSPECTOR_LOCATION + 1] == 'Z':
                                Product.write('Z')
                                Product.flush()
                                INSPECTOR_LOCATION += 2
                            break

                        Y_Value_Storage = Y_Value_Storage + \
                            SVGFile[INSPECTOR_LOCATION]
                        INSPECTOR_LOCATION += 1
        Product.write(SVGFile[INSPECTOR_LOCATION])
        Product.flush()
        INSPECTOR_LOCATION += 1
# Print time


def Print_Time():
    global SVG_FILE_NUMBER, TIME_START
    os.system("cls")
    print(
        "Mofish Pastpaper Separator [For Chemistry Multiple Choice]   Ver.15\n")
    if SVG_FILE_NUMBER >= 1:
        # 时间计算
        Average_Time = (time.perf_counter() - TIME_START) / SVG_FILE_NUMBER
        Average_Time_Left = Average_Time * \
            (len(SVG_FILE_NAME_LIST) - SVG_FILE_NUMBER)
        if time.perf_counter() - TIME_START > 60:
            Second_left = (time.perf_counter() - TIME_START) - \
                ((time.perf_counter() - TIME_START) // 60) * 60
            print('Total time taken: ' + str(int((time.perf_counter() - TIME_START) //
                                                 60)) + 'min ' + str(round(Second_left, 2)) + 's', end='')
        else:
            print('Total time taken: ' +
                  str(round(time.perf_counter() - TIME_START, 2)) + 's', end='')
        print('    Average Time taken: ' + str(round((time.perf_counter() -
                                                      TIME_START) / SVG_FILE_NUMBER, 2)) + 's per file', end='')
        if Average_Time_Left > 60:
            Second_left = Average_Time_Left - (Average_Time_Left // 60) * 60
            print('    Averge time left: ' + str(int(Average_Time_Left // 60)
                                                 ) + 'min ' + str(round(Second_left, 2)) + 's', end='\n\n')
        else:
            print('    Averge time left: ' +
                  str(round(Average_Time_Left, 2)) + 's', end='\n\n')
    else:
        print('Total time taken: ' +
              str(round(time.perf_counter() - TIME_START, 2)) + 's', end='')

    print('    Processed ' + str(SVG_FILE_NUMBER) + ' files; ' +
          str(len(SVG_FILE_NAME_LIST) - SVG_FILE_NUMBER) + ' File(s) left', end='')
    Percentage = (SVG_FILE_NUMBER + 1) / len(SVG_FILE_NAME_LIST)
    Percentage_Left = 1 - Percentage
    Percentage_Block = 0
    Percentage_Left_Block = 0
    print('    Processing file: ' + SVG_FILE_NAME_LIST[SVG_FILE_NUMBER], end='')
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
# 获取所有文件地址
for root, dirs, files in os.walk(SVG_STORAGE, topdown=True):
    for name in files:
        if re.match('.*(.svg)', os.path.join(name)) is not None:
            SVG_FILE_LOCATION_LIST.append(
                os.path.join(root) + '/' + os.path.join(name))
            SVG_FILE_NAME_LIST.append(os.path.join(name))

Bug_Reporter_Open_Location = PRODUCT_STORAGE_LOCATION + '/' + 'Bug_Reporter.txt'
Bug_Reporter = open(Bug_Reporter_Open_Location, 'w', encoding='utf-8')

while SVG_FILE_NUMBER <= len(SVG_FILE_NAME_LIST) - 1:
    BLACK_PAGE_CHECK = 1
    if SVG_FILE_NAME_LIST[SVG_FILE_NUMBER][-6: -4] == '-1':  # 不处理试卷封面
        SVG_FILE_NUMBER += 1
    # 显示部分
    Print_Time()

    #print("Start rewriting: " + SVG_FILE_NAME_LIST[SVG_FILE_NUMBER], end='  ')
    Bug_Reporter.write("Start rewriting: " +
                       SVG_FILE_NAME_LIST[SVG_FILE_NUMBER])  # writing logfile
    Bug_Reporter.flush()
    Rewrite_SVG()  # 去除Matrix
    #print("  ---Complete")
    Bug_Reporter.write('  ---Complete' + '\n')
    Bug_Reporter.flush()
    if BLACK_PAGE_CHECK == 0:
        #print('--BLANK PAGE--')
        Bug_Reporter.write('--BLANK PAGE--' + '\n')
        Bug_Reporter.flush()
    else:
        #print("Separate: " + SVG_FILE_NAME_LIST[SVG_FILE_NUMBER])
        Bug_Reporter.write(
            "Separate: " + SVG_FILE_NAME_LIST[SVG_FILE_NUMBER] + '\n')
        Bug_Reporter.flush()
        Separation()
        #print("Finished one page")
        Bug_Reporter.write("Finished one page" + '\n')
        Bug_Reporter.flush()
        BROKEN_MATRIX = 0
    # 结尾
    SVG_FILE_NUMBER += 1
    # TIME_STORAGE = time.perf_counter()
    # Time_Taken_List.append(round(time.perf_counter() - TIME_STORAGE, 3))


TIME_END = time.perf_counter()
print('End of process. Total time taken: ' +
      str(round(TIME_END - TIME_START, 3)) + 's')
