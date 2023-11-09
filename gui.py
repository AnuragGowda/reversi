import random
from time import sleep

from game2dboard import Board as BoardUI

from game import run_game
from main import Board, Agent

b = BoardUI(8, 14)
b.create_output()
current_player = 1
board = Board()
original_board = board
global board_list


def set_board(_board):
    global board
    board = _board
    match_board()
    b.show()


board_index = -1


def set_boards(_boards):
    global board, board_list
    board_index = len(_boards) - 1
    board = _boards[board_index]
    match_board()
    b.show()


def sleep_ui(ms):
    b.pause(ms)


def match_board(_board=None):
    global board
    if _board is not None:
        board = _board
    for i in range(8):
        for j in range(14):
            if not board.is_in_bounds(i, j):
                b[i][j] = "oob"
            elif board.board[i][j] == 1:
                b[i][j] = "white"
            elif board.board[i][j] == 2:
                b[i][j] = "black"
            elif board.player == 1 and board.is_valid_move((i, j)):
                b[i][j] = "white_next"
            elif board.player == 2 and board.is_valid_move((i, j)):
                b[i][j] = "black_next"
            else:
                b[i][j] = None
    b.print(board.count_score())
    if board.game_over:
        b.print("Game over", board.winner, "won", board.count_score())

match_board()


def mouse_fn(btn, row, col):
    global board

    move = (row, col)
    if board.is_valid_move(move):
        board = board.make_move(move)
    match_board()


agent = Agent()


def make_move(move):
    global board
    i, j = move
    if b[i][j] == "white_next":
        b[i][j] = "white_pick"
    elif b[i][j] == "black_next":
        b[i][j] = "black_pick"
    else:
        assert False

    b.print("making move", move)
    sleep(0.5)
    board = board.make_move(move)
    match_board()


def timer_fn():
    global board
    if board.game_over:
        return
    if board.player == 1:
        evaluation, best_move = agent.search(board)
        make_move(best_move)
    else:
        move = random.choice(board.valid_moves())
        make_move(move)


def key_fn(key):
    print(key)
    global board, board_index
    if key == "space":
        evaluation, best_move = agent.search(board)

        board = board.make_move(best_move)
        match_board()

    elif key == "p":
        evaluation, best_move = agent.search(board)
        i, j = best_move
        # b[i][j] = ""

        b.print(evaluation, best_move)
    elif key == "r":
        move = random.choice(board.valid_moves())
        board = board.make_move(move)
        match_board()

    elif key == "c":
        run_game(board, match_board, sleep_ui)
    elif key == "left":
        board_index -= 1
        board = board_list[board_index]
        match_board()


b.title = "Reversi"
b.cell_size = 120
b.cell_color = "bisque"
b.on_mouse_click = mouse_fn
# on spacebar press
b.on_key_press = key_fn
b.on_timer = timer_fn

if __name__ == "__main__":
    board.read_board()
    match_board()
    b.show()
