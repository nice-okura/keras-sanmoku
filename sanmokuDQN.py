import os
import gym
import gym.spaces
import numpy as np
import logging, logging.handlers
from sanmoku import Sanmoku as sm

LOG_LEVEL = logging.DEBUG
logger = logging.getLogger(__name__)
formatter = logging.Formatter(
    fmt="%(asctime)s:[%(name)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
# ログ出力
file_handler = logging.handlers.RotatingFileHandler(
    os.path.join(os.path.abspath(os.path.dirname(__file__)), "log", "sanmokuDQN.log"),
    maxBytes=50000000, backupCount=5)
file_handler.setFormatter(formatter)
file_handler.setLevel(LOG_LEVEL)
logger.addHandler(file_handler)
#stream_handler = logging.StreamHandler()
#stream_handler.setLevel(logging.DEBUG)
#logger.addHandler(stream_handler)

# 三目並べをDQNで学習
# action: 3x3の9マスなので9パターン
#
class SanmokuDQN(gym.core.Env):
    PLAYER = 1 # o

    def __init__(self):
        logger.debug("_init")

        self.sm = sm()

        # action: 3x3の9マスなので9パターン
        self.action_space = gym.spaces.Discrete(9)

        # 9マスそれぞれに
        # 0: None
        # 1: O
        # 2: X
        # の3値をとるので、最大値は2
        self.observation_space = gym.spaces.Box(low=np.array([0.0]*9), high=np.array([2.0]*9))

    def _step(self, action):

        status = self.sm.action(action, 1)

        logger.debug("action: %d" % action)
        #self.sm.view()
        #input()
        # statusがDraw(1)またはPlayerWin(2)の場合終了
        # エラー()-1)の場合も終了とする
        done = status in {-1, 1, 2}

        if status == -1:
            reward = 0.0
        elif status == 1:
            reward = 0.0
        elif status == 2:
            reward = 1.0
        else:
            status = self.sm.random()
            reward = 0.0
            if status == 2:
                reward = -1.0

        return self.sm.state, reward, done, {}

    def _reset(self):
        logger.debug("_reset")
        self.sm.reset()

        return self.sm.state

    def _render(self, mode='human', close=False):
        pass
