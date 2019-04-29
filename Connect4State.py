def xyToArray(row, col):
    """
    Returns a position in the array that represents a given row and column
    """
    return row * 7 + col

class Connect4State:
    """
    Defines a state of Connect4.
    _boardArray is length 42, which represents the 7x6 array
    """
    def __init__(self, boardArray, toMove):
        assert len(boardArray) == 42, "Invalid boardArray length"
        assert toMove == True or toMove == False, "Invalid toMove"
        self._boardArray = boardArray
        self.toMove = toMove

    def __str__(self):
        _str = ""
        for row in range(5, -1, -1):
            for col in range(0, 7):
                _str = _str + str(self._boardArray[xyToArray(row, col)])
            _str = _str + "\n"
        return _str

    def dropPiece(self, col):
        """
        Drops the current player's piece on the board and returns that new Connect4State or False if it's an invalid state
        """
        assert 0 <= col and col <= 6, "Invalid column number outside 0-6"

        if(self.pieceAt(5, col) != None):
            return False

        for row in range(0, 6):
            if(self.pieceAt(row, col) == None):
                return self.setPiece(row, col)

    def setPiece(self, row, col):
        """
        Sets a a row,col to the current player's then returns the new state with the opposite player playing next.
        """
        boardCopy = self._boardArray[:]
        boardCopy[xyToArray(row, col)] = self.toMove
        return Connect4State(boardCopy, not self.toMove)

    def legalMoves(self):
        """
        Returns an array of legal column moves
        """
        moves = []
        for col in range(0, 7):
            if self.dropPiece(col) != False:
                moves.append(col)
        return moves

    def successors(self):
        """
        Returns an array of tuples (column, state) of legal moves and the state that follows them
        """
        return [(move, self.dropPiece(move))
            for move in self.legalMoves()]

    def pieceAt(self, row, col):
        """
        Returns the piece at the given row and column. None, False, or True
        """
        if 0 <= row and row <= 5 and 0 <= col and col <= 6: 
            return self._boardArray[xyToArray(row, col)]
        else:
            return None

    def winner(self):
        """
        Returns if there is a winner. True or False, or None if no winner
        """
        for row in range (0, 6):
            for col in range(0, 7):
                color = self.pieceAt(row, col)
                if color != None:
                    if (self.pieceAt(row + 1, col) == color 
                        and self.pieceAt(row + 2, col) == color 
                        and self.pieceAt(row + 3, col) == color):
                            return color
                    if (self.pieceAt(row, col + 1) == color 
                        and self.pieceAt(row, col + 2) == color 
                        and self.pieceAt(row, col + 3) == color):
                            return color
                    if (self.pieceAt(row + 1, col + 1) == color 
                        and self.pieceAt(row + 2, col + 2) == color 
                        and self.pieceAt(row + 3, col + 3) == color):
                            return color
                    if (self.pieceAt(row + 1, col - 1) == color 
                        and self.pieceAt(row + 2, col - 2) == color 
                        and self.pieceAt(row + 3, col - 3) == color):
                            return color

    def tie(self):
        """
        Returns if the game is in a tie
        """
        return (not (self.winner() == True or self.winner() == False)
            and None not in self._boardArray)
    @staticmethod
    def createEmptyState(toMove):
        return Connect4State([None] * 42, toMove)