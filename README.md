## Description
keras-rlで三目並べを強化学習する

## Requirement
- tensorflow (1.2.0)
- Keras (2.0.5)
- keras-rl (0.3.0)
- gym (0.9.2)
- h5py (2.7.0)

### pip command
`pip install tensorflow keras keras-rl gym h5py`

## Usage
### 学習する
`python dqn.py`
### 重みファイルを読み込んで対戦する
`python dqn.py -l WEIGHT_FILE`
### サンプル重みファイル
- dqn_Sanmoku_weights_strong.h5f : 強いやつ
- dqn_Sanmoku_weights_weak.h5f : よわいやつ

## Installation
`git clone https://github.com/nice-okura/keras-sanmoku.git`
