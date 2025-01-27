import app


class DerDieDasGame(app.tk.Toplevel):
    def __init__(self, geometry=None, parent_window=None):
        super().__init__()

        # Set parent window and geometry if provided and geometry if provided
        # otherwise testing it as a standalone app
        if parent_window:
            self.parent_window = parent_window
            # Lock the parent window
            self.transient(parent_window) # Makes this window a child of the parent window
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


        self.title("Der Die Das Game")

        self.img = app.tk.PhotoImage(file="app-icon.png")
        self.iconphoto(False, self.img)


        self.consent_to_goethe_list = None
        # Game state initialization
        self.priority_list = app.words_to_study("noun")[0]
        self.normal_list = app.words_to_study("noun")[1]
        self.goethe_list = app.words_to_study("noun")[2]
        self.all_lists = [self.priority_list, self.normal_list, self.goethe_list]

        self.info_label = app.ttk.Label(self, text="What is the correct article for")
        self.info_label.grid(row=1, column=2, padx=10, pady=(0,5))

        self.word_label = app.ttk.Label(self, text="Word will appear here", font=("Arial", 18))
        self.word_label.grid(row=2, column=2, padx=10, pady=(50,50))

        self.radio_var = app.tk.StringVar(value="")
        self.correct_article =""

        self.style = app.ttk.Style()
        self.style.configure('Custom.TRadiobutton', font=('Arial', 14))

        self.radio_button_der = app.ttk.Radiobutton(self, text="der", variable=self.radio_var, value="der", style= 'Custom.TRadiobutton')
        self.radio_button_die = app.ttk.Radiobutton(self, text="die", variable=self.radio_var, value="die", style= 'Custom.TRadiobutton')
        self.radio_button_das = app.ttk.Radiobutton(self, text="das", variable=self.radio_var, value="das", style= 'Custom.TRadiobutton')

        self.radio_button_der.grid(row=3, column=1)
        self.radio_button_die.grid(row=3, column=2)
        self.radio_button_das.grid(row=3, column=3)

        self.next_button = app.ttk.Button(self, text="Next", command=self.check_answer)
        self.next_button.grid(row=4, column=2, pady=(70,10))

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(5, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(4, weight=1)

        #self.protocol("WM_DELETE_WINDOW", self.close_window)

        self.next_word()#call it initially to set teh first word adn answers

    def next_word(self):
        # Shuffle each lists
        for lst in self.all_lists:
            app.random.shuffle(lst)
        # Prioritize the lists (priority list first, then normal list, then Goethe list)
        self.radio_var.set("") #reset the radio button=
        if self.priority_list:
            element = self.priority_list.pop()
            line = element.strip().split(', ')
            word_dict = {pair.split(': ')[0]: pair.split(': ')[1] for pair in line}
            current_word = word_dict['Word']
            self.correct_article = word_dict['Article']
            self.word_label.config(text=f"'{current_word}'")

        elif self.normal_list:
            element = self.normal_list.pop()
            line = element.strip().split(', ')
            word_dict = {pair.split(': ')[0]: pair.split(': ')[1] for pair in line}
            current_word = word_dict['Word']
            self.correct_article = word_dict['Article']
            self.word_label.config(text=f"'{current_word}'")
        elif self.goethe_list:
            element = self.goethe_list.pop()
            line = element.strip().split(', ')
            word_dict = {pair.split(': ')[0]: pair.split(': ')[1] for pair in line}
            current_word = word_dict['Word']
            self.correct_article = word_dict['Article']
            self.word_label.config(text=f"'{current_word}'")

            if not self.consent_to_goethe_list:
                self.consent_to_goethe_list = app.messagebox.askyesno("Goethe List", "We are moving to Goethe list", parent=self)
                if not self.consent_to_goethe_list:
                    self.destroy()
        else:
            app.messagebox.showinfo("Game Over", "All nouns have been practiced!")
            self.destroy()

    def check_answer(self):
        user_guess = self.radio_var.get()
        if user_guess == self.correct_article:
            pass
            # app.messagebox.showinfo("Success", "correct ✓")
        else:
            app.messagebox.showerror("Incorrect",f"Incorrect! The correct article is '{self.correct_article}'.", parent=self)
        self.next_word()  # Move to the next word

    # def close_window(self):
    #     """ Close the child window and re-enable the parent window """
    #     if self.master:
    #         # Re-enable interaction with the parent window
    #         self.master.attributes('-disabled', False)
    #     self.destroy()