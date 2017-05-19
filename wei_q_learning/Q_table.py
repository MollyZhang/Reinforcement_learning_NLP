import codecs
from textblob import TextBlob
import numpy as np
import os
import pandas as pd
import pickle
import Qlearning

all_convs = os.listdir("Data/")
question_list = {'Do','Does','Did','Who','Where','When','What','How','Is','Are','do','does','did','who','where','when','what','how','is','are'}
action_list = ['question','negative','affirmative','neutral','elaborate','opinion']
action_dic = {'question':0,'negetive':0,'affirmative':0,'neutral':0,'elaborate':0,'opinion':0}

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

reward_table = pd.read_pickle("reward.pkl")

q_learning = Qlearning.Qlearning(actions = action_list)

for file in all_convs:
    with codecs.open("Data/"+ file, 'r','utf-8') as f:
        lines = f.readlines()
        try:
            if lines:
                last_line = lines[-1]
                last_line = last_line.strip().split(',')
                score1 = last_line[0].split('=')
                overall = eval(str(score1[1]))

                first_line = lines[0]
                next_action = first_line.strip().split('_')[1]
                cur_action = 'null'
                initial_state = 'Null Null Null Null'
                cur_state = initial_state

                for line in lines[1:-1]:
                    line = line.strip()
                    tmp = line.split('_')
                    action = tmp[1]
                    if action == 'None':
                        utt = tmp[2].split(':')[-1]
                        next_state = next_action + ' '+ isQuestion(utt)+' '+longUtt(utt)+' '+ sentiment(utt)
                        cur_action = next_action

                    else:
                        cur_state = next_state
                        next_action = action
                        if action not in action_dic:
                            action_dic[action] = 1
                        else:
                            action_dic[action] += 1
                        reward = reward_table.ix[cur_state,action]
                        q_learning.learn(cur_state, action, reward, next_state)

        except (RuntimeError, ):
            print "RuntimeError"
            pass
        except(TypeError):
            print "TypeError"
            pass
        except(NameError):
            print"NemeError"
            pass
        except(IndexError):
            print "IndexError"
            print 'file name:' + file
            pass
        except(UnicodeEncodeError):
            print "UnicodeEncodeError"
            print 'file name:' + file
            pass
print q_learning.q_table
q_learning.q_table.to_pickle('Q_table.pkl')



