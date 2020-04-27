"""
Tic Tac Toe Player
"""

import math
import copy 
import numpy as np

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

    n_X = sum(item.count(X) for item in board)
    n_O = sum(item.count(O) for item in board)

    if(n_X == n_O):
        return X
    else:
        return O


def actions(board):
    
    result = set()
    for i,row in enumerate(board):
        for j,col in enumerate(row):
            if col is EMPTY:
                result.add((i,j))

    return result


def result(board, action):

    res_board = copy.deepcopy(board)
    if board[action[0]][action[1]] is EMPTY:
        res_board[action[0]][action[1]] = player(board)
        return res_board
    else:
        raise NameError('Not valid action')     


def winner(board):
    
    player = [X,O]

    for p in player:
        for i in range(0,3):
            if board[i].count(p) == 3:
                return p
            col = list(np.array(board)[:,i])
            if col.count(p) == 3:
                return p

        if board[0][0] == p and board[1][1] == p and board[2][2] == p:
            return p
        if board[0][2] == p and board[1][1] == p and board[2][0] == p:
            return p

    return None


def terminal(board):
    
    n_Empty =  sum(item.count(EMPTY) for item in board)
    if winner(board) is not None or n_Empty == 0:
        return True
    else:
        return False


def utility(board):
    
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0


def minimax(board):
    
    if (player(board) is X):
        return alpha_beta_pruning(board,0,True,-10,+10)[1]
    else:
        return alpha_beta_pruning(board,0,False,-10,+10)[1]

def alpha_beta_pruning (board, depth, isMaximizingPlayer, alpha, beta):

    if terminal(board) :
        return (utility(board),None)
    
    if isMaximizingPlayer :
        bestVal = -10
        bestMov = None
        moves = actions(board)
        for m in moves:
            value = alpha_beta_pruning(result(board,m), depth+1, False, alpha, beta)[0]
            if value > bestVal:
                bestVal = value
                bestMov = m

            alpha = max( alpha, bestVal)
            if beta <= alpha:
                break
        return (bestVal,bestMov)

    else :
        bestVal = 10
        bestMov = None
        moves = actions(board)
        for m in moves:
            value = alpha_beta_pruning(result(board,m), depth+1, True, alpha, beta)[0]
            if value < bestVal:
                bestVal = value
                bestMov = m
    
            beta = min( beta, bestVal)
            if beta <= alpha:
                break
        return (bestVal,bestMov)