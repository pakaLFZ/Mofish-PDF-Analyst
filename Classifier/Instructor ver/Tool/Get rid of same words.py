import os
import re
Content = open('./1.txt', 'r').read()
Log = open('./Ver1.txt', 'w')
Book = open('./book.txt', 'r', encoding = 'utf-8').read()
Content = sorted(list(set(re.sub(r'[^\w\s]|\r|\n',' ',Content).split(' '))))
Text = ''
for i in Content:
    if Book.find(' ' + i + ' ') != -1:
        continue
    if i.isalpha():
        Text = Text + i.lower() + '\n'

Log.write(Text)
Log.flush()