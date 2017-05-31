import codecs
from textblob import TextBlob
import numpy as np
import os
import pandas as pd
import pickle
import Qlearning
import matplotlib.pyplot as plt

all_convs = os.listdir("../Data/300_convo")
question_list = {'Do','Does','Did','Who','Where','When','What','How','Is','Are','do','does','did','who','where','when','what','how','is','are'}
action_list = ['question','negative','affirmative','neutral','elaborate','opinion']

sentiment_list = ['pos','neg','neutral']
utt_length =['long','short']
QOrA= ['quest','answer']


state_list = []
for q in QOrA:
    for len in utt_length:
        for s in sentiment_list:
            for action in action_list:
                state_list.append(action + ' '+q+ ' '+ len +' ' + s)

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

reward_table = pd.read_pickle("RL_reward.pkl")

turn_list = ['0','1','2','3','4','5','6','7','8','9','10','11']
rate_table = pd.DataFrame([(0.1,0.09,0.08,0.07,0.06,0.05,0.04,0.03,0.02,0.01,0,0)],columns= turn_list)

q_learning = Qlearning.Qlearning(actions = action_list,learning_rate = rate_table)
value = []

for file in all_convs:

    with codecs.open("../Data/300_convo/" + file, 'r', 'utf-8') as f:
        lines = f.readlines()
        utt_list = []
        cov_actions = []
        try:
            if lines:
                last_line = lines[-1]
                last_line = last_line.strip().split(',')
                score1 = last_line[0].split('=')
                overall = eval(str(score1[1]))

                for line in lines[:-1]:
                    line = line.split('_')
                    action = line[1]
                    if action == 'None':
                        tmp = line[2].split(':')[-1]
                        utt_list.append(tmp)
                    else:
                        cov_actions.append(action)

            n = cov_actions.__len__()

            #for t in range(n/3):
            for i in range(n-1):
                cur_action = cov_actions[i]
                utt = utt_list[i]
                next_action = cov_actions[i + 1]
                next_utt = utt_list[i + 1]
                cur_state = cur_action + ' ' + isQuestion(utt) + ' ' + longUtt(utt) + ' ' + sentiment(utt)

                reward = reward_table.ix[cur_state, next_action]

                next_state = next_action + ' ' + isQuestion(next_utt) + ' ' + longUtt(
                                next_utt) + ' ' + sentiment(next_utt)
                q_learning.learn(cur_state, next_action, reward, next_state, str(i))

            cur_state = next_state
            next_state = 'terminal'
            q_learning.learn(cur_state, next_action, reward, next_state, str(i))


        except (RuntimeError, TypeError, NameError, IndexError):
            print "Error"
    q_learning.check_state_exist('elaborate answer short neutral')
    value.append(q_learning.q_table.ix['elaborate answer short neutral', 'affirmative'])
plt.xlabel('conversation')
plt.ylabel('q value')
plt.title('state = elaborate answer short neutral, action = affirmative')
plt.plot(value,'r--')
plt.show()

print q_learning.q_table
'''
q_learning.q_table.to_pickle('RL_Q_table.pkl')
q_learning.q_table.to_csv(r'RL_Q_table.txt', header=action_list, index=state_list, sep=' ', mode='a')
'''