# board = Board()
# print("reading")
# board.read_board()
import time

from main import RandomAgent, Agent

agentA = Agent()
agentB = RandomAgent()


def run_game(board, match_board, sleep_ui):
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
        # board_list.append(board)
        print(board.print())

        print()
        remaining_time_ms = max(1, 500 - duration)

        print("remaining", remaining_time_ms)
        match_board(board)
        sleep_ui(remaining_time_ms)

