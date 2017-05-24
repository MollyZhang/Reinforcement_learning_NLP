#CODE FOR INITIALIZING REWARD TABLE
import pickle
from pprint import pprint as pp
import datetime
import glob
import random
import os
from textblob import TextBlob
import pandas as pd
import sys



class Qlearning:
	
	N_TURN = 3
	list1=[]
	bot_strategies=[]
	learning_rate=0.9
	discount_factor=0.9
	epsilon=0.9
	data_path = "../data/300_convo/"
	R_table=pickle.load(open( "R_table.pkl", "rb" ) )
	Q_table=pickle.load(open( "Q_table.pkl", "rb" ) )
	temp_dict=pickle.load(open( "temp_dict.pkl", "rb" ) )
	evaluation_value={}
	evaluation_dict = pickle.load( open( "evaluation_dict.pkl", "rb" ) )
	standard_evaluation_dict={"overall":3,"start":3,"interupt":3,"engaing":3,"return":3}
	rel_path = "../strategies.pkl"
	abs_data_path = os.path.join(os.getcwd(), data_path)
	abs_strategies_path = os.path.join(os.getcwd(), rel_path)
	user_utterances=[]
	strategies_list=[]
	user_lines=[]
	all_state_variables=['qs+b',"qs+e","qs-b","qs-e","qs'b","qs'e","q'ls+b","q'ls+e","q'l's+b","q'l's+e","q'l's-b","q'l's-e","q'l's'b","q'l's'e","q'l's'b","q'l's'e","q'l's+b","q'l's+e","q'l's-b","q'l's-e"]
	count_evaluation_dict=0
	#temporary dictionary which stores the count of the recorded utterance till date,this is used for calculating the average to be stored in state table
	

		
	#utility functions
	
	def check_strategies(self,response):
		temp_list=response.split(":")
		temp_list2=temp_list[0].split('_')
		return temp_list2[1]
    

	def get_utterance(self,line):
		temp_list=line.split(":")
		value=temp_list[3]
		return value
		
	def max_beginning(self):
		value=''
		max=0
		for column in self.Q_table:
			for values in self.all_state_variables:
				if "b" in values:
					if self.Q_table.at[values,column]>max:
						max=self.Q_table.at[values,column]
						#print(max)
						value=column
		return value
		
	def populate_evaluation(self,line):
		list1=line.split(',')
		
		for values in list1:
			if values is not '':
				list2=values.split('=')
				self.evaluation_value[list2[0]]=list2[1]
		
		return self.evaluation_value

	
	def next_state(self,utterance_no,utterances):
		self.user_utterances=utterances
		
		if not utterance_no==len(self.user_utterances)-1:
			
			return self.user_utterances[utterance_no+1]
		else:
			return 0
    
	def max_q_value(self,utterance):
		max=0
		for column in self.Q_table:
			if self.Q_table.at[utterance,column]>max:
				max=self.Q_table.at[utterance,column]
		return max

	def max_strategy(self,utterance):
		value=''
		max=0
		
		for column in self.Q_table:
			if self.Q_table.at[utterance,column]>max:
				max=self.Q_table.at[utterance,column]
				value=column
		return value

	
	def question_or_not(self,words):
		if "?" not in words:
			q="q'"
		else:
			q="q"
    
		return q

	def count_no_words(self,words):
		no=len(words.split())
		if no>=10:
        
			l="l"
		else:
        
			l="l'"
		return l

	def sentiment(self,words):
		blob = TextBlob(words)
		senti=blob.sentiment
		if senti.polarity<0.2 and senti.polarity>-0.2:
			s="s'"
		else:
			if senti.polarity>0:
				s="s+"
			else:
				s="s-"
		return s
    
	def training(self,indexes,user_utterances,strategies_list):
		self.strategies_list=strategies_list
		self.user_utterances=user_utterances
		temp_dict=pickle.load(open( "temp_dict.pkl", "rb" ) )
		R_table=pickle.load(open( "R_table.pkl", "rb" ) )
		Q_table=pickle.load(open( "Q_table.pkl", "rb" ) )
		count=0
		for line in self.user_utterances:
			
			next_utterance=self.next_state(indexes,self.user_utterances)
			
			prev_value=Q_table.at[self.user_utterances[indexes],self.strategies_list[indexes]]
			if next_utterance is not 0:
				Q_table=pickle.load(open( "Q_table.pkl", "rb" ) )
				Q_table.at[self.user_utterances[indexes],self.strategies_list[indexes]]=((temp_dict[self.user_utterances[indexes]]-1)*Q_table.at[self.user_utterances[indexes],self.strategies_list[indexes]]+Q_table.at[self.user_utterances[indexes],self.strategies_list[indexes]]+Qlearning.learning_rate*R_table.at[self.user_utterances[indexes],self.strategies_list[indexes]] + self.discount_factor*self.max_q_value(next_utterance)-Q_table.at[self.user_utterances[indexes],self.strategies_list[indexes]])/temp_dict[self.user_utterances[indexes]]
				count=count+1
				print(user_utterances[indexes],self.strategies_list[indexes],Q_table.at[self.user_utterances[indexes],self.strategies_list[indexes]])
				#print(count)
				#print(Q_table)
				Q_table.to_pickle('Q_table.pkl')
				
			else:
				Q_table=pickle.load(open( "Q_table.pkl", "rb" ) )
				Q_table.at[self.user_utterances[indexes],self.strategies_list[indexes]]=R_table.at[user_utterances[indexes],self.strategies_list[indexes]]
				Q_table.to_pickle('Q_table.pkl')
		self.user_utterances=[]
		Q_table.to_pickle('Q_table.pkl')
		return Q_table
			

	def beginning_end(self,line,list):
		length=len(list)
		if list.index(line)==0:
        
			var="b"
		else:
        
			var="e"
		return var

	def rows_utterance(self,list1):
		self.user_utterances=[]
		for values in list1:
			if self.question_or_not(values)=="q":
				if self.sentiment(values)=="s+":
					if self.beginning_end(values,list1)=="b":
						result="qs+b"
					else:
						result="qs-e"
				elif self.sentiment(values)=="s-":
					if self.beginning_end(values,list1)=="b":
						result="qs-b"
					else:
						result="qs-e"
				else:
					if self.beginning_end(values,list1)=="b":
						result="qs'b"
					else:
						result="qs'e"
			else:
				if self.count_no_words(values)=="l":
            
					if self.sentiment(values)=="s+":
                
						if self.beginning_end(values,list1)=="b":
							result="q'ls+b"
						else:
							result="q'ls+e"
					elif self.sentiment(values)=="s-":
						if self.beginning_end(values,list1)=="b":
							result="q'ls-b"
						else:
							result="q'ls-e"
					else:
						if self.beginning_end(values,list1)=="b":
							result="q'ls'b"
						else:
							result="q'ls'e"
				else:
					if self.sentiment(values)=="s+":
                
						if self.beginning_end(values,list1)=="b":
							result="q'l's+b"
						else:
							result="q'l's+e"
					elif self.sentiment(values)=="s-":
						if self.beginning_end(values,list1)=="b":
							result="q'l's-b"
						else:
							result="q'l's-e"
					else:
						if self.beginning_end(values,list1)=="b":
							result="q'l's'b"
						else:
							result="q'l's'e"
			self.user_utterances.append(result)
		return self.user_utterances

	def single_utterance(self,values):
		if self.question_or_not(values)=="q":
			if self.sentiment(values)=="s+":
				result="qs+e"
			elif self.sentiment(values)=="s-":
				result="qs-e"
			else:
				result="qs'e"
		else:
			if self.count_no_words(values)=="l":
            
				if self.sentiment(values)=="s+":
                
					result="q'ls+e"
				elif self.sentiment(values)=="s-":
					result="q'ls-e"
				else:
					result="q'ls'e"
			else:
				if self.sentiment(values)=="s+":
                
					result="q'l's+e"
				elif self.sentiment(values)=="s-":
					result="q'l's-e"
				else:
					result="q'l's'e"
        
		return result
	def calculate_evaluation(self,temp_evaluation_dict):
		count_evaluation_dict = pickle.load( open( "count_evaluation_dict.pkl", "rb" ) )
		self.evaluation_dict = pickle.load( open( "evaluation_dict.pkl", "rb" ) )
		count_evaluation_dict=count_evaluation_dict+1
		pickle.dump( count_evaluation_dict, open( "count_evaluation_dict.pkl", "wb" ) )
		for values in temp_evaluation_dict:
			
			self.evaluation_dict[values]=(self.evaluation_dict[values]*(count_evaluation_dict-1)-temp_evaluation_dict[values]+self.standard_evaluation_dict[values])/count_evaluation_dict
		
		pickle.dump( self.evaluation_dict, open( "evaluation_dict.pkl", "wb" ) )
		
	