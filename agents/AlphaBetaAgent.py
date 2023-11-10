import time
import random

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
                next_board.player = next_board.get_opponent()
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
                print("Searched depth", depth)
                if best_move is None:
                    return random.choice(board.valid_moves())
                return best_move
            best_move = move
            depth += 1
        print("Searched depth", depth)

        if best_move is None:
            return random.choice(board.valid_moves())

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
