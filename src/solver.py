import time
from typing import List
from .nonogram import Nonogram

""" class responsible for solving a nonogram """
class Solver:
    def solve(self, nonogram: Nonogram) -> None:
        start_time = time.time()
        possible_row_solutions = []
        possible_col_solutions = []

        for i, row in enumerate(nonogram.rows):
            possible_row_solutions.append(self._get_vector_solutions_(row, nonogram.width))

        for i, col in enumerate(nonogram.columns):
            possible_col_solutions.append(self._get_vector_solutions_(col, nonogram.height))

        iteration = 0
        while not self._is_nonogram_solved_(nonogram):
            for i in range(len(possible_row_solutions)):
                possible_row_solutions[i] = self._remove_invalid_vector_solutions_(possible_row_solutions[i], nonogram.solution[i], nonogram.width)
                common_row = self._get_common_vector_solution_(possible_row_solutions[i], nonogram.width)
                for j, item in enumerate(common_row):
                    if item != 2: nonogram.solution[i][j] = item

            for i in range(len(possible_col_solutions)):
                possible_col_solutions[i] = self._remove_invalid_vector_solutions_(possible_col_solutions[i], [item[i] for item in nonogram.solution], nonogram.height)
                common_col = self._get_common_vector_solution_(possible_col_solutions[i], nonogram.height)
                for j, item in enumerate(common_col):
                    if item != 2: nonogram.solution[j][i] = item

            iteration += 1

        print('==================================================')        
        print(nonogram)
        print(f'Solution time: {time.time()-start_time:.4f} s')

    def _get_vector_solutions_(self, vector_values: List[int], length: int) -> List[int]:
        actual_length = length - sum(vector_values) + 1
        possible_solutions = []
        
        s_time = time.time()
        possible_binary_solutions = self._get_all_binary_repr_(actual_length, len(vector_values))

        s_time = time.time()
        for binary_solution in possible_binary_solutions:
            possible_solutions.append(self._convert_from_binary_solution_(binary_solution, vector_values))

        return possible_solutions

    def _convert_from_binary_solution_(self, binary_solution: str, vector_values: List[int]) -> int:
        i = 0
        solution = ''
        for bit in binary_solution:
            if bit == '0':
                solution += '0'
            else:
                if i > 0: solution += '0'
                solution += '1'*vector_values[i]
                i += 1
        return int(solution,2)

    def _is_nonogram_solved_(self, nonogram) -> bool:
        s_time = time.time()
        for i, row in enumerate(nonogram.solution):
            validity = self._check_vector_validity_(row, nonogram.rows[i])
            if not validity:
                return False
            
        for i in range(nonogram.width):
            vector = [item[i] for item in nonogram.solution]
            validity = self._check_vector_validity_(vector, nonogram.columns[i])
            if not validity:
                return False
        return True
        
    def _check_vector_validity_(self, vector: List[int], vector_values: List[int]) -> bool:
        current_value_index = 0
        current_filled_streak = 0
        only_zeros = False
        all_values_filled = False
        for element in vector:
            if only_zeros and element != 0:
                return False
            if element == 1:
                current_filled_streak += 1
            if not all_values_filled and current_filled_streak == vector_values[current_value_index]:
                current_value_index += 1
                current_filled_streak = 0
                if current_value_index == len(vector_values):
                    only_zeros = True
                    all_values_filled = True
        
        return all_values_filled
        

    def _get_common_vector_solution_(self, possible_vectors_solutions: List[int], solution_length: int) -> List[int]:
        s_time = time.time()
        solution = [2 for _ in range(solution_length)]
        only_ones_int = 2**solution_length-1
        common_ones = possible_vectors_solutions[0]
        common_zeroes = only_ones_int ^ possible_vectors_solutions[0]

        for possible_solution in possible_vectors_solutions:
            common_ones = common_ones & possible_solution
            common_zeroes = common_zeroes & (only_ones_int ^ possible_solution)

        for i, element in enumerate('{0:b}'.format(common_ones).rjust(solution_length, '0')):
            if element == '1':
                solution[i] = 1
        
        for i, element in enumerate('{0:b}'.format(common_zeroes).rjust(solution_length, '0')):
            if element == '1':
                solution[i] = 0
        
        return solution
    
    def _remove_invalid_vector_solutions_(self, current_solutions: List[int], solution_vector: List[int], solution_length: int) -> List[List[int]]:
        s_time = time.time()
        valid_solutions = []
        only_ones_int = 2**solution_length-1

        solution_vector_string = ''.join(str(x) for x in solution_vector)
        solution_vector_ones = int(solution_vector_string.replace('2', '0'),2)
        solution_vector_zeroes = only_ones_int ^ int(solution_vector_string.replace('2','1'),2)

        for single_solution in current_solutions:
            if single_solution & solution_vector_ones == solution_vector_ones and (only_ones_int ^ single_solution) & solution_vector_zeroes == solution_vector_zeroes:
                valid_solutions.append(single_solution)

        return valid_solutions
    
    def _get_all_binary_repr_(self, length: int, ones: int) -> List[str]:
        if length == 0:
            return []
        elif length == ones:
            return ['1' * length]
        elif ones == 0:
            return ['0' * length]
        
        result = []
        stack = [(length, ones, '')]
        
        while stack:
            current_length, current_ones, current_string = stack.pop()
            
            if current_length == 0:
                result.append(current_string)
            elif current_length == current_ones:
                result.append(current_string + '1' * current_length)
            elif current_ones == 0:
                result.append(current_string + '0' * current_length)
            else:
                stack.append((current_length - 1, current_ones - 1, current_string + '1'))
                stack.append((current_length - 1, current_ones, current_string + '0'))
        
        return result