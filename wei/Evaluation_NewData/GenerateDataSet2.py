import urllib2
from bs4 import BeautifulSoup
import csv
import time
from xml.etree import ElementTree


def writeFile(contents, fileName):
    f = open(str(fileName), 'w+')
    for line in contents:
        f.write(line + '\n')
    f.close()


with open('batch_edited_step_5.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    content = []
    fileName = 1
    for row in reader:
        content.append(row)
    for row in content:
        input_level0 = "user_prompt"
        input_slot0 = row.get('Input.slot0')

        input_level1 = "bot_" + row.get('Input.Dialogueacts_level1').split('.')[1]
        input_slot1 = row.get('Input.slot1')

        input_level2 = "user_" + row.get('Input.Dialogueacts_level2').split('.')[1]
        input_slot2 = row.get('Input.slot2')

        input_level3 = "bot_" + row.get('Input.Dialogueacts_level3').split('.')[1]
        input_slot3 = row.get('Input.slot3')

        input_level4 = "user_" + row.get('Input.Dialogueacts_level4').split('.')[1]
        input_slot4 = row.get('Input.slot4')

        first4 = [input_level0+":"+input_slot0,
                  input_level1+":"+input_slot1,
                  input_level2+":"+input_slot2,
                  input_level3+":"+input_slot3,
                  input_level4+":"+input_slot4]

        input_level5s = ["bot_change:"+ row.get('Answer.change'),
                        "bot_continuation:"+ row.get('Answer.continuation'),
                        "bot_elaboration:"+ row.get('Answer.elaboration'),
                        "bot_joking:"+ row.get('Answer.joking'),]
        for input_level5 in input_level5s:
            newOne = list(first4)
            newOne.append(input_level5)
            writeFile(newOne, fileName)
            fileName += 1

writeFile(content)





