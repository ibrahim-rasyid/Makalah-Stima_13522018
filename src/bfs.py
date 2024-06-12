from chess import Board, Move, engine, pgn
from algo import Algo, Result, sort_moves_by_valuation
from collections import deque
import os
import time

class BFS(Algo):
    def __init__(self, board: Board):
        super().__init__(board)
        self.result = Result()
        self.evaluator = engine.SimpleEngine.popen_uci(r"E:/stockfish/stockfish-windows-x86-64-avx2.exe")

    def getName(self):
        return "BFS"

    def findSolution(self):
        player = self.board.turn

        start_time = time.time()
        solution, depth = self.runBFS(self.board, player)
        end_time = time.time()
        self.result.moves = solution
        self.result.depth = depth
        self.result.time = (end_time-start_time)*1000
        self.evaluator.close()
        return
    
    def runBFS(self, board : Board, player):
        queue = deque([board])
        while len(queue) != 0:
            new_board = queue.popleft()
            if new_board.is_checkmate():
                return self.makeMoves(board, new_board)

            if new_board.is_stalemate():
                continue
            
            child_moves = list(new_board.legal_moves)
            if (player != new_board.turn):
                child_move = sort_moves_by_valuation(new_board, child_moves, self.evaluator)[0]
                c_board = new_board.copy()
                c_board.push(child_move)
                queue.append(c_board)
            else :
                for move in child_moves:
                    c_board = new_board.copy()
                    c_board.push(move)
                    queue.append(c_board)
    
    def makeMoves(self, start_board : Board, end_board : Board):
        moves = []
        depth = 0
        while start_board != end_board:
            move = end_board.pop()
            moves.insert(0, move)
            depth += 1
        depth = int((depth+1)/2)
        return moves, depth

if __name__ == "__main__":
    file = input("Insert .pgn file: ")
    file_path = os.path.join("test", file)
    with open(file_path) as f:
        game = pgn.read_game(f)
        game = game.end()
        board = game.board()
    
    c_board = board.copy()
    c_board.push(Move.from_uci("f2b2"))
    c_board.push(Move.from_uci("c3b4"))
    b = BFS(board)
    moves = b.makeMoves(board, c_board)
    print(moves)
    b.evaluator.close()