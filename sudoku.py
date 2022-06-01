import sys
import os

# Create the gameboard with print function
class GameBoard:

	def __init__(self, difficulty):
		self.grid = self.__create_board(difficulty)
		self.difficulty = difficulty
		self.attempted_verify = False
		self.board_reset = False
		self.solved = False
		self.row_update = 0
		self.column_update = 0
		self.number_update = 0
		self.turns = 0

	
	def __create_board(self, difficulty):
		if (difficulty == 'Easy'):
			board = [
				[6, 2, 5, 7, ' ', 9, 3, 1, 8],
				[4, 7, 8, 3, 5, 1, 2, 6, 9],
				[3, 9, 1, 6, 2, 8, 7, 5, 4],
				[9, 6, 7, ' ', 8, 5, 4, 3, 1],
				[2, 8, 3, 1, 6, 4, 5, 9, 7],
				[1, 5, 4, 9, 7, 3, 8, 2, 6],
				[5, 3, 6, 8, 9, 7, ' ', 4, 2],
				[7, 1, 9, 4, 3, 2, 6, 8, 5],
				[8, 4, 2, 5, 1, 6, 9, 7, 3]
			]
		if (difficulty == 'Medium'):
			board = [
				[8, ' ', ' ', 2, 6, ' ', ' ', ' ', 4],
				[' ', 1, ' ', ' ', 8, 3, ' ', 6, 2],
				[2, 6, ' ', 7, 4, ' ', 1, ' ', ' '],
				[' ', ' ', 6, ' ', 7, 8, 2, 1, ' '],
				[' ', ' ', 4, ' ', 3, 2, ' ', 8, ' '],
				[' ', 2, ' ', ' ', ' ', 9, ' ', ' ', 7],
				[7, 4, ' ', ' ', 1, 6, ' ', 2, ' '],
				[' ', 3, ' ', 8, ' ', 4, ' ', 7, 1],
				[' ', ' ', 1, ' ', 2, 7, ' ', ' ', 6]
			]
		if (difficulty == 'Hard'):
			board = [
				[8, 5, ' ', ' ', ' ', 1, ' ', ' ', 6],
				[' ', ' ', 7, ' ', 6, 4, 1, ' ', ' '],
				[' ', ' ', 4, ' ', 7, ' ', 5, 9, ' '],
				[2, ' ', ' ', ' ', 5, 6, ' ', ' ', 4],
				[6, ' ', ' ', 1, ' ', 9, ' ', 7, ' '],
				[7, ' ', 1, ' ', 4, ' ', ' ', ' ', 9],
				[' ', 1, ' ', 9, ' ', ' ', 4, 6, ' '],
				[' ', 9, 6, ' ', ' ', 8, ' ', ' ', 7],
				[' ', 7, ' ', 6, ' ', ' ', ' ', ' ', 1]
			]
		return board


	def update_board(self, row, column, number):
		self.grid[row][column] = int(number)
		self.row_update = row + 1
		self.column_update = column + 1
		self.number_update = number
		self.turns += 1


	def reset_board(self):
		self.grid = self.__create_board(self.difficulty)
		self.board_reset = True


	def print_board(self):
		print('************* ' + self.difficulty + 'Puzzle ************')
		print('-' * 37)
		for i, row in enumerate(self.grid):
			print(('|' + ' {}   {}   {} |' * 3).format(*[x for x in row]))
			if i == 8:
				print('-' * 37)
			elif i % 3 == 2:
				print('|' + '-' * 35 + '|')
			else:
				print('|' + '           |' * 3)




# Play the game and respond to user input
class SudokuGame:

	def __init__(self):
		self.greeting = {
			'1': self.setup,
			'2': self.quit
		}
		self.setup = {
			'1': self.easy,
			'2': self.medium,
			'3': self.hard
		}
		self.choices = {
			'1': self.enter_number,
			'2': self.verify_puzzle,
			'3': self.solve_puzzle,
			'4': self.reset,
			'5': self.exit
		}


	def display_greeting(self):
		print("""
	---Welcome to Sudoku!---

	Would you like to play?

	-Menu-

	1. Sure
	2. No thanks.

		""")

		
	def display_setup_menu(self):
		print("""
	What level of puzzle would you like?

	-Menu-

	1. Easy
	2. Medium
	3. Hard
		
		""")

	
	def display_main_menu(self):
		print("""
	-Menu-

	Please select an option:
	1. Enter a number
	2. Verify the puzzle is correct
	3. Solve the puzzle
	4. Restart
	5. Exit

		""")


	# Display the greeting to the user and get choice to play or not
	def run(self):
		while True:
			clear_terminal()
			self.display_greeting()
			choice = input('Enter an option: ')
			action = self.greeting.get(choice)
			if action:
				action()
			else:
				self.error(choice)


	# Display the setup menu to the user and get choice
	def setup(self):
		while True:
			clear_terminal()
			self.display_setup_menu()
			choice = input('Enter an option: ')
			action = self.setup.get(choice)
			if action:
				board = action()
				self.play_game(board)
			else:
				self.error(choice)

	# Flow and control of the game
	def play_game(self, board):
		while True:
			clear_terminal()
			board.print_board()
			# If previously updated the board
			if (board.turns > 0 and not board.attempted_verify and not board.board_reset):
				print('\nYou updated row ' + str(board.row_update)
					  + ' and column ' + str(board.column_update)
					  + ' with number ' + str(board.number_update))
			# If previously tried to verify
			if (board.attempted_verify):
				print('\nYou attempted to verify the puzzle and it\'s not correct.')
				board.attempted_verify = False
			# If previously reset board
			if (board.board_reset and not board.solved):
				print('\nYou have reset the board.')
				board.board_reset = False
			# If previously solved the board
			if (board.solved):
				print('\nHere is the solved board.')
				board.solved = False
			self.display_main_menu()
			choice = input('Enter an option: ')
			action = self.choices.get(choice)
			if action:
				action(board)
			else:
				self.error(choice)


	def easy(self):
		return GameBoard('Easy')


	def medium(self):
		return GameBoard('Medium')


	def hard(self):
		return GameBoard('Hard')


	def enter_number(self, board):
		row = get_user_input('row')
		column = get_user_input('column')
		number = get_user_input('number')
		board.update_board(row-1, column-1, number)


	def verify_puzzle(self, board):
		# Checks the board for any blank spaces
		if (any(' ' in sublist for sublist in board.grid)):
			board.attempted_verify = True
			return
		
		# Check each row and return to the main function if not correct
		for row in board.grid:
			if (not check_list(row)):
				board.attempted_verify = True
				return

		# Check each column and return to the main function if not correct
		for column in range(9):
			if (not check_list(extract_column(board.grid, column))):
				board.attempted_verify = True
				return

		# Create each square and return to the main function if not correct
		for row in range(0, 7, 3):
			for column in range(0, 7, 3):
				if (not check_list(extract_square(board.grid, slice(row, row+3), slice(column, column+3)))):
					board.attempted_verify = True
					return

		self.winner(board)


	def winner(self, board):
		clear_terminal()
		print('\n****** Congratulations! You solved this Sudoku puzzle ******')
		print('\nHere is the completed board.\n')
		board.print_board()
		print('\n')
		sys.exit(0)


	def solve_puzzle(self, board):
		if (not board.board_reset):
			self.reset(board)
		empty_cell = get_empty_cell(board.grid)
		if (not empty_cell):
			board.solved = True
			return True
		else:
			row, column = empty_cell
		# Attempt to add each number 1-9 to each space
		for number in range(1, 10):
			if (good_entry(board, number, row, column)):
				board.grid[row][column] = number
				# Recursively call the solve function to fill in all spaces
				if (self.solve_puzzle(board)):
					return True
				# Reset previous number if another occurence is found
				board.grid[row][column] = ' '
				
		return False


	def reset(self, board):
		board.reset_board()


	def quit(self):
		clear_terminal()
		print('\nSorry you don\'t want to play. See you again!\n')
		sys.exit(0)


	def exit(self, board):
		clear_terminal()
		print('\nThank you for playing. Take care!\n')
		sys.exit(0)


	def error(self, choice):
		clear_terminal()
		print('\n{}: is not a valid choice. Please try again.'.format(choice))




# Function that will get the input from the user
def get_user_input(what_input):
	good_input = False
	while (good_input == False):
		value = input('Please enter a ' + what_input + ' (1-9): ')
		good_input = check_user_input(value)
	return int(value)


# Function that will check the user input for correct input
def check_user_input(user_input):
	try:
		value = int(user_input)
	except ValueError:
		print('You did not enter a number. Please try again.')
		return False
	if (value >= 1 and value <= 9):
		return True
	else:
		print('Your number is out of range. Please try again.')
		return False


# Function that takes the sudoku grid and extracts a column
def extract_column(grid, i):
	return [row[i] for row in grid]


# Function that creates a list from a square portion of the grid
def extract_square(grid, row_slice, column_slice):
	result = set()
	for square in grid[row_slice]:
		for n in square[column_slice]:
			result.add(n)
	return result


# Function that checks if the contents of a list match the set 1-9
def check_list(number_set):
	checker = set(range(1, 10))
	if (set(number_set) == checker):
		return True
	else:
		return False


# Function that gets the position of an empty cell for solving
def get_empty_cell(board):
	for row in range(9):
		for column in range(9):
			if (board[row][column] == ' '):
				return row, column
	return False


# Function that checks each row, column, and square for a number to enter
def good_entry(board, number, row, column):
	# Check if number is not in row
	not_in_row = all([number != board.grid[row][j] for j in range(9)])
	if (not_in_row):
		# Check if number is not in column
		not_in_column = all([number != board.grid[i][column] for i in range(9)])
		if (not_in_column):
			# Check if number is not in square
			box_x = 3 * (row//3)
			box_y = 3 * (column//3)
			for i in range(box_x, box_x+3):
				for j in range(box_y, box_y+3):
					if board.grid[i][j] == number:
						return False
			return True
	return False


# Function that will clear the terminal
def clear_terminal():
	os.system('cls' if os.name == 'nt' else 'clear')
		






if __name__ == '__main__':
	SudokuGame().run()