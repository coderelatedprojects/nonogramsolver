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
            print(f'preparing row solutions... {i+1}/{nonogram.height} ',end="\r")
        print(f'\nrow solution finished')

        for i, col in enumerate(nonogram.columns):
            possible_col_solutions.append(self._get_vector_solutions_(col, nonogram.height))
            print(f'preparing col solutions... {i+1}/{nonogram.width} ',end="\r")
        print(f'\ncol solution finished')

        iteration = 0
        any_changes = True
        while not self._is_nonogram_solved_(nonogram) or not any_changes:
            if iteration > 20:
                break

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
            print(f'{iteration=}', end="\r")

        print('')        
        print(nonogram)
        print(f'Solution time: {time.time()-start_time:.4f} s')

    def _get_vector_solutions_(self, vector_values: List[int], length: int) -> List[int]:
        actual_length = length - sum(vector_values) + 1
        possible_solutions = []
        
        outcome_tree = [['0','1']]

        for i in range(1, actual_length):
            outcome_tree.append([])
            for combination in outcome_tree[i-1]:
                new_combination_zero = combination + '0'
                new_combination_one = combination + '1'

                if i < actual_length - 1:
                    outcome_tree[i].append(new_combination_zero)
                    if combination.count('1') < len(vector_values):
                        outcome_tree[i].append(new_combination_one)
                else:
                    if new_combination_zero.count('1') == len(vector_values): outcome_tree[i].append(new_combination_zero)
                    if new_combination_one.count('1') == len(vector_values): outcome_tree[i].append(new_combination_one)
        
        for binary_solution in outcome_tree[-1]:
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
                for j in range(vector_values[i]):
                    solution += '1'
                i += 1
        return int(solution,2)

    def _is_nonogram_solved_(self, nonogram) -> bool:
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
        summed_vector = [0 for i in range(solution_length)]
        for vector_solution in possible_vectors_solutions:
            vector_solution_string = '{0:b}'.format(vector_solution).rjust(solution_length, '0')
            summed_vector = [x + int(y) for x, y in zip(summed_vector, [*vector_solution_string])]

        common_vector = []
        for element in summed_vector:
            if element == 0:
                common_vector.append(0)
            elif element == len(possible_vectors_solutions):
                common_vector.append(1)
            else:
                common_vector.append(2)

        return common_vector
    
    def _remove_invalid_vector_solutions_(self, current_solutions: List[int], solution_vector: List[int], solution_length: int) -> List[List[int]]:
        valid_solutions = []
        for single_solution in current_solutions:
            solution_valid = True
            solution_string = '{0:b}'.format(single_solution).rjust(solution_length, '0')
            #print(f'{solution_string=}')
            for i, item in enumerate([*solution_string]):
                if solution_vector[i] != 2 and solution_vector[i] != int(item):
                    #print(f'{item=}')
                    #print(f'{solution_vector[i]=}')
                    solution_valid = False
                    break
            if solution_valid:
                valid_solutions.append(single_solution)
        return valid_solutions