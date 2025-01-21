from datetime import datetime
import random


def read(file_name):
    with open(file_name, mode="r", encoding="utf-8") as file:
        return file.readlines()


# Timer algorithm every 2, 3, 10, 17, 30 later user will make exercises
def words_to_study():
    database_file = read("user_inputs.txt")
    today = datetime.now().timetuple().tm_yday
    word_list = []
    for line in database_file:
        if "time:" in line:
            time_value = int(line.split("time:")[1].split(",")[0].strip())
            time_passed = today - time_value
            if time_passed in {2, 3, 10, 17, 30}:
                word_list.append(line)
    return word_list


# This part is for games. So we will take count from user
def get_random(count):
    words = words_to_study()
    if len(words) < count:
        return f"Your list is not that much long maybe you could learn some A1 word"
    return random.sample(words, count)


def der_die_das_game():
    print("Welcome to the Der/Die/Das Game!")
    count = int(input("How many words do you want to practice in one session? "))

    all_words = words_to_study()
    total_words = len(all_words)

    while total_words:
        # count_session = min(count,count-index)
        practice_list = random.sample(all_words, min(len(all_words),count))
        print(len(practice_list))
        for element in practice_list:
            word_info = element.strip().split(", ")
            word_type = [info.split(": ")[1] for info in word_info if info.startswith("type:")][0]
            if word_type == "NOUN":
                noun = [info.split(": ")[1] for info in word_info if info.startswith("word:")][0]
                article = [info.split(": ")[1] for info in word_info if info.startswith("gender:")][0]
                user_guess = input(f"What is the correct article for '{noun}'? (der, die, das): ").lower()
                if user_guess == article:
                    all_words.remove(element)
                    print("Correct! Well done.")
                else:
                    print(f"Incorrect! The correct article is {article}.")
        print(len(all_words))

        cont = input("Do you want to continue to the next session? (yes/no): ").strip().lower()
        print(cont)
        if cont != "y":
            print("Thanks for playing! Practice more to be pro !!")
            break
    else:
        print("You've practiced all available words! Great job.")


if __name__ == "__main__":
    der_die_das_game()
