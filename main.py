# The Undergraduate Undergraduates: Gary Peng (118730745), Anurag Gowda (119005323), Karth

import numpy as np
import random
import time

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

class Board:
    def __init__(self, board=np.zeros((8, 14), dtype=np.int16), player=1, game_over=False, winner=-1):
        self.player = player
        self.game_over = game_over
        self.winner = winner
        self.board = board.copy()

    def read_board(self):

        for index, offset in enumerate(offsets):
            line = input()
            line = line.split()
            for i in range(offset, 14 - offset):
                self.board[index][i] = int(line[i - offset])

    # def(self):
    # 	pass
    def is_in_bounds(self, i, j):
        return 0 <= i < 8 and 0 <= j < 14 and offsets[i] <= j < 14 - offsets[i]

    def cells(self):
        for i in range(8):
            for j in range(14):
                yield i, j

    def print(self):
        for index, offset in enumerate(offsets):
            print(' ' * (2 * offset), end="")
            for i in range(offset, 14 - offset):
                print(self.board[index][i], end=" ")
            print()

    def valid_moves(self):
        moves = []
        for (i, j) in self.cells():
            if self.is_in_bounds(i, j) and self.board[i][j] == self.player:
                moves.extend(self.get_moves_for_cell(i, j))
        return moves

    def get_moves_for_cell(self, i, j):
        moves = []
        for (dx, dy) in directions:
            k = 1
            while self.is_in_bounds(i + k * dx, j + k * dy) and self.board[i + k * dx][
                j + k * dy] == self.get_opponent():
                k += 1
            if self.is_in_bounds(i + k * dx, j + k * dy) and k > 1 and self.board[i + k * dx][
                j + k * dy] != self.player:
                moves.append((i + k * dx, j + k * dy))
        return moves

    def get_opponent(self):
        if self.player == 1:
            return 2
        if self.player == 2:
            return 1

    def is_valid_move(self, move):
        x, y = move
        return (x, y) in self.valid_moves()

    def copy_board(self):
        return Board(self.board, self.player, self.game_over, self.winner)

    def make_move(self, move):
        i, j = move
        child_board = self.copy_board()

        assert child_board.is_valid_move(move)
        child_board.board[i][j] = child_board.player
        for (dx, dy) in directions:
            k = 1
            while child_board.is_in_bounds(i + k * dx, j + k * dy) and child_board.board[i + k * dx][
                j + k * dy] == child_board.get_opponent():
                k += 1
            if child_board.is_in_bounds(i + k * dx, j + k * dy) and k > 1 and child_board.board[i + k * dx][
                j + k * dy] == child_board.player:
                for l in range(1, k):
                    child_board.board[i + l * dx][j + l * dy] = child_board.player

        child_board.next_turn()
        return child_board

    def count_score(self):
        player_1_count, player_2_count = 0, 0
        for (i, j) in self.cells():
            if self.board[i][j] == 1:
                player_1_count += 1
            elif self.board[i][j] == 2:
                player_2_count += 1
        return player_1_count, player_2_count

    def next_turn(self):
        self.player = self.get_opponent()
        if not self.valid_moves():
            self.player = self.get_opponent()
        if not self.valid_moves():
            self.game_over = True
            (player_1_count, player_2_count) = self.count_score()
            if player_1_count > player_2_count:
                self.winner = 1
            elif player_1_count == player_2_count:
                self.winner = 0
            else:
                self.winner = 2

    def get_winner(self):
        return self.winner


class RandomAgent:
  def best_move(self, board):
      return random.choice(board.valid_moves())



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
    _, move = agent.search(board)
    print(move[0] + 1, move[1] - offsets[move[0]] + 1)