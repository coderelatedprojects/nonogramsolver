from .nonogram import Nonogram
from .file_reader import FileReader
from .solver import Solver
import time
import argparse

EXAMPLE_PATH = 'data/nono3.txt'

class Simulation:
    def __init__(self, args: argparse.ArgumentParser) -> None:
        filepath = args.filepath if args.filepath else EXAMPLE_PATH
        self.nonogram = FileReader.read_nonogram(filepath)
        self.solver = Solver(self) #possibility to switch solvers
        start_time = time.time()
        self.solve()
        print(f'Solution time: {time.time()-start_time:.4f} s')
    
    # in future - pass solver as an argument
    def solve(self):
        self.solver.solve()