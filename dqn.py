import argparse

# 引数
parser = argparse.ArgumentParser(description='Sanmoku DQN')
parser.add_argument('-l', dest="weight_file", help='load weight file and play Sanmoku')
parser.add_argument('-d', help='show mean rewards in episode(Require: matplotlib)')
args = parser.parse_args()

from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten
from keras.optimizers import Adam, SGD, RMSprop, Adadelta, Adagrad, Adamax, Nadam, TFOptimizer

from rl.agents.dqn import DQNAgent
from rl.policy import EpsGreedyQPolicy
from rl.memory import SequentialMemory

import rl.callbacks
from sanmokuDQN import SanmokuDQN
import matplotlib.pyplot as plt
import numpy as np
from functools import reduce

# Rewardの平均を表示
def plot_history(history, filename):
    mean_rewards = []
    tmp = np.array([])
    # 精度の履歴をプロット
    for x in history.history['episode_reward']:
        tmp = np.append(tmp, x)
        mean_rewards.append(np.mean(tmp))

    plt.plot(mean_rewards,"o-",label="reward mean({})".format(filename))
    plt.title('Reward')
    plt.xlabel('Episode')
    plt.ylabel('Reward')
    plt.legend(loc="lower right")
    plt.savefig(filename)

# 三目並べ環境作成
if args.weight_file:
    # 対戦時。配置場所を指定。
    env = SanmokuDQN(mode="manual")
else:
    # 学習時。対戦相手はランダムに配置
    env = SanmokuDQN()
env.seed(123)
nb_actions = env.action_space.n

# ネットワークモデル作成
ptns = [[16],[16,16],[16,16,16],[166],[166,166],[166,166,166]]

for ptn in ptns:
    model = Sequential()
    model.add(Flatten(input_shape=(1,) + env.observation_space.shape))

    for nodes in ptn:
        model.add(Dense(nodes))
        model.add(Activation('relu'))

    model.add(Dense(nb_actions))
    model.add(Activation('linear'))
    print(model.summary())

    memory = SequentialMemory(limit=40000, window_length=1)
    policy = EpsGreedyQPolicy(eps=0.1)
    dqn = DQNAgent(model=model, nb_actions=nb_actions, memory=memory, nb_steps_warmup=100,
                                target_model_update=1e-2, policy=policy)
    dqn.compile(Adadelta())

    if args.weight_file:
        # 重みファイルを読み込んでtest
        dqn.load_weights(args.weight_file)
    else:
        # 学習
        history = dqn.fit(env, nb_steps=100000, visualize=False, verbose=1, nb_max_episode_steps=300)
        dqn.save_weights('dqn_{}_weights_{}.h5f'.format("Sanmoku",str(reduce(lambda x,y: str(x)+str(y), ptn))), overwrite=True)
        # modelに学習させた時の変化の様子をplot
        plot_history(history, "Adadelta" + str(reduce(lambda x,y: str(x)+str(y), ptn)))

    # Finally, evaluate our algorithm for 5 episodes.
    dqn.test(env, nb_episodes=10, visualize=False, nb_max_episode_steps=300)
