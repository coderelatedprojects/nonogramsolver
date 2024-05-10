import timeit

class Solver:
    def __init__(__self__, game):
        __self__.game = game

    def solve(__self__):
        start = timeit.timeit()
        possible_row_solutions = []
        possible_col_solutions = []
        
        for row in __self__.game.nonogram.row_values:
            possible_row_solutions.append(__self__._get_vector_solutions_(row, __self__.game.nonogram.rows))

        for col in __self__.game.nonogram.col_values:
            possible_col_solutions.append(__self__._get_vector_solutions_(col, __self__.game.nonogram.cols))

        iteration = 0
        while not __self__._is_game_solved_():
            print(f'ITERATION {iteration}')
            print(f'POSSIBLE ROW SOLUTIONS: {possible_row_solutions}')
            print(f'POSSIBLE COL SOLUTIONS: {possible_col_solutions}')

            for i, single_row_solutions in enumerate(possible_row_solutions):
                possible_row_solutions[i] = __self__._remove_invalid_vector_solutions_(possible_row_solutions[i], __self__.game.board[i])
                common_row = __self__._get_common_vector_solution_(single_row_solutions)
                for j, item in enumerate(common_row):
                    if item != 0: __self__.game.board[i][j] = item

            for i, single_col_solutions in enumerate(possible_col_solutions):
                possible_col_solutions[i] = __self__._remove_invalid_vector_solutions_(possible_col_solutions[i], [item[i] for item in __self__.game.board ])
                common_col = __self__._get_common_vector_solution_(single_col_solutions)
                for j, item in enumerate(common_col):
                    if item != 0: __self__.game.board[j][i] = item

            print(__self__.game)
            iteration += 1
        
        end = timeit.timeit()
        print(f'solving time {end - start}ms')


    def _get_vector_solutions_(__self__, vector_values, length):
        print(f'{vector_values=}, {length=}')
        actual_length = length - sum(vector_values) + 1
        print(f'{actual_length=}')
        possible_solutions = []
        i = 0
        
        #get binary solutions
        while i < 2**actual_length-1:
            if (bin(i).count('1') == len(vector_values)):
                #translate binary solution into vector
                binary_solution = bin(i)[2:].rjust(actual_length, '0')
                print(f'{binary_solution=}')
                possible_solutions.append(__self__._convert_from_binary_solution_(binary_solution, vector_values))
            i +=1

        return possible_solutions

    def _convert_from_binary_solution_(__self__, binary_solution, vector_values):
        i = 0
        solution = []
        for bit in binary_solution:
            if bit == '0':
                solution.append(1)
            else:
                if i > 0: solution.append(1)
                solution.extend(2 for j in range(vector_values[i]))
                i += 1
        print(f'converted solution: {solution}')
        return solution

    def _is_game_solved_(__self__):
        for i, row in enumerate(__self__.game.board):
            validity = __self__._check_vector_validity_(row, __self__.game.nonogram.row_values[i])
            if not validity:
                print(f'INVALID: row {i}')
                return False
            
        for i in range(__self__.game.nonogram.cols):
            vector = [item[i] for item in __self__.game.board]
            validity = __self__._check_vector_validity_(vector, __self__.game.nonogram.col_values[i])
            if not validity:
                print(f'INVALID: col {i}')
                return False
        return True
        
    def _check_vector_validity_(__self__, vector, vector_values):
        current_value_index = 0
        current_filled_streak = 0
        only_zeros = False
        all_values_filled = False
        for element in vector:
            if only_zeros and element != 1:
                return False
            if element == 2:
                current_filled_streak += 1
            if not all_values_filled and current_filled_streak == vector_values[current_value_index]:
                current_value_index += 1
                current_filled_streak = 0
                if current_value_index == len(vector_values):
                    only_zeros = True
                    all_values_filled = True
        
        return all_values_filled
        

    def _get_common_vector_solution_(__self__, possible_vectors_solutions):
        summed_vector = [0 for i in range(len(possible_vectors_solutions[0]))]
        for vector_solution in possible_vectors_solutions:
            summed_vector = [x + y for x, y in zip(summed_vector, vector_solution)]

        common_vector = []
        for element in summed_vector:
            if element == len(possible_vectors_solutions):
                common_vector.append(1)
            elif element == 2*len(possible_vectors_solutions):
                common_vector.append(2)
            else:
                common_vector.append(0)

        return common_vector
    
    def _remove_invalid_vector_solutions_(__self__, current_solutions, board_vector):
        valid_solutions = []
        for single_solution in current_solutions:
            solution_valid = True
            for i, item in enumerate(single_solution):
                if board_vector[i] != 0 and board_vector[i] != item:
                    solution_valid = False
            if solution_valid:
                valid_solutions.append(single_solution)
        return valid_solutions