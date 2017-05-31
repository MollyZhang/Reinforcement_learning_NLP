import codecs
import pandas as pd

action_list = ['change','continuation','elaboration','joking']

quest_list = ['quest','non-quest']
sentiment_list = ['pos','neg','neutral']
quest_table = pd.DataFrame([(0.0,0.0,0.0,0.0),(0.0,0.0,0.0,0.0)],index = quest_list, columns =action_list)
sentiment_table = pd.DataFrame([(0.0,0.0,0.0,0.0),(0.0,0.0,0.0,0.0),(0.0,0.0,0.0,0.0)],index = sentiment_list, columns =action_list)
u_action_table = pd.DataFrame([(0.0,0.0,0.0,0.0),(0.0,0.0,0.0,0.0),(0.0,0.0,0.0,0.0),(0.0,0.0,0.0,0.0)],index = action_list, columns =action_list)
b_action_table = pd.DataFrame([(0.0,0.0,0.0,0.0),(0.0,0.0,0.0,0.0),(0.0,0.0,0.0,0.0),(0.0,0.0,0.0,0.0)],index = action_list, columns =action_list)


with codecs.open('reward_table2.txt', 'r', "utf-8") as f:
    lines = f.readlines()
    if lines:
        for line in lines[1:]:
            lst = line.split(' ')

            if lst[2] == 'quest':
                quest_table.ix[0, 'change'] += eval(str(lst[4]))
                quest_table.ix[0, 'continuation'] += eval(str(lst[5]))
                quest_table.ix[0, 'elaboration'] += eval(str(lst[6]))
                quest_table.ix[0, 'joking'] += eval(str(lst[7]))

            else:
                quest_table.ix[1, 'change'] += eval(str(lst[4]))
                quest_table.ix[1, 'continuation'] += eval(str(lst[5]))
                quest_table.ix[1, 'elaboration'] += eval(str(lst[6]))
                quest_table.ix[1, 'joking'] += eval(str(lst[7]))

            if lst[1] == 'change':
                u_action_table.ix[0, 'change'] += eval(str(lst[4]))
                u_action_table.ix[0, 'continuation'] += eval(str(lst[5]))
                u_action_table.ix[0, 'elaboration'] += eval(str(lst[6]))
                u_action_table.ix[0, 'joking'] += eval(str(lst[7]))

            elif lst[1] == 'continuation':
                u_action_table.ix[1, 'change'] += eval(str(lst[4]))
                u_action_table.ix[1, 'continuation'] += eval(str(lst[5]))
                u_action_table.ix[1, 'elaboration'] += eval(str(lst[6]))
                u_action_table.ix[1, 'joking'] += eval(str(lst[7]))

            elif lst[1] == 'elaboration':
                u_action_table.ix[2, 'change'] += eval(str(lst[4]))
                u_action_table.ix[2, 'continuation'] += eval(str(lst[5]))
                u_action_table.ix[2, 'elaboration'] += eval(str(lst[6]))
                u_action_table.ix[2, 'joking'] += eval(str(lst[7]))

            else:
                u_action_table.ix[3, 'change'] += eval(str(lst[4]))
                u_action_table.ix[3, 'continuation'] += eval(str(lst[5]))
                u_action_table.ix[3, 'elaboration'] += eval(str(lst[6]))
                u_action_table.ix[3, 'joking'] += eval(str(lst[7]))

            if lst[0] == '"change':
                b_action_table.ix[0, 'change'] += eval(str(lst[4]))
                b_action_table.ix[0, 'continuation'] += eval(str(lst[5]))
                b_action_table.ix[0, 'elaboration'] += eval(str(lst[6]))
                b_action_table.ix[0, 'joking'] += eval(str(lst[7]))

            elif lst[0] == '"continuation':
                b_action_table.ix[1, 'change'] += eval(str(lst[4]))
                b_action_table.ix[1, 'continuation'] += eval(str(lst[5]))
                b_action_table.ix[1, 'elaboration'] += eval(str(lst[6]))
                b_action_table.ix[1, 'joking'] += eval(str(lst[7]))

            elif lst[0] == '"elaboration':
                b_action_table.ix[2, 'change'] += eval(str(lst[4]))
                b_action_table.ix[2, 'continuation'] += eval(str(lst[5]))
                b_action_table.ix[2, 'elaboration'] += eval(str(lst[6]))
                b_action_table.ix[2, 'joking'] += eval(str(lst[7]))

            else:
                b_action_table.ix[3, 'change'] += eval(str(lst[4]))
                b_action_table.ix[3, 'continuation'] += eval(str(lst[5]))
                b_action_table.ix[3, 'elaboration'] += eval(str(lst[6]))
                b_action_table.ix[3, 'joking'] += eval(str(lst[7]))

            if lst[3] == 'pos"':
                sentiment_table.ix[0, 'change'] += eval(str(lst[4]))
                sentiment_table.ix[0, 'continuation'] += eval(str(lst[5]))
                sentiment_table.ix[0, 'elaboration'] += eval(str(lst[6]))
                sentiment_table.ix[0, 'joking'] += eval(str(lst[7]))

            elif lst[3] == 'neg"':
                sentiment_table.ix[1, 'change'] += eval(str(lst[4]))
                sentiment_table.ix[1, 'continuation'] += eval(str(lst[5]))
                sentiment_table.ix[1, 'elaboration'] += eval(str(lst[6]))
                sentiment_table.ix[1, 'joking'] += eval(str(lst[7]))

            else:
                sentiment_table.ix[2, 'change'] += eval(str(lst[4]))
                sentiment_table.ix[2, 'continuation'] += eval(str(lst[5]))
                sentiment_table.ix[2, 'elaboration'] += eval(str(lst[6]))
                sentiment_table.ix[2, 'joking'] += eval(str(lst[7]))


for action in action_list:
    quest_table.ix[1,action] /= 37.0
    quest_table.ix[0,action] /= 14.0


for action in action_list:
    u_action_table.ix[0,action] /= 16.0
    u_action_table.ix[1, action] /= 12.0
    u_action_table.ix[2, action] /= 10.0
    u_action_table.ix[3, action] /= 13.0

for action in action_list:
    b_action_table.ix[0,action] /= 14.0
    b_action_table.ix[1, action] /= 12.0
    b_action_table.ix[2, action] /= 14.0
    b_action_table.ix[3, action] /= 11.0


for action in action_list:
    sentiment_table.ix[0,action] /= 22.0
    sentiment_table.ix[1, action] /= 6.0
    sentiment_table.ix[2, action] /= 23.0

print b_action_table
print u_action_table
print quest_table
print sentiment_table
'''
quest_table.to_pickle('quest_table.pkl')
quest_table.to_csv(r'quest_table.txt', header=action_list, index=quest_list, sep=' ', mode='a')

length_table.to_pickle('length_table.pkl')
length_table.to_csv(r'length_table.txt', header=action_list, index=quest_list, sep=' ', mode='a')

sentiment_table.to_pickle('sentiment_table.pkl')
sentiment_table.to_csv(r'sentiment_table.txt', header=action_list, index=quest_list, sep=' ', mode='a')
'''