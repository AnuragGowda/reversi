#include <iostream>
#include <utility>
#include <vector>
#include <cassert>

std::vector<int> offsets = {3, 2, 1, 0, 0, 1, 2, 3};
std::vector<std::vector<int>> directions = {
        {-1, 0},
        {-1, 1},
        {0,  1},
        {1,  1},
        {1,  0},
        {1,  -1},
        {0,  -1},
        {-1, -1}
};

template<class T>
inline void hash_combine(std::size_t & s,
const T &v
) {
std::hash<T> h;
s ^=
h(v)
+ 0x9e3779b9 + (s << 6) + (s >> 2);
}
using cell = std::pair<int, int>;

std::vector<std::vector<int>> blank_board() {
    return {8, std::vector<int>(14, 0)};
}

class Board_cpp {
public:
    int player = 1;
    int winner = -1;
    std::vector<std::vector<int>> board = blank_board();

    Board_cpp() {

    }

    Board_cpp(std::vector<std::vector<int>> initial_board) : board(initial_board) {}

    Board_cpp(std::vector<std::vector<int>> initial_board, int player, int winner) {
        board = initial_board;
        this->player = player;
        this->winner = winner;
    }

    void read_board() {
        for (int index = 0; index < 8; index++) {
            for (int i = offsets[index]; i < 14 - offsets[index]; i++) {
                std::cin >> board[index][i - offsets[index]];
            }
        }
    }

    bool is_in_bounds(int i, int j) {
        return 0 <= i && i < 8 && 0 <= j && j < 14 && offsets[i] <= j && j < 14 - offsets[i];
    }

    void output() {
        for (int index = 0; index < 8; index++) {
            for (int offset = 0; offset < 2 * offsets[index]; offset++) {
                std::cout << ' ';
            }
            for (int i = offsets[index]; i < 14 - offsets[index]; i++) {
                std::cout << board[index][i] << ' ';
            }
            std::cout << std::endl;
        }
    }

    std::vector<cell> valid_moves() {
        std::vector<cell> moves;
        for (int i = 0; i < 8; i++) {
            for (int j = 0; j < 14; j++) {
                if (is_in_bounds(i, j) && board[i][j] == player) {
                    std::vector<cell> cell_moves = get_moves_for_cell(i, j);
                    moves.insert(moves.end(), cell_moves.begin(), cell_moves.end());
                }
            }
        }
        return moves;
    }

    std::vector<cell> get_moves_for_cell(int i, int j) {
        std::vector<cell> moves;
        for (auto &direction: directions) {
            int dx = direction[0];
            int dy = direction[1];
            int k = 1;
            while (is_in_bounds(i + k * dx, j + k * dy) && board[i + k * dx][j + k * dy] == get_opponent()) {
                k++;
            }
            if (is_in_bounds(i + k * dx, j + k * dy) && k > 1 && board[i + k * dx][j + k * dy] != player) {
                moves.emplace_back(i + k * dx, j + k * dy);
            }
        }
        return moves;
    }

    int get_player() const {
        return player;
    }

    int get_opponent() const {
        if (player == 1) {
            return 2;
        }
        if (player == 2) {
            return 1;
        }
        assert(false);
        return -1;
    }

    bool is_valid_move(int i, int j) {
        std::pair<int, int> move= {i, j};
//        return std::any_of(valid_moves().begin(), valid_moves().end(), [&](cell valid_move) {
//            return valid_move == move;
//        });

        for (std::pair<int, int>& valid_move: valid_moves()) {
            if (valid_move == move) {
                return true;
            }
        }
        return false;

        if (valid_moves().size() >= 0) {
            return true;
        }
        return false;
    }

    Board_cpp copy_board() const {
        return Board_cpp(board, player, winner);
    }

    void make_move_in_place(int i, int j) {
//        auto [i, j] = move;

        assert(is_valid_move(i, j));
        board[i][j] = player;

        for (auto &direction: directions) {
            int dx = direction[0];
            int dy = direction[1];
            int k = 1;
            while (is_in_bounds(i + k * dx, j + k * dy) && board[i + k * dx][j + k * dy] == get_opponent()) {
                k++;
            }
            if (is_in_bounds(i + k * dx, j + k * dy) && k > 1 && board[i + k * dx][j + k * dy] == player) {
                for (int l = 1; l < k; l++) {
                    board[i + l * dx][j + l * dy] = player;
                }
            }
        }

        next_turn();
    }

    Board_cpp make_move(int i, int j) {
        Board_cpp child_board = copy_board();
        child_board.make_move_in_place(i, j);
        return child_board;
    }

    std::pair<int, int> count_score() {
        int player_1_count = 0;
        int player_2_count = 0;
        for (int i = 0; i < 8; i++) {
            for (int j = 0; j < 14; j++) {
                if (board[i][j] == 1) {
                    player_1_count++;
                } else if (board[i][j] == 2) {
                    player_2_count++;
                }
            }
        }
        return {player_1_count, player_2_count};
    }

    void next_turn() {
        player = get_opponent();
        if (valid_moves().empty()) {
            player = get_opponent();
        }
        if (valid_moves().empty()) {
            auto [player_1_count, player_2_count] = count_score();
            if (player_1_count > player_2_count) {
                winner = 1;
            } else if (player_1_count == player_2_count) {
                winner = 0;
            } else {
                winner = 2;
            }
        }
    }


    int get_winner() const {
        return winner;
    }

    bool game_over() const {
        return winner != -1;
    }

    std::vector<int> &operator[](int index) {
        return board[index];
    }

    size_t hash() {
        size_t hash = 0;
        for (int i = 0; i < 8; i++) {
            for (int j = offsets[i]; j < 14 - offsets[i]; j++) {
                hash_combine(hash, board[i][j]);
            }
        }
        hash_combine(hash, player);
        hash_combine(hash, winner);
        return hash;

    }

    bool operator==(const Board_cpp &node2) const {
        if (board != node2.board) {
            return false;
        }
        if (player != node2.player) {
            return false;
        }
        if (winner != node2.winner) {
            return false;
        }
        return true;
    }

    int get_cell(int i, int j) {
        return board[i][j];
    }
};


