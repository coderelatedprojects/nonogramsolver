BLANK = ' '
PRINTING_SYMBOL_MAP = {
    0 : ' ',
    1 : '•',
    2 : '█'
}

class Nonogram:
    def __init__(self, config):
        self.__dict__ = config
        self.solution = [[0 for y in range(self.width)] for x in range(self.height)]
    
    def __str__(self):
        # extend printing by title and author of the puzzle

        max_col_len = max(len(values) for values in self.columns)
        max_row_len = max(len(values) for values in self.rows)
        
        #this is disgusting, I know
        printing_array = [[BLANK if max_col_len > len(self.columns[j])+i or j < 0 else str(self.columns[j][i-(max_col_len-len(self.columns[j]))]) for j in range(-max_row_len, len(self.columns))] for i in range(max_col_len)]
        printing_array.extend([[BLANK if -i > len(self.rows[j]) else PRINTING_SYMBOL_MAP.get(self.solution[j][i]) if i>=0 else str(self.rows[j][i]) for i in range(-max_row_len,self.width)] for j in range(self.height)])

        return '\n'.join([' '.join(row) for row in printing_array])