import pickle
from pprint import pprint as pp
import datetime
import glob
import random
import os
from textblob import TextBlob
import pandas as pd
import sys
from Q_learning import Qlearning

Q_learning=Qlearning()
N_TURN = random.choice(range(5,11)) 
DATA_PATH = Q_learning.abs_data_path+'/new_convo/'
strats = pickle.load(open(Q_learning.abs_strategies_path, "rb"))
strategies_list=[]
utterances=[]
Q_table=pickle.load(open( "Q_table.pkl", "rb" ) )
def main():
	
    record_convo()
    while input("Do you want to record another conversation? (Y/N)").lower() == "y":
        record_convo()
        

def record_convo():
    # load strategies from pickle
	utterances=[]
	strategies_list=[]
	list1=[]
	try:
        # create file
		name = input("Before we start: what's your name?\n")
		date = str(datetime.datetime.today().date())
		convo_num = get_convo_num(name)
		filename = Q_learning.abs_data_path + "{0}_{1}_{2}.txt".format(name.lower(), date, convo_num) 
		f = open(filename, "w")
        
        # record converstaion
		print("----------------------------Here it goes--------------------------------")
        #strategy=Q_table.iloc[0].argmax()
		strategy = Q_learning.max_beginning()
		
		utterance = random.choice(strats[strategy])
		log("Bot", utterance, strategy, f)
		strats[strategy].remove(utterance)
		strategies_list.append(strategy)
		for turn in range(N_TURN-1):
			answer=str(input(name + ": "))
			log(name, answer, "None",f)
			utter=Q_learning.single_utterance(answer)
			strategy=''
            #for exploration
			if random.random()<Q_learning.epsilon:
				strategy = random.choice(list(strats.keys()))
			else:
				strategy=Q_learning.max_strategy(utter)
			utterances.append(utter)
			strategies_list.append(strategy)
			utterance=random.choice(list(strats[strategy]))
			log("Bot", utterance, strategy, f)
			strats[strategy].remove(utterance)
            
			utter=''
		answer=str(input(name + ": "))
		log(name, answer, "None",f) 
		strategies_list=strategies_list[1:]
    
		utterances=utterances[:len(utterances)-1]
		for values in utterances:
			Q_table=pickle.load(open( "Q_table.pkl", "rb" ) )
			indexes=utterances.index(values)
			Q_table=Q_learning.training(indexes,utterances,strategies_list)
			Q_table.to_pickle('Q_table.pkl')
		print("-----------------------------The end-------------------------------------")

        # evaluation and wrap up
		scores = get_evaluation()
		Q_learning.calculate_evaluation(scores)
		for score_type, score_value in scores.items():
			f.write("{0}={1},".format(score_type, score_value))
		f.close()
		print("Done!")
    
	except:
		os.remove(filename)
		raise    


def get_evaluation():
    scores = {}
    questions = {"overall": "How is the conveseration overall? (0 is aweful, 5 is amazing)\n",
                 "start": "How is the begining of the converstaion? (0: weird and out of context, 5: natural)\n",
                 "interupt": "How is the continuity of the conversation? (0: you get interupted too much, 5: very fluid and coherent)\n",
                 "engaing": "How engaging or interesting is the conversation? (0 is boring, 5 is very interesting)\n",
                 "return": "Would you like to talk to this bot again? (0 is not at all, 5 is definitely)\n"}
    for score_type in questions.keys():
        score = input(questions[score_type])
        while len(score) > 1 or ord(score) < ord("0") or ord(score) > ord("5"):
            score = input("Type a integer between [0,5], otherwise I will keep asking")
        scores[score_type] = int(score)
    return scores
		
    return scores


def get_convo_num(name):
    try:
        files = glob.glob(DATA_PATH + name.lower() + "_*")
        existing_nums = list(map(int, [i[:-4].split("_")[-1] for i in files]))
        return max(existing_nums) + 1
    except ValueError:
        return 1
    

def log(role, utter, strategy, file):
    if role == "Bot":
        print("Bot says: ", utter)
    time = datetime.datetime.now().strftime("%H:%M:%S")
    file.write("{0}_{1}_{2}:{3}\n".format(role, strategy, time, utter))

if __name__ == "__main__":
    
    main()