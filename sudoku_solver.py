from sudoku_board import sudokuBoard
import numpy as np

class sudokuSolver():

    def __init__(self, sudokuBoard):

        self.sudoku_board = sudokuBoard


    def insertions_left(self):
        
        # We want to enumerate the quantity of each number we need to insert
        insertions = {1: 9, 2: 9, 3: 9, 4: 9, 5: 9, 6: 9, 7: 9,\
                        8: 9, 9: 9}
        
        # Using the clues attribute for the sudokuBoard class, we can deduct
        # 1 for each number we encounter and keep track of the numbers we 
        # have still to insert.
        for clue in self.sudoku_board.clues:

            number = clue[2]
            insertions[number] -= 1
        
        return insertions
        
    def generate_solution(self):
    
        # Numbers left to choose from
        remaining_numbers = self.insertions_left()

        # Available insertions into puzzle board
        available_inserts = self.sudoku_board.available_inserts()

        
        for empty_slot in available_inserts:
            random_choices = []
                
            # Creating array of numbers that can still be inserted into 
            # the puzzle. If the number i can be picked more than zero 
            # times, then we add that to the list of random choices
            for number in remaining_numbers:
                if remaining_numbers[number] > 0:
                    random_choices.append(number)
            
            # We pick a random number from the list of random_choices 
            insert = np.random.choice(random_choices)

            # Update the spot on the baord with the new insert
            self.sudoku_board.board[empty_slot[0],empty_slot[1]] = insert

            # Subtract the number of insert needed for the remainder 
            # of the puzzle
            remaining_numbers[insert] -= 1








if __name__ == '__main__':

    # Testing sudokuBoard setup
    s = sudokuBoard(clues= [(0,0,5), (1,2,9), (4,5,8), (0,1,4), (0,3,1), (2,4,7)])
    s.show_board()

    # Testing sudokuSolver insertions_left function
    solver = sudokuSolver(s)
    print(solver.insertions_left())

    # Testing generate sudokuSolver
    solver.generate_solution()

    s.show_board()
    