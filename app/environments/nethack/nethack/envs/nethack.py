
import gym
import aicrowd_gym
import nle
import numpy as np

import random
import os
from io import StringIO
import sys
from functools import cmp_to_key

import config

from stable_baselines import logger
from stable_baselines.common import set_global_seeds


class ObservationWrapper(gym.ObservationWrapper):
    def __init__(self, env):
        super().__init__(env)
        self.observation_space = gym.spaces.Box(0, 1, (21, 79, 256))
    
    def observation(self, obs):
        # modify obs
        return np.eye(256)[obs['chars']]


class NetHackEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, verbose = False, manual = False):
        super(NetHackEnv, self).__init__()
        self.name = 'nethack'
        self.manual = manual
        
        self.n_players = 1
        self.env = gym.wrappers.TimeLimit(ObservationWrapper(aicrowd_gym.make('NetHackChallenge-v0')), max_episode_steps=10000)
        
        self.action_space = self.env.action_space
        self.observation_space = self.env.observation_space
        self.verbose = verbose


    @property
    def legal_actions(self):
        legal_actions = np.ones(self.action_space.n)
        return legal_actions


    def step(self, action):
       
        self.observation, reward, self.done, _ = self.env.step(action)

        return self.observation, [reward], self.done, {}


    def reset(self):
        
        self.current_player_num = 0
        self.turns_taken = 0
        self.done = False
        logger.debug(f'\n\n---- NEW GAME ----')
        self.observation = self.env.reset()
        os.chdir('/app')
        return self.observation


    def render(self, mode='human', close=False):

        if close:
            return
        if mode == "human" and not self.done:
            
            old_stdout = sys.stdout
            new_stdout = StringIO()
            sys.stdout = new_stdout

            self.env.render()

            output = new_stdout.getvalue()
            logger.debug(output)
            sys.stdout = old_stdout

        if self.done:
            logger.debug(f'\n\nGAME OVER')
            
    def rules_move(self):
        raise Exception('Rules based agent is not yet implemented for Nethack!')
