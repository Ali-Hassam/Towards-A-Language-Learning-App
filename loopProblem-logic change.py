from datetime import datetime
import random
###Problems Solved


def read(file_name):
    with open(file_name, mode="r", encoding="utf-8") as file:
        return file.readlines()


# Timer algorithm every 2, 3, 10, 17, 30 later user will make exercises
def words_to_study(noun_filter=None):
    database_file = read("user_inputs.txt")
    today = datetime.now().timetuple().tm_yday
    priority_list = []
    normal_list = []

    for line in database_file:
        if "time:" in line:
            time_value = int(line.split("time:")[1].split(",")[0].strip())
            time_passed = today - time_value
            word_info = line.strip().split(", ")
            word_type = [info.split(": ")[1] for info in word_info if info.startswith("type:")][0]
            if noun_filter == "noun" and word_type == "NOUN":
                if time_passed in {2, 3, 10, 17, 30}:
                    priority_list.append(line)
                else:
                    normal_list.append(line)
            elif noun_filter is None:
                if time_passed in {2, 3, 10, 17, 30}:
                    priority_list.append(line)
                else:
                    normal_list.append(line)


    return priority_list, normal_list


def get_random(count, priority_list, normal_list):
    selected_words = random.sample(priority_list, min(len(priority_list), count))
    # If there aren't enough in the priority list, fill with words from normal list
    remaining_count = count - len(selected_words)
    if remaining_count > 0:
        selected_words += random.sample(normal_list, remaining_count)

    return selected_words


def der_die_das_game():
    print("Welcome to the Der/Die/Das Game!")

    # Ask user for the number of words they want to practice
    count = int(input("How many words do you want to practice in one session? "))

    priority_list = words_to_study("noun")[0]  # Get only priority words
    normal_list = words_to_study("noun")[1]  # Get teh rest fo the words
    total_words = priority_list + normal_list

    while total_words:
        practice_list = get_random(min(count,len(total_words)), priority_list, normal_list)
        print(f"Total words selected for this session: {len(practice_list)}")
        for element in practice_list:
            line = element.strip().split(', ')
            word_dict = {pair.split(': ')[0]: pair.split(': ')[1] for pair in line}

            time_value = int (word_dict['time'])
            today = datetime.now().timetuple().tm_yday
            time_passed = today - time_value
            word = word_dict['word']
            article = word_dict['gender']
            user_guess = input(f"What is the correct article for '{word}'? (der, die, das): ").lower()
            if user_guess == article:
                print("Correct! Well done.")
                if time_passed in{2, 3, 10, 17, 30}:
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
        print("You've practiced all available words! Great job.")


if __name__ == "__main__":
    der_die_das_game()
    # x,y = words_to_study('noun')
    # # for i in x:
    # #     print (i)
    #
    # z = get_random(5,x,y)
    # for i  in z:
    #     print(i)