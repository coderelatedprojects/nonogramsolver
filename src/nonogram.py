BLANK = ' '
PRINTING_SYMBOL_MAP = {
    0 : ' ',
    1 : '•',
    2 : '█'
}

class Nonogram:
    def __init__(self, row_values, col_values):
        self.row_values = row_values
        self.col_values = col_values
        self.rows = len(row_values)
        self.cols = len(col_values)
        self.solution = [[0 for y in range(self.cols)] for x in range(self.rows)]
    
    def __str__(self):
        max_col_len = max(len(values) for values in self.col_values)
        max_row_len = max(len(values) for values in self.row_values)
        
        #this is disgusting, I know
        printing_array = [[BLANK if max_col_len > len(self.col_values[j])+i or j < 0 else str(self.col_values[j][i-(max_col_len-len(self.col_values[j]))]) for j in range(-max_row_len, len(self.col_values))] for i in range(max_col_len)]
        printing_array.extend([[BLANK if -i > len(self.row_values[j]) else PRINTING_SYMBOL_MAP.get(self.solution[j][i]) if i>=0 else str(self.row_values[j][i]) for i in range(-max_row_len,self.cols)] for j in range(self.rows)])

        return '\n'.join([' '.join(row) for row in printing_array])