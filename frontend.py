import tkinter as tk

def get_geometry(screen_width, screen_height, window_width, window_height):
    # Calculate Start X and Y coordinates
    x = (screen_width / 2) - (window_width / 2)
    y = (screen_height / 2) - (window_height / 2)
    geometry = '%dx%d+%d+%d' % (window_width, window_height, x, y)
    return geometry  # the geometry function takes ('widthxHeight+StartX+StartY')

def get_new_word(new_word, meaning):
    new_word = new_word.get()
    meaning = meaning.get()
    print(new_word, meaning)


def add_word_window(screen_width, Screen_height):
    add_word_win = tk.Toplevel(main_window)
    add_word_win.title("Add Word")
    add_word_win.geometry(get_geometry(screen_width, screen_height, 600, 300))

    word_label = tk.Label(add_word_win, text="New Word")
    word_label.pack(pady=10)
    word_input = tk.Entry(add_word_win)
    word_input.pack(pady=5)

    meaning_label = tk.Label(add_word_win, text="Its Meaning")
    meaning_label.pack(pady=10)
    meaning_input = tk.Entry(add_word_win)
    meaning_input.pack(pady=5)

    # Button to close this window and/or handle input
    submit_button = tk.Button(add_word_win, text="Submit", command=lambda: [get_new_word(word_input, meaning_input), add_word_win.destroy()])
    submit_button.pack(pady=10)
    add_word_win.mainloop()


if __name__ == "__main__":
    main_window = tk.Tk()
    main_window.title("Language Learning Application")
    screen_width = main_window.winfo_screenwidth()
    screen_height = main_window.winfo_screenheight()
    main_window.geometry(get_geometry(screen_width, screen_height, 1000, 600))

    add_word_button = tk.Button(main_window, text="Add Word", command=lambda:add_word_window(screen_width,screen_height))
    add_word_button.place(relx=0, rely=0, anchor="nw", x=10, y=10) #relx and rely = relative-positions (0-1), anchor: of the label
    main_window.mainloop()