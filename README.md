# Reinforcement_learning_NLP
Implementing Reinforcement Learning to find the best dialogue strategy for a conversation agent (chatbot) by search for maximum award.


# To record a converstaion, do:
1. `git clone https://github.com/MollyZhang/Reinforcement_learning_NLP.git`
2. `cd Reinforcement_learning_NLP`
3. `cd RL`
4. `python run.py`  


If you want to train and populate reward table based on the 300 conversations recorded,type f,if you want to try a new dialogue,type s,if you want to view the accuracy of the evaluation model,type e,if you want to view the reward table,type r,if you want to view the Q_table type q

### Future improvements
- Dealing with user saying gibberish like "dfkjlskdfj"
- Dealing user repeat itself
- Dealing with user insult

### A brief overview of the code
We have learnt currently from the 300 odd conversations and populated the Reward table based on the user evaluation metrics.
The first block initializes the variables and the Q_table and the R_table.We have 6 strategies and 18 state variables based on the 4 state metrics like (If the user utterance is a question or not,the length of the utterance,the sentiment of the uttterance and whether the utterance is at the beginning(first utterance of the user),we have thus created 18 combinations of these states.

The second block are all the utility functions used and called by the later blocks.The most prominent amongst them being the training() where we train and populate the Q_table.The logic of Q_learning is implemented here.

The third block populates the reward table according to whether the utterance is at the beginning(in this case,it is calculated according to 0.8*start+0.2* overall,while for the rest utterances,it is 0.4*engaging+04*interrupt+0.2*overall.

The fourth block is used for training where it calls the training() method.

The fifth block records the new conversations and poplates the strategies based on the Q_table and updates the Q_table.
Work on evaluation is still in progress.
