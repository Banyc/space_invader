import os

import numpy as np
import torch

import pickle

from agent import Agent
from environment import Environment


class Batch_package:
    def __init__(self) -> None:
        self.rewards = []
        self.states = []
        self.actions = []
        self.counter = 0


def save_model(anything, directory="model_data"):
    os.makedirs(directory, exist_ok=True)
    with open(os.path.join(directory, "latest.pkl"), "wb") as fp:
        pickle.dump(anything, fp)

def load_model(directory="model_data"):
    with open(os.path.join(directory, "latest.pkl"), "rb") as fp:
        pickle.load(fp)


def discount_rewards(rewards, gamma=0.99):
    rewards_discounted = []

    for i in range(rewards.__len__()):
        rewards_discounted.append(rewards[i] * (gamma ** i))

    rewards_discounted = np.array(rewards_discounted)
    
    rewards_discounted[:] = rewards_discounted[::-1].cumsum()[::-1]

    return rewards_discounted - rewards_discounted.mean()



def run_one_episode(env: Environment, agent: Agent, batch: Batch_package, total_rewards, max_step=5000):
    is_game_over = False

    states = []
    rewards = []
    actions = []
    step = 0

    while not is_game_over and step < max_step:
        state = env.get_state()
        action = agent.choose_action(state)
        env.play_step(action)
        is_game_over = env.is_game_over

        states.append(state)
        rewards.append(env.get_reward())
        actions.append(action)
        # state = env.get_state()

        step += 1

    batch.rewards.extend(discount_rewards(rewards))
    batch.states.extend(states)
    batch.actions.extend(actions)
    batch.counter += 1
    total_rewards.append(sum(rewards))


def train(num_episodes=200, batch_size=16, is_render=False):
    env = Environment()
    state = env.get_state()
    action_space = env.get_action_space()
    agent = None
    episode_index_start = 0
    try:
        agent, episode_index_start = load_model()
    except:
        agent = Agent(action_space=action_space, state_dim=state.__len__())
    

    optimizer = agent.optim

    batch = Batch_package()
    total_rewards = []


    for episode_index in range(episode_index_start, num_episodes):
        run_one_episode(env, agent, batch, total_rewards)

        if batch.counter == batch_size:
            optimizer.zero_grad()
            state_tensor = torch.FloatTensor(batch.states)
            reward_tensor = torch.FloatTensor(batch.rewards)
            action_tensor = torch.LongTensor(batch.actions)

            # loss
            log_probability = torch.log(
                agent.get_policy(state_tensor))
            selected_log_probabilities = reward_tensor * \
                log_probability[
                    np.arange(action_tensor.__len__()),
                    action_tensor]
            loss = -selected_log_probabilities.mean()

            loss.backward()
            # modify parameters
            optimizer.step()

            save_model((agent, episode_index))

            del batch.actions[:]
            del batch.rewards[:]
            del batch.states[:]
            batch.counter = 0
        env.reset()
        
        print("\rEp: {} Average of last 10: {:.2f}".format(
                    episode_index + 1, np.mean(total_rewards[-10:])), end="")

if __name__ == "__main__":
    train()

