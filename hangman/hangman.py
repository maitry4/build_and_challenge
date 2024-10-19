import random
from customtkinter import *
from PIL import Image, ImageTk  # For handling images

class Hangman(CTk):
    def __init__(self):
        super().__init__()

        # Set window title and size
        self.title("Hangman Game")
        self.geometry("900x500")

        # Add a title above the game
        self.title_label = CTkLabel(self, text="Guess the Word to Save the Man!", font=("Arial", 28, "bold"))
        self.title_label.grid(row=0, column=0, columnspan=7, pady=10)

        # List of words to choose from
        self.word_list = ["PYTHON", "CUSTOMTKINTER", "HANGMAN", "DEVELOPER", "PROGRAMMING"]
        self.selected_word = random.choice(self.word_list)  # Randomly select a word
        self.word_length = len(self.selected_word)

        # Variables to store the current state of the game
        self.correct_guesses = ['_'] * self.word_length  # List of underscores for each letter
        self.wrong_guesses = []
        self.guess_left = 8  # Total allowed wrong guesses
        self.hangman_images = [CTkImage(light_image=Image.open(f"hangman_images\\{i}.png"), size=(200, 250)) for i in range(0, 9)] #You might need to modify the image path

        # Hangman's image label (starts with the first image)
        self.image_label = CTkLabel(self, image=self.hangman_images[0], text="")
        self.image_label.grid(row=1, rowspan=7, column=7, pady=10)

        # Label below the hangman's image: "Your hangman would be here."
        self.image_message_label = CTkLabel(self, text="Your hangman would be here.", font=("Arial", 14, "italic"))
        self.image_message_label.grid(row=6, column=7, pady=10)

        # Empty space to adjust layout
        self.space_label = CTkLabel(self, text="    ")
        self.space_label.grid(row=0, column=8, pady=10)

        # Word display
        self.word_label = CTkLabel(self, text=" ".join(self.correct_guesses), font=("Arial", 24))
        self.word_label.grid(row=1, column=0, columnspan=6, pady=10)

        # Info labels (Length, Guesses Left, Wrong Guesses)
        self.length_label = CTkLabel(self, text=f"Length: {self.word_length}", font=("Arial", 16))
        self.length_label.grid(row=2, column=0, padx=5)

        self.guess_left_label = CTkLabel(self, text=f"Guess Left: {self.guess_left}", font=("Arial", 16))
        self.guess_left_label.grid(row=2, column=1, padx=5)

        self.wrong_guess_label = CTkLabel(self, text="Wrong Guess: ", font=("Arial", 16))
        self.wrong_guess_label.grid(row=2, column=2, columnspan=3, padx=5)

        # Configure columns to have equal width
        for col in range(6):
            self.grid_columnconfigure(col, weight=1, uniform="col")

        # Keyboard buttons layout
        self.create_keyboard()

    def create_keyboard(self):
        # Create the keyboard as buttons
        letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        row = 3
        col = 0
        for i, letter in enumerate(letters):
            button = CTkButton(self, text=letter, width=50, height=50, command=lambda l=letter: self.on_key_press(l))
            button.grid(row=row, column=col, padx=5, pady=5)
            col += 1
            if col > 5:  # Move to next row after 6 letters
                col = 0
                row += 1

    def on_key_press(self, letter):
        # Check if the letter is in the word
        if letter in self.selected_word:
            # If correct, update the correct guesses
            for index, char in enumerate(self.selected_word):
                if char == letter:
                    self.correct_guesses[index] = letter
            self.word_label.configure(text=" ".join(self.correct_guesses))  # Update displayed word

            # Check if the player has won (all letters guessed)
            if "_" not in self.correct_guesses:
                self.end_game(win=True)
        else:
            # If wrong, update the wrong guesses and reduce guesses left
            if letter not in self.wrong_guesses:
                self.wrong_guesses.append(letter)
                self.guess_left -= 1
                self.wrong_guess_label.configure(text=f"Wrong Guess: {', '.join(self.wrong_guesses)}")
                self.guess_left_label.configure(text=f"Guess Left: {self.guess_left}")
                
                # Update hangman image based on wrong guess count
                self.image_label.configure(image=self.hangman_images[8 - self.guess_left])

                # Clear the initial message when the first wrong guess occurs
                if self.guess_left < 8:
                    self.image_message_label.configure(text="")

                # Check if the player has lost (no guesses left)
                if self.guess_left == 0:
                    self.end_game(win=False)

    def end_game(self, win):
        if win:
            message = "Congratulations! You've won!"
        else:
            message = f"Game Over! The word was {self.selected_word}."
        
        # Display message and reset game (or quit)
        self.word_label.configure(text=message)
        for widget in self.winfo_children():
            if isinstance(widget, CTkButton):
                widget.configure(state="disabled")  # Disable all buttons after game ends

# Run the application
if __name__ == "__main__":
    app = Hangman()
    app.mainloop()
