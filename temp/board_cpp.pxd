from libcpp cimport bool
from libcpp.pair cimport pair
from libcpp.vector cimport vector
cdef extern from "board_cpp.cpp":
    pass

# Declare the class with cdef
cdef extern from "board_cpp.h":
    cdef cppclass Board_cpp:
        Board_cpp() except +
        Board_cpp(vector[vector[int]], int, int) except +
        void read_board()

        vector[pair[int, int]] valid_moves()
        bool is_valid_move(int, int)
        pair[int, int] count_score()

        void make_move_in_place(int, int)

        int get_player()
        void output()

        bool is_in_bounds(int, int)

        int get_cell(int, int)

        bool game_over()

        int get_winner()

        Board_cpp copy_board()
