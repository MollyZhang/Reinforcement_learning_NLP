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

#for training from the model
def main():
	
	R_table=pickle.load(open( "R_table.pkl", "rb" ) )
	Q_table=pickle.load(open( "Q_table.pkl", "rb" ) )
	temp_dict=pickle.load(open( "temp_dict.pkl", "rb" ) )
	for filename in os.listdir(Q_learning.abs_data_path):
		
		file = open(Q_learning.abs_data_path+filename,'r')
		strategies_list=[]
		user_lines=[]
		user_utterances=[]
		for lines in file:
        
			if not lines.startswith(("overall","engaing","return","interupt","start")):
				if lines.startswith('Bot'):
					strategies_list.insert(len(strategies_list),Q_learning.check_strategies(lines))
				else:
					user_lines.append(Q_learning.get_utterance(lines))
		user_utterances=Q_learning.rows_utterance(user_lines)
		strategies_list=strategies_list[1:]
    
		user_utterances=user_utterances[:len(user_utterances)-1]
		
		for values in user_utterances:
			Q_table=pickle.load(open( "Q_table.pkl", "rb" ) )
			indexes=user_utterances.index(values)
			
			Q_table=Q_learning.training(indexes,user_utterances,strategies_list)
			Q_table.to_pickle('Q_table.pkl')
	
		

			

if __name__ == "__main__":
    Q_learning = Qlearning()
    main()