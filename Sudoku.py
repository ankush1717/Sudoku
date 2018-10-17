'''
This program allows the user to interactively play the game of Sudoku.
'''

import sys

class SudokuError(Exception):
    pass

class SudokuMoveError(SudokuError):
    pass 

class SudokuCommandError(SudokuError):
    pass   

class Sudoku:
    '''Interactively play the game of Sudoku.'''

    def __init__(self):
        
        row = []
        board = []
        for i in range(9):
            row.append(0)
        for i in range(9):
            board.append(list(row))
        self.board = board
        
        moves = []
        self.moves = moves
        
        

    def load(self, filename):
        '''Loads a sudoku text file (named filename) into the board object'''
        
        file = open(filename, 'r')
        line_num = -1
        
        for line in file:
            list_of_nums = []
            line_num += 1
            if len(line) != 10:
                raise IOError('Not the correct amount of numbers in line')
            for num in line.strip():
                if int(num) not in range(10):
                    raise IOError('File does not only contain numbers from 0 \
                    to 9')
                list_of_nums.append(int(num))
            self.board[line_num] = list_of_nums
            
        if line_num != 8:
            raise IOError('Not the correct amount of lines in file')
        
        file.close()

    def save(self, filename):
        '''Saves the current board state into a new text file named filename'''
        
        file = open(filename, 'w')
        
        for line in self.board:
            for num in line:
                file.write(str(num))
            file.write('\n')
            
        file.close()    

    def show(self):
        '''Pretty-print the current board representation.'''
        print()
        print('   1 2 3 4 5 6 7 8 9 ')
        for i in range(9):
            if i % 3 == 0:
                print('  +-----+-----+-----+')
            print(f'{i + 1} |', end='')
            for j in range(9):
                if self.board[i][j] == 0:
                    print(end=' ')
                else:
                    print(f'{self.board[i][j]}', end='')
                if j % 3 != 2 :
                    print(end=' ')
                else:
                    print('|', end='')
            print() 
        print('  +-----+-----+-----+')
        print()

    def move(self, row, col, val):
        '''Enters in val into row and col on board. First checks if move is
        legal.'''
        
        if (row not in range(9)) or (col not in range(9)):
            raise SudokuMoveError('Input does not have correct coordinates')
        if self.board[row][col] != 0:
            raise SudokuMoveError('Space entered is occupied')
        if val in self.board[row]:
            raise SudokuMoveError('The number entered is already in this row')
        for i in range(9):
            if self.board[i][col] == val:
                raise SudokuMoveError('The number entered is already in this \
                column')
        
        row_range = int(row / 3)
        col_range = int(col / 3)
        
        for i in range(2):
            for j in range(2):
                if self.board[(row_range * 3) + j][(col_range * 3) + i] == val:
                    raise SudokuMoveError('The number entered is already in \
                    this box')
        
        self.board[row][col] = val
        
        self.moves.append((row, col, val))
        
    def undo(self):
        '''Undoes the last move on the board.'''
        
        last = self.moves.pop()
        self.board[last[0]][last[1]] = 0

    def solve(self):
        '''Starts the loop which will require user input for each command.
        Will take in certain special commands.'''
        
        while True:
            try:
                user_entry = input('Enter a command for the sudoku puzzle: ')
                if user_entry == 'q':
                    break
                elif user_entry == 'u':
                    self.undo()
                elif user_entry[0] == 's':
                    filename = user_entry[2:]
                    self.save(filename)
                elif (len(user_entry) == 3):
                    self.move(int(user_entry[0]) - 1, int(user_entry[1]) - 1, \
                              int(user_entry[2]))
                else:
                    raise SudokuCommandError(user_entry)
                
            except SudokuMoveError as e:
                print(e)
                continue
            
            except SudokuCommandError as e:
                print(e)
                continue
                
            
            self.show()
                
                
                
                
                

if __name__ == '__main__':
    s = Sudoku()

    while True:
        filename = input('Enter the sudoku filename: ')
        try:
            s.load(filename)
            break
        except IOError as e:
            print(e)

    s.show()
    s.solve()

