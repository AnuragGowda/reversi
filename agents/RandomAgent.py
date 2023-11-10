import random


class RandomAgent:
    def best_move(self, board):
        return random.choice(board.valid_moves())
