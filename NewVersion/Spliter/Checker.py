import os, re, time, sys, json

File_Storage = './B-Product'
File_List = []
for _, _, files in os.walk(File_Storage, topdown=True): # root dirs files
		for name in files:
			if re.match('.*(.svg)', os.path.join(name)) is not None:
				File_List.append(os.path.join(name))
Data = []
for Item in File_List:
	File_Name = Item[0 : Item.find('@')]
	Action = 0
	for Paper in Data:
		if Paper["paper"] == File_Name:
			Paper["no"] = Paper["no"] + 1
			Action = 1
	if Action == 0:
		Data.append({"paper": File_Name, "no": 1})
Bug = []
for Item in Data:
	if Item["no"] <= 35:
		Bug.append(Item)

Log = open('./Checker.json', 'w')
Log.write(json.dumps(Bug))
Log.flush()
print(Bug)
percentage = round((len(Bug) / len(Data)) * 100, 2)
print(str(len(Bug)) + ' files are bugged, ' + str(len(Data)) + ' files in total. Percentage: ' + str(percentage) + '%')

input()