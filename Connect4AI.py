from Connect4State import Connect4State
import random
def findNextMove(state):
    """
    Uses Minimax with alphabeta pruning to determine next move
    """
    return alphabeta_search(state, 3)

def isTerminal(state):
    """
    Returns if this state is a leaf in the state tree
    """
    return state.winner() == True or state.winner() == False or state.tie()

BigInitialValue = 1000000
def alphabeta_search(state, depthLimit):
    player = state.toMove
    """
    Does an minimax alphabeta search
    depthLimit determines how deep to search before stopping
    Borrowed from Othello project
    """

    def max_value(state, alpha, beta, depth):
        if isTerminal(state) or depth == 0:
            return calculate_utility(state, player)
        v = -BigInitialValue
        for (a, s) in state.successors():
            v = max(v, min_value(s, alpha, beta, depth - 1))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def min_value(state, alpha, beta, depth):
        if isTerminal(state) or depth == 0:
            return calculate_utility(state, player)
        v = BigInitialValue
        for (a, s) in state.successors():
            v = min(v, max_value(s, alpha, beta, depth - 1))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    # Body of alphabeta_search starts here:
    action, state = argmax(state.successors(),
#                           lambda ((a, s)): min_value(s, -BigInitialValue, BigInitialValue))
                            lambda a_s: min_value(a_s[1], -BigInitialValue, BigInitialValue, depthLimit))
    return action

def calculate_utility(state, player):
    """
    Calculates the utility of a Connect4 state then returns it
    """
    thisPlayer = player
    
    if state.winner() == (not thisPlayer):
        return -BigInitialValue
    if state.winner() == thisPlayer:
        return BigInitialValue
    return calculate_possible_fours(state, thisPlayer) - calculate_possible_fours(state, not thisPlayer)

def calculate_possible_fours(state, player):
    possible = 0
    for row in range (0, 6):
        for col in range(0, 7):
            color = state.pieceAt(row, col)
            if color == player:
                enemy = not player
                if (state.pieceAt(row + 1, col) != enemy
                    and state.pieceAt(row + 2, col) != enemy 
                    and state.pieceAt(row + 3, col) != enemy):
                        possible = possible + 1
                if (state.pieceAt(row, col + 1) != enemy
                    and state.pieceAt(row, col + 2) != enemy 
                    and state.pieceAt(row, col + 3) != enemy):
                        possible = possible + 1
                if (state.pieceAt(row + 1, col + 1) != enemy
                    and state.pieceAt(row + 2, col + 2) != enemy 
                    and state.pieceAt(row + 3, col + 3) != enemy):
                        possible = possible + 1
                if (state.pieceAt(row + 1, col - 1) != enemy
                    and state.pieceAt(row + 2, col - 2) != enemy 
                    and state.pieceAt(row + 3, col - 3) != enemy):
                        possible = possible + 1
    return possible
                            
def argmin(seq, fn):
    """Return an element with lowest fn(seq[i]) score; tie goes to first one.
    >>> argmin(['one', 'to', 'three'], len)
    'to'
    Borrowed from Othello project
    """
    best = seq[0]; best_score = fn(best)
    for x in seq:
        x_score = fn(x)
        if x_score < best_score:
            best, best_score = x, x_score
    return best


def argmax(seq, fn):
    """Return an element with highest fn(seq[i]) score; tie goes to first one.
    >>> argmax(['one', 'to', 'three'], len)
    'three'
    Borrowed from Othello project
    """
    return argmin(seq, lambda x: -fn(x))