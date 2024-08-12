import sys

# ANSI codes for colors
YELLOW = '\033[93m'
RESET = '\033[0m'

# Initialize the board...start with 1 to avoid 0 and O issues...1-9
board = list(range(1, 10))

# winning combinations (rows, columns, diag)
WINNING_COMBINATIONS = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8],[0, 4, 8], [2, 4, 6]]

#print the board
def print_board():
    for i in range(0, 9, 3): # 0, 3, 6
        row = []
        for j in range(3): # 0, 1, 2
            cell = board[i+j] 
            if cell == 'X' or cell == 'O':
                row.append(f"{YELLOW}{cell}{RESET}")
            else:
                row.append(str(cell))
        print(" | ".join(row))
        if i < 6:
            print("---------")
            
'''
1 | 2 | 3
---------
4 | 5 | 6
---------
7 | 8 | 9
'''


# game over check
def is_game_over():
    for combo in WINNING_COMBINATIONS:
        if board[combo[0]] == board[combo[1]] == board[combo[2]]:
            return board[combo[0]]
    if all(isinstance(cell, str) for cell in board):
        return 'Draw'
    return None

# Minimax function
def minimax(depth, is_maximizing, alpha, beta):
    result = is_game_over()
    if result == 'X': # if x wins
        return 1
    elif result == 'O':
        return -1
    elif result == 'Draw':
        return 0

    if is_maximizing: # Turn: Maximizing player
        best_score = -sys.maxsize # negative infinity
        for i in range(9):
            if not isinstance(board[i], str):
                temp = board[i]
                board[i] = 'X'
                score = minimax(depth + 1, False, alpha, beta) #recursive call
                board[i] = temp
                best_score = max(score, best_score)
                alpha = max(alpha, best_score)
                if beta <= alpha:
                    break
        return best_score
    else: # Turn: Minimizing player
        best_score = sys.maxsize
        for i in range(9):
            if not isinstance(board[i], str):
                temp = board[i]
                board[i] = 'O'
                score = minimax(depth + 1, True, alpha, beta) #recursive call
                board[i] = temp
                best_score = min(score, best_score)
                beta = min(beta, best_score)
                if beta <= alpha:
                    break
        return best_score

# Function to get the best move for AI
def get_best_move():
    best_score = -sys.maxsize
    best_move = -1
    for i in range(9):
        if not isinstance(board[i], str):
            temp = board[i]
            board[i] = 'X'
            score = minimax(0, False, -sys.maxsize, sys.maxsize)
            board[i] = temp
            if score > best_score:
                best_score = score
                best_move = i
    return best_move

# Main game loop
print("Welcome to Tic-Tac-Toe!")
print(f"You are {YELLOW}O{RESET}, and the AI is {YELLOW}X{RESET}.")
print("Enter a number from 1-9 to make your move.")

while True:
    print_board()
    
    # Check if the game is over
    result = is_game_over()
    if result:
        if result == 'Draw':
            print("It's a draw!")
        else:
            print(f"{YELLOW}{result}{RESET} wins!")
        break

    # Player's move
    while True:
        try:
            move = int(input("Enter your move (1-9): ")) - 1
            if move < 0 or move > 8:
                print("Invalid move. Please enter a number between 1 and 9.")
            elif isinstance(board[move], str):
                print("That space is already occupied. Try again.")
            else:
                board[move] = 'O'
                break
        except ValueError:
            print("Invalid input. Please enter a number.")

    # Check if the game is over after player's move
    result = is_game_over()
    if result:
        print_board()
        if result == 'Draw':
            print("It's a draw!")
        else:
            print(f"{YELLOW}{result}{RESET} wins!")
        break

    # AI's move
    ai_move = get_best_move()
    board[ai_move] = 'X'
    print(f"AI chooses position {ai_move + 1}")

print("Game over. Thanks for playing!")