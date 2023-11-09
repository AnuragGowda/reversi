
class OldAgent:
    DEPTH = 2

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
            evaluation *= -1
            if evaluation > value:
                value = evaluation
                best_move = move

        return evaluation, best_move

    def best_move(self, board):
        evaluation, move = self.search(board)
        return move

    def evaluate(self, boardObj):
        board = boardObj.board
        player_count, opponent_count = 0, 0
        for i in range(8):
            for j in range(14):
                if board[i][j] == boardObj.player:
                    player_count += 1
                elif board[i][j] == boardObj.get_opponent():
                    opponent_count += 1
        return player_count - opponent_count



