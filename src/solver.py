import time
from typing import List
from .nonogram import Nonogram

""" class responsible for solving a nonogram """
class Solver:
    def __init__(self, nonogram: Nonogram):
        self.nonogram = nonogram

    def solve(self) -> None:
        start_time = time.time()
        possible_row_solutions = []
        possible_col_solutions = []

        for row in self.nonogram.rows:
            possible_row_solutions.append(self._get_vector_solutions_(row, self.nonogram.width))

        for col in self.nonogram.columns:
            possible_col_solutions.append(self._get_vector_solutions_(col, self.nonogram.height))

        iteration = 0
        while not self._is_nonogram_solved_():

            for i in range(len(possible_row_solutions)):
                possible_row_solutions[i] = self._remove_invalid_vector_solutions_(possible_row_solutions[i], self.nonogram.solution[i])
                common_row = self._get_common_vector_solution_(possible_row_solutions[i])
                for j, item in enumerate(common_row):
                    if item != 0: self.nonogram.solution[i][j] = item

            for i in range(len(possible_col_solutions)):
                possible_col_solutions[i] = self._remove_invalid_vector_solutions_(possible_col_solutions[i], [item[i] for item in self.nonogram.solution ])
                common_col = self._get_common_vector_solution_(possible_col_solutions[i])
                for j, item in enumerate(common_col):
                    if item != 0: self.nonogram.solution[j][i] = item

            iteration += 1
        
        print(self.nonogram)
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

    def _convert_from_binary_solution_(self, binary_solution: str, vector_values: List[int]) -> List[int]:
        i = 0
        solution = []
        for bit in binary_solution:
            if bit == '0':
                solution.append(1)
            else:
                if i > 0: solution.append(1)
                solution.extend(2 for j in range(vector_values[i]))
                i += 1
        return solution

    def _is_nonogram_solved_(self) -> bool:
        for i, row in enumerate(self.nonogram.solution):
            validity = self._check_vector_validity_(row, self.nonogram.rows[i])
            if not validity:
                return False
            
        for i in range(self.nonogram.width):
            vector = [item[i] for item in self.nonogram.solution]
            validity = self._check_vector_validity_(vector, self.nonogram.columns[i])
            if not validity:
                return False
        return True
        
    def _check_vector_validity_(self, vector: List[int], vector_values: List[int]) -> bool:
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
        

    def _get_common_vector_solution_(self, possible_vectors_solutions: List[List[int]]) -> List[int]:
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
    
    def _remove_invalid_vector_solutions_(self, current_solutions: List[List[int]], solution_vector: List[int]) -> List[List[int]]:
        valid_solutions = []
        for single_solution in current_solutions:
            solution_valid = True
            for i, item in enumerate(single_solution):
                if solution_vector[i] != 0 and solution_vector[i] != item:
                    solution_valid = False
            if solution_valid:
                valid_solutions.append(single_solution)
        return valid_solutions