The simulation is divided into 3 parts:
Initialization block:
In this block I have initialised state variables:I have considered 4 state variables aand around 18 combinations of them
These 4 state variables are based on:
1)Whether the user utterance is a question
2)Whether the user utterence has strong sentiment(positive,negative,or neutral)
3)Whether the sentence is long enough
4)Whether the sentence is at the beginning or the end of the conversation
Accordingly,there are 4 functions:question_or_not,count_no_words,sentiment,beginning_end

I have 4 strategies defined for now:'affirmative', 'opinion', 'negative','question'

I have defined temp_dict which maintains the count of the state variables till,now this is used for storing the average in the state_action_dict dictionary
State_action_dict contains state variables as the rows and strategies as the columns

Training:
record_check:this function understands the type of state variable of the user question and stores in the state_action_dict
rows_utterance:this function takes the crude list of user utterences(eg:['Very true', 'Thanks', 'What did you mena?'] and converts in this form
["q'l's+b", "q'l's+b", "qs'e"],suitable enough to store in the state_action_dict.
main:creates the list of user_utterences(from rows_utternce) and strategies taken by the bot(here,all the strategies were selected by random)

I have trained on a relative smaller dataset(consisting of 3-4 conversations each consisting of 3 utterences per conversation).


Testing:
store:this function is used for storing the test values in the state_action_dict
check_and_pass:this function checks for the maximum values amongst the 4 strategies for the entered state variable and returns the strategy which is then 
used by the main to get random choices from the maximum strategy.
form_user_utterancelist:this is similar to the rows_utterance in the training block.
rows_utterance:this method only classifies one selected user utterence.
main:similar to the main in training block
