import numpy as np
import pandas as pd


class Qlearning:
    def __init__(self, actions,learning_rate):
        self.actions = actions  # a list
        #self.learning_rate = 0.1
        # learning rate must decaying over time/turn
        self.learning_rate = learning_rate
        self.discount = 0.9
        self.epsilon = 0.5
        self.q_table = pd.DataFrame(columns=self.actions)

    def choose_action(self, state):
        self.check_state_exist(state)
        # action selection
        if np.random.uniform() < self.epsilon:
            # choose best action
            state_action = self.q_table.ix[state, :]
            state_action = state_action.reindex(np.random.permutation(state_action.index))     # some actions have same value
            action = state_action.argmax()
        else:
            # choose random action
            action = np.random.choice(self.actions)

        return action

    def learn(self, state, action, reward, next_state, turn_number):
        self.check_state_exist(state)
        self.check_state_exist(next_state)
        q_original = self.q_table.ix[state, action]
        if state != 'terminal':
            q_target = round(reward + self.discount * self.q_table.ix[next_state, :].max() ,3) # next state is not terminal
        else:
            q_target = reward  # next state is terminal

        #self.q_table.ix[state, action] += round(self.learning_rate * (q_target - q_original),3)  # update
        self.q_table.ix[state, action] += round(self.learning_rate.ix[0,turn_number] * (q_target - q_original), 3)  # update

    def check_state_exist(self, state):
        if state not in self.q_table.index:
            # append new state to q table
            self.q_table = self.q_table.append(
                pd.Series(
                    [0]*len(self.actions),
                    index=self.q_table.columns,
                    name=state,
                )
            )