from sudoku_board import sudokuBoard
import numpy as np

class sudokuSolver():

    def __init__(self, sudokuBoard):

        self.sudoku_board = sudokuBoard

    def insertions_left(self):
        '''
        Returns a dictionary of sudoku values and the number of each that 
        still remain to be chosen
        '''
        
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
        '''
        Fills up the remaining slots of the sudoku board with random
        sudoku values according to the number of insertions left for
        each sudoku value
        '''
    
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

    def score_puzzle(self):
        '''
        Assigns a score of -1 for every unique element in each row and 
        column. The top score is -162.

        Method of scoring courtesy of: 
        https://github.com/erichowens/SudokuSolver
        '''

        # Set our score to 0
        score = 0 
        
        
        # First we score row-by-row
        for i in range(9):
            
            # Get the current row
            current_row = self.sudoku_board.board[i,:]
            
            # we store all the values into a dictionary
            values = {}

            # We go through each element in the array
            for j in range(9):
                
                # If we have not seen the current number, we store in our 
                # dictionary. If we have already seen it, we remove it
                # from our dictionary so that we only retain numbers that
                # are unique
                if current_row[j] not in values.keys():
                    values[current_row[j]] = 1
                else:
                    values.pop(current_row[j])

            # From the values dictionary, we can make a score of -1 times
            # each number of unique row elements
            for item in values.items():
                score += (-1) * (item[1])

            #print(values.items(), "    ", "score = ", score)

        
        # Now we score by column
        for i in range(9):

            # Get the current column
            current_column = self.sudoku_board.board[:,i]

            # we go through the exact same process for the columns
            values = {}

            for j in range(9):
                if current_column[j] not in values.keys():
                    values[current_column[j]] = 1
                else:
                    values.pop(current_column[j])

            for item in values.items():
                score += (-1) * (item[1])

            #print(values.items(), "    ", "score = ", score)

        return score


    def new_solution(self):
        '''
        selects a random grid within the puzzle and randomly interchanges
        2 of the slots within the grid. Then returns the new puzzle board

        Again, method of generating new solutions is courtesy of: 
        https://github.com/erichowens/SudokuSolver
        '''

        # We generate a new solution with a copy of the original board
        new_sudoku_board = sudokuBoard()
        new_sudoku_board.board = self.sudoku_board.board

        # We generate a random row and col and feed those into local_grid
        # in order to get a random grid from the board
        row = np.random.choice(range(9))
        col = np.random.choice(range(9))

        # We get the row and column values for the local grid at (row,col)
        row_values = 0
        column_values = 0
         
        if 0 <= row <= 2:
            row_values = [0, 1, 2]
        elif 3 <= row <= 5:
            row_values = [3, 4, 5]
        else:
            row_values = [6, 7, 8]

        if 0 <= col <= 2:
            column_values = [0, 1, 2]
        elif 3 <= col <= 5:
            column_values = [3, 4, 5]
        else:
            column_values = [6, 7, 8]
        
        valid_change = False
        while not valid_change:

            # We must now pick two random slots to interchange
            i_1 = np.random.choice(row_values)
            j_1 = np.random.choice(column_values)

            i_2 = np.random.choice(row_values)
            j_2 = np.random.choice(column_values)

            entry1 = (i_1,j_1, new_sudoku_board.board[i_1,j_1]) 
            entry2 = (i_2,j_2, new_sudoku_board.board[i_2,j_2]) 
            
            if entry1 not in self.sudoku_board.clues and \
                entry2 not in self.sudoku_board.clues:

                valid_change = True

            
        #print('(', i_1, ',', j_1, ')', 'interchanged with', '(', i_2, ',', j_2, ')')

        # Now we interchange the slots within the puzzle. First storing the
        # value of the first slot into a temporary variable
        tmp = new_sudoku_board.board[i_1, j_1]
            
        # Then exchange...
        new_sudoku_board.board[i_1, j_1] = new_sudoku_board.board[i_2, j_2] 
        new_sudoku_board.board[i_2, j_2] = tmp

        # We now store the new board into sudoku_board attribute
        self.sudoku_board.board = new_sudoku_board.board


    def solve_puzzle(self):
        '''
        This is the main function that aims to solve the sudoku puzzle.
        '''

        # We store the score for the current sudoku board
        current_score = self.score_puzzle()

        # We also want to keep a copy of the best solution so far
        best_score_solver = sudokuSolver(self.sudoku_board)
        best_score = current_score

        # We define a "temperature" for our system that will allows us to 
        # find the solution via simulated annealing. We set our initial 
        # temperature to .5
        T = 100

        # We also keep count of the current loop so that we may have an exit
        # condition for our while loop in case our random process of finding
        # the solution does not terminate
        i = 0
        
        # Set an upper bound of 50k cycles
        end_loop = False
        while not end_loop:
            
            # We set a hard limit on the amount of loops, since it is still
            # possible to run indefinitely, since this is a random process
            if i >= 1000000:
                end_loop = True


            # Create a new solver which we will use to generate a new board
            # and calculate the new current_score
            new_sudoku_board = sudokuBoard()
            new_sudoku_board.board = self.sudoku_board.board
            new_sudoku_board.clues = self.sudoku_board.clues
            
            # We create a new solver which has a copy of the current 
            # board. We call new_solution() to generate a random permutation
            new_solver = sudokuSolver(new_sudoku_board)
            new_solver.new_solution()

            # Calculate the new score
            new_score = new_solver.score_puzzle()
            
            # Calculate the change between the current_score and the
            # new_score
            score_diff = float(current_score - new_score)
            print("i: ", i , "current_score: ", current_score, " best_score: ", best_score, "new_score: ", new_score, "score_diff: ", score_diff)
            
            # We decide if we keep the result, or reject it. We keep if
            # the probability of such a score difference is larger than
            # a random value [0,1)
            if ((np.exp(score_diff/T) - np.random.random()) > 0):
                
                # We replace our current board with the new one and
                # we also set the current_score to be the new one
                self.sudoku_board = new_solver.sudoku_board
                current_score = new_score
            

            # If we get a better score than the best score, we set our 
            # best_score and our best_score_solver to the new_solver.
            if (current_score < best_score):
                best_score_solver.sudoku_board = self.sudoku_board
                best_score = current_score
            
            

            # We get the outright answer in our new_solver, then we can
            # set it to our best_score_solver and we exit the loop
            if new_score == -162:
                best_score_solver.sudoku_board = new_solver.sudoku_board
                best_score = new_score

                end_loop = True

            # We reduce our temperature by 99%
            T = 0.99999*T
            i += 1

        best_score_solver.sudoku_board.show_board()

if __name__ == '__main__':

    # Testing sudokuBoard setup
    s = sudokuBoard(clues= [(0,0,9), (0,1,1), (0,2,6), (0,3,3), (0,4,4), \
                            (0,6,7), (0,7,8), (1,2,2), (1,6,5), (1,7,6), \
                            (2,0,5), (2,1,3), (2,3,8), (2,4,2), (2,5,6), \
                            (2,6,4), (2,7,1), (3,4,7), (3,8,6), (4,1,9), \
                            (4,2,4), (4,3,2), (4,5,3), (5,0,2), (5,1,7), \
                            (5,7,4), (6,0,1), (6,3,6), (6,5,7), (6,8,4), \
                            (7,2,9), (7,7,3), (8,3,5), (8,4,3), (8,7,2), \
                            (8,8,1)])
    s.show_board()
    solver = sudokuSolver(s)


    # Testing sudokuSolver insertions_left function
    print("__________insertions left__________")
    print(solver.insertions_left())
    print("\n")
    
    # Generating a solution
    print("__________generating solution__________")
    solver.generate_solution()
    print("\n")

    # Testing score_puzzle
    print("__________score puzzle__________")
    print(solver.score_puzzle())
    print("\n")
    
    # Testing show_board
    print("__________show board__________")
    print(solver.sudoku_board.clues)
    s.show_board()

    # Testing new_solution
    print("__________new solution__________")
    solver.new_solution()
    solver.sudoku_board.show_board()

    # Testing solve_puzzle
    print("__________solve puzzle__________")
    solver.solve_puzzle()
    