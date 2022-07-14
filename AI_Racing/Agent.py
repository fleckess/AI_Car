import torch
import random
import numpy as np
from collections import deque

import Globals
from simulation import AI_CAR, Direction
from model import deep_QNET, Qvalue_Trainer
from visualplot import plot

MAX_MEMORY = 90_000
BATCH_SIZE = 512
LEARNING_RATE = 0.001

class Agent:
    def __init__(self):
        self.epsilon = 0
        self.n_games = 0
        self.gamma = 0.7
        self.model = deep_QNET(10, 512, 3)
        self.trainer = Qvalue_Trainer(self.model, lr=LEARNING_RATE, gamma=self.gamma)
        self.memory = deque(maxlen=MAX_MEMORY)


    def remember(self, state, action, reward, next_state, episode_end):
        self.memory.append((state, action, reward, next_state, episode_end))

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)
        else:
            mini_sample = self.memory
        states, actions, rewards, next_states, episode_ends = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, episode_ends)

    def train_short_memory(self, state, action, reward, next_state, episode_end):
        self.trainer.train_step(state, action, reward, next_state, episode_end)

    def get_action(self, state):
        self.epsilon = 85 - self.n_games
        det_move = [0,0,0]
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 2)
            det_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            det_move[move] = 1
        return det_move

    def get_state(self, game):
        car = game.player1
        point_l = (car.x -3, car.y)
        point_r = (car.x + 3, car.y)
        point_u = (car.x, car.y - 3)
        point_d = (car.x, car.y + 3)

        stripe_point = game.check_which_stripe()
        stripe_x = stripe_point[0]
        stripe_y = stripe_point[1]

        dir_f = game.direction == Direction.FORWARD
        dir_r = game.direction == Direction.RIGHT
        dir_l = game.direction == Direction.LEFT
        # Danger straight
        state = [
            (dir_f and game.outside_of_road_detection(point_r)) or
            (dir_l and game.outside_of_road_detection(point_d)) or
            (dir_r and game.outside_of_road_detection(point_u)) or
            (dir_f and game.outside_of_road_detection(point_l)),


            # Danger right
            (dir_f and game.outside_of_road_detection(point_u)) or
            (dir_l and game.outside_of_road_detection(point_u)) or
            (dir_r and game.outside_of_road_detection(point_d)) or
            (dir_l and game.outside_of_road_detection(point_l)),

            # Danger left
            (dir_f and game.outside_of_road_detection(point_d)) or
            (dir_l and game.outside_of_road_detection(point_r)) or
            (dir_r and game.outside_of_road_detection(point_r)) or
            (dir_r and game.outside_of_road_detection(point_l)),

            dir_l,
            dir_f,
            dir_r,

            stripe_x < car.x,
            stripe_x > car.x,
            stripe_y < car.y,
            stripe_y > car.y
        ]
        return np.array(state, dtype=int)

def train_agent():
    plot_scores = []
    plot_mean_scores = []
    agent = Agent()
    game = AI_CAR()
    record = 0
    total_score = 0
    while True:
        old_state = agent.get_state(game)
        move = agent.get_action(old_state)
        reward, episode_end, score = game.simulation_step(move)
        state_new = agent.get_state(game)

        agent.train_short_memory(old_state, move, reward, state_new, episode_end)
        agent.remember(old_state, move, reward, state_new, episode_end)

        if episode_end == True:
            Globals.flag_episode = False
            game.new_episode()
            agent.n_games+=1
            agent.train_long_memory()

            if score > record:
                record = score
            print("Spiel Nummer:", agent.n_games, "Score: ", score, "Record:", record)





if __name__ == '__main__':
    train_agent()


