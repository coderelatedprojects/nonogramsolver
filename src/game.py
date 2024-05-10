from .nonogram import Nonogram
from .file_reader import FileReader
from .solver import Solver

BLANK = ' '
PRINTING_SYMBOL_MAP = {
    0 : ' ',
    1 : '•',
    2 : '█'
}

class Game:
    def __init__(__self__):
        __self__.nonogram = FileReader.read_nonogram('data/nono3.txt')
        __self__.board = [[0 for y in range(__self__.nonogram.cols)] for x in range(__self__.nonogram.rows)]
        print(__self__)
        __self__.solver = Solver(__self__) #possibility to switch solvers
        __self__.solve()

    def __str__(__self__):
        max_col_len = max(len(values) for values in __self__.nonogram.col_values)
        max_row_len = max(len(values) for values in __self__.nonogram.row_values)
        
        print(f'{max_col_len=}')
        print(f'{max_row_len=}')
        print(f'{ __self__.nonogram.col_values=}')
        print(f'{ __self__.nonogram.row_values=}')
        #this is disgusting, I know
        printing_array = [[BLANK if max_col_len > len(__self__.nonogram.col_values[j])+i or j < 0 else str(__self__.nonogram.col_values[j][i-(max_col_len-len(__self__.nonogram.col_values[j]))]) for j in range(-max_row_len, len(__self__.nonogram.col_values))] for i in range(max_col_len)]
        #printing_array.extend([[BLANK if max_row_len > len(__self__.nonogram.row_values[j])-i else PRINTING_SYMBOL_MAP.get(__self__.board[j][i]) if i>=0 else str(__self__.nonogram.row_values[j][i]) for i in range(-max_row_len,__self__.nonogram.cols)] for j in range(__self__.nonogram.rows)])
        printing_array.extend([[BLANK if -i > len(__self__.nonogram.row_values[j]) else PRINTING_SYMBOL_MAP.get(__self__.board[j][i]) if i>=0 else str(__self__.nonogram.row_values[j][i]) for i in range(-max_row_len,__self__.nonogram.cols)] for j in range(__self__.nonogram.rows)])

        return '\n'.join([' '.join(row) for row in printing_array])
    
    # in future - pass solver as an argument
    def solve(__self__):
        __self__.solver.solve()