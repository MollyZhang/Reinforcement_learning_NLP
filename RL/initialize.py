import pickle
import pandas as pd

def main():
	R_table = pd.DataFrame.from_items([('qs+b', [0.0, 0.0, 0.0,0.0,0.0,0.0]), ("qs+e", [0.0, 0.0, 0.0,0.0,0.0,0.0]),("qs-b", [0.0, 0.0, 0.0,0.0,0.0,0.0]),("qs-e", [0.0, 0.0, 0.0,0.0,0.0,0.0]),
                                           ("qs'b", [0.0, 0.0, 0.0,0.0,0.0,0.0]),("qs'e", [0.0, 0.0, 0.0,0.0,0.0,0.0]),("q'ls+b", [0.0, 0.0, 0.0,0.0,0.0,0.0]),("q'ls+e", [0.0, 0.0, 0.0,0.0,0.0,0.0]),
                                            ("q'ls-b", [0.0, 0.0, 0.0,0.0,0.0,0.0]), ("q'ls-e", [0.0, 0.0, 0.0,0.0,0.0,0.0]),("q'ls'b", [0.0, 0.0, 0.0,0.0,0.0,0.0]),("q'ls'e", [0.0, 0.0, 0.0,0.0,0.0,0.0]),
                                           ("q'l's+b", [0.0, 0.0, 0.0,0.0,0.0,0.0]),("q'l's+e", [0.0, 0.0, 0.0,0.0,0.0,0.0]),("q'l's-b", [0.0, 0.0, 0.0,0.0,0.0,0.0]),("q'l's-e", [0.0, 0.0, 0.0,0.0,0.0,0.0]),
                                          ("q'l's'b", [0.0, 0.0, 0.0,0.0,0.0,0.0]),("q'l's'e", [0.0, 0.0, 0.0,0.0,0.0,0.0])],
                                            orient='index', 
                                          columns=['question', 'elaborate', 'opinion','affirmative','negative','neutral'])

	R_table.to_pickle('R_table.pkl')
	
	temp_dict={"qs+b":0,"qs+e":0,"qs-b":0,"qs-e":0,"qs'b":0,"qs'e":0,"q'ls+b":0,"q'ls+e":0,"q'ls-b":0,"q'ls-e":0,"q'ls'b":0,"q'ls'e":0,
           "q'l's+b":0,"q'l's+e":0,"q'l's-b":0,"q'l's-e":0,"q'l's'b":0,"q'l's'e":0}
	
	
	pickle.dump( temp_dict, open( "temp_dict.pkl", "wb" ) )
	
	count_evaluation_dict=0
	pickle.dump(count_evaluation_dict,open("count_evaluation_dict.pkl","wb"))
	
	evaluation_dict={"overall":0,"start":0,"interupt":0,"engaing":0,"return":0}
	pickle.dump(evaluation_dict,open("evaluation_dict.pkl","wb"))
	
	Q_table=pd.DataFrame.from_items([('qs+b', [0.0, 0.0, 0.0,0.0,0.0,0.0]), ("qs+e", [0.0, 0.0, 0.0,0.0,0.0,0.0]),("qs-b", [0.0, 0.0, 0.0,0.0,0.0,0.0]),("qs-e", [0.0, 0.0, 0.0,0.0,0.0,0.0]),
                                           ("qs'b", [0.0, 0.0, 0.0,0.0,0.0,0.0]),("qs'e", [0.0, 0.0, 0.0,0.0,0.0,0.0]),("q'ls+b", [0.0, 0.0, 0.0,0.0,0.0,0.0]),("q'ls+e", [0.0, 0.0, 0.0,0.0,0.0,0.0]),
                                            ("q'ls-b", [0.0, 0.0, 0.0,0.0,0.0,0.0]), ("q'ls-e", [0.0, 0.0, 0.0,0.0,0.0,0.0]),("q'ls'b", [0.0, 0.0, 0.0,0.0,0.0,0.0]),("q'ls'e", [0.0, 0.0, 0.0,0.0,0.0,0.0]),
                                           ("q'l's+b", [0.0, 0.0, 0.0,0.0,0.0,0.0]),("q'l's+e", [0.0, 0.0, 0.0,0.0,0.0,0.0]),("q'l's-b", [0.0, 0.0, 0.0,0.0,0.0,0.0]),("q'l's-e", [0.0, 0.0, 0.0,0.0,0.0,0.0]),
                                          ("q'l's'b", [0.0, 0.0, 0.0,0.0,0.0,0.0]),("q'l's'e", [0.0, 0.0, 0.0,0.0,0.0,0.0])],
                                            orient='index', 
                                          columns=['question', 'elaborate', 'opinion','affirmative','negative','neutral'])
	Q_table.to_pickle('Q_table.pkl')

	evaluation_dict={"overall":0,"start":0,"interupt":0,"engaing":0,"return":0}
	pickle.dump( evaluation_dict, open( "evaluation_dict.pkl", "wb" ) )
	
if __name__ == "__main__":
    
    main()