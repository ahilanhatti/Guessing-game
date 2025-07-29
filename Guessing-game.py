import tkinter as tk
from tkinter import messagebox
import random
import os

# Load word list
def load_words():
    if os.path.exists("words.txt"):
        with open("words.txt", "r") as file:
            return [line.strip().lower() for line in file if line.strip()]
    else:
        return ['apple', 'banana', 'grape', 'orange', 'melon', 'peach']

# Pick a word at random
def choose_word(word_list):
    return random.choice(word_list)

# Main GUI Game Class
class HangmanGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Hangman Game")

        self.word_list = load_words()
        self.reset_game()

        # GUI Elements
        self.word_label = tk.Label(root, text=self.get_display_word(), font=('Arial', 24))
        self.word_label.pack(pady=10)

        self.entry_label = tk.Label(root, text="Enter a letter:")
        self.entry_label.pack()

        self.guess_entry = tk.Entry(root, width=5, font=('Arial', 16))
        self.guess_entry.pack()

        self.guess_button = tk.Button(root, text="Guess", command=self.process_guess)
        self.guess_button.pack(pady=10)

        self.info_label = tk.Label(root, text=f"Guesses left: {self.attempts_left}")
        self.info_label.pack()

        self.guessed_label = tk.Label(root, text="Guessed letters: ")
        self.guessed_label.pack()

    def reset_game(self):
        self.word = choose_word(self.word_list)
        self.guessed_letters = set()
        self.max_attempts = 6
        self.attempts_left = self.max_attempts

    def get_display_word(self):
        return ' '.join([letter if letter in self.guessed_letters else '_' for letter in self.word])

    def process_guess(self):
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

        # Check win
        if all(letter in self.guessed_letters for letter in self.word):
            messagebox.showinfo("You Win!", f"Congratulations! The word was '{self.word}'.")
            self.ask_play_again()

        # Check loss
        elif self.attempts_left == 0:
            messagebox.showinfo("Game Over", f"You lost! The word was '{self.word}'.")
            self.ask_play_again()

    def ask_play_again(self):
        play_again = messagebox.askyesno("Play Again", "Do you want to play again?")
        if play_again:
            self.reset_game()
            self.word_label.config(text=self.get_display_word())
            self.info_label.config(text=f"Guesses left: {self.attempts_left}")
            self.guessed_label.config(text="Guessed letters: ")
        else:
            self.root.quit()

# Run the game
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("640x480")
    game = HangmanGame(root)
    root.mainloop() # this runs endlessly, until the window close button is clicked
