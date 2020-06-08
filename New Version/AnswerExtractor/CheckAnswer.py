import os, json

fileLocation = './log.json'
content = json.loads(open(fileLocation, 'r', encoding='utf-8').read())
log = open('./checkAnswer.json', 'w')

bug = {}
for item in content:
	if len(content[item]) != 41:
		bug[item] = len(content[item])

log.write(json.dumps(bug))
log.flush()

for item in bug:
	print(item + '  ' + str(bug[item]))

input()

# def Launcher():
# 	while 1:
# 		print('Choose a mode \n"1" check answer\n "2" check bug')
