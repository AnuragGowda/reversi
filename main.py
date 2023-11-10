# The Undergraduate Undergraduates: Gary Peng (118730745), Anurag Gowda (119005323), Karth

import random
import time

from temp.board import Board
offsets = [3, 2, 1, 0, 0, 1, 2, 3]

directions = [[-1, 0], [-1, 1], [0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1]]
weight = [
        [0, 0, 0, 100, 100, 100, 100, 100, 100, 100, 100, 0, 0, 0],
        [0, 0, 100, -50, -50, -50, -50, -50, -50, -50, -50, 100, 0, 0],
        [0, 100, -50, 25, 25, 25, 25, 25, 25, 25, 25, -50, 100, 0],
        [100, -50, 25, -12, 6, 6, 6, 6, 6, 6, -12, 25, -50, 100],
        [100, -50, 25, -12, 6, 6, 6, 6, 6, 6, -12, 25, -50, 100],
        [0, 100, -50, 25, 25, 25, 25, 25, 25, 25, 25, -50, 100, 0],
        [0, 0, 100, -50, -50, -50, -50, -50, -50, -50, -50, 100, 0, 0],
        [0, 0, 0, 100, 100, 100, 100, 100, 100, 100, 100, 0, 0, 0]
    ]


class Agent:
    DEPTH = 3

    def __init__(self):
        return

    def search(self, board, depth=DEPTH):
        # Terminal
        if (winner := board.get_winner()) != -1:
            if winner == board.player:
                return float('inf'), None
            elif winner == 0:
                return 0, None
            else:
                return -float('inf'), None

        if depth == 0:
            return self.evaluate(board), None

        value = -float('inf')
        best_move, evaluation = None, None

        for move in board.valid_moves():
            next_board = board.make_move(move)
            evaluation, _ = self.search(next_board, depth - 1)
            if next_board.player != board.player:
                evaluation *= -1
            if evaluation >= value:
                value = evaluation
                best_move = move

        return evaluation, best_move

    def best_move(self, board, time_limit=3):
        '''
        self.start_time = time.time()
        evaluation, move = None, None
        depth = 1
        while time.time() - self.start_time < time_limit:
            evaluation, move = self.search(board, depth)
            depth += 1

        return move
        '''
        _, move = self.search(board)
        return move

    def evaluate(self, boardObj):
        board = boardObj.board
        player_count, opponent_count = 0, 0
        for i in range(8):
            for j in range(14):
                if board[i][j] == boardObj.player:
                    player_count += 1 * weight[i][j]
                elif board[i][j] == boardObj.get_opponent():
                    opponent_count += 1 * weight[i][j]
        return player_count - opponent_count


if __name__ == "__main__":
    board = Board()
    board.read_board()
    agent = Agent()
    _, (best_i, best_j) = agent.search(board)
    print(best_i + 1, best_j[1] - offsets[best_i[0]] + 1)