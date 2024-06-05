from itertools import combinations
import itertools


class Puzzle:
    def __init__(self):
            # Create the matrix, with all possible values for all possible rows and columns
            self.matrix = [[[x for x in range(1, 10)]
                             for _ in range(9)] for _ in range(9)]
            # This will be a list of all the sums present within the killer puzzle
            self.sums = []


    # A program to print the matrix more cleanly
    def pretty_print(self):
        # For each row in the matrix
        for row in self.matrix:
            # Create template, which we will use to replace values
            template = "| X X X | X X X | X X X | X X X | X X X | X X X | X X X | X X X | X X X |\n| X X X | X X X | X X X | X X X | X X X | X X X | X X X | X X X | X X X |\n| X X X | X X X | X X X | X X X | X X X | X X X | X X X | X X X | X X X |\n"
            # Turn it into a list so it is mutable
            template = list(template)
            # Print seprator for each new row
            print("-"*73) 
            # for each cell in row
            for index,cell in enumerate(row):
                # For each number in the cell
                for num_pos, num in enumerate(cell):
                    # Calculate its position in the above template
                    position = 2 + (2 * (num_pos % 3)) + (8 * index) + (74 * (num_pos // 3))
                    # Replace position in template with number
                    template[position] = str(num)
            # return template to string
            template = "".join(template)
            # Print
            print(template, end = "")
        # Print final separator
        print("-"*73)


    def add_sum_constraint(self,cells,total):
        """
        Add a sum constraint for a group of cells.

        :param cells: List of tuples, where each tuple is (row, col) for a cell
        :param total: The sum that these cells must add up to
        """
        self.sums.append({'cells': cells, 'total': total})


    def check_sum_constraint(self,sum_constraint):
        """
        check the possible values that would work for sum constraint

        :param sum_constraint: The sum constraint that we are investigating
        """
        
        # Extract number of cells involved
        cell_num = len(sum_constraint['cells'])
        total = sum_constraint['total']
        # Create a list of tuples; the potential combinations of numbers that could sum to this total
        possible_combinations = [combo for combo in 
                                 combinations(range(1, 10), cell_num) if sum(combo) == total]
        
        
        # Extract all the unique potential numbers that are valid for these cells. 
        # Using tools from: https://stackoverflow.com/questions/7590950/list-of-unique-items-in-a-list-of-tuples
        possible_values = set(itertools.chain(*possible_combinations))

        # Check whether the possible values contains all the numbers 1 to 9.
        if len(possible_values) == 9:
            # If so, there is no point trying to alter potential cell numbers
            pass
        else:
        # Check these against the cells possible range
        # For each cell in sum combination...
            for cell in sum_constraint['cells']:
                # Extract row and column
                row, column = cell
                # Extract the list of current potential values
                current_values = self.matrix[row][column]
                # Remove any that not possible due to sum combination
                current_values = [value for value in current_values if value in possible_values]
                # Update cell
                self.matrix[row][column] = current_values




def main():
    puzzle = Puzzle()
    puzzle.add_sum_constraint([(0, 0), (1, 0), (2,0), (3,0), (4,0), (5,0), (6,0), (7,0), (8,0)], 45)
    puzzle.add_sum_constraint([(0,1), (1,1), (2,1), (2,2), (3,2)], 22)
    puzzle.add_sum_constraint([(3,1), (4,1), (5,1)], 12)
    puzzle.add_sum_constraint([(6,1), (7,1), (8,1), (5,2), (6,2)], 23)
    puzzle.add_sum_constraint([(4,2), (4,3)], 13)
    puzzle.add_sum_constraint([(7,2), (8,2)], 10)
    puzzle.add_sum_constraint([(0,2), (1,2)], 15)
    puzzle.add_sum_constraint([(0,3), (0,4)], 13)
    puzzle.add_sum_constraint([(1,3), (2,3), (3,3)], 18)
    puzzle.add_sum_constraint([(5,3), (6,3), (7,3)], 7)
    puzzle.add_sum_constraint([(8,3), (8,4)], 9)
    puzzle.add_sum_constraint([(1,4), (1,5), (2,4)], 15)
    puzzle.add_sum_constraint([(3,4), (4,4), (5,4)], 15)
    puzzle.add_sum_constraint([(6,4), (7,4), (7,5)], 16)
    puzzle.add_sum_constraint([(0,5), (0,6), (1,6)], 7)
    puzzle.add_sum_constraint([(2,5), (2,6), (3,6)], 17)
    puzzle.add_sum_constraint([(3,5), (4,5), (5,5)], 18)
    puzzle.add_sum_constraint([(6,5), (6,6), (5,6)], 17)
    puzzle.add_sum_constraint([(8,5), (8,6), (7,6)], 17)
    puzzle.add_sum_constraint([(4,6), (4,7), (4,8)], 9)
    puzzle.add_sum_constraint([(0,7), (1,7)], 13)
    puzzle.add_sum_constraint([(2,7), (2,8)], 13)
    puzzle.add_sum_constraint([(3,7), (3,8)], 13)
    puzzle.add_sum_constraint([(5,7), (5,8)], 11)
    puzzle.add_sum_constraint([(6,7), (6,8)], 7)
    puzzle.add_sum_constraint([(7,7), (8,7)], 15)
    puzzle.add_sum_constraint([(0,8), (1,8)], 7)
    puzzle.add_sum_constraint([(7,8), (8,8)], 8)

    for sum_constraint in puzzle.sums:
       puzzle.check_sum_constraint(sum_constraint)
     
    puzzle.pretty_print()


if __name__ == "__main__":
      main()