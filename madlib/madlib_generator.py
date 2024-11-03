from customtkinter import *
import csv
import re

class MadLib(CTk):
    def __init__(self):
        super().__init__()
        self.title("MadLib")
        self.main_menu()
    
    # Step 1: Create main menu
    def main_menu(self):
        self.title_lb = CTkLabel(self, text="Mad Lib!")
        self.title_lb.grid(row=0, column=1, padx=30, columnspan=2)

        self.add_story_btn = CTkButton(self, text="Add Story!", command=self.create_story)
        self.add_story_btn.grid(row=1, column=1, padx=10, pady=10)

        self.existing_story_btn = CTkButton(self, text="Existing Story!", command=self.show_stories)
        self.existing_story_btn.grid(row=1, column=2, padx=10, pady=10)

    # Step 2: Get all Stories
    def show_stories(self):
        """Fetches all the stories from the csv file"""
        # Clear screen and go back to main menu
        self.clear_screen()
        self.main_menu()

        self.clear_screen()

        # Display title
        title_label = CTkLabel(self, text="Existing Stories")
        title_label.grid(row=0, column=1, padx=30, pady=10, columnspan=2)

        # Read stories from the CSV file
        with open("madlib.csv", "r") as file:
            reader = csv.reader(file)
            for idx, row in enumerate(reader):
                if idx != 0:
                    sid, title, story = row
                    # Display each story title with a 'Play' button
                    title_label = CTkLabel(self, text=f"{sid}. {title}")
                    title_label.grid(row=idx, column=0, padx=10, pady=5)

                    play_btn = CTkButton(self, text="Play", command=lambda story=story: self.play(story))
                    play_btn.grid(row=idx, column=1, padx=10, pady=5)
    
    # Step 3: Play Selected Story
    def play(self, story_data):
        """Let's you play the selected story"""
        self.clear_screen()
        placeholders = set(re.findall(r'\[(\w+)\]', story_data))

        self.entry_fields = {}
        row = 0
        for placeholder in placeholders:
            CTkLabel(self, text=f"Enter {placeholder}").grid(row=row, column=0, padx=10, pady=5)
            entry = CTkEntry(self)
            entry.grid(row=row, column=1, padx=10, pady=5)

            # Save entry field for future reference
            self.entry_fields[placeholder] = entry
            row += 1
        # Button to generate completed story
        submit_btn = CTkButton(self, text="See Story", command=lambda: self.show_completed_story(self.entry_fields, story_data))
        submit_btn.grid(row=row, column=1, padx=10, pady=10)
    
    # Step 4: Show completed stories
    def show_completed_story(self, input_fields:dict, story:str):
        """Generate the final story by replacing placeholders with user input."""

        # Replace each placeholder in the story with the input from the corresponding entry field
        for placeholder, entry in input_fields.items():
            user_input = entry.get()  # Get the text from the entry field
            story = story.replace(f"[{placeholder}]", user_input)  # Replace placeholder in the story

        # Clear the screen to display the completed story
        self.clear_screen()

        # Display the completed story
        completed_story_label = CTkLabel(self, text="Your Completed Story!")
        completed_story_label.grid(row=0, column=0, padx=20, pady=10, columnspan=2)

        # Show the final story text in a label, breaking lines as needed
        story_text_label = CTkLabel(self, text=story, wraplength=400, justify="left")
        story_text_label.grid(row=1, column=0, padx=20, pady=20, columnspan=2)

        # Button to go back to the main screen or restart
        back_btn = CTkButton(self, text="Back to Menu", command=self.temp)
        back_btn.grid(row=2, column=0, padx=10, pady=10, columnspan=2)

    # Step 5: Create new story
    def create_story(self):
        """Let's create a new story. By taking story from user."""
        self.clear_screen()

        # Create label and entry for story title
        title_label = CTkLabel(self, text="Enter Story Title")
        title_label.grid(row=0, column=0, padx=10, pady=10)
        self.title_entry = CTkEntry(self, width=300)
        self.title_entry.grid(row=0, column=1, padx=10, pady=10)

        # Create label and entry for story content
        content_label = CTkLabel(self, text="Enter Story Content")
        content_label.grid(row=1, column=0, padx=10, pady=10)
        self.content_entry = CTkEntry(self, width=300, height=150)
        self.content_entry.grid(row=1, column=1, padx=10, pady=10)

        # Button to save story
        save_btn = CTkButton(self, text="Save Story", command=self.save_story)
        save_btn.grid(row=2, column=1, padx=10, pady=10)

    # Step 6: Save Created story
    def save_story(self):
        """Saves created story to the csv."""
        # Get story title and content from entry fields
        story_title = self.title_entry.get()
        story_content = self.content_entry.get()

        # Remove commas and newlines from the story content to avoid CSV format issues
        story_content = re.sub(r"[,\n\r]", "", story_content)

        # Determine the next serial number based on the last entry in the CSV
        try:
            with open("madlib.csv", "r", encoding="utf-8") as file:
                reader = csv.reader(file)
                rows = list(reader)
                if len(rows) > 1:  # Check if there are rows other than the header
                    last_sno = int(rows[-1][0])  # Get the last serial number
                    sno = last_sno + 1
                else:
                    sno = 1  # Start with 1 if no other entries
        except FileNotFoundError:
            # File doesn't exist, start from serial number 1
            sno = 1
        # Append the new story to the CSV file
        with open("madlib.csv", "a", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([sno, story_title, story_content])

    # Step 6.1:Helper For the save story method
    def temp(self):
        self.clear_screen()
        self.main_menu()

    # Step 2.1: Helper for all the methods
    def clear_screen(self):
        # Loop through all widgets and destroy them
        for widget in self.winfo_children():
            widget.destroy()


app = MadLib()
app.mainloop()
