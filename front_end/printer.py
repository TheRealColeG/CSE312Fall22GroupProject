import numpy as np
import gym
from gym import spaces
import matplotlib.pyplot as plt
import random
import time

class BoardEnvironment(gym.Env):
    
    def __init__(self):
        self.observation_space = spaces.Discrete(121)
    
    def default(self):
        #self.agent_pos = [3,1]
        #self.goal_pos = [0,3]
        #self.state = np.zeros((5,5))
        #self.state[tuple(self.agent_pos)] = 1
        #self.state[tuple(self.goal_pos)] = 0.5
        observation = self.state.flatten()
        return observation
    
    def print(self, board):
        NotImplemented
    
    def render(self):
        plt.imshow(self.state)
        plt.show()



#TA NOTES: 
#Modify the HTML to "generate" the proper image

#Need to generate a new image => host it => 

# Recommendation: go w/ htmlm front end, update as we go ahead