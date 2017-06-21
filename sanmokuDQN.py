import os
import gym
import gym.spaces
import numpy as np
import logging, logging.handlers
from sanmoku import Sanmoku as sm

# ログ設定
LOG_LEVEL = logging.DEBUG
logger = logging.getLogger(__name__)
formatter = logging.Formatter(
    fmt="%(asctime)s:[%(name)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
file_handler = logging.handlers.RotatingFileHandler(
    os.path.join(os.path.abspath(os.path.dirname(__file__)), "log", "sanmokuDQN.log"),
    maxBytes=50000000, backupCount=5)
file_handler.setFormatter(formatter)
file_handler.setLevel(LOG_LEVEL)
logger.addHandler(file_handler)

# 三目並べをDQNで学習
# action: 3x3の9マスなので9パターン
#
class SanmokuDQN(gym.core.Env):
    PLAYER = 1 # o

    # mode:
    #   random: 相手がランダムに配置
    #   manual: 配置場所を指定(対戦モード)
    def __init__(self, mode="random"):
        logger.debug("_init")

        self.mode = mode

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
        # statusがDraw(1)またはPlayerWin(2)の場合終了
        # エラー(-1)の場合も終了とする
        done = status in {-1, 1, 2}

        if status == -1:
            if self.mode == "manual":
                print("Miss position!!")
            reward = 0.0
        elif status == 1:
            if self.mode == "manual":
                print("Draw...")
            reward = 0.0
        elif status == 2:
            if self.mode == "manual":
                self.print_winner()
            reward = 1.0
        else:
            if self.mode == "random":
                status = self.sm.random()
            elif self.mode == "manual":
                status = self.sm.manual()
                if status == 2:
                    self.print_winner()
                    done = True

            if status == 2:
                reward = -1.0
            else:
                reward = 0.0

        return self.sm.state, reward, done, {}

    def _reset(self):
        logger.debug("_reset")
        self.sm.reset()

        return self.sm.state

    def _render(self, mode='human', close=False):
        pass

    def print_winner(self):
        print("Winner %s!!"%(self.sm.PLAYER_MARU if self.sm.player == 1 else self.sm.PLAYER_BATSU))
