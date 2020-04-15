import json
import os
import time
import re

class JSONObject:     
    def __init__(self, d):
        self.__dict__ = d

File_Name = 'Target'
File_Location = './' + File_Name + '.txt'
File = open(File_Location, 'r').read()
File_Length = len(File)
Content_Recorder = []

Log = open('./Log.txt', 'w')

Inspector_Location = 0
while Inspector_Location <= File_Length - 1:
    Inspector_Location = File.find('File used: ', Inspector_Location) + 11
    Location_Storage = File.find('%', Inspector_Location)
    Content_Recorder.append(["File_Name"])
    Content_Recorder.append(File[Inspector_Location : Location_Storage])
    Question_Number = 1
    while 1:
        Inspector_Location = File.find('#', Inspector_Location) + 1
        Location_Storage = File.find(':', Inspector_Location)
        Number = File[Inspector_Location : Location_Storage]
        if Question_Number == int(Number):
            Inspector_Location = File.find(':', Inspector_Location) + 1
            Location_Storage = File.find('&', Inspector_Location)
            Answer = File[Inspector_Location : Location_Storage]








s = '{"name": "ACME", "shares": 50, "price": 490.1}'
data = json.loads(s, object_hook=JSONObject)
print(data.name)