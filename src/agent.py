from os import stat
import random
import torch
import numpy as np
from torch.optim import Adam
from torch.distributions.categorical import Categorical

import net


class Agent():
    def __init__(self, action_space, state_dim, gamma=1):
        self.logits_net = net.MLP(input_dim=state_dim, output_dim=action_space.__len__())
        self.optim = Adam(self.logits_net.parameters(), lr=0.01)
        self.action_space = action_space

    def choose_action(self, state):
        action_propabilities = self.get_policy(state).detach().numpy()
        # print(f"\r{action_propabilities}", end="")
        return np.random.choice(self.action_space, p=action_propabilities)
    
    def get_policy(self, state):
        action_propabilities = self.logits_net(torch.FloatTensor(state))
        return action_propabilities
