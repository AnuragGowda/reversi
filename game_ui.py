import time

from agents import MCTSAgent, RandomAgent
from board import Board
from gui import b, match_board

agentA = RandomAgent.RandomAgent()
agentB = RandomAgent.RandomAgent()


def run_game(board, gap=0):
    b.pause(gap)
    while not board.game_over:
        agent = agentA if board.player == 1 else agentB
        start_time_ms = time.time_ns() // 1000000
        move = agent.best_move(board)
        duration = time.time_ns() // 1000000 - start_time_ms
        print("Time taken:", duration, "ms")
        print("searching")

        if move is None:
            print("No valid moves for", board.player)
            break

        print("Player", board.player, "makes move", move)

        board = board.make_move(move)

        remaining_time_ms = max(1, gap - duration)

        print("remaining", remaining_time_ms)
        match_board(board)
        b.pause(remaining_time_ms)


if __name__ == "__main__":
    board = Board()
    board.read_board()
    match_board(board)
    b.on_start = lambda: run_game(board)
    b.show()
