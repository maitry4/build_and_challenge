from customtkinter import *
from PIL import Image
import random
import cv2
import mediapipe as mp

class RockPaperScissorsApp(CTk):  # Inheriting from CTk to create the main application class
    def __init__(self):
        super().__init__()

        self.title("Rock Paper Scissors - Real-Time Play")
        self.geometry("700x350")

        # Set the default image paths
        self.waiting_image_path = "rock_paper_scissors_images\\waiting.jpg"
        self.rock_image_path = "rock_paper_scissors_images\\rock.png"
        self.paper_image_path = "rock_paper_scissors_images\\paper.png"
        self.scissors_image_path = "rock_paper_scissors_images\\scissors.png"

        self.moves = ["rock", "paper", "scissors"]  # Define the possible moves
        self.player_move = None  # To store the player's move

        # Load initial images for computer and player (waiting state)
        self.computer_image = CTkImage(Image.open(self.waiting_image_path), size=(150, 150))
        self.player_image = CTkImage(Image.open(self.waiting_image_path), size=(150, 150))

        # Create labels for Computer and Player Moves
        self.computer_move_label = CTkLabel(self, text="Computer's Move", font=("Arial", 18))
        self.computer_move_label.grid(row=0, column=0, padx=20, pady=10)

        self.player_move_label = CTkLabel(self, text="Your Move", font=("Arial", 18))
        self.player_move_label.grid(row=0, column=2, padx=20, pady=10)

        # Display the initial images for Computer and Player
        self.computer_move_image_label = CTkLabel(self, image=self.computer_image, text="")
        self.computer_move_image_label.grid(row=1, column=0, padx=20, pady=10)

        self.player_move_image_label = CTkLabel(self, image=self.player_image, text="")
        self.player_move_image_label.grid(row=1, column=2, padx=20, pady=10)

        # Camera display on top (real-time hand posture detection)
        self.camera_label = CTkLabel(self, text="Camera Feed (Hand Gesture Detection)", font=("Arial", 16))
        self.camera_label.grid(row=0, column=1, padx=20, pady=10)

        # Placeholder for the camera frame (for real-time hand detection)
        self.camera_frame = CTkLabel(self, text="Camera Feed Here", width=200, height=150, fg_color="gray")
        self.camera_frame.grid(row=1, column=1, padx=20, pady=10)

        # Button to start the 'Show' process (simulating computer's audio cue)
        self.show_button = CTkButton(self, text="Show", command=self.show_move)
        self.show_button.grid(row=2, column=1, pady=20)

        # Result label to show the outcome
        self.result_label = CTkLabel(self, text="", font=("Arial", 20))
        self.result_label.grid(row=3, column=1, pady=10)

        # Start capturing the video feed and detecting the player's move
        self.capture = cv2.VideoCapture(0)
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(max_num_hands=1)
        self.mp_draw = mp.solutions.drawing_utils

        self.update_camera_feed()

    def update_camera_feed(self):
        if not self.is_choice_locked:
            ret, frame = self.capture.read()
            if ret:
                # Convert the image to RGB
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = self.hands.process(rgb_frame)

                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        # Drawing hand landmarks
                        self.mp_draw.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                        # Detecting move
                        self.player_move = self.detect_move(hand_landmarks)
                        if self.player_move:
                            self.update_player_image(self.player_move)

                # Display the camera feed on the label
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame)
                img_tk = CTkImage(img, size=(200, 150))
                self.camera_frame.configure(image=img_tk)
                self.camera_frame.image = img_tk

            self.after(10, self.update_camera_feed)  # Continuously update the feed

    def detect_move(self, hand_landmarks):
        """
        Detect the hand gesture based on the positions of the landmarks.
        Returns 'rock', 'paper', or 'scissors'.
        """
        # Store the y-coordinates of the landmarks for all fingers
        thumb_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.THUMB_TIP].y
        index_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP].y
        middle_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y
        ring_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.RING_FINGER_TIP].y
        pinky_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.PINKY_TIP].y

        # Store the y-coordinates of the base knuckles (for comparison)
        index_mcp = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_MCP].y
        middle_mcp = hand_landmarks.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_MCP].y
        ring_mcp = hand_landmarks.landmark[self.mp_hands.HandLandmark.RING_FINGER_MCP].y
        pinky_mcp = hand_landmarks.landmark[self.mp_hands.HandLandmark.PINKY_MCP].y

        # Logic for Rock (all fingers folded)
        if index_tip > index_mcp and middle_tip > middle_mcp and ring_tip > ring_mcp and pinky_tip > pinky_mcp:
            return "rock"

        # Logic for Paper (all fingers extended)
        if index_tip < index_mcp and middle_tip < middle_mcp and ring_tip < ring_mcp and pinky_tip < pinky_mcp:
            return "paper"

        # Logic for Scissors (index and middle fingers extended, others folded)
        if index_tip < index_mcp and middle_tip < middle_mcp and ring_tip > ring_mcp and pinky_tip > pinky_mcp:
            return "scissors"

        # Default case (if the gesture is unclear)
        return None


    def show_move(self):
        # Simulate computer's random move
        computer_move = random.choice(self.moves)
        self.update_computer_image(computer_move)

        if not self.player_move:  # Check if player made a move
            self.player_move = random.choice(self.moves)

        # Check the result and display the outcome
        result = self.check_winner(self.player_move, computer_move)
        self.result_label.configure(text=result)

        # Delay before resetting the game to waiting state
        self.after(2000, self.reset_game)  # 2-second delay before resetting

    def reset_game(self):
        # Reset both images back to waiting
        self.computer_image = CTkImage(Image.open(self.waiting_image_path), size=(150, 150))
        self.player_image = CTkImage(Image.open(self.waiting_image_path), size=(150, 150))

        self.computer_move_image_label.configure(image=self.computer_image)
        self.player_move_image_label.configure(image=self.player_image)

        # Reset the result label and player's move
        self.result_label.configure(text="")
        self.player_move = None


    def update_computer_image(self, move):
        if move == "rock":
            self.computer_image = CTkImage(Image.open(self.rock_image_path), size=(150, 150))
        elif move == "paper":
            self.computer_image = CTkImage(Image.open(self.paper_image_path), size=(150, 150))
        elif move == "scissors":
            self.computer_image = CTkImage(Image.open(self.scissors_image_path), size=(150, 150))

        self.computer_move_image_label.configure(image=self.computer_image)

    def update_player_image(self, move):
        if move == "rock":
            self.player_image = CTkImage(Image.open(self.rock_image_path), size=(150, 150))
        elif move == "paper":
            self.player_image = CTkImage(Image.open(self.paper_image_path), size=(150, 150))
        elif move == "scissors":
            self.player_image = CTkImage(Image.open(self.scissors_image_path), size=(150, 150))

        self.player_move_image_label.configure(image=self.player_image)

    def check_winner(self, player_move, computer_move):
        if player_move == computer_move:
            return "It's a tie!"
        elif (player_move == "rock" and computer_move == "scissors") or \
             (player_move == "scissors" and computer_move == "paper") or \
             (player_move == "paper" and computer_move == "rock"):
            return "You win!"
        else:
            return "Computer wins!"

if __name__ == "__main__":
    app = RockPaperScissorsApp()
    app.mainloop()
