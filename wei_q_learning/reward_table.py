import codecs
from textblob import TextBlob
import numpy as np
import os
import pandas as pd
import pickle

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


reward_table = pd.DataFrame(columns=action_list)

for state in state_list:
    reward_table = reward_table.append(
        pd.Series([0]*6, index = action_list,name = state)
    )

def update(table,state,action,score):
    index = ' '.join(state)
    if index not in table.index.values.tolist():
        table.ix[index, action] = score

    else:
        table.ix[index, action] = (table.ix[index, action] * (action_dic[action] - 1) + score) / action_dic[action]


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
    with codecs.open("Data/"+ file, 'r','utf-8') as f:
        lines = f.readlines()
        try:
            if lines:
                last_line = lines[-1]
                last_line = last_line.strip().split(',')
                score1 = last_line[0].split('=')
                overall = eval(str(score1[1]))

                first_line = lines[0]
                cur_action = first_line.strip().split('_')[1]
                pre_action = 'null'

                for line in lines[1:-1]:
                    line = line.strip()
                    tmp = line.split('_')
                    action = tmp[1]
                    if action == 'None':
                        utt = tmp[2].split(':')[-1]
                        pre_action = cur_action
                        state = [pre_action, isQuestion(utt), longUtt(utt), sentiment(utt)]
                    else:
                        cur_action = action
                        if action not in action_dic:
                            action_dic[action] = 1
                        else:
                            action_dic[action] += 1
                        update(reward_table,state,cur_action,overall)
                        reward_table.groupby(reward_table.index).first()

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

print reward_table
#pickle.dump(reward_table, open("reward_value.pkl", "wb"))
reward_table.to_pickle('reward.pkl')
b = pd.read_pickle('reward.pkl')
print b


