import tkinter as tk
from tkinter import messagebox,ttk

from datetime import datetime
import random
# import app as main_file


# from spellchecker import SpellChecker
# import spacy
# from deep_translator import PonsTranslator
# ---------------------------------------------------
user_file="user_words.txt"
goethe_file_a1="goethe_a1_words.txt"
def read(file_name):
    with open(file_name, mode="r", encoding="utf-8") as file:
        return file.readlines()
# -------------------------------------------------------
# Timer algorithm every 2, 3, 10, 17, 30 later user will make exercises
def words_to_study(noun_filter=None):
    # database_file = main_file.read(main_file.user_file)
    # goethe_a1_file = main_file.read(main_file.goethe_file_a1)
    database_file = read(user_file)
    goethe_a1_file = read(goethe_file_a1)
    priority_list = []
    normal_list = []
    goethe_list = []

    for line in database_file:
        saved_date = line.split("Date:")[1].split(",")[0].strip()
        today = datetime.now().strftime("%d-%m-%Y")
        time_passed =  datetime.strptime(today, "%d-%m-%Y") - datetime.strptime(saved_date, "%d-%m-%Y")
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


# This part is for games. So we will take count from user
def get_random(count, priority_list, normal_list, goethe_list):
    # Step 1: Select words from priority list
    selected_words = random.sample(priority_list, min(len(priority_list), count)) if priority_list else []

    # Step 2: If there aren't enough words in the priority list, fill with words from normal list
    remaining_count = count - len(selected_words)
    if remaining_count > 0 and normal_list:
        selected_words += random.sample(normal_list, min(len(normal_list), remaining_count)) if normal_list else []

    # Step 3: If there still aren't enough words, fill with words from the goethe list
    remaining_count = count - len(selected_words)
    if remaining_count > 0 and goethe_list:
        selected_words += random.sample(goethe_list, min(len(goethe_list), remaining_count))

    return selected_words


# def der_die_das_game(geom, main_window):
def der_die_das_game(geom):
    # print("Welcome to the Der/Die/Das Game!")
    # Ask user for the number of words they want to practice

    # main_file.article_game_btn["state"]='disabled'
    # der_die_das_win = tk.Toplevel(main_window)
    der_die_das_win = tk.Tk()
    der_die_das_win.title("Der Die Das")
    der_die_das_win.geometry(geom)

    image = tk.PhotoImage(file="app-icon.png")
    der_die_das_win.iconphoto(False, image)

    # main_file.disable_btns(main_window)

    # Variable to store the count
    counts_var = tk.IntVar()

    count = 10
    def get_count(res):
        global count
        count = counts_var.get()
        get_count_win.destroy()


    get_count_win = tk.Toplevel(der_die_das_win)
    get_count_win.geometry('800x500+400+400')
    get_count_win.title("Get Count")

    label = tk.Label(get_count_win, text="Select the number of Nouns")
    label.grid(row=1, column=1, columnspan=3)
    rw = 2
    cl = 1
    for count in [5,10,15]:
        ttk.Radiobutton(
            get_count_win,
            text=count,
            value=count,
            variable=counts_var,
            command=lambda: get_count
        ).grid(row=rw, column=cl, sticky='ew', padx=40, pady=40)
        cl+=1

    get_count_btn = ttk.Button(get_count_win,
                               text="Get count",
                               padding=(10,5),
                               command=lambda:get_count_win.destroy()) #add_word_win.destroy()
    get_count_btn.grid(row=5, column=2)

    get_count_win.grid_rowconfigure(0, weight=1)
    get_count_win.grid_rowconfigure(6, weight=1)
    get_count_win.grid_columnconfigure(0, weight=1)
    get_count_win.grid_columnconfigure(4, weight=1)
    get_count_win.mainloop()


    # def der_die_das_win_callback():
    #     # main_file.enable_btns(main_window)
    #     der_die_das_win.destroy()
    #
    # der_die_das_win.protocol("WM_DELETE_WINDOW", der_die_das_win_callback)
    # der_die_das_win.mainloop()


    # count = int(input("How many words do you want to practice in one session? "))
    priority_list = words_to_study("noun")[0]  # Get only priority words
    normal_list = words_to_study("noun")[1]
    goethe_list = words_to_study("noun")[2]
    total_words = priority_list + normal_list
    while total_words:
        practice_list = get_random(min(count, len(total_words)), priority_list, normal_list, [])
        print(f"Total words selected for this session: {len(practice_list)}")
        for element in practice_list:
            line = element.strip().split(', ')
            word_dict = {pair.split(': ')[0]: pair.split(': ')[1] for pair in line} #convert the line to dictionary
            today = datetime.now().strftime("%d-%m-%Y")
            time_value = word_dict['Date']
            time_passed = datetime.strptime(today, "%d-%m-%Y") - datetime.strptime(time_value, "%d-%m-%Y")

            word = word_dict['Word']
            article = word_dict['Article']
            user_guess = input(f"What is the correct article for '{word}'? (der, die, das): ").lower()
            if user_guess == article:
                print("Correct! Well done.")
                if time_passed in {2, 3, 10, 17, 30}:
                    total_words.remove(element)
                    priority_list.remove(element)
                else:
                    total_words.remove(element)
                    normal_list.remove(element)
            else:
                print(f"Incorrect! The correct article is {article}.")
        cont = input("Do you want to continue to the next session? (yes/no): ").strip().lower()
        if cont != "y":
            print("Thanks for playing! Practice more to be pro!!")
            break
    else:
        # res = messagebox.askyesno(title="Shift to Goethe list", parent=main_file.main_window,
        #                           message=f"You have practiced all words in your list \n Do you want to practice Goethe {main_file.level} list?")
        res= input("do you want Goethe list?")
        if res:
            while goethe_list:
                practice_list = get_random(min(count, len(goethe_list)), [], [], goethe_list)
                print(f"Total words selected for this session: {len(practice_list)}")
                for element in practice_list:
                    line = element.strip().split(', ')
                    print(line)
                    word_dict = {pair.split(': ')[0]: pair.split(': ')[1] for pair in line}  # convert the line to dictionary
                    word = word_dict['Word']
                    article = word_dict['Article']
                    user_guess = input(f"What is the correct article for '{word}'? (der, die, das): ").lower()
                    if user_guess == article:
                        print("Correct! Well done.")
                        goethe_list.remove(element)
                    else:
                        print(f"Incorrect! The correct article is {article}.")
                cont = input("Do you want to continue to the next session? (yes/no): ").strip().lower()
                if cont != "y":
                    print("Thanks for playing! Practice more to be pro!!")
                    break
        else:
            print("All your words done. Well done")

if __name__ == "__main__":
    # the geometry function takes ('widthxHeight+StartX+StartY')
    der_die_das_game('800x500+400+400')

