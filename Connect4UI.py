from tkinter import *
from tkinter import messagebox
from Connect4State import Connect4State
from Connect4AI import findNextMove

class Connect4UI(Canvas):
    """
    Interactable canvas for Connect4
    """
    def __init__(self, master):
        Canvas.__init__(self)
        self.configure(width=500, height=450, bg="blue")

        self._state = Connect4State.createEmptyState(False)
        self.redrawState()     
        
        self.bind("<Button-1>", self.colClick)

    def colClick(self, event):
        """
        Canvas click handler
        Drops a piece if it's legal
        """
        col = event.x//72
        if col in self._state.legalMoves():
            self._state = self._state.dropPiece(col)
            self.redrawState()
            self.checkWinner()

            self._state = self._state.dropPiece(findNextMove(self._state))
            self.redrawState()
            self.checkWinner()
    def redrawState(self):
        """
        Redraws state on canvas
        """
        self.delete("all")
        for row in range (0, 6):
            for col in range (0, 7):
                color = "gray"
                piece = self._state.pieceAt(row, col)
                if piece == True:
                    color = "red"
                elif piece == False:
                    color="yellow"

                self.create_oval(col*70+10, 360 - row*70+10, 
                    col*70+70,360 - row*70+70,
                    fill=color,
                    outline="blue")

    def checkWinner(self):
        winner = self._state.winner()
        if winner == True:
            messagebox.showinfo("Winner!", "Red wins!")
            self.newGame()
        elif winner == False:
            messagebox.showinfo("Winner!", "Yellow wins!")
            self.newGame()

        if self._state.tie():
            messagebox.showinfo("Tie!", "Game is a draw!")
            self.newGame()
    
    def newGame(self):
        self._state = Connect4State.createEmptyState(False)
        self.redrawState()

def startConnect4UI():
    """
    Starts interactive Connect4 Game
    """
    root = Tk()
    root.geometry("500x450")
    root.title("CS 480 - Connect4")
    ui = Connect4UI(root)
    ui.grid(row=0, column=0)
    root.mainloop()


