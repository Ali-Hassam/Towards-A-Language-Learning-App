import re
import webbrowser
import spacy
import tkinter as tk
# import ttkbootstrap as tb
from tkinter import messagebox, ttk
from deep_translator import PonsTranslator, GoogleTranslator
from spellchecker import SpellChecker
from datetime import datetime
import string
import random
import der_die_das_game as ddd
import spelling_game as sp
import mcqs_game as mcqs
GermanWords = SpellChecker(language='de')
EnglishWords= SpellChecker(language='en')
user_file="user_words.txt"
# goethe_file_a1="goethe_a1_words.txt"

def read(file_name):
    with open(file_name, mode="r", encoding="utf-8") as file:
        return file.readlines()

def save(word):
    data = read(user_file)
    data.append(word)
    with open(user_file, mode="a", encoding="utf-8") as write_file:
        write_file.write(word)

def get_db_words():
    word_list = []
    for element in read(user_file):
        line = element.strip().split(', ')
        word_dict = {pair.split(': ')[0]: pair.split(': ')[1] for pair in line}
        word_list.append (word_dict['Word'])
    return word_list

# Translation checker
def translation(word):
    pons_meaning = [PonsTranslator(source='de', target='en').translate(word)]
    google_meaning = [GoogleTranslator(source='de', target='en').translate(text=word)]
    all_meanings = set(pons_meaning + google_meaning)
    return all_meanings

nlp = spacy.load("de_core_news_md") #load the spacy model
def artikel(word): #I simplified this function a bit
    doc = nlp(word)
    token = doc[0]
    gender = token.morph.get("Gender")
    gender = gender[0]
    if gender == "Masc":
        return 'der'
    elif gender == "Fem":
        return 'die'
    elif gender == "Neut":
        return 'das'
    else:
        return "Unknown"


# Word Type
def get_type(word): # I extended this function to get the output in a more readable form
    doc = nlp(word)
    token = doc[0]
    type_ = token.pos_
    if type_ == "NOUN":
        return "Noun"
    elif type_ == "VERB":
        return "Verb"
    elif type_ == "ADJ":
        return "Adjective"
    elif type_ == "PRON":
        return "Pronoun"
    elif type_ == 'ADP':
        return "Preposition"
    elif type_ == "DET":
        return "Determiner_or_Article"
    elif type_ == "AUX":
        return "Auxiliary_Verb"
    elif type_ == "ADV":
        return "Adverb"
    else:
        return "Unknown"

# This function returns the list of words that the user will practice/play game of
def words_to_study(level, noun_filter=None):
    if level == "Niveau: A1":
        goethe_file = "goethe_a1_words.txt"
    elif level == "Niveau: A2":
        goethe_file = "goethe_a2_words.txt"
    else:
        goethe_file = "goethe_a2_words.txt"

    database_file = read(user_file)
    goethe_a1_file = read(goethe_file)

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



def disable_btns(win):
    for widget in win.winfo_children():
        if isinstance(widget, (ttk.Button, ttk.Radiobutton, ttk.Entry, ttk.Combobox)):
            widget.config(state="disabled")
def enable_btns(win):
    for widget in win.winfo_children():
        if isinstance(widget, (ttk.Button, ttk.Radiobutton, ttk.Entry, ttk.Combobox)):
            widget.config(state="normal")

# Get the geometry of the windows
def get_geometry(parent_width, parent_height, parent_x, parent_y, window_width, window_height):
    x = int(parent_x + (parent_width / 2) - (window_width / 2))
    y = int(parent_y + (parent_height / 2) - (window_height / 2))
    # the geometry function takes ('widthxHeight+StartX+StartY')
    geometry = f"{window_width}x{window_height}+{x}+{y}"
    return geometry


# Add the new word to the custom library
def add_to_library(new_word, new_meaning, win):
    word = new_word.get()
    meaning = new_meaning.get()
    word_type = get_type(word)

    date = datetime.now().strftime("%d-%m-%Y")
    if word_type and word_type == "Noun":
        gender = artikel(word)
        new_entry = f"Word: {word}, Meaning: {meaning}, Type: {word_type}, Article: {gender}, Date: {date}, Success: {0}\n"

    else:
        new_entry = f"Word: {word}, Meaning: {meaning}, Type: {word_type}, Date: {date}, Success: {0}\n"

    save(new_entry)

    res = messagebox.askyesno(title="Word added", parent=win, message=f"{word.capitalize()} : {meaning.capitalize()} added to the library"f"\n Do you want to add another word?")
    if res:
        get_meaning_btn = win.get_meaning_btn
        get_meaning_btn.config(text='Get meaning')

        new_word.config(state="normal")
        new_word.delete(0, 'end')
        new_word.focus()

        new_meaning.config(state="normal")
        new_meaning.delete(0, 'end')
        new_meaning.config(state="readonly")

    else:
        add_word_button.config(state='normal')
        win.destroy()


# Get a new word from user
## To many checks , optimization required may be "try:catch"
def get_new_word(word,mean,win):
    new_word = word.get().lower()
    get_meaning_btn = win.get_meaning_btn
    if new_word=="":
        messagebox.showerror(title="Error", message="Word can't be empty", parent=win)
        word.focus()

    elif not new_word.strip():
        messagebox.showerror(title="Error", message="Word can't be an empty space", parent=win)
        word.focus()

    elif len(new_word.split())!=1:
        messagebox.showwarning(title="Warning", message="Please add a single word", parent=win)
        word.focus()

    elif any(char.isdigit() for char in new_word):
        messagebox.showwarning(title="Warning", message="Word can not have numbers in it", parent=win)
        word.focus()

    elif all(char in string.punctuation for char in new_word):
        messagebox.showwarning(title="Warning", message="Word can not consists of only punctuation marks", parent=win)
        word.focus()

    elif new_word in get_db_words():
        messagebox.showwarning(title="Achtung!", message=f'"{new_word.capitalize()}" already exists in the library', parent=win)
        word.focus()

    elif GermanWords.unknown([new_word]) and GermanWords.correction(new_word) is not None:
        corrected_word = GermanWords.correction(new_word)

        res = messagebox.askyesno(title="Spelling mistake", message=f"Do you mean: {corrected_word.capitalize()}", parent=win)
        if res:
            word.delete(0, 'end')
            word.insert(0, corrected_word.capitalize())
            word.focus()

        elif len(GermanWords.candidates(new_word))==1:
            messagebox.showwarning(title="No more matches", message="No more matches found. Please check the word again", parent=win)

        else:
            candidates = list(GermanWords.candidates(new_word))
            alt_word_win = tk.Toplevel(win)  # sub-child window of show alternates
            alt_word_win.title("Alternate words")
            alt_word_win.geometry(win.geometry())
            alt_word_win.iconphoto(False, image)
            alt_word_win.grab_set()

            get_meaning_btn.config(state='disable')

            line = tk.Label(alt_word_win, text=f"The close matches of: {new_word.capitalize()}")
            line.grid(row=1, column=1, columnspan=3, pady=20)

            alt_word = tk.StringVar()  # a special tk variable to hold the Radiobutton selection it changes dynamically
            select_alt_word_btn = ttk.Button(alt_word_win,
                                             text= 'OK',
                                             state='disabled',
                                             command= lambda: [word.delete(0,'end'),
                                                               word.insert(0, alt_word.get()),
                                                               get_meaning_btn.config(state='normal'),
                                                               alt_word_win.destroy()])
            rw=2
            cl=1
            for wrd in candidates:
                ttk.Radiobutton(
                            alt_word_win,
                            text = wrd.capitalize(),
                            value = wrd.capitalize(),
                            variable = alt_word,
                            command= lambda:[select_alt_word_btn.config(state='normal')]
                        ).grid(row=rw, column=cl, sticky='ew', padx=20, pady=20)
                cl += 1
                if cl==4: #a way around to place three meanings in one row
                    rw+=1
                    cl=1

            select_alt_word_btn.grid(row=rw+1, column=1, columnspan=3, pady=20)

            alt_word_win.grid_rowconfigure(0, weight=1)
            alt_word_win.grid_rowconfigure(rw+2, weight=1)
            alt_word_win.grid_columnconfigure(0, weight=1)
            alt_word_win.grid_columnconfigure(4, weight=1)

            def alt_word_win_callback():
                get_meaning_btn.config(state='normal')
                alt_word_win.destroy()

            alt_word_win.protocol("WM_DELETE_WINDOW", alt_word_win_callback)
            alt_word_win.mainloop()

    elif GermanWords.unknown([new_word]) and GermanWords.correction(new_word) is None:
        messagebox.showwarning(title="Word does not exist", message="This word does not exist in the dictionary.\nPlease check the word again",parent=win)

    else:
        meanings = translation(new_word)
        if len(meanings) == 1:
            mean.config(state="normal")
            mean.insert(0, list(meanings)[0].capitalize())
            get_meaning_btn.config(text='Add to library')
            word.config(state="readonly")
            mean.config(state="readonly")
        else:
            meaning_win = tk.Toplevel(win) # sub-child window of show alternates
            meaning_win.title("Possible Meanings")
            meaning_win.geometry(win.geometry())
            meaning_win.iconphoto(False, image)
            meaning_win.grab_set()

            get_meaning_btn.config(state="disabled")
            tkinter_meaning_var = tk.StringVar() # a special tk variable to hold the Radiobutton selection it changes dynamically

            line = tk.Label(meaning_win, text=f"The possible meanings of: {new_word.capitalize()}")
            line.grid(row=1, column=1, columnspan=3, pady=20)

            select_meaning_btn = ttk.Button(meaning_win,
                                            text='Select meaning',
                                            padding = (10, 5),
                                            state='disabled',
                                            command=lambda:[mean.config(state="normal"),
                                                            mean.insert(0, tkinter_meaning_var.get()),
                                                            word.config(state="readonly"),
                                                            mean.config(state="readonly"),
                                                            get_meaning_btn.config(state="normal"),
                                                            get_meaning_btn.config(text="Add to library"),
                                                            meaning_win.destroy()])
            rw = 2
            cl = 1
            for meaning in meanings:
                ttk.Radiobutton(
                    meaning_win,
                    text=meaning.capitalize(),
                    value=meaning.capitalize(),
                    variable=tkinter_meaning_var,
                    command= lambda : [select_meaning_btn.config(state="normal")]
                ).grid(row=rw, column=cl, sticky='ew', padx=20, pady=20)
                cl += 1
                if cl == 4:
                    rw += 1
                    cl = 1

            select_meaning_btn.grid(row=rw + 1, column=1, columnspan=3, pady=20)

            meaning_win.grid_rowconfigure(0, weight=1)
            meaning_win.grid_rowconfigure(rw + 2, weight=1)
            meaning_win.grid_columnconfigure(0, weight=1)
            meaning_win.grid_columnconfigure(4, weight=1)

            def meaning_win_callback():
                get_meaning_btn.config(state='normal')
                meaning_win.destroy()

            meaning_win.protocol("WM_DELETE_WINDOW", meaning_win_callback)
            meaning_win.mainloop()



def add_word_window(geom):
    add_word_button["state"]='disabled'
    add_word_win = tk.Toplevel(main_window) #child window of the main_window
    add_word_win.title("Add word")
    add_word_win.geometry(geom)
    add_word_win.iconphoto(False, image)
    add_word_win.grab_set()  # Locks the interaction with the parent window

    word_label = tk.Label(add_word_win, text="New word")
    word_label.grid(row=1, column=1, padx=10, pady=(10,5))
    word_input = ttk.Entry(add_word_win)
    word_input.focus()
    word_input.grid(row=2, column=1, padx=10, pady=(0,25))

    meaning_label = tk.Label(add_word_win, text="Its meaning")
    meaning_label.grid(row=3, column=1, padx=10, pady=(0,5))
    meaning_input = ttk.Entry(add_word_win)
    meaning_input = ttk.Entry(add_word_win, state='disabled')
    meaning_input.grid(row=5, column=1, padx=10, pady=(0,5))


    get_meaning_btn = ttk.Button(add_word_win,
                                 text="Get meaning", padding=(10,5),
                                 command=lambda: [get_new_word(word_input,meaning_input, add_word_win) if get_meaning_btn['text'] == "Get meaning"
                                                  else add_to_library(word_input, meaning_input, add_word_win)]) #add_word_win.destroy()
    get_meaning_btn.grid(row=6, column=1, padx=20, pady=20)

    # Store the get_meaning_btn in the window object to access it in other function
    add_word_win.get_meaning_btn = get_meaning_btn

    # Manipulate the grid to keep the widgets at the center of teh screen
    add_word_win.grid_rowconfigure(0, weight=1)
    add_word_win.grid_rowconfigure(7, weight=1)
    add_word_win.grid_columnconfigure(1, weight=1)

    def add_word_win_callback():
        add_word_button["state"]='normal'
        add_word_win.destroy()

    add_word_win.protocol("WM_DELETE_WINDOW", add_word_win_callback)
    add_word_win.mainloop()

#see your lib
def seeyourlib(geom):
    seeyourlib_win = tk.Toplevel(main_window)
    seeyourlib_win.title("Your Library")
    seeyourlib_win.geometry(geom)
    seeyourlib_win.iconphoto(False, image)
    seeyourlib_win.grab_set()  # Locks the interaction with the parent window

    database_file = read(user_file)
    words_list = []
    for line in database_file:
        entry= {'word': re.search(r"Word: (\w+)", line).group(1) if re.search(r"Word: (\w+)", line) else None,
                'article': re.search(r"Article: (\w+)", line).group(1) if re.search(r"Article: (\w+)", line) else '',
                'meaning': re.search(r"Meaning: ([^,]+)", line).group(1) if re.search(r"Meaning: ([^,]+)",
                                                                                      line) else None,
                'type': re.search(r"Type: (\w+)", line).group(1) if re.search(r"Type: (\w+)", line) else None,
                'date': re.search(r"Date: ([\d-]+)", line).group(1) if re.search(r"Date: ([\d-]+)", line) else None}
        # Extract data using regex and directly store them in the dictionary

        words_list.append(entry)



    # #Adding a scrollable area in Tkinter is a bit tricky and involves several steps
    # #1. Create a canvas to hold the scrollable area
    # # And then add a scrollbar to the canvas becase only canvas widget supports the scrollbar
    canvas = tk.Canvas(seeyourlib_win)
    canvas.pack(side="left", fill="both", expand=True)

    # Create a vertical scrollbar for the canvas
    scrollbar = tk.Scrollbar(seeyourlib_win, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")

    # Configure the canvas to work with the scrollbar
    canvas.configure(yscrollcommand=scrollbar.set)

    #2. Create a frame to hold the content inside the canvas
    scrollable_frame = tk.Frame(canvas)

    ##3. Create a window inside the canvas to contain the contents
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

    ##4. Add content to the scrollable frame
    i=0
    for entry in words_list:
        formatted_entry = f"Word: '{entry['word']}',     Article: '{entry['article']}',     Meaning: '{entry['meaning']}',     Type: '{entry['type']}',     Date: '{entry['date']}'"
        word_label = tk.Label(scrollable_frame, text=formatted_entry)
        word_label.grid(row=i, column=0, pady=5, padx=5, sticky="w")
        i+=1

    # Update the scroll region of the canvas to encompass the entire content
    scrollable_frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

    # Bind mouse wheel to the canvas to scroll
    def on_mouse_wheel(event):
        if event.delta:  # For Windows
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        else:  # For Linux
            canvas.yview_scroll(-1 * event.num, "units")

    canvas.bind_all("<MouseWheel>", on_mouse_wheel)  # For Windows
    canvas.bind_all("<Button-4>", on_mouse_wheel)  # For Linux
    canvas.bind_all("<Button-5>", on_mouse_wheel)  # For Linux


    seeyourlib_win.mainloop()


#Progressbars
def progress_(geom):
    progress_win = tk.Toplevel(main_window)  # child window of the main_window
    progress_win.title("Progress")
    progress_win.geometry(geom)
    progress_win.iconphoto(False, image)
    progress_win.grab_set()  # Locks the interaction with the parent window

    x = 100
    y = 7
    z = 90

    value_label = ttk.Label(progress_win, text=f"Your Overall Progress",font=('Helvetica', 12))
    value_label.grid(column=1, row=1)

    # Create progress bar
    pb = ttk.Progressbar(progress_win, orient='horizontal', mode='determinate', value=x, length=280)
    pb.grid(column=1, row=2, padx=10, pady=20)
    # Label to show progress, directly using the value of x
    value_label = ttk.Label(progress_win, text=f"Your Custom Library: {x}%")
    value_label.grid(column=1, row=3)

    # Create progress bar
    pb = ttk.Progressbar(progress_win, orient='horizontal', mode='determinate', value=y, length=280)
    pb.grid(column=1, row=4, padx=10, pady=20)
    # Label to show progress, directly using the value of x
    value_label = ttk.Label(progress_win, text=f"A1 Goethe List: {y}%")
    value_label.grid(column=1, row=5)

    # Create progress bar
    pb = ttk.Progressbar(progress_win, orient='horizontal', mode='determinate', value=z, length=280)
    pb.grid(column=1, row=6, padx=10, pady=20)
    # Label to show progress, directly using the value of x
    value_label = ttk.Label(progress_win, text=f"A2 Goethe List: {z}%")
    value_label.grid(column=1, row=7)


    progress_win.grid_rowconfigure(0, weight=1)
    progress_win.grid_rowconfigure(8, weight=1)
    progress_win.grid_columnconfigure(0, weight=1)
    progress_win.grid_columnconfigure(2, weight=1)
    progress_win.mainloop()

def open_link(event, url):
    # Open the URL when the link is clicked
    webbrowser.open(url)
def about(geom):
    about_win = tk.Toplevel(main_window)
    about_win.title("About")
    about_win.geometry(geom)
    about_win.iconphoto(False, image)
    about_win.grab_set()  # Locks the interaction with the parent window

    # Create a Text widget for the description with more control
    description_text = (
        "Towards-A-Language-Learning-App is a and interactive language learning platform."
        " Unlike most apps, it allows users to input and track the new words they learn, personalizing the experience to their individual journey. "
        "By integrating user-generated content, the app adapts to your learning style and pace, ensuring that each new word is retained effectively. "
        "Whether you're a beginner or advancing your skills, this app offers a tailored approach to help you achieve fluency in your language of choice.\n\n"
        "This application is developed by Hassam Ali and Zühal Yildirim at Institute for Geographical Information Systems, university of Münster."
    )

    text_widget = tk.Text(about_win, wrap="word", font=("Helvetica", 12), height=15, width=50, pady=10, padx=10)
    text_widget.insert(tk.END, description_text)
    text_widget.config(state=tk.DISABLED)  # Make the text non-editable

    # Adjust line spacing (spacing1 is before each line, spacing2 is between lines)
    text_widget.config(spacing1=5, spacing2=5)
    text_widget.pack(padx=10, pady=10)

    # Create a clickable label
    name_label1 = tk.Label(about_win, text="Hassam Ali", fg="blue", cursor="hand2",
                          font=("Helvetica", 14, "bold"))
    name_label1.pack(pady=10)
    # Bind the click event for the name label to open link
    name_label1.bind("<Button-1>", lambda event: open_link(event,"https://www.ali-hassam.github.io"))

    name_label2 = tk.Label(about_win, text="Zühal Yildirim", fg="blue", cursor="hand2",
                          font=("Helvetica", 14, "bold"))
    name_label2.pack(pady=10)
    # Bind the click event for the name label to open link
    name_label2.bind("<Button-1>", lambda event: open_link(event,"https://github.com/ZuhalYildirim"))
    about_win.mainloop()


if __name__ == "__main__":
    main_window = tk.Tk()
    main_window.title("Language Learning Application by Hassam and Zühal")
    screen_w = main_window.winfo_screenwidth()
    screen_h =main_window.winfo_screenheight()
    main_window.geometry(get_geometry(screen_w, screen_h, 0, 0,screen_w, screen_h))


    # A way around to adjust the widgets at the centre of teh window.
    main_window.grid_rowconfigure(0, weight=1)
    main_window.grid_rowconfigure(5, weight=1)
    main_window.grid_columnconfigure(0, weight=1)
    main_window.grid_columnconfigure(5, weight=1)

    progress = ttk.Progressbar(main_window, orient='horizontal', length=100, mode='determinate')


    #CallBack using protocol #uncomment at the end
    def main_window_callback():
        if messagebox.askokcancel("Quit", "Do you really wish to quit?"):
            main_window.destroy()
    main_window.protocol("WM_DELETE_WINDOW", main_window_callback)


    image = tk.PhotoImage(file="app-icon.png")
    main_window.iconphoto(False, image)

    image_label = ttk.Label(main_window, image=image)
    # image_label.grid(row=1, column=1, columnspan=3, pady=0)
    image_label.grid(row=1, column=2, rowspan=2, pady=100) #btter way

    # styles
    style = ttk.Style()
    # style.theme_use('xpnative') #Windows-XP Theme
    # print(style.theme_use()) #current theme
    style.configure('menu.TButton', font=('Helvetica', 12))
    # style.configure('primary.TButton', font=('Helvetica', 12))

    #About
    info_Button = ttk.Button(main_window, text="About", padding=(10,2), command= lambda: about(get_geometry(main_window.winfo_width(), main_window.winfo_height(), main_window.winfo_x(),main_window.winfo_y(), 800, 500)))#, style='info.Outline.TRadiobutton')
    info_Button.place(relx=0, rely=0, anchor="nw", x=10, y=10) #relx and rely = relative-positions (0-1), anchor: of the label


    #def change_level(event):
        # selected_value = level_var.get()  # Get the selected value from StringVar
        # print(f"Selected Level: {selected_value}") #to be impleemted
    # # Bind the combobox value change event to the function
    # combobox.bind("<<ComboboxSelected>>", change_level)


    levels = ["Niveau: A1", "Niveau: A2", "Niveau: B1", "Niveau: B2"]
    level_var = tk.StringVar()
    # Set a default value for the combobox
    combobox = ttk.Combobox(main_window, values=levels, state="readonly", textvariable=level_var, width=10, height=4, font=("Helvetica", 10))
    combobox.set("Niveau: A1")  # Set default value
    combobox.place(relx=1, rely=0, anchor="ne", x=-10, y=10)


    mcqsBtn = ttk.Button(main_window, text="MCQs", width=20, style='menu.TButton',  command=lambda: mcqs.MCQsGame(
        get_geometry(main_window.winfo_width(), main_window.winfo_height(), main_window.winfo_x(),
                     main_window.winfo_y(), 800, 500), main_window, combobox))
    mcqsBtn.grid(row=3, column=1, pady=10, padx=10, ipady=20, ipadx=10)

    seewordsBtn = ttk.Button(main_window, text="See Your Library", width=20, style='menu.TButton',  command=lambda : seeyourlib(
        get_geometry(main_window.winfo_width(), main_window.winfo_height(), main_window.winfo_x(),
                     main_window.winfo_y(), 800, 500)))
    seewordsBtn.grid(row=4, column=1, pady=10, padx=10, ipady=20, ipadx=10)

    spellingBtn = ttk.Button(main_window, text="Spellings", width=20, style='menu.TButton', command=lambda: sp.SpellingGame(
        get_geometry(main_window.winfo_width(), main_window.winfo_height(), main_window.winfo_x(),
                     main_window.winfo_y(), 800, 500), main_window,combobox))
    spellingBtn.grid(row=3, column=2, pady=10, padx=10, ipady=20, ipadx=10)

    derdiedasBtn = ttk.Button(main_window, text="Articles", width=20, style='menu.TButton', command=lambda: ddd.DerDieDasGame(
        get_geometry(main_window.winfo_width(), main_window.winfo_height(), main_window.winfo_x(),
                     main_window.winfo_y(), 800, 500), main_window,combobox))
    derdiedasBtn.grid(row=3, column=3, pady=10, padx=10, ipady=20, ipadx=10)

    progressBtn = ttk.Button(main_window, text="See Your Progress", width=20, style='menu.TButton', command=lambda: progress_(
        get_geometry(main_window.winfo_width(), main_window.winfo_height(), main_window.winfo_x(),
                     main_window.winfo_y(), 800, 500)))
    progressBtn.grid(row=4, column=3, pady=10, padx=10, ipady=20, ipadx=10)

    add_word_button = ttk.Button(main_window, text="Add New Word", width=20,  style='menu.TButton', command=lambda: add_word_window(
        get_geometry(main_window.winfo_width(), main_window.winfo_height(), main_window.winfo_x(),
                     main_window.winfo_y(), 800, 500)))
    add_word_button.grid(row=4, column=2, pady=10, padx=10, ipady=20, ipadx=10)
    # add_word_button.grid(row=4, column=2, pady=10, padx=10, ipady=10, ipadx=10, sticky="ew")



    main_window.mainloop()
