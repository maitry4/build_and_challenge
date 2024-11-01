from customtkinter import *
import random
from PIL import Image
class Dice(CTk):
    def __init__(self):
        super().__init__()
        self.title("Dice Simulator")
        
        # Load dice images
        self.dice1 = CTkImage(light_image=Image.open("dice_images/dice1.png"), size=(300, 300))
        self.dice2 = CTkImage(light_image=Image.open("dice_images/dice2.png"), size=(300, 300))
        self.dice3 = CTkImage(light_image=Image.open("dice_images/dice3.png"), size=(300, 300))
        self.dice4 = CTkImage(light_image=Image.open("dice_images/dice4.png"), size=(300, 300))
        self.dice5 = CTkImage(light_image=Image.open("dice_images/dice5.png"), size=(300, 300))
        self.dice6 = CTkImage(light_image=Image.open("dice_images/dice6.png"), size=(300, 300))

        # image list to make rolling a 6 tougher
        self.image_list = [self.dice1, self.dice2, self.dice3, self.dice4, self.dice5,
                           self.dice1, self.dice2, self.dice3, self.dice4, self.dice5,
                           self.dice6]  # 6 appears only once
        
        # Label for information
        label = CTkLabel(self, text="Press Enter or click the button")
        label.grid(row=0, padx=10, pady=10)
        # Button to roll the dice
        btn = CTkButton(self, text="Roll The Dice", command=self.roll)
        btn.grid(row=2, padx=10, pady=10)
        # Connect button to the Enter key
        self.bind("<Return>", lambda event: btn.invoke())

    def roll(self):
        # Choose a random die face with modified probabilities
        img = random.choice(self.image_list)
        # Display selected die face
        self.label = CTkLabel(self, text="", image=img)
        self.label.grid(row=1, padx=10, pady=10)

if __name__ == "__main__":
    app = Dice()
    app.mainloop()


