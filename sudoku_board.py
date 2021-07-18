import numpy as np

class sudokuBoard():

    def __init__(self, clues = list):

        # We represent the board as a 9x9 numpy array of zeros
        self.board = np.zeros((9,9), dtype=int)
        self.clues = clues

        # We update the board with the given clues that are given as tuples
        # of size 3, for the row, column, and value.
        for clue in self.clues:
            self.board[clue[0],clue[1]] = clue[2]
    
    # Rudimentary visualization of sudoku board
    def show_board(self):
        '''
        prints out a human-readable visualization of the board
        '''
        print("_______________________________________________")

        for i in range(9):
            print('| ', self.board[i,0], '| ', self.board[i,1], '| ', \
                    self.board[i,2], '|| ', self.board[i,3], '| ', \
                    self.board[i,4], '| ', self.board[i,5], '|| ', \
                    self.board[i,6], '| ', self.board[i,7], '| ', \
                    self.board[i,8], ' |')
            if i == 2 or i == 5:
                print(" _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _")
                
        print("_______________________________________________")


    def local_grid(self, row, column):
        '''
        Gets the grid that immediately encompasses the point (row, column)
        '''
        row_values = 0
        column_values = 0
        
        # If the row value for is in one of three blocks of the puzzle board
        # we use the respective values for the row entries
        if 0 <= row <= 2:
            row_values = [0, 1, 2]
        elif 3 <= row <= 5:
            row_values = [3, 4, 5]
        else:
            row_values = [6, 7, 8]

        # Likewise we see which block the column value lives in and return 
        # the respective values for the column entries
        if 0 <= column <= 2:
            column_values = [0, 1, 2]
        elif 3 <= column <= 5:
            column_values = [3, 4, 5]
        else:
            column_values = [6, 7, 8]

        # We now compile a numpy array for the grid 
        grid = np.array([self.board[row_values[0],column_values[0]],
                        self.board[row_values[0],column_values[1]],
                        self.board[row_values[0],column_values[2]],
                        self.board[row_values[1],column_values[0]],
                        self.board[row_values[1],column_values[1]],
                        self.board[row_values[1],column_values[2]],
                        self.board[row_values[2],column_values[0]],
                        self.board[row_values[2],column_values[1]],
                        self.board[row_values[0],column_values[2]]])
        
        return grid

    # Returns True or False if a hypothetical insert of value into
    # (row,column) is valid or not
    def valid_insert(self, row, column, value):
        '''
        Returns True or False if a hypothetical insert of value into
        (row,column) is valid or not
        '''

        grid = self.local_grid(row, column)

        # We create a numpy array for the column extending from (row,column)
        column = np.array([self.board[0,column], self.board[1,column], \
                self.board[2,column], self.board[3,column], \
                self.board[4,column], self.board[5,column], \
                self.board[6,column], self.board[7,column], \
                self.board[8,column]])

        if value not in self.board[row] and value not in column \
            and value not in grid:
            return True
        else:
            return False

    
    def available_inserts(self):
        '''
        Returns a list of tuples that represent slots in the sudoku
        board that are available for insert
        '''

        result = np.where(self.board == 0)

        return list(zip(result[0],result[1]))

if __name__ == '__main__':

    # Testing sudoku board creation
    s = sudokuBoard(clues= [(0,0,5), (1,2,9), (4,5,8), (0,1,4), (0,3,1), (2,4,7)])
    s.show_board()
    print("\n")
    
    # Testing local_grid function for top left and top middle grids
    print("Testing local grid function")
    print("_____________________________________________________________________")
    print(s.local_grid(0,1))
    print(s.local_grid(2,4))
    print("\n")
    
    # Testing valid_insert function
    print("Testing valid insertions")
    print("_____________________________________________________________________")
    print("5 at (0,2): ", s.valid_insert(0, 2, 5))
    print("5 at (1,0): ", s.valid_insert(1, 0, 5))
    print("5 at (1,1): ", s.valid_insert(1, 1, 5))
    print("4 at (0,2): ", s.valid_insert(0, 2, 4))
    print("3 at (0,2): ", s.valid_insert(0, 2, 3))
    print("5 at (8,0): ", s.valid_insert(8, 0, 5))
    print("2 at (8,2): ", s.valid_insert(8, 2, 2))
    print("7 at (0,5): ", s.valid_insert(0, 5, 7))
    print("\n")

    # Testing available inserts
    print("Available locations for new inserts")
    print("_____________________________________________________________________")
    print(s.available_inserts())