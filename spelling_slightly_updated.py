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
    # print(selected_words)
    return selected_words


class SpellingGame(tk.Tk):
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
        self.title("Spelling Game")
        self.geometry("400x300")

        # Game state initialization
        self.count = 5  # Number of words per session (can be adjusted)
        self.priority_list = words_to_study()[0]
        self.normal_list = words_to_study()[1]
        self.goethe_list = words_to_study()[2]
        # ---------------------------------- shift to grid from pack requireds
        self.total_words = self.priority_list + self.normal_list
        self.practice_list = get_random(min(self.count, len(self.total_words)), self.priority_list, self.normal_list,
                                        [])
        # ----------------------------------
        self.meaning_label = ttk.Label(self, text="Word will appear here", font=("Arial", 14))
        self.meaning_label.pack(pady=20)

        self.word_var = tk.StringVar(value="")
        self.word_enter = ttk.Entry(self)
        self.word_enter.focus()
        # word_enter.grid(row=2, column=1, padx=10, pady=(0, 25))
        self.word_enter.pack()

        self.next_button = ttk.Button(self, text="Next", command=self.check_answer)
        self.next_button.pack(pady=20)

        self.next_word()

    def next_word(self):
        # Prioritize the lists (priority list first, then normal list, then Goethe list)
        # print(self.priority_list)
        if self.priority_list:
            element = self.priority_list.pop()  # Get the next word
            line = element.strip().split(', ')
            word_dict = {pair.split(': ')[0]: pair.split(': ')[1] for pair in line}
            # print(word_dict)
            self.current_word = word_dict['Word']
            self.correct_meaning = word_dict['Meaning']
            self.word_article = ""
            word_type = word_dict['Type']
            if word_type.lower() == 'noun':
                self.word_article = word_dict['Article']
            self.meaning_label.config(text=f"What is the German word for '{self.correct_meaning}'?")

        elif self.normal_list:
            # print(self.normal_list)
            element = self.normal_list.pop()
            line = element.strip().split(', ')
            word_dict = {pair.split(': ')[0]: pair.split(': ')[1] for pair in line}
            # print(word_dict)
            self.current_word = word_dict['Word']
            self.correct_meaning = word_dict['Meaning']
            self.word_article = ""
            word_type = word_dict['Type']
            if word_type.lower() == 'noun':
                self.word_article = word_dict['Article']
            self.meaning_label.config(text=f"What is the German word for '{self.correct_meaning}'?")
        elif self.goethe_list:
            # print(self.goethe_list)
            if not self.consent:
                self.consent = messagebox.askyesno("Goethe List", "We are moving to Goethe list")
                if not self.consent:
                    self.quit()
            element = self.goethe_list.pop()
            line = element.strip().split(', ')
            word_dict = {pair.split(': ')[0]: pair.split(': ')[1] for pair in line}
            # print(word_dict)
            self.current_word = word_dict['Word']
            self.correct_meaning = word_dict['Meaning']
            self.word_article = ""
            word_type = word_dict['Type']
            if word_type.lower() == 'noun':
                self.word_article = word_dict['Article']
            print(self.current_word, self.correct_meaning, word_type, self.word_article)
            self.meaning_label.config(text=f"What is the German word for '{self.correct_meaning}'?")
        else:
            messagebox.showinfo("Game Over", "All words have been practiced!")
            self.quit()

    def check_answer(self):
        user_spelling = self.word_enter.get()
        user_spelling = user_spelling.split()
        print(f"User spellings: {user_spelling}")

        if self.word_article.lower() in ['der', 'die', 'das']:  # Check if 'gender' exists
            if len(user_spelling) == 2 and user_spelling[1] == self.current_word and user_spelling[0] == self.word_article:
                print(f"Yesss, {self.current_word} is spelled correctly!")
            else:
                if len(user_spelling) < 2:
                    print("Oops, please provide articles for te nouns as well")
                else:
                    if user_spelling[0] != self.word_article:
                        print(f"Oops, the correct article should be '{self.word_article}'")
                    if user_spelling[1] != self.current_word:
                        print(f"Oops, the correct word should be '{self.current_word}'")
        else:
            if user_spelling[0] == self.current_word:
                print(f"Yesss, {self.current_word} is spelled correctly!")
            else:
                print(f"Woops, you wrote it wrongly. The correct spelling is '{self.current_word}'")
            # messagebox.showinfo("Correct", "Correct")
        # else:
        #     messagebox.showinfo("Incorrect", f"Incorrect! The correct article is {self.correct_meaning}.")
        self.current_word = ""
        self.correct_meaning = ""
        self.word_article = ""
        self.next_word()  # Move to the next word

if __name__ == "__main__":
        game = SpellingGame()
        game.mainloop()
