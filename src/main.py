from chess import pgn, Move
import os, sys
import time

from ids import IDS
from bfs import BFS

class Main:
    def __init__(self):
        self.board = None
        self.game = None
        self.algo = None
        
    def welcome(self) -> None:
        print("""
=========--------------------------------------------=###%#########----------------=======
=========------------------------------------------=%%%%%%#%%#%#%%%%=----------------=====
=========-=----------------------------------------%%%%#%%@@%@@%@%@@%*---------------=====
========------------------------------------------#%%%#*++++*%@@@@@@@%=----------------===
========-----------------------------------------=%@%*======++*####*@@+----------------===
========------------------------------------------###+=======++***##%@*----------------===
========-----------------------------------------=*#*==+##%#++++*###%@+----------------===
========----------------------------------------===*==+#%%%%###%%%%@#*-----------------===
========-----------------------------------------==+=====+*===#%##@%#%-----------------===
========------------------------------------------=*+=====+===##*+*##*-----------------===
========-----------------------------+%%%%%%%%*-*@%#++==+*=#%%@%*+*##-=----------------===
=========---------------------------*%%%%%%%%%@@@@@***+=+*###*%%##%%+------------------===
=========----------------------==*%%%%%%%%%%@@@@@@++****#*+=++#@%%%%@#---------------=====
=========----------------=*=*%%%#*%%%%%%%%@@@@@@@%-=+###*++*#%%%%@@@@@%=--=--=------======
===========----------=#%%%%%@%%%%%#%%%%@%@@@@@@%%*:+=*%%%#*#%%%@@@@@@@@%%=================
=============+*%%%%%%%%%%%%%@%*-==---*%@@@@@@@%%%+*++=+#%@@@@@@@@@@@@@@@%%%*==============
==========#%%%%%%%%%%%%%%%@@+====--===+@@@@@%%%%%#*-=+=++*#%@@@@@@@@@%%%%%%%%%*===========
========*%%%%%%%%%%#:.::::----=##*+==-=%@@%*+=+%%%=-=*+=++***%@@@@@@%%%%%%@@@@@#==========
=======*%%%%%%%%%*::.::::.-===-==#%%##@%###%%%%%%*-::**++=*##@@@@@@@%%%%@@@@@@@#==========
=======#@@%%%%%%*:::::::-+==--*+=--*#%%%##%%%%%%%#-:::::=*%@@@@@@@@%%%@@@@@@@@@+==========
========%@@%%%@%-::::::-==***++=+*+++#%%%%%%%%%@%*-=#*#**%@@@@@@%@%%@@@#*#%@@@#=========++
===========%@@@*-------#*+***###++**#%@@@@@@@@@@*++*++*=+%@@@%%%%%@@@@%%%%@@@%=========+++
===============#@@*---+=*++=====*%%%@@@@@@@%+#@#*=*%-+==#%*#%%%%%@@%%%%%@@@@@%+=++++++++++
============+*###=====+#@=-=--+%@%@#%%@@@@@*+*%%=*#%#+==%*%@@%%@@@%%%%%@@@@##%#+++++++++++
=============%@%+*====*%@++===+*#%%+*##@@@@#+#%*-=#%=+-*%+*%%%%#=*#+#%%@@@##%@%+++++++++++
=============*#%%#====*#%%*====*%%##**#@@%*#*#+--=+%+-=%%*#@@%#*=+%%%*==*@%##%%+++++++++**
============++*##+===*#%%%====*#%%%#*++@@@##**++=*#%@*+@#+*%%%==+*%#%%-=*@%++#%*++********
===========+++####+==*-+%#*+=+**%%%**+##@*=#*##***#%%%*@#*+#%%++=++*%+--+%+++###**********
++++++*++++**######**###********#####*###**####*#######***####***#####++*#*####%#********#
------------------------------------------WELCOME-----------------------------------------
              """)
    
    def getFilePath(self):
        while True:
            file = input("Insert .pgn file: ")
            if (file == "quit"):
                sys.exit()
            file_path = os.path.join("test", file)
            try:
                with open(file_path) as f:
                    game = pgn.read_game(f)
                game = game.end()
                board = game.board()
                self.game = game
                self.board = board
                return
            except FileNotFoundError:
                raise FileNotFoundError()
    
    def getAlgo(self):
        while True:
            print("""\nAlgorithms to choose:
1. Iterative Deepening Search
2. Breadth First Search\n""")
            algo = input("Select an algorithm (1 or 2): ")
            if (algo == "1"):
                self.algo = IDS(self.board)
                return
            elif (algo == "2"):
                self.algo = BFS(self.board)
                return
            elif (algo == "quit"):
                sys.exit()
            else:
                print("Invalid input!")
    
    def printResult(self):
        print(f"Found the solution in {self.algo.result.time} ms.")
        print(f"It was mate in {self.algo.result.depth}!")
        print("The moves:")
        for move in self.algo.result.moves:
            print(Move.uci(move))
    
    def main(self) -> None:
        self.welcome()
        while True:
            try:
                self.getFilePath()
                print(self.board)
                self.getAlgo()
                self.algo.findSolution()
                self.printResult()
                self.algo.evaluator.close()
                return
            except FileNotFoundError:
                print("No file")

if __name__ == "__main__":
    m = Main()
    m.main()