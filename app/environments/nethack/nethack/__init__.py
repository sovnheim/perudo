from gym.envs.registration import register
import aicrowd_gym

register(
    id='NetHackAI-v0',
    entry_point='nethack.envs:NetHackEnv',
)