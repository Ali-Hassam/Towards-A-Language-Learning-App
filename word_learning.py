import tkinter as tk
from tkinter import messagebox, ttk, StringVar, OptionMenu
import random
'''
I wanted to create a system which we can set the sessions and learn the word from list but I get stuck while I was trying to implement session loops.
And when we click on learned we will udpdate the goethe list with todays day adn now they can be also word that we can prectice.
'''
goethe_file_a1 = "goethe_a1_words.txt"
goethe_file_a2 = "goethe_a2_words.txt"
    
def read(file_name):
    with open(file_name, mode="r", encoding="utf-8") as file:
        return file.readlines()

def words_to_study():
    goethe_a1_file = read(goethe_file_a1)
    goethe_a2_file = read(goethe_file_a2)
    goethe_a1_list = []
    goethe_a2_list = []
    
    for line in goethe_a1_file:
        word_info = line.strip().split(", ")
        word_dict_a1 = {pair.split(': ')[0]: pair.split(': ')[1] for pair in word_info}
        goethe_a1_list.append(word_dict_a1)
    
    for line in goethe_a2_file:
        parts = line.strip().split('; ')
        word_dict = {pair.split(': ')[0]: pair.split(': ')[1] for pair in parts}
        goethe_a2_list.append(word_dict)
    
    return goethe_a1_list, goethe_a2_list

class WordLearning(tk.Tk):
    def __init__(self, geometry="400x300", parent_window=None):
        super().__init__()

        self.geometry(geometry)
        self.title("Goethe Institute Words Learning")
        self.goethe_a1_list, self.goethe_a2_list = words_to_study()
        self.selected_list = tk.StringVar(value="A1")

        self.ask_list_choice()

    def ask_list_choice(self):
        frame = ttk.Frame(self)
        frame.pack(pady=20)
        label = ttk.Label(frame, text="Please select a Goethe list to start learning:")
        label.pack(pady=10)
        label.grid(row=0, column=0, columnspan=2, pady=10)

        # Dropdown menu options 
        options = [ 
            "10", 
            "15", 
            "20", 
            "25"
        ] 
        # datatype of menu text 
        self.clicked = StringVar() 
        
        # initial menu text 
        self.clicked.set( "10" ) 
        
        radio_button_a1 = ttk.Radiobutton(frame, text="A1 Goethe List", variable=self.selected_list, value="A1")
        radio_button_a2 = ttk.Radiobutton(frame, text="A2 Goethe List", variable=self.selected_list, value="A2")
        
        radio_button_a1.grid(row=1, column=0, padx=10, sticky="w") 
        radio_button_a2.grid(row=1, column=1, padx=10, sticky="e")
        label_words = ttk.Label(frame, text="How many words do you want to learn in one session:")
        label_words.grid(row=2, column=0, columnspan=2, pady=10)
        drop = OptionMenu( frame, self.clicked , *options )
        drop.grid(row=3, column=0, columnspan=2, pady=5)
        start_button = ttk.Button(frame, text="Start Learning", command=self.start_learning)
        start_button.grid(row=4, column=0, columnspan=2, pady=10)

    def start_learning(self):
        for widget in self.winfo_children():
            widget.destroy() 

        self.word_label = ttk.Label(self, text="Word will appear here", font=("Arial", 10), justify="center")
        self.word_label.pack(pady=20)

        self.radio_var = tk.StringVar(value="")
        self.radio_button_yes = ttk.Radiobutton(self, text="I learned the word", variable=self.radio_var, value="yes")
        self.radio_button_no = ttk.Radiobutton(self, text="I need more practice", variable=self.radio_var, value="no")

        self.radio_button_yes.pack()
        self.radio_button_no.pack()

        self.next_button = ttk.Button(self, text="Next", command=self.check_answer)
        self.next_button.pack(pady=20)

        self.next_word()

    def next_word(self):
        list_choice = self.selected_list.get()
        selected_value = int(self.clicked.get()) # I couldn't implement this part. I could't build the logic. In where should we implement this?
        word_info_text = ""
        if list_choice == "A1":
            word_list = self.goethe_a1_list
            word_dict = random.choice(word_list)
            for key, value in word_dict.items():
                word_info_text += f"{key}: {value}\n"
            self.word_label.config(text=word_info_text)
        else:
            word_list = self.goethe_a2_list
            word_dict = random.choice(word_list)
            for key, value in word_dict.items():
                word_info_text += f"{key}: {value}\n"
            self.word_label.config(text=word_info_text)
    def check_answer(self):
        learned = self.radio_var.get()
        if learned == "yes":
            messagebox.showinfo("Info", "This word has sved to practice list!")

            self.next_word()
        else:
            self.next_word()

if __name__ == "__main__":
    game = WordLearning()
    game.mainloop()
