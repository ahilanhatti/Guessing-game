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
                word = line.strip()
                if word:
                    word_list.append(word.lower())
    else:
        word_list = ['apple', 'banana', 'grape', 'orange', 'melon', 'peach']

    return word_list

def choose_word(word_list):
    """
    Randomly choose a word from the list.
    """
    return random.choice(word_list)

def display_progress(word, guessed_letters):
    """
    Show the current progress with guessed letters and underscores.
    """
    result = ''
    for letter in word:
        if letter in guessed_letters:
            result += letter + ' '
        else:
            result += '_ '
    return result.strip()

def get_valid_guess(guessed_letters):
    """
    Prompt the user for a valid, single alphabetical guess.
    """
    while True:
        guess = input("Guess a letter: ").strip().lower()

        if len(guess) != 1:
            print("Please enter only one letter.")
        elif not guess.isalpha():
            print("Please enter a valid alphabetical character.")
        elif guess in guessed_letters:
            print("You already guessed that letter. Try a different one.")
        else:
            return guess

def play_game(word):
    """
    Run a single round of Hangman with input validation.
    """
    guessed_letters = set()
    max_attempts = 40
    attempts_left = max_attempts

    print("\nLet's play Hangman!")
    print("You have", max_attempts, "tries to guess the word.")
    print(display_progress(word, guessed_letters))

    while attempts_left > 0:
        guess = get_valid_guess(guessed_letters)
        guessed_letters.add(guess)

        if guess in word:
            print("Good guess!")
        else:
            print("Wrong guess.")
            attempts_left -= 1

        print("Word:", display_progress(word, guessed_letters))
        print("Tries left:", attempts_left)

        # Check if word is fully guessed
        if all(letter in guessed_letters for letter in word):
            print("\n🎉 You won! The word was:", word)
            return

    print("\n💀 You lost! The word was:", word)

def main():
    """
    Main loop for playing multiple games.
    """
    word_list = load_words()

    while True:
        word_to_guess = choose_word(word_list)
        play_game(word_to_guess)

        again = input("\nWould you like to play again? (y/n): ").strip().lower()
        if again != 'y':
            print("Thanks for playing! Goodbye.")
            break

if __name__ == "__main__":
    main()
