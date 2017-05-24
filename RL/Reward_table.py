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


def main():
	
	R_table=pickle.load(open( "R_table.pkl", "rb" ) )
	Q_table=pickle.load(open( "Q_table.pkl", "rb" ) )
	for filename in os.listdir(Q_learning.abs_data_path):
		file = open(Q_learning.abs_data_path+filename,'r')
		strategies_list=[]
		user_lines=[]
		user_utterances1=[]
		temp_dict=pickle.load(open( "temp_dict.pkl", "rb" ) )
		for lines in file:
			
			if not lines.startswith(("overall","engaing","return","interupt","start")):
				if lines.startswith('Bot'):
					strategies_list.insert(len(strategies_list),Q_learning.check_strategies(lines))
				else:
					user_lines.append(Q_learning.get_utterance(lines))
                
			else:
				strategies_list=strategies_list[1:]
				if lines.endswith(','):
					evaluation_value=Q_learning.populate_evaluation(lines)
					user_utterances1=Q_learning.rows_utterance(user_lines)
					user_utterances1=user_utterances1[:len(user_utterances1)-1]
					
					temp_dict[user_utterances1[0]]=temp_dict[user_utterances1[0]]+1
					
					pickle.dump( temp_dict, open( "temp_dict.pkl", "wb" ) )
					R_table.at[user_utterances1[0],strategies_list[0]]=((temp_dict[user_utterances1[0]]-1)*R_table.at[user_utterances1[0],strategies_list[0]]+0.8*float(evaluation_value['start'])+0.2*float(evaluation_value['overall']))/temp_dict[user_utterances1[0]]
					count=1
					for line in user_utterances1[1:len(user_utterances1)]:
						temp_dict[user_utterances1[count]]=temp_dict[user_utterances1[count]]+1
						pickle.dump( temp_dict, open( "temp_dict.pkl", "wb" ) )
						R_table.at[user_utterances1[count],strategies_list[count]]=((temp_dict[user_utterances1[count]]-1)*R_table.at[user_utterances1[count],strategies_list[count]]+0.4*float(evaluation_value['engaing'])+0.4*float(evaluation_value['interupt'])+0.2*float(evaluation_value['overall']))/temp_dict[user_utterances1[count]]               
						count=count+1
					user_utterances1[:]=[]	
				else:
					pass
	    
		file.close()
	#print("following is the Reward_table")
	#print(R_table)
	R_table.to_pickle('R_table.pkl')
	pickle.dump( temp_dict, open( "temp_dict.pkl", "wb" ) )
	
	
if __name__ == "__main__":
	
    Q_learning = Qlearning()
	
    main()