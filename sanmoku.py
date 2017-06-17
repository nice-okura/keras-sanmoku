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

    def __init__(self):
        self.state = np.array([0.0]*9)
        # 先行
        self.player = np.random.randint(2)+1
        # 終了しているか
        self.done = False

    def start(self):
        print("#"+"-"*11)
        print("# START")
        print("#"+"-"*11)
        self.view()

        while True:
            print("You are %s" % (self.PLAYER_MARU if self.player == 1 else self.PLAYER_BATSU))
            print("Enter your pos[0-8]:")
            pos = input()

            # 入力した位置に配置
            if self.action([int(pos), self.player]):

                self.view()

                if self.check_win():
                    break

                self.change_player()

        print("You win!")
        exit(0)

    # 位置とプレイヤーを指定して配置
    # pos: [0-8]
    # player: 1:○ 2:×
    def action(self, pos, player):
        if not self.check_action(pos, player):
            return False

        self.state[pos] = player

        return True

    def check_win(self):

        if (all((x == self.player for x in self.pickup(0,1,2))) or
            all((x == self.player for x in self.pickup(3,4,5))) or
            all((x == self.player for x in self.pickup(6,7,8))) or
            all((x == self.player for x in self.pickup(0,3,6))) or
            all((x == self.player for x in self.pickup(1,4,7))) or
            all((x == self.player for x in self.pickup(2,5,8))) or
            all((x == self.player for x in self.pickup(0,4,8))) or
            all((x == self.player for x in self.pickup(2,4,6)))):
            return True

        return False

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

    def check_action(self, pos, player):
        if self.state[pos] != 0.0:
            print("Already set player at pos: {}", pos)
            return False
        elif pos not in range(0,9):
            print("The position {} isn't not in [0-8].", pos)
            return False

        return True

    def change_player(self):
        self.player = 2 if self.player == 1 else 1

    def pickup(self, *nums):
        return [self.state[i] for i in nums]

if __name__ == "__main__":
    game = Sanmoku()
    game.start()
