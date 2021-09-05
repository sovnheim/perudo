# guess the number: Guess a number between 1 and 10. The first agent to guess the others number wins

import numpy as np
import gym


class NumberGuesserEnv(gym.Env):
    def __init__(self):
        super(NumberGuesserEnv, self).__init__()
        self.name = 'NumberGuesser'

        self.n_players = 2
        self.current_player_num = 0
        self.pool_size = 10

        self.player_guesses = []

        self.action_space = gym.spaces.Discrete(self.pool_size)
        self.observation_space = gym.spaces.Discrete(2)

        # Calling self.reset for first instance of the environment
        self.reset()

    def reset(self):
        print("Game Reset")
        self.current_player_num = 0
        self.player_guesses = [np.random.randint(self.pool_size)
                               for player_num in range(self.n_players)]

    def step(self, action):

        # On met à jour les variables de l'environnement avec l'action

        # On regarde si l'action provoque une victoire
        # Si victoire on marque Done
