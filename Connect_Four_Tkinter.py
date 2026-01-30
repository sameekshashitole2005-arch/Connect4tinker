import tkinter as tk
from tkinter import messagebox, simpledialog
import time

ROWS = 6
COLUMNS = 7
DROP_DELAY = 0.05  # animation speed


class ConnectFourGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Connect Four")
        self.root.resizable(False, False)

        # Player names
        self.player1 = simpledialog.askstring("Player 1", "Enter Player 1 name (Red):")
        self.player2 = simpledialog.askstring("Player 2", "Enter Player 2 name (Yellow):")

        if not self.player1:
            self.player1 = "Player 1"
        if not self.player2:
            self.player2 = "Player 2"

        self.current_player = 1
        self.game_over = False

        self.board = [[0 for _ in range(COLUMNS)] for _ in range(ROWS)]

        self.frame = tk.Frame(root, bg="blue")
        self.frame.pack(padx=10, pady=10)

        self.buttons = []
        for r in range(ROWS):
            row_buttons = []
            for c in range(COLUMNS):
                btn = tk.Button(
                    self.frame,
                    width=4,
                    height=2,
                    bg="white",
                    command=lambda col=c: self.drop_piece(col)
                )
                btn.grid(row=r, column=c, padx=5, pady=5)
                row_buttons.append(btn)
            self.buttons.append(row_buttons)

        self.status = tk.Label(
            root,
            text=f"{self.player1}'s Turn (Red)",
            font=("Arial", 14)
        )
        self.status.pack(pady=10)

        self.restart_btn = tk.Button(
            root,
            text="Restart Game",
            font=("Arial", 12),
            command=self.reset_game
        )
        self.restart_btn.pack(pady=5)

    def drop_piece(self, col):
        if self.game_over:
            return

        for target_row in range(ROWS - 1, -1, -1):
            if self.board[target_row][col] == 0:
                self.animate_drop(col, target_row)
                self.board[target_row][col] = self.current_player

                if self.check_winner(self.current_player):
                    self.game_over = True
                    winner = self.player1 if self.current_player == 1 else self.player2
                    messagebox.showinfo("Game Over", f"{winner} Wins!")
                    return

                if self.is_draw():
                    self.game_over = True
                    messagebox.showinfo("Game Over", "It's a Draw!")
                    return

                self.current_player = 2 if self.current_player == 1 else 1
                self.update_status()
                break

    def animate_drop(self, col, target_row):
        color = "red" if self.current_player == 1 else "yellow"
        for r in range(target_row + 1):
            self.buttons[r][col].config(bg=color)
            self.root.update()
            time.sleep(DROP_DELAY)
            if r != target_row:
                self.buttons[r][col].config(bg="white")

    def update_status(self):
        if self.current_player == 1:
            self.status.config(text=f"{self.player1}'s Turn (Red)")
        else:
            self.status.config(text=f"{self.player2}'s Turn (Yellow)")

    def check_winner(self, piece):
        # Horizontal
        for r in range(ROWS):
            for c in range(COLUMNS - 3):
                if all(self.board[r][c + i] == piece for i in range(4)):
                    return True

        # Vertical
        for c in range(COLUMNS):
            for r in range(ROWS - 3):
                if all(self.board[r + i][c] == piece for i in range(4)):
                    return True

        # Diagonal /
        for r in range(ROWS - 3):
            for c in range(COLUMNS - 3):
                if all(self.board[r + i][c + i] == piece for i in range(4)):
                    return True

        # Diagonal \
        for r in range(3, ROWS):
            for c in range(COLUMNS - 3):
                if all(self.board[r - i][c + i] == piece for i in range(4)):
                    return True

        return False

    def is_draw(self):
        return all(self.board[0][c] != 0 for c in range(COLUMNS))

    def reset_game(self):
        self.board = [[0 for _ in range(COLUMNS)] for _ in range(ROWS)]
        self.current_player = 1
        self.game_over = False

        for r in range(ROWS):
            for c in range(COLUMNS):
                self.buttons[r][c].config(bg="white")

        self.update_status()


root = tk.Tk()
app = ConnectFourGUI(root)
root.mainloop()
