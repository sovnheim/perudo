# guess the number: Guess a number between 1 and 10. The first agent to guess the others number wins

import numpy as np
import gym


class NumberGuesserEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, verbose=False, manual=False):
        super(NumberGuesserEnv, self).__init__()
        self.name = 'NumberGuesser'

        self.n_players = 2
        self.current_player_num = 0
        self.pool_size = 10

        self.num_to_be_guessed = None
        self.current_guess = None
        self.guess_history = []

        self.done = False

        self.action_space = gym.spaces.Discrete(self.pool_size)
        self.observation_space = gym.spaces.Discrete(1)

        # Calling self.reset for first instance of the environment
        self.reset()

    def reset(self):
        print("Game Reset")
        self.current_player_num = 0
        self.num_to_be_guessed = np.random.randint(self.pool_size)

    def step(self, action):
        # On evalue l'action et met à jour les variable d'observation en fonction
        reward = [0, 0]
        self.current_guess = action
        if action == self.num_to_be_guessed:
            done = True
            reward[self.current_player_num] = 1
        if action != self.num_to_be_guessed:
            done = False

        self.guess_history.append(action)
        self.done = done

        return self.observation, reward, done, {}

    @property
    def observation(self):
        # 0 si c'est moins, 1 si c'est plus
        if self.current_guess <= self.num_to_be_guessed:
            return np.array([0])
        if self.current_guess > self.num_to_be_guessed:
            return np.array([1])

    @property
    def legal_actions(self):
        la_array = []
        for action in range(self.pool_size):
            if action in self.guess_history:
                la_array.append([action, 0])
            if action not in self.guess_history:
                la_array.append([action, 1])

    @property
    def render(self, mode='human', close=False):
        if self.done:
            print(f'GAME OVER')
        if close:
            return
        else:
            print(
                f"Player {self.current_player_num} guesses {self.current_guess}")
