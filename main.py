# The Undergraduate Undergraduates: Gary Peng (118730745), Anurag Gowda (119005323), Karth


from agents.AlphaBetaAgent import AlphaBetaAgent
from board import Board

offsets = [3, 2, 1, 0, 0, 1, 2, 3]



if __name__ == "__main__":
    board = Board()
    board.read_board()
    agent = AlphaBetaAgent()
    _, move = agent.best_move(board)
    print(move[0] + 1, move[1] - offsets[move[0]] + 1)