import math

class Puzzle:
    # Initialise the empty puzzle matrix, and a dictionary of the boxes in a sudoku
    def __init__(self):
            # Create the matrix, with all possible values for all possible rows and columns
            self.matrix = [[[x for x in range(1, 10)]
                             for _ in range(9)] for _ in range(9)]
            # Generate dictionary of 3x3 boxes and their respective cells
            self.boxes = self.generate_boxes()


    # Prints the sudoku with all possible values for each cell. 
    def __str__(self):
        # The full sudoku template
        full_matrix = ""
        # For each row in the matrix
        for row in self.matrix:
            # Create template, which we will use to replace values
            template = "| X X X | X X X | X X X | X X X | X X X | X X X | X X X | X X X | X X X |\n| X X X | X X X | X X X | X X X | X X X | X X X | X X X | X X X | X X X |\n| X X X | X X X | X X X | X X X | X X X | X X X | X X X | X X X | X X X |\n"
            # Turn it into a list so it is mutable
            template = list(template)
            # Print seprator for each new row
            full_matrix += "-"*73 + "\n"
            # for each cell in row
            for index,cell in enumerate(row):
                # If it is an int, place it in the top left X
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
            # return template to string format
            template = "".join(template)
            # Append it to our full template
            full_matrix += template
        # Once all rows are added, add a final horizontal seperator
        full_matrix += "-"*73 + "\n"
        return full_matrix


    # A function to solve the sudoku
    def solve(self):
        # If the puzzle is not solved
        while not self.is_solved():
            # Store the original
            old_matrix = str(self.matrix)
            # Check if any cells have been solved
            self.check_solved()
            # Remove possibilities based on known values in...
            # Rows
            self.check_row_singles()
            # Columns
            self.check_col_singles()
            # Boxes
            self.check_box_singles()
            # If no progress has been made
            if str(self.matrix) == old_matrix:
                print("No further progress can be made with current techniques.")
                break


    # Check whether the sudoku is solved
    def is_solved(self):
        # If there are any lists in our cells, it is not solved
        for row in self.matrix:
            for cell in row:
                if isinstance(cell, list):
                    return False
        # If you don't find any, it is solved
        return True


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
                        

    # A program that checks for known values in rows, and removes them from other cells in the same row
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


    # A function that checks for known values in columns, and removes them from other cells in the same column
    def check_col_singles(self):
        # For each column
        for x in range(9):
            # Create an empty cell list
            cells = []
            # For each cell in the column
            for y in range(9):
                cells.append(self.matrix[y][x])
            # Isolate any single values
            singles = self.check_singles(cells)
            # For each cell in the column
            for y in range(9):
                if isinstance(self.matrix[y][x], list):
                    self.matrix[y][x] = [item for item in self.matrix[y][x] if item not in singles]


    # A function that checks single values in boxes, and removes them from other cells in the same row
    def check_box_singles(self):
        # For each of the boxes, extract the relevant cells
        for box in self.boxes.values():
            # Create an empty cell list
            cells = []
            # Extract position of each relevant cell
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

    # Generates a dictionary of the 9 3x3 boxes that make a sudoku grid
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



def main():
    puzzle = Puzzle()
    # Transferring over puzzle contents
    numbers = "003020600900305001001806400008102900700000008006708200002609500800203009005010300"

    # replace known values in the sudoku
    for index, cell in enumerate(numbers):
         if cell != "0":
              row = math.floor(index/9)
              column = index % 9
              puzzle.matrix[row][column] = int(cell)

    print(puzzle)
    puzzle.solve()
    print(puzzle)


    # Got a couple of improvements to make. I need to start incorporating naked pairs calculation. This seems like it might help to sort out the more complex problems in the project Euler problem, at least it will make some progress on them. It shouldn't be too difficut. 
    # I also need to make it either more interactive or smarter. Currently it just runs through them blindly, and I have to tell it what to do. In reality I would like to make it so that it checks whether progress was made or not, if so it consolidates this progress and repeats, otherwise it moves to more complex methods in an iterative process. 
        




if __name__ == "__main__":
     main()