from game2dboard import Board as BoardUI
from main import offsets, Board

b = BoardUI(8, 14)
b.create_output()
current_player = 1
board = Board()
board.read_board()
original_board = board


def match_board():
    for i in range(8):
        for j in range(14):
            if not board.is_in_bounds(i, j):
                b[i][j] = "oob"
            elif board.board[i][j] == 1:
                b[i][j] = "white"
            elif board.board[i][j] == 2:
                b[i][j] = "black"
            elif board.player == 1 and board.is_valid_move(i, j):
                b[i][j] = "white_next"
            elif board.player == 2 and board.is_valid_move(i, j):
                b[i][j] = "black_next"
            else:
                b[i][j] = None
    b.print(board.count_score())
    if board.game_over:
        b.print("Game over", board.winner, "won", board.count_score())


match_board()


def mouse_fn(btn, row, col):
    moves = board.valid_moves()
    print(moves)
    if moves:
        x, y = moves[0]
        board.make_move(x, y)

    # if board.is_valid_move(row, col):
    #     board.make_move(row, col)
    match_board()


b.title = "Reversi"
b.cell_size = 120
b.cell_color = "bisque"
b.on_mouse_click = mouse_fn
b.show()
