"""
Tic Tac Toe Player
"""

import math

X = "X"
O = "O"
EMPTY = None



def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    countOfX = 0
    countOfY = 0
    numRows = 3
    numColumns = 3
    for row in range(numRows):
        for column in range(numColumns):
            if board[row][column] == X:
                countOfX += 1
            elif board[row][column] == O:
                countOfY += 1
    return X if countOfX == countOfY else O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = set()
    numRows = 3
    numColumns = 3
    for row in range(numRows):
        for column in range(numColumns):
            if board[row][column] == EMPTY:
                actions.add((row,column))
    return actions
            



def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    newBoard = list.copy(board)
    row,column = action
    if newBoard[row][column] == EMPTY:
        newBoard[row][column] = player(board)
    else:
        raise Exception("SPACE TAKEN")
    return newBoard


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """       
    for symbol in [X,O]:
        for i in range(3):
            # check for horazontal win
            if board[i][0] == board[i][1] == board[i][2] == symbol:
                return symbol
             # check for vertical win
            if board[0][i] == board[1][i] == board[2][i] == symbol:
                return symbol
        # check diagonal win
        if board[0][0] == board[1][1] == board[2][2] == symbol or board[0][2] == board[1][1] == board[2][0] == symbol :
            return symbol

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    return len(actions(board)) == 0


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    theWinner = winner(board)
    if theWinner == X:
        return 1
    if theWinner == O:
        return -1
    else:
        return 0

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    raise NotImplementedError

testBoard = [[O, O, X],
            [X, X, O],
            [O, O, X]]
testAction = (0,2)
print(utility(testBoard))