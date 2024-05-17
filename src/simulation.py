from .nonogram import Nonogram
from .file_reader import FileReader
from .solver import Solver
import argparse

EXAMPLE_PATH = 'examples/complicated.non'

""" class responsible for handling simulation """
class Simulation:
    def __init__(self, args: argparse.ArgumentParser):
        filepath = args.filepath if args.filepath else EXAMPLE_PATH
        self.nonogram = FileReader.read_nonogram(filepath)
        self.solver = Solver(self.nonogram)
        
    def solve(self) -> None:
        self.solver.solve()