from chess import Board, Move, engine
from algo import Algo, Result, sort_moves_by_valuation
import time

class IDS(Algo):
    def __init__(self, board : Board):
        super().__init__(board)
        self.result = Result()
        self.evaluator = engine.SimpleEngine.popen_uci(r"E:/stockfish/stockfish-windows-x86-64-avx2.exe")

    def getName(self):
        return "IDS"

    def findSolution(self):
        depth = 1
        moves = []
        player = self.board.turn

        start_time = time.time()
        while True:
            mate_moves = self.DLS(self.board, player, moves, depth)
            if mate_moves != None:
                end_time = time.time()
                self.result.depth = int((depth+1)/2)
                self.result.moves = mate_moves
                self.result.time = (end_time-start_time)*1000
                self.evaluator.close()
                return
            depth += 2
    
    def DLS(self, board : Board, player, moves : list[Move], depth):
        if (board.is_checkmate()):
            return moves
        
        if depth <= 0 or board.is_stalemate():
            return None
        
        child_moves = list(board.legal_moves)
        if (player != board.turn):
            child_move = sort_moves_by_valuation(board, child_moves, self.evaluator)[0]
            moves.append(child_move)
            board.push(child_move)
            next = self.DLS(board, player, moves, depth-1)
            if next != None:
                return next
            moves.remove(child_move)
            board.pop()
        else :
            for move in child_moves:
                moves.append(move)
                board.push(move)
                next = self.DLS(board, player, moves, depth-1)
                if next != None:
                    return next
                moves.remove(move)
                board.pop()
        
        return None
    


if __name__ == "__main__":
    pass