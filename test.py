from cython_output.board import Board
board = Board()

board.read_board()
board.output()
moves = board.valid_moves()
print(moves)
print(board.count_score())

board.make_move_in_place(moves[0])


print(board.count_score())