# distutils: language = c++
# distutils: extra_compile_args = -std=c++20

from board_cpp cimport Board_cpp

# Create a Cython extension type which holds a C++ instance
# as an attribute and create a bunch of forwarding methods
# Python extension type.
cdef class Board:
    cdef Board_cpp c_board  # Hold a C++ instance which we're wrapping

    def __init__(self):
        self.c_board = Board_cpp()

    # def __init__(self, board, player, winner):
    #     self.c_board = Board_cpp(board, player, winner)



    # def get_area(self):
    #     return self.c_rect.getArea()
    #
    #
    # def get_size(self):
    #     cdef int width, height
    #     self.c_rect.getSize(&width, &height)
    #     return width, height
    #
    # def move(self, dx, dy):
    #     self.c_rect.move(dx, dy)
    def get_player(self):
        return self.c_board.get_player()
    def valid_moves(self):
        return self.c_board.valid_moves()
    def read_board(self):
        return self.c_board.read_board()
    def make_move_in_place(self, move):
        self.c_board.make_move_in_place(move[0], move[1])
    def make_move(self, move):
        new_board = self.copy_board()
        new_board.make_move_in_place(move)
        return new_board
    def count_score(self):
        return self.c_board.count_score()

    def output(self):
        self.c_board.output()

    def is_in_bounds(self, move):
        return self.c_board.is_in_bounds(move[0], move[1])

    def get_cell(self, cell):
        return self.c_board.get_cell(cell[0], cell[1])

    def is_valid_move(self, cell):
        return self.c_board.is_valid_move(cell[0], cell[1])

    # def game_over(self):
    #     return self.c_board.game_over()
    def get_winner(self):
        return self.c_board.get_winner()


    @property
    def game_over(self):
        return self.c_board.game_over()

    @property
    def player(self):
        return self.c_board.get_player()

    @property
    def winner(self):
        return self.c_board.get_winner()

    def copy_board(self):
        new_board = Board()
        new_board.c_board = self.c_board.copy_board()
        return new_board
    # @x0.setter
    # def x0(self, x0):
    #     self.c_rect.x0 = x0
