import codecs
import pandas as pd

action_list = ['question','negative','affirmative','neutral','elaborate','opinion']

quest_list = ['quest','non-quest']
length_list = ['long','short']
sentiment_list = ['pos','neg','neutral']
quest_table = pd.DataFrame([(0.0,0.0,0.0,0.0,0.0,0.0),(0.0,0.0,0.0,0.0,0.0,0.0)],index = quest_list, columns =action_list)
length_table = pd.DataFrame([(0.0,0.0,0.0,0.0,0.0,0.0),(0.0,0.0,0.0,0.0,0.0,0.0)],index = length_list, columns =action_list)
sentiment_table = pd.DataFrame([(0.0,0.0,0.0,0.0,0.0,0.0),(0.0,0.0,0.0,0.0,0.0,0.0),(0.0,0.0,0.0,0.0,0.0,0.0)],index = sentiment_list, columns =action_list)

with codecs.open('RL_reward_table.txt', 'r', "utf-8") as f:
    lines = f.readlines()
    if lines:
        for line in lines[1:]:
            lst = line.split(' ')

            if lst[1] == 'quest':
                quest_table.ix[0, 'question'] += eval(str(lst[4]))
                quest_table.ix[0, 'negative'] += eval(str(lst[5]))
                quest_table.ix[0, 'affirmative'] += eval(str(lst[6]))
                quest_table.ix[0, 'neutral'] += eval(str(lst[7]))
                quest_table.ix[0, 'elaborate'] += eval(str(lst[8]))
                quest_table.ix[0, 'opinion'] += eval(str(lst[9]))

            else:
                quest_table.ix[1, 'question'] += eval(str(lst[4]))
                quest_table.ix[1, 'negative'] += eval(str(lst[5]))
                quest_table.ix[1, 'affirmative'] += eval(str(lst[6]))
                quest_table.ix[1, 'neutral'] += eval(str(lst[7]))
                quest_table.ix[1, 'elaborate'] += eval(str(lst[8]))
                quest_table.ix[1, 'opinion'] += eval(str(lst[9]))

            if lst[2] == 'long':
                length_table.ix[0, 'question'] += eval(str(lst[4]))
                length_table.ix[0, 'negative'] += eval(str(lst[5]))
                length_table.ix[0, 'affirmative'] += eval(str(lst[6]))
                length_table.ix[0, 'neutral'] += eval(str(lst[7]))
                length_table.ix[0, 'elaborate'] += eval(str(lst[8]))
                length_table.ix[0, 'opinion'] += eval(str(lst[9]))

            else:
                length_table.ix[1, 'question'] += eval(str(lst[4]))
                length_table.ix[1, 'negative'] += eval(str(lst[5]))
                length_table.ix[1, 'affirmative'] += eval(str(lst[6]))
                length_table.ix[1, 'neutral'] += eval(str(lst[7]))
                length_table.ix[1, 'elaborate'] += eval(str(lst[8]))
                length_table.ix[1, 'opinion'] += eval(str(lst[9]))

            if lst[3] == 'pos"':
                sentiment_table.ix[0, 'question'] += eval(str(lst[4]))
                sentiment_table.ix[0, 'negative'] += eval(str(lst[5]))
                sentiment_table.ix[0, 'affirmative'] += eval(str(lst[6]))
                sentiment_table.ix[0, 'neutral'] += eval(str(lst[7]))
                sentiment_table.ix[0, 'elaborate'] += eval(str(lst[8]))
                sentiment_table.ix[0, 'opinion'] += eval(str(lst[9]))

            elif lst[3] == 'neg"':
                sentiment_table.ix[1, 'question'] += eval(str(lst[4]))
                sentiment_table.ix[1, 'negative'] += eval(str(lst[5]))
                sentiment_table.ix[1, 'affirmative'] += eval(str(lst[6]))
                sentiment_table.ix[1, 'neutral'] += eval(str(lst[7]))
                sentiment_table.ix[1, 'elaborate'] += eval(str(lst[8]))
                sentiment_table.ix[1, 'opinion'] += eval(str(lst[9]))

            else:
                sentiment_table.ix[2, 'question'] += eval(str(lst[4]))
                sentiment_table.ix[2, 'negative'] += eval(str(lst[5]))
                sentiment_table.ix[2, 'affirmative'] += eval(str(lst[6]))
                sentiment_table.ix[2, 'neutral'] += eval(str(lst[7]))
                sentiment_table.ix[2, 'elaborate'] += eval(str(lst[8]))
                sentiment_table.ix[2, 'opinion'] += eval(str(lst[9]))

for index in quest_list:
    for action in action_list:
        quest_table.at[index,action] /= 36.0

for index in length_list:
    for action in action_list:
        length_table.at[index,action] /= 36.0

for index in sentiment_list:
    for action in action_list:
        sentiment_table.at[index,action] /= 24.0


print quest_table
print length_table
print sentiment_table
'''
quest_table.to_pickle('quest_table.pkl')
quest_table.to_csv(r'quest_table.txt', header=action_list, index=quest_list, sep=' ', mode='a')

length_table.to_pickle('length_table.pkl')
length_table.to_csv(r'length_table.txt', header=action_list, index=quest_list, sep=' ', mode='a')

sentiment_table.to_pickle('sentiment_table.pkl')
sentiment_table.to_csv(r'sentiment_table.txt', header=action_list, index=quest_list, sep=' ', mode='a')
'''