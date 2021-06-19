import csv
import gym
import envs
from env.controller import Controller
import numpy as np 

my_contr = Controller()
ENV_ID = "CustomEnv-v0"
my_env = gym.make(ENV_ID)
done = False
my_env.current_states = my_env.reset()
my_env.save_counter = 10000
my_env.constant_dict = {
    "u": 0.0,
    "v": 1.0,
    "w": 1.0,
    "p": 1.0,
    "q": 1.0,
    "r": 1.0,
    "fi": 1.0,
    "theta": 1.0,
    "si": 1.0,
    "x": 1.0,
    "y": 1.0,
    "z": 1.0,
    "a": 1.0,
    "b": 1.0,
    "c": 1.0,
    "d": 1.0,
}
while not done:
    current_action = my_contr.Controller_model(my_env.current_states, my_env.Ts * my_env.counter)
    # print(current_action[1], current_action[2])
    my_env.current_states, b, done, _ = my_env.step(np.array((0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0), dtype=np.float64))
    # my_env.current_states, b, done, _ = my_env.step([current_action[0], 0.1, current_action[2], current_action[3]])

    # print(my_env.current_states)

    fields = current_action
    with open("ctrl.csv", "a") as f:
        writer = csv.writer(f)
        writer.writerow(fields)
my_env.reset()
# if my_env.best_reward > current_best_rew:
#     current_best_rew = my_env.best_reward
# with open("reward_step.csv", "a") as f:
#     writer = csv.writer(f)
#     writer.writerow(sl_action)
