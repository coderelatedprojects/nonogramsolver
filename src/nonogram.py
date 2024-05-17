BLANK = ' '
PRINTING_SYMBOL_MAP = {
    0 : ' ',
    1 : '•',
    2 : '█'
}

""" class that represents the nonogram puzzle and its solution """
class Nonogram:
    def __init__(self, config: dict):
        self.__dict__ = config
        self.max_col_len = max(len(values) for values in self.columns)
        self.max_row_len = max(len(values) for values in self.rows)
        max_row_value_len = max(max(len(str(row_element)) for row_element in row) for row in self.rows)
        max_col_value_len = max(max(len(str(col_element)) for col_element in column) for column in self.columns)
        self.max_value_len = max([max_row_value_len, max_col_value_len])
        self.solution = [[0 for _ in range(self.width)] for _ in range(self.height)]
    
    def __str__(self) -> str:
        #this is disgusting, I know
        info = [
            f'title: {self.title}',
            f'author: {self.by if self.by else "unknown"}'
        ]
        printing_array = [[BLANK*self.max_value_len if self.max_col_len > len(self.columns[j])+i or j < 0 else str(self.columns[j][i-(self.max_col_len-len(self.columns[j]))]).ljust(self.max_value_len, ' ') for j in range(-self.max_row_len, len(self.columns))] for i in range(self.max_col_len)]
        printing_array.extend([[BLANK*self.max_value_len if -i > len(self.rows[j]) else PRINTING_SYMBOL_MAP.get(self.solution[j][i]).ljust(self.max_value_len, ' ') if i>=0 else str(self.rows[j][i]).ljust(self.max_value_len, ' ') for i in range(-self.max_row_len,self.width)] for j in range(self.height)])

        return '\n'.join(info) + '\n'.join([' '.join(row) for row in printing_array])