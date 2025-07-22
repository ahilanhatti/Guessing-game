# Phase 1: Basic Command Line Hangman

def display_progress(word, guessed_letters):
    return ' '.join([letter if letter in guessed_letters else '_' for letter in word])

def play_game():
    word_to_guess = "apple"
    guessed_letters = set()
    max_attempts = 6
    attempts_left = max_attempts

    print("Welcome to Hangman!")
    print(f"You have {attempts_left} incorrect guesses allowed.")
    print(display_progress(word_to_guess, guessed_letters))

    while attempts_left > 0:
        guess = input("Guess a letter: ").lower()

        if guess in guessed_letters:
            print("You already guessed that letter.")
            continue

        guessed_letters.add(guess)

        if guess in word_to_guess:
            print("Good guess!")
        else:
            print("Wrong guess!")
            attempts_left -= 1

        print(f"\n{display_progress(word_to_guess, guessed_letters)}")
        print(f"Guesses left: {attempts_left}")

        if all(letter in guessed_letters for letter in word_to_guess):
            print("\nCongratulations! You guessed the word.")
            break
    else:
        print(f"\nGame Over! The word was '{word_to_guess}'.")

if __name__ == "__main__":
    play_game()
