import codecs
from textblob import TextBlob
import numpy as np
import os
import pandas as pd
import pickle
import Qlearning
import matplotlib.pyplot as plt

all_convs = os.listdir("Data/300_convo/")
question_list = {'Do','Does','Did','Who','Where','When','What','How','Is','Are','do','does','did','who','where','when','what','how','is','are'}
action_list = ['question','negative','affirmative','neutral','elaborate','opinion']

sentiment_list = ['pos','neg','neutral']
utt_length =['long','short']
QOrA= ['quest','answer']
action_list = ['question','negative','affirmative','neutral','elaborate','opinion']

# all states
state_list = []
for q in QOrA:
    for len in utt_length:
        for s in sentiment_list:
            for action in action_list:
                state_list.append(action + ' '+q+ ' '+ len +' ' + s)

#initialize reward table to all zeros.
reward_table = pd.DataFrame(columns=action_list)
for state in state_list:
    reward_table = reward_table.append(
        pd.Series([0.0]*6, index = action_list,name = state)
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

#check the user utterance: asking a question or not
def isQuestion(utt):
    if utt[-1] =='?':
        return 'quest'
    elif utt.strip().split(' ')[0] in question_list:
        return 'quest'
    else:
        return 'answer'
#print isQuestion("Do you want to build a snowman")

#check the length of the user utterance
def longUtt(utt):
    count = utt.split(' ').__len__()
    if count> 5:
        return 'long'
    else:
        return 'short'

#check the sentiment of the user utterance
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

#read all training conversations and record the reward table
'''
#read all training conversations and record the reward table
for file in all_convs:
    with codecs.open("Data/300_convo/"+ file, 'r','utf-8') as f:
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
        except (RuntimeError,TypeError,NameError,IndexError):
            print "RuntimeError"

reward_table.to_csv(r'RL_reward_table.txt', header=action_list, index=state_list, sep=' ', mode='a')
reward_table.to_pickle('RL_reward.pkl')

#print reward_table
'''
#the initial Q_table

'''
reward_table = pd.read_pickle("RL_reward.pkl")

q_learning = Qlearning.Qlearning(actions=action_list)

for file in all_convs:
    with codecs.open("Data/300_convo/" + file, 'r', 'utf-8') as f:
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

            for i  in range(n-2):
                cur_action = cov_actions[i]
                utt = utt_list [i]
                next_action = cov_actions[i+1]
                next_utt = utt_list[i+1]
                cur_state =  cur_action + ' ' + isQuestion(utt) + ' ' + longUtt(utt) + ' ' + sentiment(utt)

                reward = reward_table.ix[cur_state, next_action]
                if i != n - 2:
                    next_state = next_action + ' ' + isQuestion(next_utt) + ' ' + longUtt(next_utt) + ' ' + sentiment(next_utt)
                    q_learning.learn(cur_state, next_action, reward, next_state)
                if i == n - 2:
                    next_state = 'terminal'
                    q_learning.learn(cur_state, next_action, reward, next_state)
        except (RuntimeError, TypeError, NameError, IndexError):
            print "Error"

print q_learning.q_table
q_learning.q_table.to_pickle('RL_Q_table.pkl')
q_learning.q_table.to_csv(r'RL_Q_table.txt', header=action_list, index=state_list, sep=' ', mode='a')
'''

# policy iteration
#initialize the policy for each state, randomly choose an action from action list.
policy_table = pd.DataFrame([('question','question','question','question','question','question',
                             'question','question','question','question','question','question',
                             'question', 'question', 'question','question','question','question',
                             'question', 'question', 'question','question','question','question',
                             'question', 'question', 'question','question','question','question',
                             'question', 'question', 'question','question','question','question',
                             'question', 'question', 'question','question','question','question',
                             'question', 'question', 'question','question','question','question',
                             'question', 'question', 'question','question','question','question',
                             'question', 'question', 'question','question','question','question',
                             'question', 'question', 'question','question','question','question',
                             'question', 'question', 'question','question','question','question')],columns = state_list)

q_learning = Qlearning.Qlearning(action_list)
q_learning.q_table = pd.read_pickle("Q_table2.pkl")
for s in state_list:
    if s not in q_learning.q_table.index:
    # append new state to q table
        q_learning.q_table = q_learning.q_table.append(
            pd.Series(
                [0] * action_list.__len__(),
                index=q_learning.q_table.columns,
                name=s,
            )
        )
    policy_table.ix[0,s] = np.random.choice(action_list)
    # policy_table, V_list = policy_improvement(policy_eval_fn=policy_eval, discount_factor=1.0)

def action_prob():
    action_prob = pd.DataFrame(index = state_list, columns=action_list)
    for state in state_list:
        action_sum = 0
        for action in action_list:
            action_sum += q_learning.q_table.ix[state, action]
            # Look at the possible next actions
        for action in action_list:
            if action_sum == 0:
                action_prob.ix[state, action] = 0
            else:
                action_prob.ix[state, action] = round(q_learning.q_table.ix[state, action] / action_sum, 3)
    return action_prob

def calculate_prob():
    #calculate the probability of current stase on previous action. row is next_state, column is actions acted prevoiusly
    prob_table = pd.DataFrame(index = state_list,columns = action_list)
    action_column_sum = pd.DataFrame([(0,0,0,0,0,0)],columns=action_list)
    action_sum = pd.DataFrame([(0,0,0,0,0,0)],columns=action_list)
    action_sub_sum = pd.DataFrame([(0, 0, 0, 0, 0, 0)], columns=action_list)
    for action in action_list:
        for state in state_list:
            action_column_sum.ix[0,action] += q_learning.q_table.ix[state,action]

    for action in action_list:
        for state in state_list:
            if action_column_sum.ix[0, action] == 0:
                action_sum.ix[0, action] = 0
            else:
                action_sum.ix[0,action] += q_learning.q_table.ix[state,action] * q_learning.q_table.ix[state,action] /action_column_sum.ix[0,action]

    for action in action_list:
        for state in state_list:
            if action in state:
                action_sub_sum.ix[0,action] += q_learning.q_table.ix[state,action]


    for action in action_list:
        for state in state_list:
            if action in state:
                if action_sub_sum.ix[0,action] == 0:
                    prob_table.ix[state, action] = 0
                else:
                    prob_table.ix[state,action] = round(q_learning.q_table.ix[state,action] * action_sum.ix[0,action] / action_sub_sum.ix[0,action], 3)
            else:
                prob_table.ix[state, action] = 0
    return prob_table


def policy_eval(q_table, discount_factor=1.0, theta=0.005):

    # Start with a random (all 0) value function
    V_list = pd.DataFrame(columns=state_list)
    V_list = V_list.append(
                pd.Series(
                    [0]*state_list.__len__(),
                    index=V_list.columns,
                    name = action
                ))
    Prob_action = action_prob()
    prob = calculate_prob()
    #print Prob_action
    #print prob

    while True:
        delta = 0
        # For each state, perform a "full backup"
        for s in state_list:
            v = 0
            for a in action_list:
                # For each action, look at the possible next states...
                reward = q_table.ix[s, a]
                next_state_set = []
                for tmp in state_list:
                    act = tmp.split(' ')[0]
                    if a in tmp:
                        next_state_set.append(tmp)
                for next_state in next_state_set:
                    # Calculate the expected value

                    v += Prob_action.ix[s,a] * prob.ix[s,a] * (reward + discount_factor * V_list.ix[0,next_state])

            # How much our value function changed (across any states)
            delta = max(delta, np.abs(v - V_list.ix[0, s]))
            #print delta
            V_list.ix[0, s] = v
        # Stop evaluating once our value function change is below a threshold
        if delta < theta:
            break
    return V_list


def policy_improvement(policy_eval_fn=policy_eval, discount_factor=1.0):

    while True:
        # Evaluate the current policy
        V = policy_eval_fn(q_learning.q_table, discount_factor)

        # Will be set to false if we make any changes to the policy
        policy_stable = True

        # For each state...
        for s in state_list:
            # The best action we would take under the currect policy

            chosen_a = q_learning.choose_action(s,policy_table)
            #chosen_a = policy_table.ix[0,s]
            #print policy_table
            # Find the best action by one-step lookahead
            # Ties are resolved arbitarily
            action_values = {'question': 0, 'negative': 0, 'affirmative': 0, 'neutral': 0, 'elaborate': 0, 'opinion': 0}
            for a in action_list:
                reward = q_learning.q_table.ix[s, a]
                next_state_set = []
                sum_value = 0
                for tmp in state_list:
                    if a in tmp:
                        next_state_set.append(tmp)
                        sum_value += np.sum(q_learning.q_table.ix[tmp, :])
                for next_state in next_state_set:
                    prob = round(np.sum(q_learning.q_table.ix[next_state, :]) / sum_value, 3)
                    action_values[a] += prob * (reward + discount_factor * V.ix[0,next_state])
            best_a = max(action_values, key=action_values.get)
            #print best_a
            # Greedily update the policy
            print chosen_a, best_a
            if chosen_a != best_a:
                policy_stable = False
                policy_table.ix[0,s] = best_a
        #print policy_table
        # If the policy is stable we've found an optimal policy. Return it
        print '-----------------------------------'
        if policy_stable:
            return policy_table, V
'''
policy_table, V_list = policy_improvement(policy_eval_fn=policy_eval, discount_factor=1.0)
print policy_table
print V_list
policy_table.to_pickle('policy_table.pkl')
V_list.to_pickle('V_list.pkl')
policy_table.to_csv(r'policy_table.txt', header=state_list, sep=' ', mode='a')
V_list.to_csv(r'V_list.txt', header=state_list, sep=' ', mode='a')

'''
def update_Q():

    while True:
    # for a each state, calculate new q_table based on policy
        delta = 0
        for state in state_list:
            optimal_action = policy_table.ix[0,state]
            prob_table = calculate_prob()
            q_original = q_learning.q_table.ix[state, optimal_action]
            q_update = 0
            #find all possible next state
            for s in state_list:
                if optimal_action in s:
                    q_update += prob_table.ix[s, optimal_action] * q_learning.q_table.ix[s, policy_table.ix[0,s]]

            # How much our value function changed (across any states)
        delta = max(delta, np.abs(q_update - q_original))
        q_learning.q_table.ix[state, optimal_action] = q_update
        if delta < 0.005:
            break
    print q_learning.q_table
    return q_learning.q_table
'''
optimal_Q_table = update_Q()
print optimal_Q_table
optimal_Q_table.to_pickle('optimal_Q_table.pkl')
optimal_Q_table.to_csv(r'optimal_Q_table.txt', header=action_list, index=state_list, sep=' ', mode='a')
'''

def RL():
    policy, V = policy_improvement(policy_eval_fn=policy_eval, discount_factor=1.0)
    q_learning.q_table= update_Q()
    policy2, V2 = policy_improvement(policy_eval_fn=policy_eval, discount_factor=1.0)

    for state in state_list:
        if policy.ix[0,state] != policy2.ix[0,state]:
            RL()
    return q_learning.q_table

optimal_Q_table = RL()
print optimal_Q_table
optimal_Q_table.to_pickle('optimal_Q_table3.pkl')
optimal_Q_table.to_csv(r'optimal_Q_table3.txt', header=action_list, index=state_list, sep=' ', mode='a')
