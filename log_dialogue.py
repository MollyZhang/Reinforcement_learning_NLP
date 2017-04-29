import pickle
from pprint import pprint as pp
import datetime
import glob
import random

N_TURN = 10

def main():

    # load strategies from pickle
    strats = pickle.load(open("strategies.pkl", "rb"))

    # create file
    name = input("Before we start: what's your name? (Molly, Wei or Nehal)?\n")
    date = str(datetime.datetime.today().date())
    convo_num = get_convo_num(name)
    f = open("./data/{0}_{1}_{2}.txt".format(name.lower(), date, convo_num), "w")
    
    # record converstaion
    strategy = random.choice(list(strats.keys()))
    print("--------------------here it gones--------------------------------")
    log("Bot", random.choice(strats[strategy]), strategy, f)
    for turn in range(N_TURN-1):
        log(name, input(), "None", f)
        strategy = random.choice(list(strats.keys()))
        log("Bot", random.choice(strats[strategy]), strategy, f)
    log(name, input(), "None", f)

    # evaluation and wrap up
    try:
        score = int(input("\nHow is the conveseration? (number between 0 to 5) "))
    except:
        score = int(input("Type a number between 0-5, otherwise you'll have to type everything all over again"))
    f.write("evaluation={0}".format(score))
    f.close()


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
