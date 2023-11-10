import numpy as np

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

    def make_move(self, move, in_place=False):
        if not in_place:
            child_board = self.copy_board()
            child_board.make_move(move, in_place=True)
            return child_board

        i, j = move
        assert self.is_valid_move(move)
        self.board[i][j] = self.player
        for (dx, dy) in directions:
            k = 1
            while self.is_in_bounds(i + k * dx, j + k * dy) and self.board[i + k * dx][j + k * dy] == self.get_opponent():
                k += 1
            if self.is_in_bounds(i + k * dx, j + k * dy) and k > 1 and self.board[i + k * dx][j + k * dy] == self.player:
                for l in range(1, k):
                    self.board[i + l * dx][j + l * dy] = self.player

        self.next_turn()

    def make_move_in_place(self, move):
        self.make_move(move, in_place=True)
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
    def __getitem__(self, index):
        return self.board[index]

    def __hash__(self):
        return hash((self.board.tobytes(), self.player, self.game_over, self.winner))

    def __eq__(self, node2):
        if not np.array_equal(self.board, node2.board):
            return False
        if self.player != node2.player:
            return False
        if self.game_over != node2.game_over:
            return False
        if self.winner != node2.winner:
            return False
        return True




