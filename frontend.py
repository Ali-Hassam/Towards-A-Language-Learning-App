import tkinter as tk
from tkinter import messagebox,ttk


# Get the geometry of the windows
def get_geometry(parent_width, parent_height, parent_x, parent_y, window_width, window_height):
    x = int(parent_x + (parent_width / 2) - (window_width / 2))
    y = int(parent_y + (parent_height / 2) - (window_height / 2))
    # the geometry function takes ('widthxHeight+StartX+StartY')
    # geometry = '%dx%d+%d+%d' % (window_width, window_height, x, y)
    geometry = f"{window_width}x{window_height}+{x}+{y}"
    return geometry

# A custom messagebox
def message_box(message, window):
    # messagebox.showerror(title=None, message=message, parent=window, type='abortretryignore', default="retry")
    messagebox.showerror(title="Error", message=message, parent=window)
    messagebox.askquestion(title="Add Another Word", message="Add another word?", parent=window)


# Get a new word from user
def get_new_word(word, meaning, win):
    new_word = word.get()
    new_meaning = meaning.get()
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
    elif new_word == "Spelling mistake":  # backend handle this please
        messagebox.showwarning(title="Spelling mistake", message="Please check spellings of the word", parent=win)
        word.focus()
        return 1
    elif new_meaning=="Spelling mistake": #backend handle this please
        messagebox.showwarning(title="Spelling mistake", message="Please check spellings of the meaning", parent=win)
        meaning.focus()
        return 1
    else:
        res = messagebox.askyesno(title="Word added", message=f"{new_word} is added to the library.\n\nAdd another word?", parent=win)
        if res:
            word.delete(0, 'end')
            word.focus()
            meaning.delete(0, 'end')
        else:
            win.destroy()



def add_word_window(geom):
    add_word_win = tk.Toplevel(main_window) #child window of the main_window
    add_word_win.title("Add Word")
    # add_word_win.geometry(get_geometry(screen_width, screen_height, 600, 300))
    add_word_win.geometry(geom)

    word_label = tk.Label(add_word_win, text="New Word")
    word_label.pack(pady=5)
    word_input = ttk.Entry(add_word_win)
    word_input.focus()
    word_input.pack(pady=(5,25))

    meaning_label = tk.Label(add_word_win, text="Its Meaning")
    meaning_label.pack(pady=5)
    meaning_input = ttk.Entry(add_word_win)
    meaning_input.pack(pady=(5,10))

    # Button to close this window and/or handle input
    #submit_button = ttk.Button(add_word_win, text="Add Word", command=lambda: [print("Problem1") if get_new_word(word_input, meaning_input, add_word_win)==1 else print("No Problem")]) #add_word_win.destroy()
    submit_button = ttk.Button(add_word_win, text="Add Word", command=lambda: [get_new_word(word_input, meaning_input, add_word_win)]) #add_word_win.destroy()
    submit_button.pack(pady=10)
    add_word_win.mainloop()





if __name__ == "__main__":
    main_window = tk.Tk()
    main_window.title("Language Learning Application by Hassam and Zühal")
    main_window.geometry(get_geometry(main_window.winfo_screenwidth(), main_window.winfo_screenheight(), 0, 0,1000, 600))

    add_word_button = ttk.Button(main_window, text="Add New Word", command=lambda:add_word_window(get_geometry(main_window.winfo_width(), main_window.winfo_height(), main_window.winfo_x(),main_window.winfo_y(), 400, 200)))
    add_word_button.place(relx=0, rely=0, anchor="nw", x=10, y=10) #relx and rely = relative-positions (0-1), anchor: of the label

    main_window.mainloop()