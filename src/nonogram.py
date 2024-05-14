class Nonogram:
    def __init__(__self__, row_values, col_values):
        __self__.row_values = row_values
        __self__.col_values = col_values
        __self__.rows = len(row_values)
        __self__.cols = len(col_values)
    
    def __str__(__self__):
        return f'Nonogram ({len(__self__.row_values)},{len(__self__.col_values)}) \
                Rows: {__self__.row_values} \
                Columns: {__self__.col_values}'