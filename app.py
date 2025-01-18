import math
import tkinter as tk
from tkinter import messagebox,ttk
from tkinter.constants import DISABLED, NORMAL

import json
from spellchecker import SpellChecker


GermanWords = SpellChecker(language='de')
EnglishWords= SpellChecker(language='en')
db_file="database.json"

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

def read():
    with open(db_file, mode="r", encoding="utf-8") as read_file:
        return json.load(read_file)


def save(word):
    data = read()
    data["user_inputs"].append(word)
    with open(db_file, mode="w", encoding="utf-8") as write_file:
        json.dump(data, write_file, ensure_ascii=False, indent=4)

def get_words():
    database_file = read()
    word_list = []
    for i in database_file["user_inputs"]:
        word_list.append(i['word'])
    return word_list


# -------------------------------------------------------------



# Add the new word to the custom library
def add_to_library(new_word, meaning):
    add_word_button["state"]=NORMAL
    # Zuhal Please implement/modify the function to add the word into the library (text or JSON file) here
    saved_words = get_words()
    if new_word not in saved_words:
        new_entry = {
                    "word": new_word,
                    "meaning": meaning.capitalize()
                    }
        save(new_entry)
        messagebox.showinfo(title="Word added", message=f"{new_word} added to the library")
    else:
        messagebox.showinfo(title="Word added", message=f"{new_word} already exist the library")



# Get a new word from user
## To many checks , optimization required may be "try:catch"
def get_new_word(word, meaning, win):
    new_word = word.get().lower()
    new_meaning = meaning.get().lower()

    # with open(db_file, mode="r", encoding="utf-8") as read_file:
    #     database_file = json.load(read_file)
    #     word_list = []
    #     for i in database_file["user_inputs"]:
    #         word_list.append(i['word'])
    #     # return word_list
    #     saved_words = database.get_words()
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

    elif new_meaning =="":
        messagebox.showerror(title="Error", message="Meaning can't be empty", parent=win)
        meaning.focus()
        return 1

    elif new_word=="Already exist": #backend handle this please
        messagebox.showwarning(title="Warning", message="Word already exists", parent=win)
        word.focus()
        return 1

    elif len(new_word.split())!=1:
        messagebox.showwarning(title="Warning", message="Please add a single word", parent=win)
        word.focus()
        return 1

    elif GermanWords.unknown([new_word]) and GermanWords.correction(new_word) is not None:
        corrected_word = GermanWords.correction(new_word)
        res = messagebox.askyesno(title="Spelling mistake", message=f"Do you mean: {corrected_word.capitalize()}", parent=win)
        if res:
            add_word_button["state"] = NORMAL
            add_to_library(corrected_word.capitalize(), new_meaning)
            res = messagebox.askyesno(title="Word added", message=f"{corrected_word.capitalize()} is added to the library.\n\nAdd another word?", parent=win)
            if res:
                word.delete(0, 'end')
                word.focus()
                meaning.delete(0, 'end')
            else:
                # print("goog")
                add_word_button["state"] = NORMAL
                win.destroy()

        elif GermanWords.candidates(new_word):
            candidates = list(GermanWords.candidates(new_word))
            alt_word_win = tk.Toplevel(win)  # sub-child window of show alternates
            alt_word_win.title("Alternate words")
            alt_word_win.geometry(win.geometry())

            line = tk.Label(alt_word_win, text=f"The close matches of: {new_word.capitalize()}")
            line.grid(row=1, column=1, columnspan=3, pady=20)

            ok_btn = ttk.Button(alt_word_win, text = 'OK',state=DISABLED, command = lambda: add_to_library(var.get(),new_meaning))
            def enable_button():
                ok_btn["state"] = NORMAL

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
        add_to_library(new_word.capitalize(), new_meaning)
        res = messagebox.askyesno(title="Word added", message="Add another word?", parent=win)
        if res:
            word.delete(0, 'end')
            word.focus()
            meaning.delete(0, 'end')
        else:
            # print("goog")
            add_word_button["state"] = NORMAL
            win.destroy()


def add_word_window(geom):
    add_word_button["state"]=DISABLED
    add_word_win = tk.Toplevel(main_window) #child window of the main_window
    add_word_win.title("Add word")
    add_word_win.geometry(geom)

    word_label = tk.Label(add_word_win, text="New word")
    word_label.grid(row=1, column=1, padx=10, pady=(10,5))
    word_input = ttk.Entry(add_word_win)
    word_input.focus()
    word_input.grid(row=2, column=1, padx=10, pady=(0,25))

    meaning_label = tk.Label(add_word_win, text="Its meaning")
    meaning_label.grid(row=3, column=1, padx=10, pady=(0,5))
    meaning_input = ttk.Entry(add_word_win)
    meaning_input.grid(row=5, column=1, padx=10, pady=(0,5))


    # Button to close this window and/or handle input
    submit_button = ttk.Button(add_word_win, text="Add word", command=lambda: [get_new_word(word_input, meaning_input, add_word_win)]) #add_word_win.destroy()
    submit_button.grid(row=6, column=1, padx=20, pady=20)

    # Manipulate the grid to keep the widgets at the center of teh screen
    add_word_win.grid_rowconfigure(0, weight=1)
    add_word_win.grid_rowconfigure(7, weight=1)
    add_word_win.grid_columnconfigure(1, weight=1)


    def add_word_win_callback():
        add_word_button["state"]=NORMAL
        add_word_win.destroy()

    add_word_win.protocol("WM_DELETE_WINDOW", add_word_win_callback)
    add_word_win.mainloop()





if __name__ == "__main__":
    main_window = tk.Tk()
    main_window.title("Language Learning Application by Hassam and Zühal")
    main_window.geometry(get_geometry(main_window.winfo_screenwidth(), main_window.winfo_screenheight(), 0, 0,1000, 600))

    add_word_button = ttk.Button(main_window, text="Add new word", command=lambda:add_word_window(get_geometry(main_window.winfo_width(), main_window.winfo_height(), main_window.winfo_x(),main_window.winfo_y(), 800, 500)))
    add_word_button.place(relx=0, rely=0, anchor="nw", x=10, y=10) #relx and rely = relative-positions (0-1), anchor: of the label

    # def main_window_callback():
    #     if messagebox.askokcancel("Quit", "Do you really wish to quit?"):
    #         main_window.destroy()
    #
    # main_window.protocol("WM_DELETE_WINDOW", main_window_callback)

    main_window.mainloop()