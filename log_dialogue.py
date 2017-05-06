import pickle
from pprint import pprint as pp
import datetime
import glob
import random
import os

N_TURN = random.choice(range(5,11)) 
DATA_PATH = "./data/300_convo/"


def main():
    record_convo()
    while input("Do you want to record another conversation? (Y/N)").lower() == "y":
        record_convo()
        

def record_convo():
    # load strategies from pickle
    strats = pickle.load(open("strategies.pkl", "rb"))
    try:
        # create file
        name = input("Before we start: what's your name?\n")
        date = str(datetime.datetime.today().date())
        convo_num = get_convo_num(name)
        filename = DATA_PATH + "{0}_{1}_{2}.txt".format(name.lower(), date, convo_num) 
        f = open(filename, "w")
        
        # record converstaion
        print("----------------------------Here it gones--------------------------------")
        for turn in range(N_TURN):
            strategy = random.choice(list(strats.keys()))
            utterance = random.choice(strats[strategy])
            log("Bot", utterance, strategy, f)
            log(name, input(name + ": "), "None", f)
            strats[strategy].remove(utterance)
        print("-----------------------------The end-------------------------------------")

        # evaluation and wrap up
        scores = get_evaluation()
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
        scores[score_type] = score
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
