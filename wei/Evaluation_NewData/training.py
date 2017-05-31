import codecs
from textblob import TextBlob
import numpy as np
import os
import pandas as pd
import pickle
import Qlearning
import matplotlib.pyplot as plt

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

# str = 'we have a small house, we been livd here for 2 years, my children like to play in the back yard'
def lexical_diversity(text):
    return len(set(text)) / len(text)
# print lexical_diversity(str)

#print sentiment("what is the weather?")

reward_table = pd.read_pickle("reward2.pkl")

turn_list = ['0','1','2']
rate_table = pd.DataFrame([(0.02,0.01,0.005)],columns= turn_list)

q_learning = Qlearning.Qlearning(actions = action_list,learning_rate = rate_table)
q_table = q_learning.q_table
for state in state_list:
    q_table = q_table.append(
        pd.Series(
            [0] * len(action_list),
            index=q_table.columns,
            name=state,
        )
    )

value = []

for file in all_convs:
    with codecs.open("NewData2/" + file, 'r', 'utf-8') as f:
        lines = f.readlines()
        utt_list = []
        bot_actions = []
        user_actions =[]
        try:
            if lines:
                text = lines[3].split(':')[-1] + lines[5].split(':')[-1]
                score = lexical_diversity(text) * 5

                cur_state = 'null prompt pos answer'
                next_action = 'joking'
                for line in lines[2:]:
                    line = line.split('_')
                    agent = line[0]
                    action = line[1].split(':')[0]
                    if agent == 'user':
                        user_actions.append(action)
                        tmp = line[1].split(':')[-1]
                        utt_list.append(tmp)
                    else:
                        bot_actions.append(action)
            
            q_learning.learn(cur_state, next_action, reward_table.ix[cur_state, next_action], next_action + ' '+ user_actions[0]+ ' ' + isQuestion(utt_list[0]) + ' ' + sentiment(utt_list[0]), '0')
            cur_state = next_action + ' '+ user_actions[0]+ ' ' + isQuestion(utt_list[0]) + ' ' + sentiment(utt_list[0])
            next_action = bot_actions[0]
            q_learning.learn(cur_state, next_action, reward_table.ix[cur_state, next_action],
                                 next_action + ' ' + user_actions[1] + ' ' + isQuestion(utt_list[1]) + ' ' + sentiment(utt_list[1]),
                                 '1')
            cur_state = next_action + ' ' + user_actions[1] + ' ' + isQuestion(utt_list[1]) + ' ' + sentiment(utt_list[1])
            next_action = bot_actions[1]
            q_learning.learn(cur_state, next_action, reward_table.ix[cur_state, next_action],'terminal','2')

        except (RuntimeError, TypeError, NameError, IndexError):
            print "Error"

    q_learning.check_state_exist('change elaboration answer neutral')
    value.append(q_learning.q_table.ix['change elaboration answer neutral', 'continuation'])

plt.xlabel('conversation')
plt.ylabel('q value')
plt.title('state = change elaboration answer neutral, action = continuation')
plt.plot(value,'r--')
plt.show()

print q_learning.q_table

q_learning.q_table.to_pickle('Q_table.pkl')
q_learning.q_table.to_csv(r'Q_table.txt', header=action_list, index=state_list, sep=' ', mode='a')
