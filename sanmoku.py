import numpy as np
# 三目並べクラス
#
# Player:
# 1: o
# 2: x
#
# __init__: 初期化関数
#
# メンバ変数
# state: 9次元配列。それぞれの要素の値がo or x を表す
#   0: 空きマス
#   1: o
#   2: x
#
# 0 | 1 | 2
#---+---+---
# 3 | 4 | 5
#---+---+---
# 6 | 7 | 8
#
# action:

class Sanmoku:
    PLAYER_MARU = "○"
    PLAYER_BATSU = "×"
    WIN_LINES = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]

    def __init__(self):
        self.state = np.array([0.0]*9)
        # 先行
        self.player = 1 # ○

    def start(self):
        print("#"+"-"*11)
        print("# START")
        print("#"+"-"*11)

        while True:
            if self.player == 1:
                status = self.manual()
            else:
                status = self.chance_getter_man()

            if status == 0:
                continue
            elif status == 1:
                self.view()
                print("Draw...")
                break
            elif status == 2:
                self.view()
                print("You win!")
                break

    # 位置とプレイヤーを指定して配置
    # pos: [0-8]
    # player: 1:○ 2:×
    #
    # Return:
    # -1: Error
    # 0: Continue
    # 1: Draw
    # 2: Player Win

    def action(self, pos, player):
        if not self.valid_action(pos):
            return -1

        # oxを配置
        self.state[pos] = player
        # 盤面の状態を確認
        status = self.get_status()
        # Continue(0)ならばプレイヤー変更
        if status == 0:
            self.change_player()

        return status

    # 盤面の状態を確認
    # Return
    # 0: Continue
    # 1: Draw
    # 2: Player Win
    def get_status(self):
        if (all((x == self.player for x in self.pickup(0,1,2))) or
            all((x == self.player for x in self.pickup(3,4,5))) or
            all((x == self.player for x in self.pickup(6,7,8))) or
            all((x == self.player for x in self.pickup(0,3,6))) or
            all((x == self.player for x in self.pickup(1,4,7))) or
            all((x == self.player for x in self.pickup(2,5,8))) or
            all((x == self.player for x in self.pickup(0,4,8))) or
            all((x == self.player for x in self.pickup(2,4,6)))):
            return 2
        elif len([i for i,x in enumerate(self.state) if x==0.0]) == 0:
            return 1

        return 0

    def view(self):
        row = " {} | {} | {} "
        hr = "\n---+---+---\n"
        tempboard = []
        for i in self.state:
            if i == 1.0:
                tempboard.append(self.PLAYER_MARU)
            elif i == 2.0:
                tempboard.append(self.PLAYER_BATSU)
            else:
                tempboard.append(" ")
        print((row + hr + row + hr + row).format(*tempboard))

    def valid_action(self, pos):
        try:
            if int(pos) not in range(0,9):
                print("The position isn't not in [0-8].")
                return False
        except ValueError:
            print("The position isn't not in [0-8].")
            return False

        if self.state[int(pos)] != 0.0:
            #print("Already set player at pos: %d"%pos)
            return False

        return True

    def change_player(self):
        self.player = 2 if self.player == 1 else 1

    def pickup(self, *nums):
        return np.array([self.state[i] for i in nums])

    def reset(self):
        self.state = np.array([0.0]*9)
        # 先行
        self.player = 1 # ○

    # ランダムに1手配置
    def random(self):
        # まだoもxも書いていない箇所からランダムに選択
        candidates = [i for i,x in enumerate(self.state) if x==0.0]
        pos = np.random.choice(candidates)
        return self.action(pos, self.player)

    # 配置場所指定
    def manual(self):
        self.view()

        while True:
            print("You are %s" % (self.PLAYER_MARU if self.player == 1 else self.PLAYER_BATSU))
            print("Enter your pos[0-8]:")
            pos = input()
            if self.valid_action(pos):
                break

        # 入力した位置に配置
        status = self.action(int(pos), self.player)

        return status

    # 真ん中が空いていれば必ず真ん中に置き
    # あと1手で勝てる場合は必ず勝てる手を置き
    # そうでなければランダムに置く人
    def chance_getter_man(self):
        # 真ん中(4)が空いていれば必ず真ん中に置く
        if self.state[4] == 0:
            return self.action(4, self.player)

        # あと1手で勝てる場合は勝てる手を置く
        for idxs in self.WIN_LINES:
            line = self.pickup(*idxs)
            # すでに誰かが置いた位置
            players_pos = line[line != 0.0]
            # あと1手で勝てる場合
            if len(players_pos) == 2 and all(players_pos == self.player):
                pos = np.where(line == 0.0)[0][0]
                return self.action(idxs[pos], self.player)

        # なければランダム
        return self.random()


if __name__ == "__main__":
    game = Sanmoku()
    game.start()
