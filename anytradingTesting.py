import gym
import gym_anytrading

from stable_baselines3.common.vec_env import DummyVecEnv
from stable_baselines3 import A2C

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from old_shit.dataGetter import getDf


df = getDf("NVDA", "2023-05-1", "2023-06-1", "5min")

print(df.shape)
