import json
import codecs
import random
#list2 includes set of strategies for each topic
file = open("list2.txt", 'r') 
strategies_dict = {}
for line in file: 
    d2 = json.load(codecs.open(line, "r",encoding='utf-8', errors='ignore'))
    for key, value in d2.items():
        strategies_dict[key]=value
    print("topic is about harry potter!")
for strategy in strategies_dict.keys():
    print("this is for strategy: "+strategy)
    for turns in range(0,15):
        input('Enter your dialogue: ')
        action=random.choice(strategies_dict[strategy])
        print action
        
