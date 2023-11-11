# The Undergraduate Undergraduates: Gary Peng (118730745), Anurag Gowda (119005323), Karthikeya Kona (117933048)
import time
import random
import numpy as np

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


class AlphaBetaAgent:
    def __init__(self):
        self.milliseconds = 0
        self.time_up = False
        self.start_time = 0
        return

    def search(self, board, alpha, beta, depth):
        if (time.time() - self.start_time) * 1000 >= self.milliseconds:
            self.time_up = True
            return None, None

        if (winner := board.get_winner()) != -1:
            if winner == board.player:
                return float('inf'), None
            elif winner == 0:
                return 0, None
            else:
                return -float('inf'), None

        if depth == 0:
            return self.evaluate(board), None

        best_move = None
        for move in board.valid_moves():
            next_board = board.make_move(move)
            if next_board.player == board.player:
                evaluation, _ = self.search(next_board, alpha, beta, depth - 1)
            else:
                evaluation, _ = self.search(next_board, -beta, -alpha, depth - 1)
            if self.time_up:
                return None, None
            evaluation *= -1
            if evaluation >= beta:
                return evaluation, None
            if evaluation > alpha:
                alpha = evaluation
                best_move = move

        return alpha, best_move

    def best_move(self, board, milliseconds=2800):
        self.milliseconds = milliseconds
        self.time_up = False
        self.start_time = time.time()

        _, best_move = None, None
        depth = 1
        while (time.time() - self.start_time) * 1000 < self.milliseconds:
            _, move = self.search(board, -float('inf'), float('inf'), depth)
            if self.time_up:
                if best_move is None:
                    return random.choice(board.valid_moves())
                return best_move
            best_move = move
            depth += 1

        if best_move is None:
            return random.choice(board.valid_moves())
        return best_move

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

offsets = [3, 2, 1, 0, 0, 1, 2, 3]
directions = [[-1, 0], [-1, 1], [0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1]]


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
        child_board = self.copy_board()
        child_board.make_move_in_place(move)
        return child_board
    def make_move_in_place(self, move):
        i, j = move

        assert self.is_valid_move(move)
        self.board[i][j] = self.player
        for (dx, dy) in directions:
            k = 1
            while self.is_in_bounds(i + k * dx, j + k * dy) and self.board[i + k * dx][
                j + k * dy] == self.get_opponent():
                k += 1
            if self.is_in_bounds(i + k * dx, j + k * dy) and k > 1 and self.board[i + k * dx][
                j + k * dy] == self.player:
                for l in range(1, k):
                    self.board[i + l * dx][j + l * dy] = self.player

        self.next_turn()
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
        if self.valid_moves():
            return
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



if __name__ == "__main__":
    main_board = Board()
    main_board.read_board()
    agent = AlphaBetaAgent()
    main_move = agent.best_move(main_board)
    print(main_move[0] + 1, main_move[1] - offsets[main_move[0]] + 1)