#docker run -ti --rm -v E:\0Mofish\PDF\Table-26:/pdf bwits/pdf2htmlex pdf2htmlEX --zoom 1.3 Files/1.pdf
import os, re

def Launcher():
	File_Location = './Files'
	Files = Get_File_List(File_Location)
	Command_Raw = 'docker run -ti --rm -v E:\\0Mofish\\PDF\\Table-26:/pdf bwits/pdf2htmlex pdf2htmlEX --zoom 1.3 Files/{File_Name}'
	for File_Name in Files:
		Command = Command_Raw.format(File_Name=File_Name)
		print(Command)
		os.system(Command)
	print('Done')

def Get_File_List(File_Position):
	Files = []
	for root, dirs, files in os.walk(File_Position, topdown=True):
		for name in files:
			Files.append(os.path.join(name))
	return Files
Launcher()
