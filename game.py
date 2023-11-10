import time
from collections import defaultdict

from agents import RandomAgent, AlphaBetaAgent
from board import Board
from gui import b, match_board, mark_best


class Game:
    def __init__(self, agentA, agentB, board):
        self.agentA = agentA
        self.agentB = agentB
        self.board = board

    def best_move(self):
        agent = agentA if self.board.player == 1 else agentB
        move = agent.best_move(self.board)
        assert move is not None
        return move

    def run_game(self):
        move_count = 0
        while not self.board.game_over:
            next_move = self.best_move()
            self.board.make_move_in_place(next_move)
            move_count += 1
            # print(move_count)

        print("Game over", self.board.get_winner(), "won", self.board.count_score())
        return self.board.get_winner()

    def run_game_ui(self, gap=2000):
        def on_start():
            match_board(self.board)
            b.pause(gap)
            while not self.board.game_over:
                start_time_ms = time.time_ns() // 1000000
                move = self.best_move()
                duration = time.time_ns() // 1000000 - start_time_ms
                print("duration", duration)
                assert move is not None
                # print("Player", self.board.player, "makes move", move)
                mark_best(move)
                b.pause(500)
                self.board.make_move_in_place(move)

                remaining_time_ms = max(1, gap - duration)

                print("remaining", remaining_time_ms)
                match_board(self.board)
                b.pause(remaining_time_ms)

        b.on_start = on_start
        b.show()


if __name__ == "__main__":
    original_board = Board()
    original_board.read_board()
    # agentA = RandomAgent.RandomAgent()
    agentA = AlphaBetaAgent.AlphaBetaAgent()
    agentB = RandomAgent.RandomAgent()
    wins = {1: 0, 0:0, 2: 0}
    while True:
        current_board = original_board.copy_board()
        current_game = Game(agentA, agentB, current_board)
        winner = current_game.run_game()
        wins[winner] += 1
        print(wins)
    # game = Game(agentA, agentB, original_board)

    # game.run_game_ui()
    # game.run_game()
