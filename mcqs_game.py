from numpy.ma.extras import column_stack

import app
class MCQsGame(app.tk.Toplevel):
    def __init__(self, geometry=None, parent_window=None, combobox=None):
        super().__init__()

        # Set parent window and geometry if provided and geometry if provided
        # otherwise testing it as a standalone app
        if parent_window:
            self.parent_window = parent_window
            # Lock the parent window
            self.transient(parent_window)  # Makes this window a child of the parent window
            self.grab_set()  # Locks the interaction with the parent window until this one is closed

            # OR

            # Disable interaction with the parent window (including preventing movement)
            # The best method but with a closing protocol of this child window
            # parent_window.attributes('-disabled', True)
        else:
            self.parent_window = self

        if geometry:
            self.geometry = self.geometry(geometry)
        else:
            self.geometry = self.geometry("400x300")
        self.title("MCQs Game")

        if combobox:
            self.level = combobox.get()

        self.img = app.tk.PhotoImage(file="app-icon.png")
        self.iconphoto(False, self.img)
        # self.resizable(True, True) # not working due to self.transient propety.

        if self.level not in ["Niveau: A1", "Niveau: A2"]:
            app.messagebox.showinfo("Entschuldigung ", "Entschuldigung ! only level A1 and A2 are available at the moment.")
            self.destroy()
            return


        self.consent_to_goethe_list = None
        # Game state initialization
        self.priority_list = app.words_to_study(self.level, None)[0]
        self.normal_list = app.words_to_study(self.level, None)[1]
        self.goethe_list = app.words_to_study(self.level,None)[2]
        self.all_lists = [self.priority_list, self.normal_list, self.goethe_list]

        self.total_words = self.priority_list + self.normal_list + self.goethe_list
        self.word_dict = {}

        self.meanings_list = []
        for meanings in self.total_words:
            self.split_line = meanings.strip().split(", ")
            self.meaning = [info.split(": ")[1] for info in self.split_line if info.startswith("Meaning")][0]
            self.meanings_list.append(self.meaning)

        self.info_label = app.ttk.Label(self, text="What is the correct meaning of")
        self.info_label.grid(row=1, column=2, padx=10, pady=(0,5))

        self.word_label = app.ttk.Label(self, text="Word will appear here", font=("Helvetica", 20))
        self.word_label.grid(row=2, column=2, padx=(50,50), pady=(50,50))

        self.radio_var = app.tk.StringVar(value="")
        self.correct_meaning =""

        self.style = app.ttk.Style()
        self.style.configure('Custom.TRadiobutton', font=('Helvetica', 14))

        self.radio_var = app.tk.StringVar(value="")
        self.radio_button_o1 = app.ttk.Radiobutton(self, text="", variable=self.radio_var, value="", style= 'Custom.TRadiobutton')
        self.radio_button_o2 = app.ttk.Radiobutton(self, text="", variable=self.radio_var, value="",  style= 'Custom.TRadiobutton')
        self.radio_button_o3 = app.ttk.Radiobutton(self, text="", variable=self.radio_var, value="",  style= 'Custom.TRadiobutton')
        #self.radio_button_o4 = app.ttk.Radiobutton(self, text="", variable=self.radio_var, value="", style= 'Custom.TRadiobutton')

        self.radio_button_o1.grid(row=3, column=1)
        self.radio_button_o2.grid(row=3, column=2)
        self.radio_button_o3.grid(row=3, column=3)
        #self.radio_button_o4.grid(row=4, column=3, sticky='w', pady=10)

        self.next_button = app.ttk.Button(self, text="Next", command=self.check_answer)
        self.next_button.grid(row=4, column=2, pady=(70,10))

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(5, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(4, weight=1)

        self.next_word()

    def next_word(self):
        self.radio_var.set("") #reset the radio button
        if self.priority_list:
            app.random.shuffle(self.priority_list)
            element = self.priority_list.pop()  # Get the next word
            line = element.strip().split(', ')
            word_dict = {pair.split(': ')[0]: pair.split(': ')[1] for pair in line}
            current_word = word_dict['Word']
            current_type = word_dict['Type']
            if current_type.lower() == "noun":
                current_word = word_dict['Article']+" "+current_word
            self.correct_meaning = word_dict['Meaning']
            self.word_label.config(text=f"'{current_word}'")
            choices = app.random.sample(self.meanings_list, 3)
            if self.correct_meaning in choices:
                choices.remove(self.correct_meaning)
            else:
                choices.pop()
            choices.append(self.correct_meaning)
            app.random.shuffle(choices)
            self.radio_button_o1.config(text=choices[0].capitalize(), value=choices[0])
            self.radio_button_o2.config(text=choices[1].capitalize(), value=choices[1])
            self.radio_button_o3.config(text=choices[2].capitalize(), value=choices[2])
            #self.radio_button_o4.config(text=choices[3].capitalize(), value=choices[3])

        elif self.normal_list:
            app.random.shuffle(self.normal_list)
            element = self.normal_list.pop()
            line = element.strip().split(', ')
            word_dict = {pair.split(': ')[0]: pair.split(': ')[1] for pair in line}
            current_word = word_dict['Word']
            current_type = word_dict['Type']
            if current_type.lower() == "noun":
                current_word = word_dict['Article']+" "+current_word
            self.correct_meaning = word_dict['Meaning']
            self.word_label.config(text=f"'{current_word}'")
            choices = app.random.sample(self.meanings_list, 3)
            if self.correct_meaning in choices:
                choices.remove(self.correct_meaning)
            else:
                choices.pop()
            choices.append(self.correct_meaning)
            app.random.shuffle(choices)
            self.radio_button_o1.config(text=choices[0].capitalize(), value=choices[0])
            self.radio_button_o2.config(text=choices[1].capitalize(), value=choices[1])
            self.radio_button_o3.config(text=choices[2].capitalize(), value=choices[2])
            #self.radio_button_o4.config(text=choices[3].capitalize(), value=choices[3])
        elif self.goethe_list:
            # print(self.goethe_list)
            if not self.consent_to_goethe_list:
                self.consent_to_goethe_list = app.messagebox.askyesno("Goethe List", "We are moving to Goethe list")
                if not self.consent_to_goethe_list:
                    self.destroy()
            element = self.goethe_list.pop()
            line = element.strip().split(', ')
            word_dict = {pair.split(': ')[0]: pair.split(': ')[1] for pair in line}
            current_word = word_dict['Word']
            current_type = word_dict['Type']
            if current_type.lower() == "noun":
                current_word = word_dict['Article']+" "+current_word
            self.correct_meaning = word_dict['Meaning']
            self.word_label.config(text=f"'{current_word}'")
            choices = app.random.sample(self.meanings_list, 3)
            if self.correct_meaning in choices:
                choices.remove(self.correct_meaning)
            else:
                choices.pop()
            choices.append(self.correct_meaning)
            app.random.shuffle(choices)
            self.radio_button_o1.config(text=choices[0].capitalize(), value=choices[0])
            self.radio_button_o2.config(text=choices[1].capitalize(), value=choices[1])
            self.radio_button_o3.config(text=choices[2].capitalize(), value=choices[2])
            #self.radio_button_o4.config(text=choices[3].capitalize(), value=choices[3])
        else:
            app.messagebox.showinfo("Game Over", "All words have been practiced!")
            self.destroy()

    def check_answer(self):
        user_guess = self.radio_var.get()

        if user_guess == self.correct_meaning:
            ""
            # messagebox.showinfo("Correct", "Correct")
        else:
            app.messagebox.showinfo("Incorrect", f"Incorrect! The correct answer is '{self.correct_meaning.capitalize()}'.")

        self.next_word()  # Move to the next word



if __name__ == "__main__":
    game = MCQsGame()
    game.mainloop()