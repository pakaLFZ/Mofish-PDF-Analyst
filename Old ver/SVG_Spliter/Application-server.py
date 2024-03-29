#!/usr/bin/env python
import os
import time
import re
import threading
#import logging # python logging


# File storage information
SVG_STORAGE = "/home/PDFs/SVGs"
SVG_FILE_LOCATION_LIST = []
SVG_FILE_NAME_LIST = []
PRODUCT_STORAGE_LOCATION = "/home/PDFs/Product"
SVG_FILE_NUMBER = 0
BUG_FILE_LOCATION = '/home/PDFs/Product/BugFile'
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
SVG_FILE_STORAGE = ''
QUESTION_NUMBER_LIST = []
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
BLACK_PAGE_CHECK = 1
Location_Indicator = 0
# Bug Storage
BROKEN_MATRIX = 0  # 检测有多少不能处理的Matrix


# Other function
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

def Bug_File_Copier():      #将有问题的文件复制到BugFile文件夹内
    global SVG_FILE_LOCATION_LIST, SVG_FILE_NUMBER, BUG_FILE_LOCATION, SVG_FILE_NAME_LIST
    #File_Location_Storage = ''
    #Command_Storage = ''
    #File_Location_Storage = Space_Eliminator(
    #    SVG_FILE_LOCATION_LIST[SVG_FILE_NUMBER])
    #Bug_File_Location_Storage = BUG_FILE_LOCATION + \
    #    '/' + SVG_FILE_NAME_LIST[SVG_FILE_NUMBER]
    #File_Product_Location_Storage = Space_Eliminator(Bug_File_Location_Storage)
    #Command_Storage = 'copy ' + File_Location_Storage + \
    #    ' ' + File_Product_Location_Storage
    #logging.debug(Command_Storage)
    #os.system(Command_Storage)
    print("-------Bug------")
# Rewrite SVG
def Finding_Elements(SVG_FILE):     #寻找所有的tranformation，并将他们记录下来。为之后修改坐标做准备
    global INSPECTOR_LOCATION, SVG_FILE_TRANSFORMATION_RECORDER, BROKEN_MATRIX, BLACK_PAGE_CHECK, BUG_REPORTER, SVG_FILE_NUMBER, SVG_FILE_LOCATION_LIST
    SVG_FILE_TRANSFORMATION_RECORDER.append(SVG_FILE_TRANSFORMATION_TAG_LABEL)
    #以下全是识别相关label然后记录在SVG_FILE_TRANSFORMATION_RECORDER内
    while INSPECTOR_LOCATION <= len(SVG_FILE) - 1:
        # Matrix
        if SVG_FILE[INSPECTOR_LOCATION: INSPECTOR_LOCATION + 7] == 'matrix(':
            INSPECTOR_LOCATION += 7
            First_Number = ''
            Second_Number = ''
            Third_Number = ''
            Last_Number = ''
            Translation_First_Number = ''
            Translation_Last_Number = ''

            while True:
                if SVG_FILE[INSPECTOR_LOCATION] == ' ':
                    INSPECTOR_LOCATION += 1
                    break
                First_Number = First_Number + SVG_FILE[INSPECTOR_LOCATION]
                INSPECTOR_LOCATION += 1
            while True:
                if SVG_FILE[INSPECTOR_LOCATION] == ' ':
                    INSPECTOR_LOCATION += 1
                    break
                Second_Number = Second_Number + SVG_FILE[INSPECTOR_LOCATION]
                INSPECTOR_LOCATION += 1
            while True:
                if SVG_FILE[INSPECTOR_LOCATION] == ' ':
                    INSPECTOR_LOCATION += 1
                    break
                Third_Number = Third_Number + SVG_FILE[INSPECTOR_LOCATION]
                INSPECTOR_LOCATION += 1
            while True:
                if SVG_FILE[INSPECTOR_LOCATION] == ' ':
                    INSPECTOR_LOCATION += 1
                    break
                Last_Number = Last_Number + SVG_FILE[INSPECTOR_LOCATION]
                INSPECTOR_LOCATION += 1
            while True:
                if SVG_FILE[INSPECTOR_LOCATION] == ' ':
                    INSPECTOR_LOCATION += 1
                    break
                Translation_First_Number = Translation_First_Number + \
                    SVG_FILE[INSPECTOR_LOCATION]
                INSPECTOR_LOCATION += 1
            while True:
                if SVG_FILE[INSPECTOR_LOCATION] == ')':
                    INSPECTOR_LOCATION += 1
                    break
                Translation_Last_Number = Translation_Last_Number + \
                    SVG_FILE[INSPECTOR_LOCATION]
                INSPECTOR_LOCATION += 1

            if float(Third_Number) != 0.0 or float(Second_Number) != 0.0:
                Matrix_Storage = 'Matrix(' + First_Number + ' ' + Second_Number + ' ' + Third_Number + \
                    ' ' + Last_Number + ' ' + Translation_First_Number + \
                    ' ' + Translation_Last_Number + ')'
                BROKEN_MATRIX += 1
                BUG_REPORTER.write(
                    'File: ' + str(SVG_FILE_LOCATION_LIST[SVG_FILE_NUMBER]) + '\n' + '##Unexpected matrix attribute: ' + Matrix_Storage + '\n')
                BUG_REPORTER.flush()

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
        if SVG_FILE[INSPECTOR_LOCATION: INSPECTOR_LOCATION + 10] == 'translate(':
            INSPECTOR_LOCATION += 10
            SVG_FILE_TRANSFORMATION_RECORDER.append('Start_Translation')
            Translation_Width_Storage = ''
            Translation_Height_Storage = ''
            while True:
                if SVG_FILE[INSPECTOR_LOCATION] == ' ' or SVG_FILE[INSPECTOR_LOCATION] == ')':
                    SVG_FILE_TRANSFORMATION_RECORDER.append(
                        Translation_Width_Storage)
                    INSPECTOR_LOCATION += 1
                    break
                Translation_Width_Storage = Translation_Width_Storage + \
                    SVG_FILE[INSPECTOR_LOCATION]
                INSPECTOR_LOCATION += 1
            while True:
                if SVG_FILE[INSPECTOR_LOCATION] == ' ' or SVG_FILE[INSPECTOR_LOCATION] == ')':
                    INSPECTOR_LOCATION += 1
                    SVG_FILE_TRANSFORMATION_RECORDER.append(
                        Translation_Height_Storage)
                    break
                Translation_Height_Storage = Translation_Height_Storage + \
                    SVG_FILE[INSPECTOR_LOCATION]
                INSPECTOR_LOCATION += 1
            SVG_FILE_TRANSFORMATION_RECORDER.append('End_Translation')
        # Scale
        if SVG_FILE[INSPECTOR_LOCATION: INSPECTOR_LOCATION + 6] == 'scale(':
            INSPECTOR_LOCATION += 6
            SVG_FILE_TRANSFORMATION_RECORDER.append('Start_Scale')
            Scale_Width_Storage = ''
            Scale_Height_Storage = ''
            # X coordinate
            while True:
                if SVG_FILE[INSPECTOR_LOCATION: INSPECTOR_LOCATION + 2] == ', ':
                    INSPECTOR_LOCATION += 2
                    break
                if SVG_FILE[INSPECTOR_LOCATION] == ' ':
                    INSPECTOR_LOCATION += 1
                    break
                Scale_Width_Storage = Scale_Width_Storage + \
                    SVG_FILE[INSPECTOR_LOCATION]
                INSPECTOR_LOCATION += 1
            SVG_FILE_TRANSFORMATION_RECORDER.append(float(Scale_Width_Storage))
            # Y coordinate
            while True:
                if SVG_FILE[INSPECTOR_LOCATION] == ')':
                    INSPECTOR_LOCATION += 1
                    break
                Scale_Height_Storage = Scale_Height_Storage + \
                    SVG_FILE[INSPECTOR_LOCATION]
                INSPECTOR_LOCATION += 1

            SVG_FILE_TRANSFORMATION_RECORDER.append(float(Scale_Height_Storage))
            SVG_FILE_TRANSFORMATION_RECORDER.append('End_Scale')

        if SVG_FILE[INSPECTOR_LOCATION] == '"':
            INSPECTOR_LOCATION += 1
            break

        INSPECTOR_LOCATION += 1

def Coordinate_X_Converter():   #根据Finding_Elements记录下来的transformation记录（SVGFile_Transformation_Recorder）修改坐标值
    global COORDINATE_X_LIST, SVG_FILE_TRANSFORMATION_RECORDER, SVG_FILE_TRANSFORMATION_TAG_LABEL, SVG_FILE_PRODUCT, SVG_FILE_STORAGE
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

def Coordinate_X_Analyst():     #有时坐标是一串的，它的作用是将一串坐标变成一个list
    global COORDINATE_X, COORDINATE_X_LIST, SVG_FILE_TRANSFORMATION_RECORDER, SVG_FILE_TRANSFORMATION_TAG_LABEL, SVG_FILE_PRODUCT, SVG_FILE_STORAGE
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
    SVG_FILE_STORAGE = SVG_FILE_STORAGE + 'x="'
    SVG_FILE_STORAGE = SVG_FILE_STORAGE + COORDINATE_X
    SVG_FILE_STORAGE = SVG_FILE_STORAGE + '" '
    
def Coordinate_Y_Converter():
    global COORDINATE_Y_LIST, SVG_FILE_TRANSFORMATION_RECORDER, SVG_FILE_TRANSFORMATION_TAG_LABEL, SVG_FILE_PRODUCT
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
    global COORDINATE_Y, COORDINATE_Y_LIST, SVG_FILE_TRANSFORMATION_RECORDER, SVG_FILE_TRANSFORMATION_TAG_LABEL, SVG_FILE_STORAGE
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
    SVG_FILE_STORAGE = SVG_FILE_STORAGE + 'y="'
    SVG_FILE_STORAGE = SVG_FILE_STORAGE + COORDINATE_Y
    SVG_FILE_STORAGE = SVG_FILE_STORAGE + '" '
    
def Path_Route_Analyst():        #将Path里的坐标提炼出来用Coordinate_X_Converter()和Coordinate_Y_Converter()转换坐标
    global PATH_ROUTE, SVG_FILE_TRANSFORMATION_RECORDER, SVG_FILE_TRANSFORMATION_TAG_LABEL, COORDINATE_X_LIST, COORDINATE_Y_LIST, SVG_FILE_STORAGE
    Inner_Inspector_Location = 0
    Path_Route_List = []
    # 将坐标由字符串转换成list
    while Inner_Inspector_Location <= len(PATH_ROUTE) - 1:
        Path_Route_Inner_Storage = ''
        while Inner_Inspector_Location <= len(PATH_ROUTE) - 1:
            if PATH_ROUTE[Inner_Inspector_Location] == ' ':
                Path_Route_List.append(Path_Route_Inner_Storage)
                Inner_Inspector_Location += 1
                break
            Path_Route_Inner_Storage = Path_Route_Inner_Storage + \
                PATH_ROUTE[Inner_Inspector_Location]
            Inner_Inspector_Location += 1
        if Inner_Inspector_Location > len(PATH_ROUTE) - 1:
            Path_Route_List.append(Path_Route_Inner_Storage)
    # 转换
    Inner_Inspector_Location = 0
    X_Check = 1  # 用来检测该坐标是否为X轴坐标，1为是，0为不是
    while Inner_Inspector_Location <= len(Path_Route_List) - 1:
        # logging.debug(Path_Route_List[Inner_Inspector_Location])
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
    PATH_ROUTE = ''
    for List_Component in Path_Route_List:
        PATH_ROUTE = PATH_ROUTE + str(List_Component) + ' '
    PATH_ROUTE = PATH_ROUTE[:-1]
    SVG_FILE_STORAGE = SVG_FILE_STORAGE + 'd="'
    SVG_FILE_STORAGE = SVG_FILE_STORAGE + PATH_ROUTE
    SVG_FILE_STORAGE = SVG_FILE_STORAGE + '" '
    
def Stroke_Width_Analyst():     #修改线条宽度
    global STROKE_WIDTH, SVG_FILE_TRANSFORMATION_RECORDER, SVG_FILE_TRANSFORMATION_TAG_LABEL, SVG_FILE_STORAGE
    Inner_Inspector_Location = -1
    while len(SVG_FILE_TRANSFORMATION_RECORDER) >= 1:
        if str(SVG_FILE_TRANSFORMATION_RECORDER[Inner_Inspector_Location]).isdigit():
            Inner_Inspector_Location += -1
        else:
            if str(SVG_FILE_TRANSFORMATION_RECORDER[Inner_Inspector_Location]) == 'End_Translation':
                Inner_Inspector_Location += -4
            if str(SVG_FILE_TRANSFORMATION_RECORDER[Inner_Inspector_Location]) == 'End_Scale':
                Inner_Inspector_Location += -2
                STROKE_WIDTH = float(
                    STROKE_WIDTH) * float(SVG_FILE_TRANSFORMATION_RECORDER[Inner_Inspector_Location])
                Inner_Inspector_Location += -2
            if str(SVG_FILE_TRANSFORMATION_RECORDER[Inner_Inspector_Location]) == '1':
                break

def Font_Size_Analyst():        #修改字体宽度
    global FONT_SIZE, SVG_FILE_TRANSFORMATION_RECORDER, SVG_FILE_TRANSFORMATION_TAG_LABEL, SVG_FILE_STORAGE
    Inner_Inspector_Location = -1
    while len(SVG_FILE_TRANSFORMATION_RECORDER) >= 1:
        if str(SVG_FILE_TRANSFORMATION_RECORDER[Inner_Inspector_Location]).isdigit():
            Inner_Inspector_Location += -1
        else:
            if str(SVG_FILE_TRANSFORMATION_RECORDER[Inner_Inspector_Location]) == 'End_Translation':
                Inner_Inspector_Location += -4
            if str(SVG_FILE_TRANSFORMATION_RECORDER[Inner_Inspector_Location]) == 'End_Scale':
                Inner_Inspector_Location += -2
                FONT_SIZE = float(
                    FONT_SIZE) * float(SVG_FILE_TRANSFORMATION_RECORDER[Inner_Inspector_Location])
                Inner_Inspector_Location += -2
            if str(SVG_FILE_TRANSFORMATION_RECORDER[Inner_Inspector_Location]) == '1':
                break

def Rewrite_SVG():          #去除文件中的transformation并利用以上工具转换坐标
    global INSPECTOR_LOCATION, BLACK_PAGE_CHECK, SVG_FILE, SVG_FILE_PRODUCT, SVG_FILE_TAGLIST, SVG_FILE_TRANSFORMATION_TAG_LABEL, SVG_FILE_TRANSFORMATION_RECORDER, PATH_ROUTE, COORDINATE_X, COORDINATE_Y, STROKE_WIDTH, FONT_SIZE, OUT_MODE_INDICATOR, SVG_FILE_STORAGE, BUG_REPORTER
    INSPECTOR_LOCATION = 0
    SVGFile_Open = open(
        SVG_FILE_LOCATION_LIST[SVG_FILE_NUMBER], 'r', encoding='utf-8')
    SVG_FILE = SVGFile_Open.read()
    SVG_FILE_STORAGE = ''
    while INSPECTOR_LOCATION <= len(SVG_FILE) - 1:
        if SVG_FILE[INSPECTOR_LOCATION] == '<' and SVG_FILE[INSPECTOR_LOCATION + 1] != '/':
            InTag_Transform_Exist = 0
            while INSPECTOR_LOCATION <= len(SVG_FILE) - 1:
                # Detection for transformations
                if SVG_FILE[INSPECTOR_LOCATION: INSPECTOR_LOCATION + 10] == 'transform=':
                    INSPECTOR_LOCATION += 11
                    SVG_FILE_TRANSFORMATION_TAG_LABEL += 1
                    Finding_Elements(SVG_FILE)
                    InTag_Transform_Exist = 1
                    SVG_FILE_TAGLIST.append(SVG_FILE_TRANSFORMATION_TAG_LABEL)
                # Writing for the question content
                # 检测坐标
                if SVG_FILE[INSPECTOR_LOCATION: INSPECTOR_LOCATION + 2] == 'y=' and SVG_FILE[INSPECTOR_LOCATION - 1] == ' ':
                    COORDINATE_Y = ''
                    INSPECTOR_LOCATION += 3
                    while True:
                        if SVG_FILE[INSPECTOR_LOCATION] == '"':
                            INSPECTOR_LOCATION += 1
                            break
                        COORDINATE_Y = COORDINATE_Y + \
                            SVG_FILE[INSPECTOR_LOCATION]
                        INSPECTOR_LOCATION += 1
                    Coordinate_Y_Analyst()

                if SVG_FILE[INSPECTOR_LOCATION: INSPECTOR_LOCATION + 2] == 'x=' and SVG_FILE[INSPECTOR_LOCATION - 1] == ' ':
                    COORDINATE_X = ''
                    INSPECTOR_LOCATION += 3
                    while True:
                        if SVG_FILE[INSPECTOR_LOCATION] == '"':
                            INSPECTOR_LOCATION += 1
                            break
                        COORDINATE_X = COORDINATE_X + \
                            SVG_FILE[INSPECTOR_LOCATION]
                        INSPECTOR_LOCATION += 1
                    Coordinate_X_Analyst()

                if SVG_FILE[INSPECTOR_LOCATION: INSPECTOR_LOCATION + 2] == 'd=' and SVG_FILE[INSPECTOR_LOCATION - 1] == ' ':
                    PATH_ROUTE = ''
                    INSPECTOR_LOCATION += 3
                    while True:
                        if SVG_FILE[INSPECTOR_LOCATION] == '"':
                            INSPECTOR_LOCATION += 1
                            break
                        PATH_ROUTE = PATH_ROUTE + SVG_FILE[INSPECTOR_LOCATION]
                        INSPECTOR_LOCATION += 1
                    Path_Route_Analyst()

                if SVG_FILE[INSPECTOR_LOCATION: INSPECTOR_LOCATION + 13] == 'stroke-width=' and SVG_FILE[INSPECTOR_LOCATION - 1] == ' ':
                    INSPECTOR_LOCATION += 14
                    SVG_FILE_STORAGE = SVG_FILE_STORAGE + 'stroke-width="'
                    Stroke_Width_Recorder = ''
                    while True:
                        if SVG_FILE[INSPECTOR_LOCATION] == '"':
                            INSPECTOR_LOCATION += 1
                            break
                        Stroke_Width_Recorder = Stroke_Width_Recorder + \
                            SVG_FILE[INSPECTOR_LOCATION]
                        INSPECTOR_LOCATION += 1
                    STROKE_WIDTH = float(Stroke_Width_Recorder[:-2])
                    Stroke_Width_Analyst()
                    SVG_FILE_STORAGE = SVG_FILE_STORAGE + str(STROKE_WIDTH) + 'px'
                    SVG_FILE_STORAGE = SVG_FILE_STORAGE + '" '
                    
                if SVG_FILE[INSPECTOR_LOCATION: INSPECTOR_LOCATION + 11] == 'font-size="' and SVG_FILE[INSPECTOR_LOCATION - 1] == ' ':
                    INSPECTOR_LOCATION += 11
                    SVG_FILE_STORAGE = SVG_FILE_STORAGE + 'font-size="'
                    
                    Font_Size_Recorder = ''
                    while True:
                        if SVG_FILE[INSPECTOR_LOCATION] == '"':
                            INSPECTOR_LOCATION += 1
                            break
                        Font_Size_Recorder = Font_Size_Recorder + \
                            SVG_FILE[INSPECTOR_LOCATION]
                        INSPECTOR_LOCATION += 1
                    FONT_SIZE = float(Font_Size_Recorder[:-2])
                    Font_Size_Analyst()
                    SVG_FILE_STORAGE = SVG_FILE_STORAGE + str(FONT_SIZE) + 'px'
                    SVG_FILE_STORAGE = SVG_FILE_STORAGE + '" '
                    
                if SVG_FILE[INSPECTOR_LOCATION] == '>':
                    SVG_FILE_STORAGE = SVG_FILE_STORAGE + '>'
                    
                    INSPECTOR_LOCATION += 1
                    while True:
                        if SVG_FILE[INSPECTOR_LOCATION: INSPECTOR_LOCATION + 10] == 'BLANK PAGE':
                            BLACK_PAGE_CHECK = 0
                            break
                        if SVG_FILE[INSPECTOR_LOCATION] == '<':
                            break
                        SVG_FILE_STORAGE = SVG_FILE_STORAGE + SVG_FILE[INSPECTOR_LOCATION]
                        
                        INSPECTOR_LOCATION += 1
                    # Record for Taglist
                    if InTag_Transform_Exist == 0:
                        SVG_FILE_TAGLIST.append(0)
                        InTag_Transform_Exist = 0
                    # 结束循环
                    break
                # Writing for the tag content
                SVG_FILE_STORAGE = SVG_FILE_STORAGE + SVG_FILE[INSPECTOR_LOCATION]     
                INSPECTOR_LOCATION += 1
        if SVG_FILE[INSPECTOR_LOCATION: INSPECTOR_LOCATION + 2] == '</':
            # Dealing with the recording of Tags
            if len(SVG_FILE_TAGLIST) != 0:
                if SVG_FILE_TAGLIST[-1] != 0:
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
            while INSPECTOR_LOCATION <= len(SVG_FILE) - 1:
                if SVG_FILE[INSPECTOR_LOCATION] == '>':
                    SVG_FILE_STORAGE = SVG_FILE_STORAGE + '>'
                    INSPECTOR_LOCATION += 1
                    break
                SVG_FILE_STORAGE = SVG_FILE_STORAGE + SVG_FILE[INSPECTOR_LOCATION]
                INSPECTOR_LOCATION += 1
        if INSPECTOR_LOCATION <= len(SVG_FILE) - 1:
            if SVG_FILE[INSPECTOR_LOCATION] != '<':
                INSPECTOR_LOCATION += 1
# Separate SVG
def Page_Ending_Detecter():
    global SVG_FILE, SU_Inspector_Location, Page_Ending_Indicator, Paper_End_Type, SVG_FILE_SEPARATION_POINT
    if SVG_FILE[SU_Inspector_Location: SU_Inspector_Location + 10] == 'Permission':
        Paper_End_Type = 1
        Page_Ending_Indicator = 1

    #0625/01/M/J/0
    if SVG_FILE[SU_Inspector_Location + 4] == '/' and  SVG_FILE[SU_Inspector_Location + 7] == '/':
        if Paper_End_Type == 1:
            pass
        else:
            Page_Ending_Indicator = 1
            Paper_End_Type = 2

    if SVG_FILE[SU_Inspector_Location] == '©':
        if Paper_End_Type == 1 or Paper_End_Type == 2:
            pass
        else:
            Page_Ending_Indicator = 1

    if Page_Ending_Indicator == 1:
        SU_Inspector_Location_1 = SU_Inspector_Location
        SU_Inspector_Location += 1
        Coordinate_Storage = ''
        Block_End = 1
        while Block_End:
            if SVG_FILE[SU_Inspector_Location_1: SU_Inspector_Location_1 + 3] == 'y="' and SVG_FILE[SU_Inspector_Location_1 - 1] == ' ':
                SU_Inspector_Location_1 += 3
                while True:
                    if SVG_FILE[SU_Inspector_Location_1] == '"':
                        #将坐标写入表
                        if Paper_End_Type == 1:
                            SVG_FILE_SEPARATION_POINT.append(str(float(Coordinate_Storage) - 50))
                        else:
                            SVG_FILE_SEPARATION_POINT.append(str(float(Coordinate_Storage) - 20))
                        Block_End = 0
                        break
                    Coordinate_Storage = Coordinate_Storage + SVG_FILE[SU_Inspector_Location_1]
                    SU_Inspector_Location_1 += 1
            SU_Inspector_Location_1 += -1
        Page_Ending_Indicator = 0

def Find_Separation_Location(SVG_FILE):  # 寻找分割点
    global SVG_FILE_SEPARATION_POINT, QUESTION_NUMBER_LIST, Page_Ending_Indicator, Paper_End_Type, SU_Inspector_Location
    SU_Inspector_Location = 0
    QUESTION_NUMBER_LIST = []
    Paper_End_Type = 0
    Page_Ending_Indicator= 0
    while SU_Inspector_Location < len(SVG_FILE) - 1:
        if SVG_FILE[SU_Inspector_Location: SU_Inspector_Location + 10] == '<svg:tspan':
            if SVG_FILE[SU_Inspector_Location + 24: SU_Inspector_Location + 31] == 'g_font_' or SVG_FILE[SU_Inspector_Location + 24: SU_Inspector_Location + 33] == 'Helvetica':        #找到目标
                SU_Inspector_Location_3 = SU_Inspector_Location + 31
                Font_Type_No_1 = ''
                while True:
                    if SVG_FILE[SU_Inspector_Location_3] == '"':
                        break
                    Font_Type_No_1 = Font_Type_No_1 + \
                        SVG_FILE[SU_Inspector_Location_3]
                    SU_Inspector_Location_3 += 1
                It_Is_Question_Number = 0
                First_Task = 0
                Second_Task = 0
                First_Block = 0
                SU_Inspector_Location_1 = SU_Inspector_Location
                SU_Inspector_Location += 1
                while True:
                    if SVG_FILE[SU_Inspector_Location_1] == '>':
                        SU_Inspector_Location_1 += 1
                        break
                    SU_Inspector_Location_1 += 1
                #题号位置  --->分析是不是题号数字
                First_Number = 0
                QUESTION_NUMBER_STORAGE = ''
                while True:
                    if First_Number == 0:
                        if SVG_FILE[SU_Inspector_Location_1].isdigit() and SVG_FILE[SU_Inspector_Location_1] != ' ':
                            QUESTION_NUMBER_STORAGE = QUESTION_NUMBER_STORAGE + str(SVG_FILE[SU_Inspector_Location_1])
                            SU_Inspector_Location_1 += 1
                            First_Number = 1
                        else:
                            break
                    else:
                        if SVG_FILE[SU_Inspector_Location_1].isdigit() or SVG_FILE[SU_Inspector_Location_1] == ' ':
                            if SVG_FILE[SU_Inspector_Location_1].isdigit():
                                QUESTION_NUMBER_STORAGE = QUESTION_NUMBER_STORAGE + str(SVG_FILE[SU_Inspector_Location_1])
                            SU_Inspector_Location_1 += 1
                        else:
                            break
                    if SVG_FILE[SU_Inspector_Location_1] == '<':
                        First_Task = 1
                        break
                while First_Task:# Get rid of </svg:tspan>
                    if SVG_FILE[SU_Inspector_Location_1] == '>':
                        First_Block = 1
                        SU_Inspector_Location_1 += 1
                        break
                    SU_Inspector_Location_1 += 1
                #对比字体   --->第二部检测
                while First_Task:
                    if SVG_FILE[SU_Inspector_Location_1] == '>':
                        break

                    if SVG_FILE[SU_Inspector_Location_1: SU_Inspector_Location_1 + 7] == 'g_font_' and First_Block == 1:
                        SU_Inspector_Location_3 = SU_Inspector_Location_1 + 7
                        Font_Type_No_2 = ''
                        while True:
                            if SVG_FILE[SU_Inspector_Location_3] == '"':
                                break
                            Font_Type_No_2 = Font_Type_No_2 + \
                                SVG_FILE[SU_Inspector_Location_3]
                            SU_Inspector_Location_3 += 1
                        if Font_Type_No_1 != Font_Type_No_2:
                            Second_Task = 1
                        break

                    if SVG_FILE[SU_Inspector_Location_1: SU_Inspector_Location_1 + 9] == 'Helvetica' and First_Block == 1:
                        Second_Task = 1

                    SU_Inspector_Location_1 += 1
                Sentence_Length = 0
                while Second_Task:
                    if SVG_FILE[SU_Inspector_Location_1] == '>':
                        SU_Inspector_Location_1 += 1
                        while True:
                            Page_Ending_Indicator = 0
                            if SU_Inspector_Location <= len(SVG_FILE) - 5:
                                Page_Ending_Detecter() #---------->检测页尾标识
                            if SVG_FILE[SU_Inspector_Location_1] == ' ':
                                SU_Inspector_Location_1 += 1
                            else:
                                It_Is_Question_Number = 1
                                SU_Inspector_Location_1 += 1
                            Sentence_Length += 1
                            if SVG_FILE[SU_Inspector_Location_1] == '<':
                                Second_Task = 0
                                break
                    SU_Inspector_Location_1 += 1
                #满足了最终条件，开始记录坐标
                if It_Is_Question_Number == 1 and Sentence_Length >= 15:
                    QUESTION_NUMBER_LIST.append(QUESTION_NUMBER_STORAGE)
                    Block_End = 1
                    while Block_End:
                        Coordinate_Storage = ''
                        if SVG_FILE[SU_Inspector_Location: SU_Inspector_Location + 3] == 'y="' and SVG_FILE[SU_Inspector_Location - 1] == ' ':
                            SU_Inspector_Location += 3
                            while True:
                                if SVG_FILE[SU_Inspector_Location] == '"':
                                    SVG_FILE_SEPARATION_POINT.append(
                                        Coordinate_Storage)
                                    SU_Inspector_Location += 1
                                    Block_End = 0
                                    break
                                Coordinate_Storage = Coordinate_Storage + \
                                    SVG_FILE[SU_Inspector_Location]
                                SU_Inspector_Location += 1
                        SU_Inspector_Location += 1
        # 页尾检测
        if SU_Inspector_Location <= len(SVG_FILE) - 5:
            Page_Ending_Detecter()
        SU_Inspector_Location += 1

    #保4为有效数字
    SU_Inspector_Location = 0
    while SU_Inspector_Location <= len(SVG_FILE_SEPARATION_POINT) - 1:
        SVG_FILE_SEPARATION_POINT[SU_Inspector_Location] = round(float(SVG_FILE_SEPARATION_POINT[SU_Inspector_Location]), 4)
        SU_Inspector_Location += 1
    
    # 排序 从左到右按从小到大排序
    length = len(SVG_FILE_SEPARATION_POINT)
    for i in range(length - 1):
        for j in range(0, length - i - 1):  
            if SVG_FILE_SEPARATION_POINT[j] > SVG_FILE_SEPARATION_POINT[j+1]:
                SVG_FILE_SEPARATION_POINT[j], SVG_FILE_SEPARATION_POINT[j+1] = SVG_FILE_SEPARATION_POINT[j+1], SVG_FILE_SEPARATION_POINT[j]

    if len(SVG_FILE_SEPARATION_POINT) <= 1:
        SVG_FILE_SEPARATION_POINT = []
    # 过滤，去除重复的点
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

def Start_Separation(SVG_FILE):
    global SVG_FILE_SEPARATION_POINT, QUESTION_NUMBER, TARGET_HEIGHT, BUG_REPORTER, SVG_FILE_NUMBER, SVG_FILE_NAME_LIST, BROKEN_MATRIX, QUESTION_NUMBER_LIST
    Question_Count = len(SVG_FILE_SEPARATION_POINT) - 1
    if Question_Count <= 1 or Question_Count > 6:
        if BROKEN_MATRIX <= 3:
            BUG_REPORTER.write(SVG_FILE_NAME_LIST[SVG_FILE_NUMBER])
            BUG_REPORTER.write('\n')
            BUG_REPORTER.flush()
            Bug_File_Copier()
    QUESTION_NUMBER = 0
    # Find the number of questions
    while QUESTION_NUMBER <= Question_Count - 1 and BROKEN_MATRIX <= 4:
        SU_Inspector_Location = 1
        try:
            Product = open(PRODUCT_STORAGE_LOCATION + '/WareHouse' + '/' +
                       SVG_FILE_NAME_LIST[SVG_FILE_NUMBER][:-4] + '_' +str(QUESTION_NUMBER) + '@' + str(QUESTION_NUMBER_LIST[QUESTION_NUMBER]) + '.svg', 'w', encoding='utf-8')
        except:
            QUESTION_NUMBER += 1
            continue
        Product.write(SVG_FILE_HEADER)
        Product.flush()
        Upper_Boundary = float(
            SVG_FILE_SEPARATION_POINT[QUESTION_NUMBER])  # 上边界
        Lower_Boundary = float(
            SVG_FILE_SEPARATION_POINT[QUESTION_NUMBER + 1])  # 下边界
        while SU_Inspector_Location <= len(SVG_FILE) - 1:
            if SVG_FILE[SU_Inspector_Location: SU_Inspector_Location + 3] == 'y="' and SVG_FILE[SU_Inspector_Location - 1] == ' ':
                SU_Inspector_Location += 3
                Coordinate_Y_Storage = ''
                while True:
                    if SVG_FILE[SU_Inspector_Location] == '"':
                        break
                    Coordinate_Y_Storage = Coordinate_Y_Storage + \
                        SVG_FILE[SU_Inspector_Location]
                    SU_Inspector_Location += 1
                # 假如Y值在区间内
                if float(Coordinate_Y_Storage) >= Upper_Boundary - 5.5 and float(Coordinate_Y_Storage) < Lower_Boundary - 5.5:
                    # Record the label
                    while True:
                        if SVG_FILE[SU_Inspector_Location] == '<':
                            SU_Inspector_Location += 1
                            break
                        SU_Inspector_Location += -1
                    Label_Storage = '<'
                    End_Label_Count = 0
                    while True:
                        if SVG_FILE[SU_Inspector_Location] == '>':
                            if End_Label_Count == 1:
                                SU_Inspector_Location += 1
                                break
                            else:
                                End_Label_Count = 1
                        Label_Storage = Label_Storage + \
                            SVG_FILE[SU_Inspector_Location]
                        SU_Inspector_Location += 1
                    Label_Storage = Label_Storage + ">"
                    Product.write(Label_Storage)
                    Product.flush()

            if SVG_FILE[SU_Inspector_Location: SU_Inspector_Location + 9] == '<svg:path':
                Highest_Point = 0
                Lowest_Point = 9999999999999999999999999999999999999
                In_Tag_Check = 1
                while In_Tag_Check:
                    if SVG_FILE[SU_Inspector_Location: SU_Inspector_Location + 3] == 'd="' and SVG_FILE[SU_Inspector_Location - 1] == ' ':
                        SU_Inspector_Location += 4
                        Y_Value_Storage = ''
                        In_Tag_Check = 1
                        while In_Tag_Check:
                            Y_Value_Storage = ''
                            if SVG_FILE[SU_Inspector_Location] == 'Z' or SVG_FILE[SU_Inspector_Location] == '"':
                                break
                            if SVG_FILE[SU_Inspector_Location] == ' ':
                                SU_Inspector_Location += 1

                                while True:
                                    if SVG_FILE[SU_Inspector_Location] == ' ':
                                        SU_Inspector_Location += 1
                                        break
                                    SU_Inspector_Location += 1

                                while True:
                                    if SVG_FILE[SU_Inspector_Location] == ' ' or SVG_FILE[SU_Inspector_Location] == '"':
                                        if float(Y_Value_Storage) < Lowest_Point:
                                            Lowest_Point = float(
                                                Y_Value_Storage)
                                        if float(Y_Value_Storage) > Highest_Point:
                                            Highest_Point = float(
                                                Y_Value_Storage)
                                        if SVG_FILE[SU_Inspector_Location + 1] == 'M' or SVG_FILE[SU_Inspector_Location + 1] == 'L' or SVG_FILE[SU_Inspector_Location + 1] == 'C':
                                            SU_Inspector_Location += 2
                                        if SVG_FILE[SU_Inspector_Location + 1] == 'Z' or SVG_FILE[SU_Inspector_Location] == '"':
                                            In_Tag_Check = 0
                                        break
                                    Y_Value_Storage = Y_Value_Storage + \
                                        SVG_FILE[SU_Inspector_Location]
                                    SU_Inspector_Location += 1
                    SU_Inspector_Location += 1

                if Lowest_Point >= Upper_Boundary and Highest_Point < Lower_Boundary:
                    Keep_Writing_Path_Tag = 1
                    while Keep_Writing_Path_Tag:
                        if SVG_FILE[SU_Inspector_Location: SU_Inspector_Location + 9] == '<svg:path':
                            SU_Inspector_Location += 9
                            Product.write('<svg:path')
                            Product.flush()

                            End_Tag_Indicator = 0
                            while True:
                                if SVG_FILE[SU_Inspector_Location] == '>':
                                    if End_Tag_Indicator == 1:
                                        Product.write('>')
                                        Product.flush()
                                        SU_Inspector_Location += 1
                                        Keep_Writing_Path_Tag = 0
                                        break
                                    if End_Tag_Indicator == 0:
                                        End_Tag_Indicator = 1
                                Product.write(SVG_FILE[SU_Inspector_Location])
                                Product.flush()
                                SU_Inspector_Location += 1

                        SU_Inspector_Location += -1

            if SVG_FILE[SU_Inspector_Location: SU_Inspector_Location + 9] == '<svg:text':
                Product.write('<svg:text  xml:space="preserve">')
                Product.flush()
                SU_Inspector_Location += 9

            if SVG_FILE[SU_Inspector_Location: SU_Inspector_Location + 10] == '</svg:text':
                Product.write('</svg:text>')
                Product.flush()
                SU_Inspector_Location += 10

            if SVG_FILE[SU_Inspector_Location: SU_Inspector_Location + 9] == '<svg:defs':
                while True:
                    if SVG_FILE[SU_Inspector_Location: SU_Inspector_Location + 11] == '</svg:defs>':
                        SU_Inspector_Location += 11
                        Product.write('</svg:defs>')
                        Product.flush()
                        break
                    Product.write(SVG_FILE[SU_Inspector_Location])
                    Product.flush()
                    SU_Inspector_Location += 1

            SU_Inspector_Location += 1
        Product.write('</svg:svg>')
        Product.flush()
        Product.close()
        Relocate_Rewrite_Coordinates()
        QUESTION_NUMBER += 1

def Separation():
    global SVG_FILE, SVG_FILE_SEPARATION_POINT, SVG_FILE_STORAGE, BUG_REPORTER
    SVG_FILE = SVG_FILE_STORAGE
    SVG_FILE_SEPARATION_POINT = []
    Find_Separation_Location(SVG_FILE)
    BUG_REPORTER.write(str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) + ' ')
    BUG_REPORTER.write('--Finished finding separation points\n')
    BUG_REPORTER.flush()
    Start_Separation(SVG_FILE)

def Relocate_Rewrite_Coordinates():     #分割后的文件的坐标仍然是在页面中的位置，它将它们移上去
    global QUESTION_NUMBER, SVG_FILE, TARGET_HEIGHT, SVG_FILE_NUMBER, PRODUCT_STORAGE_LOCATION, SVG_FILE_NAME_LIST, SVG_FILE_UPPER_BLANK, QUESTION_NUMBER_LIST
    Functioning_Indicator = 1
    try:
        SVGFile_Open = open(PRODUCT_STORAGE_LOCATION + '/WareHouse' + '/' +
                       SVG_FILE_NAME_LIST[SVG_FILE_NUMBER][:-4] + '_' +str(QUESTION_NUMBER) + '@' + str(QUESTION_NUMBER_LIST[QUESTION_NUMBER]) + '.svg', 'r', encoding='utf-8')
        SVG_FILE = SVGFile_Open.read()
        TARGET_HEIGHT = float(SVG_FILE_SEPARATION_POINT[QUESTION_NUMBER])

        Product = open(PRODUCT_STORAGE_LOCATION + '/WareHouse' + '/' +
                        SVG_FILE_NAME_LIST[SVG_FILE_NUMBER][:-4] + '_' +str(QUESTION_NUMBER) + '@' + str(QUESTION_NUMBER_LIST[QUESTION_NUMBER]) + '.svg', 'w', encoding='utf-8')
    except:
        Functioning_Indicator = 0
    
    INSPECTOR_LOCATION = 0
    while INSPECTOR_LOCATION <= len(SVG_FILE) - 1 and Functioning_Indicator == 1:
        if SVG_FILE[INSPECTOR_LOCATION: INSPECTOR_LOCATION + 3] == 'y="' and SVG_FILE[INSPECTOR_LOCATION - 1] == ' ':
            INSPECTOR_LOCATION += 3
            Y_Value_Storage = ''
            while True:
                if SVG_FILE[INSPECTOR_LOCATION] == '"':
                    Product.write(
                        'y="' + str(float(Y_Value_Storage) - (TARGET_HEIGHT - SVG_FILE_UPPER_BLANK)))
                    Product.flush()
                    break
                Y_Value_Storage = Y_Value_Storage + SVG_FILE[INSPECTOR_LOCATION]
                INSPECTOR_LOCATION += 1

        if SVG_FILE[INSPECTOR_LOCATION: INSPECTOR_LOCATION + 3] == 'd="' and SVG_FILE[INSPECTOR_LOCATION - 1] == ' ':
            INSPECTOR_LOCATION += 4

            Product.write('d="M')
            Product.flush()

            Y_Value_Storage = ''
            In_Tag_Check = 1
            while In_Tag_Check:
                Y_Value_Storage = ''
                if SVG_FILE[INSPECTOR_LOCATION] == '"':
                    Product.write('" ')
                    Product.flush()
                    INSPECTOR_LOCATION += 1
                    break

                if SVG_FILE[INSPECTOR_LOCATION] == ' ':
                    Product.write(' ')
                    Product.flush()
                    INSPECTOR_LOCATION += 1

                    if SVG_FILE[INSPECTOR_LOCATION] == 'M':
                        Product.write('M ')
                        Product.flush()
                        INSPECTOR_LOCATION += 2
                    if SVG_FILE[INSPECTOR_LOCATION] == 'L':
                        Product.write('L ')
                        Product.flush()
                        INSPECTOR_LOCATION += 2
                    if SVG_FILE[INSPECTOR_LOCATION] == 'C':
                        Product.write('C ')
                        Product.flush()
                        INSPECTOR_LOCATION += 2

                    while True:
                        if SVG_FILE[INSPECTOR_LOCATION] == ' ':
                            Product.write(' ')
                            Product.flush()
                            INSPECTOR_LOCATION += 1
                            break
                        Product.write(SVG_FILE[INSPECTOR_LOCATION])
                        Product.flush()
                        INSPECTOR_LOCATION += 1
                    while True:
                        if SVG_FILE[INSPECTOR_LOCATION] == ' ' or SVG_FILE[INSPECTOR_LOCATION] == '"':
                            Product.write(
                                str(float(Y_Value_Storage) - (TARGET_HEIGHT - SVG_FILE_UPPER_BLANK)))
                            Product.flush()
                            if SVG_FILE[INSPECTOR_LOCATION] == ' ':
                                Product.write(' ')
                                Product.flush()
                            if SVG_FILE[INSPECTOR_LOCATION + 1] == 'M':
                                Product.write('M')
                                Product.flush()
                                INSPECTOR_LOCATION += 2
                            if SVG_FILE[INSPECTOR_LOCATION + 1] == 'L':
                                Product.write('L')
                                Product.flush()
                                INSPECTOR_LOCATION += 2
                            if SVG_FILE[INSPECTOR_LOCATION + 1] == 'C':
                                Product.write('C')
                                Product.flush()
                                INSPECTOR_LOCATION += 2

                            if SVG_FILE[INSPECTOR_LOCATION + 1] == 'Z':
                                Product.write('Z')
                                Product.flush()
                                INSPECTOR_LOCATION += 2
                            break

                        Y_Value_Storage = Y_Value_Storage + \
                            SVG_FILE[INSPECTOR_LOCATION]
                        INSPECTOR_LOCATION += 1
        Product.write(SVG_FILE[INSPECTOR_LOCATION])
        Product.flush()
        INSPECTOR_LOCATION += 1
# Print time
def Print_Time():
    global SVG_FILE_NUMBER, TIME_START, INSPECTOR_LOCATION
    #os.system("clean")
    print("\n\nMofish Pastpaper Separator  time: ",end='')
    print(str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) + ' ')
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
    
    # print(INSPECTOR_LOCATION)
    # Location_Indicator_Storage = 0
    # print('>',end='')
    # while Location_Indicator_Storage <= Location_Indicator:
    #     print('=',end='')
    #     Location_Indicator_Storage += 1

#os.system("clean")
# 获取所有文件地址
for root, dirs, files in os.walk(SVG_STORAGE, topdown=True):
    for name in files:
        if re.match('.*(.svg)', os.path.join(name)) is not None:
            SVG_FILE_LOCATION_LIST.append(
                os.path.join(root) + '/' + os.path.join(name))
            SVG_FILE_NAME_LIST.append(os.path.join(name))

Bug_Reporter_Open_Location = PRODUCT_STORAGE_LOCATION + '/' + 'BUG_REPORTER.txt'
BUG_REPORTER = open(Bug_Reporter_Open_Location, 'w', encoding='utf-8')

while SVG_FILE_NUMBER <= len(SVG_FILE_NAME_LIST) - 1:
    BLACK_PAGE_CHECK = 1
    if SVG_FILE_NAME_LIST[SVG_FILE_NUMBER][-6: -4] == '-1':  # 不处理试卷封面
        SVG_FILE_NUMBER += 1
    # 显示部分
    Print_Time()
    #logging.debug("Start rewriting: " + SVG_FILE_NAME_LIST[SVG_FILE_NUMBER], end='  ')
    BUG_REPORTER.write(str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) + ' ')
    BUG_REPORTER.write("Start rewriting: " +
                       SVG_FILE_NAME_LIST[SVG_FILE_NUMBER] + '\n')  # writing logfile
    BUG_REPORTER.flush()
    Rewrite_SVG()  # 去除Matrix
    #logging.debug("  ---Complete")
    BUG_REPORTER.write(str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) + ' ')
    BUG_REPORTER.write('---Complete' + '\n')
    BUG_REPORTER.flush()
    if BLACK_PAGE_CHECK == 0:
        #logging.debug('--BLANK PAGE--')
        BUG_REPORTER.write('--BLANK PAGE--' + '\n')
        BUG_REPORTER.flush()
    else:
        #logging.debug("Separate: " + SVG_FILE_NAME_LIST[SVG_FILE_NUMBER])
        BUG_REPORTER.write(str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) + ' ')
        BUG_REPORTER.write(
            "Separate: " + SVG_FILE_NAME_LIST[SVG_FILE_NUMBER] + '\n')
        BUG_REPORTER.flush()
        Separation()
        #logging.debug("Finished one page")
        BUG_REPORTER.write(str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) + ' ')
        BUG_REPORTER.write("Finished one page" + '\n\n')
        BUG_REPORTER.flush()
        BROKEN_MATRIX = 0
    # 结尾
    SVG_FILE_NUMBER += 1


TIME_END = time.perf_counter()
print('End of process. Total time taken: ' +
      str(round(TIME_END - TIME_START, 3)) + 's')
