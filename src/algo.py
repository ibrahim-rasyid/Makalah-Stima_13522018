from chess import Board, Move, engine, pgn
from abc import ABC, abstractmethod
import os

class Algo(ABC):
    def __init__(self, board: Board):
        self.board = board

    @abstractmethod
    def findSolution(self):
        pass

class Result:
    moves = []
    time = 0.0
    depth = 0

def evaluate_move(board : Board, move : Move, evaluator : engine.SimpleEngine):
    board.push(move)
    info = evaluator.analyse(board, engine.Limit(depth=5))
    board.pop()
    return info["score"].pov(not board.turn).score(mate_score=10000)

def sort_moves_by_valuation(board : Board, moves : list[Move], evaluator : engine.SimpleEngine):  
    return sorted(moves, key=lambda move: evaluate_move(board, move, evaluator), reverse=False)

if __name__ == "__main__":
    file = input("Insert .pgn file: ")
    file_path = os.path.join("test", file)
    with open(file_path) as f:
        game = pgn.read_game(f)
        game = game.end()
        board = game.board()
    
    child_moves = list(board.legal_moves)
    print(child_moves)
    evaluator = engine.SimpleEngine.popen_uci(r"E:/stockfish/stockfish-windows-x86-64-avx2.exe")
    child_moves = sort_moves_by_valuation(board, child_moves, evaluator)
    evaluator.quit()
    print(child_moves)