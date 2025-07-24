# Phase 1: Basic Command Line Hangman
import random
import os

def load_words():
    """
    Load words from a file if available, otherwise use a default list.
    """
    word_list = []
    filename = "words.txt"

    if os.path.exists(filename):
        with open(filename, 'r') as file:
            for line in file:
                # Strip whitespace and skip empty lines
                word = line.strip()
                if word:
                    word_list.append(word.lower())
    else:
        # Default word list if file not found
        word_list = ['apple', 'banana', 'grape', 'orange', 'melon', 'peach']

    return word_list

def choose_word(word_list):
    """
    Randomly choose a word from the list.
    """
    return random.choice(word_list)

def display_progress(word, guessed_letters):
    """
    Return a string showing guessed letters and underscores for remaining ones.
    Example: "_ a _ a _ a"
    """
    result = ''
    for letter in word:
        if letter in guessed_letters:
            result += letter + ' '
        else:
            result += '_ '
    return result.strip()

def play_game(word):
    """
    Main game logic for a single round of Hangman.
    """
    guessed_letters = set()
    max_attempts = 30
    attempts_left = max_attempts

    print("\nLet's play Hangman!")
    print("You have", max_attempts, "tries to guess the word.")
    print(display_progress(word, guessed_letters))

    while attempts_left > 0:
        guess = input("\nGuess a letter: ").lower()

        if guess in guessed_letters:
            print("You already guessed that letter. Try another.")
            continue

        guessed_letters.add(guess)

        if guess in word:
            print("Nice! That letter is in the word.")
        else:
            print("Oops! That letter is not in the word.")
            attempts_left -= 1

        print("Word:", display_progress(word, guessed_letters))
        print("Tries left:", attempts_left)

        # Check if all letters have been guessed
        all_guessed = True
        for letter in word:
            if letter not in guessed_letters:
                all_guessed = False
                break

        if all_guessed:
            print("\n🎉 Congratulations! You guessed the word:", word)
            return

    print("\n💀 Game over! The word was:", word)

def main():
    """
    The main loop to play and replay the game.
    """
    word_list = load_words()

    while True:
        word_to_guess = choose_word(word_list)
        play_game(word_to_guess)

        again = input("\nWould you like to play again? (y/n): ").lower()
        if again != 'y':
            print("Thanks for playing! Goodbye.")
            break

if __name__ == "__main__":
    main()
