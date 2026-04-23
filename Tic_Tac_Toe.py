import tkinter as tk
from tkinter import messagebox, font
import random

class TicTacToe:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Tic Tac Toe")
        self.font = font.Font(family="Arial", size=20)

        self.board = [''] * 9
        self.human = 'X'
        self.ai = 'O'
        self.current_player = self.human

        self.buttons = []
        for i in range(9):
            button = tk.Button(self.root, width=6, height=3, font=self.font,
                               command=lambda x=i: self.handle_click(x))
            button.grid(row=i // 3, column=i % 3, sticky="nsew")
            self.buttons.append(button)

        for i in range(3):
            self.root.grid_rowconfigure(i, weight=1)
            self.root.grid_columnconfigure(i, weight=1)

        self.status = tk.Label(self.root, text=f"Player {self.current_player}'s turn",
                               font=(self.font.cget("family"), 14))
        self.status.grid(row=3, column=0, columnspan=3, sticky="nsew")


        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        game_menu = tk.Menu(menubar, tearoff=0)
        game_menu.add_command(label="New Game", command=self.new_game)
        menubar.add_cascade(label="Game", menu=game_menu)

    def handle_click(self, position):
        if self.board[position] != '' or self.current_player != self.human:
            return

        self.make_move(position, self.human)
        if self.check_win(self.human):
            self.end_game(winner=self.human)
        elif self.check_tie():
            self.end_game(tie=True)
        else:
            self.current_player = self.ai
            self.root.after(500, self.ai_move)

    def ai_move(self):
        best_move = self.find_best_move()
        self.make_move(best_move, self.ai)
        if self.check_win(self.ai):
            self.end_game(winner=self.ai)
        elif self.check_tie():
            self.end_game(tie=True)
        else:
            self.current_player = self.human
            self.status.config(text=f"Player {self.current_player}'s turn")

    def find_best_move(self):
        empty_cells = [i for i, cell in enumerate(self.board) if cell == '']

        for pos in empty_cells:
            self.board[pos] = self.ai
            if self.check_win(self.ai):
                self.board[pos] = ''
                return pos
            self.board[pos] = ''

        for pos in empty_cells:
            self.board[pos] = self.human
            if self.check_win(self.human):
                self.board[pos] = '' 
                return pos
            self.board[pos] = ''

        if 4 in empty_cells:
            return 4

        return random.choice(empty_cells)

    def make_move(self, position, symbol):
        self.buttons[position]['text'] = symbol
        self.buttons[position].config(state='disabled')
        self.board[position] = symbol

    def check_win(self, player):
        win_positions = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ]
        for pos in win_positions:
            if all(self.board[i] == player for i in pos):
                for i in pos:
                    self.buttons[i].config(bg="lightgreen")
                return True
        return False

    def check_tie(self):
        return '' not in self.board

    def end_game(self, winner=None, tie=False):
        for button in self.buttons:
            button.config(state='disabled')
        message = "It's a tie!" if tie else f"Player {winner} wins!"
        messagebox.showinfo("Game Over", message)
        self.status.config(text="Game Over")

    def new_game(self):
        self.board = [''] * 9
        self.current_player = self.human if random.choice([True, False]) else self.ai

        if self.current_player == self.ai:
            self.human, self.ai = self.ai, self.human

        for button in self.buttons:
            button.config(text='', state='active', bg="SystemButtonFace")

        self.status.config(text=f"Player {self.current_player}'s turn")

        if self.current_player == self.ai:
            self.root.after(500, self.ai_move)

if __name__ == "__main__":
    game = TicTacToe()
    game.root.mainloop()
