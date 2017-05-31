import codecs
import numpy as np
import os

all_convs = os.listdir("./Data/300_convo/")

#print(all_convs)

for file in all_convs:
    with codecs.open("./Data/300_convo/"+ file, 'r','utf-8') as f:
        lines = f.readlines()
        try:
            if lines:
                first_line = lines[0]
                last_line = lines[-1]

                first_line = first_line.strip()
                last_line = last_line.strip()

                begin_sentence = first_line.split('_')
                begin_action = begin_sentence[1]
                #print begin_action

                eval_scores = last_line.split(',')
                begin_score = eval_scores[1].split("=")
                score = begin_score[1]
            #print score
        except(RuntimeError, TypeError, NameError,IndexError):
            pass
    with open('begin_action.txt', 'a') as bfile:
        bfile.write(begin_action + ":" + score+ '\n')





