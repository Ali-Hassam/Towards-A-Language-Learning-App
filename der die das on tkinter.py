import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
import random

# File paths
user_file = "user_words.txt"
goethe_file_a1 = "goethe_a1_words.txt"


def read(file_name):
    with open(file_name, mode="r", encoding="utf-8") as file:
        return file.readlines()


# This function returns the list of words that the user will practice
def words_to_study(noun_filter=None):
    database_file = read(user_file)
    goethe_a1_file = read(goethe_file_a1)

    priority_list = []
    normal_list = []
    goethe_list = []

    for line in database_file:
        saved_date = line.split("Date:")[1].split(",")[0].strip()
        today = datetime.now().strftime("%d-%m-%Y")
        time_passed = datetime.strptime(today, "%d-%m-%Y") - datetime.strptime(saved_date, "%d-%m-%Y")
        time_passed = time_passed.days

        word_info = line.strip().split(", ")
        word_type = [info.split(": ")[1] for info in word_info if info.startswith("Type:")][0]

        if noun_filter == "noun" and word_type == "Noun":
            if time_passed in {2, 3, 10, 17, 30}:
                priority_list.append(line)
            else:
                normal_list.append(line)
        elif noun_filter is None:
            if time_passed in {2, 3, 10, 17, 30}:
                priority_list.append(line)
            else:
                normal_list.append(line)

    for line in goethe_a1_file:
        word_info = line.strip().split(", ")
        word_type = [info.split(": ")[1] for info in word_info if info.startswith("Type:")][0]

        if noun_filter == "noun" and word_type == "Noun":
            goethe_list.append(line)
        elif noun_filter is None:
            goethe_list.append(line)

    return priority_list, normal_list, goethe_list


def get_random(count, priority_list, normal_list, goethe_list):
    selected_words = []
    # First, select words from the priority list
    selected_words += random.sample(priority_list, min(len(priority_list), count)) if priority_list else []
    remaining_count = count - len(selected_words)

    # Then, fill with words from the normal list
    if remaining_count > 0 and normal_list:
        selected_words += random.sample(normal_list, min(len(normal_list), remaining_count))

    remaining_count = count - len(selected_words)
    # Finally, if there are still remaining words, fill with words from the Goethe list
    if remaining_count > 0 and goethe_list:
        selected_words += random.sample(goethe_list, min(len(goethe_list), remaining_count))
    print(selected_words)
    return selected_words


class DerDieDasGame(tk.Tk):
    def __init__(self, geometry="400x300", parent_window=None):
        super().__init__()

        # Set window geometry
        self.consent = None
        self.geometry(geometry)

        # Set parent window if provided
        if parent_window:
            self.parent_window = parent_window
        else:
            self.parent_window = self

        # Window setup
        self.title("Der Die Das Game")
        self.geometry("400x300")

        # Game state initialization
        self.count = 5  # Number of words per session (can be adjusted)
        self.priority_list = words_to_study("noun")[0]
        self.normal_list = words_to_study("noun")[1]
        self.goethe_list = words_to_study("noun")[2]
        # ---------------------------------- shift to grid from pack requireds
        self.total_words = self.priority_list + self.normal_list
        self. practice_list = get_random(min(self.count, len(self.total_words)), self.priority_list, self.normal_list, [])
# ----------------------------------
        self.word_label = ttk.Label(self, text="Word will appear here", font=("Arial", 14))
        self.word_label.pack(pady=20)

        self.radio_var = tk.StringVar(value="")
        self.radio_button_der = ttk.Radiobutton(self, text="der", variable=self.radio_var, value="der")
        self.radio_button_die = ttk.Radiobutton(self, text="die", variable=self.radio_var, value="die")
        self.radio_button_das = ttk.Radiobutton(self, text="das", variable=self.radio_var, value="das")

        self.radio_button_der.pack()
        self.radio_button_die.pack()
        self.radio_button_das.pack()

        self.next_button = ttk.Button(self, text="Next", command=self.check_answer)
        self.next_button.pack(pady=20)

        self.next_word()

    def next_word(self):
        # Prioritize the lists (priority list first, then normal list, then Goethe list)
        print(self.priority_list)
        if self.priority_list:
            element = self.priority_list.pop()  # Get the next word
            line = element.strip().split(', ')
            word_dict = {pair.split(': ')[0]: pair.split(': ')[1] for pair in line}
            self.current_word = word_dict['Word']
            self.correct_article = word_dict['Article']
            self.word_label.config(text=f"What is the correct article for '{self.current_word}'?")

        elif self.normal_list:
            print(self.normal_list)
            element = self.normal_list.pop()
            line = element.strip().split(', ')
            word_dict = {pair.split(': ')[0]: pair.split(': ')[1] for pair in line}
            self.current_word = word_dict['Word']
            self.correct_article = word_dict['Article']
            self.word_label.config(text=f"What is the correct article for '{self.current_word}'?")
        elif self.goethe_list:
            print(self.goethe_list)
            if not self.consent:
                self.consent = messagebox.askyesno("Goethe List", "We are moving to Goethe list")
                if not self.consent:
                    self.quit()
            element = self.goethe_list.pop()
            line = element.strip().split(', ')
            word_dict = {pair.split(': ')[0]: pair.split(': ')[1] for pair in line}
            self.current_word = word_dict['Word']
            self.correct_article = word_dict['Article']
            self.word_label.config(text=f"What is the correct article for '{self.current_word}'?")
        else:
            messagebox.showinfo("Game Over", "All words have been practiced!")
            self.quit()

    def check_answer(self):
        user_guess = self.radio_var.get()

        if user_guess == self.correct_article:
            ""
            # messagebox.showinfo("Correct", "Correct")
        else:
            messagebox.showinfo("Incorrect", f"Incorrect! The correct article is {self.correct_article}.")

        self.next_word()  # Move to the next word


if __name__ == "__main__":
    game = DerDieDasGame()
    game.mainloop()