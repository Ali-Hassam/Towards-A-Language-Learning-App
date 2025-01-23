import spacy
import tkinter as tk
from tkinter import messagebox,ttk
from deep_translator import PonsTranslator, GoogleTranslator
from spellchecker import SpellChecker

GermanWords = SpellChecker(language='de')
EnglishWords= SpellChecker(language='en')
user_file="user_inputs.txt"
goethe_file="user_inputs.txt"

# Get the geometry of the windows
def get_geometry(parent_width, parent_height, parent_x, parent_y, window_width, window_height):
    x = int(parent_x + (parent_width / 2) - (window_width / 2))
    y = int(parent_y + (parent_height / 2) - (window_height / 2))
    # the geometry function takes ('widthxHeight+StartX+StartY')
    # geometry = '%dx%d+%d+%d' % (window_width, window_height, x, y)
    geometry = f"{window_width}x{window_height}+{x}+{y}"
    return geometry


# Backend functions - Zühal
# -----------------------------------------------------------------------------


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
    for element in read("user_inputs.txt"):
        line = element.strip().split(', ')
        word_dict = {pair.split(': ')[0]: pair.split(': ')[1] for pair in line}
        word_list.append (word_dict['word'])
    return word_list

# Translation checker
def translation(word):
    pons_translation = PonsTranslator(source='de', target='en').translate(word)
    google_translation = GoogleTranslator(source='de', target='en').translate(text=word)
    if pons_translation != google_translation:
        pons_translation = [google_translation, pons_translation]
    return pons_translation


nlp = spacy.load("de_core_news_md")


def artikel(word):
    artikels = {
        "masculine": {
            "definite": "der",
            "indefinite": "ein"
        },
        "feminine": {
            "definite": "die",
            "indefinite": "eine"
        },
        "neuter": {
            "definite": "das",
            "indefinite": "ein"
        },
        "plural": {
            "definite": "die",
            "indefinite": None
        }
    }

    doc = nlp(word)
    token = doc[0]
    gender = token.morph.get("Gender")
    gender = gender[0]
    if gender == "Masc":
        return artikels["masculine"]["definite"]
    elif gender == "Fem":
        return artikels["feminine"]["definite"]
    elif gender == "Neut":
        return artikels["neuter"]["definite"]
    else:
        return "Maybe this is not a nounn "


# And now we also have the type writer
def get_type(word):
    doc = nlp(word)
    for token in doc:
        return token.pos_
# -------------------------------------------------------------



# Add the new word to the custom library
def add_to_library(new_word, meaning):
    
    
    add_word_button["state"]='normal'
    # Zuhal Please implement/modify the function to add the word into the library (text or JSON file) here
    saved_words = get_db_words()
    if new_word not in saved_words:
        messagebox.showinfo(title="Word added", message=f"{new_word} : {meaning} \nadded to the library")
    #     new_entry = {
    #                 "word": new_word,
    #                 "meaning": meaning.capitalize()
    #                 }
    #     save(new_entry)
    #     messagebox.showinfo(title="Word added", message=f"{new_word} added to the library")
    # else:
    #     messagebox.showinfo(title="Word added", message=f"{new_word} already exist the library")



# Get a new word from user
## To many checks , optimization required may be "try:catch"
def get_new_word(word, win):
    new_word = word.get().lower()
    # new_meaning = meaning.get().lower()

    # with open(db_file, mode="r", encoding="utf-8") as read_file:
    #     database_file = json.load(read_file)
    #     word_list = []
    #     for i in database_file["user_inputs"]:
    #         word_list.append(i['word'])
    #     # return word_list
    #     saved_words = database.get_db_words()
    #     db = database.read()
    #     if word not in saved_words:
    #         result = inputcontroller.spelling(word)
    #         if result == True:
    #             new_entry = {
    #                 "word": word,
    #                 "translation": meaning
    #             }
    #             database.save(new_entry)

    if new_word=="":
        messagebox.showerror(title="Error", message="Word can't be empty", parent=win)
        word.focus()
        return 1

    elif len(new_word.split())!=1:
        messagebox.showwarning(title="Warning", message="Please add a single word", parent=win)
        word.focus()
        return 1

    # elif new_meaning =="":
    #     messagebox.showerror(title="Error", message="Meaning can't be empty", parent=win)
    #     meaning.focus()
    #     return 1

    elif new_word=="Already exist": #backend handle this please
        messagebox.showwarning(title="Warning", message="Word already exists", parent=win)
        word.focus()
        return 1

    elif GermanWords.unknown([new_word]) and GermanWords.correction(new_word) is not None:
        corrected_word = GermanWords.correction(new_word)
        
        res = messagebox.askyesno(title="Spelling mistake", message=f"Do you mean: {corrected_word.capitalize()}", parent=win)
        if res:
            add_word_button["state"] = 'normal'
            add_to_library(corrected_word.capitalize(), new_meaning)
            res = messagebox.askyesno(title="Word added", message=f"{corrected_word.capitalize()} is added to the library.\n\nAdd another word?", parent=win)
            if res:
                word.delete(0, 'end')
                word.focus()
                # meaning.delete(0, 'end')
            else:
                # print("goog")
                add_word_button["state"] = 'normal'
                win.destroy()

        elif GermanWords.candidates(new_word):
            candidates = list(GermanWords.candidates(new_word))
            alt_word_win = tk.Toplevel(win)  # sub-child window of show alternates
            alt_word_win.title("Alternate words")
            alt_word_win.geometry(win.geometry())
            alt_word_win.iconphoto(False, image)

            line = tk.Label(alt_word_win, text=f"The close matches of: {new_word.capitalize()}")
            line.grid(row=1, column=1, columnspan=3, pady=20)

            ok_btn = ttk.Button(alt_word_win, text = 'OK',state='disabled', command = lambda: add_to_library(var.get(),new_meaning))
            def enable_button():
                ok_btn["state"] = 'normal'

            rw=2
            cl=1
            var = tk.StringVar() #a special tk variable to hold the Radiobutton selection it changes dynamically
            for word in candidates:
                ttk.Radiobutton(
                            alt_word_win,
                            text = word.capitalize()+": Meaning",
                            value = word.capitalize(),
                            variable = var,
                            command= enable_button
                        ).grid(row=rw, column=cl, sticky='ew', padx=20, pady=20)
                cl += 1
                if cl==4:
                    rw+=1
                    cl=1


            ok_btn.grid(row=rw+1, column=1, columnspan=3, pady=20)


            alt_word_win.grid_rowconfigure(0, weight=1)
            alt_word_win.grid_rowconfigure(rw+2, weight=1)
            alt_word_win.grid_columnconfigure(0, weight=1)
            alt_word_win.grid_columnconfigure(4, weight=1)

            alt_word_win.mainloop()
        else:
            messagebox.showwarning(title="No more matches", message="No more matches found. Please check the word again", parent=win)

    elif GermanWords.unknown([new_word]) and GermanWords.correction(new_word) is None:
        messagebox.showwarning(title="Word does not exist", message="This word does not exist in the dictionary.\nPlease check the word again",parent=win)

    else:
        meanings = translation(new_word)
        meaning_win = tk.Toplevel(win)  # sub-child window of show alternates
        meaning_win.title("Possible Meanings")
        meaning_win.geometry(win.geometry())
        meaning_win.iconphoto(False, image)

        tkinter_meaning_var = tk.StringVar()

        line = tk.Label(meaning_win, text=f"The possible meanings of: {new_word.capitalize()}")
        line.grid(row=1, column=1, columnspan=3, pady=20)

        ok_btn = ttk.Button(meaning_win, text='OK', state='disabled', command=lambda: add_to_library(new_word, tkinter_meaning_var.get()))

        def enable_button():
            ok_btn["state"] = 'normal'

        rw = 2
        cl = 1
        var = tk.StringVar()  # a special tk variable to hold the Radiobutton selection it changes dynamically
        for word in meanings:
            ttk.Radiobutton(
                meaning_win,
                text=word.capitalize(),
                value=word.capitalize(),
                variable=tkinter_meaning_var,
                command=enable_button
            ).grid(row=rw, column=cl, sticky='ew', padx=20, pady=20)
            cl += 1
            if cl == 4:
                rw += 1
                cl = 1

        ok_btn.grid(row=rw + 1, column=1, columnspan=3, pady=20)

        meaning_win.grid_rowconfigure(0, weight=1)
        meaning_win.grid_rowconfigure(rw + 2, weight=1)
        meaning_win.grid_columnconfigure(0, weight=1)
        meaning_win.grid_columnconfigure(4, weight=1)

        meaning_win.mainloop()






        # add_to_library(new_word.capitalize(), new_meaning)
        # res = messagebox.askyesno(title="Word added", message="Add another word?", parent=win)
        # if res:
        #     word.delete(0, 'end')
        #     word.focus()
        #     meaning.delete(0, 'end')
        # else:
        #     # print("goog")
        #     add_word_button["state"] = 'normal'
        #     win.destroy()


def add_word_window(geom):
    add_word_button["state"]='disabled'
    add_word_win = tk.Toplevel(main_window) #child window of the main_window
    add_word_win.title("Add word")
    add_word_win.geometry(geom)
    add_word_win.iconphoto(False, image)

    word_label = tk.Label(add_word_win, text="New word")
    word_label.grid(row=1, column=1, padx=10, pady=(10,5))
    word_input = ttk.Entry(add_word_win)
    word_input.focus()
    word_input.grid(row=2, column=1, padx=10, pady=(0,25))

    # meaning_label = tk.Label(add_word_win, text="Its meaning")
    # meaning_label.grid(row=3, column=1, padx=10, pady=(0,5))
    # # meaning_input = ttk.Entry(add_word_win, state='readonly')
    # meaning_input = ttk.Entry(add_word_win)
    # meaning_input.grid(row=5, column=1, padx=10, pady=(0,5))


    # Button to close this window and/or handle input
    submit_button = ttk.Button(add_word_win, text="Get meaning", padding=(10,5), command=lambda: [ get_new_word(word_input, add_word_win)]) #add_word_win.destroy()
    submit_button.grid(row=3, column=1, padx=20, pady=20)

    # Manipulate the grid to keep the widgets at the center of teh screen
    add_word_win.grid_rowconfigure(0, weight=1)
    add_word_win.grid_rowconfigure(4, weight=1)
    add_word_win.grid_columnconfigure(1, weight=1)


    def add_word_win_callback():
        add_word_button["state"]='normal'
        add_word_win.destroy()

    add_word_win.protocol("WM_DELETE_WINDOW", add_word_win_callback)
    add_word_win.mainloop()





if __name__ == "__main__":
    main_window = tk.Tk()
    main_window.title("Language Learning Application by Hassam and Zühal")
    main_window.geometry(get_geometry(main_window.winfo_screenwidth(), main_window.winfo_screenheight(), 0, 0,1000, 600))


    # A way around to adjust the widgets at the centre of teh window.
    main_window.grid_rowconfigure(0, weight=1)
    main_window.grid_rowconfigure(2, weight=1)
    main_window.grid_columnconfigure(0, weight=1)
    main_window.grid_columnconfigure(4, weight=1)

    progress = ttk.Progressbar(main_window, orient='horizontal', length=100, mode='determinate')


    #CallBack using protocol #uncomment at the end
    # def main_window_callback():
    #     if messagebox.askokcancel("Quit", "Do you really wish to quit?"):
    #         main_window.destroy()
    #
    # main_window.protocol("WM_DELETE_WINDOW", main_window_callback)


    image = tk.PhotoImage(file="app-icon.png")

    main_window.iconphoto(False, image)

    image_label = ttk.Label(main_window, image=image)
    # image_label.grid(row=1, column=1, columnspan=3, pady=0)
    image_label.grid(row=1, column=2) #btter way

    # styles
    style = ttk.Style()
    # style.theme_use('xpnative') #Windows-XP Theme
    # print(style.theme_use()) #current theme
    style.configure('menu.TButton', font=('Arial', 12))

    #About
    info_Button = ttk.Button(main_window, text="About", padding=(10,2), style='menu.TButton')
    info_Button.place(relx=0, rely=0, anchor="nw", x=10, y=10) #relx and rely = relative-positions (0-1), anchor: of the label


    def change_level(event):
        selected_value = level_var.get()  # Get the selected value from StringVar
        print(f"Selected Level: {selected_value}") #to be impleemted


    levels = ["Niveau: A1", "Niveau: A2", "Niveau: B1", "Niveau: B2"]
    level_var = tk.StringVar()
    # Set a default value for the combobox
    combobox = ttk.Combobox(main_window, values=levels, state="readonly", textvariable=level_var, width=10, height=5, font=("Arial", 12))
    combobox.set("Niveau: A1")  # Set default value
    combobox.place(relx=1, rely=0, anchor="ne", x=-10, y=10)

    # Bind the combobox value change event to the function
    combobox.bind("<<ComboboxSelected>>", change_level)


    MenuBtn1 = ttk.Button(main_window, text="Quiz", width=20, style='menu.TButton')
    MenuBtn1.grid(row=2, column=1, pady=10, padx=10, ipady=20, ipadx=10)

    MenuBtn2 = ttk.Button(main_window, text="MCQs", width=20, style='menu.TButton')
    MenuBtn2.grid(row=2, column=2, pady=10, padx=10, ipady=20, ipadx=10)

    MenuBtn3 = ttk.Button(main_window, text="Articles", width=20, style='menu.TButton')
    MenuBtn3.grid(row=2, column=3, pady=10, padx=10, ipady=20, ipadx=10)

    add_word_button = ttk.Button(main_window, text="Add new word", style='menu.TButton', command=lambda: add_word_window(
        get_geometry(main_window.winfo_width(), main_window.winfo_height(), main_window.winfo_x(),
                     main_window.winfo_y(), 800, 500)))
    add_word_button.grid(row=3, column=2, pady=10, padx=10, ipady=10, ipadx=10, sticky="ew")



    main_window.mainloop()