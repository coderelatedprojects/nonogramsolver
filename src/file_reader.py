from .reader import ReaderInterface
from .nonogram import Nonogram

class FileReader(ReaderInterface):
    def read_nonogram(path) -> Nonogram:
        # add checks for incorrect data and regex
        with open(path, 'r') as reader:
            row_values = [[int(rowvalue) for rowvalue in row.split(';')] for row in reader.readline().split(',')]
            col_values = [[int(colvalue) for colvalue in col.split(';')] for col in reader.readline().split(',')]
        return Nonogram(row_values, col_values)
                