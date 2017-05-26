import codecs
from textblob import TextBlob
import numpy as np
import os
import pandas as pd
import pickle

all_convs = os.listdir("../Data/300_convo/")
question_list = {'Do','Does','Did','Who','Where','When','What','How','Is','Are','do','does','did','who','where','when','what','how','is','are'}
action_list = ['question','negative','affirmative','neutral','elaborate','opinion']
action_dic = {'question':0,'negative':0,'affirmative':0,'neutral':0,'elaborate':0,'opinion':0}

sentiment_list = ['pos','neg','neutral']
utt_length =['long','short']
QOrA= ['quest','answer']
action_list = ['question','negative','affirmative','neutral','elaborate','opinion']

state_list = []
for q in QOrA:
    for len in utt_length:
        for s in sentiment_list:
            for action in action_list:
                state_list.append(action + ' '+q+ ' '+ len +' ' + s)


reward_table = pd.DataFrame(columns=action_list)

for state in state_list:
    reward_table = reward_table.append(
        pd.Series([0]*6, index = action_list,name = state)
    )

#count number of times
count_table = pd.DataFrame(columns=action_list)
for state in state_list:
    count_table = count_table.append(
        pd.Series([0]*6, index = action_list,name = state)
    )

#updata the reward table,by calculate the mean reward for each state
def update(table,state,action,score):
    index = ' '.join(state)
    if index not in table.index.values.tolist():
        table.ix[index, action] = score
    else:
        table.ix[index, action] = (table.ix[index, action] * (count_table.ix[index,action] - 1) + score) / count_table.ix[index,action]
        table.ix[index, action] = round(table.ix[index, action],3)

def isQuestion(utt):
    if utt[-1] =='?':
        return 'quest'
    elif utt.strip().split(' ')[0] in question_list:
        return 'quest'
    else:
        return 'answer'
#print isQuestion("Do you want to build a snowman")

def longUtt(utt):
    count = utt.split(' ').__len__()
    if count> 5:
        return 'long'
    else:
        return 'short'

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

#print sentiment("what is the weather?")

for file in all_convs:
    with codecs.open("../Data/300_convo/"+ file, 'r','utf-8') as f:
        lines = f.readlines()
        try:
            if lines:
                last_line = lines[-1]
                last_line = last_line.strip().split(',')
                score1 = last_line[0].split('=')
                overall = eval(str(score1[1]))

                pre_action = lines[-5].split('_')[1]
                utt = lines[-4].split('_')[2].split(':')[-1]
                cur_action = lines[-3].split('_')[1]
                state = [pre_action, isQuestion(utt), longUtt(utt), sentiment(utt)]
                state_str = ' '.join(state)
                count_table.ix[state_str, cur_action] += 1
                update(reward_table, state, cur_action, overall)
        except (RuntimeError, TypeError, NameError, IndexError):
            print "RuntimeError"

        reward_table.to_csv(r'RL_reward_table.txt', header=action_list, index=state_list, sep=' ', mode='a')
        reward_table.to_pickle('RL_reward.pkl')

print reward_table