## I am going to start by creating a standard sudoku solver, and then I can move onto the killer sudoku. We will start by transferring a lot of the other problem over. 

from itertools import combinations
import itertools
import math

class Puzzle:
    # Initialise the empty puzzle matrix, and a dictionary of the boxes in a sudoku
    def __init__(self):
            # Create the matrix, with all possible values for all possible rows and columns
            self.matrix = [[[x for x in range(1, 10)]
                             for _ in range(9)] for _ in range(9)]
            # Generate dictionary of boxes and their cells
            self.boxes = self.generate_boxes()


    def generate_boxes(self):
        boxes = {}
        box_id = 0
        # Loop over each 3x3 box starting point
        for box_row in range(0, 9, 3):
            for box_col in range(0, 9, 3):
                box_cells = []
                # Loop over each cell within a 3x3 box
                for row in range(3):
                    for col in range(3):
                        box_cells.append((box_row + row, box_col + col))
                # Add the cells to the dictionary
                boxes[f"box_{box_id}"] = box_cells
                box_id += 1

        return boxes



    # Pretty printing of the sudoku, so that we can see the possible values for each square printed in a clearer format
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
                    if isinstance(cell, int):
                        position = 2 + (8 * index)
                        template[position] = str(cell)
                    else:
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

    # A function to find instances in the sudoku where there is only one possible number, and to replace it with an int
    def check_solved(self):
        # For each row in the matrix
        for row_pos, row in enumerate(self.matrix):
            # For each cell within the row
            for col_pos, cell in enumerate(row):
                # If it is a list of length 1
                if isinstance(cell, list) and len(cell) == 1:
                    # Replace the cell with an int of the number
                    self.matrix[row_pos][col_pos] = cell[0]
                        
    # A program that checks for single values in rows, and removes them from other cells in the same row
    def check_row_singles(self):
        # For each row
        for y in range(9):
            # Create an empty cell list
            cells = []
            # For each cell in the row
            for x in range(9):
                # Append it to the list
                cells.append(self.matrix[y][x])
            # Isolate any single values
            singles = self.check_singles(cells)
            # For each cell in the row
            for x in range(9):
                # If the cell is a list
                if isinstance(self.matrix[y][x], list):
                    # Remove any impossibilities (based on singles) from the list
                    self.matrix[y][x] = [item for item in self.matrix[y][x] if item not in singles]

    # A function that checks for single values in columns, and removes them from other cells in the same row
    def check_col_singles(self):
        # for each column
        for x in range(9):
            # Create an empty cell list
            cells = []
            # For each cell in column
            for y in range(9):
                cells.append(self.matrix[y][x])
            # Isolate any single valyes
            singles = self.check_singles(cells)
            # For each cell in the column
            for y in range(9):
                if isinstance(self.matrix[y][x], list):
                    self.matrix[y][x] = [item for item in self.matrix[y][x] if item not in singles]

    # A function that checks single values in boxes, and removes them from other cells in the same row
    def check_box_singles(self):
        # For each of the boxes, extract the relevant cells
        for box in self.boxes.values():
            # create an empty cell list
            cells = []
            # Extract position for each relevant cell
            for y, x in box:
                cells.append(self.matrix[y][x])
            # Isolate any single values
            singles = self.check_singles(cells)
            # For each cell in box
            for y,x in box:
                if isinstance(self.matrix[y][x], list):
                    self.matrix[y][x] = [item for item in self.matrix[y][x] if item not in singles]


    # A function taking the list of cells as an input, and returning a list of single numbers
    def check_singles(self, cells):
        # Create an empty list to store known values
        singles = []
        # For each cell in the passed cells list
        for cell in cells:
            # If it is an int
            if isinstance(cell, int):
                # Append it to our list of known values
                singles.append(cell)
        # Return known values
        return singles

        
def main():
    puzzle = Puzzle()
    # Transferring over puzzle contents
    # Always add an extra 0 at the start to even out the numbers
    numbers = "003020600900305001001806400008102900700000008006708200002609500800203009005010300"

    for index, cell in enumerate(numbers):
         if cell != "0":
              row = math.floor(index/9)
              column = index % 9
              puzzle.matrix[row][column] = int(cell)

    for _ in range(10):
        puzzle.check_solved()
        puzzle.check_row_singles()
        puzzle.check_solved()
        puzzle.check_col_singles()
        puzzle.check_solved()
        puzzle.check_box_singles()

    puzzle.pretty_print()
        




if __name__ == "__main__":
     main()