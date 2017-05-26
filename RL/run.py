import sys
import os
import pickle
def main():

	while input("Do you want to run this : ").lower() == "y":
		start()
def start():		
	print("If you are running it for first time,ie:if you want to train the model and learn"
	"type f,if you want to run again,type s,if you want to see the evaluation,type e","if you want to see the Q_table,type q",
	"if you want to see the Reward table,type r")


	arg=str(input())
	if(arg=='f'):

		os.system("python initialize.py")
		os.system("python Reward_table.py")
		os.system("python training.py")
		os.system("python Reinforcement_Learning.py")
	elif(arg=='s'):
		os.system("python Reinforcement_Learning.py")
	elif(arg=='e'):
		evaluation_dict = pickle.load( open( "evaluation_dict.pkl", "rb" ) )
		for values in evaluation_dict.keys():
			evaluation_dict[values]=100-(evaluation_dict[values]*20)
		print("Following is the accuracy of the evaluated score in percentages")
		print(evaluation_dict)
	elif(arg=='q'):
		Q_table = pickle.load( open( "Q_table.pkl", "rb" ) )
		
		print("Following is the Q_table")
		print(Q_table)
	elif(arg=='r'):
		R_table = pickle.load( open( "R_table.pkl", "rb" ) )
		
		print("Following is the R_table")
		print(R_table)
	else:
		print("type again")
		
if __name__ == "__main__":
    
    main()