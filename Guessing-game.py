import tkinter as tk
from tkinter import messagebox
import random
import os

class HangmanGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Hangman Game with Categories")

        self.categories = self.load_categories()
        self.selected_category = tk.StringVar(value=list(self.categories.keys())[0])

        self.setup_category_selection_ui()

    def load_categories(self):
        """
        Load categories from .txt files in the current directory.
        Each filename (without .txt) is treated as a category.
        """
        categories = {}
        for file in os.listdir():
            if file.endswith('.txt'):
                category_name = file[:-4].capitalize()
                with open(file, 'r') as f:
                    words = [line.strip().lower() for line in f if line.strip()]
                    if words:
                        categories[category_name] = words
        return categories

    def setup_category_selection_ui(self):
        """
        Show dropdown to select category before game starts.
        """
        self.clear_window()

        tk.Label(self.root, text="Select a Category:", font=('Arial', 16)).pack(pady=10)
        category_menu = tk.OptionMenu(self.root, self.selected_category, *self.categories.keys())
        category_menu.config(font=('Arial', 14))
        category_menu.pack()

        tk.Button(self.root, text="Start Game", font=('Arial', 14), command=self.start_game).pack(pady=20)

    def clear_window(self):
        """
        Remove all widgets from the window.
        """
        for widget in self.root.winfo_children():
            widget.destroy()

    def start_game(self):
        """
        Initialize a new game using the selected category.
        """
        self.word = random.choice(self.categories[self.selected_category.get()])
        self.guessed_letters = set()
        self.max_attempts = 6
        self.attempts_left = self.max_attempts

        self.build_game_ui()

    def build_game_ui(self):
        """
        Build the main gameplay interface.
        """
        self.clear_window()

        self.word_label = tk.Label(self.root, text=self.get_display_word(), font=('Arial', 24))
        self.word_label.pack(pady=10)

        self.entry_label = tk.Label(self.root, text="Enter a letter:")
        self.entry_label.pack()

        self.guess_entry = tk.Entry(self.root, width=5, font=('Arial', 16))
        self.guess_entry.pack()

        self.guess_button = tk.Button(self.root, text="Guess", command=self.process_guess)
        self.guess_button.pack(pady=10)

        self.info_label = tk.Label(self.root, text=f"Guesses left: {self.attempts_left}")
        self.info_label.pack()

        self.guessed_label = tk.Label(self.root, text="Guessed letters: ")
        self.guessed_label.pack()

    def get_display_word(self):
        """
        Show the current word with guessed letters revealed.
        """
        return ' '.join([letter if letter in self.guessed_letters else '_' for letter in self.word])

    def process_guess(self):
        """
        Handle a letter guess: validate, update state, refresh UI, check win/loss.
        """
        guess = self.guess_entry.get().strip().lower()
        self.guess_entry.delete(0, tk.END)

        if len(guess) != 1 or not guess.isalpha():
            messagebox.showwarning("Invalid input", "Please enter a single alphabetical letter.")
            return

        if guess in self.guessed_letters:
            messagebox.showinfo("Already guessed", f"You already guessed '{guess}'. Try a different letter.")
            return

        self.guessed_letters.add(guess)

        if guess not in self.word:
            self.attempts_left -= 1

        # Update UI
        self.word_label.config(text=self.get_display_word())
        self.info_label.config(text=f"Guesses left: {self.attempts_left}")
        self.guessed_label.config(text="Guessed letters: " + ', '.join(sorted(self.guessed_letters)))

        if all(letter in self.guessed_letters for letter in self.word):
            messagebox.showinfo("You Win!", f"Congratulations! The word was '{self.word}'.")
            self.setup_category_selection_ui()

        elif self.attempts_left == 0:
            messagebox.showinfo("Game Over", f"You lost! The word was '{self.word}'.")
            self.setup_category_selection_ui()


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("640x480")
    game = HangmanGame(root)
    root.mainloop()
