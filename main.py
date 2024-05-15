from src.simulation import Simulation
import argparse

parser = argparse.ArgumentParser(
    prog='nonogram_solver',
    description="Program dedicated to solving nonograms",
    epilog='coderelatedprojects.com'
)

parser.add_argument('-f', '--filepath', help="Solve nonogram from file *.non format")
parser.add_argument('-v', '--verbose', action="count", default=0, help="Display additional information during processing")
parser.add_argument('-s', '--step-by-step', action="store_true", help="Perform single step and wait for input")
parser.add_argument('--version', action="version", version="%(prog)s 1.0")

if __name__ == '__main__':
    print('Nonogram Solver v. 1.0')
    simulation = Simulation(parser.parse_args())