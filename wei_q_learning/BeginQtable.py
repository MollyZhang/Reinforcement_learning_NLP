import numpy as np
import pandas as pd
import codecs
import sys

class BeginQtable:
    def __init__(self, actions, dic):
        self.actions = actions
        self.q_table = pd.DataFrame([(0.0,0.0,0.0,0.0,0.0,0.0)], columns = self.actions)
        self.action_dic = dic

    def learn(self,action,score):
        if self.action_dic[action] == 0:
            self.q_table.ix[0,action] = 0
        elif self.action_dic[action] == 1:
            self.q_table.ix[0,action] = score
        else:
            self.q_table.ix[0,action] = (self.q_table.ix[0,action] * (self.action_dic[action]-1) + score) / self.action_dic[action]


action_list = ['question','negative','affirmative','neutral','elaborate','opinion']
action_dic = {'question':0,'negative':0,'affirmative':0,'neutral':0,'elaborate':0,'opinion':0}

begin_table = BeginQtable(action_list,action_dic)

with codecs.open("begin_action.txt", 'r',"utf-8") as f:
    for line in f:
        line = line.strip()
        line = line.split(':')
        begin_action = line[0]
        score = line[1]
        score = eval(str(score))

        if begin_action not in action_dic:
            action_dic[begin_action] = 1
        else:
            action_dic[begin_action] += 1

        begin_table.learn(begin_action, score)

print begin_table.q_table
#begin_table.q_table.to_csv(sys.stdout)
begin_table.q_table.to_pickle('beginning.pkl')

#    question  negative  affirmative  neutral  elaborate  opinion
# 0  4.222222  1.157895         1.08  1.47619   0.653846      3.
