import pickle
from pprint import pprint as pp
import datetime
import glob
import random
import os

N_TURN = 10

def main():
    # load strategies from pickle
    strats = pickle.load(open("strategies.pkl", "rb"))

    try:
        # create file
        name = input("Before we start: what's your name? (Molly, Wei or Nehal)?\n")
        date = str(datetime.datetime.today().date())
        convo_num = get_convo_num(name)
        filename = "./data/{0}_{1}_{2}.txt".format(name.lower(), date, convo_num) 
        f = open(filename, "w")
    
        # record converstaion
        strategy = random.choice(list(strats.keys()))
        print("--------------------here it gones--------------------------------")
        log("Bot", random.choice(strats[strategy]), strategy, f)
        for turn in range(N_TURN-1):
            log(name, input(name + ": "), "None", f)
            strategy = random.choice(list(strats.keys()))
            log("Bot", random.choice(strats[strategy]), strategy, f)
        log(name, input(name + ": "), "None", f)

        # evaluation and wrap up
        score = input("\nHow is the conveseration? (number between 0 to 5) ")
        while ord(score) < ord("0") or ord(score) > ord("5"):
            score = input("Type a integer in [0,1,2,3,4,5], otherwise I will keep asking")
        f.write("evaluation={0}".format(score))
        f.close()
        print("Done!")
    
    except KeyboardInterrupt:
        os.remove(filename)
        print("key board interupted, nothing is recorded")
    except:
        raise    


def get_convo_num(name):
    try:
        files = glob.glob("./data/{0}_*".format(name))
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
