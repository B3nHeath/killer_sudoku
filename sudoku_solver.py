import math
import numpy as np

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
            # Append it to our full sudoku
            full_matrix += template
        # Once all rows are added, add a final horizontal seperator
        full_matrix += "-"*73 + "\n"
        return full_matrix


    # A function to solve the sudoku
    def solve(self):
        # Initialise variable telling us whether programme is able to make progress
        progress_made = True
        # If the puzzle is not solved and we are making progress
        while not self.is_solved() and progress_made:
            # Store the original
            old_matrix = str(self.matrix)
            # Check if any cells have been solved
            self.check_solved()
            # Check for naked and hidden singles
            self.check_singles()
            # If no progress has been made, go up in order complexity
            if str(self.matrix) == old_matrix:
                # Check for naked and hidden pairs
                self.check_pairs()
                if str(self.matrix) == old_matrix:
                    print("No further progress can be made with current techniques.")
                    progress_made = False


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


    def check_singles(self):
        for i in range(9):
            self.eliminate_knowns(self.matrix[i], 'row', i)
            self.hidden_singles(self.matrix[i], 'row', i)
            self.eliminate_knowns([self.matrix[x][i] for x in range(9)], 'col', i)
            self.hidden_singles([self.matrix[x][i] for x in range(9)], 'col', i) 
        # Need to write box logic, feel that there is a way to incorporate this with a bit of thinking
        for box in self.boxes.values():
            self.eliminate_knowns([self.matrix[y][x] for y,x in box], "box", box)
            self.hidden_singles([self.matrix[y][x] for y,x in box], "box", box)


    def check_pairs(self):
        for i in range(9):
            self.naked_pairs(self.matrix[i], 'row', i)
            self.naked_pairs([self.matrix[x][i] for x in range(9)], 'col', i)
        # Need to write box logic, feel that there is a way to incorporate this with a bit of thinking
        for box in self.boxes.values():
            self.naked_pairs([self.matrix[y][x] for y,x in box], "box", box)


    def eliminate_knowns(self, cells, container_type, container_num):
        singles = self.get_singles(cells)
        for index, cell in enumerate(cells):
            if isinstance(cell, list):
                new_candidates = [item for item in cell if item not in singles]
                self.update_matrix(new_candidates, container_type, container_num, index)


    def hidden_singles(self, cells, container_type, container_num):
        singles = self.get_singles(cells)
        counts = count_elements_lists(flatten_list(cells))
        unique_values = []
        for value in counts.keys():
            if counts[value] == 1 and value not in singles:
                # find occurrence of value in the row, and replace the cell value
                unique_values.append(value)

        for index, cell in enumerate(cells):
            if isinstance(cell, list):
                for unique_value in unique_values:
                    if unique_value in cell:
                        self.update_matrix(unique_value, container_type, container_num, index)


    # A function taking the list of cells as an input, and returning a list of single numbers
    def get_singles(self, cells):
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


    def naked_pairs(self, cells, container_type, container_num):
        pairs = self.get_pairs(cells)
        for index, cell in enumerate(cells):
            # If the cell is a list
            if isinstance(cell, list):
                if not set(cell).issubset(pairs):
                    new_candidates = [item for item in cell if item not in pairs]
                    self.update_matrix(new_candidates, container_type, container_num, index)


    def get_pairs(self, cells):
        naked_pairs = []
        pairs = [cell for cell in cells if isinstance(cell, list) and len(cell) == 2]
        pairs_count = {tuple(pair): pairs.count(pair) for pair in pairs}
        for num1,num2 in pairs_count:
            if pairs_count[(num1,num2)] == 2:
                naked_pairs += [num1, num2]
        return naked_pairs


    def update_matrix(self, new_candidates, container_type, container_num, index):
        if container_type == "row":
            self.matrix[container_num][index] = new_candidates
        if container_type == "col":
            self.matrix[index][container_num] = new_candidates
        if container_type == "box":
            y,x = container_num[index]
            self.matrix[y][x] = new_candidates
            # Need to write box logic


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


# Flattens lists of lists into a single list
def flatten_list(nested_list):
    flattened = []
    for item in nested_list:
        if isinstance(item, list):
            flattened.extend(flatten_list(item))
        else:
            flattened.append(item)
    return flattened


# Counts the frequency of elements in a list and returns a dictionary
def count_elements_lists(nums):
    counts = {}
    for num in nums:
        # Check if the element 'num' is already in the dictionary
        if num in counts.keys():
            # If yes, increment the frequency count
            counts[num] += 1
        else:
            # If not, create a new entry in the dictionary with key 'num' and initial value 1
            counts[num] = 1
    return counts



def main():
    puzzle = Puzzle()
    # Transferring over puzzle contents
    numbers = "300200000000107000706030500070009080900020004010800050009040301000702000000008006"

    # replace known values in the sudoku
    for index, cell in enumerate(numbers):
         if cell != "0":
              row = math.floor(index/9)
              column = index % 9
              puzzle.matrix[row][column] = int(cell)
    print(puzzle, end = "\n\n")
    puzzle.solve()
    print(puzzle)


    # Got a couple of improvements to make. I need to start incorporating naked pairs calculation. This seems like it might help to sort out the more complex problems in the project Euler problem, at least it will make some progress on them. It shouldn't be too difficut. 
    # I also need to make it either more interactive or smarter. Currently it just runs through them blindly, and I have to tell it what to do. In reality I would like to make it so that it checks whether progress was made or not, if so it consolidates this progress and repeats, otherwise it moves to more complex methods in an iterative process. 
        




if __name__ == "__main__":
     main()