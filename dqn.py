import argparse

# 引数
parser = argparse.ArgumentParser(description='Sanmoku DQN')
parser.add_argument('-l', dest="weight_file", help='load weight file and play Sanmoku')
args = parser.parse_args()

from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten
from keras.optimizers import Adam

from rl.agents.dqn import DQNAgent
from rl.policy import EpsGreedyQPolicy
from rl.memory import SequentialMemory

import rl.callbacks
from sanmokuDQN import SanmokuDQN

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
model = Sequential()
model.add(Flatten(input_shape=(1,) + env.observation_space.shape))
model.add(Dense(166))
model.add(Activation('relu'))
model.add(Dense(nb_actions))
model.add(Activation('linear'))
print(model.summary())

memory = SequentialMemory(limit=1000, window_length=1)
policy = EpsGreedyQPolicy(eps=0.1)
dqn = DQNAgent(model=model, nb_actions=nb_actions, memory=memory, nb_steps_warmup=100,
                            target_model_update=1e-2, policy=policy)
dqn.compile(Adam(lr=1e-3), metrics=['mae'])

if args.weight_file:
    # 重みファイルを読み込んでtest
    dqn.load_weights(args.weight_file)
else:
    # 学習
    history = dqn.fit(env, nb_steps=10000, visualize=False, verbose=2, nb_max_episode_steps=300)
    dqn.save_weights('dqn_{}_weights.h5f'.format("Sanmoku"), overwrite=True)

# Finally, evaluate our algorithm for 5 episodes.
dqn.test(env, nb_episodes=5, visualize=False, nb_max_episode_steps=300)
