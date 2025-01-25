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
def der_die_das_game():
    print("Welcome to the Der/Die/Das Game!")
    # Ask user for the number of words they want to practice
    count = int(input("How many words do you want to practice in one session? "))
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
            time_passed = time_passed.days
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
        cont = input("Do you want to continue to the next session? (yes/no): ").lower()
        if cont != "y" and cont != "yes":
            print("Thanks for playing! Practice more to be pro!!")
            break
    else:
        # res = messagebox.askyesno(title="Shift to Goethe list", parent=main_file.main_window,
        #                           message=f"You have practiced all words in your list \n Do you want to practice Goethe {main_file.level} list?")
        res = input("do you want Goethe list (yes/no)?").strip().lower()
        if res =="y" or res == "yes":
            while goethe_list:
                practice_list = get_random(min(count, len(goethe_list)), [], [], goethe_list)
                print(f"Total words selected for this session: {len(practice_list)}")
                for element in practice_list:
                    line = element.strip().split(', ')
                    word_dict = {pair.split(': ')[0]: pair.split(': ')[1] for pair in line}  # convert the line to dictionary
                    word = word_dict['Word']
                    article = word_dict['Article']
                    user_guess = input(f"What is the correct article for '{word}'? (der, die, das): ").lower()
                    if user_guess == article:
                        print("Correct! Well done.")
                        goethe_list.remove(element)
                    else:
                        print(f"Incorrect! The correct article is {article}.")
                cont = input("Do you want to continue to the next session? (yes/no): ").lower()
                if cont != "y" and cont != "yes":
                    print("Thanks for playing! Practice more to be pro!!")
                    break
            else:
                print("All goethe words also done. Well done")
        if cont != "y":
            print("Thanks for playing! Practice more to be pro!!")
if __name__ == "__main__":
    # the geometry function takes ('widthxHeight+StartX+StartY')
    der_die_das_game()

