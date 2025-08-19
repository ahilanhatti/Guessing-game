import tkinter as tk
from tkinter import messagebox
import random
import os
import json

SCORE_FILE = "scores.json"

class HangmanGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Hangman Game - Phase 8")

        # Scores persist across sessions
        self.scores = self.load_scores()

        # Categories and difficulties
        self.categories = self.load_categories()
        self.selected_category = tk.StringVar(value=list(self.categories.keys())[0])
        self.difficulties = {"Easy": 8, "Medium": 6, "Hard": 4}
        self.selected_difficulty = tk.StringVar(value="Medium")

        self.setup_category_selection_ui()

    # -------------------------
    # Score handling
    # -------------------------
    def load_scores(self):
        if os.path.exists(SCORE_FILE):
            with open(SCORE_FILE, 'r') as f:
                return json.load(f)
        else:
            return {"wins": 0, "losses": 0}

    def save_scores(self):
        with open(SCORE_FILE, 'w') as f:
            json.dump(self.scores, f)

    def show_stats(self):
        wins = self.scores.get("wins", 0)
        losses = self.scores.get("losses", 0)
        messagebox.showinfo("Game Stats", f"Wins: {wins}\nLosses: {losses}")

    # -------------------------
    # Category + word loading
    # -------------------------
    def load_categories(self):
        categories = {}
        for file in os.listdir():
            if file.endswith('.txt'):
                category_name = file[:-4].capitalize()
                with open(file, 'r') as f:
                    words = [line.strip().lower() for line in f if line.strip()]
                    if words:
                        categories[category_name] = words
        return categories

    # -------------------------
    # UI setup
    # -------------------------
    def setup_category_selection_ui(self):
        self.clear_window()

        tk.Label(self.root, text="Select a Category:", font=('Arial', 16)).pack(pady=5)
        category_menu = tk.OptionMenu(self.root, self.selected_category, *self.categories.keys())
        category_menu.config(font=('Arial', 14))
        category_menu.pack()

        tk.Label(self.root, text="Select Difficulty:", font=('Arial', 16)).pack(pady=5)
        difficulty_menu = tk.OptionMenu(self.root, self.selected_difficulty, *self.difficulties.keys())
        difficulty_menu.config(font=('Arial', 14))
        difficulty_menu.pack()

        tk.Button(self.root, text="Start Game", font=('Arial', 14), command=self.start_game).pack(pady=10)
        tk.Button(self.root, text="View Stats", font=('Arial', 14), command=self.show_stats).pack(pady=5)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    # -------------------------
    # Game logic
    # -------------------------
    def start_game(self):
        self.word = random.choice(self.categories[self.selected_category.get()])
        self.guessed_letters = set()
        self.max_attempts = self.difficulties[self.selected_difficulty.get()]
        self.attempts_left = self.max_attempts

        self.build_game_ui()

        # Bind keyboard input
        self.root.bind("<Key>", self.handle_keypress)

    def build_game_ui(self):
        self.clear_window()

        # Word display
        self.word_label = tk.Label(self.root, text=self.get_display_word(), font=('Arial', 24))
        self.word_label.pack(pady=10)

        # Manual entry (still available if preferred)
        self.entry_label = tk.Label(self.root, text="Enter a letter or use your keyboard:")
        self.entry_label.pack()

        self.guess_entry = tk.Entry(self.root, width=5, font=('Arial', 16))
        self.guess_entry.pack()

        self.guess_button = tk.Button(self.root, text="Guess", command=self.process_guess_from_entry)
        self.guess_button.pack(pady=10)

        # Info labels
        self.info_label = tk.Label(self.root, text=f"Guesses left: {self.attempts_left}")
        self.info_label.pack()

        self.guessed_label = tk.Label(self.root, text="Guessed letters: ")
        self.guessed_label.pack()

        # Canvas for drawing hangman
        self.canvas = tk.Canvas(self.root, width=200, height=250, bg="white")
        self.canvas.pack(pady=10)

        self.draw_base()

    def get_display_word(self):
        return ' '.join([letter if letter in self.guessed_letters else '_' for letter in self.word])

    def process_guess_from_entry(self):
        guess = self.guess_entry.get().strip().lower()
        self.guess_entry.delete(0, tk.END)
        if guess:
            self.process_guess(guess)

    def handle_keypress(self, event):
        """Allow direct keyboard typing."""
        guess = event.char.lower()
        if guess.isalpha() and len(guess) == 1:
            self.process_guess(guess)

    def process_guess(self, guess):
        if len(guess) != 1 or not guess.isalpha():
            return

        if guess in self.guessed_letters:
            messagebox.showinfo("Already guessed", f"You already guessed '{guess}'.")
            return

        self.guessed_letters.add(guess)

        if guess not in self.word:
            self.attempts_left -= 1
            self.draw_hangman()

        self.word_label.config(text=self.get_display_word())
        self.info_label.config(text=f"Guesses left: {self.attempts_left}")
        self.guessed_label.config(text="Guessed letters: " + ', '.join(sorted(self.guessed_letters)))

        if all(letter in self.guessed_letters for letter in self.word):
            self.scores["wins"] += 1
            self.save_scores()
            messagebox.showinfo("You Win!", f"Congratulations! The word was '{self.word}'.")
            self.reset_to_menu()

        elif self.attempts_left == 0:
            self.scores["losses"] += 1
            self.save_scores()
            messagebox.showinfo("Game Over", f"You lost! The word was '{self.word}'.")
            self.reset_to_menu()

    def reset_to_menu(self):
        self.root.unbind("<Key>")  # stop capturing keyboard events
        self.setup_category_selection_ui()

    # -------------------------
    # Drawing methods
    # -------------------------
    def draw_base(self):
        self.canvas.create_line(20, 230, 180, 230)  # base
        self.canvas.create_line(50, 230, 50, 20)    # pole
        self.canvas.create_line(50, 20, 120, 20)    # top beam
        self.canvas.create_line(120, 20, 120, 50)   # rope

    def draw_hangman(self):
        """Draw hangman body parts depending on wrong attempts."""
        parts = self.max_attempts - self.attempts_left

        if parts == 1:  # head
            self.canvas.create_oval(100, 50, 140, 90)
        elif parts == 2:  # body
            self.canvas.create_line(120, 90, 120, 150)
        elif parts == 3:  # left arm
            self.canvas.create_line(120, 100, 90, 130)
        elif parts == 4:  # right arm
            self.canvas.create_line(120, 100, 150, 130)
        elif parts == 5:  # left leg
            self.canvas.create_line(120, 150, 90, 190)
        elif parts == 6:  # right leg
            self.canvas.create_line(120, 150, 150, 190)
        elif parts == 7:  # left eye
            self.canvas.create_line(110, 60, 115, 65)
            self.canvas.create_line(115, 60, 110, 65)
        elif parts == 8:  # right eye
            self.canvas.create_line(125, 60, 130, 65)
            self.canvas.create_line(130, 60, 125, 65)


if __name__ == "__main__":
    root = tk.Tk()
    game = HangmanGame(root)
    root.mainloop()
