from __future__ import division
import codecs
from textblob import TextBlob
import numpy as np
import os
import pandas as pd
import pickle

all_convs = os.listdir("NewData2/")
question_list = {'Do','Does','Did','Who','Where','When','What','How','Is','Are','do','does','did','who','where','when','what','how','is','are'}
action_list = ['change','continuation','elaboration','joking']

sentiment_list = ['pos','neg','neutral']
QOrA= ['quest','answer']

state_list = []
for q in QOrA:
    for s in sentiment_list:
        for user_action in action_list:
            for bot_pre_action in action_list:
                state_list.append(bot_pre_action + ' ' + user_action + ' '+q +' ' + s)


reward_table = pd.DataFrame(columns=action_list)
init_state = ['null', 'prompt', 'pos', 'answer']
reward_table = reward_table.append(
        pd.Series([0]*4, index = action_list,name = 'null prompt pos answer')
    )

for state in state_list:
    reward_table = reward_table.append(
        pd.Series([0]*4, index = action_list,name = state)
    )

#count number of times
count_table = pd.DataFrame(columns=action_list)
for state in state_list:
    count_table = count_table.append(
        pd.Series([0]*4, index = action_list,name = state)
    )

#updata the reward table,by calculate the mean reward for each state
def update(table,state,action,score):
    index = ' '.join(state)
    if index not in table.index.values.tolist():
        table.ix[index, action] = score
    else:
        table.ix[index, action] = (table.ix[index, action] * (count_table.ix[index,action] - 1) + score) / count_table.ix[index,action]
        table.ix[index, action] = round(table.ix[index, action],3)

#str = 'we have a small house, we been livd here for 2 years, my children like to play in the back yard'
def lexical_diversity(text):
    return len(set(text)) / len(text)
#print lexical_diversity(str)

def isQuestion(utt):
    if '?' in utt:
        return 'quest'
    elif utt.strip().split(' ')[0] in question_list:
        return 'quest'
    else:
        return 'answer'
#print isQuestion("Do you want to build a snowman")

def sentiment(utt):
    blob = TextBlob(utt)
    senti=blob.sentiment
    if senti.polarity<0.2 and senti.polarity>-0.2:
        return 'neutral'
    else:
        if senti.polarity>0:
            return 'pos'
        else:
            return 'neg'

#print sentiment("I love walking along the beach.")

for file in all_convs:
    with codecs.open("NewData2/"+ file, 'r','utf-8') as f:
        lines = f.readlines()

        try:
            if lines:
                text = lines[3].split(':')[-1] + lines[5].split(':')[-1]
                score = lexical_diversity(text) * 10

                pre_action = lines[-3].split(':')[0].split('_')[1]
                user_action = lines[-2].split(':')[0].split('_')[1]
                utt = lines[-2].split(':')[-1]
                cur_action = lines[-1].split(':')[0].split('_')[1]
                state = [pre_action, user_action, isQuestion(utt), sentiment(utt)]
                state_str = ' '.join(state)
                count_table.ix[state_str, cur_action] += 1
                update(reward_table, state, cur_action, score)
        except (RuntimeError, TypeError, NameError, IndexError):
            print "RuntimeError"

reward_table.to_csv(r'reward_table2.txt', header=action_list, index=state_list, sep=' ', mode='a')
reward_table.to_pickle('reward2.pkl')

#print reward_table

'''

'''
