import random

from game import Game

if __name__ == '__main__':
    game = Game(True, 'ii2', random.randint(0, 1000000), 1)

    print(game.play())
