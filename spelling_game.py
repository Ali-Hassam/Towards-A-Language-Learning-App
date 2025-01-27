import app

class SpellingGame(app.tk.Toplevel):
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


        self.title("Spelling Game")
        self.img = app.tk.PhotoImage(file="app-icon.png")
        self.iconphoto(False, self.img)


        self.consent_to_goethe_list = None
        # Game state initialization
        self.priority_list = app.words_to_study()[0]
        self.normal_list = app.words_to_study()[1]
        self.goethe_list = app.words_to_study()[2]
        self.all_lists = [self.priority_list, self.normal_list, self.goethe_list]

        self.info_label = app.ttk.Label(self, text="What is the correct meaning of")
        self.info_label.grid(row=1, column=2, padx=10, pady=(0,5))

        self.meaning_label = app.ttk.Label(self, text="Word will appear here", font=("Arial", 18))
        self.meaning_label.grid(row=2, column=2, padx=10, pady=(50,50))

        self.word_var = app.tk.StringVar(value="")
        self.current_word =""
        self.correct_meaning = ""
        self.word_article = ""


        self.word_enter = app.ttk.Entry(self)
        self.word_enter.focus()
        self.word_enter.grid(row=3, column=2, padx=10, pady=(0, 25))

        self.next_button = app.ttk.Button(self, text="Next", command=self.check_answer)
        self.next_button.grid(row=4, column=2, pady=50)


        self.info_label = app.ttk.Label(self, text="German nouns always start with a capital letter.")
        self.info_label.grid(row=5, column=1, columnspan=3,  pady=(5,5))
        self.info_label = app.ttk.Label(self, text="On Windows: Alt+142=Ä,  Alt+132=ä,  Alt+153=Ö,  Alt+148=ö,  Alt+129=ü,  Alt+154=Ü,  Alt+225=ß")
        self.info_label.grid(row=6, column=1, columnspan=3,  pady=(5,5))

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(5, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(4, weight=1)

        self.next_word()

    def next_word(self):
        # Shuffle each lists
        for lst in self.all_lists:
            app.random.shuffle(lst)
        self.word_enter.delete(0,'end')
        # Prioritize the lists (priority list first, then normal list, then Goethe list)
        if self.priority_list:
            element = self.priority_list.pop()  # Get the next word
            line = element.strip().split(', ')
            word_dict = {pair.split(': ')[0]: pair.split(': ')[1] for pair in line}
            self.current_word = word_dict['Word']
            self.correct_meaning = word_dict['Meaning']
            self.word_article = ""
            word_type = word_dict['Type']
            if word_type.lower() == 'noun':
                self.word_article = word_dict['Article']
            self.meaning_label.config(text=f"'{self.correct_meaning.capitalize()}'")

        elif self.normal_list:
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
            self.meaning_label.config(text=f"'{self.correct_meaning.capitalize()}'")
        elif self.goethe_list:
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
            self.meaning_label.config(text=f"'{self.correct_meaning.capitalize()}'")
            if not self.consent_to_goethe_list:
                self.consent_to_goethe_list = app.messagebox.askyesno("Goethe List", "We are moving to Goethe list")
                if not self.consent_to_goethe_list:
                    self.destroy()
        else:
            app.messagebox.showinfo("Game Over", "All words have been practiced!")
            self.destroy()

    def check_answer(self):
        user_spelling = self.word_enter.get()
        user_spelling = user_spelling.split()
        if len(user_spelling) == 0:
            app.messagebox.showwarning("Warning", "Please provide something to check. Don't mess around!")
        else:
            if self.word_article.lower() in ['der', 'die', 'das']:
                if len(user_spelling) == 2:
                    if user_spelling[0].lower() == self.word_article.lower() and user_spelling[1] == self.current_word:
                        pass
                    elif user_spelling[0].lower() != self.word_article.lower() and user_spelling[1] != self.current_word:
                        app.messagebox.showerror("Wrong Word and Article",
                                             f"The correct word with article is '{self.word_article} {self.current_word.capitalize()}'")
                    elif user_spelling[0].lower() == self.word_article.lower() and user_spelling[1] != self.current_word:
                        app.messagebox.showerror("Wrong Word", f"Article is correct. But, the correct word is '{self.current_word.capitalize()}'")

                    elif user_spelling[0].lower() != self.word_article.lower() and user_spelling[1] == self.current_word:
                        app.messagebox.showwarning("Wrong Article",
                                             f"The word is correct. But the correct article for '{self.current_word.capitalize()}' is '{self.word_article}'")

                else:
                    if user_spelling[0].lower() == self.word_article.lower():
                        app.messagebox.showerror("Correct Article",
                                                f"The article '{self.word_article}' is correct, but the word should be '{self.current_word}'.")
                    elif user_spelling[0] == self.current_word:
                        app.messagebox.showwarning("Missing Article", "Correct word but missing article.\nPlease provide the article for the nouns as well.")

                    else:
                        app.messagebox.showerror("Wrong Word and Article", "The word or article provided is incorrect.")


            else:
                if len(user_spelling) == 1:
                    if user_spelling[0].lower() == self.current_word.lower():
                        pass  # Correct input, do nothing
                    else:
                        app.messagebox.showerror("Wrong Word", f"The correct word is '{self.current_word.capitalize()}'")
                elif len(user_spelling) > 1:
                    if user_spelling[0].lower() == self.current_word.lower():
                        pass
                    else:
                        app.messagebox.showerror("Wrong Word", f"The correct word is '{self.current_word.capitalize()}'")

        self.current_word = ""
        self.correct_meaning = ""
        self.word_article = ""
        self.next_word()  # Move to the next word

# if __name__ == "__main__":
#         game = SpellingGame()
#         game.mainloop()
